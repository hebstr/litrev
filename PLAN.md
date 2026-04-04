# Litrev — Plan

## Current objective

Priority E complete. Awaiting next objective.

## Steps

| # | Step | Status |
|---|------|--------|
| 1 | E1: `fetch_fulltext` + `get_section` — PMC/Unpaywall/S2 cascade | done |
| 2 | E2: `search_scopus` | deferred |
| 3 | E3: `search_wos` | deferred |
| 4 | E4: EMBASE | deferred |

## Resume context

E1 done (2026-04-04). E2/E3/E4 deferred (2026-04-04): require institutional API keys, marginal value over existing PubMed + OpenAlex + S2 coverage for medical reviews.
Unit tests added for 5 previously untested MCP modules (2026-04-04): abstracts, openalex_search, pubmed_search, s2_search, snowball. 288 tests pass, 14 tools.
No blockers. No active steps.

## Reference files

- `DEFERRED.md` — backlog items not on the current plan
- `mcp/` — MCP server source and tests
- `skills/` — 5 skills (orchestrator + 4 sub-skills)
