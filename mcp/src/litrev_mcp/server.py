"""litrev-mcp: MCP server exposing literature review tools.

Tools:
  - search_pubmed: keyword search on PubMed via NCBI E-utilities
  - search_s2: keyword search on Semantic Scholar (authenticated)
  - search_openalex: keyword search on OpenAlex Works API
  - process_results: deduplicate, rank, filter, format search results
  - deduplicate_results: deduplicate combined_results.json in place
  - fetch_abstracts: fetch missing abstracts from PubMed for screening
  - extract_claims_regex: regex-based quantitative claim extraction
  - citation_chain: backward/forward citation chaining via S2 + OpenAlex
  - verify_dois: validate DOIs/PMIDs, check retractions
  - generate_bibliography: 3-level DOI resolution to BibTeX
  - audit_claims: cross-verify numbers in review vs extracted claims
  - validate_gate: mechanical gate validation for review pipeline phases
"""

from typing import Literal

from mcp.server.fastmcp import FastMCP

from .tools.search import process_results as _process_results
from .tools.search import deduplicate_results as _deduplicate_results
from .tools.abstracts import fetch_abstracts as _fetch_abstracts
from .tools.claims import extract_claims_regex as _extract_claims_regex
from .tools.snowball import citation_chain as _citation_chain
from .tools.s2_search import search_s2 as _search_s2
from .tools.pubmed_search import search_pubmed as _search_pubmed
from .tools.openalex_search import search_openalex as _search_openalex
from .tools.verify import verify_dois as _verify_dois
from .tools.verify import generate_bibliography as _generate_bibliography
from .tools.verify import audit_claims as _audit_claims
from .tools.gates import validate_gate as _validate_gate
from .lib.http import env_tips


def _with_tips(result: dict, *var_names: str) -> dict:
    tips = env_tips(*var_names)
    if tips:
        result["tips"] = tips
    return result


mcp = FastMCP(
    "litrev-mcp",
    instructions="Literature review tools: search processing, screening support, citation chaining, claim extraction, verification, and bibliography generation.",
)


@mcp.tool()
def process_results(
    results_path: str,
    output_format: Literal["markdown", "json", "bibtex", "ris"] = "markdown",
    output_path: str | None = None,
    rank_by: Literal["citations", "year", "relevance"] | None = None,
    year_start: int | None = None,
    year_end: int | None = None,
    study_types: list[str] | None = None,
    deduplicate: bool = True,
    top_n: int = 20,
) -> dict:
    """Rank, filter, and format literature search results for review.

    Reads combined_results.json, applies optional deduplication and filters,
    then writes formatted output (markdown table, JSON, BibTeX, or RIS).
    For deduplication only (in-place, with field merging), use deduplicate_results instead.

    Args:
        results_path: Path to combined_results.json
        output_format: Output format — "markdown", "json", "bibtex", or "ris"
        output_path: Where to write output (default: review/search_results.<ext>)
        rank_by: Sort criteria — "citations", "year", or "relevance"
        year_start: Filter out articles before this year
        year_end: Filter out articles after this year
        study_types: Keep only these study types (e.g. ["rct", "cohort"])
        deduplicate: Remove duplicates by PMID/DOI/title (default: true)
        top_n: Number of top-cited articles to detail in markdown output; ignored for other formats (default: 20)
    """
    return _process_results(
        results_path,
        output_format=output_format,
        output_path=output_path,
        rank_by=rank_by,
        year_start=year_start,
        year_end=year_end,
        study_types=study_types,
        deduplicate=deduplicate,
        top_n=top_n,
    )


@mcp.tool()
def deduplicate_results(
    results_path: str,
    output_path: str | None = None,
) -> dict:
    """Deduplicate combined_results.json by PMID, DOI, or normalized title.

    Merges non-empty fields from duplicates into the kept record.
    WARNING: overwrites the input file by default. Pass output_path to write
    to a separate file and preserve the original.

    Args:
        results_path: Path to combined_results.json
        output_path: Where to write deduplicated results (default: overwrite input file)
    """
    return _deduplicate_results(results_path, output_path)


@mcp.tool()
def fetch_abstracts(
    results_path: str,
    indices: list[int],
    fetch_missing: bool = True,
    output_path: str | None = None,
) -> dict:
    """Fetch missing abstracts from PubMed and format articles for screening.

    Selects articles by row index from combined_results.json, fetches
    abstracts via PubMed EFetch for articles that have a PMID but no abstract,
    backfills them into combined_results.json, and writes a markdown file
    with all selected articles formatted for screening review.

    Args:
        results_path: Path to combined_results.json
        indices: 0-based row indices of articles to extract
        fetch_missing: Fetch missing abstracts from PubMed (default: true)
        output_path: Where to write markdown output (default: review/abstracts_for_screening.md)
    """
    return _with_tips(
        _fetch_abstracts(
            results_path,
            indices,
            fetch_missing=fetch_missing,
            output_path=output_path,
        ),
        "LITREV_EMAIL",
        "NCBI_API_KEY",
    )


@mcp.tool()
def extract_claims_regex(
    results_path: str,
    indices: list[int] | None = None,
    indices_file: str | None = None,
    fetch_missing: bool = True,
    output_path: str = "review/extracted_claims.json",
) -> dict:
    """Extract quantitative claims from article abstracts using regex patterns.

    Finds statistics (OR, HR, RR, p-values, 95% CI), percentages, and numbers
    in abstracts of included articles. Fetches missing abstracts from PubMed.
    Produces extracted_claims.json with per-article claims keyed by BibTeX key.

    This is the automated first pass — the LLM enriches with semantic claims,
    quality assessment, and themes afterward.

    Args:
        results_path: Path to combined_results.json
        indices: List of 0-based article indices to process (default: all articles — can be slow on large files)
        indices_file: Path to JSON file with indices (e.g. included_indices.json)
        fetch_missing: Fetch missing abstracts from PubMed (default: true)
        output_path: Where to write output (default: review/extracted_claims.json)
    """
    return _with_tips(
        _extract_claims_regex(
            results_path,
            indices=indices,
            indices_file=indices_file,
            fetch_missing=fetch_missing,
            output_path=output_path,
        ),
        "LITREV_EMAIL",
        "NCBI_API_KEY",
    )


@mcp.tool()
def search_pubmed(
    query: str,
    date_start: str | None = None,
    date_end: str | None = None,
    limit: int = 200,
    output_path: str | None = None,
) -> dict:
    """Search PubMed by keywords via NCBI E-utilities.

    Runs esearch → esummary → efetch to retrieve articles with metadata
    and abstracts. Uses NCBI_API_KEY if configured (10 req/s vs 3 req/s).

    Args:
        query: PubMed search query (supports MeSH terms and Boolean operators)
        date_start: Start year filter, YYYY format (e.g. "2020")
        date_end: End year filter, YYYY format (e.g. "2026")
        limit: Max results to return (default: 200)
        output_path: Write results to JSON file (optional; if omitted, results are returned inline)
    """
    return _with_tips(
        _search_pubmed(
            query,
            date_start=date_start,
            date_end=date_end,
            limit=limit,
            output_path=output_path,
        ),
        "NCBI_API_KEY",
        "LITREV_EMAIL",
    )


@mcp.tool()
def search_openalex(
    query: str,
    year_start: int | None = None,
    year_end: int | None = None,
    limit: int = 50,
    output_path: str | None = None,
) -> dict:
    """Search OpenAlex Works API by keywords.

    Queries journal articles sorted by citation count. Uses LITREV_EMAIL
    for polite pool (faster rate limits) if configured. OpenAlex does not
    return abstracts — use fetch_abstracts to retrieve them from PubMed.

    Args:
        query: Short search query (2-3 key terms, no Boolean operators)
        year_start: Filter out articles before this year
        year_end: Filter out articles after this year
        limit: Max results to return (default: 50, max: 200)
        output_path: Write results to JSON file (optional; if omitted, results are returned inline)
    """
    return _with_tips(
        _search_openalex(
            query,
            year_start=year_start,
            year_end=year_end,
            limit=limit,
            output_path=output_path,
        ),
        "LITREV_EMAIL",
    )


@mcp.tool()
def search_s2(
    query: str,
    year_start: int | None = None,
    year_end: int | None = None,
    fields_of_study: str | None = "Medicine",
    limit: int = 100,
    output_path: str | None = None,
) -> dict:
    """Search Semantic Scholar by keywords (authenticated).

    Uses the Academic Graph API with the configured S2_API_KEY for
    reliable rate limits. Returns normalized article records matching
    the combined_results.json schema.

    Args:
        query: Plain-language search query (no Boolean operators)
        year_start: Filter out articles before this year
        year_end: Filter out articles after this year
        fields_of_study: S2 field filter (default: "Medicine")
        limit: Max results to return (max 100 per query)
        output_path: Write results to JSON file (optional; if omitted, results are returned inline)
    """
    return _with_tips(
        _search_s2(
            query,
            year_start=year_start,
            year_end=year_end,
            fields_of_study=fields_of_study,
            limit=limit,
            output_path=output_path,
        ),
        "S2_API_KEY",
    )


@mcp.tool()
def citation_chain(
    results_path: str,
    indices: list[int],
    direction: Literal["backward", "forward", "both"] = "both",
    sources: Literal["s2", "openalex", "s2,openalex"] = "s2,openalex",
    output_path: str = "review/chaining_candidates.json",
) -> dict:
    """Find additional papers via backward and forward citation chaining.

    Takes seed papers from combined_results.json, queries Semantic Scholar
    and OpenAlex for their references (backward) and citing papers (forward),
    deduplicates against existing results, and outputs new unique candidates.

    Args:
        results_path: Path to combined_results.json
        indices: 0-based row indices of seed papers
        direction: "backward", "forward", or "both" (default: "both")
        sources: Comma-separated API sources — "s2", "openalex", or "s2,openalex"
        output_path: Where to write candidates (default: review/chaining_candidates.json)
    """
    return _with_tips(
        _citation_chain(
            results_path,
            indices,
            direction=direction,
            sources=sources,
            output_path=output_path,
        ),
        "S2_API_KEY",
        "LITREV_EMAIL",
    )


@mcp.tool()
def verify_dois(
    review_path: str,
    check_retractions: bool = True,
    timeout: int = 10,
    output_path: str | None = None,
) -> dict:
    """Verify DOIs and PMIDs in a review document.

    Extracts all DOIs and PMIDs from the markdown review, validates each
    against doi.org handle API and PubMed, checks for retracted publications,
    and produces a JSON verification report.

    Args:
        review_path: Path to the review markdown file
        check_retractions: Check PubMed for retractions (default: true)
        timeout: HTTP timeout in seconds (default: 10)
        output_path: Where to write report (default: <review>_citation_report.json)
    """
    return _with_tips(
        _verify_dois(
            review_path,
            check_retractions=check_retractions,
            timeout=timeout,
            output_path=output_path,
        ),
        "LITREV_EMAIL",
        "NCBI_API_KEY",
    )


@mcp.tool()
def generate_bibliography(
    review_path: str,
    output_path: str = "review/references.bib",
    timeout: int = 10,
) -> dict:
    """Generate a BibTeX bibliography from DOIs in a review.

    Scans the review markdown for DOIs, resolves each through a 3-level chain
    (doi.org native BibTeX → CrossRef API → PubMed API). For DOIs that also
    appear in an embedded BibTeX block, cross-verifies author names and years
    against the embedded metadata; DOIs found only in prose are resolved
    without cross-verification.

    Args:
        review_path: Path to the review markdown file
        output_path: Where to write references.bib (default: review/references.bib)
        timeout: HTTP timeout in seconds (default: 10)
    """
    return _with_tips(
        _generate_bibliography(
            review_path,
            output_path=output_path,
            timeout=timeout,
        ),
        "LITREV_EMAIL",
        "NCBI_API_KEY",
    )


@mcp.tool()
def audit_claims(
    review_path: str,
    claims_path: str = "review/extracted_claims.json",
    bib_path: str | None = None,
    output_path: str = "review/claims_audit.json",
) -> dict:
    """Cross-verify numerical claims in a review against extracted data.

    Requires extract_claims_regex to have been run first — reads its output
    (extracted_claims.json) as the reference dataset. Optionally uses
    generate_bibliography output (references.bib) for DOI-based key resolution.

    Finds every number near a Pandoc citation ([@key]) in the review markdown,
    resolves the citation key to the corresponding article in extracted_claims.json,
    and checks whether the number appears in the article's extracted claims.
    Only Pandoc/Quarto citation syntax is supported.

    Statuses: VERIFIED (found in abstract), UNVERIFIED (not found — may be
    from full-text or hallucinated), NO_ABSTRACT, NO_EXTRACTION.

    Args:
        review_path: Path to the review markdown file
        claims_path: Path to extracted_claims.json (from extract_claims_regex)
        bib_path: Path to references.bib for DOI-based key resolution (auto-detected from review dir)
        output_path: Where to write audit report (default: review/claims_audit.json)
    """
    return _audit_claims(
        review_path,
        claims_path=claims_path,
        bib_path=bib_path,
        output_path=output_path,
    )


@mcp.tool()
def validate_gate(
    gate: str,
    review_dir: str,
) -> dict:
    """Validate a mechanical gate for a literature review phase.

    Checks structural requirements (file existence, format, content) for a
    specific pipeline phase. Returns PASS/FAIL with detailed per-check results.

    Args:
        gate: Gate identifier — "1", "2", "3a", "3b", "4", "5", "6", "7", "8", or "9"
        review_dir: Path to the review directory containing output files
    """
    return _validate_gate(gate, review_dir)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
