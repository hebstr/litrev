"""Tests for process_results: dedup, filtering, ranking, output formats."""

import json
import os
import tempfile

import pytest

from litrev_mcp.tools.search import (
    process_results,
    deduplicate_results,
    generate_search_summary,
)


def _write_results(results):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(results, f)
    f.close()
    return f.name


SAMPLE_RESULTS = [
    {
        "pmid": "1",
        "title": "Study Alpha",
        "authors": ["Smith, J", "Jones, A"],
        "year": 2020,
        "journal": "Journal A",
        "citations": 50,
        "doi": "10.1000/alpha",
        "source": "PubMed",
        "study_type": "RCT",
    },
    {
        "pmid": "2",
        "title": "Study Beta",
        "authors": "Lee, B and Park, C",
        "year": 2019,
        "journal": "Journal B",
        "citations": 100,
        "doi": "10.1000/beta",
        "source": "Semantic Scholar",
        "study_type": "meta-analysis",
    },
    {
        "pmid": "3",
        "title": "Study Gamma",
        "authors": ["Chen, D"],
        "year": 2021,
        "journal": "Journal C",
        "citations": 10,
        "doi": "10.1000/gamma",
        "source": "PubMed",
        "study_type": "RCT",
    },
]


class TestGenerateSearchSummary:
    def test_basic_summary(self):
        summary = generate_search_summary(SAMPLE_RESULTS)
        assert summary["total_results"] == 3
        assert summary["sources"]["PubMed"] == 2
        assert summary["sources"]["Semantic Scholar"] == 1
        assert summary["total_citations"] == 160
        assert summary["avg_citations"] == pytest.approx(160 / 3)

    def test_empty_results(self):
        summary = generate_search_summary([])
        assert summary["total_results"] == 0
        assert summary["total_citations"] == 0

    def test_missing_citations(self):
        results = [{"title": "No citations"}, {"citations": "bad"}]
        summary = generate_search_summary(results)
        assert summary["total_citations"] == 0

    def test_year_distribution(self):
        summary = generate_search_summary(SAMPLE_RESULTS)
        assert summary["year_distribution"][2020] == 1
        assert summary["year_distribution"][2019] == 1
        assert summary["year_distribution"][2021] == 1


class TestProcessResults:
    def test_markdown_output(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.md")
            try:
                result = process_results(
                    path, output_format="markdown", output_path=out
                )
                assert result["total_results"] == 3
                assert os.path.isfile(out)
                with open(out) as f:
                    content = f.read()
                assert "Study Alpha" in content
                assert "Study Beta" in content
            finally:
                os.unlink(path)

    def test_json_output(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(path, output_format="json", output_path=out)
                with open(out) as f:
                    data = json.load(f)
                assert len(data) == 3
                assert "_original_idx" not in data[0]
            finally:
                os.unlink(path)

    def test_bibtex_output(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.bib")
            try:
                process_results(path, output_format="bibtex", output_path=out)
                with open(out) as f:
                    content = f.read()
                assert "@article{" in content
                assert "10.1000/alpha" in content
            finally:
                os.unlink(path)

    def test_ris_output(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.ris")
            try:
                process_results(path, output_format="ris", output_path=out)
                with open(out) as f:
                    content = f.read()
                assert "TY  - JOUR" in content
                assert "DO  - 10.1000/alpha" in content
            finally:
                os.unlink(path)

    def test_unknown_format_returns_error(self):
        path = _write_results(SAMPLE_RESULTS)
        try:
            result = process_results(path, output_format="xml")
            assert "error" in result
        finally:
            os.unlink(path)

    def test_invalid_json_returns_error(self):
        path = _write_results({"not": "a list"})
        try:
            result = process_results(path)
            assert "error" in result
        finally:
            os.unlink(path)

    def test_deduplication(self):
        duped = SAMPLE_RESULTS + [
            {
                "pmid": "1",
                "title": "Study Alpha duplicate",
                "year": 2020,
                "abstract": "Extra abstract",
            }
        ]
        path = _write_results(duped)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path, output_format="json", output_path=out, deduplicate=True
                )
                assert result["total_results"] == 3
                assert "Deduplicated: 4 -> 3" in result["log"]
            finally:
                os.unlink(path)

    def test_no_deduplication(self):
        duped = SAMPLE_RESULTS + [{"pmid": "1", "title": "Dup"}]
        path = _write_results(duped)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    deduplicate=False,
                )
                assert result["total_results"] == 4
            finally:
                os.unlink(path)

    def test_year_filter(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    year_start=2020,
                )
                assert result["total_results"] == 2
            finally:
                os.unlink(path)

    def test_year_filter_end(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    year_end=2019,
                )
                assert result["total_results"] == 1
            finally:
                os.unlink(path)

    def test_study_type_filter(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                result = process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    study_types=["RCT"],
                )
                assert result["total_results"] == 2
            finally:
                os.unlink(path)

    def test_rank_by_citations(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    rank_by="citations",
                )
                with open(out) as f:
                    data = json.load(f)
                assert data[0]["title"] == "Study Beta"
                assert data[-1]["title"] == "Study Gamma"
            finally:
                os.unlink(path)

    def test_rank_by_year(self):
        path = _write_results(SAMPLE_RESULTS)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "results.json")
            try:
                process_results(
                    path,
                    output_format="json",
                    output_path=out,
                    rank_by="year",
                )
                with open(out) as f:
                    data = json.load(f)
                assert data[0]["year"] == 2021
            finally:
                os.unlink(path)


class TestDeduplicateResults:
    def test_basic_dedup(self):
        duped = [
            {"pmid": "1", "title": "A", "doi": ""},
            {"pmid": "1", "title": "A copy", "doi": "10.1000/x"},
            {"pmid": "2", "title": "B"},
        ]
        path = _write_results(duped)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "deduped.json")
            try:
                result = deduplicate_results(path, output_path=out)
                assert result["before"] == 3
                assert result["after"] == 2
                assert result["removed"] == 1
                assert result["duplicates_by_pmid"] == 1
                assert result["duplicates_by_doi"] == 0
                assert result["duplicates_by_title"] == 0
                with open(out) as f:
                    data = json.load(f)
                assert len(data) == 2
            finally:
                os.unlink(path)

    def test_author_string_split(self):
        results = [{"pmid": "1", "title": "A", "authors": "Smith, J, Jones, A"}]
        path = _write_results(results)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "deduped.json")
            try:
                deduplicate_results(path, output_path=out)
                with open(out) as f:
                    data = json.load(f)
                assert isinstance(data[0]["authors"], list)
            finally:
                os.unlink(path)

    def test_in_place_dedup(self):
        results = [{"pmid": "1", "title": "A"}]
        path = _write_results(results)
        try:
            result = deduplicate_results(path)
            assert result["output_path"] == path
            with open(path) as f:
                data = json.load(f)
            assert len(data) == 1
        finally:
            os.unlink(path)
