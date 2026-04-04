"""Tests for abstracts: fetch_abstracts + _format_articles."""

import json
import os
from unittest.mock import patch

import pytest

from litrev_mcp.tools.abstracts import fetch_abstracts, _format_articles


def _write_results(tmp_path, articles):
    path = str(tmp_path / "combined_results.json")
    with open(path, "w") as f:
        json.dump(articles, f)
    return path


class TestFormatArticles:
    def test_basic_formatting(self):
        articles = [
            (
                0,
                {
                    "title": "Test Article",
                    "authors": ["Smith J", "Doe A"],
                    "year": 2020,
                    "doi": "10.1234/test",
                    "pmid": "12345",
                    "abstract": "This is the abstract.",
                },
            )
        ]
        result = _format_articles(articles)
        assert "## [0] Test Article" in result
        assert "Smith J, Doe A" in result
        assert "DOI: 10.1234/test" in result
        assert "PMID: 12345" in result
        assert "This is the abstract." in result

    def test_authors_truncated_after_three(self):
        articles = [
            (
                0,
                {
                    "title": "Title",
                    "authors": ["A", "B", "C", "D", "E"],
                    "year": 2021,
                },
            )
        ]
        result = _format_articles(articles)
        assert "A, B, C et al." in result

    def test_three_authors_no_et_al(self):
        articles = [
            (
                0,
                {
                    "title": "Title",
                    "authors": ["A", "B", "C"],
                    "year": 2021,
                },
            )
        ]
        result = _format_articles(articles)
        assert "A, B, C" in result
        assert "et al." not in result

    def test_authors_as_string(self):
        articles = [(0, {"title": "T", "authors": "Smith J", "year": 2020})]
        result = _format_articles(articles)
        assert "Smith J" in result

    def test_missing_fields_defaults(self):
        articles = [(5, {})]
        result = _format_articles(articles)
        assert "## [5] Untitled" in result
        assert "Unknown" in result
        assert "N/A" in result
        assert "No abstract available" in result

    def test_no_doi_no_pmid_no_meta_line(self):
        articles = [(0, {"title": "T", "authors": [], "year": 2020, "abstract": "A"})]
        result = _format_articles(articles)
        assert "DOI:" not in result
        assert "PMID:" not in result

    def test_study_type_shown(self):
        articles = [
            (
                0,
                {
                    "title": "T",
                    "study_type": "RCT",
                },
            )
        ]
        result = _format_articles(articles)
        assert "Type: RCT" in result


class TestFetchAbstracts:
    def test_empty_indices(self, tmp_path):
        path = _write_results(tmp_path, [{"title": "A"}])
        result = fetch_abstracts(path, [])
        assert "error" in result

    def test_all_indices_out_of_bounds(self, tmp_path):
        path = _write_results(tmp_path, [{"title": "A"}])
        result = fetch_abstracts(path, [5, 10])
        assert "error" in result

    def test_valid_indices_with_abstracts(self, tmp_path):
        articles = [
            {"title": "Article 1", "abstract": "Abstract 1", "authors": ["X"]},
            {"title": "Article 2", "abstract": "Abstract 2", "authors": ["Y"]},
        ]
        path = _write_results(tmp_path, articles)
        out = str(tmp_path / "review" / "abstracts.md")
        result = fetch_abstracts(path, [0, 1], output_path=out)
        assert result["total"] == 2
        assert result["with_abstract"] == 2
        assert result["without_abstract"] == 0
        assert result["fetched_from_pubmed"] == 0
        assert os.path.exists(out)

    @patch("litrev_mcp.tools.abstracts.fetch_abstracts_from_pubmed")
    def test_fetch_missing_from_pubmed(self, mock_fetch, tmp_path):
        mock_fetch.return_value = {"111": "Fetched abstract"}
        articles = [
            {"title": "No abs", "pmid": "111", "authors": ["A"]},
        ]
        path = _write_results(tmp_path, articles)
        out = str(tmp_path / "review" / "abstracts.md")
        result = fetch_abstracts(path, [0], output_path=out)
        assert result["fetched_from_pubmed"] == 1
        assert result["fetch_attempted"] == 1
        assert result["with_abstract"] == 1
        with open(path) as f:
            updated = json.load(f)
        assert updated[0]["abstract"] == "Fetched abstract"

    @patch("litrev_mcp.tools.abstracts.fetch_abstracts_from_pubmed")
    def test_no_fetch_when_disabled(self, mock_fetch, tmp_path):
        articles = [{"title": "T", "pmid": "111", "authors": ["A"]}]
        path = _write_results(tmp_path, articles)
        out = str(tmp_path / "review" / "abstracts.md")
        result = fetch_abstracts(path, [0], fetch_missing=False, output_path=out)
        mock_fetch.assert_not_called()
        assert result["fetch_attempted"] == 0

    @patch("litrev_mcp.tools.abstracts.fetch_abstracts_from_pubmed")
    def test_no_fetch_when_abstract_present(self, mock_fetch, tmp_path):
        articles = [
            {"title": "T", "pmid": "111", "abstract": "Exists", "authors": ["A"]}
        ]
        path = _write_results(tmp_path, articles)
        out = str(tmp_path / "review" / "abstracts.md")
        fetch_abstracts(path, [0], output_path=out)
        mock_fetch.assert_not_called()

    @patch("litrev_mcp.tools.abstracts.fetch_abstracts_from_pubmed")
    def test_no_fetch_without_pmid(self, mock_fetch, tmp_path):
        articles = [{"title": "T", "authors": ["A"]}]
        path = _write_results(tmp_path, articles)
        out = str(tmp_path / "review" / "abstracts.md")
        result = fetch_abstracts(path, [0], output_path=out)
        mock_fetch.assert_not_called()
        assert result["fetch_attempted"] == 0

    @patch("litrev_mcp.tools.abstracts.fetch_abstracts_from_pubmed")
    def test_dedup_pmids(self, mock_fetch, tmp_path):
        mock_fetch.return_value = {"111": "Abstract"}
        articles = [
            {"title": "A", "pmid": "111", "authors": ["X"]},
            {"title": "B", "pmid": "111", "authors": ["Y"]},
        ]
        path = _write_results(tmp_path, articles)
        out = str(tmp_path / "review" / "abstracts.md")
        fetch_abstracts(path, [0, 1], output_path=out)
        mock_fetch.assert_called_once_with(["111"])

    def test_mixed_valid_invalid_indices(self, tmp_path):
        articles = [{"title": "Only", "abstract": "A", "authors": ["X"]}]
        path = _write_results(tmp_path, articles)
        out = str(tmp_path / "review" / "abstracts.md")
        result = fetch_abstracts(path, [0, 5, -1], output_path=out)
        assert result["total"] == 1

    def test_default_output_path(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        articles = [{"title": "T", "abstract": "A", "authors": ["X"]}]
        path = _write_results(tmp_path, articles)
        result = fetch_abstracts(path, [0])
        assert result["output_path"] == "review/abstracts_for_screening.md"
        assert os.path.exists("review/abstracts_for_screening.md")
