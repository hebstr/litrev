# Review Quality Report — litrev-synthesize

**Date:** 2026-04-01
**Target:** `~/.claude/skills/litrev-synthesize`
**Reviewer:** skill-adversary (via foreground Agent)
**Walkthrough:** review-walkthrough with `--adversarial` flag
**Context:** personal (detected from path `~/.claude/skills/`)
**Calibration:** none (skill reviewers get no calibration injection)
**Model:** claude-opus-4-6

## Review summary

| # | Finding | Severity | Status | Mode |
|---|---------|----------|--------|------|
| 1 | Template sections without SKILL.md guidance | HIGH→MEDIUM | ACCEPTED (narrowed) | manual |
| 2 | `$SKILL_DIR` dependency not explicit | MEDIUM | REJECTED | manual |
| 3 | Iteration-1 benchmark missing 3 assertions | MEDIUM | REJECTED | manual |
| 4 | Resume path missing YAML header check | MEDIUM | ACCEPTED | manual |
| 5 | Bibliometric Overview placeholder left for LLM to delete | MEDIUM | REJECTED | manual |
| 6 | UNVERIFIED flag vs self-check item 3 conflict | MEDIUM | ACCEPTED | manual |
| 7 | Missing Glob/Grep in allowed-tools | LOW | REJECTED | manual |
| 8 | Review type adaptation placement unspecified | LOW | REJECTED | manual |
| 9 | Long description field | LOW | NOTED | manual |
| 10 | Appendix F/G placeholders for all review types | LOW | REJECTED | manual |
| 11 | Unconditional GRADE eval assertion | LOW | ACCEPTED | manual |

**Totals:** 4 accepted, 5 rejected, 1 noted, 0 deferred

## Mechanisms used

| Mechanism | Invocations | Details |
|-----------|-------------|---------|
| Author's defense | 6/6 Important+ | 2 held (findings 2, 5 → rejected), 4 did not hold (findings 1, 3→rejected on other grounds, 4, 6 → accepted) |
| Cross-model L1 (intra-family) | 1/6 Important+ | Agent sonnet on Finding 1 — partial agree, confirmed narrowing to Methodological Approaches only. 5 skipped (clear verdicts) |
| Cross-model L2 (cross-provider) | 0 | No HIGH after downgrade of Finding 1, no L1 divergence |
| QA auto | 0 | No ambiguous verdicts |
| Lateral think | 0 | No stuck points or regressions |
| Evaluate | skipped | Fewer than 4 code fixes; changes were to SKILL.md text and evals.json |
| Drift check | skipped | Fewer than 4 fixes |
| Batch triage | inactive | 11 findings < 15 threshold |

## Changes applied

### 1. SKILL.md — New Step 4f (Methodological Approaches)

**Finding 1 (narrowed):** Reviewer flagged 5 template sections without explicit guidance. Cross-model L1 (sonnet) confirmed only `## Methodological Approaches` (Results-level) was genuinely unguided. The other 4 sections (Protocol, Tools and Software, Comparison with Previous Reviews, Future Research) are covered by parent-section instructions (Steps 4c and 4h).

**Fix:** Added `#### 4f. Results — Methodological Approaches` with conditional inclusion rule (>=10 heterogeneous studies) and data source constraint (`quality.design` and `quality.recommended_tool` fields only). Renumbered 4f-4j → 4g-4k.

**Lines affected:** ~160-166 (new section), plus renumbering at ~168, 175, 179, 196.

### 2. SKILL.md — Resume path YAML header check

**Finding 4:** When resuming an existing `*_review.md` file, the skill skipped the template copy but never verified `bibliography` and `csl` YAML fields. Self-check item 7 would catch this post-hoc, but the LLM should verify early.

**Fix:** Added sentence to line 97: "Verify its YAML header contains `bibliography: references.bib` and `csl: vancouver.csl`; add them if missing."

### 3. SKILL.md — Self-check item 3 (UNVERIFIED consistency)

**Finding 6:** The constrained writing rule allows `<!-- UNVERIFIED -->` flags for numbers not in the extraction. But self-check item 3 said "All numeric claims must appear in extracted_claims.json" and "fix it before proceeding" — treating UNVERIFIED flags as failures.

**Fix:** Updated item 3 to: "All numeric claims in the text appear in `extracted_claims.json` for the cited article, or are flagged with `<!-- UNVERIFIED -->`. Report the count of UNVERIFIED flags but do not treat them as failures."

### 4. evals/evals.json — Conditional GRADE assertion

**Finding 11:** Eval 1 (systematic-rotator-cuff) unconditionally required a GRADE table, but SKILL.md qualifies it ("if enough homogeneous studies"). The test case has 4 heterogeneous studies across 4 themes.

**Fix:** Updated assertion text to: "GRADE Summary of Findings table is present, or its absence is justified due to study heterogeneity (systematic review type)."

## Rejected findings — calibration patterns

Three generalizable patterns captured in `feedback_review_severity.md` (project memory):

1. **Conditional template sections with dual-layer instruction** (HTML comment + SKILL.md directive) are not findings — they are the standard mechanism (from Findings 5, 10).

2. **Implicit sequential dependencies** in SKILL.md (Setup before Steps) follow universal skill convention — no explicit dependency notes needed (from Finding 2).

3. **Minimal `allowed-tools`** is intentional when the skill works with known file paths — expanding tool surface without need is not an improvement (from Finding 7).

## Quality assessment of the skill-adversary review

### Signal quality

- **True positives:** 4/11 (36%) — Findings 1 (narrowed), 4, 6, 11 identified real gaps that were fixed.
- **Partial true positive:** Finding 1 was directionally correct but over-scoped (5 sections flagged, only 1 was genuinely unguided). Cross-model L1 was essential for scoping correction.
- **False positives:** 5/11 (45%) — Findings 2, 5, 7, 8, 10 flagged patterns that are standard skill conventions or already handled by existing mechanisms.
- **Informational:** 1/11 (9%) — Finding 9 (long description) is a noted observation with no actionable fix.

### Severity calibration

- Finding 1 was rated HIGH but downgraded to MEDIUM after L1 cross-model narrowing — the reviewer over-scoped the problem.
- Findings 2-6 were all rated MEDIUM; 3 were rejected (overcalibrated for this context), 2 accepted.
- LOW findings were appropriately calibrated — minor or informational.

### Observations for future reviews

- The reviewer has a pattern of flagging "LLM must remember to X" as a problem when the instruction is already explicit. This is a philosophical disagreement about skill design, not a real gap — skills inherently rely on LLM instruction-following.
- The reviewer does not account for eval coverage — several "risks" it flags (Bibliometric Overview, Appendices) are already tested by evals and confirmed working.
- Grouping multiple sub-issues into a single finding (Finding 1: 5 sections) inflates severity. The reviewer should separate distinct issues.

## Sync audit (post-fix)

| File | Status |
|------|--------|
| assets/review_template.md | OK — already has `## Methodological Approaches`, now covered by new Step 4f |
| workspace/iteration-1/benchmark.md | OK — frozen historical snapshot |
| workspace/iteration-1/benchmark.json | OK — frozen historical snapshot |
| workspace/iteration-2/benchmark.md | OK — frozen historical snapshot |

No stale files detected.
