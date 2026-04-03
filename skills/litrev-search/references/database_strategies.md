# Database Search Strategies

Reference documentation for database query syntax. All main database searches (PubMed, Semantic Scholar, OpenAlex) are executed via MCP tools (`search_pubmed`, `search_s2`, `search_openalex`) — do not call these APIs manually with WebFetch. This file documents the query syntax each tool accepts.

## Table of Contents

1. [PubMed/MEDLINE](#pubmedmedline)
2. [Semantic Scholar](#semantic-scholar)
3. [OpenAlex](#openalex)
4. [ClinicalTrials.gov](#clinicaltrialsgov)
5. [medRxiv/bioRxiv](#medrxivbiorxiv)
6. [EMBASE (Ovid)](#embase-ovid) — institutional access
7. [Cochrane CENTRAL](#cochrane-central) — institutional access
8. [Scopus](#scopus) — institutional access
9. [Web of Science](#web-of-science) — institutional access
10. [CINAHL](#cinahl) — institutional access

---

## PubMed/MEDLINE

### API: Entrez E-utilities

**Base URL**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

**Endpoints**:
- `esearch.fcgi` — search and get PMIDs
- `esummary.fcgi` — article metadata (no abstracts, no citation counts)
- `efetch.fcgi` — full records including abstracts (XML)

### Search syntax

#### MeSH terms
- `"rotator cuff"[MeSH]` — exploded by default (includes narrower terms)
- `"rotator cuff"[MeSH:NoExp]` — exact term only
- `"rotator cuff/surgery"[MeSH]` — MeSH with subheading

#### Field tags
- `[tiab]` — title + abstract
- `[ti]` — title only
- `[au]` — author
- `[ta]` — journal abbreviation
- `[DP]` — date of publication (format: `2010:2026`)
- `[pt]` — publication type
- `[la]` — language

#### Publication types
- `"systematic review"[pt]`
- `"meta-analysis"[pt]`
- `"review"[pt]`
- `"randomized controlled trial"[pt]`
- `"clinical trial"[pt]`
- `"observational study"[pt]`

#### Boolean operators
- AND, OR, NOT (uppercase)
- Parentheses for grouping

#### Wildcards
- `inject*` matches injection, injections, injectable

### Example query
```
("rotator cuff"[MeSH] OR "shoulder pain"[MeSH] OR "scapulalgia"[tiab])
AND ("epidemiology"[MeSH] OR "prevalence"[tiab] OR "incidence"[tiab])
AND ("systematic review"[pt] OR "meta-analysis"[pt])
AND 2010:2026[DP]
```

### esummary response parsing

The JSON response has quirks that have caused bugs:

```python
data = response.json()
result = data["result"]
uids = result["uids"]  # list of PMID strings

for uid in uids:
    info = result[uid]  # dict — but check isinstance(info, dict)

    # pubtype is a list of STRINGS, not dicts
    pub_types = info["pubtype"]  # ["Journal Article", "Review"]

    # authors is a list of dicts
    authors = [a["name"] for a in info["authors"] if isinstance(a, dict)]

    # DOI is in articleids
    doi = ""
    for aid in info.get("articleids", []):
        if isinstance(aid, dict) and aid.get("idtype") == "doi":
            doi = aid["value"]
            break

    # Citation counts are NOT available via esummary
```

### Rate limits
- Without API key: 3 requests/second (minimum delay: 0.4s)
- With API key (`&api_key=...`): 10 requests/second (minimum delay: 0.15s)
- API key is managed by the MCP server (`search_pubmed` tool) — do not read or inject it manually

---

## Semantic Scholar

### API: Academic Graph API v1

**Base URL**: `https://api.semanticscholar.org/graph/v1/`

### Paper search

```
GET /paper/search?query=<terms>&year=<start>-<end>&fieldsOfStudy=Medicine&fields=title,authors,year,citationCount,journal,externalIds,abstract&limit=100
```

- `query`: plain-language terms (no Boolean, no field tags)
- `year`: range filter (e.g., `2010-2026`)
- `fieldsOfStudy`: `Medicine`, `Biology`, etc.
- `fields`: comma-separated list of fields to return
- `limit`: max 100 per request
- `offset`: for pagination

### Rate limits — CRITICAL

**Without API key: 1 request per second.** HTTP 429 returned immediately on violation.

1. Execute requests **sequentially** — never in parallel
2. Wait **≥1.5 seconds** between requests
3. On 429: wait 5 seconds, retry once, then log failure and skip

### Extracting identifiers

```python
external_ids = paper.get("externalIds", {})
doi = external_ids.get("DOI", "")
pmid = external_ids.get("PubMed", "")
```

---

## OpenAlex

### API: REST

**Base URL**: `https://api.openalex.org/`

### Searching works

```
GET /works?search=<query>&filter=publication_year:<start>-<end>,type:journal-article&sort=cited_by_count:desc&per_page=50
```

**CRITICAL syntax rules** (caused complete failure in real-world usage):
- Use `search=` for query text — NOT `filter=default.search:`
- Do NOT use `select=` on search queries — truncates response fields
- URL-encode spaces as `%20`
- Keep queries **short** (2-3 key terms). Longer queries dilute relevance — OpenAlex `search=` is keyword-based with no Boolean/field scoping. Run multiple focused queries rather than one broad one.
- If results are mostly off-topic, the query is too broad — rely on OpenAlex primarily for citation enrichment instead.

### Polite pool
When `LITREV_EMAIL` is set in the MCP server environment, the `mailto` parameter is automatically added to OpenAlex requests (polite pool — faster rate limits). No manual configuration needed.

### Extracting fields

```python
work = response["results"][0]
title = work["title"]
year = work["publication_year"]
doi = work["doi"]  # "https://doi.org/10.1234/..." — strip prefix
cited_by = work["cited_by_count"]
journal = work.get("primary_location", {}).get("source", {}).get("display_name", "")
authors = [a["author"]["display_name"] for a in work.get("authorships", [])]
```

### Citation count enrichment (by DOI or PMID)

```
GET /works?filter=doi:<doi>&select=id,cited_by_count
GET /works?filter=pmid:<pmid>&select=id,cited_by_count
```

`select=` works on filter-based lookups (single field selection) — only fails on search queries.

---

## ClinicalTrials.gov

### API: v2

```
GET https://clinicaltrials.gov/api/v2/studies?query.cond=<condition>&query.intr=<intervention>&filter.overallStatus=COMPLETED&pageSize=50&format=json
```

Parameters: `query.cond`, `query.intr`, `query.term`, `filter.overallStatus`, `filter.phase`, `pageSize` (max 100).

---

## medRxiv/bioRxiv

### API: Content API

```
GET https://api.medrxiv.org/details/medrxiv/<YYYY-MM-DD>/<YYYY-MM-DD>/<cursor>
```

Returns up to 100 per page. No content-based search — filter locally.

---

## EMBASE (Ovid) — Institutional Access

Requires subscription via Ovid platform.

- `exp shoulder pain/` — explode Emtree term
- `.tw.` — text word, `.ti.` — title, `.ab.` — abstract
- `/dt` — drug therapy subheading
- `limit to (systematic reviews or meta analysis)`
- `limit to yr="2010-2026"`

EMBASE adds ~30-40% unique content vs PubMed alone (European journals, conference proceedings, drug/pharmacology literature). Suggest to users with institutional access.

---

## Cochrane CENTRAL — Institutional Access

- `[mh "rotator cuff"]` — MeSH descriptor
- `:ti,ab` — title/abstract, `:kw` — keywords
- `with Publication Year from 2010 to 2026`

---

## Scopus — Institutional Access

- `TITLE-ABS-KEY(rotator cuff AND prevalence)`
- `DOCTYPE(re)` — reviews
- `PUBYEAR > 2009`
- `SUBJAREA(MEDI)`

---

## Web of Science — Institutional Access

- `TS=` — topic, `TI=` — title, `AU=` — author
- `PY=` — year, `DT=` — document type

---

## CINAHL — Institutional Access

EBSCO platform. Nursing and allied health focus. MeSH subject headings, `TI`/`AB` fields, limiters for publication type and peer review.
