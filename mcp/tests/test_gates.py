"""Tests for validate_gate MCP tool."""

import json
import os

import pytest

from litrev_mcp.tools.gates import validate_gate


@pytest.fixture()
def review_dir(tmp_path):
    return tmp_path


def _write(directory, name, content=""):
    path = os.path.join(directory, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


class TestInvalidInput:
    def test_unknown_gate(self, review_dir):
        result = validate_gate("99", str(review_dir))
        assert result["status"] == "FAIL"
        assert "unknown gate" in result["checks"][0]["detail"]

    def test_missing_directory(self):
        result = validate_gate("1", "/nonexistent/path")
        assert result["status"] == "FAIL"
        assert "directory not found" in result["checks"][0]["detail"]


class TestGate1:
    def test_missing_protocol(self, review_dir):
        result = validate_gate("1", str(review_dir))
        assert result["status"] == "FAIL"

    def test_pass(self, review_dir):
        _write(
            review_dir,
            "protocol.md",
            """# Protocol
## Research Question
What is X?
## Framework: PEO
| P | E | O |
## Inclusion Criteria
Adults only
""",
        )
        result = validate_gate("1", str(review_dir))
        assert result["status"] == "PASS"
        assert all(c["passed"] for c in result["checks"])

    def test_missing_question(self, review_dir):
        _write(review_dir, "protocol.md", "# Protocol\n## Framework\n## Criteria\n")
        result = validate_gate("1", str(review_dir))
        assert result["status"] == "FAIL"
        names = {c["name"] for c in result["checks"] if not c["passed"]}
        assert "contains question" in names


class TestGate2:
    def test_missing_files(self, review_dir):
        result = validate_gate("2", str(review_dir))
        assert result["status"] == "FAIL"

    def test_pass(self, review_dir):
        _write(review_dir, "combined_results.json", json.dumps([{"title": "A"}]))
        _write(review_dir, "search_results.md", "# Results")
        _write(review_dir, "search_log.md", "# Log")
        result = validate_gate("2", str(review_dir))
        assert result["status"] == "PASS"

    def test_empty_results(self, review_dir):
        _write(review_dir, "combined_results.json", json.dumps([]))
        _write(review_dir, "search_results.md", "")
        _write(review_dir, "search_log.md", "")
        result = validate_gate("2", str(review_dir))
        assert result["status"] == "FAIL"
        names = {c["name"] for c in result["checks"] if not c["passed"]}
        assert ">= 1 result" in names


class TestGate3a:
    def test_pass(self, review_dir):
        _write(review_dir, "screening_log.md", "### Retained (5)\n0 1 2 3 4")
        _write(review_dir, "included_indices.json", json.dumps([0, 1, 2, 3, 4]))
        result = validate_gate("3a", str(review_dir))
        assert result["status"] == "PASS"

    def test_multi_stage_uses_last_retained(self, review_dir):
        log = (
            "## Title screening\n"
            "### Retained (425)\n"
            "Kept 425 after title screen\n\n"
            "## Full-text screening\n"
            "### Retained (358)\n"
            "Kept 358 after full-text screen\n"
        )
        indices = list(range(358))
        _write(review_dir, "screening_log.md", log)
        _write(review_dir, "included_indices.json", json.dumps(indices))
        result = validate_gate("3a", str(review_dir))
        assert result["status"] == "PASS"

    def test_inconsistent_counts(self, review_dir):
        _write(review_dir, "screening_log.md", "### Retained (10)\n0 1 2")
        _write(review_dir, "included_indices.json", json.dumps([0, 1, 2]))
        result = validate_gate("3a", str(review_dir))
        assert result["status"] == "FAIL"
        failed = [c for c in result["checks"] if not c["passed"]]
        assert any("PRISMA" in c["name"] for c in failed)


class TestGate3b:
    def test_no_snowball_section(self, review_dir):
        _write(review_dir, "screening_log.md", "# Screening\nNo relevant section here")
        result = validate_gate("3b", str(review_dir))
        assert result["status"] == "FAIL"
        assert "N/A if intentionally skipped" in result["checks"][0]["detail"]

    def test_pass_with_complete(self, review_dir):
        _write(review_dir, "screening_log.md", "## Snowballing\nStatus: COMPLETE\n")
        result = validate_gate("3b", str(review_dir))
        assert result["status"] == "PASS"


class TestGate4:
    def test_missing_file(self, review_dir):
        result = validate_gate("4", str(review_dir))
        assert result["status"] == "FAIL"

    def test_pass(self, review_dir):
        data = {
            "articles": {
                "Smith_2020": {
                    "semantic_claims": [{"claim": "X increases Y"}],
                }
            }
        }
        _write(review_dir, "extracted_claims.json", json.dumps(data))
        result = validate_gate("4", str(review_dir))
        assert result["status"] == "PASS"

    def test_no_semantic_claims(self, review_dir):
        data = {"articles": {"Smith_2020": {"semantic_claims": []}}}
        _write(review_dir, "extracted_claims.json", json.dumps(data))
        result = validate_gate("4", str(review_dir))
        assert result["status"] == "FAIL"


class TestGate5:
    def test_missing_review(self, review_dir):
        result = validate_gate("5", str(review_dir))
        assert result["status"] == "FAIL"

    def test_pass(self, review_dir):
        content = """---
title: "Test Review"
---
# Abstract
Text
# Methods
Text
# Results
Text [@Smith_2020]
# Discussion
Text
"""
        _write(review_dir, "test_review.md", content)
        result = validate_gate("5", str(review_dir))
        assert result["status"] == "PASS"


class TestGate6:
    def test_missing_files(self, review_dir):
        result = validate_gate("6", str(review_dir))
        assert result["status"] == "FAIL"

    def test_pass(self, review_dir):
        _write(review_dir, "references.bib", "@article{Smith_2020, title={X}}")
        _write(review_dir, "claims_audit.json", json.dumps({"summary": {}}))
        _write(review_dir, "test_citation_report.json", json.dumps({}))
        result = validate_gate("6", str(review_dir))
        assert result["status"] == "PASS"


class TestGate7:
    def test_pass_via_pipeline_log(self, review_dir):
        _write(
            review_dir, "pipeline_log.md", "| G7 Quality Check | PASSED | all items |"
        )
        result = validate_gate("7", str(review_dir))
        assert result["status"] == "PASS"

    def test_fail_via_pipeline_log(self, review_dir):
        _write(review_dir, "pipeline_log.md", "| G7 Quality Check | FAILED | item 3 |")
        result = validate_gate("7", str(review_dir))
        assert result["status"] == "FAIL"


class TestGate8:
    def test_missing_files(self, review_dir):
        result = validate_gate("8", str(review_dir))
        assert result["status"] == "FAIL"

    def test_pass(self, review_dir):
        _write(
            review_dir, "audit_fidelity.md", "# Fidelity Audit\nNo critical findings"
        )
        _write(
            review_dir,
            "audit_methodology.md",
            "# Methodology Audit\nNo critical findings",
        )
        _write(review_dir, "pipeline_log.md", "| G8 Double Audit | PASSED | all done |")
        result = validate_gate("8", str(review_dir))
        assert result["status"] == "PASS"

    def test_unresolved_critical(self, review_dir):
        _write(
            review_dir,
            "audit_fidelity.md",
            "### [F-01] Bad DOIs -- critical\nNot fixed",
        )
        _write(review_dir, "audit_methodology.md", "# OK")
        _write(review_dir, "pipeline_log.md", "| G8 Double Audit | PASSED |")
        result = validate_gate("8", str(review_dir))
        assert result["status"] == "FAIL"


class TestGate9:
    def test_missing_file(self, review_dir):
        result = validate_gate("9", str(review_dir))
        assert result["status"] == "FAIL"

    def test_pass(self, review_dir):
        content = """# Run Report
## Funnel Metrics
| Stage | N |
## Gate Log
| Gate | Status |
## Timing
| Phase | Duration |
"""
        _write(review_dir, "pipeline_log.md", content)
        result = validate_gate("9", str(review_dir))
        assert result["status"] == "PASS"
