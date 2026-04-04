# Litrev — Plan

## Current objective

Run the validation pipeline end-to-end in example-4, then design orchestrator and synthesize evals (F26-F27).

## Steps

| # | Step | Status |
|---|------|--------|
| 1 | Prepare workspace/example-4: new topic, PROMPT.md, CONTEXT files | done |
| 2 | Prepare a BibTeX or PMID list file to test Phase 2b (import_corpus) | done |
| P1 | Plugin conversion: move repo to `~/.claude/plugins/marketplaces/litrev/` | done |
| P2 | Plugin conversion: `.mcp.json` at plugin root with env vars, global entry cleared | done |
| P3 | Plugin conversion: register `"litrev@litrev": true` in `settings.json` | done |
| P4 | Plugin conversion: verify skill discovery + MCP connection (requires restart) | done |
| P5 | Plugin conversion: migrate memory to new project context path, remove symlink | deferred |
| 3 | Run full pipeline end-to-end (Phases 1-9) in external research project (not example-4) | todo |
| 4 | Triage issues found during run | todo |
| 5 | Fix issues (if any) | todo |
| 6 | F26: design + implement orchestrator evals | todo |
| 7 | F27: design + implement synthesize evals | todo |

## Dependencies

- Steps 1-2: done
- P1 → P2 → P3 (sequential — each depends on the previous)
- P4 depends on P3 + session restart
- P5 deferred to a future session (symlink keeps current session functional)
- Step 3 depends on P4 (plugin functional)
- Step 4 depends on 3; step 5 depends on 4
- Steps 6-7 depend on 3

## Plugin conversion — design decisions

**Approach: symlink bridge (option B)**

1. Move repo to `~/.claude/plugins/marketplaces/litrev/`
2. Symlink `~/.claude/skills/litrev → ~/.claude/plugins/marketplaces/litrev/` (session continuity)
3. Move `.claude-plugin/.mcp.json` to plugin root, add env vars (S2_API_KEY, NCBI_API_KEY, LITREV_EMAIL)
4. Remove `litrev-mcp` from global `~/.claude/.mcp.json`
5. Register `"litrev@litrev": true` in `settings.json`
6. Session restart → verify skill discovery + MCP
7. (Later) Migrate memory to new project context path, remove symlink

**Risks:**
- Session restart required after P3 for Claude Code to discover the plugin
- Symlink keeps old project context path functional until P5 migration

## Resume context

Feature F complete (2026-04-04). E1 done. 338 tests, 15 tools.
Steps 1-2 done (2026-04-04): example-4 prepared (topic: postoperative delirium prediction in elderly).
Plugin conversion P1-P3 done (2026-04-04): repo at `~/.claude/plugins/marketplaces/litrev/`, `.mcp.json` with env vars at root, registered in settings.json, global `.mcp.json` cleared.
Symlink at old path NOT created — Bash was unavailable (sandbox CWD mismatch). Not critical: old path only needed for memory project context.
P4 verified (2026-04-04): 5 skills discovered, MCP tools connected. Plugin conversion complete.
Next: step 3 — run full pipeline end-to-end in external research project (real conditions, single MCP instance).
Testing moved out of workspace/example-4/ to avoid double MCP instance issue when working inside the plugin repo.
PROMPT.md, CONTEXT.md, and import_corpus.bib to be copied to the research project.

## Reference files

- `DEFERRED.md` — backlog items not on the current plan
- `mcp/` — MCP server source and tests
- `skills/` — 5 skills (orchestrator + 4 sub-skills)
