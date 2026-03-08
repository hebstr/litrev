# Database Search Syntax Reference

Quick reference for database-specific search syntax. For methodology, frameworks (PICO, GRADE), and workflow, see `SKILL.md`.

---

## PubMed / MEDLINE

**Field tags:**
| Tag | Meaning | Example |
|-----|---------|---------|
| `[MeSH]` | MeSH controlled term | `"Diabetes Mellitus, Type 2"[MeSH]` |
| `[Title]` | Title only | `"GLP-1"[Title]` |
| `[tiab]` | Title/Abstract | `"MACE"[tiab]` |
| `[Author]` | Author name | `"Marso SP"[Author]` |
| `[Journal]` | Journal name | `"NEJM"[Journal]` |
| `[DP]` | Publication date | `2017:2026[DP]` |
| `[pt]` | Publication type | `"Randomized Controlled Trial"[pt]` |
| `[Language]` | Language filter | `English[Language]` |

**MeSH tips:**
- Explode (include narrower terms): default behavior, use `[MeSH:NoExp]` to disable
- Subheadings: `"Diabetes Mellitus, Type 2/therapy"[MeSH]`
- Available subheadings: `/therapy`, `/diagnosis`, `/epidemiology`, `/adverse effects`, `/drug therapy`, `/surgery`, `/prevention and control`
- MeSH browser: https://meshb.nlm.nih.gov/search

**Wildcards:** `*` for truncation (`cardiovascul*` matches cardiovascular, cardiovasculaire)

**Example — intervention review:**
```
("GLP-1 receptor agonists"[MeSH] OR "GLP-1 RA"[tiab] OR "semaglutide"[tiab] OR "liraglutide"[tiab])
AND ("cardiovascular diseases"[MeSH] OR "MACE"[tiab])
AND ("diabetes mellitus, type 2"[MeSH])
AND ("Randomized Controlled Trial"[pt] OR "Meta-Analysis"[pt])
AND 2017:2026[DP]
AND English[Language]
```

**Filters (via URL or sidebar):**
- Article type: Clinical Trial, RCT, Meta-Analysis, Systematic Review
- Species: Humans
- Age groups: Adult, Child, Aged

---

## EMBASE (Ovid)

**Syntax:**
| Operator | Meaning | Example |
|----------|---------|---------|
| `exp` | Explode Emtree term | `exp diabetes mellitus/` |
| `.tw.` | Text word (title/abstract) | `cardiovascular.tw.` |
| `.ti.` | Title only | `GLP-1.ti.` |
| `.ab.` | Abstract only | `semaglutide.ab.` |
| `/` | Emtree heading | `exp cardiovascular disease/` |
| `limit` | Apply limits | `limit 1 to (english language and yr="2017-2026")` |

**Subheadings:** `/dt` (drug therapy), `/th` (therapy), `/di` (diagnosis), `/ae` (adverse effects)

**Unique value vs PubMed:** stronger coverage of pharmacology, drug safety, European literature, conference abstracts

**Example:**
```
1. exp glucagon like peptide 1 receptor agonist/
2. (GLP-1 OR semaglutide OR liraglutide).tw.
3. 1 OR 2
4. exp cardiovascular disease/
5. MACE.tw.
6. 4 OR 5
7. exp non insulin dependent diabetes mellitus/
8. 3 AND 6 AND 7
9. limit 8 to (english language and yr="2017-2026")
10. limit 9 to (randomized controlled trial or meta analysis)
```

---

## Cochrane Library (CENTRAL)

**Search fields:**
- Title/Abstract/Keywords (default)
- MeSH descriptor: `[mh "Diabetes Mellitus, Type 2"]`
- Title: `ti:` | Abstract: `ab:` | Keywords: `kw:`

**Example:**
```
[mh "GLP-1 receptor agonists"] OR (GLP-1 OR semaglutide OR liraglutide):ti,ab
AND [mh "cardiovascular diseases"] OR MACE:ti,ab
AND [mh "Diabetes Mellitus, Type 2"]
```

**Tips:**
- Check existing Cochrane Reviews on the topic before starting a new review
- CENTRAL indexes RCTs from PubMed, EMBASE, and hand-searched journals

---

## ClinicalTrials.gov

**Search fields:** Condition, Intervention, Other terms, Status, Phase, Study type

**Advanced search URL parameters:**
- `cond=` Condition/disease
- `intr=` Intervention/treatment
- `type=` Study type (Interventional, Observational)
- `rslt=` Results (With, Without)
- `phase=` Phase (0-4)
- `strd_s=` Start date | `strd_e=` End date

**Example:** Completed Phase 3+ RCTs with results:
```
cond=type 2 diabetes
intr=GLP-1 receptor agonist
type=Interventional
phase=2,3,4
rslt=With
```

**Value:** Reduces publication bias by identifying unpublished trial results

---

## Semantic Scholar API

**Base URL:** `https://api.semanticscholar.org/graph/v1/paper/search`

**Parameters:**
| Parameter | Example |
|-----------|---------|
| `query` | `GLP-1 cardiovascular outcomes` |
| `year` | `2017-2026` |
| `fieldsOfStudy` | `Medicine` |
| `fields` | `title,authors,year,citationCount,journal,externalIds` |
| `limit` | `100` (max) |
| `offset` | `0` (for pagination) |

**Bulk search:** `https://api.semanticscholar.org/graph/v1/paper/search/bulk`

**Rate limits:** 1 request/second without key, 10/second with key

**Features:** `influentialCitationCount`, `citationVelocity`, related papers via `/recommendations`

---

## Google Scholar

**No official API.** Use for manual coverage checks and citation tracking.

**Search operators:**
| Operator | Example |
|----------|---------|
| `allintitle:` | `allintitle: GLP-1 cardiovascular` |
| `author:` | `author:"Marso SP"` |
| `source:` | `source:"NEJM"` |
| `""` | Exact phrase: `"cardiovascular outcomes"` |
| `-` | Exclude: `-review` |

**Date filter:** Use sidebar or `&as_ylo=2017&as_yhi=2026` in URL

**"Cited by" feature:** Essential for forward citation chaining — sort citing papers by citation count

---

## Scopus (Elsevier)

**Access:** Requires institutional access or API key (https://dev.elsevier.com/)

**Search fields:**
| Field | Meaning | Example |
|-------|---------|---------|
| `TITLE()` | Title | `TITLE("GLP-1")` |
| `TITLE-ABS-KEY()` | Title/Abstract/Keywords | `TITLE-ABS-KEY(cardiovascular)` |
| `AUTH()` | Author | `AUTH(Marso)` |
| `SRCTITLE()` | Source title (journal) | `SRCTITLE("NEJM")` |
| `PUBYEAR` | Publication year | `PUBYEAR > 2016` |
| `DOCTYPE()` | Document type | `DOCTYPE(ar)` (article), `DOCTYPE(re)` (review) |
| `SUBJAREA()` | Subject area | `SUBJAREA(MEDI)` |
| `LANGUAGE()` | Language | `LANGUAGE(english)` |

**Operators:** `AND`, `OR`, `AND NOT`, `W/n` (proximity within n words)

**Example:**
```
TITLE-ABS-KEY("GLP-1 receptor agonist*" OR semaglutide OR liraglutide)
AND TITLE-ABS-KEY(cardiovascular OR "MACE")
AND TITLE-ABS-KEY("type 2 diabetes")
AND PUBYEAR > 2016
AND DOCTYPE(ar OR re)
AND LANGUAGE(english)
```

**Unique value vs PubMed:** broader multidisciplinary coverage, citation metrics (h-index, SJR), author profiling, affiliation data

---

## Web of Science (Clarivate)

**Access:** Requires institutional subscription

**Search fields:**
| Field | Meaning | Example |
|-------|---------|---------|
| `TS=` | Topic (title/abstract/keywords) | `TS="GLP-1"` |
| `TI=` | Title only | `TI="cardiovascular outcomes"` |
| `AU=` | Author | `AU=Marso SP` |
| `SO=` | Source (journal) | `SO="New England Journal of Medicine"` |
| `PY=` | Publication year | `PY=2017-2026` |
| `DT=` | Document type | `DT=Article` |
| `LA=` | Language | `LA=English` |
| `WC=` | Web of Science category | `WC="Endocrinology & Metabolism"` |

**Operators:** `AND`, `OR`, `NOT`, `NEAR/n` (proximity), `SAME` (same sentence)
**Wildcards:** `*` (0+ chars), `?` (1 char), `$` (0 or 1 char)

**Example:**
```
TS=("GLP-1 receptor agonist*" OR semaglutide OR liraglutide)
AND TS=(cardiovascular OR "MACE")
AND TS=("type 2 diabetes")
AND PY=2017-2026
AND DT=(Article OR Review)
AND LA=English
```

**Unique value vs PubMed:** Journal Impact Factor, citation reports, cross-disciplinary coverage (science, social science, arts & humanities), cited reference search for backward/forward chaining

---

## OpenAlex API

**Base URL:** `https://api.openalex.org/works`

**Filters (free, no key):**
```
?filter=default.search:GLP-1 cardiovascular,
  publication_year:2017-2026,
  type:journal-article,
  language:en
&sort=cited_by_count:desc
&per_page=100
```

**Useful for:** Citation counts, author disambiguation, institutional analysis, open access status

---

## Citation Chaining

Supplement database searches with backward and forward citation chaining to capture studies missed by keyword-based queries.

### Backward chaining (reference list scanning)
- Review reference lists of included studies and relevant reviews
- Identify seminal/foundational papers cited across multiple studies
- Tools: manual review, Zotero "Related" feature

### Forward chaining (cited-by tracking)
- Find newer studies that cite key included papers
- **Google Scholar**: "Cited by" link → sort by relevance or date
- **Scopus**: "Cited by" tab with refined search within citing articles
- **Web of Science**: "Cited Reference Search" and "Citation Report"
- **Semantic Scholar**: `/references` and `/citations` API endpoints
- **OpenAlex**: `cited_by` and `referenced_works` fields

### When to use
- After initial database search is complete
- Start from the 5–10 most relevant included studies
- Document which seed papers were used and how many new papers were found
- Apply the same inclusion/exclusion criteria to newly found papers

---

## medRxiv / bioRxiv (Preprint Servers)

**Search URL:** `https://www.medrxiv.org/search/` | `https://www.biorxiv.org/search/`

**API:** `https://api.medrxiv.org/details/medrxiv/` (free, no key)

**Search syntax:**
- Simple keyword search in title/abstract
- Date filters: `jcode:medrxiv date_filter:2017-01-01 2026-12-31`
- No controlled vocabulary (no MeSH/Emtree)

**API example:**
```
https://api.medrxiv.org/details/medrxiv/2017-01-01/2026-12-31/0/json
```
Returns batches of 100; use offset for pagination.

**Value:** Captures recent research before peer review; reduces publication lag bias. Flag as preprint in evidence synthesis and note lack of peer review in quality assessment.

---

## CINAHL (EBSCO)

**Access:** Requires institutional subscription (EBSCO)

**Search fields:**
| Field | Meaning | Example |
|-------|---------|---------|
| `TI` | Title | `TI "GLP-1"` |
| `AB` | Abstract | `AB "cardiovascular"` |
| `MH` | CINAHL Subject Heading | `MH "Diabetes Mellitus, Type 2+"` |
| `AU` | Author | `AU "Marso SP"` |
| `SO` | Journal | `SO "NEJM"` |
| `PT` | Publication type | `PT "Clinical Trial"` |

**Operators:** `AND`, `OR`, `NOT`
**Explode:** `+` suffix on subject heading (e.g., `MH "Diabetes Mellitus+"`)
**Wildcards:** `*` (truncation), `?` (single character), `#` (zero or one character)

**Example:**
```
S1  MH "Glucagon-Like Peptide 1+"
S2  TI "GLP-1" OR TI "semaglutide" OR TI "liraglutide"
S3  S1 OR S2
S4  MH "Cardiovascular Diseases+"
S5  TI "MACE" OR AB "MACE"
S6  S4 OR S5
S7  MH "Diabetes Mellitus, Type 2+"
S8  S3 AND S6 AND S7
S9  S8   Limiters - Published Date: 20170101-20261231; Language: English; Publication Type: Clinical Trial
```

**Unique value vs PubMed:** Strongest coverage of nursing, allied health, and patient-centered outcomes research

---

## Search Documentation Template

Copy-paste template for documenting each database search:

```markdown
## Search Strategy

### Database: [Name]
- **Date searched**: YYYY-MM-DD
- **Date range**: YYYY-MM-DD to YYYY-MM-DD
- **Search string**:
  ```
  [Complete search string]
  ```
- **Filters applied**: [Language, study type, species, etc.]
- **Results**: n articles
- **After deduplication**: n articles

### Total
- **Combined results**: n unique articles
- **After title screening**: n
- **After abstract screening**: n
- **Included in review**: n
```
