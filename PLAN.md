# Litrev — Plan

## Current objective

Priority E: New source integrations (fetch_fulltext, search_scopus, search_wos)

## Steps

| # | Step | Status |
|---|------|--------|
| 1 | E1: `fetch_fulltext` — DOI to full text via Unpaywall/PMC/S2/CORE/Sci-Hub cascade | todo |
| 2 | E2: `search_scopus` — Elsevier API, dedup-compatible output | todo |
| 3 | E3: `search_wos` — Clarivate Starter API (no abstracts) | todo |
| 4 | E4: EMBASE — deferred (no public API) | deferred |

New tools land in `mcp/src/litrev_mcp/tools/`.

## Resume context

Migration complete (2026-04-03). Priorities A-F all done. 180 MCP tests pass, 12 tools, plugin structure verified.
No blockers. No decisions pending.

## Reference files

- `ROADMAP.md` — full history of priorities A-F (archive)
- `DEFERRED.md` — backlog items not on the current plan
- `mcp/` — MCP server source and tests
- `skills/` — 5 skills (orchestrator + 4 sub-skills)
