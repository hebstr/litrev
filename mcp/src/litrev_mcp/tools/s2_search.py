"""MCP tool: keyword search on Semantic Scholar Academic Graph API."""

import json
import os
import re

from ..lib.http import S2_CLIENT, S2_API_KEY, s2_throttle, request_with_retry

S2_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_FIELDS = "title,authors,year,externalIds,journal,citationCount,abstract,url"


def _s2_result_to_record(p: dict) -> dict | None:
    title = p.get("title")
    if not title:
        return None
    ext = p.get("externalIds") or {}
    authors_raw = p.get("authors") or []
    authors = [a.get("name", "") for a in authors_raw if a.get("name")]
    record = {
        "title": title,
        "authors": authors,
        "year": str(p.get("year") or ""),
        "doi": ext.get("DOI", ""),
        "pmid": ext.get("PubMed", ""),
        "journal": (p.get("journal") or {}).get("name", ""),
        "abstract": p.get("abstract") or "",
        "citations": p.get("citationCount") or 0,
        "url": p.get("url", ""),
        "source": "S2-search",
    }
    if authors:
        record["first_author"] = re.split(r"[,\s]", authors[0])[0]
    return record


def search_s2(
    query: str,
    *,
    year_start: int | None = None,
    year_end: int | None = None,
    fields_of_study: str | None = "Medicine",
    limit: int = 100,
    output_path: str | None = None,
) -> dict:
    params: dict = {
        "query": query,
        "fields": S2_FIELDS,
        "limit": min(limit, 100),
    }
    if year_start and year_end:
        params["year"] = f"{year_start}-{year_end}"
    elif year_start:
        params["year"] = f"{year_start}-"
    elif year_end:
        params["year"] = f"-{year_end}"
    if fields_of_study:
        params["fieldsOfStudy"] = fields_of_study

    s2_throttle()
    try:
        resp = request_with_retry(
            "GET",
            S2_SEARCH_URL,
            params=params,
            timeout=15,
            client=S2_CLIENT,
        )
        resp.raise_for_status()
        body = resp.json()
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "has_api_key": bool(S2_API_KEY),
            "results": [],
            "total": 0,
        }

    total = body.get("total", 0)
    raw_papers = body.get("data", [])
    records = []
    for p in raw_papers:
        rec = _s2_result_to_record(p)
        if rec:
            records.append(rec)

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

    return {
        "status": "ok",
        "has_api_key": bool(S2_API_KEY),
        "query": query,
        "total_in_s2": total,
        "returned": len(records),
        "output_path": output_path,
        "results": records if not output_path else [],
    }
