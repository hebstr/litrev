"""MCP tool: keyword search on OpenAlex Works API."""

import json
import os
import re

from ..lib.http import OA_CLIENT, LITREV_EMAIL, request_with_retry

OA_SEARCH_URL = "https://api.openalex.org/works"


def _oa_result_to_record(work: dict) -> dict | None:
    title = work.get("title")
    if not title:
        return None

    authorships = work.get("authorships") or []
    authors = []
    for a in authorships:
        author = a.get("author") or {}
        name = author.get("display_name")
        if name:
            authors.append(name)

    doi_raw = work.get("doi") or ""
    doi = doi_raw.replace("https://doi.org/", "")

    pmid_raw = (work.get("ids") or {}).get("pmid", "") or ""
    pmid = pmid_raw.replace("https://pubmed.ncbi.nlm.nih.gov/", "").rstrip("/")

    primary_loc = work.get("primary_location") or {}
    source = primary_loc.get("source") or {}
    journal = source.get("display_name") or ""

    record = {
        "title": title,
        "authors": authors,
        "year": str(work.get("publication_year") or ""),
        "doi": doi,
        "pmid": pmid,
        "journal": journal,
        "abstract": "",
        "citations": work.get("cited_by_count") or 0,
        "url": work.get("id") or "",
        "source": "OpenAlex-search",
    }
    if authors:
        record["first_author"] = re.split(r"[,\s]", authors[0])[0]
    return record


def search_openalex(
    query: str,
    *,
    year_start: int | None = None,
    year_end: int | None = None,
    limit: int = 50,
    output_path: str | None = None,
) -> dict:
    filters = ["type:article"]
    if year_start and year_end:
        filters.append(f"publication_year:{year_start}-{year_end}")
    elif year_start:
        filters.append(f"publication_year:>={year_start}")
    elif year_end:
        filters.append(f"publication_year:<={year_end}")

    params: dict = {
        "search": query,
        "filter": ",".join(filters),
        "sort": "cited_by_count:desc",
        "per_page": min(limit, 200),
    }
    if LITREV_EMAIL:
        params["mailto"] = LITREV_EMAIL

    try:
        resp = request_with_retry(
            "GET",
            OA_SEARCH_URL,
            params=params,
            timeout=15,
            client=OA_CLIENT,
        )
        resp.raise_for_status()
        body = resp.json()
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "has_email": bool(LITREV_EMAIL),
            "results": [],
            "total_in_openalex": 0,
        }

    meta = body.get("meta") or {}
    total = meta.get("count", 0)
    raw_works = body.get("results") or []
    records = []
    for w in raw_works:
        rec = _oa_result_to_record(w)
        if rec:
            records.append(rec)

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

    return {
        "status": "ok",
        "has_email": bool(LITREV_EMAIL),
        "query": query,
        "total_in_openalex": total,
        "returned": len(records),
        "output_path": output_path,
        "results": records if not output_path else [],
    }
