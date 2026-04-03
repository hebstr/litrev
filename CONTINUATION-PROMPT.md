# Session handoff — litrev stabilisation: C1 dedup stats + memory updates + sync

## Context
Continuing stabilisation of the `litrev` skill suite (6 components: orchestrator, 4 sub-skills, 1 Python MCP server). This session resumed from a compacted conversation. Prior sessions completed priorities A (MCP bug fixes), B (synthesis quality), unit tests (177 tests), and PMID resolver. This session updated stale memory files, ran `/sync-files --deep`, implemented C1 (dedup stats), and ran another deep sync to verify consistency.

## Key decisions
- **C1 approach**: `deduplicate_merge` in `dedup.py` gained a `track_stats=True` parameter rather than always returning stats. This preserves backward compatibility — existing callers (including `process_results` which calls `deduplicate_merge` without `track_stats`) are unaffected. Only `deduplicate_results` uses the new parameter.
- **Memory discipline feedback saved**: user gave explicit instruction "toujours update la mémoire" — saved as `feedback_always_update_memory.md`. All state-changing work must be accompanied by memory updates in the same response.
- **Deep sync false positive triaged**: orchestrator SKILL.md declares 6 MCP tools it doesn't directly call (search_pubmed, search_s2, search_openalex, process_results, fetch_abstracts, extract_claims_regex). These are needed in `allowed-tools` because sub-skills inherit parent permissions. Not a real issue.

## Current state

### Files modified this session

**Python (litrev-mcp, sibling directory `~/.claude/skills/litrev-mcp/`):**
- `src/litrev_mcp/lib/dedup.py:41-86` — `deduplicate_merge` gains `track_stats` parameter, returns `(list, stats_dict)` tuple when True
- `src/litrev_mcp/tools/search.py:340,355-361` — `deduplicate_results` uses `track_stats=True`, returns `duplicates_by_pmid/doi/title`
- `tests/test_dedup.py:96-120` — 3 new tests: `test_track_stats_returns_tuple`, `test_track_stats_counts_methods`, `test_no_track_stats_returns_list`
- `tests/test_process_results.py:291-293` — updated `test_basic_dedup` to assert new stats keys

**Skill instructions:**
- `litrev-search/SKILL.md:163` — Step 3: documents dedup stats fields returned by tool
- `litrev-search/SKILL.md:230` — Step 6 template: example shows per-method breakdown

**Tracking files (litrev root):**
- `ROADMAP.md:79-87` — C1 marked done with checkboxes, execution sequence updated (C1 ✓)
- `ROADMAP.md:168-171` — execution sequence and status line updated
- `ROBUST.md:21` — test count updated to 180/180
- `CONTINUATION-PROMPT.md` — this file
- `DEFERRED.md` — unchanged this session

**Memory (outside git, `~/.claude/projects/.../memory/`):**
- `project_plan_2026q2.md` — step 2 marked DONE (unit tests + PMID resolver), step 5 marked skipped, next actions updated
- `project_mcp_bugs_2026q2.md` — all 6 bugs marked FIXED (Gate 3a, Unicode middle dots, spelled-out numbers were OPEN)
- `feedback_always_update_memory.md` — NEW: always update memory on state change
- `MEMORY.md` — index updated (plan date, bug count, memory discipline entry)

### Tests verified
- Full suite: 180/180 PASS (`uv run pytest tests/ -v`)
- No regressions from C1 changes

## Open items

1. **C2 — Grey literature / guideline database support** (ROADMAP). French institutional guidelines (HAS, SOFCOT, SFR, INRS) not searchable via PubMed/S2/OA. Approach undecided: (a) manual search checklist in protocol, (b) scraping HAS recommandations, (c) dedicated search tool.

2. **D1 — AI-assisted timeline disclosure** (ROADMAP). Synthesize should auto-disclose single-day review timeline in limitations.

3. **D2 — Skipped phase disclosure** (ROADMAP). When snowballing is skipped, pass this to synthesize as a required limitation item.

4. **Eval fixtures for Phase 6/8** (DEFERRED.md). No evals for verification or audit phases — highest MCP bug surface area.

5. **Micro-audits (plan step 6)** — inter-phase quality checkpoints for systematic/meta-analysis reviews. Not yet designed.

## Continuation prompt

```
I'm stabilising the litrev skill suite. All Priority A (MCP fixes), B (synthesis quality), and C1 (dedup stats) are DONE. 180 tests passing.

Next priorities:

1. Priority C2: grey literature / guideline database support (HAS, SOFCOT, SFR, INRS). Approach TBD — options in ROADMAP.md C2.
2. Priority D1/D2: orchestrator improvements — auto-disclose AI-assisted timeline (D1) and skipped phases (D2) in review limitations section.
3. Eval fixtures for Phase 6 (verification) and Phase 8 (audit) — highest MCP bug surface, no evals yet.
4. Plan step 6: micro-audits (inter-phase quality checkpoints for systematic/meta-analysis reviews).

Key files:
- `litrev/ROADMAP.md` (canonical roadmap, A+B+C1 done, C2/D/E remaining)
- `litrev/DEFERRED.md` (deferred items including eval fixtures)
- `litrev-mcp/src/litrev_mcp/lib/dedup.py` (deduplicate_merge with track_stats)
- `litrev-mcp/src/litrev_mcp/tools/search.py` (deduplicate_results with per-method stats)
- `litrev-search/SKILL.md` (Step 3 + Step 6 dedup logging instructions)
- `litrev-synthesize/SKILL.md` (target for D1/D2 limitation disclosures)
- `litrev/SKILL.md` (orchestrator — target for D2 skipped-phase passing)
- Memory: project_plan_2026q2.md, feedback_always_update_memory.md

Constraints: user manages all git operations (never run git write commands). Existing tests must keep passing (180/180). Always update memory files when state changes (feedback rule).
```
