#!/usr/bin/env python3
"""Unit tests for citation_chaining.py (no network calls)."""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from citation_chaining import (
    _resolve_s2_id,
    _s2_paper_to_record,
    _oa_work_to_record,
    chain,
)


class TestResolveS2Id(unittest.TestCase):
    def test_doi_preferred(self):
        paper = {"doi": "10.1234/abc", "pmid": "12345"}
        assert _resolve_s2_id(paper) == "DOI:10.1234/abc"

    def test_pmid_fallback(self):
        paper = {"pmid": "12345"}
        assert _resolve_s2_id(paper) == "PMID:12345"

    def test_none_when_no_ids(self):
        assert _resolve_s2_id({}) is None
        assert _resolve_s2_id({"doi": "", "pmid": ""}) is None

    def test_whitespace_doi_ignored(self):
        assert _resolve_s2_id({"doi": "  ", "pmid": "999"}) == "PMID:999"


class TestS2PaperToRecord(unittest.TestCase):
    def test_full_record(self):
        p = {
            "title": "Test Study",
            "authors": [{"name": "Smith J"}, {"name": "Doe A"}],
            "year": 2023,
            "externalIds": {"DOI": "10.1234/test", "PubMed": "99999"},
            "journal": {"name": "Test Journal"},
            "citationCount": 42,
            "abstract": "Some abstract.",
            "url": "https://example.com",
        }
        rec = _s2_paper_to_record(p, "S2-forward")
        assert rec["title"] == "Test Study"
        assert rec["authors"] == ["Smith J", "Doe A"]
        assert rec["year"] == 2023
        assert rec["doi"] == "10.1234/test"
        assert rec["pmid"] == "99999"
        assert rec["journal"] == "Test Journal"
        assert rec["citations"] == 42
        assert rec["source"] == "S2-forward"
        assert rec["first_author"] == "Smith"

    def test_missing_title_returns_none(self):
        assert _s2_paper_to_record({}, "S2-backward") is None
        assert _s2_paper_to_record({"title": None}, "S2-backward") is None

    def test_minimal_record(self):
        p = {"title": "Minimal"}
        rec = _s2_paper_to_record(p, "S2-forward")
        assert rec["title"] == "Minimal"
        assert rec["doi"] == ""
        assert rec["authors"] == []
        assert rec["citations"] == 0

    def test_empty_authors_skipped(self):
        p = {"title": "T", "authors": [{"name": ""}, {"name": "Real"}]}
        rec = _s2_paper_to_record(p, "S2-forward")
        assert rec["authors"] == ["Real"]


class TestOaWorkToRecord(unittest.TestCase):
    def test_full_record(self):
        w = {
            "display_name": "OA Study",
            "doi": "https://doi.org/10.5678/oa",
            "ids": {"pmid": "https://pubmed.ncbi.nlm.nih.gov/88888/"},
            "authorships": [
                {"author": {"display_name": "Jones K"}},
                {"author": {"display_name": "Lee M"}},
            ],
            "publication_year": 2022,
            "cited_by_count": 15,
            "primary_location": {"source": {"display_name": "OA Journal"}},
        }
        rec = _oa_work_to_record(w, "OA-backward")
        assert rec["title"] == "OA Study"
        assert rec["doi"] == "10.5678/oa"
        assert rec["pmid"] == "88888"
        assert rec["authors"] == ["Jones K", "Lee M"]
        assert rec["year"] == 2022
        assert rec["citations"] == 15
        assert rec["journal"] == "OA Journal"
        assert rec["source"] == "OA-backward"
        assert rec["first_author"] == "Jones"

    def test_missing_title_returns_none(self):
        assert _oa_work_to_record({}, "OA-forward") is None

    def test_no_doi_prefix(self):
        w = {"display_name": "T", "doi": "10.1234/raw"}
        rec = _oa_work_to_record(w, "OA-forward")
        assert rec["doi"] == "10.1234/raw"

    def test_missing_optional_fields(self):
        w = {"display_name": "Sparse"}
        rec = _oa_work_to_record(w, "OA-forward")
        assert rec["doi"] == ""
        assert rec["pmid"] == ""
        assert rec["authors"] == []
        assert rec["journal"] == ""
        assert rec["citations"] == 0


class TestChain(unittest.TestCase):
    def _make_seed(self, doi="10.1234/seed", pmid=""):
        return {"title": "Seed", "doi": doi, "pmid": pmid}

    @patch("citation_chaining.fetch_s2_references")
    @patch("citation_chaining.fetch_s2_citations")
    @patch("citation_chaining.fetch_oa_references")
    @patch("citation_chaining.fetch_oa_citations")
    def test_both_directions_both_sources(self, mock_oa_cit, mock_oa_ref, mock_s2_cit, mock_s2_ref):
        mock_s2_ref.return_value = [{"title": "S2 ref", "source": "S2-backward"}]
        mock_s2_cit.return_value = [{"title": "S2 cit", "source": "S2-forward"}]
        mock_oa_ref.return_value = [{"title": "OA ref", "source": "OA-backward"}]
        mock_oa_cit.return_value = [{"title": "OA cit", "source": "OA-forward"}]

        results = chain([self._make_seed()], ["backward", "forward"], ["s2", "openalex"])
        assert len(results) == 4
        mock_s2_ref.assert_called_once()
        mock_s2_cit.assert_called_once()
        mock_oa_ref.assert_called_once()
        mock_oa_cit.assert_called_once()

    @patch("citation_chaining.fetch_s2_references")
    @patch("citation_chaining.fetch_s2_citations")
    def test_forward_only(self, mock_s2_cit, mock_s2_ref):
        mock_s2_cit.return_value = [{"title": "Cit"}]
        mock_s2_ref.return_value = []

        results = chain([self._make_seed()], ["forward"], ["s2"])
        assert len(results) == 1
        mock_s2_ref.assert_not_called()
        mock_s2_cit.assert_called_once()

    @patch("citation_chaining.fetch_s2_references")
    @patch("citation_chaining.fetch_s2_citations")
    def test_no_doi_no_pmid_skips_s2(self, mock_s2_cit, mock_s2_ref):
        results = chain([self._make_seed(doi="", pmid="")], ["backward", "forward"], ["s2"])
        assert len(results) == 0
        mock_s2_ref.assert_not_called()
        mock_s2_cit.assert_not_called()

    @patch("citation_chaining.fetch_oa_references")
    @patch("citation_chaining.fetch_oa_citations")
    def test_no_doi_skips_openalex(self, mock_oa_cit, mock_oa_ref):
        results = chain([self._make_seed(doi="")], ["backward", "forward"], ["openalex"])
        assert len(results) == 0
        mock_oa_ref.assert_not_called()
        mock_oa_cit.assert_not_called()

    @patch("citation_chaining.fetch_s2_references")
    def test_multiple_seeds(self, mock_s2_ref):
        mock_s2_ref.side_effect = [
            [{"title": "From seed 1"}],
            [{"title": "From seed 2"}],
        ]
        seeds = [self._make_seed(doi="10.1/a"), self._make_seed(doi="10.1/b")]
        results = chain(seeds, ["backward"], ["s2"])
        assert len(results) == 2
        assert mock_s2_ref.call_count == 2


if __name__ == "__main__":
    unittest.main()
