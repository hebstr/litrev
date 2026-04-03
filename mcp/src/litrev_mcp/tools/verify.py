"""MCP tools: citation verification, bibliography generation, claims audit."""

import json
import os
import re
import time
from typing import Any


from ..lib.http import request_with_retry, ncbi_params
from ..lib.bibtex import (
    strip_code_blocks,
    extract_doi_matches,
    extract_pmid_entries,
    parse_bib_keys_to_doi,
    build_bibtex_entry,
    unique_key,
)
from ..lib.patterns import STAT_PATTERN, NUM_PATTERN


# ---------------------------------------------------------------------------
# Tool 1: verify_dois
# ---------------------------------------------------------------------------


def _get_crossref_metadata(doi: str) -> dict:
    try:
        url = f"https://api.crossref.org/works/{doi}"
        response = request_with_retry("GET", url)
        if response.status_code == 200:
            message = response.json().get("message", {})
            authors_list = message.get("author", [])
            formatted = []
            for author in authors_list[:3]:
                given = author.get("given", "")
                family = author.get("family", "")
                name = author.get("name", "")
                if family:
                    formatted.append(f"{family}, {given[0]}." if given else family)
                elif name:
                    formatted.append(name)
            if len(authors_list) > 3:
                formatted.append("et al.")
            year = ""
            for field in ("published", "published-print", "published-online"):
                date_parts = message.get(field, {}).get("date-parts", [[]])
                if date_parts and date_parts[0]:
                    year = str(date_parts[0][0])
                    break
            return {
                "title": message.get("title", [""])[0],
                "authors": ", ".join(formatted),
                "year": year,
                "journal": message.get("container-title", [""])[0],
                "volume": message.get("volume", ""),
                "pages": message.get("page", ""),
                "doi": doi,
            }
        return {}
    except Exception:
        return {}


def _pmid_from_doi(doi: str) -> str:
    try:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        response = request_with_retry(
            "GET",
            url,
            params=ncbi_params(
                {"db": "pubmed", "term": f"{doi}[doi]", "retmode": "json"}
            ),
        )
        if response.status_code == 200:
            ids = response.json().get("esearchresult", {}).get("idlist", [])
            if ids:
                return ids[0]
    except Exception:
        pass
    return ""


def _check_retraction(pmid: str) -> bool:
    try:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        term = (
            f"(retracted publication[pt] OR retraction of publication[pt]) "
            f"AND {pmid}[pmid]"
        )
        response = request_with_retry(
            "GET",
            url,
            params=ncbi_params({"db": "pubmed", "term": term, "retmode": "json"}),
        )
        if response.status_code == 200:
            count = int(response.json().get("esearchresult", {}).get("count", 0))
            return count > 0
    except Exception:
        pass
    return False


def verify_dois(
    review_path: str,
    *,
    check_retractions: bool = True,
    timeout: int = 10,
    output_path: str | None = None,
) -> dict:
    with open(review_path, "r", encoding="utf-8") as f:
        content = f.read()

    text = strip_code_blocks(content, keep_bibtex=True)
    dois = extract_doi_matches(text)

    pmids_in_text = re.findall(r"PMID:\s*(\d+)", content)
    pmids_in_text += re.findall(r"pmid\s*=\s*\{(\d+)\}", content, re.IGNORECASE)
    pmids_in_text = list(dict.fromkeys(pmids_in_text))

    report: dict[str, Any] = {
        "total_dois": len(dois),
        "total_pmids": len(pmids_in_text),
        "verified": [],
        "failed": [],
        "retracted": [],
        "retraction_unchecked": [],
        "metadata": {},
    }

    seen_pmids: set[str] = set()

    for doi in dois:
        try:
            url = f"https://doi.org/api/handles/{doi}"
            response = request_with_retry("GET", url, timeout=timeout)
            if response.status_code == 200:
                metadata = _get_crossref_metadata(doi)
                report["verified"].append(doi)
                report["metadata"][doi] = metadata
                if check_retractions:
                    pmid = _pmid_from_doi(doi)
                    if pmid:
                        seen_pmids.add(pmid)
                        if _check_retraction(pmid):
                            report["retracted"].append(doi)
                    else:
                        report["retraction_unchecked"].append(doi)
            else:
                report["failed"].append(doi)
        except Exception:
            report["failed"].append(doi)

    for pmid in pmids_in_text:
        if pmid in seen_pmids:
            continue
        try:
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            response = request_with_retry(
                "GET",
                url,
                params=ncbi_params({"db": "pubmed", "id": pmid, "retmode": "json"}),
                timeout=timeout,
            )
            if response.status_code == 200:
                data = response.json()
                result = data.get("result", {}).get(str(pmid), {})
                if "error" not in result:
                    report["verified"].append(f"PMID:{pmid}")
                    if check_retractions and _check_retraction(pmid):
                        report["retracted"].append(f"PMID:{pmid}")
                else:
                    report["failed"].append(f"PMID:{pmid}")
            else:
                report["failed"].append(f"PMID:{pmid}")
        except Exception:
            report["failed"].append(f"PMID:{pmid}")

    out = output_path or os.path.splitext(review_path)[0] + "_citation_report.json"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return {
        "output_path": out,
        "total_dois": report["total_dois"],
        "total_pmids": report["total_pmids"],
        "verified": len(report["verified"]),
        "failed": len(report["failed"]),
        "retracted": len(report["retracted"]),
        "retraction_unchecked": len(report["retraction_unchecked"]),
        "retracted_list": report["retracted"],
        "failed_list": report["failed"],
    }


_IDCONV_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
_IDCONV_BATCH = 200


def _resolve_pmids_to_dois(pmids: list[str], timeout: int = 10) -> dict[str, str]:
    result: dict[str, str] = {}
    for start in range(0, len(pmids), _IDCONV_BATCH):
        batch = pmids[start : start + _IDCONV_BATCH]
        ids_str = ",".join(batch)
        try:
            resp = request_with_retry(
                "GET",
                _IDCONV_URL,
                params=ncbi_params({"ids": ids_str, "format": "json"}),
                timeout=timeout,
            )
            if resp.status_code != 200:
                continue
            records = resp.json().get("records", [])
            for rec in records:
                doi = rec.get("doi", "").strip()
                pmid = rec.get("pmid", "").strip()
                if doi and pmid:
                    result[pmid] = doi
        except Exception:
            continue
        time.sleep(0.5)
    return result


# ---------------------------------------------------------------------------
# Tool 2: generate_bibliography
# ---------------------------------------------------------------------------

_CROSSREF_TYPE_MAP = {
    "journal-article": "article",
    "book": "book",
    "book-chapter": "incollection",
    "proceedings-article": "inproceedings",
    "monograph": "book",
    "edited-book": "book",
    "posted-content": "article",
    "report": "techreport",
    "dataset": "misc",
    "standard": "misc",
    "other": "misc",
}


def _resolve_bibtex_from_doi(doi: str, timeout: int = 10) -> str:
    r = request_with_retry(
        "GET",
        f"https://doi.org/{doi}",
        headers={"Accept": "application/x-bibtex"},
        timeout=timeout,
    )
    r.raise_for_status()
    text = r.text.strip()
    if not re.match(r"@\w+\{", text):
        raise ValueError("Response is not valid BibTeX")
    return text


def _bibtex_from_crossref(doi: str, timeout: int = 10) -> str:
    r = request_with_retry(
        "GET", f"https://api.crossref.org/works/{doi}", timeout=timeout
    )
    r.raise_for_status()
    meta = r.json()["message"]
    entry_type = _CROSSREF_TYPE_MAP.get(meta.get("type", ""), "article")
    authors = " and ".join(
        f"{a.get('family', '')}, {a.get('given', '')}"
        if a.get("given")
        else a.get("family") or a.get("name", "")
        for a in meta.get("author", [])
    )
    year = ""
    for field in ("published", "published-print", "published-online"):
        dp = meta.get(field, {}).get("date-parts", [[]])
        if dp and dp[0]:
            year = str(dp[0][0])
            break
    first_a = (meta.get("author") or [{}])[0]
    key = first_a.get("family") or first_a.get("name") or "Unknown"
    if year:
        key += f"_{year}"
    journal_field = (
        "booktitle" if entry_type in ("incollection", "inproceedings") else "journal"
    )
    fields = {
        "title": meta.get("title", [""])[0],
        "author": authors,
        journal_field: meta.get("container-title", [""])[0],
        "year": year,
        "volume": meta.get("volume", ""),
        "number": meta.get("issue", ""),
        "pages": meta.get("page", ""),
        "doi": doi,
    }
    return build_bibtex_entry(entry_type, key, fields)


def _bibtex_from_pubmed(doi: str, timeout: int = 10) -> str:
    r = request_with_retry(
        "GET",
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        params=ncbi_params({"db": "pubmed", "term": f"{doi}[doi]", "retmode": "json"}),
        timeout=timeout,
    )
    r.raise_for_status()
    ids = r.json()["esearchresult"]["idlist"]
    if not ids:
        raise ValueError("DOI not found on PubMed")
    pmid = ids[0]
    r = request_with_retry(
        "GET",
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
        params=ncbi_params({"db": "pubmed", "id": pmid, "retmode": "json"}),
        timeout=timeout,
    )
    r.raise_for_status()
    meta = r.json()["result"][pmid]
    authors = " and ".join(
        a["name"] for a in meta.get("authors", []) if a.get("authtype") == "Author"
    )
    pd = meta.get("pubdate", "")
    ym = re.search(r"\d{4}", pd)
    year = ym.group() if ym else ""
    pubtypes = [pt.lower() for pt in meta.get("pubtype", [])]
    entry_type = "book" if any("book" in pt for pt in pubtypes) else "article"
    first_author = next(
        (a["name"] for a in meta.get("authors", []) if a.get("authtype") == "Author"),
        "Unknown",
    )
    key = first_author.split()[0]
    if year:
        key += f"_{year}"
    journal_field = (
        "booktitle" if entry_type in ("incollection", "inproceedings") else "journal"
    )
    fields = {
        "title": meta.get("title", ""),
        "author": authors,
        journal_field: meta.get("fulljournalname", meta.get("source", "")),
        "year": year,
        "volume": meta.get("volume", ""),
        "number": meta.get("issue", ""),
        "pages": meta.get("pages", ""),
        "doi": doi,
    }
    return build_bibtex_entry(entry_type, key, fields)


def _extract_bibtex_entries(text: str) -> list[str]:
    entries = []
    for m in re.finditer(r"@\w+\{", text):
        start = m.start()
        depth = 1
        i = m.end()
        while i < len(text) and depth > 0:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        if depth == 0:
            entries.append(text[start:i])
    return entries


def _extract_refs_md(files: list[str]) -> dict[str, dict]:
    refs_md: dict[str, dict] = {}
    for f in files:
        with open(f, encoding="utf-8") as fh:
            text = strip_code_blocks(fh.read(), keep_bibtex=True)
        for block in _extract_bibtex_entries(text):
            doi_m = re.search(r"doi\s*=\s*\{(.+?)\}", block, re.IGNORECASE)
            if not doi_m:
                continue
            doi = doi_m.group(1).strip().rstrip(".,;:")
            key_m = re.match(r"@\w+\{([^,]+),", block)
            key = key_m.group(1).strip() if key_m else ""
            year_m = re.search(r"year\s*=\s*\{?(\d{4})", block)
            author_m = re.search(r"author\s*=\s*\{(.+?)\}", block, re.DOTALL)
            title_m = re.search(r"title\s*=\s*\{(.+?)\}", block, re.DOTALL)
            year = year_m.group(1) if year_m else ""
            if author_m:
                first_author = author_m.group(1).split(" and ")[0].strip()
                first_author = re.split(r"[,\s]", first_author)[0]
            else:
                first_author = ""
            title = title_m.group(1).strip() if title_m else ""
            refs_md[doi] = {
                "author": first_author,
                "year": year,
                "key": key,
                "title": title,
            }
    return refs_md


def _set_entry_key(entry: str, new_key: str) -> str:
    return re.sub(r"(@\w+)\{[^,]+,", rf"\1{{{new_key},", entry, count=1)


def generate_bibliography(
    review_path: str,
    *,
    output_path: str = "review/references.bib",
    timeout: int = 10,
) -> dict:
    files = [review_path]
    with open(review_path, encoding="utf-8") as f:
        text = strip_code_blocks(f.read(), keep_bibtex=True)
    dois = list(dict.fromkeys(extract_doi_matches(text)))
    refs_md = _extract_refs_md(files)
    md_keys = {doi: info["key"] for doi, info in refs_md.items() if info["key"]}

    pmid_entries = extract_pmid_entries(text)
    pmids_without_doi = [p for p, info in pmid_entries.items() if not info["has_doi"]]
    doi_set = set(dois)
    if pmids_without_doi:
        pmid_to_doi = _resolve_pmids_to_dois(pmids_without_doi, timeout=timeout)
        for pmid, doi in pmid_to_doi.items():
            if doi not in doi_set:
                dois.append(doi)
                doi_set.add(doi)
            info = pmid_entries[pmid]
            md_keys.setdefault(doi, info["key"])
            refs_md.setdefault(
                doi,
                {
                    "author": info["author"],
                    "year": info["year"],
                    "key": info["key"],
                    "title": info["title"],
                },
            )

    bib_entries: dict[str, str] = {}
    seen_keys = set(md_keys.values())

    resolvers = [
        ("doi.org", _resolve_bibtex_from_doi),
        ("CrossRef", _bibtex_from_crossref),
        ("PubMed", _bibtex_from_pubmed),
    ]

    log_lines: list[str] = []

    for doi in dois:
        for name, resolver in resolvers:
            try:
                entry = resolver(doi, timeout=timeout)
                if doi in md_keys:
                    entry = _set_entry_key(entry, md_keys[doi])
                else:
                    m = re.match(r"(@\w+)\{([^,]+),", entry)
                    if m:
                        old_key = m.group(2)
                        new_key, renamed = unique_key(old_key, seen_keys)
                        if new_key != old_key:
                            entry = entry.replace(
                                f"{m.group(1)}{{{old_key},",
                                f"{m.group(1)}{{{new_key},",
                                1,
                            )
                        if renamed:
                            old_name, new_name = renamed
                            for d, e in bib_entries.items():
                                if re.match(rf"@\w+\{{{re.escape(old_name)},", e):
                                    bib_entries[d] = _set_entry_key(e, new_name)
                                    break
                bib_entries[doi] = entry.strip()
                log_lines.append(f"OK ({name}): {doi}")
                break
            except Exception as e:
                log_lines.append(f"  {name} failed for {doi} ({e})")
                time.sleep(0.5)
        else:
            log_lines.append(f"FAILED: {doi} (all resolvers exhausted)")
        time.sleep(0.5)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as bib:
        bib.write("\n\n".join(bib_entries.values()) + "\n")

    errors = []
    for doi, md in refs_md.items():
        entry = bib_entries.get(doi)
        if not entry:
            errors.append(f"MISSING in bib: {doi} ({md['author']} {md['year']})")
            continue
        bib_year_m = re.search(r"year\s*=\s*\{?(\d{4})", entry)
        bib_author_m = re.search(r"author\s*=\s*\{(.+?)\}", entry)
        bib_year = bib_year_m.group(1) if bib_year_m else "?"
        if bib_author_m:
            raw = bib_author_m.group(1)
            first = raw.split(" and ")[0].strip()
            bib_first_author = re.split(r"[,\s]", first)[0]
        else:
            bib_first_author = "?"
        if md["year"] != bib_year:
            errors.append(f"MISMATCH year: {doi} md={md['year']} bib={bib_year}")
        if bib_first_author != "?" and md["author"].lower() != bib_first_author.lower():
            errors.append(
                f"MISMATCH author: {doi} md={md['author']} bib={bib_first_author}"
            )
        if md.get("title"):
            bib_title_m = re.search(r"title\s*=\s*\{(.+?)\}", entry, re.DOTALL)
            if bib_title_m:
                md_words = set(re.findall(r"\w{4,}", md["title"].lower()))
                bib_words = set(re.findall(r"\w{4,}", bib_title_m.group(1).lower()))
                if (
                    md_words
                    and bib_words
                    and len(md_words & bib_words) / max(len(md_words), 1) < 0.3
                ):
                    errors.append(
                        f"MISMATCH title: {doi} — embedded BibTeX title does not match resolved title"
                    )

    return {
        "output_path": output_path,
        "entries": len(bib_entries),
        "errors": errors,
        "log": log_lines,
    }


# ---------------------------------------------------------------------------
# Tool 3: audit_claims
# ---------------------------------------------------------------------------

_CITE_RE = re.compile(
    r"\[@([\w-]+(?:_\d{4}[a-z]?)?(?:\s*;\s*@[\w-]+(?:_\d{4}[a-z]?)?)*)\]"
)

_SENTENCE_SPLIT = re.compile(r"\.(?:\s+[A-Z]|\s*\n)")


def _split_sentence(text: str, pos: int) -> tuple[int, int]:
    start = 0
    for m in _SENTENCE_SPLIT.finditer(text):
        boundary = m.start() + 1
        if boundary <= pos:
            start = boundary
        else:
            return start, boundary
    return start, len(text)


def _build_doi_index(extraction: dict) -> dict[str, str]:
    doi_to_key: dict[str, str] = {}
    for ext_key, article in extraction.get("articles", {}).items():
        doi = (article.get("doi") or "").strip().lower()
        if doi:
            doi_to_key[doi] = ext_key
    return doi_to_key


def _resolve_key(
    review_key: str,
    articles: dict,
    bib_dois: dict[str, str],
    doi_index: dict[str, str],
) -> str | None:
    if review_key in articles:
        return review_key
    doi = bib_dois.get(review_key, "")
    if doi and doi in doi_index:
        return doi_index[doi]
    parts = re.match(r"^(.+?)_(\d{4})([a-z]?)$", review_key)
    if parts:
        name_fragment = parts.group(1).lower()
        year = parts.group(2)
        for ext_key in articles:
            ext_match = re.match(r"^(.+?)_(\d{4})([a-z]?)$", ext_key)
            if (
                ext_match
                and ext_match.group(2) == year
                and ext_match.group(1).lower().startswith(name_fragment)
            ):
                return ext_key
    return None


_WORD_ONES = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
}
_WORD_TENS = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}
_WORD_MULT = {"hundred": 100, "thousand": 1000}


def _words_to_digits(text: str) -> str:
    pattern = (
        r"(?i)\b("
        r"(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)"
        r"[-\s]"
        r"(?:one|two|three|four|five|six|seven|eight|nine)"
        r"|(?:zero|one|two|three|four|five|six|seven|eight|nine|ten"
        r"|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen"
        r"|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy"
        r"|eighty|ninety)"
        r")"
        r"(?:\s*(?:hundred|thousand))?"
        r"\b"
    )

    def _convert(m: re.Match) -> str:
        raw = m.group(0).lower().strip()
        parts = re.split(r"[\s-]+", raw)
        total = 0
        current = 0
        for p in parts:
            if p in _WORD_ONES:
                current += _WORD_ONES[p]
            elif p in _WORD_TENS:
                current += _WORD_TENS[p]
            elif p in _WORD_MULT:
                current = (current or 1) * _WORD_MULT[p]
                if p == "thousand":
                    total += current
                    current = 0
        total += current
        if total == 0 and "zero" not in raw:
            return m.group(0)
        return str(total)

    return re.sub(pattern, _convert, text)


def _normalize_number(value: str) -> str:
    value = value.replace("\u00b7", ".")
    value = re.sub(r"(?<=\d)[\s\u00a0](?=\d{3}(?!\d))", "", value)
    value = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", value)
    value = value.replace(",", ".").replace(" ", "").replace("\u00a0", "")
    value = re.sub(r"(\d\.\d+?)0+(?=\D|$)", r"\1", value)
    return value


def _number_matches(review_num: str, claim_value: str) -> bool:
    norm_review = _normalize_number(review_num)
    norm_claim = _normalize_number(_words_to_digits(claim_value))
    return bool(
        re.search(rf"(?<!\d)(?<!\.){re.escape(norm_review)}(?!\d)(?!\.\d)", norm_claim)
    )


def _mask_citations(sentence: str) -> str:
    return _CITE_RE.sub(lambda m: " " * len(m.group(0)), sentence)


def _extract_review_claims(text: str) -> list[dict[str, str]]:
    claims: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for cite_m in _CITE_RE.finditer(text):
        keys = re.findall(r"@?([\w-]+(?:_\d{4}[a-z]?)?)", cite_m.group(1))
        sent_start, sent_end = _split_sentence(text, cite_m.start())
        sentence = text[sent_start:sent_end]
        masked = _mask_citations(sentence)
        offset = sent_start

        stat_spans: list[tuple[int, int]] = []
        for m in STAT_PATTERN.finditer(masked):
            stat_value = m.group(0).strip()
            stat_spans.append((m.start(), m.end()))
            for key in keys:
                pair = (stat_value, key)
                if pair not in seen:
                    seen.add(pair)
                    ctx_start = max(0, offset + m.start() - 40)
                    ctx_end = min(len(text), cite_m.end() + 10)
                    claims.append(
                        {
                            "value": stat_value,
                            "type": "statistic",
                            "citation_key": key,
                            "context": text[ctx_start:ctx_end]
                            .replace("\n", " ")
                            .strip(),
                        }
                    )

        for m in NUM_PATTERN.finditer(masked):
            num_value = m.group(0).strip()
            if len(num_value) == 1:
                continue
            already_in_stat = any(
                m.start() >= ss and m.end() <= se for ss, se in stat_spans
            )
            if already_in_stat:
                continue
            abs_start = offset + m.start()
            abs_end = offset + m.end()
            if "%" not in num_value:
                pct_check = text[abs_start : min(abs_end + 2, len(text))]
                if "%" in pct_check:
                    num_value += "%"
            for key in keys:
                pair = (num_value, key)
                if pair not in seen:
                    seen.add(pair)
                    ctx_start = max(0, abs_start - 20)
                    ctx_end = min(len(text), cite_m.end() + 10)
                    claims.append(
                        {
                            "value": num_value,
                            "type": "percentage" if "%" in num_value else "number",
                            "citation_key": key,
                            "context": text[ctx_start:ctx_end]
                            .replace("\n", " ")
                            .strip(),
                        }
                    )

    return claims


def audit_claims(
    review_path: str,
    *,
    claims_path: str = "review/extracted_claims.json",
    bib_path: str | None = None,
    output_path: str = "review/claims_audit.json",
) -> dict:
    with open(review_path, "r", encoding="utf-8") as f:
        review_text = f.read()

    with open(claims_path, "r", encoding="utf-8") as f:
        extraction = json.load(f)

    if bib_path is None:
        candidate = os.path.join(os.path.dirname(review_path), "references.bib")
        if os.path.isfile(candidate):
            bib_path = candidate

    bib_dois: dict[str, str] = {}
    if bib_path:
        bib_dois = parse_bib_keys_to_doi(bib_path)

    articles = extraction.get("articles", {})
    doi_index = _build_doi_index(extraction)

    review_claims = _extract_review_claims(review_text)

    results: list[dict[str, Any]] = []
    summary = {
        "verified": 0,
        "unverified": 0,
        "no_abstract": 0,
        "no_extraction": 0,
        "total": 0,
    }

    for claim in review_claims:
        summary["total"] += 1
        key = claim["citation_key"]
        resolved = _resolve_key(key, articles, bib_dois, doi_index)
        entry: dict[str, Any] = {
            "value": claim["value"],
            "type": claim["type"],
            "citation_key": key,
            "context": claim["context"],
        }
        if resolved and resolved != key:
            entry["resolved_to"] = resolved

        if resolved is None:
            entry["status"] = "NO_EXTRACTION"
            entry["detail"] = f"Key '{key}' not found in extracted_claims.json"
            summary["no_extraction"] += 1
        elif not articles[resolved].get("has_abstract", False):
            entry["status"] = "NO_ABSTRACT"
            entry["detail"] = "Article had no abstract available"
            summary["no_abstract"] += 1
        else:
            article_claims = articles[resolved].get("claims", [])
            semantic = articles[resolved].get("semantic_claims", [])
            all_claims = article_claims + semantic
            matched = False
            for ac in all_claims:
                ac_value = (
                    ac.get("value") or ac.get("effect_size") or ac.get("claim") or ""
                )
                if _number_matches(claim["value"], ac_value):
                    matched = True
                    entry["status"] = "VERIFIED"
                    entry["matched_claim"] = ac
                    summary["verified"] += 1
                    break
            if not matched:
                entry["status"] = "UNVERIFIED"
                entry["detail"] = "Number not found in abstract-extracted claims"
                summary["unverified"] += 1

        results.append(entry)

    audit = {"summary": summary, "claims": results}

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)

    return {
        "output_path": output_path,
        "total": summary["total"],
        "verified": summary["verified"],
        "unverified": summary["unverified"],
        "no_abstract": summary["no_abstract"],
        "no_extraction": summary["no_extraction"],
    }
