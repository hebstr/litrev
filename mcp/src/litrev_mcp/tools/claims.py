"""MCP tool: regex-based quantitative claim extraction from abstracts."""

import json
import os
import tempfile
from typing import Any

from ..lib.pubmed import fetch_abstracts_from_pubmed
from ..lib.patterns import extract_claims
from ..lib.bibtex import make_bibtex_key, deduplicate_keys


def extract_claims_regex(
    results_path: str,
    *,
    indices: list[int] | None = None,
    indices_file: str | None = None,
    fetch_missing: bool = True,
    output_path: str = "review/extracted_claims.json",
) -> dict:
    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    if indices_file:
        with open(indices_file, "r", encoding="utf-8") as f:
            idx_list = json.load(f)
    elif indices is not None:
        idx_list = indices
    else:
        idx_list = list(range(len(results)))

    idx_list = [i for i in idx_list if 0 <= i < len(results)]
    selected = [results[i] for i in idx_list]

    base_dir = os.path.dirname(os.path.abspath(results_path))
    if not os.path.isabs(output_path):
        output_path = os.path.join(base_dir, output_path)

    backfilled = 0
    if fetch_missing:
        missing_pmids = [
            str(a["pmid"]) for a in selected if not a.get("abstract") and a.get("pmid")
        ]
        if missing_pmids:
            fetched = fetch_abstracts_from_pubmed(missing_pmids)
            for a in selected:
                pmid = str(a.get("pmid", ""))
                if not a.get("abstract") and pmid in fetched:
                    a["abstract"] = fetched[pmid]
                    backfilled += 1

            if backfilled > 0:
                tmp_fd, tmp_path = tempfile.mkstemp(
                    dir=os.path.dirname(os.path.abspath(results_path)),
                    suffix=".tmp",
                )
                try:
                    with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                        json.dump(results, f, indent=2, ensure_ascii=False)
                    os.replace(tmp_path, results_path)
                except BaseException:
                    os.unlink(tmp_path)
                    raise

    raw_keys = [make_bibtex_key(a) for a in selected]
    keys = deduplicate_keys(raw_keys)

    extraction: dict[str, Any] = {}
    stats = {
        "total": len(selected),
        "with_abstract": 0,
        "with_claims": 0,
        "total_quantitative_claims": 0,
    }

    for key, article, idx in zip(keys, selected, idx_list):
        abstract = article.get("abstract", "")
        entry: dict[str, Any] = {
            "index": idx,
            "title": article.get("title", ""),
            "doi": article.get("doi", ""),
            "pmid": article.get("pmid", ""),
            "year": article.get("year", ""),
            "study_type": article.get("study_type", ""),
            "has_abstract": bool(abstract),
            "abstract_snippet": abstract[:200] + "..."
            if len(abstract) > 200
            else abstract,
            "claims": [],
        }

        if abstract:
            stats["with_abstract"] += 1
            found_claims = extract_claims(abstract)
            entry["claims"] = found_claims
            if found_claims:
                stats["with_claims"] += 1
                stats["total_quantitative_claims"] += len(found_claims)

        extraction[key] = entry

    output = {"stats": stats, "articles": extraction}

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return {
        "output_path": output_path,
        "stats": stats,
    }
