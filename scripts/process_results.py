#!/usr/bin/env python3
"""
Literature Search Results Processor
Processes, deduplicates, ranks, filters, and formats search results.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from bibtex_keys import unique_key as _unique_key, escape_bibtex as _escape_bibtex, build_bibtex_entry as _build_bibtex_entry

def _format_markdown(results: list[dict], top_n: int = 0) -> str:
    md = "# Literature Search Results\n\n"
    md += f"**Search Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    md += f"**Total Results**: {len(results)}\n\n"

    summary = generate_search_summary(results)

    md += "## Summary Statistics\n\n"
    md += f"- **Total**: {summary['total_results']}\n"
    if summary.get('total_citations'):
        md += f"- **Total Citations**: {summary['total_citations']}\n"
        md += f"- **Average Citations**: {summary['avg_citations']:.1f}\n"
    md += "\n"

    if summary['sources']:
        md += "### Results by Source\n\n"
        for source, count in sorted(summary['sources'].items(), key=lambda x: x[1], reverse=True):
            md += f"- {source}: {count}\n"
        md += "\n"

    if summary['year_distribution']:
        md += "### Results by Year\n\n"
        for year, count in sorted(summary['year_distribution'].items(), key=lambda x: str(x[0]), reverse=True):
            md += f"- {year}: {count}\n"
        md += "\n"

    study_types = {}
    for r in results:
        st = r.get('study_type') or r.get('publication_type') or 'unspecified'
        study_types[st] = study_types.get(st, 0) + 1
    if study_types:
        md += "### Results by Study Type\n\n"
        for st, count in sorted(study_types.items(), key=lambda x: x[1], reverse=True):
            md += f"- {st}: {count}\n"
        md += "\n"

    if top_n > 0:
        top_results = sorted(results, key=lambda x: x.get('citations', 0), reverse=True)[:top_n]
        md += f"## Top {min(top_n, len(top_results))} Most-Cited Articles\n\n"
        for i, result in enumerate(top_results, 1):
            md += f"### {i}. {result.get('title', 'Untitled')}\n\n"
            authors = result.get('authors', 'Unknown')
            if isinstance(authors, list):
                authors = ', '.join(authors[:3]) + (' et al.' if len(authors) > 3 else '')
            md += f"**Authors**: {authors}\n\n"
            md += f"**Year**: {result.get('year', 'N/A')}"
            if result.get('journal'):
                md += f" | **Journal**: {result['journal']}"
            if result.get('citations'):
                md += f" | **Citations**: {result['citations']}"
            md += "\n\n"
            if result.get('doi'):
                md += f"**DOI**: {result['doi']}\n\n"
            if result.get('abstract'):
                md += f"**Abstract**: {result['abstract']}\n\n"
            md += "---\n\n"

    md += "## All Results\n\n"
    md += "| # | Title | First Author | Year | Journal | Citations | DOI |\n"
    md += "|---|-------|--------------|------|---------|-----------|-----|\n"
    for i, result in enumerate(results, 1):
        title = result.get('title', 'Untitled')
        if len(title) > 80:
            title = title[:77] + "..."
        title = title.replace('|', '\\|')
        authors = result.get('authors', 'Unknown')
        if isinstance(authors, list):
            first_author = authors[0] if authors else 'Unknown'
        elif isinstance(authors, str):
            first_author = authors.split(',')[0].split(' and ')[0].strip()
        else:
            first_author = 'Unknown'
        if len(first_author) > 25:
            first_author = first_author[:22] + "..."
        first_author = first_author.replace('|', '\\|')
        year = result.get('year', 'N/A')
        journal = (result.get('journal') or '')[:30].replace('|', '\\|')
        citations = result.get('citations', '')
        doi = result.get('doi', '')
        md += f"| {i} | {title} | {first_author} | {year} | {journal} | {citations} | {doi} |\n"

    md += f"\n*Full details (abstracts, URLs) available in combined_results.json*\n"
    return md


def _format_bibtex(results: list[dict]) -> str:
    entries = []
    seen_keys = set()
    key_to_index = {}
    for result in results:
        entry_type = result.get('type', 'article')
        first_author = result.get('first_author', '')
        if not first_author:
            authors = result.get('authors', '')
            if isinstance(authors, list) and authors:
                first_author = re.split(r'[,\s]', authors[0])[0]
            elif isinstance(authors, str) and authors:
                first_author = re.split(r'[,\s]', authors.split(' and ')[0].strip())[0]
        first_author = first_author or 'unknown'
        base_key = re.sub(r'[^a-zA-Z0-9_\-]', '', f"{first_author}_{result.get('year', '0000')}")
        cite_key, renamed = _unique_key(base_key, seen_keys)
        if renamed:
            old_name, new_name = renamed
            idx = key_to_index.pop(old_name)
            entries[idx] = entries[idx].replace(f"{{{old_name},", f"{{{new_name},", 1)
            key_to_index[new_name] = idx
        key_to_index[cite_key] = len(entries)

        authors_val = result.get('authors', '')
        if isinstance(authors_val, list):
            authors_val = ' and '.join(authors_val)
        fields = {
            "title": result.get('title', ''),
            "author": authors_val,
            "year": result.get('year', ''),
            "journal": result.get('journal', ''),
            "volume": result.get('volume', ''),
            "pages": result.get('pages', ''),
            "doi": result.get('doi', ''),
        }
        entries.append(_build_bibtex_entry(entry_type, cite_key, fields))

    return "\n\n".join(entries) + "\n" if entries else ""


_RIS_TYPE_MAP = {
    'article': 'JOUR',
    'book': 'BOOK',
    'chapter': 'CHAP',
    'conference': 'CONF',
    'review': 'JOUR',
    'preprint': 'JOUR',
}


def _format_ris(results: list[dict]) -> str:
    ris = ""
    for result in results:
        ris += f"TY  - {_RIS_TYPE_MAP.get(result.get('type', 'article'), 'JOUR')}\n"
        ris += f"TI  - {result.get('title', '')}\n"

        authors = result.get('authors', '')
        if isinstance(authors, list):
            for author in authors:
                ris += f"AU  - {author}\n"
        else:
            ris += f"AU  - {authors}\n"

        ris += f"PY  - {result.get('year', '')}\n"

        if result.get('journal'):
            ris += f"JO  - {result['journal']}\n"

        if result.get('volume'):
            ris += f"VL  - {result['volume']}\n"

        if result.get('pages'):
            pages = str(result['pages'])
            if '--' in pages or '-' in pages:
                parts = re.split(r'--?', pages, maxsplit=1)
                ris += f"SP  - {parts[0].strip()}\n"
                if len(parts) > 1:
                    ris += f"EP  - {parts[1].strip()}\n"
            else:
                ris += f"SP  - {pages}\n"

        if result.get('doi'):
            ris += f"DO  - {result['doi']}\n"

        if result.get('pmid'):
            ris += f"AN  - {result['pmid']}\n"

        if result.get('abstract'):
            ris += f"AB  - {result['abstract']}\n"

        if result.get('url'):
            ris += f"UR  - {result['url']}\n"

        ris += "ER  - \n\n"

    return ris


_FORMATTERS = {
    'json': lambda results, **_: json.dumps(results, indent=2),
    'markdown': _format_markdown,
    'bibtex': lambda results, **_: _format_bibtex(results),
    'ris': lambda results, **_: _format_ris(results),
}


def format_search_results(results: list[dict], output_format: str = 'json', top_n: int = 0) -> str:
    formatter = _FORMATTERS.get(output_format)
    if formatter is None:
        raise ValueError(f"Unknown format: {output_format}")
    return formatter(results, top_n=top_n)

def deduplicate_results(results: list[dict]) -> list[dict]:
    """
    Remove duplicate results based on PMID, DOI, or title.

    Args:
        results: List of search results

    Returns:
        Deduplicated list
    """
    seen_pmids = set()
    seen_dois = set()
    seen_titles = set()
    unique_results = []

    for result in results:
        pmid = str(result.get('pmid', '')).strip()
        doi = result.get('doi', '').lower().strip()
        title = re.sub(r'[^a-z0-9]', '', result.get('title', '').lower())

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

        unique_results.append(result)

    return unique_results

def rank_results(results: list[dict], criteria: str = 'citations') -> list[dict]:
    """
    Rank results by specified criteria.

    Args:
        results: List of search results
        criteria: Ranking criteria (citations, year, relevance)

    Returns:
        Ranked list
    """
    if criteria == 'citations':
        return sorted(results, key=lambda x: x.get('citations', 0), reverse=True)
    elif criteria == 'year':
        return sorted(results, key=lambda x: x.get('year', '0'), reverse=True)
    elif criteria == 'relevance':
        return sorted(results, key=lambda x: x.get('relevance_score', 0), reverse=True)
    else:
        return results

def filter_by_year(results: list[dict], start_year: int = None, end_year: int = None) -> list[dict]:
    """
    Filter results by publication year range.

    Args:
        results: List of search results
        start_year: Minimum year (inclusive)
        end_year: Maximum year (inclusive)

    Returns:
        Filtered list
    """
    filtered = []

    for result in results:
        try:
            year = int(result.get('year', 0))
            if start_year is not None and year < start_year:
                continue
            if end_year is not None and year > end_year:
                continue
            filtered.append(result)
        except (ValueError, TypeError):
            # Include if year parsing fails
            filtered.append(result)

    return filtered

def generate_search_summary(results: list[dict]) -> dict:
    """
    Generate summary statistics for search results.

    Args:
        results: List of search results

    Returns:
        Summary dictionary
    """
    summary = {
        'total_results': len(results),
        'sources': {},
        'year_distribution': {},
        'avg_citations': 0,
        'total_citations': 0
    }

    citations = []

    for result in results:
        # Count by source
        source = result.get('source', 'Unknown')
        summary['sources'][source] = summary['sources'].get(source, 0) + 1

        # Count by year
        year = result.get('year', 'Unknown')
        summary['year_distribution'][year] = summary['year_distribution'].get(year, 0) + 1

        # Collect citations
        if result.get('citations'):
            try:
                citations.append(int(result['citations']))
            except (ValueError, TypeError):
                pass

    if citations:
        summary['avg_citations'] = sum(citations) / len(citations)
        summary['total_citations'] = sum(citations)

    return summary

def filter_by_study_type(results: list[dict], study_types: list[str]) -> list[dict]:
    """
    Filter results by study design type.

    Args:
        results: List of search results
        study_types: List of acceptable types (e.g., ['rct', 'meta-analysis', 'cohort'])

    Returns:
        Filtered list
    """
    study_types_lower = [t.lower() for t in study_types]
    filtered = []

    for result in results:
        result_type = result.get('study_type', '').lower()
        publication_type = result.get('publication_type', '').lower()
        if result_type in study_types_lower or publication_type in study_types_lower:
            filtered.append(result)

    return filtered

def main():
    """Command-line interface for search result processing."""
    parser = argparse.ArgumentParser(description="Process, deduplicate, and format literature search results.")
    parser.add_argument("file", help="JSON file with search results")
    parser.add_argument("--format", dest="output_format", default="markdown",
                        choices=["json", "markdown", "bibtex", "ris"],
                        help="Output format (default: markdown)")
    parser.add_argument("--output", help="Output file (default: review/search_results.<format>)")
    parser.add_argument("--rank", choices=["citations", "year", "relevance"],
                        help="Rank results by criteria")
    parser.add_argument("--year-start", type=int, help="Filter by start year")
    parser.add_argument("--year-end", type=int, help="Filter by end year")
    parser.add_argument("--study-type", help="Filter by study type (comma-separated, e.g. rct,cohort)")
    parser.add_argument("--deduplicate", action="store_true", help="Remove duplicates")
    parser.add_argument("--top", type=int, default=20, help="Number of top-cited articles to detail in markdown (default: 20, 0 to disable)")
    parser.add_argument("--summary", action="store_true", help="Show summary statistics")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f"File not found: {args.file}")

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error loading results: {e}")
        sys.exit(1)

    if not isinstance(results, list):
        print(f"Error: expected a JSON array, got {type(results).__name__}")
        sys.exit(1)
    if results and not isinstance(results[0], dict):
        print(f"Error: expected array of objects, got array of {type(results[0]).__name__}")
        sys.exit(1)

    if args.deduplicate:
        results = deduplicate_results(results)
        print(f"After deduplication: {len(results)} results")

    if args.study_type:
        study_types = [t.strip() for t in args.study_type.split(',')]
        results = filter_by_study_type(results, study_types)
        print(f"After study-type filter: {len(results)} results")

    if args.year_start is not None or args.year_end is not None:
        results = filter_by_year(results, args.year_start, args.year_end)
        print(f"After year filter: {len(results)} results")

    if args.rank:
        results = rank_results(results, args.rank)
        print(f"Ranked by: {args.rank}")

    if args.summary:
        summary = generate_search_summary(results)
        print("\n" + "="*60)
        print("SEARCH SUMMARY")
        print("="*60)
        print(json.dumps(summary, indent=2))
        print()

    output = format_search_results(results, args.output_format, top_n=args.top)

    ext_map = {"json": "json", "markdown": "md", "bibtex": "bib", "ris": "ris"}
    output_path = args.output or f"review/search_results.{ext_map[args.output_format]}"
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"Results saved to: {output_path}")

if __name__ == "__main__":
    main()
