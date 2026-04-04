# Litrev — Plan

## Current objective

Validation run (example-4) — end-to-end test on a new topic to validate Feature F (import_corpus), E1 (fetch_fulltext/get_section), and the 15-tool pipeline before designing evals.

## Steps

| # | Step | Status |
|---|------|--------|
| 1 | Prepare workspace/example-4: new topic, PROMPT.md, CONTEXT files | done |
| 2 | Prepare a BibTeX or PMID list file to test Phase 2b (import_corpus) | done |
| 3 | Run full pipeline end-to-end (Phases 1-9) | todo |
| 4 | Triage issues found during run | todo |
| 5 | Fix issues (if any) | todo |
| 6 | F26: design + implement orchestrator evals | todo |
| 7 | F27: design + implement synthesize evals | todo |

## Dependencies

- Steps 1-2 are independent (parallelisable)
- Step 3 depends on 1 + 2
- Step 4 depends on 3
- Step 5 depends on 4
- Steps 6-7 depend on 3 (run informs eval design) but not on 5

## Design decisions

- New topic (not reused from example-1/2/3) to avoid bias
- Phase 2b tested with a real file (BibTeX or PMIDs) to validate import_corpus integration
- Run produces workspace/example-4/ as reference output and eval fixture material

## Resume context

Feature F complete (2026-04-04). E1 done. 338 tests, 15 tools.
Sync-files --deep done (2026-04-04): mcp/README.md and orchestrator allowed-tools fixed.
Steps 1-2 done (2026-04-04): example-4 prepared (topic: postoperative delirium prediction in elderly).
Restructured: example_v* moved from skills/litrev/ to workspace/example-{1,2,3}, gitignore updated (workspace/iteration* only).
Settings: workspace/example-4/.claude/settings.local.json with glob MCP permissions.
Next: step 3 — run full pipeline end-to-end in workspace/example-4/.

## Reference files

- `DEFERRED.md` — backlog items not on the current plan
- `mcp/` — MCP server source and tests
- `skills/` — 5 skills (orchestrator + 4 sub-skills)
