#!/usr/bin/env python3
import argparse
import os
import re
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(__file__))
from bibtex_keys import unique_key as _unique_key, strip_code_blocks as _strip_code_blocks, extract_doi_matches as _extract_doi_matches, build_bibtex_entry as _build_bibtex_entry
from http_utils import request_with_retry as _request_with_retry, ncbi_params as _ncbi_params

# 3-level resolution chain:
# doi.org — primary resolver (native BibTeX)
# CrossRef API — fallback if doi.org fails
# PubMed API — fallback if CrossRef fails (publishers not registered with CrossRef)


def bibtex_from_pubmed(doi, timeout=10):
    r = _request_with_retry("GET",
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        params=_ncbi_params({"db": "pubmed", "term": f"{doi}[doi]", "retmode": "json"}),
        timeout=timeout
    )
    r.raise_for_status()
    ids = r.json()["esearchresult"]["idlist"]
    if not ids:
        raise ValueError("DOI not found on PubMed")
    pmid = ids[0]
    r = _request_with_retry("GET",
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
        params=_ncbi_params({"db": "pubmed", "id": pmid, "retmode": "json"}),
        timeout=timeout
    )
    r.raise_for_status()
    meta = r.json()["result"][pmid]
    authors = " and ".join(a["name"] for a in meta.get("authors", []) if a.get("authtype") == "Author")
    _pd = meta.get("pubdate", "")
    _ym = re.search(r'\d{4}', _pd)
    year = _ym.group() if _ym else ""
    pubtypes = [pt.lower() for pt in meta.get("pubtype", [])]
    entry_type = "book" if any("book" in pt for pt in pubtypes) else "article"
    first_author = next((a["name"] for a in meta.get("authors", []) if a.get("authtype") == "Author"), "Unknown")
    key = first_author.split()[0]
    if year:
        key += f"_{year}"
    journal_field = "booktitle" if entry_type in ("incollection", "inproceedings") else "journal"
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
    return _build_bibtex_entry(entry_type, key, fields)


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


def bibtex_from_crossref(doi, timeout=10):
    r = _request_with_retry("GET",
        f"https://api.crossref.org/works/{doi}",
        timeout=timeout
    )
    r.raise_for_status()
    meta = r.json()["message"]
    entry_type = _CROSSREF_TYPE_MAP.get(meta.get("type", ""), "article")
    authors = " and ".join(
        f"{a.get('family', '')}, {a.get('given', '')}" if a.get('given') else a.get('family') or a.get('name', '')
        for a in meta.get("author", [])
    )
    year = ""
    for _field in ("published", "published-print", "published-online"):
        _dp = meta.get(_field, {}).get("date-parts", [[]])
        if _dp and _dp[0]:
            year = str(_dp[0][0])
            break
    _first_a = (meta.get("author") or [{}])[0]
    key = _first_a.get("family") or _first_a.get("name") or "Unknown"
    if year:
        key += f"_{year}"
    journal_field = "booktitle" if entry_type in ("incollection", "inproceedings") else "journal"
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
    return _build_bibtex_entry(entry_type, key, fields)


def extract_dois(files):
    dois = {}
    for f in files:
        with open(f, encoding='utf-8') as fh:
            text = _strip_code_blocks(fh.read(), keep_bibtex=True)
        for doi in _extract_doi_matches(text):
            dois[doi] = None
    return list(dois)


def _extract_bibtex_entries(text):
    """Extract BibTeX entries by tracking brace depth (handles @ and nested braces in values)."""
    entries = []
    for m in re.finditer(r'@\w+\{', text):
        start = m.start()
        depth = 1
        i = m.end()
        while i < len(text) and depth > 0:
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
            i += 1
        if depth == 0:
            entries.append(text[start:i])
    return entries


def extract_refs_md(files):
    refs_md = {}
    for f in files:
        with open(f, encoding='utf-8') as fh:
            text = _strip_code_blocks(fh.read(), keep_bibtex=True)
        for block in _extract_bibtex_entries(text):
            doi_m = re.search(r'doi\s*=\s*\{(.+?)\}', block, re.IGNORECASE)
            if not doi_m:
                continue
            doi = doi_m.group(1).strip().rstrip('.,;:')
            key_m = re.match(r'@\w+\{([^,]+),', block)
            key = key_m.group(1).strip() if key_m else ""
            year_m = re.search(r'year\s*=\s*\{?(\d{4})', block)
            author_m = re.search(r'author\s*=\s*\{(.+?)\}', block, re.DOTALL)
            year = year_m.group(1) if year_m else ""
            if author_m:
                first_author = author_m.group(1).split(" and ")[0].strip()
                first_author = re.split(r'[,\s]', first_author)[0]
            else:
                first_author = ""
            refs_md[doi] = {"author": first_author, "year": year, "key": key}
    return refs_md


def resolve_bibtex(doi, timeout=10):
    r = _request_with_retry("GET",
        f"https://doi.org/{doi}",
        headers={"Accept": "application/x-bibtex"},
        allow_redirects=True,
        timeout=timeout
    )
    r.raise_for_status()
    text = r.text.strip()
    if not re.match(r'@\w+\{', text):
        raise ValueError("Response is not valid BibTeX")
    return text



def _rekey_entry(entry, seen_keys):
    """Assign a unique key to a BibTeX entry.

    Returns (entry, renamed_original) where renamed_original is (old, new)
    if the first occurrence needs retroactive renaming, or None.
    """
    m = re.match(r'(@\w+)\{([^,]+),', entry)
    if not m:
        return entry, None
    prefix, old_key = m.group(1), m.group(2)
    new_key, renamed = _unique_key(old_key, seen_keys)
    if new_key != old_key:
        entry = entry.replace(f"{prefix}{{{old_key},", f"{prefix}{{{new_key},", 1)
    return entry, renamed


def _set_entry_key(entry, new_key):
    """Replace the BibTeX key in an entry string."""
    return re.sub(r'(@\w+)\{[^,]+,', rf'\1{{{new_key},', entry, count=1)


def generate_bib(files, output, timeout=10):
    dois = extract_dois(files)
    refs_md = extract_refs_md(files)
    md_keys = {doi: info["key"] for doi, info in refs_md.items() if info["key"]}
    bib_entries = {}
    seen_keys = set(md_keys.values())  # reserves markdown keys so orphan DOIs don't collide; retroactive rename of a pinned md key can't happen in practice because all cited DOIs have a md_keys entry (SKILL.md workflow enforces bibtex blocks)

    resolvers = [
        ("doi.org", resolve_bibtex),
        ("CrossRef", bibtex_from_crossref),
        ("PubMed", bibtex_from_pubmed),
    ]
    for doi in dois:
        for name, resolver in resolvers:
            try:
                entry = resolver(doi, timeout=timeout)
                if doi in md_keys:
                    entry = _set_entry_key(entry, md_keys[doi])
                else:
                    entry, renamed = _rekey_entry(entry, seen_keys)
                    if renamed:
                        old_name, new_name = renamed
                        for d, e in bib_entries.items():
                            if re.match(rf'@\w+\{{{re.escape(old_name)},', e):
                                bib_entries[d] = _set_entry_key(e, new_name)
                                break
                bib_entries[doi] = entry.strip()
                print(f"OK ({name}): {doi}")
                break
            except (requests.RequestException, ValueError, KeyError) as e:
                print(f"  {name} failed for {doi} ({e})")
                time.sleep(0.5)
        else:
            print(f"FAILED: {doi} (all resolvers exhausted)")
        time.sleep(0.5)

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    with open(output, "w", encoding="utf-8") as bib:
        bib.write("\n\n".join(bib_entries.values()) + "\n")

    print(f"\n{len(bib_entries)} entry(ies) written to {output}")
    return verify(refs_md, bib_entries)


def verify(refs_md, bib_entries):
    print("\n--- Cross-checking references ---\n")
    errors = []
    for doi, md in refs_md.items():
        entry = bib_entries.get(doi)
        if not entry:
            errors.append(f"MISSING in bib: {doi} ({md['author']} {md['year']})")
            continue
        bib_year_m = re.search(r'year\s*=\s*\{?(\d{4})', entry)
        bib_author_m = re.search(r'author\s*=\s*\{(.+?)\}', entry)
        bib_year = bib_year_m.group(1) if bib_year_m else "?"
        if bib_author_m:
            raw = bib_author_m.group(1)
            first = raw.split(" and ")[0].strip()
            bib_first_author = re.split(r'[,\s]', first)[0]
        else:
            bib_first_author = "?"
        ok = True
        msgs = []
        if md["year"] != bib_year:
            msgs.append(f"year md={md['year']} vs bib={bib_year}")
            ok = False
        if bib_first_author != "?" and md["author"].lower() != bib_first_author.lower():
            msgs.append(f"author md={md['author']} vs bib={bib_first_author}")
            ok = False
        if ok:
            print(f"  OK: {doi} — {md['author']} ({md['year']})")
        else:
            msg = f"  MISMATCH: {doi} — " + ", ".join(msgs)
            print(msg)
            errors.append(msg)

    for doi in bib_entries:
        if doi not in refs_md:
            print(f"  EXTRA in bib (DOI not in markdown): {doi}")
            errors.append(f"EXTRA: {doi}")

    if errors:
        print(f"\n{len(errors)} issue(s) detected.")
        return 1
    print("\nAll references match.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Generate a BibTeX file from DOIs found in markdown documents, "
                    "with author/year cross-verification."
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="Markdown files to process"
    )
    parser.add_argument(
        "--output", "-o",
        default="review/references.bib",
        help="Output BibTeX file (default: review/references.bib)"
    )
    parser.add_argument(
        "--timeout", type=int, default=10,
        help="HTTP timeout in seconds (default: 10)"
    )
    args = parser.parse_args()
    missing = [f for f in args.files if not os.path.isfile(f)]
    if missing:
        parser.error(f"File(s) not found: {', '.join(missing)}")
    sys.exit(generate_bib(args.files, args.output, timeout=args.timeout))


if __name__ == "__main__":
    main()
