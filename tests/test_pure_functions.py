#!/usr/bin/env python3
"""Unit tests for pure functions (no network calls)."""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from verify_citations import CitationVerifier
from generate_bib import extract_dois, extract_refs_md, _extract_bibtex_entries, _CROSSREF_TYPE_MAP
from bibtex_keys import unique_key as _unique_key, strip_code_blocks as _strip_code_blocks, extract_doi_matches as _extract_doi_matches, escape_bibtex as _escape_bibtex
from process_results import deduplicate_results, filter_by_year, rank_results, format_search_results
from bibtex_keys import _next_suffix


class TestExtractDois(unittest.TestCase):
    def test_basic_doi(self):
        text = "See 10.1234/test-article for details."
        assert extract_dois([]) == []
        verifier = CitationVerifier()
        assert verifier.extract_dois(text) == ["10.1234/test-article"]

    def test_doi_with_trailing_punctuation(self):
        verifier = CitationVerifier()
        assert verifier.extract_dois("DOI: 10.1234/abc.") == ["10.1234/abc"]
        assert verifier.extract_dois("10.1234/abc, 10.5678/def;") == ["10.1234/abc", "10.5678/def"]

    def test_doi_deduplication(self):
        verifier = CitationVerifier()
        text = "10.1234/abc and again 10.1234/abc"
        assert verifier.extract_dois(text) == ["10.1234/abc"]

    def test_doi_excluded_from_code_blocks(self):
        verifier = CitationVerifier()
        text = "Real DOI 10.1234/real\n```\n10.9999/fake\n```\nAnother 10.5678/also-real"
        result = verifier.extract_dois(text)
        assert "10.1234/real" in result
        assert "10.5678/also-real" in result
        assert "10.9999/fake" not in result


class TestExtractDoiMatches(unittest.TestCase):
    def test_parenthesized_doi(self):
        text = "See 10.1002/(SICI)1097-0142 for details."
        assert _extract_doi_matches(text) == ["10.1002/(SICI)1097-0142"]

    def test_doi_in_markdown_link(self):
        text = "[link](https://doi.org/10.1234/abc)"
        assert _extract_doi_matches(text) == ["10.1234/abc"]

    def test_balanced_parens_preserved(self):
        text = "10.1000/test(1)suffix end"
        assert _extract_doi_matches(text) == ["10.1000/test(1)suffix"]

    def test_unbalanced_trailing_paren_stripped(self):
        text = "(see 10.1234/abc)"
        assert _extract_doi_matches(text) == ["10.1234/abc"]


class TestExtractPmids(unittest.TestCase):
    def test_pmid_colon(self):
        verifier = CitationVerifier()
        assert verifier.extract_pmids("PMID: 12345678") == ["12345678"]

    def test_pmid_bibtex(self):
        verifier = CitationVerifier()
        assert verifier.extract_pmids("pmid = {12345678}") == ["12345678"]

    def test_pmid_dedup(self):
        verifier = CitationVerifier()
        text = "PMID: 111 and pmid = {111}"
        assert verifier.extract_pmids(text) == ["111"]


class TestStripCodeBlocks(unittest.TestCase):
    def test_removes_fenced_blocks(self):
        text = "before\n```python\ncode\n```\nafter"
        assert _strip_code_blocks(text) == "before\n\nafter"

    def test_no_code_blocks(self):
        text = "plain text"
        assert _strip_code_blocks(text) == "plain text"

    def test_keep_bibtex_blocks(self):
        text = "before\n```python\ncode\n```\nmid\n```bibtex\n@article{X}\n```\nafter"
        result = _strip_code_blocks(text, keep_bibtex=True)
        assert "code" not in result
        assert "@article{X}" in result


class TestUniqueKey(unittest.TestCase):
    def test_first_key(self):
        seen = set()
        key, renamed = _unique_key("Smith_2023", seen)
        assert key == "Smith_2023"
        assert renamed is None

    def test_collision_renames_first(self):
        seen = set()
        _unique_key("Smith_2023", seen)
        key, renamed = _unique_key("Smith_2023", seen)
        assert key == "Smith_2023b"
        assert renamed == ("Smith_2023", "Smith_2023a")

    def test_second_collision_gets_b(self):
        seen = set()
        _unique_key("X", seen)
        key, _ = _unique_key("X", seen)
        assert key == "Xb"
        assert "Xa" in seen

    def test_triple_collision_gets_c(self):
        seen = set()
        _unique_key("X", seen)
        _unique_key("X", seen)
        key, renamed = _unique_key("X", seen)
        assert key == "Xc"
        assert renamed is None


class TestCrossrefTypeMap(unittest.TestCase):
    def test_expected_types(self):
        assert _CROSSREF_TYPE_MAP["journal-article"] == "article"
        assert _CROSSREF_TYPE_MAP["book-chapter"] == "incollection"
        assert _CROSSREF_TYPE_MAP["report"] == "techreport"
        assert _CROSSREF_TYPE_MAP["dataset"] == "misc"


class TestDeduplicateResults(unittest.TestCase):
    def test_dedup_by_doi(self):
        results = [
            {"title": "A", "doi": "10.1234/a"},
            {"title": "A copy", "doi": "10.1234/a"},
        ]
        assert len(deduplicate_results(results)) == 1

    def test_dedup_by_pmid(self):
        results = [
            {"title": "B", "pmid": "111"},
            {"title": "B copy", "pmid": "111"},
        ]
        assert len(deduplicate_results(results)) == 1

    def test_dedup_by_normalized_title(self):
        results = [
            {"title": "My Great Study."},
            {"title": "My great study"},
        ]
        assert len(deduplicate_results(results)) == 1

    def test_no_false_dedup(self):
        results = [
            {"title": "Study A", "doi": "10.1234/a"},
            {"title": "Study B", "doi": "10.1234/b"},
        ]
        assert len(deduplicate_results(results)) == 2

    def test_dedup_same_title_different_dois(self):
        results = [
            {"title": "Same Title", "doi": "10.1234/a"},
            {"title": "Same Title", "doi": "10.1234/b"},
        ]
        assert len(deduplicate_results(results)) == 1


class TestNextSuffix(unittest.TestCase):
    def test_letters(self):
        assert _next_suffix(1) == "a"
        assert _next_suffix(26) == "z"

    def test_numbers_after_z(self):
        assert _next_suffix(27) == "27"
        assert _next_suffix(100) == "100"


class TestFilterByYear(unittest.TestCase):
    def test_start_year(self):
        results = [{"year": "2020"}, {"year": "2022"}, {"year": "2018"}]
        filtered = filter_by_year(results, start_year=2020)
        assert len(filtered) == 2

    def test_end_year(self):
        results = [{"year": "2020"}, {"year": "2022"}, {"year": "2018"}]
        filtered = filter_by_year(results, end_year=2020)
        assert len(filtered) == 2

    def test_range(self):
        results = [{"year": "2018"}, {"year": "2020"}, {"year": "2022"}]
        filtered = filter_by_year(results, start_year=2019, end_year=2021)
        assert len(filtered) == 1
        assert filtered[0]["year"] == "2020"

    def test_invalid_year_included(self):
        results = [{"year": "N/A"}, {"year": "2020"}]
        filtered = filter_by_year(results, start_year=2019)
        assert len(filtered) == 2


class TestRankResults(unittest.TestCase):
    def test_rank_by_citations(self):
        results = [{"citations": 5}, {"citations": 20}, {"citations": 1}]
        ranked = rank_results(results, "citations")
        assert ranked[0]["citations"] == 20
        assert ranked[-1]["citations"] == 1

    def test_rank_by_year(self):
        results = [{"year": "2018"}, {"year": "2022"}, {"year": "2020"}]
        ranked = rank_results(results, "year")
        assert ranked[0]["year"] == "2022"

    def test_unknown_criteria(self):
        results = [{"title": "A"}, {"title": "B"}]
        assert rank_results(results, "unknown") == results


class TestFormatSearchResults(unittest.TestCase):
    def test_json_format(self):
        results = [{"title": "Test"}]
        output = format_search_results(results, "json")
        assert '"title": "Test"' in output

    def test_unknown_format_raises(self):
        with self.assertRaises(ValueError):
            format_search_results([], "xml")

    def test_empty_bibtex(self):
        assert format_search_results([], "bibtex") == ""


class TestEscapeBibtex(unittest.TestCase):
    def test_ampersand(self):
        assert _escape_bibtex("R&D") == r"R\&D"

    def test_percent(self):
        assert _escape_bibtex("100%") == r"100\%"

    def test_hash_underscore_dollar(self):
        assert _escape_bibtex("a#b_c$d") == r"a\#b\_c\$d"

    def test_no_special(self):
        assert _escape_bibtex("Normal title") == "Normal title"

    def test_multiple_specials(self):
        assert _escape_bibtex("A & B: 50% of C#1") == r"A \& B: 50\% of C\#1"


class TestExtractBibtexEntries(unittest.TestCase):
    def test_simple_entry(self):
        text = '@article{Key, title={Test}}'
        entries = _extract_bibtex_entries(text)
        assert len(entries) == 1
        assert entries[0] == text

    def test_at_in_field_value(self):
        text = '@article{Key, author={user@example.com}, title={Test}}'
        entries = _extract_bibtex_entries(text)
        assert len(entries) == 1
        assert "user@example.com" in entries[0]

    def test_nested_braces(self):
        text = '@article{Key, title={{Nested {braces} here}}}'
        entries = _extract_bibtex_entries(text)
        assert len(entries) == 1
        assert entries[0] == text

    def test_multiple_entries(self):
        text = '@article{A, title={First}}\n\n@book{B, title={Second}}'
        entries = _extract_bibtex_entries(text)
        assert len(entries) == 2

    def test_surrounding_text_ignored(self):
        text = 'Some text before\n@article{Key, doi={10.1234/abc}}\nSome text after'
        entries = _extract_bibtex_entries(text)
        assert len(entries) == 1
        assert "10.1234/abc" in entries[0]


class TestBibtexFormatEscaping(unittest.TestCase):
    def test_special_chars_in_title(self):
        results = [{"title": "R&D in 50% of cases", "authors": "Smith, J.", "year": "2023"}]
        output = format_search_results(results, "bibtex")
        assert r"R\&D in 50\% of cases" in output

    def test_special_chars_in_journal(self):
        results = [{"title": "Test", "authors": "A", "year": "2023", "journal": "Science & Nature"}]
        output = format_search_results(results, "bibtex")
        assert r"Science \& Nature" in output


if __name__ == "__main__":
    unittest.main()
