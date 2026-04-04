---
name: litrev-search
context: fork
description: Search medical and clinical databases for literature reviews. Queries PubMed/MEDLINE, Semantic Scholar, OpenAlex (and optionally ClinicalTrials.gov, medRxiv) via public APIs, aggregates and deduplicates results into normalized JSON, and produces a ranked markdown summary. Use whenever the user needs to search biomedical databases for a review, build a multi-database search strategy, or says things like "search the literature on [medical topic]", "find studies about [treatment]", "do a lit search on [topic]", "recherche bibliographique", "recherche biblio", "interroger PubMed/les bases", "interroger plusieurs bases", "chercher dans les bases", "cherche les articles sur [sujet médical]". Also triggers when the orchestrator skill (litrev) delegates its search phase. Do NOT trigger for: general web searches, non-medical database queries, searching code, fetching metadata for known articles (by PMID, DOI, or title — single or batch), post-processing existing search results (deduplication/ranking of an existing combined_results.json), writing methods sections for a review, bibliometric or scientometric analysis, or Google Scholar query refinement.
allowed-tools: Read Write Edit WebFetch mcp__litrev-mcp__search_pubmed mcp__litrev-mcp__search_s2 mcp__litrev-mcp__search_openalex mcp__litrev-mcp__deduplicate_results mcp__litrev-mcp__process_results mcp__litrev-mcp__import_corpus
---

# Literature Search for Medical Reviews

## Pre-loaded pipeline state

### Working directory
!`pwd`

### Review artifacts found
!`ls -1 review/ 2>/dev/null || echo "(no review/ directory yet)"`

### Protocol (if exists)
!`cat review/protocol.md 2>/dev/null || echo "(no protocol yet)"`

Search multiple medical databases, aggregate results into a normalized dataset, and produce a ranked summary table. This skill is one component of a literature review pipeline — it handles the search and aggregation phase only.

## Usage Modes

**Standalone**: the user asks directly to search databases. Handle the full workflow below, including asking for missing inputs.

**Orchestrated**: called by the `litrev` orchestrator skill. The orchestrator has already established the protocol (question, framework, criteria, databases) in Phase 1. Read the protocol from the conversation context and proceed to Step 1 without re-asking. If any required field is missing from the orchestrator's context, halt and return an error listing the missing fields — do not guess, and do not ask the user directly.

## Input Requirements

Before starting, confirm these are available (provided by the user or established by the orchestrator):

| Field | Required | Example |
|-------|----------|---------|
| Research question | Yes | "What is the effect of X on Y?" |
| Framework | Yes | PICO, PEO, or SPIDER with each component filled |
| Review type | Yes | systematic, scoping, narrative, meta-analysis, rapid |
| Date range | Yes | 2015–2026 |
| Databases | Yes | PubMed, Semantic Scholar, OpenAlex (minimum 3; minimum 2 for rapid) |
| Search concepts + synonyms | Yes | 2–4 concepts with MeSH terms and free-text variants |
| Inclusion/exclusion criteria | Yes | Study types, population, language, etc. |

If any required field is missing, ask the user before proceeding. Do not guess or fill in defaults for any required field.

## Output Files

All outputs go in `review/` at the project root (create the directory if it doesn't exist). Never place output files at the project root — always inside `review/`:

- **`review/combined_results.json`** — every article from every database, normalized to the schema in `references/json_schema.md`
- **`review/search_results.md`** — deduplicated, ranked markdown table with summary statistics
- **`review/search_log.md`** — full documentation of every search attempt (successes and failures)

## Workflow

### Step 0 — Pre-flight check

Before any search, verify that the MCP server is reachable and API keys are working:

Call `search_s2(query="test", limit=1)`. Check the response:
- If `has_api_key: true` and `status: "ok"` → proceed.
- If `has_api_key: false` or `status: "error"` → **STOP**. Tell the user: "The MCP server's S2 API key is not configured or not reaching the server. Check `.mcp.json` and restart Claude Code." Do NOT continue with degraded search.

### Step 1 — Prepare search queries

For each concept, build database-specific queries:

- **PubMed**: use MeSH terms + free-text `[tiab]` synonyms combined with OR, then AND across concepts. Add date range `[DP]` and publication type filters `[pt]` as needed. Read `references/database_strategies.md § PubMed/MEDLINE` for syntax.
- **Semantic Scholar**: construct plain-language queries from concept keywords. S2 doesn't support Boolean or field tags — use the most distinctive terms.
- **OpenAlex**: same as S2 — plain-language queries via the `search=` parameter.

In standalone mode, present the planned queries to the user and wait for approval before executing. If the user requests changes, revise the queries accordingly and re-present for approval. Repeat until approved. In orchestrated mode, log the queries in `search_log.md` and proceed without waiting.

**Institutional databases** (EMBASE, Scopus, Web of Science): these require institutional access and have no public API — they cannot be queried programmatically. Ask the user: "Do you have institutional access to EMBASE, Scopus, or Web of Science? If so, I'll prepare ready-to-paste queries for their web portals. You run them, export the results (RIS or CSV), and I'll import them with `import_corpus`."

If the user provides exported files, call `import_corpus(file_path=<path>, output_path="review/imported_<db>.json")`. The tool auto-detects Scopus CSV, Web of Science TSV, RIS, and BibTeX formats, and enriches sparse records with metadata from PubMed/CrossRef/OpenAlex. Then merge the imported records into `review/combined_results.json` during Step 3 (normalize and aggregate). Document the suggestion and outcome in `search_log.md` regardless of whether the user follows through.

### Step 2 — Execute searches

All three main databases are searched via MCP tools. The tools handle API keys, rate limiting, and response normalization internally. Do NOT use WebFetch to query PubMed, Semantic Scholar, or OpenAlex — always use the corresponding MCP tool.

#### PubMed/MEDLINE

Call the MCP tool `search_pubmed` for each PubMed query. The tool runs esearch → esummary → efetch internally and returns normalized records with abstracts.

Parameters:
- `query`: PubMed search query (MeSH terms + Boolean operators supported, e.g. `("rotator cuff"[MeSH] OR "shoulder pain"[MeSH]) AND "prevalence"[tiab]`)
- `date_start` / `date_end`: year filter in YYYY format (e.g. `"2015"`, `"2026"`)
- `limit`: max results (default 200)

The tool returns `has_api_key: bool` indicating whether `NCBI_API_KEY` is configured. Relay any `tips` to the user.

Run multiple queries if needed (one per concept facet). Collect all results, then combine.

#### Semantic Scholar

Call the MCP tool `search_s2` for each S2 query.

Parameters:
- `query`: plain-language keywords (no Boolean operators, no field tags)
- `year_start` / `year_end`: date range filter
- `fields_of_study`: `"Medicine"` (default)
- `limit`: `100` (max per query)

Execute queries one at a time. If any call returns `status: "error"` or `has_api_key: false`, **STOP** and alert the user.

#### OpenAlex

Call the MCP tool `search_openalex` for each OpenAlex query.

Parameters:
- `query`: short, focused query (2-3 key terms max — longer queries dilute relevance)
- `year_start` / `year_end`: date range filter
- `limit`: `50` (default)

OpenAlex does not return abstracts — these are fetched later via PubMed (Step 4 enrichment or `fetch_abstracts` during screening).

**Niche topics** (expected total results <100): use the most specific terms possible. After retrieving results, spot-check the first 10 titles — if more than 3 look off-topic, discard that query's results and rely on OpenAlex only for citation enrichment. Log discarded queries in `search_log.md`.

If the topic has multiple facets, run multiple short queries rather than one long one.

#### Optional databases (direct HTTP via WebFetch)

These databases have no API key requirements and are queried via WebFetch only when requested by the protocol.

**ClinicalTrials.gov** (for intervention reviews):
```
https://clinicaltrials.gov/api/v2/studies?query.cond=<condition>&query.intr=<intervention>&filter.overallStatus=COMPLETED&pageSize=50
```
Skip for epidemiology-only or scoping reviews unless the user requests it.

**medRxiv/bioRxiv** (for preprints):
```
https://api.medrxiv.org/details/medrxiv/<YYYY-MM-DD>/<YYYY-MM-DD>/<cursor>
```
No content-based search — filter locally by title/abstract keywords after fetching.

### Step 3 — Normalize and aggregate

Convert all results to the standard schema defined in `references/json_schema.md`. The example below shows the most common fields — populate all schema fields when the source data provides them (including `publication_type`, `relevance_score`, `type`, `url`):

```json
{
  "title": "...",
  "authors": ["LastName1 AB", "LastName2 CD"],
  "first_author": "LastName1",
  "year": "2023",
  "doi": "10.1234/example",
  "pmid": "12345678",
  "journal": "Full Journal Name",
  "volume": "12",
  "pages": "100-110",
  "abstract": "...",
  "source": "PubMed-search",
  "study_type": "meta-analysis",
  "citations": 42
}
```

Set `source` to the database of origin. Aggregate results in source-priority order: PubMed first, then Semantic Scholar, then OpenAlex. Save all results to `review/combined_results.json`.

Then call the MCP tool `deduplicate_results` to deduplicate by PMID/DOI/normalized title with field merging:
- `results_path`: `"review/combined_results.json"`
- `output_path`: `"review/combined_results.json"` (in-place)

The tool returns `before`, `after`, `removed`, and a per-method breakdown (`duplicates_by_pmid`, `duplicates_by_doi`, `duplicates_by_title`). Log all of these in `search_log.md` (see Step 6 template).

### Step 4 — Enrich citation counts

PubMed doesn't provide citation counts. After aggregation, enrich from OpenAlex using WebFetch with DOI or PMID lookup:

```
https://api.openalex.org/works?filter=doi:<doi>&select=id,cited_by_count
```

This is a simple unauthenticated GET — no API key required. If `LITREV_EMAIL` is available (check the `has_email` field from any prior `search_openalex` response), append `&mailto=<email>` for faster rate limits.

Batch enrichment: collect all DOIs missing citation counts, then loop through them with WebFetch. Update `citations` in `review/combined_results.json` in place.

This step matters because citation counts drive ranking and help prioritize articles for screening downstream.

### Step 5 — Deduplicate and rank

Generate `review/search_results.md` by calling the MCP tool `process_results`. Do not write the markdown file manually — the tool produces a standardized table that downstream skills expect.

Call `process_results` with:
- `results_path`: `"review/combined_results.json"`
- `output_format`: `"markdown"`
- `output_path`: `"review/search_results.md"`
- `rank_by`: `"citations"`
- `deduplicate`: `true`
- `top_n`: `20`

Optional parameters: `rank_by` (`"citations"`, `"year"`, `"relevance"`), `year_start`/`year_end` (int), `study_types` (list of strings, e.g. `["rct", "cohort"]`), `output_format` (`"json"`, `"markdown"`, `"bibtex"`, `"ris"`).

If most records have `citations: 0` after enrichment (enrichment failed or articles too recent), fall back to `rank_by: "year"` and note the enrichment failure in `search_log.md`.

### Step 5b — Grey literature checklist

After database searches, prompt the user to check grey literature and guideline sources relevant to the review topic. This step is manual — the user searches these sources themselves and provides any additional references.

Present the checklist as a numbered list adapted to the review domain:

**Clinical / therapeutic reviews:**
- HAS (Haute Autorité de Santé) — recommandations, avis de la commission de la transparence
- NICE (National Institute for Health and Care Excellence) — guidelines, technology appraisals
- WHO — guidelines, technical reports
- Cochrane Library — Cochrane Reviews (if not already captured by database search)
- ClinicalTrials.gov / ICTRP — ongoing or unpublished trials

**Occupational health / epidemiology:**
- INRS (Institut National de Recherche et de Sécurité) — dossiers médico-techniques, fiches
- ANSES — avis et rapports
- Relevant learned societies (e.g., SOFCOT, SFR, SFMT) — consensus statements, guidelines

**General:**
- Institutional reports, theses, conference proceedings relevant to the topic

Ask the user: "Have you checked these sources? If you found relevant references, provide them (title, authors, year, URL) and I'll add them to `combined_results.json` with `source: "grey_literature"`."

If the user provides references, add them to `combined_results.json` with `source: "grey_literature"` and `search_db: "manual"`. If the user declines or has no additions, document it in `search_log.md` and proceed.

### Step 6 — Document everything

Finalize `review/search_log.md`. The log should be written incrementally throughout Steps 1–5 (each query logged immediately after execution), so that partial results survive if the process fails mid-run. This step adds the summary table and any final notes:

```markdown
## PubMed — Query 1 (Epidemiology)

- **Date searched**: 2026-03-22
- **Date range**: 2010–2026
- **Query**: `("rotator cuff"[MeSH] OR "shoulder pain"[MeSH]) AND ("prevalence"[tiab]) AND 2010:2026[DP]`
- **Filters**: Systematic Review [pt], Meta-Analysis [pt]
- **Results**: 166
- **Status**: SUCCESS

## Semantic Scholar — Query 2

- **Date searched**: 2026-03-22
- **Query**: `rotator cuff comorbidity diabetes outcome`
- **Results**: 0
- **Status**: FAILED (HTTP 429 — rate limited, retry also failed)
- **Action**: Skipped
```

End with a summary table:

```markdown
## Summary

| Database | Queries | Succeeded | Failed | Total Results |
|----------|---------|-----------|--------|---------------|
| PubMed | 4 | 4 | 0 | 433 |
| Semantic Scholar | 3 | 1 | 2 | 50 |
| OpenAlex | 2 | 2 | 0 | 87 |
| **Total** | **9** | **7** | **2** | **570** |

After deduplication: **458 unique articles** (112 duplicates removed: 67 by PMID, 31 by DOI, 14 by title)

### Grey literature
- Sources checked by user: [list or "none"]
- References added: [count or 0]

### Databases not searched
- EMBASE: requires institutional access (suggested to user)
```

## Completion Criteria

The search is complete when:
1. `review/combined_results.json` exists with all aggregated results
2. `review/search_results.md` exists with deduplicated, ranked results and summary statistics
3. `review/search_log.md` documents every search attempt
4. At least the minimum number of databases contributed topical search results (3 for systematic/scoping/meta-analysis, 2 for narrative/rapid). A database used only for citation enrichment (e.g., OpenAlex in Step 4) does not count toward this minimum.
5. Summary statistics have been reviewed (total by source, by year, by study type)

If fewer databases succeeded than required, alert the user with the failure details and propose options: (a) retry the failed database, (b) substitute with another available database, (c) proceed with fewer databases and document the limitation, (d) downgrade the review type (e.g., systematic → rapid) to lower the threshold.

## Reference Files

Read these as needed:

- `references/database_strategies.md` — detailed search syntax for each database
- `references/json_schema.md` — normalized JSON schema for `combined_results.json`
