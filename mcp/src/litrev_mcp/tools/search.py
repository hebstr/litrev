"""Search-related MCP tools: process_results, deduplicate, rank, filter, format."""

import json
import os
import re
from datetime import datetime

from ..lib.bibtex import unique_key, build_bibtex_entry
from ..lib.dedup import deduplicate_merge


def _format_markdown(results: list[dict], top_n: int = 0) -> str:
    md = "# Literature Search Results\n\n"
    md += f"**Search Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    md += f"**Total Results**: {len(results)}\n\n"

    summary = generate_search_summary(results)

    md += "## Summary Statistics\n\n"
    md += f"- **Total**: {summary['total_results']}\n"
    if summary.get("total_citations"):
        md += f"- **Total Citations**: {summary['total_citations']}\n"
        md += f"- **Average Citations**: {summary['avg_citations']:.1f}\n"
    md += "\n"

    if summary["sources"]:
        md += "### Results by Source\n\n"
        for source, count in sorted(
            summary["sources"].items(), key=lambda x: x[1], reverse=True
        ):
            md += f"- {source}: {count}\n"
        md += "\n"

    if summary["year_distribution"]:
        md += "### Results by Year\n\n"
        for year, count in sorted(
            summary["year_distribution"].items(), key=lambda x: str(x[0]), reverse=True
        ):
            md += f"- {year}: {count}\n"
        md += "\n"

    study_types: dict[str, int] = {}
    for r in results:
        st = r.get("study_type") or r.get("publication_type") or "unspecified"
        study_types[st] = study_types.get(st, 0) + 1
    if study_types:
        md += "### Results by Study Type\n\n"
        for st, count in sorted(study_types.items(), key=lambda x: x[1], reverse=True):
            md += f"- {st}: {count}\n"
        md += "\n"

    if top_n > 0:
        top_results = sorted(
            results, key=lambda x: x.get("citations", 0), reverse=True
        )[:top_n]
        md += f"## Top {min(top_n, len(top_results))} Most-Cited Articles\n\n"
        for i, result in enumerate(top_results, 1):
            md += f"### {i}. {result.get('title', 'Untitled')}\n\n"
            authors = result.get("authors", "Unknown")
            if isinstance(authors, list):
                authors = ", ".join(authors[:3]) + (
                    " et al." if len(authors) > 3 else ""
                )
            md += f"**Authors**: {authors}\n\n"
            md += f"**Year**: {result.get('year', 'N/A')}"
            if result.get("journal"):
                md += f" | **Journal**: {result['journal']}"
            if result.get("citations"):
                md += f" | **Citations**: {result['citations']}"
            md += "\n\n"
            if result.get("doi"):
                md += f"**DOI**: {result['doi']}\n\n"
            if result.get("abstract"):
                md += f"**Abstract**: {result['abstract']}\n\n"
            md += "---\n\n"

    md += "## All Results\n\n"
    md += "| Rank | Title | First Author | Year | Journal | Citations | DOI |\n"
    md += "|------|-------|--------------|------|---------|-----------|-----|\n"
    for result in results:
        idx = result.get("_original_idx", 0)
        title = result.get("title", "Untitled")
        if len(title) > 80:
            title = title[:77] + "..."
        title = title.replace("|", "\\|")
        authors = result.get("authors", "Unknown")
        if isinstance(authors, list):
            first_author = authors[0] if authors else "Unknown"
        elif isinstance(authors, str):
            first_author = authors.split(",")[0].split(" and ")[0].strip()
        else:
            first_author = "Unknown"
        if len(first_author) > 25:
            first_author = first_author[:22] + "..."
        first_author = first_author.replace("|", "\\|")
        year = result.get("year", "N/A")
        journal = (result.get("journal") or "")[:30].replace("|", "\\|")
        citations = result.get("citations", "")
        doi = result.get("doi", "")
        md += f"| {idx} | {title} | {first_author} | {year} | {journal} | {citations} | {doi} |\n"

    md += "\n*Full details (abstracts, URLs) available in combined_results.json*\n"
    return md


def _format_bibtex(results: list[dict]) -> str:
    entries = []
    seen_keys: set[str] = set()
    key_to_index: dict[str, int] = {}
    for result in results:
        entry_type = result.get("type", "article")
        first_author = result.get("first_author", "")
        if not first_author:
            authors = result.get("authors", "")
            if isinstance(authors, list) and authors:
                first_author = re.split(r"[,\s]", authors[0])[0]
            elif isinstance(authors, str) and authors:
                first_author = re.split(r"[,\s]", authors.split(" and ")[0].strip())[0]
        first_author = first_author or "unknown"
        base_key = re.sub(
            r"[^a-zA-Z0-9_\-]", "", f"{first_author}_{result.get('year', '0000')}"
        )
        cite_key, renamed = unique_key(base_key, seen_keys)
        if renamed:
            old_name, new_name = renamed
            idx = key_to_index.pop(old_name)
            entry_lines = entries[idx].split("\n", 1)
            entry_lines[0] = entry_lines[0].replace(
                f"{{{old_name},", f"{{{new_name},", 1
            )
            entries[idx] = "\n".join(entry_lines)
            key_to_index[new_name] = idx
        key_to_index[cite_key] = len(entries)

        authors_val = result.get("authors", "")
        if isinstance(authors_val, list):
            authors_val = " and ".join(authors_val)
        fields = {
            "title": result.get("title", ""),
            "author": authors_val,
            "year": result.get("year", ""),
            "journal": result.get("journal", ""),
            "volume": result.get("volume", ""),
            "pages": result.get("pages", ""),
            "doi": result.get("doi", ""),
        }
        entries.append(build_bibtex_entry(entry_type, cite_key, fields))

    return "\n\n".join(entries) + "\n" if entries else ""


_RIS_TYPE_MAP = {
    "article": "JOUR",
    "book": "BOOK",
    "chapter": "CHAP",
    "conference": "CONF",
    "review": "JOUR",
    "preprint": "JOUR",
}


def _format_ris(results: list[dict]) -> str:
    ris = ""
    for result in results:
        ris += f"TY  - {_RIS_TYPE_MAP.get(result.get('type', 'article'), 'JOUR')}\n"
        ris += f"TI  - {result.get('title', '')}\n"
        authors = result.get("authors", "")
        if isinstance(authors, list):
            for author in authors:
                ris += f"AU  - {author}\n"
        else:
            ris += f"AU  - {authors}\n"
        ris += f"PY  - {result.get('year', '')}\n"
        if result.get("journal"):
            ris += f"JO  - {result['journal']}\n"
        if result.get("volume"):
            ris += f"VL  - {result['volume']}\n"
        if result.get("pages"):
            pages = str(result["pages"])
            if "--" in pages or "-" in pages:
                parts = re.split(r"--?", pages, maxsplit=1)
                ris += f"SP  - {parts[0].strip()}\n"
                if len(parts) > 1:
                    ris += f"EP  - {parts[1].strip()}\n"
            else:
                ris += f"SP  - {pages}\n"
        if result.get("doi"):
            ris += f"DO  - {result['doi']}\n"
        if result.get("pmid"):
            ris += f"AN  - {result['pmid']}\n"
        if result.get("abstract"):
            ris += f"AB  - {result['abstract']}\n"
        if result.get("url"):
            ris += f"UR  - {result['url']}\n"
        ris += "ER  - \n\n"
    return ris


def generate_search_summary(results: list[dict]) -> dict:
    summary: dict = {
        "total_results": len(results),
        "sources": {},
        "year_distribution": {},
        "avg_citations": 0,
        "total_citations": 0,
    }
    citations = []
    for result in results:
        source = result.get("source", "Unknown")
        summary["sources"][source] = summary["sources"].get(source, 0) + 1
        year = result.get("year", "Unknown")
        summary["year_distribution"][year] = (
            summary["year_distribution"].get(year, 0) + 1
        )
        if result.get("citations"):
            try:
                citations.append(int(result["citations"]))
            except (ValueError, TypeError):
                pass
    if citations:
        summary["avg_citations"] = sum(citations) / len(citations)
        summary["total_citations"] = sum(citations)
    return summary


def process_results(
    results_path: str,
    *,
    output_format: str = "markdown",
    output_path: str | None = None,
    rank_by: str | None = None,
    year_start: int | None = None,
    year_end: int | None = None,
    study_types: list[str] | None = None,
    deduplicate: bool = True,
    top_n: int = 20,
) -> dict:
    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    if not isinstance(results, list):
        return {"error": f"Expected JSON array, got {type(results).__name__}"}

    log_lines = []

    if deduplicate:
        before = len(results)
        results = deduplicate_merge(results)
        log_lines.append(f"Deduplicated: {before} -> {len(results)}")

    if study_types:
        types_lower = [t.lower() for t in study_types]
        results = [
            r
            for r in results
            if (r.get("study_type") or "").lower() in types_lower
            or (r.get("publication_type") or "").lower() in types_lower
        ]
        log_lines.append(f"After study-type filter: {len(results)}")

    if year_start is not None or year_end is not None:
        filtered = []
        for r in results:
            try:
                year = int(r.get("year", 0))
                if year_start is not None and year < year_start:
                    continue
                if year_end is not None and year > year_end:
                    continue
                filtered.append(r)
            except (ValueError, TypeError):
                filtered.append(r)
        results = filtered
        log_lines.append(f"After year filter: {len(results)}")

    def _safe_int(val, default=0):
        try:
            return int(val)
        except (ValueError, TypeError):
            return default

    for idx, r in enumerate(results):
        r["_original_idx"] = idx

    if rank_by:
        if rank_by == "citations":
            results = sorted(
                results, key=lambda x: _safe_int(x.get("citations", 0)), reverse=True
            )
        elif rank_by == "year":
            results = sorted(
                results, key=lambda x: _safe_int(x.get("year", 0)), reverse=True
            )
        elif rank_by == "relevance":
            results = sorted(
                results,
                key=lambda x: _safe_int(x.get("relevance_score", 0)),
                reverse=True,
            )

    def _clean_json(r, **_):
        cleaned = [
            {k: v for k, v in item.items() if k != "_original_idx"} for item in r
        ]
        return json.dumps(cleaned, indent=2)

    formatters = {
        "json": _clean_json,
        "markdown": _format_markdown,
        "bibtex": lambda r, **_: _format_bibtex(r),
        "ris": lambda r, **_: _format_ris(r),
    }
    formatter = formatters.get(output_format)
    if formatter is None:
        return {"error": f"Unknown format: {output_format}"}

    output = formatter(results, top_n=top_n)

    ext_map = {"json": "json", "markdown": "md", "bibtex": "bib", "ris": "ris"}
    out_path = output_path or f"review/search_results.{ext_map[output_format]}"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)

    summary = generate_search_summary(results)

    return {
        "output_path": out_path,
        "total_results": len(results),
        "summary": summary,
        "log": log_lines,
    }


def deduplicate_results(results_path: str, output_path: str | None = None) -> dict:
    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    before = len(results)
    deduped, match_stats = deduplicate_merge(results, track_stats=True)
    after = len(deduped)

    for r in deduped:
        a = r.get("authors")
        if isinstance(a, str) and a:
            r["authors"] = [
                x.strip() for x in re.split(r",\s*(?=[A-Z])", a) if x.strip()
            ]

    out = output_path or results_path
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(deduped, f, indent=2, ensure_ascii=False)

    return {
        "before": before,
        "after": after,
        "removed": before - after,
        "duplicates_by_pmid": match_stats["by_pmid"],
        "duplicates_by_doi": match_stats["by_doi"],
        "duplicates_by_title": match_stats["by_title"],
        "output_path": out,
    }
