# Litrev — Plan

## Current objective

Feature F: `import_corpus` — allow users to bring their own articles (BibTeX, RIS, CSV Scopus/WoS, PMIDs, DOIs) into the pipeline alongside API search results.

## Steps

| # | Step | Status |
|---|------|--------|
| 1 | F1: `lib/parsers.py` — 6 format parsers + auto-detect | todo |
| 2 | F2: `tests/test_parsers.py` — unit tests for all parsers | todo |
| 3 | F3: `lib/enrich.py` — metadata enrichment (PubMed, CrossRef, OpenAlex) | todo |
| 4 | F4: `tools/import_corpus.py` — MCP tool (parse → enrich → write JSON) | todo |
| 5 | F5: `tests/test_import_corpus.py` — integration tests | todo |
| 6 | F6: `server.py` — register `import_corpus` tool | todo |
| 7 | F7: SKILL.md updates — orchestrator Phase 2b + search sub-skill | todo |

## Dependencies

- F1 and F3 are independent (parallelisable)
- F2 depends on F1
- F4 depends on F1 + F3
- F5 depends on F4
- F6 depends on F4
- F7 depends on F6

## Design decisions

- **6 formats**: BibTeX, RIS, CSV Scopus, CSV WoS (tab-separated), PMID list, DOI list
- **Auto-detect**: heuristic on file content (leading `@` → BibTeX, `TY  -` → RIS, etc.)
- **Parsers are pure functions** (str → list[dict]) — no I/O, independently testable
- **Enrichment**: sparse inputs (bare PMIDs/DOIs) get metadata via PubMed esummary/efetch + CrossRef; complete inputs (BibTeX/RIS) only get missing abstracts + citation counts
- **No dedup in tool**: import appends to `combined_results.json`; dedup is handled by existing `deduplicate_results` tool
- **Pipeline integration**: Phase 2a (search) + Phase 2b (import, optional) → dedup → Gate 2 (unchanged)

## Resume context

E1 done (2026-04-04). E2/E3/E4 deferred. 288 tests pass, 14 tools.
Feature F started 2026-04-04.

## Reference files

- `DEFERRED.md` — backlog items not on the current plan
- `mcp/` — MCP server source and tests
- `skills/` — 5 skills (orchestrator + 4 sub-skills)
