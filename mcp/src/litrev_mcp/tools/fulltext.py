"""MCP tools: fetch full text and retrieve sections for scientific articles."""

from ..lib.fulltext import clear_cache, fetch_and_cache, get_cached_section


def fetch_fulltext(doi: str) -> dict:
    return fetch_and_cache(doi)


def get_section(
    doi: str,
    section: str = "results",
    max_chars: int = 15000,
) -> dict:
    return get_cached_section(doi, section, max_chars)
