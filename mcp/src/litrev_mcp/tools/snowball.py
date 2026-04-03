"""MCP tool: citation chaining (backward/forward) via Semantic Scholar and OpenAlex."""

import json
import os
import re
import sys

from ..lib.http import S2_CLIENT, OA_CLIENT, request_with_retry, s2_throttle
from ..lib.dedup import deduplicate_simple

S2_BASE = "https://api.semanticscholar.org/graph/v1/paper"
S2_FIELDS = "title,authors,year,externalIds,journal,citationCount,abstract,url"

OA_BASE = "https://api.openalex.org/works"


def _resolve_s2_id(paper: dict) -> str | None:
    doi = (paper.get("doi") or "").strip()
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


def _fetch_s2_references(paper_id: str, limit: int = 500) -> list[dict]:
    s2_throttle()
    url = f"{S2_BASE}/{paper_id}/references"
    params = {"fields": S2_FIELDS, "limit": min(limit, 500)}
    try:
        resp = request_with_retry(
            "GET", url, params=params, timeout=15, client=S2_CLIENT
        )
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


def _fetch_s2_citations(paper_id: str, limit: int = 500) -> list[dict]:
    s2_throttle()
    url = f"{S2_BASE}/{paper_id}/citations"
    params = {"fields": S2_FIELDS, "limit": min(limit, 500)}
    try:
        resp = request_with_retry(
            "GET", url, params=params, timeout=15, client=S2_CLIENT
        )
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
    pmid = (
        (ids.get("pmid") or "")
        .replace("https://pubmed.ncbi.nlm.nih.gov/", "")
        .rstrip("/")
    )
    authorships = w.get("authorships") or []
    authors = []
    for a in authorships:
        name = (a.get("author") or {}).get("display_name", "")
        if name:
            authors.append(name)
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
        "url": w.get("id") or "",
        "source": source_label,
    }
    if authors:
        record["first_author"] = re.split(r"[,\s]", authors[0])[0]
    return record


def _fetch_oa_references(doi: str) -> list[dict]:
    oa_id = f"https://doi.org/{doi}"
    try:
        resp = request_with_retry(
            "GET",
            f"{OA_BASE}/{oa_id}",
            params={
                "select": "referenced_works",
            },
            timeout=15,
            client=OA_CLIENT,
        )
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        ref_ids = resp.json().get("referenced_works") or []
        if not ref_ids:
            return []
        results = []
        for start in range(0, len(ref_ids), 50):
            batch = ref_ids[start : start + 50]
            pipe_filter = "|".join(batch)
            resp2 = request_with_retry(
                "GET",
                OA_BASE,
                params={
                    "filter": f"openalex:{pipe_filter}",
                    "per_page": 50,
                    "select": "display_name,doi,ids,authorships,publication_year,cited_by_count,primary_location",
                },
                timeout=15,
                client=OA_CLIENT,
            )
            resp2.raise_for_status()
            for w in resp2.json().get("results", []):
                rec = _oa_work_to_record(w, "OA-backward")
                if rec:
                    results.append(rec)
        return results
    except Exception as e:
        print(f"  OpenAlex references error for {doi}: {e}", file=sys.stderr)
        return []


def _fetch_oa_citations(doi: str, limit: int = 200) -> list[dict]:
    try:
        resp = request_with_retry(
            "GET",
            OA_BASE,
            params={
                "filter": f"cites:https://doi.org/{doi}",
                "per_page": min(limit, 200),
                "sort": "cited_by_count:desc",
                "select": "display_name,doi,ids,authorships,publication_year,cited_by_count,primary_location",
            },
            timeout=15,
            client=OA_CLIENT,
        )
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


def citation_chain(
    results_path: str,
    indices: list[int],
    *,
    direction: str = "both",
    sources: str = "s2,openalex",
    output_path: str = "review/chaining_candidates.json",
) -> dict:
    with open(results_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    seed_pairs = [(r, existing[r]) for r in indices if 0 <= r < len(existing)]
    if not seed_pairs:
        return {"error": "No valid seed papers found for given row numbers."}

    directions = [direction] if direction != "both" else ["backward", "forward"]
    source_list = [s.strip() for s in sources.split(",")]

    all_found: list[dict] = []
    seed_log: list[dict] = []

    for row_idx, paper in seed_pairs:
        title_short = (paper.get("title") or "?")[:60]
        s2_id = _resolve_s2_id(paper)
        doi = (paper.get("doi") or "").strip()
        entry_log = {"index": row_idx, "title": title_short, "refs": 0, "cites": 0}

        if "backward" in directions:
            if "s2" in source_list and s2_id:
                refs = _fetch_s2_references(s2_id)
                entry_log["refs"] += len(refs)
                all_found.extend(refs)
            if "openalex" in source_list and doi:
                refs = _fetch_oa_references(doi)
                entry_log["refs"] += len(refs)
                all_found.extend(refs)

        if "forward" in directions:
            if "s2" in source_list and s2_id:
                cits = _fetch_s2_citations(s2_id)
                entry_log["cites"] += len(cits)
                all_found.extend(cits)
            if "openalex" in source_list and doi:
                cits = _fetch_oa_citations(doi)
                entry_log["cites"] += len(cits)
                all_found.extend(cits)

        seed_log.append(entry_log)

    raw_count = len(all_found)
    deduped_raw = deduplicate_simple(all_found)
    deduped_count = len(deduped_raw)

    from ..lib.dedup import deduplicate_merge

    existing_deduped = deduplicate_merge(existing)
    combined = existing_deduped + deduped_raw
    full_dedup = deduplicate_merge(combined)
    new_candidates = full_dedup[len(existing_deduped) :]

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(new_candidates, f, indent=2, ensure_ascii=False)

    return {
        "output_path": output_path,
        "seeds": len(seed_pairs),
        "directions": directions,
        "sources": source_list,
        "raw_results": raw_count,
        "after_internal_dedup": deduped_count,
        "new_unique_candidates": len(new_candidates),
        "seed_log": seed_log,
    }
