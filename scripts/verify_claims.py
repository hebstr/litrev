#!/usr/bin/env python3
"""
Cross-verify numerical claims in a review document against extracted data.

Reads the review markdown, finds every number associated with a [@citation],
and checks whether that number appears in the extracted_claims.json for the
corresponding article. Produces an audit report with status:
  - VERIFIED: number found in the article's abstract
  - UNVERIFIED: number NOT found in the abstract (may be from full-text)
  - NO_ABSTRACT: article had no abstract to check against
  - NO_EXTRACTION: article not in the extraction file

Usage:
    python verify_claims.py review/<topic>_review.md \
        --claims review/extracted_claims.json \
        --output review/claims_audit.json
"""

import argparse
import json
import os
import re
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(__file__))
from bibtex_keys import parse_bib_keys_to_doi as _parse_bib_keys_to_doi
from claim_patterns import STAT_PATTERN as _STAT_PATTERN, NUM_PATTERN as _NUM_PATTERN

_CITE_RE = re.compile(
    r"\[@([\w-]+(?:_\d{4}[a-z]?)(?:\s*;\s*@[\w-]+(?:_\d{4}[a-z]?))*)\]"
)  # \w = [a-zA-Z0-9_]; dots excluded — safe because build_bibtex_entry strips them from all keys

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


def build_doi_index(extraction: dict[str, Any]) -> dict[str, str]:
    doi_to_key: dict[str, str] = {}
    for ext_key, article in extraction.get("articles", {}).items():
        doi = article.get("doi", "").strip().lower()
        if doi:
            doi_to_key[doi] = ext_key
    return doi_to_key


def resolve_key(
    review_key: str,
    articles: dict[str, Any],
    bib_dois: dict[str, str],
    doi_index: dict[str, str],
) -> str | None:
    # extract_data.py and generate_bib.py generate keys independently.
    # Direct match handles the common case; DOI fallback bridges when keys
    # diverge (e.g. collision dedup ordering, doi.org non-standard keys).
    if review_key in articles:
        return review_key
    doi = bib_dois.get(review_key, "")
    if doi and doi in doi_index:
        return doi_index[doi]
    return None


def normalize_number(value: str) -> str:
    return value.replace(",", ".").replace(" ", "").replace("\u00a0", "")


def number_matches(review_num: str, claim_value: str) -> bool:
    norm_review = normalize_number(review_num)
    norm_claim = normalize_number(claim_value)
    return bool(re.search(rf'(?<!\d)(?<!\.){re.escape(norm_review)}(?!\d)(?!\.\d)', norm_claim))


def extract_review_claims(text: str) -> list[dict[str, str]]:
    claims: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for cite_m in _CITE_RE.finditer(text):
        keys = re.findall(r"@?([\w-]+(?:_\d{4}[a-z]?))", cite_m.group(1))
        sent_start, sent_end = _split_sentence(text, cite_m.start())
        sentence = text[sent_start:sent_end]
        offset = sent_start

        stat_spans: list[tuple[int, int]] = []
        for m in _STAT_PATTERN.finditer(sentence):
            stat_value = m.group(0).strip()
            stat_spans.append((m.start(), m.end()))
            for key in keys:
                pair = (stat_value, key)
                if pair not in seen:
                    seen.add(pair)
                    ctx_start = max(0, offset + m.start() - 40)
                    ctx_end = min(len(text), cite_m.end() + 10)
                    claims.append({
                        "value": stat_value,
                        "type": "statistic",
                        "citation_key": key,
                        "context": text[ctx_start:ctx_end].replace("\n", " ").strip(),
                    })

        for m in _NUM_PATTERN.finditer(sentence):
            num_value = m.group(0).strip()
            if len(num_value) == 1:
                continue
            already_in_stat = any(
                m.start() >= ss and m.end() <= se
                for ss, se in stat_spans
            )
            if already_in_stat:
                continue
            abs_start = offset + m.start()
            abs_end = offset + m.end()
            pct_check = text[abs_start:min(abs_end + 2, len(text))]
            if "%" in pct_check:
                num_value += "%"
            for key in keys:
                pair = (num_value, key)
                if pair not in seen:
                    seen.add(pair)
                    ctx_start = max(0, abs_start - 20)
                    ctx_end = min(len(text), cite_m.end() + 10)
                    claims.append({
                        "value": num_value,
                        "type": "percentage" if "%" in num_value else "number",
                        "citation_key": key,
                        "context": text[ctx_start:ctx_end].replace("\n", " ").strip(),
                    })

    return claims


def verify(
    review_claims: list[dict[str, str]],
    extraction: dict[str, Any],
    bib_dois: dict[str, str] | None = None,
) -> dict[str, Any]:
    articles = extraction.get("articles", {})
    doi_index = build_doi_index(extraction)
    if bib_dois is None:
        bib_dois = {}
    results: list[dict[str, Any]] = []
    summary = {"verified": 0, "unverified": 0, "no_abstract": 0, "no_extraction": 0, "total": 0}

    for claim in review_claims:
        summary["total"] += 1
        key = claim["citation_key"]
        resolved = resolve_key(key, articles, bib_dois, doi_index)
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
            entry["detail"] = f"Key '{key}' not found in extracted_claims.json (no DOI match either)"
            summary["no_extraction"] += 1
        elif not articles[resolved].get("has_abstract", False):
            entry["status"] = "NO_ABSTRACT"
            entry["detail"] = "Article had no abstract available"
            summary["no_abstract"] += 1
        else:
            article_claims = articles[resolved].get("claims", [])
            matched = False
            for ac in article_claims:
                if number_matches(claim["value"], ac["value"]):
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

    return {"summary": summary, "claims": results}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cross-verify review claims against extracted data."
    )
    parser.add_argument("review", help="Path to the review markdown file")
    parser.add_argument(
        "--claims",
        default="review/extracted_claims.json",
        help="Path to extracted_claims.json (default: review/extracted_claims.json)",
    )
    parser.add_argument(
        "--bib",
        default=None,
        help="Path to references.bib for DOI-based key resolution (auto-detected if not set)",
    )
    parser.add_argument(
        "--output",
        default="review/claims_audit.json",
        help="Output audit report (default: review/claims_audit.json)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.review):
        parser.error(f"Review file not found: {args.review}")
    if not os.path.isfile(args.claims):
        parser.error(f"Claims file not found: {args.claims}")

    bib_path = args.bib
    if bib_path is None:
        candidate = os.path.join(os.path.dirname(args.review), "references.bib")
        if os.path.isfile(candidate):
            bib_path = candidate

    bib_dois: dict[str, str] = {}
    if bib_path:
        bib_dois = _parse_bib_keys_to_doi(bib_path)
        print(f"Loaded {len(bib_dois)} DOI mappings from {bib_path}")

    with open(args.review, "r", encoding="utf-8") as f:
        review_text = f.read()

    with open(args.claims, "r", encoding="utf-8") as f:
        extraction = json.load(f)

    review_claims = extract_review_claims(review_text)
    audit = verify(review_claims, extraction, bib_dois)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)

    s = audit["summary"]
    total = s["total"]
    print(f"Claims audit: {total} numerical claims found in review")
    print(f"  VERIFIED:      {s['verified']}")
    print(f"  UNVERIFIED:    {s['unverified']}")
    print(f"  NO_ABSTRACT:   {s['no_abstract']}")
    print(f"  NO_EXTRACTION: {s['no_extraction']}")

    if s["unverified"] > 0:
        print(f"\n⚠ {s['unverified']} claims could not be verified against abstracts.")
        print("These may be from full-text or may be hallucinated. Manual check required.")

    print(f"\nAudit report: {args.output}")


if __name__ == "__main__":
    main()
