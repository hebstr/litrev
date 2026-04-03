"""MCP tool: mechanical gate validation for literature review phases."""

import glob as _glob
import json
import os
import re
from collections.abc import Callable


def _check(name: str, passed: bool, detail: str) -> dict:
    return {"name": name, "passed": passed, "detail": detail}


def _file_exists(path: str) -> bool:
    return os.path.isfile(path)


def _read_text(path: str) -> str | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return None


def _load_json(path: str) -> tuple[object | None, str | None]:
    text = _read_text(path)
    if text is None:
        return None, f"cannot read {os.path.basename(path)}"
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"


def _find_review_md(review_dir: str) -> str | None:
    candidates = _glob.glob(os.path.join(review_dir, "*_review.md"))
    return candidates[0] if candidates else None


def _gate_1(d: str) -> list[dict]:
    checks: list[dict] = []
    path = os.path.join(d, "protocol.md")
    if not _file_exists(path):
        checks.append(_check("protocol.md exists", False, "file not found"))
        return checks
    checks.append(_check("protocol.md exists", True, "ok"))

    text = _read_text(path) or ""
    has_question = bool(re.search(r"(?i)##?\s*(research\s+)?question", text))
    checks.append(
        _check(
            "contains question",
            has_question,
            "section heading found" if has_question else "no question heading found",
        )
    )

    has_framework = bool(re.search(r"(?i)##?\s*framework", text))
    checks.append(
        _check(
            "contains framework",
            has_framework,
            "section heading found" if has_framework else "no framework heading found",
        )
    )

    has_criteria = bool(re.search(r"(?i)(inclusion|exclusion|eligib|criteria)", text))
    checks.append(
        _check(
            "contains criteria",
            has_criteria,
            "criteria keywords found" if has_criteria else "no criteria keywords found",
        )
    )
    return checks


def _gate_2(d: str) -> list[dict]:
    checks: list[dict] = []
    for fname in ("combined_results.json", "search_results.md", "search_log.md"):
        path = os.path.join(d, fname)
        checks.append(
            _check(
                f"{fname} exists",
                _file_exists(path),
                "ok" if _file_exists(path) else "file not found",
            )
        )

    json_path = os.path.join(d, "combined_results.json")
    data, err = _load_json(json_path)
    if err:
        checks.append(_check("JSON parseable", False, err))
    else:
        checks.append(_check("JSON parseable", True, "ok"))
        count = len(data) if isinstance(data, list) else 0
        checks.append(_check(">= 1 result", count >= 1, f"{count} results"))
    return checks


def _gate_3a(d: str) -> list[dict]:
    checks: list[dict] = []

    sl_path = os.path.join(d, "screening_log.md")
    checks.append(
        _check(
            "screening_log.md exists",
            _file_exists(sl_path),
            "ok" if _file_exists(sl_path) else "file not found",
        )
    )

    ii_path = os.path.join(d, "included_indices.json")
    checks.append(
        _check(
            "included_indices.json exists",
            _file_exists(ii_path),
            "ok" if _file_exists(ii_path) else "file not found",
        )
    )

    data, err = _load_json(ii_path)
    if err:
        checks.append(_check("JSON parseable", False, err))
    else:
        checks.append(_check("JSON parseable", True, "ok"))
        if isinstance(data, list):
            n_indices = len(data)
        else:
            n_indices = 0
            checks.append(
                _check("indices is a list", False, f"got {type(data).__name__}")
            )
            return checks

    sl_text = _read_text(sl_path) or ""
    snowball_pos = re.search(r"(?i)^##\s*citation\s*snowball", sl_text, re.MULTILINE)
    search_region = sl_text[: snowball_pos.start()] if snowball_pos else sl_text
    retained_matches = re.findall(
        r"(?i)###?\s*retained\s*\((\d[\d,]*)\)", search_region
    )
    if retained_matches:
        retained_str = retained_matches[-1].replace(",", "")
        n_retained = int(retained_str)
        consistent = n_indices == n_retained
        checks.append(
            _check(
                "PRISMA counts consistent",
                consistent,
                f"included_indices: {n_indices}, screening_log retained: {n_retained}",
            )
        )
    else:
        checks.append(
            _check(
                "PRISMA counts consistent",
                True,
                f"no retained count in screening_log to compare; {n_indices} indices",
            )
        )
    return checks


def _gate_3b(d: str) -> list[dict]:
    checks: list[dict] = []
    sl_path = os.path.join(d, "screening_log.md")
    text = _read_text(sl_path) or ""

    has_snowball = bool(re.search(r"(?i)(snowball|citation.chain)", text))
    if not has_snowball:
        checks.append(
            _check(
                "snowballing section present",
                False,
                "no snowballing/citation-chaining section found (gate N/A if intentionally skipped)",
            )
        )
        return checks

    checks.append(_check("snowballing section present", True, "section found"))
    has_complete = bool(re.search(r"(?i)status\s*:\s*complete", text))
    checks.append(
        _check(
            "snowballing Status: COMPLETE",
            has_complete,
            "status complete" if has_complete else "Status: COMPLETE not found",
        )
    )
    return checks


def _gate_4(d: str) -> list[dict]:
    checks: list[dict] = []
    path = os.path.join(d, "extracted_claims.json")
    if not _file_exists(path):
        checks.append(_check("extracted_claims.json exists", False, "file not found"))
        return checks
    checks.append(_check("extracted_claims.json exists", True, "ok"))

    data, err = _load_json(path)
    if err:
        checks.append(_check("JSON parseable", False, err))
        return checks
    checks.append(_check("JSON parseable", True, "ok"))

    articles = {}
    if isinstance(data, dict):
        articles = data.get("articles", data)

    n_with_semantic = 0
    for _key, article in articles.items():
        if isinstance(article, dict):
            sc = article.get("semantic_claims", [])
            if sc:
                n_with_semantic += 1

    has_any = n_with_semantic >= 1
    checks.append(
        _check(
            ">= 1 article with semantic_claims",
            has_any,
            f"{n_with_semantic} articles with non-empty semantic_claims",
        )
    )
    return checks


def _gate_5(d: str) -> list[dict]:
    checks: list[dict] = []
    review_path = _find_review_md(d)
    if not review_path:
        checks.append(_check("*_review.md exists", False, "no *_review.md found"))
        return checks
    checks.append(_check("*_review.md exists", True, os.path.basename(review_path)))

    text = _read_text(review_path) or ""

    has_yaml = text.startswith("---")
    checks.append(
        _check(
            "YAML header present",
            has_yaml,
            "starts with ---" if has_yaml else "no YAML front matter",
        )
    )

    required_sections = [
        "R.sum.",
        "M.thod",
        "R.sultat",
        "Discussion",
        "Conclusion",
        "Abstract",
        "Method",
        "Result",
        "Introduction",
    ]
    found_sections = [
        s for s in required_sections if re.search(rf"(?i)#{{1,3}}\s*.*{s}", text)
    ]
    has_sections = len(found_sections) >= 3
    checks.append(
        _check(
            "required sections present",
            has_sections,
            f"found: {', '.join(found_sections)}"
            if found_sections
            else "no required sections found",
        )
    )

    citation_count = len(re.findall(r"\[@[\w]+", text))
    has_citations = citation_count >= 1
    checks.append(
        _check(">= 1 [@citation]", has_citations, f"{citation_count} citations found")
    )
    return checks


def _gate_6(d: str) -> list[dict]:
    checks: list[dict] = []

    bib_path = os.path.join(d, "references.bib")
    checks.append(
        _check(
            "references.bib exists",
            _file_exists(bib_path),
            "ok" if _file_exists(bib_path) else "file not found",
        )
    )

    ca_path = os.path.join(d, "claims_audit.json")
    checks.append(
        _check(
            "claims_audit.json exists",
            _file_exists(ca_path),
            "ok" if _file_exists(ca_path) else "file not found",
        )
    )

    cr_files = _glob.glob(os.path.join(d, "*_citation_report.json"))
    has_cr = len(cr_files) >= 1
    checks.append(
        _check(
            "*_citation_report.json exists",
            has_cr,
            f"{len(cr_files)} file(s)" if has_cr else "no citation report found",
        )
    )

    if _file_exists(bib_path):
        bib_text = _read_text(bib_path) or ""
        entry_count = len(re.findall(r"@\w+\{", bib_text))
        parseable = entry_count >= 1
        checks.append(
            _check(
                "BibTeX parseable",
                parseable,
                f"{entry_count} entries" if parseable else "no BibTeX entries found",
            )
        )
    return checks


def _gate_7(d: str) -> list[dict]:
    checks: list[dict] = []
    pl_path = os.path.join(d, "pipeline_log.md")
    text = _read_text(pl_path) or ""

    g7_match = re.search(r"(?i)G7.*?Quality.*?\|\s*(PASSED|FAILED|N/A)", text)
    if g7_match:
        status = g7_match.group(1).upper()
        passed = status in ("PASSED", "N/A")
        checks.append(_check("G7 in pipeline_log", passed, f"status: {status}"))
    else:
        review_path = _find_review_md(d)
        if review_path:
            review_text = _read_text(review_path) or ""
            pass_count = len(re.findall(r"\[(?:PASS|x)\]", review_text, re.IGNORECASE))
            fail_count = len(re.findall(r"\[FAIL\]", review_text, re.IGNORECASE))
            unresolvable = len(re.findall(r"(?i)UNRESOLVABLE", review_text))
            all_ok = fail_count == 0 or (fail_count > 0 and unresolvable >= fail_count)
            checks.append(
                _check(
                    "checklist items",
                    all_ok,
                    f"{pass_count} PASS, {fail_count} FAIL, {unresolvable} UNRESOLVABLE",
                )
            )
        else:
            checks.append(
                _check(
                    "checklist items",
                    False,
                    "no pipeline_log G7 entry and no review file found",
                )
            )
    return checks


def _gate_8(d: str) -> list[dict]:
    checks: list[dict] = []

    af_path = os.path.join(d, "audit_fidelity.md")
    checks.append(
        _check(
            "audit_fidelity.md exists",
            _file_exists(af_path),
            "ok" if _file_exists(af_path) else "file not found",
        )
    )

    am_path = os.path.join(d, "audit_methodology.md")
    checks.append(
        _check(
            "audit_methodology.md exists",
            _file_exists(am_path),
            "ok" if _file_exists(am_path) else "file not found",
        )
    )

    pl_path = os.path.join(d, "pipeline_log.md")
    pl_text = _read_text(pl_path) or ""
    g8_match = re.search(r"(?i)G8.*?Double\s+Audit.*?\|\s*(PASSED|FAILED|N/A)", pl_text)
    if g8_match:
        status = g8_match.group(1).upper()
        passed = status in ("PASSED", "N/A")
        checks.append(_check("walkthroughs completed", passed, f"G8 status: {status}"))
    else:
        has_walkthrough = bool(
            re.search(r"(?i)walkthrough|corrections applied", pl_text)
        )
        checks.append(
            _check(
                "walkthroughs completed",
                has_walkthrough,
                "walkthrough section found"
                if has_walkthrough
                else "no walkthrough evidence in pipeline_log",
            )
        )

    for label, path in [
        ("audit_fidelity.md", af_path),
        ("audit_methodology.md", am_path),
    ]:
        text = _read_text(path) or ""
        criticals = re.findall(r"(?i)--\s*critical", text)
        n_critical = len(criticals)
        resolved_markers = len(re.findall(r"(?i)\b(ACCEPTED|RESOLVED)\b", text))
        if n_critical == 0:
            checks.append(
                _check(f"{label}: 0 CRITICAL unresolved", True, "no critical findings")
            )
        else:
            all_resolved = resolved_markers >= n_critical
            checks.append(
                _check(
                    f"{label}: 0 CRITICAL unresolved",
                    all_resolved,
                    f"{n_critical} critical, {resolved_markers} resolved markers",
                )
            )
    return checks


def _gate_9(d: str) -> list[dict]:
    checks: list[dict] = []
    path = os.path.join(d, "pipeline_log.md")
    if not _file_exists(path):
        checks.append(_check("pipeline_log.md exists", False, "file not found"))
        return checks
    checks.append(_check("pipeline_log.md exists", True, "ok"))

    text = _read_text(path) or ""

    has_funnel = bool(re.search(r"(?i)funnel\s+metrics", text))
    checks.append(
        _check(
            "contains Funnel Metrics",
            has_funnel,
            "section found" if has_funnel else "section not found",
        )
    )

    has_gate_log = bool(re.search(r"(?i)gate\s+log", text))
    checks.append(
        _check(
            "contains Gate Log",
            has_gate_log,
            "section found" if has_gate_log else "section not found",
        )
    )

    has_notes = bool(
        re.search(
            r"(?i)(run.specific\s+notes|observations|timing|output\s+files)", text
        )
    )
    checks.append(
        _check(
            "contains Run-Specific Notes",
            has_notes,
            "section found" if has_notes else "section not found",
        )
    )
    return checks


_GATE_DISPATCH: dict[str, Callable] = {
    "1": _gate_1,
    "2": _gate_2,
    "3a": _gate_3a,
    "3b": _gate_3b,
    "4": _gate_4,
    "5": _gate_5,
    "6": _gate_6,
    "7": _gate_7,
    "8": _gate_8,
    "9": _gate_9,
}

VALID_GATES = sorted(_GATE_DISPATCH.keys(), key=lambda g: (g.rstrip("ab"), g))


def validate_gate(gate: str, review_dir: str) -> dict:
    gate = gate.strip().lower()
    if gate not in _GATE_DISPATCH:
        return {
            "gate": gate,
            "status": "FAIL",
            "checks": [
                _check(
                    "valid gate",
                    False,
                    f"unknown gate '{gate}'; valid: {', '.join(VALID_GATES)}",
                )
            ],
        }

    review_dir = os.path.expanduser(review_dir)
    if not os.path.isdir(review_dir):
        return {
            "gate": gate,
            "status": "FAIL",
            "checks": [
                _check("review_dir exists", False, f"directory not found: {review_dir}")
            ],
        }

    checks = _GATE_DISPATCH[gate](review_dir)
    status = "PASS" if all(c["passed"] for c in checks) else "FAIL"
    return {"gate": gate, "status": status, "checks": checks}
