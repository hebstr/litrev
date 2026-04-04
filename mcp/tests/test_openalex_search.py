"""Tests for openalex_search: search_openalex + _oa_result_to_record."""

import json
import os
from unittest.mock import patch, MagicMock

import pytest

from litrev_mcp.tools.openalex_search import search_openalex, _oa_result_to_record


def _mock_response(body, status_code=200):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = body
    resp.raise_for_status.return_value = None
    return resp


class TestOaResultToRecord:
    def test_full_record(self):
        work = {
            "title": "Test Paper",
            "doi": "https://doi.org/10.1234/test",
            "ids": {"pmid": "https://pubmed.ncbi.nlm.nih.gov/99999/"},
            "authorships": [
                {"author": {"display_name": "Smith John"}},
                {"author": {"display_name": "Doe Jane"}},
            ],
            "publication_year": 2023,
            "cited_by_count": 42,
            "primary_location": {"source": {"display_name": "Nature"}},
            "id": "https://openalex.org/W12345",
        }
        rec = _oa_result_to_record(work)
        assert rec["title"] == "Test Paper"
        assert rec["doi"] == "10.1234/test"
        assert rec["pmid"] == "99999"
        assert rec["authors"] == ["Smith John", "Doe Jane"]
        assert rec["year"] == "2023"
        assert rec["citations"] == 42
        assert rec["journal"] == "Nature"
        assert rec["source"] == "OpenAlex-search"
        assert rec["first_author"] == "Smith"

    def test_no_title_returns_none(self):
        assert _oa_result_to_record({}) is None
        assert _oa_result_to_record({"title": ""}) is None
        assert _oa_result_to_record({"title": None}) is None

    def test_missing_optional_fields(self):
        rec = _oa_result_to_record({"title": "Minimal"})
        assert rec["doi"] == ""
        assert rec["pmid"] == ""
        assert rec["authors"] == []
        assert rec["journal"] == ""
        assert rec["year"] == ""
        assert rec["citations"] == 0
        assert "first_author" not in rec

    def test_null_nested_fields(self):
        work = {
            "title": "T",
            "authorships": None,
            "ids": None,
            "primary_location": None,
        }
        rec = _oa_result_to_record(work)
        assert rec["authors"] == []
        assert rec["pmid"] == ""
        assert rec["journal"] == ""

    def test_doi_without_prefix(self):
        rec = _oa_result_to_record({"title": "T", "doi": "10.1234/raw"})
        assert rec["doi"] == "10.1234/raw"

    def test_author_with_no_name_skipped(self):
        work = {
            "title": "T",
            "authorships": [
                {"author": {"display_name": "Good"}},
                {"author": {}},
                {"author": None},
                {},
            ],
        }
        rec = _oa_result_to_record(work)
        assert rec["authors"] == ["Good"]


@patch("litrev_mcp.tools.openalex_search.request_with_retry")
class TestSearchOpenalex:
    def test_happy_path(self, mock_req, tmp_path):
        mock_req.return_value = _mock_response(
            {
                "meta": {"count": 100},
                "results": [{"title": "Paper A", "publication_year": 2022}],
            }
        )
        result = search_openalex("rotator cuff")
        assert result["status"] == "ok"
        assert result["total_in_openalex"] == 100
        assert result["returned"] == 1
        assert len(result["results"]) == 1
        assert result["results"][0]["title"] == "Paper A"

    def test_api_error(self, mock_req):
        mock_req.side_effect = Exception("timeout")
        result = search_openalex("query")
        assert result["status"] == "error"
        assert "timeout" in result["error"]
        assert result["results"] == []

    def test_empty_results(self, mock_req):
        mock_req.return_value = _mock_response(
            {
                "meta": {"count": 0},
                "results": [],
            }
        )
        result = search_openalex("nonexistent topic xyz")
        assert result["returned"] == 0
        assert result["results"] == []

    def test_skips_titleless_works(self, mock_req):
        mock_req.return_value = _mock_response(
            {
                "meta": {"count": 2},
                "results": [
                    {"title": "Good"},
                    {"title": None},
                ],
            }
        )
        result = search_openalex("q")
        assert result["returned"] == 1

    def test_output_path_writes_file(self, mock_req, tmp_path):
        mock_req.return_value = _mock_response(
            {
                "meta": {"count": 1},
                "results": [{"title": "Paper"}],
            }
        )
        out = str(tmp_path / "out.json")
        result = search_openalex("q", output_path=out)
        assert result["output_path"] == out
        assert result["results"] == []
        with open(out) as f:
            data = json.load(f)
        assert len(data) == 1

    def test_year_range_params(self, mock_req):
        mock_req.return_value = _mock_response({"meta": {}, "results": []})
        search_openalex("q", year_start=2020, year_end=2023)
        call_kwargs = mock_req.call_args
        params = call_kwargs.kwargs.get("params") or call_kwargs[1].get("params")
        assert "publication_year:2020-2023" in params["filter"]

    def test_year_start_only(self, mock_req):
        mock_req.return_value = _mock_response({"meta": {}, "results": []})
        search_openalex("q", year_start=2020)
        params = mock_req.call_args.kwargs.get("params") or mock_req.call_args[1].get(
            "params"
        )
        assert "publication_year:>=2020" in params["filter"]

    def test_year_end_only(self, mock_req):
        mock_req.return_value = _mock_response({"meta": {}, "results": []})
        search_openalex("q", year_end=2019)
        params = mock_req.call_args.kwargs.get("params") or mock_req.call_args[1].get(
            "params"
        )
        assert "publication_year:<=2019" in params["filter"]

    def test_limit_capped(self, mock_req):
        mock_req.return_value = _mock_response({"meta": {}, "results": []})
        search_openalex("q", limit=500)
        params = mock_req.call_args.kwargs.get("params") or mock_req.call_args[1].get(
            "params"
        )
        assert params["per_page"] == 200
