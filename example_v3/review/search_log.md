# Search Log — Subacromial Corticosteroid Injections for Shoulder Pain

**Date**: 2026-04-02
**Review type**: Scoping review
**Date range**: 2010–2026

---

## PubMed — Query 1 (Main: Concept 1 AND Concept 2)

- **Date searched**: 2026-04-02
- **Date range**: 2010–2026
- **Query**: `("rotator cuff"[MeSH] OR "shoulder pain"[MeSH] OR "shoulder impingement syndrome"[MeSH] OR "subacromial pain syndrome"[tiab] OR "scapulalgia"[tiab] OR "rotator cuff tendinopathy"[tiab] OR "subacromial impingement"[tiab]) AND ("corticosteroid injection"[tiab] OR "steroid injection"[tiab] OR "subacromial injection"[tiab] OR "cortisone injection"[tiab] OR "glucocorticoid injection"[tiab] OR "adrenal cortex hormones"[MeSH] AND "injections"[MeSH]) AND 2010:2026[DP]`
- **Filters**: None (broad scoping query)
- **Results**: 235
- **Status**: SUCCESS

## PubMed — Query 2 (Care pathway / Surgical outcomes)

- **Date searched**: 2026-04-02
- **Date range**: 2010–2026
- **Query**: `("rotator cuff"[MeSH] OR "shoulder pain"[MeSH]) AND ("subacromial injection"[tiab] OR "corticosteroid injection"[tiab] OR "steroid injection"[tiab]) AND ("rotator cuff repair"[tiab] OR "arthroscopic surgery"[tiab] OR "preoperative"[tiab] OR "surgical outcome"[tiab] OR "time to surgery"[tiab] OR "conservative management"[tiab] OR "care pathway"[tiab] OR "stepped care"[tiab]) AND 2010:2026[DP]`
- **Results**: 34
- **Status**: SUCCESS
- **Note**: High overlap with Query 1; 26 new PMIDs added

## PubMed — Abstract Retrieval

- **Date searched**: 2026-04-02
- **Method**: efetch.fcgi in batches of 200
- **Total PMIDs**: 255 unique
- **Abstracts retrieved**: 223/226 (after exclusion filtering)
- **Status**: SUCCESS

## PubMed — Post-retrieval Filtering

- **Excluded**: 29 articles (case reports, editorials, letters, comments, animal/cadaveric studies, off-topic articles outside shoulder scope, articles published before 2010)
- **Retained**: 226 articles

---

## Semantic Scholar — Query 1 (Efficacy)

- **Date searched**: 2026-04-02
- **Query**: `subacromial corticosteroid injection shoulder pain efficacy`
- **Year filter**: 2010–2026
- **Fields of study**: Medicine
- **Results**: 100 (of 3390 total)
- **Status**: SUCCESS (via WebFetch; direct API re-fetch returned HTTP 429)
- **Note**: Only first 100 results retrieved due to API pagination limits

## Semantic Scholar — Query 2 (Care pathway)

- **Date searched**: 2026-04-02
- **Query**: `corticosteroid injection rotator cuff repair preoperative outcome`
- **Results**: 0
- **Status**: FAILED (HTTP 429 — rate limited without API key)
- **Action**: Skipped; S2 Query 1 already provided substantial coverage

## Semantic Scholar — Rate Limiting Note

S2_API_KEY not configured. Rate limiting is aggressive (1 req/s without key). Only 1 of 2 queries succeeded. This is expected behavior per the skill documentation.

---

## OpenAlex — Query 1 (Subacromial injection)

- **Date searched**: 2026-04-02
- **Query**: `subacromial corticosteroid injection shoulder impingement`
- **Date filter**: 2010–2026
- **Total in OpenAlex**: 1565
- **Results retrieved**: 25
- **Relevance check**: 5/10 first titles matched shoulder keywords — borderline, kept with title-based filtering
- **After relevance filtering**: 13 articles retained
- **Status**: SUCCESS

## OpenAlex — Query 2 (Surgical outcomes)

- **Date searched**: 2026-04-02
- **Query**: `rotator cuff steroid injection surgical outcome preoperative`
- **Date filter**: 2010–2026
- **Total in OpenAlex**: 770
- **Results retrieved**: 25
- **Relevance check**: 4/10 first titles matched shoulder keywords — borderline, kept with title-based filtering
- **After relevance filtering**: 8 articles retained
- **Status**: SUCCESS

## OpenAlex — Citation Enrichment

- **Date searched**: 2026-04-02
- **Method**: Batch DOI lookup via `filter=doi:<pipe-separated-dois>&select=id,doi,cited_by_count`
- **Articles needing enrichment**: 206
- **Successfully enriched**: 204
- **Failed**: 2 (DOI not found in OpenAlex)
- **Status**: SUCCESS

---

## Institutional Databases — Not Searched

EMBASE, Scopus, Web of Science, and Cochrane CENTRAL require institutional access and cannot be queried via public API. The user was not asked about institutional access (orchestrated mode). If institutional access is available, ready-to-paste queries can be prepared for:

- **EMBASE (Ovid)**: `exp shoulder pain/ OR exp rotator cuff/ AND (corticosteroid injection.tw. OR steroid injection.tw. OR subacromial injection.tw.) AND limit to yr="2010-2026"`
- **Scopus**: `TITLE-ABS-KEY("subacromial" AND "corticosteroid injection") AND PUBYEAR > 2009 AND SUBJAREA(MEDI)`

EMBASE would likely add 30-40% unique content over PubMed alone.

---

## Deduplication

- **Method**: MCP tool `deduplicate_results` (PMID/DOI/normalized title matching with field merging)
- **Before**: 275 articles
- **After**: 264 unique articles
- **Duplicates removed**: 11

---

## Summary

| Database | Queries | Succeeded | Failed | Total Results |
|----------|---------|-----------|--------|---------------|
| PubMed | 2 | 2 | 0 | 226 |
| Semantic Scholar | 2 | 1 | 1 | 28 |
| OpenAlex | 2 | 2 | 0 | 21 |
| **Total** | **6** | **5** | **1** | **275** |

After deduplication: **264 unique articles**

### Citation enrichment

- Articles with citation count > 0: 239/264 (90.5%)
- Average citations: 54.3
- Total citations across corpus: 12,966
- Ranking method: by citation count (sufficient enrichment coverage)

### Databases not searched

- EMBASE: requires institutional access (queries can be prepared on request)
- Scopus: requires institutional access
- Web of Science: requires institutional access
- Cochrane CENTRAL: requires institutional access
- ClinicalTrials.gov: not searched (scoping review, not intervention-focused trial registry search)
- medRxiv/bioRxiv: not searched (preprint coverage deemed low-priority for this established topic)

### Database minimum check

Scoping review requires minimum 3 databases. All 3 planned databases (PubMed, Semantic Scholar, OpenAlex) contributed topical search results. Requirement met.
