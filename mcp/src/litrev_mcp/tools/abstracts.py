"""MCP tool: fetch missing abstracts from PubMed and format for screening."""

import json
import os
import tempfile

from ..lib.pubmed import fetch_abstracts_from_pubmed


def _format_articles(indexed_articles: list[tuple[int, dict]]) -> str:
    lines = []
    for idx, a in indexed_articles:
        title = a.get("title", "Untitled")
        authors = a.get("authors", "Unknown")
        if isinstance(authors, list):
            authors = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")
        year = a.get("year", "N/A")
        doi = a.get("doi", "")
        pmid = a.get("pmid", "")
        abstract = a.get("abstract") or "No abstract available"
        study_type = a.get("study_type", "")

        lines.append(f"## [{idx}] {title}")
        lines.append(f"**{authors} ({year})**")
        meta_parts = []
        if doi:
            meta_parts.append(f"DOI: {doi}")
        if pmid:
            meta_parts.append(f"PMID: {pmid}")
        if study_type:
            meta_parts.append(f"Type: {study_type}")
        if meta_parts:
            lines.append(" | ".join(meta_parts))
        lines.append(f"\n{abstract}\n")
        lines.append("---\n")
    return "\n".join(lines)


def fetch_abstracts(
    results_path: str,
    indices: list[int],
    *,
    fetch_missing: bool = True,
    output_path: str | None = None,
) -> dict:
    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    indexed_articles = [(i, results[i]) for i in indices if 0 <= i < len(results)]
    if not indexed_articles:
        return {"error": "No matching articles found for given indices."}

    backfilled = 0
    fetch_attempted = 0
    if fetch_missing:
        missing_pmids: dict[str, int] = {}
        for idx, a in indexed_articles:
            if not a.get("abstract") and a.get("pmid"):
                pmid_key = str(a["pmid"])
                if pmid_key not in missing_pmids:
                    missing_pmids[pmid_key] = idx

        fetch_attempted = len(missing_pmids)
        if missing_pmids:
            fetched = fetch_abstracts_from_pubmed(list(missing_pmids.keys()))
            for pmid, abstract in fetched.items():
                idx = missing_pmids[pmid]
                results[idx]["abstract"] = abstract
                backfilled += 1

            if backfilled > 0:
                tmp_fd, tmp_path = tempfile.mkstemp(
                    dir=os.path.dirname(os.path.abspath(results_path)), suffix=".tmp"
                )
                try:
                    with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                        json.dump(results, f, indent=2, ensure_ascii=False)
                    os.replace(tmp_path, results_path)
                except BaseException:
                    os.unlink(tmp_path)
                    raise

    with_abstract = sum(1 for _, a in indexed_articles if a.get("abstract"))
    without_abstract = len(indexed_articles) - with_abstract

    output = _format_articles(indexed_articles)

    out_path = output_path or "review/abstracts_for_screening.md"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)

    return {
        "output_path": out_path,
        "total": len(indexed_articles),
        "with_abstract": with_abstract,
        "without_abstract": without_abstract,
        "fetch_attempted": fetch_attempted,
        "fetched_from_pubmed": backfilled,
    }
