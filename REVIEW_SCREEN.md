# Review Walkthrough Report — litrev-screen

| | |
|---|---|
| **Date** | 2026-04-01 |
| **Target** | `~/.claude/skills/litrev-screen` |
| **Reviewer** | skill-adversary |
| **Flags** | `--adversarial` |
| **Deployment context** | personal (path ~/.claude/skills/) |
| **Calibration** | none (first audit of this skill) |

## Findings summary

| # | ID | Finding | Severity | Status | Files modified |
|---|-----|---------|----------|--------|----------------|
| 1 | H1 | `allowed-tools` missing MCP `fetch_abstracts` + stale benchmark assertions (`extract_abstracts.py`) | HIGH→MEDIUM | ACCEPTED | `SKILL.md`, `workspace/iteration-1/benchmark.json`, `workspace/iteration-2/benchmark.json` |
| 2 | M1 | `search_log.md` reference should be `search_results.md` | MEDIUM | ACCEPTED | `SKILL.md` |
| 3 | M2 | Destructive `##`-boundary deletion in resume logic | MEDIUM | REJECTED | — |
| 4 | M3 | No-abstract path from Step 3 to final `included_indices.json` implicit | MEDIUM | NOTED | — |
| 5 | M4 | Missing exact-match assertion for eval 1 included set | MEDIUM | ACCEPTED | `evals/evals.json` |
| 6 | M5 | Missing negative assertion for Anderson (index 8) | MEDIUM | ACCEPTED (resolved by #5) | — |
| 7 | M6 | Stale `(process_results.py)` parenthetical in source table | MEDIUM | ACCEPTED | `SKILL.md` |
| 8 | M7 | Rapid review table wording backwards ("Combined with title") | MEDIUM | ACCEPTED | `SKILL.md` |
| 9 | L1 | Non-standard `!`command`` shell syntax in pre-loaded pipeline state | LOW | REJECTED | — |
| 10 | L2 | Description field too long in frontmatter | LOW | REJECTED | — |
| 11 | L3 | Benchmark eval 2 passed by testing parent-agent behavior | LOW | NOTED | — |
| 12 | L4 | No eval coverage for rapid review + no-abstract path | LOW | DEFERRED | — |
| 13 | L5 | Step 3 mandatory pass-through for no-abstract already documented | LOW | REJECTED | — |

**Counts:** 6 accepted, 4 rejected, 2 noted, 1 deferred.

## Mechanisms used

| Mechanism | Invocations | Detail |
|-----------|-------------|--------|
| Author's defense | 2/2 HIGH | H1: defense partially holds (fallback exists at line 118) → severity downgraded to MEDIUM, fixes still applied |
| Cross-model L1 | 1/1 | Agent (sonnet) on H1 — disagrees on severity: MEDIUM not HIGH given graceful fallback. Confirmed downgrade. |
| Cross-model L2 | 0/1 | Attempted on H1 (Blocking + `--adversarial`), runtime error from `ouroboros_evaluate` — not blocking |
| QA auto | 0/13 | No ambiguous verdicts |
| Lateral think | 0 | No stuck points or regressions |
| Evaluate | skipped | Not a git repo — no clean diff baseline for validation |
| Drift check | skipped | Same reason (no git repo) |
| Batch mode | inactive | 13 findings < 15 threshold |

## Calibration suppressed (prior audit)

None — first audit of this skill.

## New calibration rules added

4 new rules added to `feedback_review_severity.md` from rejected findings:

1. **`!`command`` shell syntax** — valid Claude Code dynamic expansion at skill load time, works in `context: fork`
2. **Long `description` field** — standard pattern for trigger phrase matching, no alternative frontmatter key exists
3. **`##`-boundary deletion in resume logic** — `screening_log.md` is a skill-controlled file with predictable headings, not user-edited
4. **Step 3 pass-through for no-abstract** — already explicitly documented at SKILL.md line 169

## Fixes applied

### Fix 1 — H1: `allowed-tools` + stale benchmark assertions

- `SKILL.md:5`: added `mcp__litrev-mcp__fetch_abstracts` to `allowed-tools`
- `workspace/iteration-2/benchmark.json:78`: replaced stale `extract_abstracts.py` assertion with `MCP tool fetch_abstracts was called with fetch_missing true`
- `workspace/iteration-1/benchmark.json`: same replacement (2 occurrences)

### Fix 2 — M1: `search_log.md` → `search_results.md`

`SKILL.md:216`: corrected file reference from `review/search_log.md` to `review/search_results.md`.

### Fix 3 — M4: exact-match assertion for eval 1

`evals/evals.json`: added assertion `"included_indices.json contains exactly [0, 1, 4, 6] (no extra indices)"` to catch false inclusions. Also resolves M5 (Anderson index 8).

### Fix 4 — M6: stale parenthetical

`SKILL.md:36`: removed `(process_results.py)` parenthetical from source table — stale reference to pre-MCP implementation.

### Fix 5 — M7: rapid review table wording

`SKILL.md:230`: replaced confusing "Required (combined with abstract in one pass)" / "Combined with title" with "Combined (single title + abstract pass)" in both columns.

## Rejected findings — reasoning summary

| ID | Rejection reason |
|----|-----------------|
| M2 | `screening_log.md` is a skill-generated file with predictable headings. No user edits, no unexpected `##` sections. The `##`-boundary deletion is safe for this controlled format. |
| L1 | `!`command`` is documented Claude Code skill syntax for dynamic shell expansion at load time. Works in all contexts including `context: fork`. |
| L2 | Long description is the only mechanism for trigger phrase matching. No `triggers` or `examples` frontmatter key exists. Token cost is marginal. |
| L5 | The pass-through behavior is already explicitly documented: "If no additional information is available beyond what was already screened, retain the article and note it in the log" (line 169). |

## Deferred findings

| Finding | Reason | Next step |
|---------|--------|-----------|
| L4: No eval for rapid + no-abstract | Requires creating new test data | Add a test case (or extend test-case-3) with articles missing abstracts in a rapid review scenario |

## Quality metrics

| Metric | Value |
|--------|-------|
| Total findings | 13 |
| Acceptance rate | 46% (6/13) |
| False positive rate | 31% (4/13 rejected) |
| Severity accuracy | 1/2 HIGH downgraded to MEDIUM after L1 cross-model validation |
| Files modified | 5 (`SKILL.md`, `evals/evals.json`, `workspace/iteration-1/benchmark.json`, `workspace/iteration-2/benchmark.json`, `DEFERRED.md`) |

## Observations for reviewer calibration

1. **skill-adversary correctly identified the pre-MCP artifact residue** — findings 1, 7, and 11 all trace to the same root cause: stale references to `extract_abstracts.py` / `process_results.py` from a pre-MCP implementation. The reviewer found three independent surface manifestations of one underlying migration debt.
2. **Cross-model L1 added value on severity** — sonnet's disagreement on H1 was substantive: it identified the graceful fallback (line 118) that the original reviewer missed. This led to a justified severity downgrade. The defense mechanism and L1 reinforced each other.
3. **Reviewer doesn't understand Claude Code skill internals** — two rejections (L1: shell syntax, L2: description length) stem from the reviewer not knowing how skills work. The `!`command`` syntax and long descriptions are standard patterns, not anti-patterns. Future skill-adversary runs on Claude Code skills should be calibrated for skill-format awareness.
4. **MEDIUM findings were the most productive tier** — 5/6 MEDIUM accepted (83%), vs 1/2 HIGH accepted-as-downgraded (50%), vs 0/5 LOW accepted (0%). The reviewer's MEDIUM findings were actionable and correctly scoped. LOW findings were mostly noise or documentation taste.
5. **Eval coverage gaps are real but low-impact** — the rapid+no-abstract gap (L4, deferred) and the parent-vs-fork measurement issue (L3, noted) are legitimate eval design concerns. Neither affects the skill's runtime behavior, but they reduce confidence in benchmark results.
