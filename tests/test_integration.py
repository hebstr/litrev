#!/usr/bin/env python3
"""Integration tests with mocked HTTP responses."""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from generate_bib import resolve_bibtex, bibtex_from_crossref, bibtex_from_pubmed, generate_bib
from verify_citations import CitationVerifier


def _mock_response(status_code=200, text="", json_data=None, headers=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    resp.headers = headers or {}
    if json_data is not None:
        resp.json.return_value = json_data
    resp.raise_for_status.side_effect = None
    return resp


class TestResolveBibtex(unittest.TestCase):
    @patch("generate_bib._request_with_retry")
    def test_valid_bibtex_response(self, mock_req):
        bib = '@article{Smith_2023, title={Test}, author={Smith, J.}, year={2023}}'
        mock_req.return_value = _mock_response(text=bib)
        result = resolve_bibtex("10.1234/test")
        assert result == bib

    @patch("generate_bib._request_with_retry")
    def test_non_bibtex_response_raises(self, mock_req):
        mock_req.return_value = _mock_response(text="<html>Not Found</html>")
        with self.assertRaises(ValueError):
            resolve_bibtex("10.1234/test")


class TestBibtexFromCrossref(unittest.TestCase):
    @patch("generate_bib._request_with_retry")
    def test_journal_article(self, mock_req):
        mock_req.return_value = _mock_response(json_data={
            "message": {
                "type": "journal-article",
                "title": ["A Great Study"],
                "author": [{"family": "Doe", "given": "Jane"}],
                "container-title": ["Nature"],
                "published": {"date-parts": [[2024]]},
                "volume": "42",
                "issue": "3",
                "page": "100-110",
            }
        })
        result = bibtex_from_crossref("10.1234/test")
        assert "@article{Doe_2024," in result
        assert "A Great Study" in result
        assert "Nature" in result
        assert "doi={10.1234/test}" in result

    @patch("generate_bib._request_with_retry")
    def test_book_chapter(self, mock_req):
        mock_req.return_value = _mock_response(json_data={
            "message": {
                "type": "book-chapter",
                "title": ["Chapter One"],
                "author": [{"family": "Lee", "given": "A."}],
                "container-title": ["Big Book"],
                "published-print": {"date-parts": [[2020]]},
                "volume": "",
                "issue": "",
                "page": "1-20",
            }
        })
        result = bibtex_from_crossref("10.5678/ch1")
        assert "@incollection{Lee_2020," in result
        assert "booktitle={Big Book}" in result


class TestBibtexFromPubmed(unittest.TestCase):
    @patch("generate_bib._request_with_retry")
    @patch("generate_bib.time.sleep")
    def test_pubmed_article(self, mock_sleep, mock_req):
        mock_req.side_effect = [
            _mock_response(json_data={
                "esearchresult": {"idlist": ["12345"]}
            }),
            _mock_response(json_data={
                "result": {
                    "12345": {
                        "title": "PubMed Study",
                        "authors": [{"name": "Kim S", "authtype": "Author"}],
                        "pubdate": "2022 Jan",
                        "fulljournalname": "The Lancet",
                        "volume": "10",
                        "issue": "2",
                        "pages": "50-60",
                        "pubtype": ["Journal Article"],
                    }
                }
            }),
        ]
        result = bibtex_from_pubmed("10.9999/pm")
        assert "@article{Kim_2022," in result
        assert "PubMed Study" in result
        assert "doi={10.9999/pm}" in result

    @patch("generate_bib._request_with_retry")
    def test_pubmed_not_found(self, mock_req):
        mock_req.return_value = _mock_response(json_data={
            "esearchresult": {"idlist": []}
        })
        with self.assertRaises(ValueError):
            bibtex_from_pubmed("10.0000/missing")


class TestVerifyCitations(unittest.TestCase):
    @patch("verify_citations._request_with_retry")
    def test_verify_doi_valid(self, mock_req):
        mock_req.side_effect = [
            _mock_response(status_code=200, json_data={}),
            _mock_response(status_code=200, json_data={
                "message": {
                    "title": ["Valid Paper"],
                    "author": [{"family": "Brown", "given": "A."}],
                    "published": {"date-parts": [[2023]]},
                    "container-title": ["Science"],
                    "volume": "1",
                    "page": "1-5",
                }
            }),
        ]
        verifier = CitationVerifier()
        valid, meta = verifier.verify_doi("10.1234/valid")
        assert valid
        assert meta["title"] == "Valid Paper"

    @patch("verify_citations._request_with_retry")
    def test_verify_doi_not_found(self, mock_req):
        mock_req.return_value = _mock_response(status_code=404)
        verifier = CitationVerifier()
        valid, meta = verifier.verify_doi("10.0000/fake")
        assert not valid

    @patch("verify_citations._request_with_retry")
    def test_check_retraction_positive(self, mock_req):
        mock_req.return_value = _mock_response(json_data={
            "esearchresult": {"count": "1"}
        })
        verifier = CitationVerifier()
        assert verifier.check_retraction("99999") is True

    @patch("verify_citations._request_with_retry")
    def test_check_retraction_negative(self, mock_req):
        mock_req.return_value = _mock_response(json_data={
            "esearchresult": {"count": "0"}
        })
        verifier = CitationVerifier()
        assert verifier.check_retraction("11111") is False


class TestGenerateBibEndToEnd(unittest.TestCase):
    @patch("generate_bib._request_with_retry")
    @patch("generate_bib.time.sleep")
    def test_generates_bib_from_markdown(self, mock_sleep, mock_req):
        bib_entry = '@article{Smith_2024, title={Test}, author={Smith, J.}, year={2024}, doi={10.1234/abc}}'
        mock_req.return_value = _mock_response(text=bib_entry)

        md_content = "# Review\n\nSee 10.1234/abc for details.\n\n```bibtex\n@article{Smith_2024,\n  author={Smith, J.},\n  year={2024},\n  doi={10.1234/abc}\n}\n```\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = os.path.join(tmpdir, "review.md")
            bib_path = os.path.join(tmpdir, "refs.bib")
            with open(md_path, "w") as f:
                f.write(md_content)

            result = generate_bib([md_path], bib_path)

            assert os.path.isfile(bib_path)
            with open(bib_path) as f:
                content = f.read()
            assert "Smith_2024" in content
            assert "10.1234/abc" in content


if __name__ == "__main__":
    unittest.main()
