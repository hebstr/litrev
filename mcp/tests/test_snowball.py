"""Tests for snowball: citation_chain + helper functions."""

import json
import os
from unittest.mock import patch, MagicMock

import pytest

from litrev_mcp.tools.snowball import (
    citation_chain,
    _resolve_s2_id,
    _s2_paper_to_record,
    _oa_work_to_record,
)


def _mock_response(body, status_code=200):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = body
    resp.raise_for_status.return_value = None
    return resp


def _write_results(tmp_path, articles):
    path = str(tmp_path / "combined_results.json")
    with open(path, "w") as f:
        json.dump(articles, f)
    return path


class TestResolveS2Id:
    def test_doi_preferred(self):
        assert _resolve_s2_id({"doi": "10.1/x", "pmid": "111"}) == "DOI:10.1/x"

    def test_pmid_fallback(self):
        assert _resolve_s2_id({"pmid": "111"}) == "PMID:111"

    def test_pmid_int(self):
        assert _resolve_s2_id({"pmid": 111}) == "PMID:111"

    def test_neither(self):
        assert _resolve_s2_id({}) is None
        assert _resolve_s2_id({"doi": "", "pmid": ""}) is None

    def test_whitespace_doi(self):
        assert _resolve_s2_id({"doi": "  ", "pmid": "111"}) == "PMID:111"


class TestS2PaperToRecord:
    def test_full_record(self):
        p = {
            "title": "Paper",
            "authors": [{"name": "Smith"}],
            "year": 2022,
            "externalIds": {"DOI": "10.1/x", "PubMed": "111"},
            "journal": {"name": "BMJ"},
            "citationCount": 10,
            "abstract": "Abs",
            "url": "https://s2.org/1",
        }
        rec = _s2_paper_to_record(p, "S2-backward")
        assert rec["source"] == "S2-backward"
        assert rec["doi"] == "10.1/x"
        assert rec["first_author"] == "Smith"

    def test_no_title_returns_none(self):
        assert _s2_paper_to_record({}, "S2-backward") is None


class TestOaWorkToRecord:
    def test_display_name_used(self):
        w = {"display_name": "Title A"}
        rec = _oa_work_to_record(w, "OA-forward")
        assert rec["title"] == "Title A"
        assert rec["source"] == "OA-forward"

    def test_title_fallback(self):
        w = {"title": "Title B"}
        rec = _oa_work_to_record(w, "OA-backward")
        assert rec["title"] == "Title B"

    def test_no_title_returns_none(self):
        assert _oa_work_to_record({}, "OA-backward") is None

    def test_doi_normalized(self):
        w = {"display_name": "T", "doi": "https://doi.org/10.1/x"}
        rec = _oa_work_to_record(w, "OA-backward")
        assert rec["doi"] == "10.1/x"

    def test_pmid_normalized(self):
        w = {
            "display_name": "T",
            "ids": {"pmid": "https://pubmed.ncbi.nlm.nih.gov/99999/"},
        }
        rec = _oa_work_to_record(w, "OA-backward")
        assert rec["pmid"] == "99999"


@patch("litrev_mcp.tools.snowball.s2_throttle")
@patch("litrev_mcp.tools.snowball.request_with_retry")
class TestCitationChain:
    def test_no_valid_seeds(self, mock_req, mock_throttle, tmp_path):
        path = _write_results(tmp_path, [{"title": "A"}])
        result = citation_chain(path, [5, 10])
        assert "error" in result

    def test_empty_indices(self, mock_req, mock_throttle, tmp_path):
        path = _write_results(tmp_path, [{"title": "A"}])
        result = citation_chain(path, [])
        assert "error" in result

    def test_backward_s2_only(self, mock_req, mock_throttle, tmp_path):
        seed = {"title": "Seed", "doi": "10.1/seed", "pmid": "111"}
        path = _write_results(tmp_path, [seed])
        out = str(tmp_path / "chaining.json")

        mock_req.return_value = _mock_response(
            {
                "data": [
                    {
                        "citedPaper": {
                            "title": "Ref A",
                            "authors": [],
                            "year": 2020,
                            "externalIds": {"DOI": "10.1/a"},
                        }
                    },
                    {"citedPaper": {"title": None}},
                ]
            }
        )

        result = citation_chain(
            path,
            [0],
            direction="backward",
            sources="s2",
            output_path=out,
        )
        assert result["seeds"] == 1
        assert result["directions"] == ["backward"]
        assert result["sources"] == ["s2"]
        assert result["raw_results"] == 1
        assert os.path.exists(out)

    def test_forward_openalex_only(self, mock_req, mock_throttle, tmp_path):
        seed = {"title": "Seed", "doi": "10.1/seed"}
        path = _write_results(tmp_path, [seed])
        out = str(tmp_path / "chaining.json")

        mock_req.return_value = _mock_response(
            {
                "results": [
                    {"display_name": "Citing A", "doi": "https://doi.org/10.1/c1"},
                ]
            }
        )

        result = citation_chain(
            path,
            [0],
            direction="forward",
            sources="openalex",
            output_path=out,
        )
        assert result["directions"] == ["forward"]
        assert result["sources"] == ["openalex"]
        assert result["raw_results"] >= 1

    def test_both_directions(self, mock_req, mock_throttle, tmp_path):
        seed = {"title": "Seed", "doi": "10.1/seed", "pmid": "111"}
        path = _write_results(tmp_path, [seed])
        out = str(tmp_path / "chaining.json")

        mock_req.return_value = _mock_response({"data": [], "results": []})

        result = citation_chain(path, [0], output_path=out)
        assert result["directions"] == ["backward", "forward"]

    def test_no_doi_no_pmid_skips_sources(self, mock_req, mock_throttle, tmp_path):
        seed = {"title": "Seed"}
        path = _write_results(tmp_path, [seed])
        out = str(tmp_path / "chaining.json")

        result = citation_chain(path, [0], output_path=out)
        assert result["raw_results"] == 0
        mock_req.assert_not_called()

    def test_s2_404_returns_empty(self, mock_req, mock_throttle, tmp_path):
        seed = {"title": "Seed", "doi": "10.1/seed"}
        path = _write_results(tmp_path, [seed])
        out = str(tmp_path / "chaining.json")

        mock_req.return_value = _mock_response({}, status_code=404)

        result = citation_chain(
            path,
            [0],
            direction="backward",
            sources="s2",
            output_path=out,
        )
        assert result["raw_results"] == 0

    def test_seed_log_populated(self, mock_req, mock_throttle, tmp_path):
        seed = {"title": "Seed Paper Title That Is Long", "doi": "10.1/x"}
        path = _write_results(tmp_path, [seed])
        out = str(tmp_path / "chaining.json")

        mock_req.return_value = _mock_response({"data": [], "results": []})

        result = citation_chain(path, [0], output_path=out)
        assert len(result["seed_log"]) == 1
        log = result["seed_log"][0]
        assert log["index"] == 0
        assert "refs" in log
        assert "cites" in log

    def test_duplicates_against_existing(self, mock_req, mock_throttle, tmp_path):
        existing = [
            {"title": "Existing", "doi": "10.1/existing", "pmid": "222"},
        ]
        path = _write_results(tmp_path, existing)
        out = str(tmp_path / "chaining.json")

        mock_req.return_value = _mock_response(
            {
                "data": [
                    {
                        "citedPaper": {
                            "title": "Existing",
                            "externalIds": {"DOI": "10.1/existing"},
                            "authors": [],
                        }
                    },
                    {
                        "citedPaper": {
                            "title": "New Paper",
                            "externalIds": {"DOI": "10.1/new"},
                            "authors": [],
                        }
                    },
                ]
            }
        )

        result = citation_chain(
            path,
            [0],
            direction="backward",
            sources="s2",
            output_path=out,
        )
        assert result["raw_results"] == 2
        assert result["new_unique_candidates"] <= 2
