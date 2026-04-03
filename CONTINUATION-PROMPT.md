# Session handoff — litrev plugin migration: Phases 1-7 DONE

## Context
Plugin migration of the `litrev` skill suite. Consolidated 6 standalone components (orchestrator, 4 sub-skills, 1 Python MCP server) into a single plugin under `~/.claude/skills/litrev/`. Phases 1-7 of MIGRATION_PLAN.md complete. MCP server verified working from new location (12 tools, prefix unchanged). 180 tests passing. Deep consistency scan: 0 issues.

## What was done (Phases 1-7)

1. **Phase 1**: Created `.claude-plugin/` (marketplace.json, plugin.json, .mcp.json). Moved orchestrator into `skills/litrev/` (SKILL.md, agents/, evals/, example_v1-v3/, PROMPT_RECOS.md).
2. **Phase 2**: Copied 4 sub-skills into `skills/` (litrev-search, litrev-screen, litrev-extract, litrev-synthesize). Checksums verified. workspace/ excluded.
3. **Phase 3**: Absorbed litrev-mcp into `mcp/` (src/, tests/, docs/, pyproject.toml, uv.lock). Consolidated DEFERRED.md. 180 tests passed.
4. **Phase 4**: Fixed all paths in SKILL.md files (absolute → relative) and tracking docs (litrev-mcp/ → mcp/, litrev-xxx/ → skills/litrev-xxx/).
5. **Phase 5**: Merged .gitignore (root litrev + litrev-mcp).
6. **Phase 6**: Updated `~/.claude/.mcp.json` to use `uv run --directory /home/julien/.claude/skills/litrev/mcp litrev-mcp`.
7. **Phase 7**: 180 tests pass, skill names unchanged, MCP tools accessible (prefix `mcp__litrev-mcp__*` preserved), deep scan 0 issues.

## What remains

### Immediate: Phase 8 — Cleanup
Delete the 5 old standalone directories (backup exists at `~/.claude/skills/litrev-backup-20260403.tar.gz`, 16 MB):
- `~/.claude/skills/litrev-search/`
- `~/.claude/skills/litrev-screen/`
- `~/.claude/skills/litrev-extract/`
- `~/.claude/skills/litrev-synthesize/`
- `~/.claude/skills/litrev-mcp/`

Then 3 smoke tests:
- `/litrev-screen` standalone: verify `references/screening_criteria.md` resolution
- `/litrev-synthesize` standalone: verify `assets/review_template.md` resolution
- `/litrev` orchestrator: verify sub-skill delegation

### After migration: Priority E — New source integrations
- E1: fetch_fulltext (DOI → full text via Unpaywall/PMC/S2/CORE/Sci-Hub cascade)
- E2: search_scopus (api.elsevier.com)
- E3: search_wos (api.clarivate.com)
- E4: EMBASE (deferred — no public API)

### DEFERRED items
- FN-3/GAP-3: Import path for pre-existing corpus
- Umbrella review workflow
- Unit tests for 5/10 MCP tool modules
- Edge-case evals (F24-F27)

## Key files
- `MIGRATION_PLAN.md` — canonical plan, Phases 1-7 checked, Phase 8 pending
- `ROADMAP.md` — all priorities, execution sequence
- `mcp/` — MCP server (180 tests)
- `skills/` — 5 skills (orchestrator + 4 sub-skills)
- `.claude-plugin/` — plugin manifests
- Memory: `project_plan_2026q2.md` (step 10 = migration, Phases 1-7 done)

## Continuation prompt

```
Litrev plugin migration Phases 1-7 DONE and committed. 180 MCP tests pass, 12 tools accessible, prefix unchanged.

Next: Phase 8 — delete old standalone directories:
  rm -rf ~/.claude/skills/litrev-{search,screen,extract,synthesize} ~/.claude/skills/litrev-mcp
Backup: ~/.claude/skills/litrev-backup-20260403.tar.gz

Then 3 smoke tests: /litrev-screen, /litrev-synthesize, /litrev standalone invocation.

After migration: Priority E (new sources — fetch_fulltext, search_scopus, search_wos).

Key files: MIGRATION_PLAN.md (Phase 8 checkboxes), ROADMAP.md, mcp/, skills/.
Constraints: user manages all git operations. Always update memory files when state changes.
```
