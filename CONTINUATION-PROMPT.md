# Session handoff — litrev plugin migration COMPLETE

## Context
Plugin migration of the `litrev` skill suite is COMPLETE (2026-04-03). All 6 standalone components consolidated into a single plugin under `~/.claude/skills/litrev/`. 180 MCP tests pass, 12 tools accessible, prefix `mcp__litrev-mcp__*` unchanged. Old directories deleted, backup at `~/.claude/skills/litrev-backup-20260403.tar.gz`.

## What was done (Phases 1-8)

1. **Phase 1**: Created `.claude-plugin/` (marketplace.json, plugin.json, .mcp.json). Moved orchestrator into `skills/litrev/`.
2. **Phase 2**: Copied 4 sub-skills into `skills/`. workspace/ excluded.
3. **Phase 3**: Absorbed litrev-mcp into `mcp/`. Consolidated DEFERRED.md. 180 tests passed.
4. **Phase 4**: Fixed all paths (absolute to relative) in SKILL.md files and tracking docs.
5. **Phase 5**: Merged .gitignore.
6. **Phase 6**: Updated `~/.claude/.mcp.json` to point to `litrev/mcp`.
7. **Phase 7**: Full verification — 180 tests, skill names unchanged, MCP tools accessible, deep scan 0 issues.
8. **Phase 8**: Deleted 5 old standalone directories. Structural smoke tests PASS.

## What remains

### Next: Priority E — New source integrations
- E1: fetch_fulltext (DOI to full text via Unpaywall/PMC/S2/CORE/Sci-Hub cascade)
- E2: search_scopus (api.elsevier.com)
- E3: search_wos (api.clarivate.com)
- E4: EMBASE (deferred — no public API)

New tools land in `mcp/src/litrev_mcp/tools/`.

### DEFERRED items
- FN-3/GAP-3: Import path for pre-existing corpus
- Umbrella review workflow
- Unit tests for 5/10 MCP tool modules
- Edge-case evals (F24-F27)

## Key files
- `ROADMAP.md` — all priorities A-F done, E next
- `MIGRATION_PLAN.md` — all 8 phases checked
- `mcp/` — MCP server (180 tests)
- `skills/` — 5 skills (orchestrator + 4 sub-skills)
- `.claude-plugin/` — plugin manifests
- Memory: `project_plan_2026q2.md`

## Continuation prompt

```
Litrev plugin migration COMPLETE (Phases 1-8). 180 MCP tests pass, 12 tools, prefix unchanged.
Old directories deleted, backup at ~/.claude/skills/litrev-backup-20260403.tar.gz.

Next: Priority E (new sources — fetch_fulltext, search_scopus, search_wos).
New tools go in mcp/src/litrev_mcp/tools/.

Key files: ROADMAP.md (Priority E), mcp/, skills/.
Constraints: user manages all git operations. Always update memory files when state changes.
```
