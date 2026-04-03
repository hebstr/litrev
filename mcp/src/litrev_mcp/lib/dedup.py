"""Deduplication utilities for literature search results.

Two variants:
- deduplicate_simple: fast, first-seen wins (from snowball)
- deduplicate_merge: merges non-empty fields from duplicates (from search)
"""

import re


def deduplicate_simple(results: list[dict]) -> list[dict]:
    seen_pmids: set[str] = set()
    seen_dois: set[str] = set()
    seen_titles: set[str] = set()
    unique: list[dict] = []

    for result in results:
        pmid = str(result.get("pmid", "")).strip()
        doi = (result.get("doi") or "").lower().strip()
        title = re.sub(r"[^a-z0-9]", "", (result.get("title") or "").lower())

        if pmid and pmid in seen_pmids:
            continue
        if doi and doi in seen_dois:
            continue
        if title and title in seen_titles:
            continue

        if pmid:
            seen_pmids.add(pmid)
        if doi:
            seen_dois.add(doi)
        if title:
            seen_titles.add(title)

        unique.append(result)

    return unique


def deduplicate_merge(
    results: list[dict], *, track_stats: bool = False
) -> list[dict] | tuple[list[dict], dict[str, int]]:
    pmid_to_idx: dict[str, int] = {}
    doi_to_idx: dict[str, int] = {}
    title_to_idx: dict[str, int] = {}
    unique: list[dict] = []
    stats = {"by_pmid": 0, "by_doi": 0, "by_title": 0}

    for result in results:
        pmid = str(result.get("pmid", "")).strip()
        doi = (result.get("doi") or "").lower().strip()
        title = re.sub(r"[^a-z0-9]", "", (result.get("title") or "").lower())

        existing_idx = None
        if pmid and pmid in pmid_to_idx:
            existing_idx = pmid_to_idx[pmid]
            stats["by_pmid"] += 1
        elif doi and doi in doi_to_idx:
            existing_idx = doi_to_idx[doi]
            stats["by_doi"] += 1
        elif title and title in title_to_idx:
            existing_idx = title_to_idx[title]
            stats["by_title"] += 1

        if existing_idx is not None:
            existing = unique[existing_idx]
            for key, value in result.items():
                if value and not existing.get(key):
                    existing[key] = value
            continue

        idx = len(unique)
        if pmid:
            pmid_to_idx[pmid] = idx
        if doi:
            doi_to_idx[doi] = idx
        if title:
            title_to_idx[title] = idx

        unique.append(result)

    if track_stats:
        return unique, stats
    return unique
