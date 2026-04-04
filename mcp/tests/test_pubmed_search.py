"""Tests for pubmed_search: search_pubmed + helper functions."""

import json
import os
from unittest.mock import patch, MagicMock, call

import pytest

from litrev_mcp.tools.pubmed_search import (
    search_pubmed,
    _extract_doi,
    _extract_year,
    _summary_to_record,
)


def _mock_response(body, status_code=200):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = body
    resp.raise_for_status.return_value = None
    return resp


class TestExtractDoi:
    def test_finds_doi(self):
        ids = [
            {"idtype": "pubmed", "value": "12345"},
            {"idtype": "doi", "value": "10.1234/test"},
        ]
        assert _extract_doi(ids) == "10.1234/test"

    def test_no_doi(self):
        assert _extract_doi([{"idtype": "pubmed", "value": "12345"}]) == ""

    def test_empty_list(self):
        assert _extract_doi([]) == ""

    def test_doi_without_value(self):
        assert _extract_doi([{"idtype": "doi"}]) == ""


class TestExtractYear:
    def test_standard_pubdate(self):
        assert _extract_year("2020 Jan 15") == "2020"

    def test_year_only(self):
        assert _extract_year("2023") == "2023"

    def test_empty_string(self):
        assert _extract_year("") == ""

    def test_none(self):
        assert _extract_year(None) == ""

    def test_no_year_pattern(self):
        assert _extract_year("Jan") == ""


class TestSummaryToRecord:
    def test_full_record(self):
        doc = {
            "title": "Test Article",
            "authors": [{"name": "Smith J"}, {"name": "Doe A"}],
            "pubdate": "2021 Mar",
            "articleids": [{"idtype": "doi", "value": "10.1/x"}],
            "fulljournalname": "The Lancet",
            "pubtype": ["Journal Article"],
        }
        rec = _summary_to_record("99999", doc, "Abstract text")
        assert rec["title"] == "Test Article"
        assert rec["pmid"] == "99999"
        assert rec["authors"] == ["Smith J", "Doe A"]
        assert rec["year"] == "2021"
        assert rec["doi"] == "10.1/x"
        assert rec["journal"] == "The Lancet"
        assert rec["abstract"] == "Abstract text"
        assert rec["source"] == "PubMed-search"
        assert rec["first_author"] == "Smith"
        assert rec["publication_type"] == ["Journal Article"]
        assert "pubmed.ncbi.nlm.nih.gov/99999" in rec["url"]

    def test_no_title_returns_none(self):
        assert _summary_to_record("1", {"title": ""}, "") is None
        assert _summary_to_record("1", {}, "") is None

    def test_missing_optional_fields(self):
        rec = _summary_to_record("1", {"title": "T"}, "")
        assert rec["authors"] == []
        assert rec["doi"] == ""
        assert rec["year"] == ""
        assert rec["publication_type"] == []
        assert "first_author" not in rec


@patch("litrev_mcp.tools.pubmed_search.fetch_abstracts_from_pubmed")
@patch("litrev_mcp.tools.pubmed_search.request_with_retry")
class TestSearchPubmed:
    def _esearch_response(self, pmids, count=None):
        return _mock_response(
            {
                "esearchresult": {
                    "count": str(count or len(pmids)),
                    "idlist": pmids,
                }
            }
        )

    def _esummary_response(self, docs):
        return _mock_response({"result": docs})

    def test_happy_path(self, mock_req, mock_abs):
        mock_req.side_effect = [
            self._esearch_response(["111", "222"]),
            self._esummary_response(
                {
                    "111": {
                        "title": "Paper A",
                        "authors": [{"name": "X"}],
                        "pubdate": "2020",
                        "articleids": [],
                    },
                    "222": {
                        "title": "Paper B",
                        "authors": [{"name": "Y"}],
                        "pubdate": "2021",
                        "articleids": [],
                    },
                }
            ),
        ]
        mock_abs.return_value = {"111": "Abs A", "222": "Abs B"}
        result = search_pubmed("test query")
        assert result["status"] == "ok"
        assert result["returned"] == 2
        assert result["results"][0]["title"] == "Paper A"
        assert result["results"][0]["abstract"] == "Abs A"

    def test_esearch_error(self, mock_req, mock_abs):
        mock_req.side_effect = Exception("connection error")
        result = search_pubmed("query")
        assert result["status"] == "error"
        assert result["results"] == []
        mock_abs.assert_not_called()

    def test_no_results(self, mock_req, mock_abs):
        mock_req.return_value = self._esearch_response([], count=0)
        result = search_pubmed("obscure query")
        assert result["status"] == "ok"
        assert result["returned"] == 0
        assert result["results"] == []
        mock_abs.assert_not_called()

    def test_esummary_batch_failure_continues(self, mock_req, mock_abs):
        mock_req.side_effect = [
            self._esearch_response(["111"]),
            Exception("batch failed"),
        ]
        mock_abs.return_value = {}
        result = search_pubmed("q")
        assert result["status"] == "ok"
        assert result["returned"] == 0

    def test_date_params(self, mock_req, mock_abs):
        mock_req.return_value = self._esearch_response([])
        search_pubmed("q", date_start="2020/01/01", date_end="2023/12/31")
        params = mock_req.call_args.kwargs.get("params") or mock_req.call_args[1].get(
            "params"
        )
        assert params["datetype"] == "pdat"
        assert params["mindate"] == "2020/01/01"
        assert params["maxdate"] == "2023/12/31"

    def test_output_path_writes_file(self, mock_req, mock_abs, tmp_path):
        mock_req.side_effect = [
            self._esearch_response(["111"]),
            self._esummary_response(
                {"111": {"title": "P", "pubdate": "2020", "articleids": []}}
            ),
        ]
        mock_abs.return_value = {}
        out = str(tmp_path / "results.json")
        result = search_pubmed("q", output_path=out)
        assert result["results"] == []
        assert os.path.exists(out)
        with open(out) as f:
            data = json.load(f)
        assert len(data) == 1

    def test_titleless_doc_skipped(self, mock_req, mock_abs):
        mock_req.side_effect = [
            self._esearch_response(["111"]),
            self._esummary_response({"111": {"title": "", "pubdate": "2020"}}),
        ]
        mock_abs.return_value = {}
        result = search_pubmed("q")
        assert result["returned"] == 0

    def test_pmid_missing_from_summary(self, mock_req, mock_abs):
        mock_req.side_effect = [
            self._esearch_response(["111", "222"]),
            self._esummary_response(
                {"111": {"title": "P", "pubdate": "2020", "articleids": []}}
            ),
        ]
        mock_abs.return_value = {}
        result = search_pubmed("q")
        assert result["returned"] == 1
