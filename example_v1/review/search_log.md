# Search Log

## PubMed — Epidemiology

- **Date searched**: 2026-03-27
- **Date range**: 2010–2026
- **Query**: `("rotator cuff"[MeSH] OR "shoulder pain"[MeSH] OR "shoulder impingement syndrome"[MeSH] OR "scapulalgia"[tiab] OR "rotator cuff"[tiab] OR "shoulder pain"[tiab]) AND ("epidemiology"[MeSH] OR "prevalence"[tiab] OR "incidence"[tiab]) AND 2010:2026[DP]`
- **Results**: 2435
- **Retrieved**: 2000
- **Status**: SUCCESS

## PubMed — Risk factors

- **Date searched**: 2026-03-27
- **Date range**: 2010–2026
- **Query**: `("rotator cuff"[MeSH] OR "shoulder pain"[MeSH] OR "shoulder impingement syndrome"[MeSH] OR "scapulalgia"[tiab] OR "rotator cuff"[tiab]) AND ("risk factors"[MeSH] OR "risk factor"[tiab] OR "occupational diseases"[MeSH] OR "occupational"[tiab] OR "work-related"[tiab] OR "comorbidity"[MeSH]) AND 2010:2026[DP]`
- **Results**: 1291
- **Retrieved**: 1291
- **Status**: SUCCESS

## PubMed — Occupational disease

- **Date searched**: 2026-03-27
- **Date range**: 2010–2026
- **Query**: `("rotator cuff"[MeSH] OR "shoulder pain"[MeSH] OR "scapulalgia"[tiab]) AND ("occupational diseases"[MeSH] OR "workers compensation"[MeSH] OR "maladie professionnelle"[tiab] OR "occupational disease"[tiab]) AND 2010:2026[DP]`
- **Results**: 244
- **Retrieved**: 244
- **Status**: SUCCESS

## PubMed — Socioeconomic burden

- **Date searched**: 2026-03-27
- **Date range**: 2010–2026
- **Query**: `("rotator cuff"[MeSH] OR "shoulder pain"[MeSH] OR "scapulalgia"[tiab]) AND ("cost of illness"[MeSH] OR "sick leave"[MeSH] OR "absenteeism"[MeSH] OR "economic burden"[tiab] OR "socioeconomic"[tiab] OR "work disability"[tiab] OR "cost"[tiab]) AND 2010:2026[DP]`
- **Results**: 369
- **Retrieved**: 369
- **Status**: SUCCESS

## Semantic Scholar — Epidemiology

- **Date searched**: 2026-03-27
- **Date range**: 2010–2026
- **Query**: `rotator cuff shoulder pain prevalence incidence epidemiology`
- **Results**: 922
- **Retrieved**: 100
- **Status**: SUCCESS

## Semantic Scholar — Socioeconomic

- **Date searched**: 2026-03-27
- **Date range**: 2010–2026
- **Query**: `rotator cuff occupational disease economic burden sick leave`
- **Results**: 11
- **Retrieved**: 11
- **Status**: SUCCESS

## OpenAlex — Topical search (all queries)

- **Date searched**: 2026-03-27
- **Date range**: 2010–2026
- **Queries attempted**: 5 (epidemiology, risk factors, socioeconomic — two rounds with different filter syntax)
- **Results**: All queries returned off-topic results (top hits unrelated to shoulder/rotator cuff) or 0 results (due to deprecated `type:journal-article` filter)
- **Status**: DISCARDED — OpenAlex used for citation enrichment only
- **Action**: Citation counts enriched for 2778/3199 PubMed articles via OpenAlex DOI lookup

## Institutional databases

- **Scopus**: requires institutional access — ready-to-paste query prepared below
- **Web of Science**: requires institutional access — ready-to-paste query prepared below

### Scopus query (ready to paste)

```
TITLE-ABS-KEY("rotator cuff" OR "shoulder pain" OR "scapulalgia" OR "shoulder impingement") AND TITLE-ABS-KEY("prevalence" OR "incidence" OR "epidemiology" OR "risk factor" OR "occupational" OR "cost" OR "economic burden" OR "sick leave" OR "work disability") AND PUBYEAR > 2009 AND PUBYEAR < 2027 AND SUBJAREA(MEDI)
```

### Web of Science query (ready to paste)

```
TS=("rotator cuff" OR "shoulder pain" OR "scapulalgia" OR "shoulder impingement") AND TS=("prevalence" OR "incidence" OR "epidemiology" OR "risk factor" OR "occupational" OR "cost" OR "economic burden" OR "sick leave" OR "work disability") AND PY=(2010-2026)
```

## Summary

| Database | Queries | Succeeded | Failed | Total Results |
|----------|---------|-----------|--------|---------------|
| PubMed | 4 | 4 | 0 | 3321 |
| Semantic Scholar | 2 | 2 | 0 | 111 |
| OpenAlex (topical) | 5 | 0 | 5 (off-topic/API) | 0 |
| OpenAlex (enrichment) | — | — | — | 2778 enriched |
| **Total** | **11** | **6** | **5** | **3432** |

After deduplication: **3368 unique articles**

### Databases not searched (topical)

- OpenAlex: queries returned off-topic results; used for citation enrichment only (2778 articles enriched)
- Scopus: requires institutional access (query prepared above)
- Web of Science: requires institutional access (query prepared above)
- EMBASE: requires institutional access

