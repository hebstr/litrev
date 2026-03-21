#!/usr/bin/env python3
"""
Citation chaining: find additional papers via backward and forward citation tracking.

Uses Semantic Scholar and OpenAlex APIs (both free, no key required) to retrieve
references (backward) and citations (forward) from seed papers, then deduplicates
against existing combined_results.json.
"""

import argparse
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from http_utils import request_with_retry
from process_results import deduplicate_results

S2_BASE = "https://api.semanticscholar.org/graph/v1/paper"
S2_FIELDS = "title,authors,year,externalIds,journal,citationCount,abstract,url"
S2_RATE_INTERVAL = 1.0

OA_BASE = "https://api.openalex.org/works"

_last_s2_call = 0.0


def _s2_throttle():
    global _last_s2_call
    now = time.monotonic()
    elapsed = now - _last_s2_call
    if elapsed < S2_RATE_INTERVAL:
        time.sleep(S2_RATE_INTERVAL - elapsed)
    _last_s2_call = time.monotonic()


def _resolve_s2_id(paper: dict) -> str | None:
    doi = paper.get("doi", "").strip()
    if doi:
        return f"DOI:{doi}"
    pmid = str(paper.get("pmid", "")).strip()
    if pmid:
        return f"PMID:{pmid}"
    return None


def _s2_paper_to_record(p: dict, source_label: str) -> dict | None:
    title = p.get("title")
    if not title:
        return None
    ext = p.get("externalIds") or {}
    authors_raw = p.get("authors") or []
    authors = [a.get("name", "") for a in authors_raw if a.get("name")]
    record = {
        "title": title,
        "authors": authors,
        "year": p.get("year") or "",
        "doi": ext.get("DOI", ""),
        "pmid": ext.get("PubMed", ""),
        "journal": (p.get("journal") or {}).get("name", ""),
        "abstract": p.get("abstract") or "",
        "citations": p.get("citationCount") or 0,
        "url": p.get("url", ""),
        "source": source_label,
    }
    if authors:
        record["first_author"] = re.split(r"[,\s]", authors[0])[0]
    return record


def fetch_s2_references(paper_id: str, limit: int = 500) -> list[dict]:
    _s2_throttle()
    url = f"{S2_BASE}/{paper_id}/references"
    params = {"fields": S2_FIELDS, "limit": min(limit, 500)}
    try:
        resp = request_with_retry("GET", url, params=params, timeout=15)
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        data = resp.json().get("data", [])
        results = []
        for item in data:
            cited = item.get("citedPaper")
            if cited:
                rec = _s2_paper_to_record(cited, "S2-backward")
                if rec:
                    results.append(rec)
        return results
    except Exception as e:
        print(f"  S2 references error for {paper_id}: {e}", file=sys.stderr)
        return []


def fetch_s2_citations(paper_id: str, limit: int = 500) -> list[dict]:
    _s2_throttle()
    url = f"{S2_BASE}/{paper_id}/citations"
    params = {"fields": S2_FIELDS, "limit": min(limit, 500)}
    try:
        resp = request_with_retry("GET", url, params=params, timeout=15)
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        data = resp.json().get("data", [])
        results = []
        for item in data:
            citing = item.get("citingPaper")
            if citing:
                rec = _s2_paper_to_record(citing, "S2-forward")
                if rec:
                    results.append(rec)
        return results
    except Exception as e:
        print(f"  S2 citations error for {paper_id}: {e}", file=sys.stderr)
        return []


def _oa_work_to_record(w: dict, source_label: str) -> dict | None:
    title = w.get("display_name") or w.get("title")
    if not title:
        return None
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    ids = w.get("ids") or {}
    pmid = (ids.get("pmid") or "").replace("https://pubmed.ncbi.nlm.nih.gov/", "").rstrip("/")
    authorships = w.get("authorships") or []
    authors = []
    for a in authorships:
        name = (a.get("author") or {}).get("display_name", "")
        if name:
            authors.append(name)
    journal = ""
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    journal = src.get("display_name", "")
    record = {
        "title": title,
        "authors": authors,
        "year": w.get("publication_year") or "",
        "doi": doi,
        "pmid": pmid,
        "journal": journal,
        "abstract": "",
        "citations": w.get("cited_by_count") or 0,
        "url": w.get("doi") or "",
        "source": source_label,
    }
    if authors:
        record["first_author"] = re.split(r"[,\s]", authors[0])[0]
    return record


def fetch_oa_references(doi: str) -> list[dict]:
    oa_id = f"https://doi.org/{doi}"
    try:
        resp = request_with_retry("GET", f"{OA_BASE}/{oa_id}", params={
            "select": "referenced_works",
        }, timeout=15)
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        ref_ids = resp.json().get("referenced_works") or []
        if not ref_ids:
            return []
        batch = ref_ids[:50]
        pipe_filter = "|".join(batch)
        resp2 = request_with_retry("GET", OA_BASE, params={
            "filter": f"openalex:{pipe_filter}",
            "per_page": 50,
            "select": "display_name,doi,ids,authorships,publication_year,cited_by_count,primary_location",
        }, timeout=15)
        resp2.raise_for_status()
        results = []
        for w in resp2.json().get("results", []):
            rec = _oa_work_to_record(w, "OA-backward")
            if rec:
                results.append(rec)
        return results
    except Exception as e:
        print(f"  OpenAlex references error for {doi}: {e}", file=sys.stderr)
        return []


def fetch_oa_citations(doi: str, limit: int = 200) -> list[dict]:
    try:
        resp = request_with_retry("GET", OA_BASE, params={
            "filter": f"cites:https://doi.org/{doi}",
            "per_page": min(limit, 200),
            "sort": "cited_by_count:desc",
            "select": "display_name,doi,ids,authorships,publication_year,cited_by_count,primary_location",
        }, timeout=15)
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        results = []
        for w in resp.json().get("results", []):
            rec = _oa_work_to_record(w, "OA-forward")
            if rec:
                results.append(rec)
        return results
    except Exception as e:
        print(f"  OpenAlex citations error for {doi}: {e}", file=sys.stderr)
        return []


def chain(seeds: list[dict], directions: list[str], sources: list[str]) -> list[dict]:
    all_found = []
    for i, paper in enumerate(seeds):
        title_short = (paper.get("title") or "?")[:60]
        print(f"\n[{i+1}/{len(seeds)}] {title_short}")

        s2_id = _resolve_s2_id(paper)
        doi = paper.get("doi", "").strip()

        if "backward" in directions:
            if "s2" in sources and s2_id:
                refs = fetch_s2_references(s2_id)
                print(f"  S2 backward: {len(refs)}")
                all_found.extend(refs)
            if "openalex" in sources and doi:
                refs = fetch_oa_references(doi)
                print(f"  OA backward: {len(refs)}")
                all_found.extend(refs)

        if "forward" in directions:
            if "s2" in sources and s2_id:
                cits = fetch_s2_citations(s2_id)
                print(f"  S2 forward: {len(cits)}")
                all_found.extend(cits)
            if "openalex" in sources and doi:
                cits = fetch_oa_citations(doi)
                print(f"  OA forward: {len(cits)}")
                all_found.extend(cits)

    return all_found


def main():
    parser = argparse.ArgumentParser(
        description="Citation chaining: find papers that cite or are cited by seed papers."
    )
    parser.add_argument("file", help="Path to combined_results.json")
    parser.add_argument("--rows", nargs="+", type=int, required=True,
                        help="0-based row numbers of seed papers in combined_results.json")
    parser.add_argument("--direction", choices=["backward", "forward", "both"], default="both",
                        help="Chaining direction (default: both)")
    parser.add_argument("--sources", default="s2,openalex",
                        help="Comma-separated API sources: s2,openalex (default: both)")
    parser.add_argument("--output", default="review/chaining_candidates.json",
                        help="Output file for new candidates (default: review/chaining_candidates.json)")
    parser.add_argument("--merge", action="store_true",
                        help="Merge new candidates into combined_results.json (with deduplication)")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f"File not found: {args.file}")

    with open(args.file, "r", encoding="utf-8") as f:
        existing = json.load(f)

    seeds = [existing[i] for i in args.rows if 0 <= i < len(existing)]
    if not seeds:
        print("Error: no valid seed papers found for the given row numbers.", file=sys.stderr)
        sys.exit(1)

    print(f"Seed papers: {len(seeds)}")
    print(f"Existing results: {len(existing)}")

    directions = [args.direction] if args.direction != "both" else ["backward", "forward"]
    sources = [s.strip() for s in args.sources.split(",")]

    raw = chain(seeds, directions, sources)
    print(f"\nRaw results from chaining: {len(raw)}")

    deduped_raw = deduplicate_results(raw)
    print(f"After internal deduplication: {len(deduped_raw)}")

    combined = existing + deduped_raw
    deduped_all = deduplicate_results(combined)
    new_count = len(deduped_all) - len(existing)
    new_candidates = deduped_all[len(existing):]
    print(f"New unique candidates (not in existing results): {new_count}")

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(new_candidates, f, indent=2, ensure_ascii=False)
    print(f"Candidates saved to: {args.output}")

    if args.merge:
        with open(args.file, "w", encoding="utf-8") as f:
            json.dump(deduped_all, f, indent=2, ensure_ascii=False)
        print(f"Merged into {args.file}: {len(deduped_all)} total results")

    print(f"\n{'='*60}")
    print("CITATION CHAINING SUMMARY")
    print(f"{'='*60}")
    print(f"Seed papers:          {len(seeds)}")
    print(f"Direction:            {', '.join(directions)}")
    print(f"Sources:              {', '.join(sources)}")
    print(f"Raw results:          {len(raw)}")
    print(f"New unique candidates: {new_count}")
    if args.merge:
        print(f"Total after merge:    {len(deduped_all)}")


if __name__ == "__main__":
    main()
