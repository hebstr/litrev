# Review Walkthrough Report — litrev-search

| | |
|---|---|
| **Date** | 2026-04-01 |
| **Target** | `~/.claude/skills/litrev-search` |
| **Reviewer** | skill-adversary |
| **Flags** | `--adversarial` |
| **Deployment context** | personal skill (detected from `~/.claude/skills/` path) |
| **Calibration** | none (no prior `feedback_review_severity.md`) |

## Findings summary

| # | ID | Finding | Severity | Status | Mode | Files modified |
|---|-----|---------|----------|--------|------|----------------|
| 1 | B1 | Niche topic noise control broken — spot-check heuristic too vague, eval regression | Blocking | ACCEPTED | manual | `SKILL.md` |
| 2 | B2 | MCP tools `deduplicate_results`, `process_results` undeclared in `allowed-tools` | Blocking | ACCEPTED | manual | `SKILL.md` |
| 3 | B3 | Eval threshold mismatch: evals.json says <150, benchmark.json says <80 | Blocking | ACCEPTED | batch | `evals/evals.json` |
| 4 | I1 | No post-search relevance filtering mechanism | Important | REJECTED | manual | — |
| 5 | I2 | `process_results` output format not enforced (card vs table in iteration-2) | Important | REJECTED | manual | — |
| 6 | I3 | Semantic Scholar near-guaranteed 429 without API key, counted toward min-3 | Important | REJECTED | manual | — |
| 7 | I4 | `context: fork` may cause CWD confusion with `review/` output path | Important | REJECTED | manual | — |
| 8 | I5 | No error handling for efetch XML parsing (structured/missing abstracts) | Important | ACCEPTED | manual | `SKILL.md` |
| 9 | I6 | Schema field `authors` type inconsistency (string in example vs list in schema) | Important | ACCEPTED | batch | `SKILL.md` |
| 10 | S1 | Evals lack negative/edge-case scenarios | Suggestion | REJECTED | batch | — |
| 11 | S2 | `paper_prioritization.md` listed in Reference Files but unused by this skill | Suggestion | ACCEPTED | batch | `SKILL.md` |
| 12 | S3 | No `agents/` or `templates/` directories | Suggestion | REJECTED | batch | — |
| 13 | S4 | Benchmark notes mention inconsistent output path across evals | Suggestion | REJECTED | batch | — |
| 14 | S5 | Rate-limit wait times hardcoded in prose | Suggestion | REJECTED | batch | — |
| 15 | S6 | `allowed-tools` should include Bash or document why excluded | Suggestion | REJECTED | batch | — |
| 16 | S7 | medRxiv date range instruction relies on LLM knowing current date | Suggestion | REJECTED | manual | — |

**Counts:** 6 accepted, 10 rejected, 0 noted, 0 deferred.
**Batch:** 3 auto-fix, 5 auto-reject. **Manual:** 3 accepted, 5 rejected.

## Changes applied

### B1 — Niche topic OpenAlex heuristic tightened

**File:** `SKILL.md` line 128 (OpenAlex § Niche topics)

- `per_page` reduced from 50 to 25 for niche topics
- Spot-check window increased from 5 to 10 titles
- Discard threshold tightened from "more than half" to "more than 3 out of 10"
- Added instruction to log discarded queries in `search_log.md`

### B2 — MCP tools added to `allowed-tools`

**File:** `SKILL.md` line 5

Added `mcp__litrev-mcp__deduplicate_results` and `mcp__litrev-mcp__process_results`. Syntax confirmed against `litrev-screen/SKILL.md` which uses the same `mcp__litrev-mcp__` prefix convention.

### B3 — Eval threshold aligned

**File:** `evals/evals.json` eval 2, expectation 4

Changed `"fewer than 150 articles"` to `"fewer than 80 articles"` to match the benchmark.json grading threshold. The tighter threshold (80) is the meaningful one for a niche topic.

### I5 — efetch XML parsing instruction expanded

**File:** `SKILL.md` line 97

Replaced `Parse <AbstractText> from the XML response` with explicit handling:
- Concatenate all `<AbstractText>` elements with their `Label` attributes for structured abstracts
- Set abstract to `null` when no `<AbstractText>` exists

### I6 — authors example fixed (batch)

**File:** `SKILL.md` line 167

Changed `"authors": "LastName1 AB, LastName2 CD"` (string) to `"authors": ["LastName1 AB", "LastName2 CD"]` (list) to match `json_schema.md` type declaration.

### S2 — Dead reference removed (batch)

**File:** `SKILL.md` line 272

Removed `paper_prioritization.md` from the Reference Files section. The file itself remains in `references/` for potential use by downstream skills.

## Rejection rationale (manual findings)

| # | Finding | Author's defense | Verdict rationale |
|---|---------|-----------------|-------------------|
| I1 | No relevance filtering | Relevance filtering is the screening skill's job; search optimizes for recall | Pipeline architecture separates search (recall) from screening (precision). Adding per-article filtering here duplicates litrev-screen logic. |
| I2 | Output format not enforced | Instruction already says "Do not write manually"; failure was LLM non-compliance | The MCP tool produces a deterministic format. The skill instruction is correct — the iteration-2 failure was the model ignoring the prohibition, not a skill defect. |
| I3 | S2 counts toward min-3 | Skill documents S2 unreliability, suggests substitutes, escalates to user when threshold not met | Existing fallback logic (retry, substitute, proceed with fewer, downgrade review type) handles S2 failure explicitly. The 3-database threshold is intentionally aspirational. |
| I4 | CWD confusion | Pre-loaded `pwd` anchors CWD; benchmark inconsistency was in without_skill runs | Factual check: all with_skill eval runs produce `review/` outputs correctly. The benchmark note about inconsistent paths refers to without_skill baselines. |
| S7 | medRxiv date fragile | N/A (Suggestion, no defense applied) | The current date is reliably injected in the Claude Code environment via `currentDate` system context. Theoretical fragility that doesn't manifest in practice. |

## Mechanisms report

| Mechanism | Invocations | Notes |
|-----------|-------------|-------|
| Batch triage | 8/16 | 3 auto-fix, 5 auto-reject |
| Author's defense | 7/8 Important+ | 4 held (I1, I3, I4, S7 via defense logic), 3 did not hold (B1, B2, I5) |
| QA auto | 0 | No ambiguous verdicts |
| Cross-model L1 | 0/8 Important+ | All resolved by author's defense or factual check before escalation |
| Cross-model L2 | 0 | No L1 divergence to escalate |
| Lateral think | 0 | No stuck points or regressions |
| Evaluate | 0 (failed) | See Ouroboros issue below |
| Drift | skipped | Manual consistency check substituted |

## Ouroboros integration issue

`ouroboros_evaluate` failed with `Claude Agent SDK request failed` (exit code 1). Root cause: the tool was called with an invented `session_id` (`litrev-search-review-2026-04-01`). `ouroboros_evaluate` requires a real Ouroboros session created via `ouroboros_execute_seed` — it is not a standalone validation tool.

**Correct alternative:** `ouroboros_qa` is standalone and accepts an artifact + quality bar without requiring a session. The review-walkthrough bridge should route final validation through `ouroboros_qa`, not `ouroboros_evaluate`, when no Ouroboros session exists.

**Impact on this walkthrough:** the final automated validation step was skipped. A manual consistency check (re-reading all modified files and their dependents) was performed instead. No issues found.

## Quality assessment of the review itself

**Reviewer (skill-adversary) performance:**
- 3/3 Blocking findings were real and actionable — good signal-to-noise at the top tier
- 2/6 Important findings were real (I5, I6); 4/6 were either false positives (I4) or already handled by existing skill logic (I1, I2, I3) — 33% precision at this tier
- 0/7 Suggestion findings were accepted after evaluation — mostly inapplicable to a personal skill context or proposing complexity with no benefit
- Overall precision: 6/16 (38%) — acceptable for an adversarial review, which intentionally over-reports

**Walkthrough process:**
- Batch triage correctly routed mechanical fixes (B3, I6, S2) and clear false positives (S3, S5, S6) out of manual review
- Author's defense was the most productive mechanism — it surfaced the pipeline boundary argument (I1) and the existing fallback logic (I3) that the reviewer missed
- Cross-model validation never triggered because all findings resolved cleanly via defense or factual check — this is expected for a well-scoped skill with clear architecture
- The Ouroboros integration bug (`evaluate` vs `qa`) should be fixed in the walkthrough bridge for future sessions
