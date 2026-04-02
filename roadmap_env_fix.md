# Roadmap: reliable API key delivery in litrev-search

## Problem

`litrev-search` fails 5/5 at using API keys (S2, NCBI, EMAIL).
Root cause: the skill prompt mixes two API access modes — MCP tools (S2) and direct WebFetch (PubMed, OpenAlex).
Claude follows the dominant pattern (WebFetch) and ignores the exception (MCP for S2).
Keys are correctly configured in `.mcp.json` and the MCP server receives them — the bug is 100% on the prompt/orchestration side.

## Fix principle

**Route everything through the MCP server.** Zero WebFetch calls to scientific APIs from litrev-search.

This eliminates:
- Prompt ambiguity (single pattern: call an MCP tool)
- `.mcp.json` reading by the skill (no longer needed — MCP manages its own keys)
- WebFetch bypass risk (WebFetch removed from allowed-tools for this skill)

The MCP server already has all required HTTP infrastructure (`http.py`: authenticated clients, rate limiting, retry, throttle for NCBI and S2).
Two tools are missing: `search_pubmed` and `search_openalex`.

## Steps

### 1. MCP: add `search_pubmed`

**File**: `litrev-mcp/src/litrev_mcp/tools/pubmed_search.py` (new)

Logic:
- Parameters: `query` (str), `date_start` (str, YYYY), `date_end` (str, YYYY), `limit` (int, default 200)
- Build esearch request → retrieve PMIDs
- Call esummary in batches (200/batch) → extract title, authors, year, DOI, journal, type
- Call efetch in batches → extract abstracts (reuse `pubmed.py:fetch_abstracts_from_pubmed`)
- Return normalized records (same schema as `search_s2`) + `has_api_key: bool`
- Rate limiting via existing `ncbi_params()` and `_ncbi_throttle()`

**Registration**: add `search_pubmed` in `server.py` with `_with_tips(result, "NCBI_API_KEY", "LITREV_EMAIL")`

**Scope**: ~80 lines. Most PubMed logic already exists in `http.py` and `pubmed.py`.

### 2. MCP: add `search_openalex`

**File**: `litrev-mcp/src/litrev_mcp/tools/openalex_search.py` (new)

Logic:
- Parameters: `query` (str), `year_start` (int), `year_end` (int), `limit` (int, default 50)
- Build OpenAlex URL `/works?search=...&filter=publication_year:...`
- Add `mailto=<LITREV_EMAIL>` if available (polite pool)
- Normalize records to same schema (source: "OpenAlex-search")
- Return records + `has_email: bool`

**Registration**: add `search_openalex` in `server.py` with `_with_tips(result, "LITREV_EMAIL")`

**Scope**: ~60 lines. `OA_CLIENT` and `request_with_retry` already exist in `http.py`.

### 3. Skill: rewrite search section of `litrev-search/SKILL.md`

Changes:
- **`allowed-tools`**: remove `WebFetch` and `WebSearch`, add `mcp__litrev-mcp__search_pubmed` and `mcp__litrev-mcp__search_openalex`
- **Step 0 — Pre-flight** (new): call `search_s2(query="test", limit=1)` → check `has_api_key: true`. If false → STOP.
- **Step 2 — Search databases**: rewrite so each database is an MCP call:
  - PubMed → `search_pubmed(query=..., date_start=..., date_end=..., limit=200)`
  - Semantic Scholar → `search_s2(query=..., year_start=..., year_end=..., limit=100)`
  - OpenAlex → `search_openalex(query=..., year_start=..., year_end=..., limit=50)`
- **Remove** all sections describing manual URL construction (esearch, esummary, efetch, api.openalex.org)
- **Keep** ClinicalTrials.gov and medRxiv as WebFetch (optional, no API key) — isolate in a clearly separated "Optional databases (direct HTTP)" section. If WebFetch is removed from allowed-tools, add it back ONLY for these optional databases or move them to MCP later.

### 4. Skill: update `litrev/SKILL.md` (orchestrator)

- Update `allowed-tools` to include the new MCP tools
- Remove any reference to reading `.mcp.json` for API keys
- Pre-flight lives in litrev-search, no need to duplicate it in the orchestrator

### 5. Cleanup

- Update `litrev-search/references/database_strategies.md` (remove `.mcp.json` reading instructions)
- Update memory files (`project_mcp_s2_env.md`, `feedback_s2_api_key_detection.md`) to reflect the fix
- Test with `example_v3`

## Out of scope

- No changes to `http.py` (HTTP infrastructure is solid)
- No changes to `run.sh` or `.mcp.json` (config is correct)
- No "hot reload" mechanism for keys — import-time capture is sufficient
- No `get_env` tool — no longer needed, keys stay in the MCP process

## Execution order

```
1. search_pubmed (MCP tool)     — standalone, testable alone
2. search_openalex (MCP tool)   — standalone, testable alone
3. litrev-search SKILL.md       — depends on 1 and 2
4. litrev SKILL.md              — depends on 3
5. cleanup + test               — depends on 4
```

Steps 1 and 2 can run in parallel.

## Expected outcome

After the fix, `litrev-search`:
- Has no WebFetch access for main databases
- Runs a mandatory MCP pre-flight check
- Uses 3 MCP tools (search_s2, search_pubmed, search_openalex) that manage their own keys
- Zero `.mcp.json` reads by the skill
- Zero prompt ambiguity
