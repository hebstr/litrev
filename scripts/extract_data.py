#!/usr/bin/env python3
"""
Extract quantitative claims from abstracts of selected articles.

Produces a structured JSON file mapping each article's BibTeX key to the
numerical claims found in its abstract. This file serves as the single
source of truth for numbers that may be cited in the review.

Usage:
    python extract_data.py review/combined_results.json \
        --rows 3 17 33 62 \
        --output review/extracted_claims.json
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Any


NUM_PATTERN = re.compile(
    r"(?<![A-Za-z\d/])"
    r"("
    r"\d+(?:[.,]\d+)?%"             # percentage: 9.7%, 36,4%
    r"|\d+(?:[.,]\d+)?"             # plain number: 1600, 3.2
    r")"
    r"(?![A-Za-z\d])"
)

STAT_PATTERN = re.compile(
    r"("
    r"(?:OR|HR|RR|RD|AOR|aOR|aHR|CI|NNT|NNH|SMD|WMD|MD|IRR|SIR|PR)"
    r"[\s:=]*"
    r"[\d.,\-–\s()%]+"
    r"|p\s*[<=>\s]+\s*[\d.,]+"
    r"|(?:95\s*%?\s*CI)\s*[:=]?\s*[\[(][\d.,\-–\s]+[\])]"
    r")",
    re.IGNORECASE,
)


EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BATCH_SIZE = 200


def fetch_abstracts_from_pubmed(pmids: list[str]) -> dict[str, str]:
    abstracts: dict[str, str] = {}
    for i in range(0, len(pmids), BATCH_SIZE):
        batch = pmids[i:i + BATCH_SIZE]
        params = urllib.parse.urlencode({
            "db": "pubmed",
            "id": ",".join(batch),
            "rettype": "xml",
            "retmode": "xml",
        })
        url = f"{EFETCH_URL}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "LiteratureReviewSkill/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            xml_data = resp.read().decode("utf-8")

        root = ET.fromstring(xml_data)
        for article in root.findall(".//PubmedArticle"):
            pmid_el = article.find(".//PMID")
            if pmid_el is None:
                continue
            pmid = pmid_el.text

            abstract_parts = article.findall(".//AbstractText")
            if abstract_parts:
                parts = []
                for part in abstract_parts:
                    label = part.get("Label", "")
                    text = "".join(part.itertext()).strip()
                    if label:
                        parts.append(f"{label}: {text}")
                    else:
                        parts.append(text)
                abstracts[pmid] = " ".join(parts)

        if i + BATCH_SIZE < len(pmids):
            time.sleep(0.4)

    return abstracts


def make_bibtex_key(article: dict[str, Any]) -> str:
    authors = article.get("authors", "")
    last_name = ""
    if isinstance(authors, list):
        if authors:
            last_name = authors[0].split()[0].rstrip(",")
    elif authors:
        first_entry = authors.split(";")[0].strip()
        parts = first_entry.split()
        if len(parts) >= 2:
            last_name = parts[0].rstrip(",")
        elif parts:
            last_name = parts[0]
    if not last_name:
        last_name = article.get("first_author", "Unknown")
    year = str(article.get("year", "0000"))
    return f"{last_name}_{year}"


def deduplicate_keys(keys: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    for k in keys:
        counts[k] = counts.get(k, 0) + 1

    duplicates = {k for k, v in counts.items() if v > 1}
    if not duplicates:
        return keys

    suffix_counters: dict[str, int] = {}
    result = []
    for k in keys:
        if k in duplicates:
            suffix_counters[k] = suffix_counters.get(k, 0) + 1
            result.append(f"{k}{chr(96 + suffix_counters[k])}")
        else:
            result.append(k)
    return result


def extract_context(abstract: str, match_start: int, match_end: int, window: int = 80) -> str:
    start = max(0, match_start - window)
    end = min(len(abstract), match_end + window)

    snippet = abstract[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(abstract):
        snippet = snippet + "..."
    return snippet


def extract_claims(abstract: str) -> list[dict[str, str]]:
    if not abstract:
        return []

    claims: list[dict[str, str]] = []
    seen: set[str] = set()

    for m in STAT_PATTERN.finditer(abstract):
        value = m.group(0).strip()
        if value in seen:
            continue
        seen.add(value)
        claims.append({
            "type": "statistic",
            "value": value,
            "verbatim": extract_context(abstract, m.start(), m.end()),
        })

    for m in NUM_PATTERN.finditer(abstract):
        value = m.group(0).strip()
        if value in seen or len(value) == 1:
            continue

        already_in_stat = any(
            m.start() >= sm.start() and m.end() <= sm.end()
            for sm in STAT_PATTERN.finditer(abstract)
        )
        if already_in_stat:
            continue

        seen.add(value)
        claim_type = "percentage" if "%" in value else "number"
        claims.append({
            "type": claim_type,
            "value": value,
            "verbatim": extract_context(abstract, m.start(), m.end()),
        })

    return claims


def process_articles(
    results: list[dict[str, Any]],
    rows: list[int] | None = None,
    dois: list[str] | None = None,
    fetch_missing: bool = False,
) -> dict[str, Any]:
    if rows:
        selected = [results[i - 1] for i in rows if 1 <= i <= len(results)]
    elif dois:
        dois_lower = {d.lower().strip() for d in dois}
        selected = [r for r in results if r.get("doi", "").lower().strip() in dois_lower]
    else:
        selected = results

    if fetch_missing:
        missing_pmids = [
            str(a["pmid"]) for a in selected
            if not a.get("abstract") and a.get("pmid")
        ]
        if missing_pmids:
            print(f"Fetching {len(missing_pmids)} abstracts from PubMed...", file=sys.stderr)
            fetched = fetch_abstracts_from_pubmed(missing_pmids)
            print(f"  Retrieved {len(fetched)} abstracts", file=sys.stderr)
            for a in selected:
                pmid = str(a.get("pmid", ""))
                if not a.get("abstract") and pmid in fetched:
                    a["abstract"] = fetched[pmid]

    raw_keys = [make_bibtex_key(a) for a in selected]
    keys = deduplicate_keys(raw_keys)

    extraction: dict[str, Any] = {}
    stats = {"total": len(selected), "with_abstract": 0, "with_claims": 0, "total_claims": 0}

    for key, article in zip(keys, selected):
        abstract = article.get("abstract", "")
        entry: dict[str, Any] = {
            "title": article.get("title", ""),
            "doi": article.get("doi", ""),
            "pmid": article.get("pmid", ""),
            "year": article.get("year", ""),
            "has_abstract": bool(abstract),
            "abstract_snippet": abstract[:200] + "..." if len(abstract) > 200 else abstract,
            "claims": [],
        }

        if abstract:
            stats["with_abstract"] += 1
            claims = extract_claims(abstract)
            entry["claims"] = claims
            if claims:
                stats["with_claims"] += 1
                stats["total_claims"] += len(claims)

        extraction[key] = entry

    return {"stats": stats, "articles": extraction}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract quantitative claims from article abstracts."
    )
    parser.add_argument("file", help="Path to combined_results.json")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--rows", nargs="+", type=int, help="Row numbers (1-based)")
    group.add_argument("--dois", nargs="+", help="DOIs to extract")
    group.add_argument(
        "--from-bib",
        help="Extract all articles cited in a .bib file (matches by DOI)",
    )
    parser.add_argument(
        "--output",
        default="review/extracted_claims.json",
        help="Output JSON file (default: review/extracted_claims.json)",
    )
    parser.add_argument(
        "--fetch-abstracts",
        action="store_true",
        help="Fetch missing abstracts from PubMed via PMID",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f"File not found: {args.file}")

    with open(args.file, "r", encoding="utf-8") as f:
        results = json.load(f)

    dois_list = args.dois
    if args.from_bib:
        if not os.path.isfile(args.from_bib):
            parser.error(f"Bib file not found: {args.from_bib}")
        with open(args.from_bib, "r", encoding="utf-8") as f:
            bib_content = f.read()
        dois_list = re.findall(r"doi\s*=\s*\{([^}]+)\}", bib_content, re.IGNORECASE)
        dois_list = [d.strip() for d in dois_list if d.strip()]
        print(f"Found {len(dois_list)} DOIs in {args.from_bib}", file=sys.stderr)

    output = process_articles(
        results, rows=args.rows, dois=dois_list, fetch_missing=args.fetch_abstracts
    )

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    s = output["stats"]
    print(f"Extracted claims from {s['total']} articles:")
    print(f"  With abstract: {s['with_abstract']}")
    print(f"  With claims:   {s['with_claims']}")
    print(f"  Total claims:  {s['total_claims']}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()
