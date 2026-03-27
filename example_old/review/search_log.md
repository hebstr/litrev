# Search Log

## Date
2026-03-27

## Research Question
Épidémiologie des scapulalgies et pathologies de la coiffe des rotateurs chez l'adulte : prévalence, incidence, facteurs de risque, et poids socio-économique.

## Databases Searched

### 1. PubMed/MEDLINE

**Query 1 (main):**
```
(("shoulder pain" OR "rotator cuff" OR "subacromial impingement" OR scapulalgia)
AND (epidemiology OR prevalence OR incidence OR "risk factor" OR "occupational disease"
OR socioeconomic OR cost OR "sick leave" OR "work disability" OR burden))
```
- Date filter: 2010–2026
- Sort: relevance
- Results: 5,012 total; top 80 retrieved

**Query 2 (French context):**
```
((scapulalgie OR "coiffe des rotateurs" OR "maladie professionnelle")
AND (epaule OR shoulder)
AND (France OR French))
```
- Date filter: 2010–2026
- Sort: relevance
- Results: 10 retrieved

### 2. Semantic Scholar

**Query:**
```
rotator cuff epidemiology prevalence incidence risk factors occupational
```
- Year filter: 2010–2026
- Status: FAILED (HTTP 429 — rate limited, 3 attempts)
- Results: 0

### 3. OpenAlex

**Query:**
```
shoulder pain rotator cuff epidemiology prevalence incidence risk factors socioeconomic
```
- Date filter: 2010-01-01 to 2026-12-31
- Sort: relevance_score descending
- Results: 256 total; top 50 retrieved

## Aggregation

| Source | Retrieved | After dedup |
|--------|-----------|-------------|
| PubMed (main) | 80 | 80 |
| PubMed (French) | 10 | 10 |
| OpenAlex | 50 | 50 |
| **Total** | **140** | **140** |

Deduplication method: exact PMID, exact DOI (case-insensitive), fuzzy title matching (SequenceMatcher > 0.85).

## Limitations

- Semantic Scholar was unavailable due to API rate limiting (no API key). This reduces database coverage from 3 to 2 active sources.
- PubMed retrieval was capped at 80 (main query) from 5,012 available results. The relevance sort prioritizes the most pertinent articles.
- OpenAlex retrieval was capped at 50 from 256 available results.
