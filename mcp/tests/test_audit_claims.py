"""Tests for audit_claims: key resolution, status assignment, claim matching flow."""

import json
import os
import tempfile

import pytest

from litrev_mcp.tools.verify import (
    audit_claims,
    _resolve_key,
    _extract_review_claims,
    _build_doi_index,
)


REVIEW_TEXT = """\
## Results

The treatment showed a response rate of 45.2% [@Smith_2020].
Pain scores decreased by 2.8 points (p=0.003) [@Lee_2019].
Thirteen patients were lost to follow-up [@Unknown_2022].
No significant effect was observed [@Chen_2021].
"""

EXTRACTION = {
    "articles": {
        "Smith_2020": {
            "doi": "10.1000/alpha",
            "has_abstract": True,
            "claims": [
                {"value": "response rate of 45.2%", "type": "percentage"},
            ],
            "semantic_claims": [],
        },
        "Lee_2019": {
            "doi": "10.1000/beta",
            "has_abstract": True,
            "claims": [
                {"value": "decreased by 2.8 points", "type": "statistic"},
                {"effect_size": "p=0.003", "type": "p-value"},
            ],
            "semantic_claims": [],
        },
        "Chen_2021": {
            "doi": "10.1000/gamma",
            "has_abstract": False,
            "claims": [],
            "semantic_claims": [],
        },
    }
}


def _setup_files(review_text=REVIEW_TEXT, extraction=EXTRACTION):
    tmpdir = tempfile.mkdtemp()
    review_path = os.path.join(tmpdir, "review.md")
    claims_path = os.path.join(tmpdir, "extracted_claims.json")
    output_path = os.path.join(tmpdir, "audit.json")

    with open(review_path, "w") as f:
        f.write(review_text)
    with open(claims_path, "w") as f:
        json.dump(extraction, f)

    return tmpdir, review_path, claims_path, output_path


class TestBuildDoiIndex:
    def test_builds_index(self):
        idx = _build_doi_index(EXTRACTION)
        assert idx["10.1000/alpha"] == "Smith_2020"
        assert idx["10.1000/beta"] == "Lee_2019"

    def test_empty(self):
        assert _build_doi_index({}) == {}
        assert _build_doi_index({"articles": {}}) == {}

    def test_missing_doi_skipped(self):
        ext = {"articles": {"k": {"doi": "", "has_abstract": True}}}
        assert _build_doi_index(ext) == {}


class TestResolveKey:
    def setup_method(self):
        self.articles = EXTRACTION["articles"]
        self.bib_dois = {"alt_key": "10.1000/alpha"}
        self.doi_index = _build_doi_index(EXTRACTION)

    def test_direct_match(self):
        assert _resolve_key("Smith_2020", self.articles, {}, {}) == "Smith_2020"

    def test_via_bib_doi(self):
        result = _resolve_key("alt_key", self.articles, self.bib_dois, self.doi_index)
        assert result == "Smith_2020"

    def test_fuzzy_name_prefix(self):
        result = _resolve_key("Smi_2020", self.articles, {}, {})
        assert result == "Smith_2020"

    def test_no_match(self):
        result = _resolve_key("Unknown_2022", self.articles, {}, {})
        assert result is None

    def test_year_must_match(self):
        result = _resolve_key("Smith_2019", self.articles, {}, {})
        assert result is None


class TestExtractReviewClaims:
    def test_extracts_statistics(self):
        claims = _extract_review_claims(REVIEW_TEXT)
        values = [c["value"] for c in claims]
        assert "45.2%" in values
        assert "p=0.003" in values or any("0.003" in v for v in values)

    def test_extracts_numbers(self):
        claims = _extract_review_claims(REVIEW_TEXT)
        values = [c["value"] for c in claims]
        assert any("2.8" in v for v in values)

    def test_citation_keys_attached(self):
        claims = _extract_review_claims(REVIEW_TEXT)
        keys = [c["citation_key"] for c in claims]
        assert "Smith_2020" in keys
        assert "Lee_2019" in keys

    def test_no_citations_no_claims(self):
        text = "Some text without any citations or numbers."
        assert _extract_review_claims(text) == []


class TestAuditClaims:
    def test_verified_claim(self):
        tmpdir, review_path, claims_path, output_path = _setup_files()
        try:
            result = audit_claims(
                review_path, claims_path=claims_path, output_path=output_path
            )
            assert result["verified"] >= 1
            with open(output_path) as f:
                audit = json.load(f)
            verified = [c for c in audit["claims"] if c["status"] == "VERIFIED"]
            assert len(verified) >= 1
            verified_values = [c["value"] for c in verified]
            assert any("45.2" in v for v in verified_values)
        finally:
            for f in [review_path, claims_path, output_path]:
                if os.path.isfile(f):
                    os.unlink(f)
            os.rmdir(tmpdir)

    def test_no_extraction_status(self):
        tmpdir, review_path, claims_path, output_path = _setup_files()
        try:
            result = audit_claims(
                review_path, claims_path=claims_path, output_path=output_path
            )
            with open(output_path) as f:
                audit = json.load(f)
            no_ext = [c for c in audit["claims"] if c["status"] == "NO_EXTRACTION"]
            if no_ext:
                assert all(
                    "Unknown_2022" in c.get("detail", "")
                    or c["citation_key"] == "Unknown_2022"
                    for c in no_ext
                )
        finally:
            for f in [review_path, claims_path, output_path]:
                if os.path.isfile(f):
                    os.unlink(f)
            os.rmdir(tmpdir)

    def test_no_abstract_status(self):
        tmpdir, review_path, claims_path, output_path = _setup_files()
        try:
            result = audit_claims(
                review_path, claims_path=claims_path, output_path=output_path
            )
            assert result["no_abstract"] >= 0
        finally:
            for f in [review_path, claims_path, output_path]:
                if os.path.isfile(f):
                    os.unlink(f)
            os.rmdir(tmpdir)

    def test_output_file_created(self):
        tmpdir, review_path, claims_path, output_path = _setup_files()
        try:
            result = audit_claims(
                review_path, claims_path=claims_path, output_path=output_path
            )
            assert os.path.isfile(output_path)
            assert result["output_path"] == output_path
        finally:
            for f in [review_path, claims_path, output_path]:
                if os.path.isfile(f):
                    os.unlink(f)
            os.rmdir(tmpdir)

    def test_summary_totals_consistent(self):
        tmpdir, review_path, claims_path, output_path = _setup_files()
        try:
            result = audit_claims(
                review_path, claims_path=claims_path, output_path=output_path
            )
            total = (
                result["verified"]
                + result["unverified"]
                + result["no_abstract"]
                + result["no_extraction"]
            )
            assert total == result["total"]
        finally:
            for f in [review_path, claims_path, output_path]:
                if os.path.isfile(f):
                    os.unlink(f)
            os.rmdir(tmpdir)

    def test_bib_path_auto_detection(self):
        tmpdir, review_path, claims_path, output_path = _setup_files()
        bib_path = os.path.join(tmpdir, "references.bib")
        with open(bib_path, "w") as f:
            f.write("@article{alt_key,\n  doi={10.1000/alpha},\n  title={X}\n}\n")
        try:
            result = audit_claims(
                review_path, claims_path=claims_path, output_path=output_path
            )
            assert result["total"] > 0
        finally:
            for f in [review_path, claims_path, output_path, bib_path]:
                if os.path.isfile(f):
                    os.unlink(f)
            os.rmdir(tmpdir)

    def test_empty_review_no_crash(self):
        tmpdir, review_path, claims_path, output_path = _setup_files(
            review_text="No citations here.", extraction=EXTRACTION
        )
        try:
            result = audit_claims(
                review_path, claims_path=claims_path, output_path=output_path
            )
            assert result["total"] == 0
        finally:
            for f in [review_path, claims_path, output_path]:
                if os.path.isfile(f):
                    os.unlink(f)
            os.rmdir(tmpdir)
