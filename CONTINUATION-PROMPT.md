# Session handoff — litrev Layer 1 robustness: fixtures + MCP bug fixes

## Context
Working on the `litrev` Claude Code skill (`~/.claude/skills/litrev/`) and its companion MCP server (`~/.claude/skills/litrev-mcp/`). The skill orchestrates systematic literature reviews through 9 phases. A terrain test (example_v2, scapulalgie scoping review) was completed on 2026-04-01. This session focused on the next robustness priorities from `ROBUST.md` § Priorisation.

## Key decisions
- **Daliri_2023 and Engebretsen_2020 design labels were wrong** in `evals/fixtures/extract_10articles/expected.json`. Daliri is cross-sectional (not RCT, confirmed by abstract: "large population cross-sectional study"). Engebretsen is cohort (not RCT, confirmed by PubMed publication_type: "Observational Study" and abstract: "prospective cohort"). Corrected both, plus the design distribution in assertions.
- **Bug 2 (French thousands) fix strategy**: two-layer fix — `NUM_PATTERN` in `lib/patterns.py` now matches space-separated thousands as a single token, AND `_normalize_number` in `tools/verify.py` strips thousand-separator spaces before general whitespace removal. This ensures both extraction and audit handle French numbers correctly.
- **Bug 3 (DOI mapping) is upstream**: root cause is LLM-hallucinated DOIs in embedded BibTeX. MCP-side mitigation added (title cross-verification with 30% word-overlap threshold), but the real fix belongs in `litrev-synthesize` (strip DOIs from embedded BibTeX). This is documented in memory but not yet implemented.
- **Phase 5 fixture uses 8 articles** (not "20 claims" as originally described) — the 8 articles contain 22 quantitative + 26 semantic claims across 7 themes, which exceeds the expected.json assertion thresholds.

## Current state

### Completed (all uncommitted, 7 files across 2 repos)

**litrev repo** (7 uncommitted files):
- `evals/evals.json` — 5 eval cases (was 3), added id:4 (extraction) and id:5 (synthesis)
- `evals/fixtures/extract_10articles/combined_results.json` — 12 articles extracted from example_v2
- `evals/fixtures/extract_10articles/included_indices.json` — `[0..11]` remapped indices
- `evals/fixtures/extract_10articles/expected.json` — corrected designs + distribution
- `evals/fixtures/synthesize_20claims/extracted_claims.json` — 8 articles, 22+26 claims
- `evals/fixtures/synthesize_20claims/protocol.md` — copied from example_v2
- `DEFERRED.md` — evals line marked resolved
- `ROBUST.md` — priorities 3, 4b marked done; priority 5 marked "next"

**litrev-mcp repo** (uncommitted):
- `src/litrev_mcp/tools/claims.py:34-35` — output_path resolved relative to results_path
- `src/litrev_mcp/lib/patterns.py:11` — NUM_PATTERN: added `\d{1,3}(?:[\s\u00a0]\d{3})+` alternative
- `src/litrev_mcp/tools/verify.py:486` — `_normalize_number`: thousand-separator stripping before general cleanup
- `src/litrev_mcp/tools/verify.py:350-363` — `_extract_refs_md`: extracts title field from embedded BibTeX
- `src/litrev_mcp/tools/verify.py:452-464` — `generate_bibliography`: title cross-verification (word overlap < 30% = MISMATCH)
- `tests/test_patterns.py:30-45` — 5 new test cases for French thousands
- All 78 tests pass

**Memory updated**:
- `project_mcp_bugs_2026q2.md` — all 3 bugs marked as fixed/mitigated with details

## Open items

1. **`/skill-adversary` on litrev orchestrator** — Priority 5 in ROBUST.md, next step. Target: `~/.claude/skills/litrev/` (SKILL.md + agents/ + evals/). Previous adversary runs on sub-skills found 47% FP rate; expect similar here.
2. **Upstream fix for DOI hallucination** — `litrev-synthesize` should stop embedding DOIs in BibTeX blocks, letting `generate_bibliography` resolve from PMIDs only. Not yet started.
3. **Layer 1 mechanical gates** — Priority 6 in ROBUST.md. Validation scripts to check file structure after each phase.
4. **Nothing is committed** — user manages git. 7 files in litrev + several in litrev-mcp are staged/unstaged.

## Continuation prompt

```
Context: litrev skill (~/.claude/skills/litrev/) robustness work. Priorities 1-4b in ROBUST.md are done. Fixtures for Phase 4+5 evals created, 3 MCP bugs fixed (uncommitted in litrev-mcp), DEFERRED.md and ROBUST.md updated. 7 uncommitted files in litrev, several in litrev-mcp. Memory file project_mcp_bugs_2026q2.md is current.

Next task: run /skill-adversary on the litrev orchestrator (priority 5 in ROBUST.md § Priorisation). This is the last Layer 1 item. Target directory: ~/.claude/skills/litrev/ (SKILL.md is the main orchestrator, 592 lines, 9 phases + 9 gates). Also review agents/audit_fidelity.md and agents/audit_methodology.md. Previous adversary runs on the 4 sub-skills found 64 findings with 47% FP rate — read ~/.claude/projects/-home-julien--claude-skills-litrev/memory/skipped_review_points.md BEFORE reporting to avoid re-raising dismissed points.

Key files:
- ~/.claude/skills/litrev/SKILL.md (orchestrator)
- ~/.claude/skills/litrev/agents/audit_fidelity.md, audit_methodology.md
- ~/.claude/skills/litrev/evals/evals.json (5 eval cases)
- ~/.claude/skills/litrev/ROBUST.md (robustness plan, priority table)
- ~/.claude/skills/litrev/DEFERRED.md (deferred findings)

Constraints: user manages all git operations (no commits). Code text in English, conversation in French. No emojis. Read skipped_review_points.md before any review output.
```
