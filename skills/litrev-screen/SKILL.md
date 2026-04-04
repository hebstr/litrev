---
name: litrev-screen
context: fork
description: Screen articles for inclusion in medical literature reviews. Decides which papers to keep or exclude by applying inclusion/exclusion criteria (also called eligibility criteria) to titles and abstracts from search results, fetches missing abstracts from PubMed, documents every decision in a structured screening log, and produces PRISMA-compliant counts. Use this skill whenever the user wants to go through search results and decide which articles are relevant, filter or sort articles by inclusion/exclusion criteria for a review, triage papers, figure out which papers are relevant, or determine which studies to include in a review. Trigger on any of these intents even if phrased informally — "screen these results", "apply inclusion criteria", "apply eligibility criteria", "title/abstract screening", "which of these are relevant", "go through the papers and decide which to keep", "figure out which ones are about my topic", "triage these references", "trier les articles", "cribler les résultats", "passer au crible", "sélectionner les articles", "filtrer les articles", "quels articles garder", "appliquer les critères d'inclusion". Also triggers when the orchestrator skill (litrev) delegates its screening phase, or when the user has just completed a search phase (litrev-search) and wants to narrow down results or move to the next step (e.g., "now what", "next phase", "what's next"). Do NOT trigger for: running database searches (use litrev-search), citation chaining or snowballing (handled by orchestrator via MCP `citation_chain`), data extraction from included articles (use litrev-extract), full-text PDF retrieval, quality/risk-of-bias assessment, summarizing included articles, building PRISMA flow diagrams, or filtering non-review datasets (e.g., pandas/SQL filtering of research data).
allowed-tools: Read Write Edit WebFetch mcp__litrev-mcp__fetch_abstracts mcp__litrev-mcp__fetch_fulltext mcp__litrev-mcp__get_section
---

# Article Screening for Medical Literature Reviews

## Pre-loaded pipeline state

### Working directory
!`pwd`

### Review artifacts found
!`ls -1 review/ 2>/dev/null || echo "(no review/ directory yet)"`

### Search results summary (first 30 lines)
!`head -30 review/search_results.md 2>/dev/null || echo "(no search_results.md yet)"`

### Article count in combined_results.json
!`python3 -c "import json; d=json.load(open('review/combined_results.json')); print(f'{len(d)} articles in pool')" 2>/dev/null || echo "(no combined_results.json yet)"`

Screen search results against inclusion/exclusion criteria following a multi-pass approach: title screening, then abstract screening, then optional full-text screening. Produce a structured screening log and PRISMA-compliant counts.

## Usage Modes

**Standalone**: the user asks to screen search results directly. Confirm that input files exist, that criteria are available, and that the review type is specified before starting. If the user does not provide a review type, ask — do not assume a default.

**Orchestrated**: called by the `litrev` orchestrator skill after Phase 2a (search). The orchestrator has already established criteria in Phase 1. Read them from the conversation context and proceed without re-asking.

## Input Requirements

| File / Info | Required | Source |
|-------------|----------|--------|
| `review/search_results.md` | Yes | Produced by `litrev-search` |
| `review/combined_results.json` | Yes | Produced by `litrev-search` |
| Inclusion criteria | Yes | From user or orchestrator (population, study types, date range, language, etc.) |
| Exclusion criteria | Yes | From user or orchestrator |
| Review type | Yes | systematic, scoping, narrative, meta-analysis, rapid |
| `review/protocol.md` | Optional | Produced by `litrev` orchestrator — contains research question, framework, criteria, review type |

If `review/search_results.md` or `review/combined_results.json` does not exist, stop and tell the user to run the search phase first (`litrev-search`).

In **standalone** mode, criteria can come in any form: inline text, a file reference, or prior conversation turns. If `review/protocol.md` exists, read it to recover inclusion/exclusion criteria and review type — this is especially useful when resuming a previous session. If the user provides only inclusion criteria, ask for exclusion criteria before starting. If they say "none" or "no specific exclusions", proceed and document this in the screening log.

## Output Files

All outputs go in `review/` at the project root:

- **`review/screening_log.md`** — structured log of all screening decisions (designed for session resumption)
- **`review/included_indices.json`** — JSON array of 0-based indices into `combined_results.json` for included articles

## Workflow

### Step 0 — Resume detection

Check whether `review/screening_log.md` already exists. If it does:
- Parse it to find which screening steps have `Status: COMPLETE`
- If a section exists without `Status: COMPLETE`, delete everything from its `##` heading to the next `##` heading (or end of file if last section) and restart that step
- Resume from the first incomplete or missing step
- Tell the user which steps are already done and which will be resumed

### Step 1 — Title screening

Read the full table in `review/search_results.md` (the `## All Results` section). For each article, evaluate the title against inclusion/exclusion criteria.

**How to screen titles:**
1. Read `references/screening_criteria.md` for methodology guidance
2. For each title, check exclusion criteria in order — exclude at the FIRST criterion that fails (do not continue checking). When in doubt, INCLUDE — screening is meant to be sensitive (high recall), not specific
3. Group exclusions by reason — do not just list index numbers without explanation

**Decision rules:**
- If the title clearly indicates the article is irrelevant (no inclusion criterion is plausibly met) → EXCLUDE with reason
- If the title is ambiguous or could be relevant → INCLUDE (will be resolved at abstract stage)
- If the title mentions a population, intervention, or outcome from any inclusion criterion → INCLUDE

**Volume management:** if >200 articles remain after title screening, flag to the user that criteria may be too broad and discuss narrowing before proceeding.

**Output:** append to `review/screening_log.md`:

```markdown
## Title Screening

- **Date**: YYYY-MM-DD
- **Review type**: <systematic | scoping | narrative | meta-analysis | rapid>
- **Pool**: <total articles in search_results.md>
- **Criteria applied**: <brief summary of inclusion/exclusion criteria>

### Retained (<count>)

<space-separated 0-based indices>

### Excluded (<count>)

| Index | Title (truncated) | Reason |
|-------|-------------------|--------|
| 42 | Pediatric shoulder ... | Pediatric population |
| 87 | Canine rotator cuff ... | Animal study |

Status: COMPLETE
```

### Step 2 — Abstract screening

Fetch abstracts for retained articles, then apply criteria more rigorously.

**Step 2a — Fetch abstracts:**

If zero articles were retained in Step 1, skip to the zero-retention handler in Completion Criteria — do not invoke the tool.

Call the MCP tool `fetch_abstracts` with:
- `results_path`: `"review/combined_results.json"`
- `indices`: list of 0-based indices retained from Step 1
- `fetch_missing`: `true`
- `output_path`: `"review/abstracts_for_screening.md"`

If the `fetch_abstracts` tool is not available (MCP server not connected), tell the user to restart Claude Code so the litrev-mcp server loads. If that is not possible, proceed with abstracts already present in `combined_results.json` and note the gap in the screening report.

The tool fetches abstracts from PubMed (efetch XML) for articles that have a PMID but no abstract in `combined_results.json`. Fetched abstracts are also backfilled into `combined_results.json`.

If the tool reports fetch failures, tell the user which batches failed and ask whether to retry, proceed with the abstracts that were fetched, or stop. Do not silently proceed with a partial result.

**Step 2b — Screen abstracts:**

Read `review/abstracts_for_screening.md` and apply all inclusion/exclusion criteria to each abstract. At this stage, screening is more rigorous than title screening:
- Check population, intervention/exposure, outcome, study design, date range, language
- For each exclusion, cite the specific criterion violated
- Articles with no abstract available: list them in the `### No Abstract` section (not in `### Retained`) — they proceed to full-text screening

**Counting rule:** `Retained + Excluded + No Abstract = Pool`. Articles in `### No Abstract` are neither retained nor excluded at this stage — they are deferred. The `### Retained` count only includes articles that were screened and passed.

**Output:** append to `review/screening_log.md`:

```markdown
## Abstract Screening

- **Date**: YYYY-MM-DD
- **Pool**: <count from title screening>
- **Abstracts available**: <count with abstract> / <total>

### Retained (<count>)

<space-separated 0-based indices — only articles with abstracts that passed screening>

### Excluded (<count>)

| Index | First Author (Year) | Reason |
|-------|---------------------|--------|
| 23 | Smith (2019) | Wrong population (children <18) |
| 45 | Jones (2015) | Case report, N=12 |

### No Abstract (<count>)

<space-separated indices — these proceed to full-text screening>

Status: COMPLETE
```

### Step 3 — Full-text screening (when applicable)

Full-text screening applies when:
- Articles had no abstract and were listed in `### No Abstract` in Step 2 (regardless of review type — these always need further assessment)
- The review type is systematic or meta-analysis (recommended for all retained articles)
- The user explicitly requests it

For scoping, narrative, or rapid reviews, full-text screening of articles that already passed abstract screening is optional. If skipped, document this in the screening log. However, no-abstract articles from Step 2 must always pass through Step 3.

**What Step 3 can do:** re-examine articles using title, metadata (study type, journal, year), and any available abstract. For no-abstract articles or borderline cases, use `fetch_fulltext` + `get_section` to retrieve the abstract or introduction from the full text (PMC/Unpaywall/S2 cascade) — this is a targeted lookup, not a bulk download. Step 3 adds value by: (a) catching no-abstract articles that are clearly out of scope based on metadata or fetched content, (b) identifying duplicate cohorts among retained articles, (c) applying stricter scrutiny to borderline cases. If no additional information is available beyond what was already screened, retain the article and note it in the log.

The **pool** entering Step 3 is: `Retained from Step 2 + No Abstract from Step 2`.

**Output:** append to `review/screening_log.md`:

```markdown
## Full-Text Screening

- **Date**: YYYY-MM-DD
- **Pool**: <Retained from Step 2 + No Abstract from Step 2>

### Retained (<count>)

<space-separated 0-based indices>

### Excluded (<count>)

| Index | First Author (Year) | Reason |
|-------|---------------------|--------|
| 67 | Lee (2021) | Duplicate cohort from same registry as #34 |

Status: COMPLETE
```

### Step 4 — Produce outputs

After all screening steps are complete:

1. **Write `review/included_indices.json`**: a JSON array of the final 0-based indices of included articles.

2. **Append a Limitations section** to `review/screening_log.md`:

```markdown
## Limitations

Screening performed by a single AI reviewer (LLM). PRISMA recommends dual independent screening. For formal systematic reviews, a human second reviewer should validate a sample of decisions, particularly exclusions.
```

3. **Print a screening summary** to the user showing the counts at each stage. Example:

```
Screening summary: 10 records screened → 5 excluded at title (3 wrong population, 1 animal, 1 editorial) → 5 abstracts assessed → 1 excluded (wrong outcome) → 4 included.
```

Adapt the format to the number of stages actually performed (e.g., rapid reviews have a single combined pass). Include top exclusion reasons. The counts at each step must be arithmetically consistent (retained + excluded = pool; at abstract screening: retained + excluded + no abstract = pool).

Note: the pre-deduplication count ("Records identified") comes from `review/search_results.md` produced by `litrev-search`. If that file is not available, omit it. Citation chaining adds additional studies — that is handled by the orchestrator (Phase 3b, MCP `citation_chain`) and will produce its own counts.

## Row Numbering Convention

All `indices` arguments and index references use **0-based** indices matching the `combined_results.json` array. The `#` column in `search_results.md` uses the same numbering. Always cross-reference by index, not by title or DOI, within a single screening session. If `combined_results.json` is modified between sessions (e.g., by citation chaining adding articles), previous indices remain valid — new articles are appended.

## Review Type Adaptations

| Review Type | Title Screening | Abstract Screening | Full-Text Screening |
|-------------|----------------|-------------------|---------------------|
| Systematic | Required | Required | Required |
| Meta-Analysis | Required | Required | Required |
| Scoping | Required | Required | Optional* |
| Narrative | Required | Required | Optional* |
| Rapid | Combined (single title + abstract pass) | Combined (single title + abstract pass) | Optional* |

*Optional for articles that passed abstract screening, but **required** for articles listed in `### No Abstract` in Step 2 — these must always go through Step 3 regardless of review type. If no other articles need full-text screening, run Step 3 limited to no-abstract articles only.

For **rapid reviews**, combine title and abstract screening into a single pass: fetch abstracts for all articles upfront, then screen title+abstract together. Use the following log section (note the heading name — the resumption logic depends on it):

```markdown
## Combined Title/Abstract Screening

- **Date**: YYYY-MM-DD
- **Review type**: Rapid
- **Pool**: <total articles>
- **Abstracts available**: <count with abstract> / <total>
- **Criteria applied**: <brief summary of inclusion/exclusion criteria>

### Retained (<count>)

<space-separated 0-based indices>

### Excluded (<count>)

| Index | Title (truncated) | Reason |
|-------|-------------------|--------|
| 42 | Pediatric shoulder ... | Pediatric population |

### No Abstract (<count>)

<space-separated indices — these proceed to full-text screening if applicable>

Status: COMPLETE
```

## Screening Log Format (for resumption)

The screening log is designed so that an interrupted session can be resumed. Each section represents one screening step. The `Status: COMPLETE` marker indicates the step was finished. Rules:

- If a section exists but has no `Status: COMPLETE`, the step was interrupted — redo it entirely
- If a section does not exist, the step has not started
- The `### Retained` line contains space-separated indices that feed into the next step
- Always write the section header and content BEFORE writing `Status: COMPLETE`

## Completion Criteria

The screening is complete when:
1. `review/screening_log.md` exists with all applicable screening steps marked `Status: COMPLETE`
2. `review/included_indices.json` exists with the final list of included article indices
3. Screening summary has been printed with consistent counts
4. Retained + excluded counts at each step sum to the pool size

If zero articles are retained at any step, stop and ask the user whether to broaden criteria, expand the search, or report the absence of evidence as a finding. If reporting absence: write `review/included_indices.json` as `[]`, complete the screening log with all steps performed marked `Status: COMPLETE`, and print a summary stating zero articles met the inclusion criteria.
