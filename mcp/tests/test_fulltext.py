"""Tests for fulltext: JATS XML parsing, cache, section retrieval."""

import pytest

from litrev_mcp.lib.fulltext import (
    _parse_jats_xml,
    _normalize_section,
    _cache,
    fetch_and_cache,
    get_cached_section,
    clear_cache,
)


JATS_SIMPLE = b"""\
<article>
  <front>
    <article-meta>
      <abstract><p>This is the abstract text.</p></abstract>
    </article-meta>
  </front>
  <body>
    <sec>
      <title>Introduction</title>
      <p>Background information here.</p>
    </sec>
    <sec>
      <title>Methods</title>
      <p>We used a randomized design.</p>
    </sec>
    <sec>
      <title>Results</title>
      <p>Treatment showed 45% response rate.</p>
    </sec>
    <sec>
      <title>Discussion</title>
      <p>These findings suggest efficacy.</p>
    </sec>
  </body>
</article>
"""

JATS_FLAT_BODY = b"""\
<article>
  <front>
    <article-meta>
      <abstract><p>Abstract here.</p></abstract>
    </article-meta>
  </front>
  <body>
    <p>This article has no sections, just flat paragraphs.</p>
    <p>Second paragraph of content.</p>
  </body>
</article>
"""

JATS_ALT_TITLES = b"""\
<article>
  <front>
    <article-meta>
      <abstract><p>Abstract.</p></abstract>
    </article-meta>
  </front>
  <body>
    <sec>
      <title>Background</title>
      <p>Intro text.</p>
    </sec>
    <sec>
      <title>Materials and methods</title>
      <p>Lab procedures.</p>
    </sec>
    <sec>
      <title>Findings</title>
      <p>Key results.</p>
    </sec>
  </body>
</article>
"""

JATS_WRAPPED = b"""\
<pmc-articleset>
<article>
  <front>
    <article-meta>
      <abstract><p>Wrapped abstract.</p></abstract>
    </article-meta>
  </front>
  <body>
    <sec>
      <title>Results</title>
      <p>Data here.</p>
    </sec>
  </body>
</article>
</pmc-articleset>
"""


class TestNormalizeSection:
    def test_exact_match(self):
        assert _normalize_section("Methods") == "methods"
        assert _normalize_section("Results") == "results"

    def test_alias(self):
        assert _normalize_section("Materials and methods") == "methods"
        assert _normalize_section("Background") == "introduction"
        assert _normalize_section("Findings") == "results"

    def test_unknown(self):
        assert _normalize_section("Supplementary data") is None

    def test_whitespace(self):
        assert _normalize_section("  Methods  ") == "methods"


class TestParseJatsXml:
    def test_simple_article(self):
        sections = _parse_jats_xml(JATS_SIMPLE)
        assert "abstract" in sections
        assert "introduction" in sections
        assert "methods" in sections
        assert "results" in sections
        assert "discussion" in sections
        assert "full" in sections
        assert "abstract text" in sections["abstract"]
        assert "45% response rate" in sections["results"]

    def test_flat_body(self):
        sections = _parse_jats_xml(JATS_FLAT_BODY)
        assert "abstract" in sections
        assert "full" in sections
        assert "flat paragraphs" in sections["full"]

    def test_alt_section_titles(self):
        sections = _parse_jats_xml(JATS_ALT_TITLES)
        assert "introduction" in sections
        assert "methods" in sections
        assert "results" in sections

    def test_pmc_articleset_wrapper(self):
        sections = _parse_jats_xml(JATS_WRAPPED)
        assert "results" in sections
        assert "Data here" in sections["results"]

    def test_full_combines_all(self):
        sections = _parse_jats_xml(JATS_SIMPLE)
        full = sections["full"]
        assert "Background information" in full
        assert "randomized design" in full
        assert "45% response rate" in full


class TestCache:
    def setup_method(self):
        _cache.clear()

    def test_get_section_not_cached(self):
        result = get_cached_section("10.1234/test", "results", 15000)
        assert "error" in result
        assert "Not cached" in result["error"]

    def test_cache_and_retrieve(self):
        _cache["10.1234/test"] = {
            "source": "pmc",
            "sections": {
                "abstract": "The abstract.",
                "results": "Treatment was effective.",
                "full": "The abstract.\n\nTreatment was effective.",
            },
            "word_count": 10,
        }

        result = get_cached_section("10.1234/test", "results", 15000)
        assert result["text"] == "Treatment was effective."
        assert result["truncated"] is False
        assert result["source"] == "pmc"

    def test_truncation(self):
        _cache["10.1234/long"] = {
            "source": "pdf",
            "sections": {"full": "x" * 20000},
            "word_count": 5000,
        }

        result = get_cached_section("10.1234/long", "full", 100)
        assert len(result["text"]) == 100
        assert result["truncated"] is True

    def test_section_not_found(self):
        _cache["10.1234/test"] = {
            "source": "pmc",
            "sections": {"results": "Data."},
            "word_count": 1,
        }

        result = get_cached_section("10.1234/test", "methods", 15000)
        assert "error" in result
        assert "Section not found" in result["error"]

    def test_clear_cache(self):
        _cache["10.1234/a"] = {"source": "pmc", "sections": {}, "word_count": 0}
        _cache["10.1234/b"] = {"source": "pdf", "sections": {}, "word_count": 0}
        n = clear_cache()
        assert n == 2
        assert len(_cache) == 0

    def test_cached_hit_returns_cached_flag(self):
        _cache["10.1234/hit"] = {
            "source": "pmc",
            "sections": {"full": "text"},
            "word_count": 1,
        }

        result = fetch_and_cache("10.1234/hit")
        assert result["cached"] is True
        assert result["source"] == "pmc"

    def test_doi_case_insensitive(self):
        _cache["10.1234/test"] = {
            "source": "pmc",
            "sections": {"full": "text"},
            "word_count": 1,
        }

        result = get_cached_section("10.1234/TEST", "full", 15000)
        assert result["text"] == "text"

    def test_section_alias_lookup(self):
        _cache["10.1234/alias"] = {
            "source": "pmc",
            "sections": {"introduction": "Intro text here."},
            "word_count": 3,
        }

        result = get_cached_section("10.1234/alias", "background", 15000)
        assert result["text"] == "Intro text here."
