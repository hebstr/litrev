"""Tests for generate_bibliography: PMID→DOI resolution, resolver cascade, key dedup, mismatch detection."""

import json
import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from litrev_mcp.tools.verify import (
    generate_bibliography,
    _resolve_pmids_to_dois,
    _extract_bibtex_entries,
    _extract_refs_md,
    _set_entry_key,
)


SAMPLE_REVIEW = """# Review

Some text about the study.

```bibtex
@article{Smith_2020,
  title={Effect of X on Y},
  author={Smith, John and Jones, Alice},
  year={2020},
  journal={Journal A},
  pmid={12345678}
}
```

```bibtex
@article{Lee_2019,
  title={Drug Z outcomes},
  author={Lee, B and Park, C},
  year={2019},
  journal={Journal B},
  doi={10.1000/existing},
  pmid={87654321}
}
```

```bibtex
@article{Chen_2021,
  title={Meta-analysis of W},
  author={Chen, D},
  year={2021},
  journal={Journal C},
  pmid={11111111}
}
```
"""


class TestExtractBibtexEntries:
    def test_extracts_entries(self):
        text = "@article{k1, title={A}} and @book{k2, title={B}}"
        entries = _extract_bibtex_entries(text)
        assert len(entries) == 2
        assert entries[0].startswith("@article{k1,")
        assert entries[1].startswith("@book{k2,")

    def test_nested_braces(self):
        text = "@article{k, title={A {B} C}}"
        entries = _extract_bibtex_entries(text)
        assert len(entries) == 1
        assert "A {B} C" in entries[0]

    def test_no_entries(self):
        assert _extract_bibtex_entries("no bibtex here") == []

    def test_unbalanced_brace_skipped(self):
        text = "@article{k, title={unclosed"
        entries = _extract_bibtex_entries(text)
        assert len(entries) == 0


class TestExtractRefsMd:
    def test_extracts_doi_keyed_refs(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(SAMPLE_REVIEW)
            path = f.name
        try:
            refs = _extract_refs_md([path])
            assert "10.1000/existing" in refs
            assert refs["10.1000/existing"]["key"] == "Lee_2019"
            assert refs["10.1000/existing"]["year"] == "2019"
            assert refs["10.1000/existing"]["author"] == "Lee"
        finally:
            os.unlink(path)

    def test_entries_without_doi_skipped(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(SAMPLE_REVIEW)
            path = f.name
        try:
            refs = _extract_refs_md([path])
            assert len(refs) == 1
        finally:
            os.unlink(path)


class TestSetEntryKey:
    def test_replaces_key(self):
        entry = "@article{OldKey, title={X}}"
        result = _set_entry_key(entry, "NewKey")
        assert result == "@article{NewKey, title={X}}"

    def test_preserves_rest(self):
        entry = "@book{k,\n  title={Y},\n  year={2020}\n}"
        result = _set_entry_key(entry, "replaced")
        assert "title={Y}" in result
        assert result.startswith("@book{replaced,")


class TestResolvePmidsToDois:
    @patch("litrev_mcp.tools.verify.request_with_retry")
    def test_batch_resolution(self, mock_req):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "records": [
                {"pmid": "111", "doi": "10.1000/aaa"},
                {"pmid": "222", "doi": "10.2000/bbb"},
                {"pmid": "333", "doi": ""},
            ]
        }
        mock_req.return_value = mock_resp

        result = _resolve_pmids_to_dois(["111", "222", "333"], timeout=5)
        assert result == {"111": "10.1000/aaa", "222": "10.2000/bbb"}

    @patch("litrev_mcp.tools.verify.request_with_retry")
    def test_api_failure_returns_empty(self, mock_req):
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_req.return_value = mock_resp

        result = _resolve_pmids_to_dois(["111"], timeout=5)
        assert result == {}

    @patch("litrev_mcp.tools.verify.request_with_retry")
    def test_empty_input(self, mock_req):
        result = _resolve_pmids_to_dois([], timeout=5)
        assert result == {}
        mock_req.assert_not_called()

    @patch("litrev_mcp.tools.verify.request_with_retry")
    def test_network_error_returns_empty(self, mock_req):
        mock_req.side_effect = Exception("network error")
        result = _resolve_pmids_to_dois(["111"], timeout=5)
        assert result == {}


class TestGenerateBibliography:
    def _make_review_file(self, content):
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False)
        f.write(content)
        f.close()
        return f.name

    def _make_mock_resolver(self, doi_to_bibtex):
        def resolver(doi, timeout=10):
            if doi in doi_to_bibtex:
                return doi_to_bibtex[doi]
            raise ValueError(f"DOI not found: {doi}")

        return resolver

    @patch("litrev_mcp.tools.verify._resolve_pmids_to_dois")
    @patch("litrev_mcp.tools.verify._bibtex_from_pubmed")
    @patch("litrev_mcp.tools.verify._bibtex_from_crossref")
    @patch("litrev_mcp.tools.verify._resolve_bibtex_from_doi")
    def test_pmid_resolution_feeds_resolver_cascade(
        self, mock_doi_org, mock_crossref, mock_pubmed, mock_pmid_resolve
    ):
        mock_pmid_resolve.return_value = {"12345678": "10.9999/resolved-from-pmid"}
        mock_doi_org.return_value = (
            "@article{Smith_2020,\n"
            "  title={Effect of X on Y},\n"
            "  author={Smith, John},\n"
            "  year={2020},\n"
            "  doi={10.9999/resolved-from-pmid}\n"
            "}"
        )
        mock_crossref.side_effect = ValueError("not needed")
        mock_pubmed.side_effect = ValueError("not needed")

        review_path = self._make_review_file(SAMPLE_REVIEW)
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "refs.bib")
            try:
                result = generate_bibliography(
                    review_path, output_path=out_path, timeout=5
                )
                assert result["entries"] >= 1
                with open(out_path) as f:
                    bib_content = f.read()
                assert "10.9999/resolved-from-pmid" in bib_content
            finally:
                os.unlink(review_path)

    @patch("litrev_mcp.tools.verify._resolve_pmids_to_dois")
    @patch("litrev_mcp.tools.verify._bibtex_from_pubmed")
    @patch("litrev_mcp.tools.verify._bibtex_from_crossref")
    @patch("litrev_mcp.tools.verify._resolve_bibtex_from_doi")
    def test_existing_doi_not_duplicated(
        self, mock_doi_org, mock_crossref, mock_pubmed, mock_pmid_resolve
    ):
        mock_pmid_resolve.return_value = {}
        mock_doi_org.return_value = (
            "@article{Lee_2019,\n"
            "  title={Drug Z outcomes},\n"
            "  author={Lee, B},\n"
            "  year={2019},\n"
            "  doi={10.1000/existing}\n"
            "}"
        )
        mock_crossref.side_effect = ValueError("fallback")
        mock_pubmed.side_effect = ValueError("fallback")

        review_path = self._make_review_file(SAMPLE_REVIEW)
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "refs.bib")
            try:
                result = generate_bibliography(
                    review_path, output_path=out_path, timeout=5
                )
                with open(out_path) as f:
                    bib_content = f.read()
                assert bib_content.count("10.1000/existing") == 1
            finally:
                os.unlink(review_path)

    @patch("litrev_mcp.tools.verify._resolve_pmids_to_dois")
    @patch("litrev_mcp.tools.verify._bibtex_from_pubmed")
    @patch("litrev_mcp.tools.verify._bibtex_from_crossref")
    @patch("litrev_mcp.tools.verify._resolve_bibtex_from_doi")
    def test_all_resolvers_fail_produces_empty_bib(
        self, mock_doi_org, mock_crossref, mock_pubmed, mock_pmid_resolve
    ):
        mock_pmid_resolve.return_value = {
            "12345678": "10.9999/will-fail",
            "11111111": "10.9999/also-fails",
        }
        mock_doi_org.side_effect = ValueError("fail")
        mock_crossref.side_effect = ValueError("fail")
        mock_pubmed.side_effect = ValueError("fail")

        review_path = self._make_review_file(SAMPLE_REVIEW)
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "refs.bib")
            try:
                result = generate_bibliography(
                    review_path, output_path=out_path, timeout=5
                )
                assert result["entries"] == 0
                assert any("FAILED" in line for line in result["log"])
            finally:
                os.unlink(review_path)

    @patch("litrev_mcp.tools.verify._resolve_pmids_to_dois")
    @patch("litrev_mcp.tools.verify._bibtex_from_pubmed")
    @patch("litrev_mcp.tools.verify._bibtex_from_crossref")
    @patch("litrev_mcp.tools.verify._resolve_bibtex_from_doi")
    def test_mismatch_detection_year(
        self, mock_doi_org, mock_crossref, mock_pubmed, mock_pmid_resolve
    ):
        mock_pmid_resolve.return_value = {}
        mock_doi_org.return_value = (
            "@article{Lee_2019,\n"
            "  title={Drug Z outcomes},\n"
            "  author={Lee, B},\n"
            "  year={2018},\n"
            "  doi={10.1000/existing}\n"
            "}"
        )
        mock_crossref.side_effect = ValueError("fallback")
        mock_pubmed.side_effect = ValueError("fallback")

        review_path = self._make_review_file(SAMPLE_REVIEW)
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "refs.bib")
            try:
                result = generate_bibliography(
                    review_path, output_path=out_path, timeout=5
                )
                assert any("MISMATCH year" in e for e in result["errors"])
            finally:
                os.unlink(review_path)

    @patch("litrev_mcp.tools.verify._resolve_pmids_to_dois")
    @patch("litrev_mcp.tools.verify._bibtex_from_pubmed")
    @patch("litrev_mcp.tools.verify._bibtex_from_crossref")
    @patch("litrev_mcp.tools.verify._resolve_bibtex_from_doi")
    def test_key_preserved_from_markdown(
        self, mock_doi_org, mock_crossref, mock_pubmed, mock_pmid_resolve
    ):
        mock_pmid_resolve.return_value = {}
        mock_doi_org.return_value = (
            "@article{wrong_key,\n"
            "  title={Drug Z outcomes},\n"
            "  author={Lee, B},\n"
            "  year={2019},\n"
            "  doi={10.1000/existing}\n"
            "}"
        )
        mock_crossref.side_effect = ValueError("fallback")
        mock_pubmed.side_effect = ValueError("fallback")

        review_path = self._make_review_file(SAMPLE_REVIEW)
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "refs.bib")
            try:
                generate_bibliography(review_path, output_path=out_path, timeout=5)
                with open(out_path) as f:
                    bib = f.read()
                assert "@article{Lee_2019," in bib
                assert "wrong_key" not in bib
            finally:
                os.unlink(review_path)
