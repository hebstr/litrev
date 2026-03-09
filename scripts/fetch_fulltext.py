#!/usr/bin/env python3
"""
Fetch full-text articles and extract numerical claims.

Cascade: PMC → Unpaywall → Publisher → Sci-Hub.
Enriches extracted_claims.json with claims from full-text for articles
that could not be verified from abstracts alone.

The Publisher source works automatically when a VPN provides institutional
access. No configuration needed — just connect to your university VPN.

Usage:
    python fetch_fulltext.py review/claims_audit.json \
        --extraction review/extracted_claims.json \
        --bib review/references.bib \
        --output review/extracted_claims.json

    python fetch_fulltext.py \
        --dois 10.1097/GME.0b013e31829638e3 \
        --extraction review/extracted_claims.json \
        --output review/extracted_claims.json
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from typing import Any
from urllib.parse import quote

import requests

sys.path.insert(0, os.path.dirname(__file__))
from bibtex_keys import parse_bib_keys_to_doi as _parse_bib_keys_to_doi
from claim_patterns import extract_claims as _extract_claims
from http_utils import request_with_retry as _request_with_retry


SCIHUB_MIRRORS = [
    "https://sci-hub.ru",
    "https://sci-hub.st",
    "https://sci-hub.se",
]

PDF_URL_PATTERN = re.compile(
    r'citation_pdf_url"\s+content="([^"]+)"'
)

ELINK_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
UNPAYWALL_URL = "https://api.unpaywall.org/v2"
DEFAULT_EMAIL = "literature-review-skill@example.com"
DOI_RESOLVER = "https://doi.org"

_BROWSER_SESSION = requests.Session()
_BROWSER_SESSION.headers.update({"User-Agent": "LiteratureReviewSkill/1.0"})


# --- Source 1: PubMed Central (PMC) ---

def doi_to_pmcid(doi: str, email: str = DEFAULT_EMAIL) -> str | None:
    try:
        response = _request_with_retry(
            "GET",
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            params={"db": "pubmed", "term": f"{doi}[doi]", "retmode": "json"},
            timeout=10,
        )
        data = response.json()
        pmids = data.get("esearchresult", {}).get("idlist", [])
        if not pmids:
            return None

        response = _request_with_retry(
            "GET", ELINK_URL,
            params={
                "dbfrom": "pubmed",
                "db": "pmc",
                "id": pmids[0],
                "linkname": "pubmed_pmc",
                "retmode": "json",
                "tool": "LiteratureReviewSkill",
                "email": email,
            },
            timeout=10,
        )
        link_data = response.json()

        linksets = link_data.get("linksets", [])
        for ls in linksets:
            for ldb in ls.get("linksetdbs", []):
                if ldb.get("dbto") == "pmc":
                    links = ldb.get("links", [])
                    if links:
                        return links[0]
    except (requests.RequestException, ValueError, KeyError, json.JSONDecodeError) as e:
        print(f"  PMC ID lookup failed for {doi}: {e}", file=sys.stderr)
    return None


def fetch_pmc_text(pmcid: str, email: str = DEFAULT_EMAIL) -> str | None:
    try:
        response = _request_with_retry(
            "GET", EFETCH_URL,
            params={
                "db": "pmc",
                "id": pmcid,
                "rettype": "xml",
                "retmode": "xml",
                "tool": "LiteratureReviewSkill",
                "email": email,
            },
            timeout=30,
        )
        response.raise_for_status()
        root = ET.fromstring(response.text)  # safe: CPython expat doesn't resolve external entities (no XXE)
        texts = []
        for body in root.findall(".//body"):
            texts.append("".join(body.itertext()))
        if not texts:
            for abstract in root.findall(".//abstract"):
                texts.append("".join(abstract.itertext()))
        return " ".join(texts) if texts else None
    except (requests.RequestException, ET.ParseError) as e:
        print(f"  PMC text fetch failed for {pmcid}: {e}", file=sys.stderr)
        return None


def try_pmc(doi: str, email: str = DEFAULT_EMAIL) -> tuple[str | None, str]:
    pmcid = doi_to_pmcid(doi, email=email)
    if not pmcid:
        return None, "no PMC link"
    text = fetch_pmc_text(pmcid, email=email)
    if text and len(text) > 500:
        return text, f"PMC:{pmcid}"
    return None, "PMC text too short or empty"


# --- Source 2: Unpaywall ---

def try_unpaywall(doi: str, email: str = DEFAULT_EMAIL) -> tuple[str | None, str]:
    url = f"{UNPAYWALL_URL}/{quote(doi, safe='')}?email={email}"
    try:
        response = _request_with_retry("GET", url, timeout=10)
        data = response.json()
    except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
        return None, f"Unpaywall API error: {e}"

    best_oa = data.get("best_oa_location")
    if not best_oa:
        return None, "no OA version"

    pdf_url = best_oa.get("url_for_pdf") or best_oa.get("url")
    if not pdf_url:
        return None, "no OA URL"

    return pdf_url, "unpaywall"


# --- Source 3: Publisher (works transparently with VPN) ---

def try_publisher(doi: str, tmpdir: str, index: int) -> tuple[str | None, str]:
    url = f"{DOI_RESOLVER}/{doi}"
    try:
        response = _request_with_retry(
            "GET", url,
            session=_BROWSER_SESSION,
            headers={"Accept": "application/pdf"},
            timeout=30,
            allow_redirects=True,
        )
        if response.status_code != 200:
            return None, f"publisher HTTP {response.status_code}"
        content_type = response.headers.get("Content-Type", "")
        if "pdf" in content_type:
            pdf_path = os.path.join(tmpdir, f"article_{index}.pdf")
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            if os.path.getsize(pdf_path) > 1000:
                text = pdf_to_text(pdf_path)
                os.unlink(pdf_path)
                if text:
                    return text, "publisher"
    except (requests.RequestException, OSError) as e:
        print(f"  Publisher access failed for {doi}: {e}", file=sys.stderr)
    return None, "publisher access denied"


# --- Source 4: Sci-Hub ---

def find_working_mirror() -> str | None:
    for mirror in SCIHUB_MIRRORS:
        try:
            response = _BROWSER_SESSION.get(mirror, timeout=10)
            if response.status_code == 200:
                return mirror
        except requests.RequestException:
            continue
    return None


def try_scihub(doi: str, mirror: str) -> tuple[str | None, str]:
    url = f"{mirror}/{doi}"
    try:
        response = _BROWSER_SESSION.get(url, timeout=20)
        html = response.text
        m = PDF_URL_PATTERN.search(html)
        if m:
            pdf_url = m.group(1)
            if pdf_url.startswith("//"):
                pdf_url = "https:" + pdf_url
            return pdf_url, "sci-hub"
    except requests.RequestException as e:
        return None, f"sci-hub error: {e}"
    return None, "no PDF on sci-hub"


# --- PDF handling ---

_PDF_MAGIC = b"%PDF"
_PDF_MAX_SIZE = 100_000_000


def download_pdf(pdf_url: str, output_path: str) -> bool:
    try:
        response = _request_with_retry(
            "GET", pdf_url, session=_BROWSER_SESSION, timeout=30, stream=True,
        )
        if response.status_code != 200:
            return False
        size = 0
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(8192):
                size += len(chunk)
                if size > _PDF_MAX_SIZE:
                    return False
                f.write(chunk)
        if size < 1000:
            return False
        with open(output_path, "rb") as f:
            if not f.read(4).startswith(_PDF_MAGIC):
                os.unlink(output_path)
                return False
        return True
    except (requests.RequestException, OSError):
        return False


def pdf_to_text(pdf_path: str) -> str:
    # pdf_path is always os.path.join(tmpdir, f"article_{int}.pdf") — no user input reaches argv
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", pdf_path, "-"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout
    except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
        print(f"  pdftotext failed for {pdf_path}: {e}", file=sys.stderr)
        return ""


def extract_claims_from_text(text: str, source: str = "fulltext") -> list[dict[str, str]]:
    return _extract_claims(text, source=source)


# --- Orchestration ---

def fetch_article_text(
    doi: str,
    tmpdir: str,
    index: int,
    scihub_mirror: str | None,
    email: str = DEFAULT_EMAIL,
) -> tuple[str, str]:
    text, source = try_pmc(doi, email=email)
    if text:
        return text, "pmc"

    pdf_url, source = try_unpaywall(doi, email=email)
    if pdf_url:
        pdf_path = os.path.join(tmpdir, f"article_{index}.pdf")
        if download_pdf(pdf_url, pdf_path):
            text = pdf_to_text(pdf_path)
            os.unlink(pdf_path)
            if text:
                return text, "unpaywall"
            print(f"  Unpaywall PDF downloaded but text extraction failed (scanned?)", file=sys.stderr)

    text, source = try_publisher(doi, tmpdir, index)
    if text:
        return text, "publisher"

    if scihub_mirror:
        pdf_url, source = try_scihub(doi, scihub_mirror)
        if pdf_url:
            pdf_path = os.path.join(tmpdir, f"article_{index}.pdf")
            if download_pdf(pdf_url, pdf_path):
                text = pdf_to_text(pdf_path)
                os.unlink(pdf_path)
                if text:
                    return text, "sci-hub"
                print(f"  Sci-Hub PDF downloaded but text extraction failed (scanned?)", file=sys.stderr)

    return "", "not found"


def get_unverified_dois(
    audit_path: str,
    bib_dois: dict[str, str],
) -> list[tuple[str, str]]:
    with open(audit_path, "r", encoding="utf-8") as f:
        audit = json.load(f)

    doi_keys: list[tuple[str, str]] = []
    seen_dois: set[str] = set()

    for claim in audit.get("claims", []):
        if claim.get("status") != "UNVERIFIED":
            continue
        key = claim["citation_key"]
        doi = bib_dois.get(key, "")
        if doi and doi.lower() not in seen_dois:
            seen_dois.add(doi.lower())
            doi_keys.append((doi, key))

    return doi_keys


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch full-text articles and extract claims. "
        "Tries PMC and Unpaywall first, then Sci-Hub as fallback."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("audit", nargs="?", help="Path to claims_audit.json")
    group.add_argument("--dois", nargs="+", help="DOIs to fetch directly")
    parser.add_argument(
        "--extraction",
        default="review/extracted_claims.json",
        help="Path to extracted_claims.json to enrich",
    )
    parser.add_argument(
        "--bib",
        default="review/references.bib",
        help="Path to references.bib",
    )
    parser.add_argument(
        "--output",
        help="Output path (default: overwrite --extraction)",
    )
    parser.add_argument(
        "--mirror",
        help="Sci-Hub mirror URL (auto-detected if not set)",
    )
    parser.add_argument(
        "--email",
        help="Email for Unpaywall API (default: UNPAYWALL_EMAIL env var, "
        "or literature-review-skill@example.com)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=3.0,
        help="Delay between requests in seconds (default: 3)",
    )
    args = parser.parse_args()

    output_path = args.output or args.extraction

    email = (
        args.email
        or os.environ.get("UNPAYWALL_EMAIL")
        or DEFAULT_EMAIL
    )

    bib_dois = _parse_bib_keys_to_doi(args.bib)

    if args.dois:
        doi_keys = [(doi, "") for doi in args.dois]
    elif args.audit:
        if not os.path.isfile(args.audit):
            parser.error(f"Audit file not found: {args.audit}")
        doi_keys = get_unverified_dois(args.audit, bib_dois)
    else:
        parser.error("Provide either an audit file or --dois")
        return

    if not doi_keys:
        print("No DOIs to fetch.")
        return

    print(f"Articles to fetch: {len(doi_keys)}", file=sys.stderr)

    scihub_mirror = args.mirror
    if not scihub_mirror:
        print("Finding working Sci-Hub mirror...", file=sys.stderr)
        scihub_mirror = find_working_mirror()
        if scihub_mirror:
            print(f"  Using mirror: {scihub_mirror}", file=sys.stderr)
        else:
            print("  No Sci-Hub mirror found, using OA sources only", file=sys.stderr)

    if os.path.isfile(args.extraction):
        with open(args.extraction, "r", encoding="utf-8") as f:
            extraction = json.load(f)
    else:
        extraction = {"stats": {}, "articles": {}}

    doi_to_ext_key: dict[str, str] = {}
    for ext_key, article in extraction.get("articles", {}).items():
        doi = article.get("doi", "").strip().lower()
        if doi:
            doi_to_ext_key[doi] = ext_key

    stats = {"pmc": 0, "unpaywall": 0, "publisher": 0, "sci-hub": 0, "failed": 0, "new_claims": 0}

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, (doi, bib_key) in enumerate(doi_keys):
            print(f"[{i+1}/{len(doi_keys)}] {doi} ({bib_key})", file=sys.stderr)

            text, source = fetch_article_text(doi, tmpdir, i, scihub_mirror, email=email)

            if not text:
                print(f"  FAILED: {source}", file=sys.stderr)
                stats["failed"] += 1
            else:
                fulltext_claims = extract_claims_from_text(text, source)
                stats[source] = stats.get(source, 0) + 1
                stats["new_claims"] += len(fulltext_claims)
                print(f"  OK ({source}): {len(fulltext_claims)} claims", file=sys.stderr)

                ext_key = doi_to_ext_key.get(doi.lower(), "")
                if ext_key and ext_key in extraction["articles"]:
                    existing = extraction["articles"][ext_key].get("claims", [])
                    existing_values = {c["value"] for c in existing}
                    new_claims = [c for c in fulltext_claims if c["value"] not in existing_values]
                    existing.extend(new_claims)
                    extraction["articles"][ext_key]["claims"] = existing
                    extraction["articles"][ext_key]["has_fulltext"] = True
                    extraction["articles"][ext_key]["fulltext_source"] = source

            if i + 1 < len(doi_keys):
                time.sleep(args.delay)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(extraction, f, indent=2, ensure_ascii=False)

    print(f"\nFull-text fetch complete:")
    print(f"  PMC:        {stats['pmc']}")
    print(f"  Unpaywall:  {stats['unpaywall']}")
    print(f"  Publisher:  {stats['publisher']}")
    print(f"  Sci-Hub:    {stats['sci-hub']}")
    print(f"  Failed:     {stats['failed']}")
    print(f"  New claims: {stats['new_claims']}")
    print(f"Output: {output_path}")

    if stats["publisher"] == 0 and stats["failed"] > 0:
        print(
            "\nNote: no articles were retrieved via publisher direct access. "
            "If you have institutional access, connect to your university VPN "
            "before running this script to unlock paywalled PDFs.",
        )


if __name__ == "__main__":
    main()
