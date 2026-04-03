# Session handoff — litrev stabilisation: all functional improvements DONE

## Context
Stabilisation of the `litrev` skill suite (6 components: orchestrator, 4 sub-skills, 1 Python MCP server). This session completed all remaining functional improvements (D1/D2, C2, eval fixtures, micro-audits) and resequenced the plan to place plugin migration as capstone. All priorities A-D done, eval fixtures and micro-audits done. 180 MCP tests passing.

## Key decisions
- **Sequence**: functional improvements before plugin migration. Migration is structural only (move files, update paths, create plugin manifest). New sources (E) after migration so they land in final structure.
- **C2 approach**: manual checklist (option a) — no API exists for French institutional sources (HAS, SOFCOT, SFR, INRS). Step 5b in litrev-search prompts user, search_log.md documents results, synthesize auto-detects missing grey literature.
- **Micro-audits**: lightweight inline checks (3-line summaries), not full agents. Systematic/meta-analysis only. 4 checkpoints after Gates 2, 3a, 4, 5.
- **Eval fixtures**: compact fixtures from example_v3 (5 articles, 19 audit claims). Eval #6 tests Phase 6 verification pipeline, eval #7 tests Phase 8 parallel audit agents.

## Files modified this session

**Skill instructions:**
- `litrev/SKILL.md` — Phase 5 auto-detection note (D2), 4 micro-audits (after Gates 2, 3a, 4, 5)
- `litrev-search/SKILL.md` — Step 5b grey literature checklist, search_log.md template `### Grey literature` section
- `litrev-synthesize/SKILL.md` — Step 4h: 3 required limitation items (AI timeline, skipped phases, grey literature)

**Evals:**
- `evals/evals.json` — eval #6 (Phase 6 verification) + eval #7 (Phase 8 audit)
- `evals/fixtures/verify_phase6/` — review.md, extracted_claims.json, claims_audit.json, references.bib, protocol.md
- `evals/fixtures/audit_phase8/` — same fixture set (Phase 8 needs Phase 6 outputs)

**Tracking:**
- `ROADMAP.md` — date updated, Priority F added (migration), D1/D2/C2 marked done, execution sequence updated
- `ROBUST.md` — micro-audits section updated (implemented)
- `DEFERRED.md` — eval fixtures item struck through (done)
- `README.md` — "priorities A-E" → "A-F"
- `CONTINUATION-PROMPT.md` — this file

**Memory:**
- `project_plan_2026q2.md` — steps 6-9 marked DONE, next → step 10
- `project_roadmap_sources.md` — sequence and description aligned

## Open items

1. **Plugin migration (MIGRATION_PLAN.md)** — 8 phases. Consolidate orchestrator, 4 sub-skills, MCP server into single plugin under `~/.claude/skills/litrev/`. Structural only.

2. **Priority E: new source integrations** — fetch_fulltext, search_scopus, search_wos. After migration.

### DEFERRED items (not in current roadmap)
- FN-3/GAP-3: Import path for pre-existing corpus (PMIDs, BibTeX, PDFs → combined_results.json)
- Umbrella review (review of reviews) workflow
- Unit tests manquants pour 5/10 modules MCP tools (abstracts, openalex_search, pubmed_search, s2_search, snowball)

## Continuation prompt

```
All functional improvements for litrev are DONE. 180 MCP tests passing. Ready for plugin migration.

Next: execute MIGRATION_PLAN.md — consolidate 6 components (orchestrator, litrev-search, litrev-screen, litrev-extract, litrev-synthesize, litrev-mcp) into a single Claude Code plugin.

The plan has 8 phases:
1. Scaffold plugin (.claude-plugin/ manifest)
2. Copy sub-skills into skills/ subdirectory
3. Absorb litrev-mcp into mcp/ subdirectory
4. Fix all paths in SKILL.md files and tracking docs
5. Update .gitignore
6. Update MCP config (~/.claude/.mcp.json)
7. Verification (tests, skill invocation, MCP tools)
8. Cleanup (delete old standalone directories)

Key files:
- `litrev/MIGRATION_PLAN.md` (canonical plan, all 8 phases with checkboxes)
- `litrev/ROADMAP.md` (Priority F = migration)
- `litrev-mcp/` (MCP server to absorb, 180 tests)
- `litrev-search/`, `litrev-screen/`, `litrev-extract/`, `litrev-synthesize/` (sub-skills to consolidate)
- Memory: project_plan_2026q2.md (step 10 = migration)

Known risks:
- MCP prefix may change from `mcp__litrev-mcp__` to `mcp__plugin_litrev__` — test in Phase 7 before deleting old dirs
- Absolute paths in litrev-screen/SKILL.md:69 and litrev-synthesize/SKILL.md:74 — fix in Phase 4
- Shell `cp` commands in litrev-synthesize/SKILL.md — replace with Read/Write instructions

Constraints: user manages all git operations (never run git write commands). Always update memory files when state changes.
```
