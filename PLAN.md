# Litrev — Plan

## Current objective

Convert litrev from a personal skill to a proper Claude Code plugin, then resume the validation run (example-4).

## Steps

| # | Step | Status |
|---|------|--------|
| 1 | Prepare workspace/example-4: new topic, PROMPT.md, CONTEXT files | done |
| 2 | Prepare a BibTeX or PMID list file to test Phase 2b (import_corpus) | done |
| P1 | Plugin conversion: move litrev to `~/.claude/plugins/marketplaces/litrev/` | todo |
| P2 | Plugin conversion: create `marketplace.json`, fix `plugin.json` paths | todo |
| P3 | Plugin conversion: move MCP config from global `.mcp.json` to plugin-local `.mcp.json` | todo |
| P4 | Plugin conversion: register in `settings.json` (`enabledPlugins`) | todo |
| P5 | Plugin conversion: verify skill discovery (all 5 skills visible) + MCP connection | todo |
| P6 | Plugin conversion: update PLAN.md paths, DEFERRED.md, memory files for new root | todo |
| 3 | Run full pipeline end-to-end (Phases 1-9) in example-4 | todo |
| 4 | Triage issues found during run | todo |
| 5 | Fix issues (if any) | todo |
| 6 | F26: design + implement orchestrator evals | todo |
| 7 | F27: design + implement synthesize evals | todo |

## Dependencies

- Steps 1-2: done
- P1 → P2 → P3 → P4 → P5 (sequential — each depends on the previous)
- P6 depends on P1 (new root path known)
- Step 3 depends on P5 (plugin functional)
- Step 4 depends on 3; step 5 depends on 4
- Steps 6-7 depend on 3

## Plugin conversion — design decisions

**Target structure** (modeled on Ouroboros plugin):
```
~/.claude/plugins/marketplaces/litrev/
├── .claude-plugin/
│   ├── plugin.json            ← already exists, fix relative paths
│   └── marketplace.json       ← new: marketplace registration
├── .mcp.json                  ← move from .claude-plugin/.mcp.json to root level
├── skills/
│   ├── litrev/SKILL.md        ← orchestrator
│   ├── litrev-search/SKILL.md
│   ├── litrev-screen/SKILL.md
│   ├── litrev-extract/SKILL.md
│   └── litrev-synthesize/SKILL.md
├── mcp/                       ← MCP server (Python, uv)
├── workspace/                 ← example runs (gitignored outputs)
├── PLAN.md
├── DEFERRED.md
└── README.md
```

**Key changes from current layout:**
- Root moves from `~/.claude/skills/litrev/` to `~/.claude/plugins/marketplaces/litrev/`
- `.mcp.json` at plugin root (not inside `.claude-plugin/`) — matches Ouroboros pattern
- MCP removed from global `~/.claude/.mcp.json` (loaded via plugin mechanism instead)
- `enabledPlugins` gets `"litrev@litrev": true`
- `extraKnownMarketplaces` not needed (local install, not from GitHub)
- All internal relative paths in SKILL.md files remain valid (skills/ structure unchanged)
- Memory project path updates: `~/.claude/projects/-home-julien--claude-skills-litrev/` may need a new project context path

**Risks:**
- Session restart required after step P4 for Claude Code to discover the plugin
- Memory files reference old path — need P6 cleanup
- Global `.mcp.json` env vars (API keys) must transfer to plugin `.mcp.json`

## Resume context

Feature F complete (2026-04-04). E1 done. 338 tests, 15 tools.
Steps 1-2 done (2026-04-04): example-4 prepared (topic: postoperative delirium prediction in elderly).
During example-4 run attempt (2026-04-04): discovered sub-skills not discoverable by Skill tool — litrev is structured as a plugin but not registered as one. Plugin conversion required before resuming.
Partial search results exist in workspace/example-4/review/ (pubmed_q1.json, s2_q1.json) — will be discarded and re-run after plugin conversion.

## Reference files

- `DEFERRED.md` — backlog items not on the current plan
- `mcp/` — MCP server source and tests
- `skills/` — 5 skills (orchestrator + 4 sub-skills)
