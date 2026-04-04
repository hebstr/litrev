"""Tests for s2_search: search_s2 + _s2_result_to_record."""

import json
import os
from unittest.mock import patch, MagicMock

import pytest

from litrev_mcp.tools.s2_search import search_s2, _s2_result_to_record


def _mock_response(body, status_code=200):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = body
    resp.raise_for_status.return_value = None
    return resp


class TestS2ResultToRecord:
    def test_full_record(self):
        paper = {
            "title": "Test Paper",
            "authors": [{"name": "Smith J"}, {"name": "Doe A"}],
            "year": 2022,
            "externalIds": {"DOI": "10.1234/test", "PubMed": "99999"},
            "journal": {"name": "Nature"},
            "citationCount": 50,
            "abstract": "Abstract text.",
            "url": "https://s2.org/p/123",
        }
        rec = _s2_result_to_record(paper)
        assert rec["title"] == "Test Paper"
        assert rec["doi"] == "10.1234/test"
        assert rec["pmid"] == "99999"
        assert rec["authors"] == ["Smith J", "Doe A"]
        assert rec["year"] == "2022"
        assert rec["citations"] == 50
        assert rec["journal"] == "Nature"
        assert rec["abstract"] == "Abstract text."
        assert rec["source"] == "S2-search"
        assert rec["first_author"] == "Smith"

    def test_no_title_returns_none(self):
        assert _s2_result_to_record({}) is None
        assert _s2_result_to_record({"title": ""}) is None
        assert _s2_result_to_record({"title": None}) is None

    def test_missing_optional_fields(self):
        rec = _s2_result_to_record({"title": "Minimal"})
        assert rec["doi"] == ""
        assert rec["pmid"] == ""
        assert rec["authors"] == []
        assert rec["journal"] == ""
        assert rec["year"] == ""
        assert rec["abstract"] == ""
        assert rec["citations"] == 0
        assert "first_author" not in rec

    def test_null_external_ids(self):
        rec = _s2_result_to_record({"title": "T", "externalIds": None})
        assert rec["doi"] == ""
        assert rec["pmid"] == ""

    def test_null_journal(self):
        rec = _s2_result_to_record({"title": "T", "journal": None})
        assert rec["journal"] == ""

    def test_null_authors(self):
        rec = _s2_result_to_record({"title": "T", "authors": None})
        assert rec["authors"] == []

    def test_author_without_name_skipped(self):
        paper = {"title": "T", "authors": [{"name": "Good"}, {}, {"name": ""}]}
        rec = _s2_result_to_record(paper)
        assert rec["authors"] == ["Good"]


@patch("litrev_mcp.tools.s2_search.s2_throttle")
@patch("litrev_mcp.tools.s2_search.request_with_retry")
class TestSearchS2:
    def test_happy_path(self, mock_req, mock_throttle):
        mock_req.return_value = _mock_response(
            {
                "total": 200,
                "data": [{"title": "Paper A", "year": 2022}],
            }
        )
        result = search_s2("rotator cuff")
        assert result["status"] == "ok"
        assert result["total_in_s2"] == 200
        assert result["returned"] == 1
        assert len(result["results"]) == 1
        mock_throttle.assert_called_once()

    def test_api_error(self, mock_req, mock_throttle):
        mock_req.side_effect = Exception("timeout")
        result = search_s2("query")
        assert result["status"] == "error"
        assert "timeout" in result["error"]
        assert result["results"] == []

    def test_empty_results(self, mock_req, mock_throttle):
        mock_req.return_value = _mock_response({"total": 0, "data": []})
        result = search_s2("nonexistent")
        assert result["returned"] == 0
        assert result["results"] == []

    def test_skips_titleless_papers(self, mock_req, mock_throttle):
        mock_req.return_value = _mock_response(
            {
                "total": 2,
                "data": [{"title": "Good"}, {"title": None}],
            }
        )
        result = search_s2("q")
        assert result["returned"] == 1

    def test_output_path_writes_file(self, mock_req, mock_throttle, tmp_path):
        mock_req.return_value = _mock_response(
            {
                "total": 1,
                "data": [{"title": "Paper"}],
            }
        )
        out = str(tmp_path / "out.json")
        result = search_s2("q", output_path=out)
        assert result["output_path"] == out
        assert result["results"] == []
        with open(out) as f:
            data = json.load(f)
        assert len(data) == 1

    def test_year_range_params(self, mock_req, mock_throttle):
        mock_req.return_value = _mock_response({"total": 0, "data": []})
        search_s2("q", year_start=2020, year_end=2023)
        params = mock_req.call_args.kwargs.get("params") or mock_req.call_args[1].get(
            "params"
        )
        assert params["year"] == "2020-2023"

    def test_year_start_only(self, mock_req, mock_throttle):
        mock_req.return_value = _mock_response({"total": 0, "data": []})
        search_s2("q", year_start=2020)
        params = mock_req.call_args.kwargs.get("params") or mock_req.call_args[1].get(
            "params"
        )
        assert params["year"] == "2020-"

    def test_year_end_only(self, mock_req, mock_throttle):
        mock_req.return_value = _mock_response({"total": 0, "data": []})
        search_s2("q", year_end=2019)
        params = mock_req.call_args.kwargs.get("params") or mock_req.call_args[1].get(
            "params"
        )
        assert params["year"] == "-2019"

    def test_limit_capped_at_100(self, mock_req, mock_throttle):
        mock_req.return_value = _mock_response({"total": 0, "data": []})
        search_s2("q", limit=500)
        params = mock_req.call_args.kwargs.get("params") or mock_req.call_args[1].get(
            "params"
        )
        assert params["limit"] == 100

    def test_fields_of_study_none(self, mock_req, mock_throttle):
        mock_req.return_value = _mock_response({"total": 0, "data": []})
        search_s2("q", fields_of_study=None)
        params = mock_req.call_args.kwargs.get("params") or mock_req.call_args[1].get(
            "params"
        )
        assert "fieldsOfStudy" not in params

    def test_fields_of_study_default(self, mock_req, mock_throttle):
        mock_req.return_value = _mock_response({"total": 0, "data": []})
        search_s2("q")
        params = mock_req.call_args.kwargs.get("params") or mock_req.call_args[1].get(
            "params"
        )
        assert params["fieldsOfStudy"] == "Medicine"
