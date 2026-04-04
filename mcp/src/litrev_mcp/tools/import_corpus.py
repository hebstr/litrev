"""MCP tool: import user-supplied bibliographic files into the pipeline.

Supports BibTeX, RIS, CSV (Scopus), TSV (Web of Science), PMID list, DOI list.
Parses → enriches sparse records → writes normalised JSON compatible with
combined_results.json.
"""

import json
import os

from ..lib.parsers import Format, detect_format, parse
from ..lib.enrich import enrich_records


def import_corpus(
    file_path: str,
    *,
    format: Format | None = None,
    enrich: bool = True,
    output_path: str | None = None,
) -> dict:
    """Parse a bibliographic file and enrich sparse records.

    Args:
        file_path: Path to the import file.
        format: Explicit format override. Auto-detected if omitted.
        enrich: Fetch missing metadata from PubMed/CrossRef/OpenAlex (default: true).
        output_path: Where to write results JSON. Defaults to <dir>/imported_results.json.

    Returns:
        Status dict with counts and output path.
    """
    if not os.path.isfile(file_path):
        return {"status": "error", "error": f"File not found: {file_path}"}

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    try:
        if format is None:
            format = detect_format(text)
        records = parse(text, fmt=format)
    except ValueError as e:
        return {"status": "error", "error": str(e)}

    if not records:
        return {
            "status": "ok",
            "format": format,
            "parsed": 0,
            "enrichment": None,
            "output_path": None,
        }

    enrichment_stats = None
    if enrich:
        enrichment_stats = enrich_records(records)

    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(file_path) or ".", "imported_results.json"
        )

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    return {
        "status": "ok",
        "format": format,
        "parsed": len(records),
        "enrichment": enrichment_stats,
        "output_path": output_path,
    }
