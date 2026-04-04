"""Full-text retrieval cascade: PMC XML → Unpaywall PDF → S2 PDF.

Fetches and caches full text for scientific articles by DOI.
PMC provides structured JATS XML with named sections.
Unpaywall and S2 provide PDF URLs requiring pdftext extraction.
"""

import io
import re
import sys
import xml.etree.ElementTree as ET

from .http import (
    OA_CLIENT,
    S2_CLIENT,
    _CLIENT,
    _EMAIL,
    ncbi_params,
    request_with_retry,
    s2_throttle,
)

_cache: dict[str, dict] = {}

_SECTION_ALIASES = {
    "introduction": ["introduction", "background", "intro"],
    "methods": [
        "methods",
        "materials and methods",
        "material and methods",
        "patients and methods",
        "experimental procedures",
        "study design",
        "methodology",
    ],
    "results": ["results", "findings"],
    "discussion": ["discussion", "comment", "interpretation"],
    "conclusion": ["conclusion", "conclusions", "summary"],
    "abstract": ["abstract"],
}


def _normalize_section(title: str) -> str | None:
    t = title.strip().lower()
    for canonical, aliases in _SECTION_ALIASES.items():
        if t in aliases:
            return canonical
    return None


def _parse_jats_xml(xml_bytes: bytes) -> dict[str, str]:
    root = ET.fromstring(xml_bytes)

    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"

    sections: dict[str, str] = {}

    for abstract_el in root.iter(f"{ns}abstract"):
        sections["abstract"] = " ".join(abstract_el.itertext()).strip()

    body = root.find(f".//{ns}body")
    if body is None:
        flat = " ".join(root.itertext()).strip()
        if flat and "abstract" not in sections:
            sections["full"] = flat
        return sections

    sec_elements = body.findall(f"{ns}sec")
    if not sec_elements:
        sections["full"] = " ".join(body.itertext()).strip()
        return sections

    for sec in sec_elements:
        title_el = sec.find(f"{ns}title")
        if title_el is None:
            continue
        raw_title = " ".join(title_el.itertext()).strip()
        canonical = _normalize_section(raw_title)
        text = " ".join(sec.itertext()).strip()
        if text.startswith(raw_title):
            text = text[len(raw_title) :].strip()
        key = canonical or raw_title.lower()
        sections[key] = text

    all_text_parts = []
    for key in [
        "abstract",
        "introduction",
        "methods",
        "results",
        "discussion",
        "conclusion",
    ]:
        if key in sections:
            all_text_parts.append(sections[key])
    for key, text in sections.items():
        if key not in {
            "abstract",
            "introduction",
            "methods",
            "results",
            "discussion",
            "conclusion",
            "full",
        }:
            all_text_parts.append(text)
    if all_text_parts:
        sections["full"] = "\n\n".join(all_text_parts)

    return sections


def _doi_to_pmcid(doi: str) -> str | None:
    url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
    params = ncbi_params({"ids": doi, "format": "json"})
    try:
        resp = request_with_retry("GET", url, params=params)
        data = resp.json()
        records = data.get("records", [])
        if records and records[0].get("pmcid"):
            return records[0]["pmcid"]
    except Exception as e:
        print(f"  PMCID lookup failed for {doi}: {e}", file=sys.stderr)
    return None


def _fetch_pmc_xml(pmcid: str) -> bytes | None:
    numeric = pmcid.replace("PMC", "")
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = ncbi_params({"db": "pmc", "id": numeric, "rettype": "xml"})
    try:
        resp = request_with_retry("GET", url, params=params, timeout=30)
        if resp.status_code == 200 and b"<" in resp.content[:100]:
            return resp.content
    except Exception as e:
        print(f"  PMC fetch failed for {pmcid}: {e}", file=sys.stderr)
    return None


def _fetch_via_pmc(doi: str) -> dict[str, str] | None:
    pmcid = _doi_to_pmcid(doi)
    if not pmcid:
        return None
    xml_bytes = _fetch_pmc_xml(pmcid)
    if not xml_bytes:
        return None
    try:
        return _parse_jats_xml(xml_bytes)
    except ET.ParseError as e:
        print(f"  JATS parse error for {pmcid}: {e}", file=sys.stderr)
        return None


def _unpaywall_pdf_url(doi: str) -> str | None:
    url = f"https://api.unpaywall.org/v2/{doi}"
    params = {"email": _EMAIL}
    try:
        resp = request_with_retry("GET", url, params=params)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if not data.get("is_oa"):
            return None
        for loc in data.get("oa_locations", []):
            pdf = loc.get("url_for_pdf")
            if pdf:
                return pdf
        best = data.get("best_oa_location") or {}
        return best.get("url_for_pdf") or best.get("url")
    except Exception as e:
        print(f"  Unpaywall lookup failed for {doi}: {e}", file=sys.stderr)
    return None


def _s2_pdf_url(doi: str) -> str | None:
    s2_throttle()
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
    params = {"fields": "openAccessPdf,isOpenAccess"}
    try:
        resp = request_with_retry("GET", url, params=params, client=S2_CLIENT)
        if resp.status_code != 200:
            return None
        data = resp.json()
        oa_pdf = data.get("openAccessPdf")
        if oa_pdf and oa_pdf.get("url"):
            return oa_pdf["url"]
    except Exception as e:
        print(f"  S2 PDF lookup failed for {doi}: {e}", file=sys.stderr)
    return None


def _extract_text_from_pdf(pdf_bytes: bytes) -> str | None:
    try:
        from pdftext.extraction import plain_text_output
    except ImportError:
        print("  pdftext not installed — cannot extract PDF text", file=sys.stderr)
        return None

    try:
        text = plain_text_output(io.BytesIO(pdf_bytes))
        if isinstance(text, list):
            text = "\n\n".join(text)
        return text.strip() if text else None
    except Exception as e:
        print(f"  PDF text extraction failed: {e}", file=sys.stderr)
        return None


def _download_pdf(url: str) -> bytes | None:
    try:
        resp = request_with_retry("GET", url, client=OA_CLIENT, timeout=60)
        if resp.status_code == 200 and len(resp.content) > 1000:
            if resp.content[:5] == b"%PDF-" or b"%PDF-" in resp.content[:1024]:
                return resp.content
    except Exception as e:
        print(f"  PDF download failed from {url}: {e}", file=sys.stderr)
    return None


def _fetch_via_pdf(doi: str) -> dict[str, str] | None:
    pdf_url = _unpaywall_pdf_url(doi)
    if not pdf_url:
        pdf_url = _s2_pdf_url(doi)
    if not pdf_url:
        return None

    pdf_bytes = _download_pdf(pdf_url)
    if not pdf_bytes:
        return None

    text = _extract_text_from_pdf(pdf_bytes)
    if not text:
        return None

    return {"full": text}


def fetch_and_cache(doi: str) -> dict:
    doi_lower = doi.lower().strip()

    if doi_lower in _cache:
        entry = _cache[doi_lower]
        return {
            "doi": doi,
            "source": entry["source"],
            "word_count": entry["word_count"],
            "sections": list(entry["sections"].keys()),
            "cached": True,
        }

    sections = _fetch_via_pmc(doi)
    source = "pmc"

    if not sections:
        sections = _fetch_via_pdf(doi)
        source = "pdf"

    if not sections:
        return {"doi": doi, "error": "No full text found via PMC, Unpaywall, or S2."}

    full_text = sections.get("full", "")
    word_count = (
        len(full_text.split())
        if full_text
        else sum(len(t.split()) for t in sections.values())
    )

    _cache[doi_lower] = {
        "source": source,
        "sections": sections,
        "word_count": word_count,
    }

    return {
        "doi": doi,
        "source": source,
        "word_count": word_count,
        "sections": list(sections.keys()),
        "cached": False,
    }


def get_cached_section(doi: str, section: str, max_chars: int) -> dict:
    doi_lower = doi.lower().strip()

    if doi_lower not in _cache:
        return {"doi": doi, "error": "Not cached. Call fetch_fulltext first."}

    entry = _cache[doi_lower]
    sections = entry["sections"]

    if section == "full":
        text = sections.get("full", "")
    else:
        canonical = _normalize_section(section)
        key = canonical or section.lower()
        text = sections.get(key, "")

    if not text:
        available = [k for k in sections.keys() if k != "full"]
        return {
            "doi": doi,
            "section": section,
            "error": f"Section not found. Available: {available}",
        }

    truncated = len(text) > max_chars
    if truncated:
        text = text[:max_chars]

    return {
        "doi": doi,
        "section": section,
        "text": text,
        "char_count": len(text),
        "truncated": truncated,
        "source": entry["source"],
    }


def clear_cache() -> int:
    n = len(_cache)
    _cache.clear()
    return n
