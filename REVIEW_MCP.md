# Review Walkthrough Report — litrev-mcp

| | |
|---|---|
| **Date** | 2026-04-01 |
| **Target** | `~/.claude/skills/litrev-mcp` |
| **Reviewer** | mcp-adversary |
| **Flags** | `--adversarial` |
| **Deployment context** | personal / local MCP server (no CI/CD, no production indicators) |
| **Calibration** | `feedback_review_severity.md` — 7 suppressed patterns from 2026-03-30 audit |

## Findings summary

| # | ID | Finding | Severity | Status | Files modified |
|---|-----|---------|----------|--------|----------------|
| 1 | H1 | Parameter name mismatch `indices` vs `rows` in abstracts.py | HIGH | ACCEPTED | `tools/abstracts.py` |
| 2 | H2 | citation_chain new-candidate slicing assumes stable dedup order | HIGH | REJECTED | — |
| 3 | M1 | `fetch_missing` → `fetch_abstracts` kwarg rename across boundary | MEDIUM | ACCEPTED | `tools/claims.py`, `server.py` |
| 4 | M2 | `_original_idx` assigned post-filter, misleading `#` column | MEDIUM | ACCEPTED | `tools/search.py` |
| 5 | M3 | Author normalization inconsistency between dedup and process | MEDIUM | REJECTED | — |
| 6 | M4 | `sources` Literal type vs comma-split parsing mismatch | MEDIUM | REJECTED | — |
| 7 | M5 | `unique_key` incomplete disambiguation (missing 'a' suffix) | MEDIUM | NOTED | — |
| 8 | L1 | `top_n=0` skips top section, behavior undocumented | LOW | REJECTED | — |
| 9 | L2 | `generate_bibliography` DOI-only vs `verify_dois` also covers PMIDs | LOW | REJECTED | — |
| 10 | L3 | `audit_claims` docstring says "near" but uses sentence windowing | LOW | NOTED | — |
| 11 | L4 | `_check_retraction` catches retraction notices too | LOW | REJECTED | — |
| 12 | L5 | No input validation on `results_path` existence | LOW | REJECTED | — |

**Counts:** 3 accepted, 7 rejected, 2 noted, 0 deferred.

## Mechanisms used

| Mechanism | Invocations | Detail |
|-----------|-------------|--------|
| Author's defense | 2/2 High | H1: defense does not hold → accepted. H2: defense holds → rejected |
| Cross-model L1 | 1/1 | Agent (sonnet) on H1 — agrees, finding confirmed |
| Cross-model L2 | 0 | No Blocking findings, no L1 divergence |
| QA auto | 0/12 | No ambiguous verdicts |
| Lateral think | 0 | No stuck points or regressions |
| Evaluate | 1 | lint ✓, build ✓, test ✓ (73 passed); static/coverage failed — `pyright` not installed (replaced by pyrefly), `pytest-cov` absent |
| Drift check | skipped | < 4 fixes |
| Batch mode | inactive | 12 findings < 15 threshold |

## Calibration suppressed (prior audit)

7 patterns from the 2026-03-30 audit were suppressed before review: resource lifecycle, env vars at import, natural language ambiguity in descriptions, `_regex` suffix, open string types, timeout as parameter, bare exceptions in retry logic.

## New calibration rules added

4 new rules added to `feedback_review_severity.md` from rejected findings:

1. **Literal string for small enums with comma-split** — `Literal["s2", "openalex", "s2,openalex"]` is correct for 2 sources, more LLM-friendly than `list[Literal[...]]`
2. **Missing input file validation** — FastMCP catches `FileNotFoundError`, no need for `Path.exists()` guards
3. **Dedup-then-slice in citation_chain** — `full_dedup[len(existing_deduped):]` correctly returns new candidates only
4. **Author format handled at render time** — `process_results` formatters handle both `str` and `list[str]`, no normalization inconsistency

## Fixes applied

### Fix 1 — H1: `rows` → `indices` in abstracts.py

`tools/abstracts.py`: renamed parameter `rows` to `indices`, updated usage and error message. Aligns internal name with public API in `server.py`.

### Fix 2 — M1: `fetch_abstracts` → `fetch_missing` in claims.py

`tools/claims.py`: renamed kwarg `fetch_abstracts` to `fetch_missing` (parameter + body usage). `server.py`: updated call site from `fetch_abstracts=fetch_missing` to `fetch_missing=fetch_missing`.

### Fix 3 — M2: `#` → `Rank` in search.py markdown table

`tools/search.py`: renamed column header from `#` to `Rank` to clarify the value is post-filter order, not the source file index.

## Rejected findings — reasoning summary

| ID | Rejection reason |
|----|-----------------|
| H2 | Slicing logic is correct: merged candidates are enrichments of existing papers, not new entries. Traced through `deduplicate_merge` — the math holds. |
| M3 | Different tool contracts: `deduplicate_results` normalizes at source, `process_results` handles mixed formats at render time. No user-visible inconsistency. |
| M4 | String Literal covers all 3 valid combinations for 2 sources. More LLM-friendly than list type. |
| L1 | `top_n=0` meaning "none" is standard API semantics, self-evident. |
| L2 | Both tool descriptions already state their identifier scope accurately. |
| L4 | Description is accurate at the right abstraction level. |
| L5 | FastMCP catches the exception. Defensive validation adds boilerplate for no benefit in a personal server. |

## Quality metrics

| Metric | Value |
|--------|-------|
| Total findings | 12 (+ 7 suppressed by calibration) |
| Acceptance rate | 25% (3/12) |
| False positive rate | 58% (7/12 rejected) |
| Cumulative FP rate (with prior audit) | 63% (34/54 across both passes) |
| Tests post-fix | 73/73 passed |
| Files modified | 4 (`server.py`, `tools/abstracts.py`, `tools/claims.py`, `tools/search.py`) |
| Linter reformats | Yes (air auto-format on modified files, cosmetic only) |

## Observations for reviewer calibration

1. **mcp-adversary over-flags naming mismatches as HIGH** — H2 was a false positive elevated to HIGH based on a plausible-sounding but incorrect scenario. The reviewer did not trace through `deduplicate_merge` to verify the claim. Code-trace-based re-evaluation caught this.
2. **Author's defense was decisive** — both HIGH findings went through the defense. One held (H2 → rejected), one didn't (H1 → accepted). Without the defense, H2 would likely have been accepted as a bug.
3. **Cross-model L1 added confidence but no new information** — sonnet agreed with the main model on H1. No divergence triggered L2.
4. **Low-severity findings were almost entirely noise** — 0/5 accepted. The reviewer applies generic best practices (input validation, documentation completeness) that don't match the personal-server context.
