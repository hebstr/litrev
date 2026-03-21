#!/usr/bin/env python3
"""
Extract quantitative claims from abstracts of selected articles.

Produces a structured JSON file mapping each article's BibTeX key to the
numerical claims found in its abstract. This file serves as the single
source of truth for numbers that may be cited in the review.

Usage:
    python extract_data.py review/combined_results.json \
        --rows 0 2 12 33 \
        --output review/extracted_claims.json
"""

import argparse
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from typing import Any

import requests

sys.path.insert(0, os.path.dirname(__file__))
from claim_patterns import extract_claims
from bibtex_keys import unique_key as _unique_key
from http_utils import request_with_retry as _request_with_retry, ncbi_params as _ncbi_params


EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BATCH_SIZE = 200


def fetch_abstracts_from_pubmed(pmids: list[str]) -> dict[str, str]:
    abstracts: dict[str, str] = {}
    for i in range(0, len(pmids), BATCH_SIZE):
        batch = pmids[i:i + BATCH_SIZE]
        try:
            response = _request_with_retry(
                "GET", EFETCH_URL,
                params=_ncbi_params({
                    "db": "pubmed",
                    "id": ",".join(batch),
                    "rettype": "xml",
                    "retmode": "xml",
                }),
                timeout=30,
            )
            response.raise_for_status()
            root = ET.fromstring(response.text)  # safe: CPython expat doesn't resolve external entities (no XXE)
        except (requests.RequestException, ET.ParseError) as e:
            print(f"  Batch {i//BATCH_SIZE + 1} failed ({len(batch)} PMIDs): {e}", file=sys.stderr)
            continue

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
    last_name = article.get("first_author", "")
    if not last_name:
        authors = article.get("authors", "")
        if isinstance(authors, list):
            parts = authors[0].split() if authors else []
            if parts:
                last_name = parts[0].rstrip(",")
        elif authors:
            first_entry = authors.split(";")[0].split(",")[0].strip()
            parts = first_entry.split()
            if parts:
                last_name = parts[0]
    if not last_name:
        last_name = "Unknown"
    last_name = last_name.replace(" ", "")
    year = str(article.get("year", "0000"))
    return f"{last_name}_{year}"


def deduplicate_keys(keys: list[str]) -> list[str]:
    seen: set[str] = set()
    first_index: dict[str, int] = {}
    result: list[str] = []
    for i, base_key in enumerate(keys):
        new_key, renamed = _unique_key(base_key, seen)
        if renamed:
            old_name, new_name = renamed
            idx = first_index.pop(old_name)
            result[idx] = new_name
            first_index[new_name] = idx
        first_index[new_key] = len(result)
        result.append(new_key)
    return result


def process_articles(
    results: list[dict[str, Any]],
    rows: list[int] | None = None,
    dois: list[str] | None = None,
    fetch_missing: bool = False,
) -> dict[str, Any]:
    if rows:
        selected = [results[i] for i in rows if 0 <= i < len(results)]
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
    group.add_argument("--rows", nargs="+", type=int, help="Row numbers (0-based, matching combined_results.json array indices)")
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
