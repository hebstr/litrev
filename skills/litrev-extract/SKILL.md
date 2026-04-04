---
name: litrev-extract
context: fork
description: Extract claims and assess study quality from included articles in a literature review. Given screened articles from a completed screening phase, extracts quantitative and qualitative claims from abstracts (with optional full-text enrichment), assigns a quality rating to each study, and organizes findings by themes. Use this skill whenever the user wants to extract data from included studies, pull out key findings, assess study quality, do a quality assessment, do a critical appraisal, do a methodological appraisal, assess risk of bias, rate the evidence, grade the studies, organize findings by theme, make a summary table of effect sizes, or says things like "extract the data from included articles", "what do the studies say", "assess the quality of these studies", "rate the evidence", "which studies are weak", "critical appraisal tool", "extraire les donnees", "evaluer la qualite des etudes", "extraction des donnees", "grille de qualite", "evaluer le niveau de preuve", "classer par themes", "risque de biais", "tableau recapitulatif", "evaluation critique", "sorte les resultats des etudes". Also triggers when screening is complete and the user asks what to do next with included studies. Do NOT trigger for: searching databases (use litrev-search), screening articles (use litrev-screen), citation chaining (handled by orchestrator via MCP `citation_chain`), writing the synthesis (use litrev-synthesize), verifying citations (handled by orchestrator via MCP tools), generic data extraction from spreadsheets or CSVs, or assessing quality of non-research artifacts (code, writing, policy documents).
allowed-tools: Read Write Edit WebFetch mcp__litrev-mcp__extract_claims_regex mcp__litrev-mcp__fetch_fulltext mcp__litrev-mcp__get_section
---

# Data Extraction and Quality Assessment

## Pre-loaded pipeline state

### Working directory
!`pwd`

### Review artifacts found
!`ls -1 review/ 2>/dev/null || echo "(no review/ directory yet)"`

### Included articles count
!`python3 -c "import json; d=json.load(open('review/included_indices.json')); print(f'{len(d)} articles included')" 2>/dev/null || echo "(no included_indices.json yet)"`

### Screening criteria (first 20 lines)
!`head -20 review/screening_log.md 2>/dev/null || echo "(no screening_log.md yet)"`

Extract structured claims from included articles and assess study quality. This skill bridges screening (litrev-screen) and synthesis (litrev-synthesize) — it turns a list of included articles into a structured dataset of claims with quality ratings and thematic assignments.

## Prerequisites

- `review/combined_results.json` — article pool with metadata and abstracts
- `review/included_indices.json` — list of 0-based indices of included articles (from litrev-screen)
- `review/screening_log.md` — contains the inclusion/exclusion criteria used during screening

If any of these files is missing, stop and tell the user which upstream step needs to be completed first.

## Workflow

### Step 1 — Load context

Read `review/included_indices.json` to get the list of included article indices. Load the corresponding records from `review/combined_results.json`. Read `review/screening_log.md` to retrieve the review type and the inclusion criteria. The review type appears in the Title Screening section as `- **Review type**: <type>` (one of: systematic, scoping, rapid, narrative, meta-analysis). The inclusion criteria appear in `- **Criteria applied**: <criteria text>`.

Print a summary: number of included articles, how many have abstracts, how many have PMIDs (for abstract fetching).

**File writing strategy:** Steps 2-5 each update `review/extracted_claims.json` incrementally (read → enrich → write back). This allows resuming from any step if interrupted. Step 7 performs a final validation pass.

### Step 2 — Run automated claim extraction

The MCP tool handles deterministic extraction: quantitative claims (statistics, percentages, numbers) from abstracts using regex patterns, plus fetching missing abstracts from PubMed when PMIDs are available. Semantic interpretation (Step 3), quality assessment (Step 4), and theming (Step 5) are done by the LLM.

Call the MCP tool `extract_claims_regex` with:
- `results_path`: `"review/combined_results.json"`
- `indices_file`: `"review/included_indices.json"`
- `fetch_missing`: `true`
- `output_path`: `"review/extracted_claims.json"`

Alternative: pass `indices` as a list of ints directly instead of `indices_file`.

If the tool fails (network error, malformed JSON), report the error to the user. If only abstract fetching fails, proceed with available abstracts and note the gap.

Review the tool output statistics. Articles with zero quantitative claims are normal (qualitative studies, narrative abstracts) — they will still get semantic claims in Step 3. If many articles lack abstracts, note this as a limitation — those articles' claims will need manual full-text verification later.

### Step 3 — Enrich claims with LLM analysis

Read `review/extracted_claims.json`. For each article, the script has extracted raw quantitative claims. Now enrich each article entry with:

1. **Semantic claims**: Read the abstract and identify the main findings that go beyond raw numbers. Express each claim as a concise statement (e.g., "Smoking is associated with increased rotator cuff tear risk"). Assign each claim a type from this non-exhaustive list:
   - `efficacy` — treatment effect, clinical outcome
   - `risk_factor` / `association` — exposure-outcome relationship
   - `prevalence` / `incidence` — frequency measure
   - `diagnostic` — sensitivity, specificity, predictive value
   - `mechanism` — biological or physiological pathway
   - `prognosis` — disease course, recovery, recurrence
   - Other types as appropriate — the list is not closed

2. **Claim ranking**: Mark each claim as `"rank": "primary"` or `"rank": "secondary"`. Primary claims are the main conclusions of the study. Secondary claims are supporting results. From an abstract, expect 1-3 primary claims and 0-3 secondary claims. Cap at 5 total claims per article when working from abstracts only.

3. **Effect direction**: For association/efficacy claims, note the direction: `positive`, `negative`, `null`, or `mixed`.

4. **Optional fields**: When available in the abstract, include `effect_size` (e.g., "OR 2.1 (95% CI 1.4-3.2)") and `population` (e.g., "adults over 50"). Omit if not reported.

Update each article entry in the JSON with a `semantic_claims` array alongside the existing `claims` array (which holds the raw quantitative extractions). Write the enriched file back to `review/extracted_claims.json`.

### Step 4 — Assess study quality

For each included article, assess quality based on available information (abstract + metadata). This is a simplified assessment — full formal tools (RoB 2, ROBINS-I, AMSTAR-2) require full-text access and cannot be reliably applied by a LLM from abstracts alone.

Assess each study on these axes:

| Axis | Values | Source |
|------|--------|--------|
| Study design | RCT, cohort, cross-sectional, case-control, case series, SR/MA, qualitative, other | abstract + `study_type` field |
| Sample size | numeric or "not reported" | abstract |
| Bias risk | low / moderate / high / unclear | judgment from abstract limitations, design, blinding |
| Limitations noted | yes / no | whether the abstract mentions limitations |
| Funding/COI | reported / not reported / industry | if mentioned in abstract |

Assign an `overall_rating`: **low** / **moderate** / **high** / **unclear** (overall risk of bias, synthesized from all axes above — distinct from the per-axis `bias_risk`).

Note which formal quality assessment tool would be appropriate for each study design:
- RCT → RoB 2
- Non-randomized interventional → ROBINS-I
- Observational (cohort, case-control, cross-sectional) → Newcastle-Ottawa Scale
- Diagnostic accuracy → QUADAS-2
- Systematic review / meta-analysis → AMSTAR 2
- Qualitative → JBI Critical Appraisal Checklist

Write the quality assessment into each article entry in `review/extracted_claims.json` as a `quality` object.

#### Review type adaptations

- **Systematic review / meta-analysis**: Full quality assessment with all axes. Note the recommended formal tool for each study.
- **Scoping review**: Quality assessment may be omitted (per PRISMA-ScR). If the user requests it, apply the simplified grid above. Default: skip quality assessment — set `"quality": null` for each article and add `"quality_skipped": "scoping review (PRISMA-ScR)"` in `quality_summary`.
- **Narrative review**: Simplified quality assessment — design + sample size + overall bias risk. May omit formal tool recommendation.
- **Rapid review**: Same as narrative.

### Step 5 — Organize by themes

Identify 3-7 major themes across the included studies. Themes should emerge from the claims, not be imposed a priori. Common theme patterns in medical reviews:
- By outcome (mortality, morbidity, quality of life)
- By exposure/intervention
- By population subgroup
- By mechanism

Assign each article to one or more themes. Write theme assignments into each article entry as a `themes` array.

After assigning themes, print a summary table:

```
| Theme | Studies | Key direction |
|-------|---------|---------------|
| Diabetes and RC tears | 3 | positive association |
| Smoking and healing | 2 | negative effect |
| ...   | ...     | ...           |
```

### Step 6 — Generate summary table

Print a summary table of all included studies:

```
| # | Author (Year) | Design | N | Bias Risk | Key Finding | Theme(s) |
|---|---------------|--------|---|-----------|-------------|----------|
| 0 | Smith (2020)  | Cohort | 450 | Moderate | Smoking doubles RC tear risk | Smoking |
```

This table serves as the Gate 4 output when running in orchestrated mode.

### Step 7 — Save final output

Ensure `review/extracted_claims.json` contains for each article:
- `title`, `doi`, `pmid`, `year`, `has_abstract`, `abstract_snippet`
- `claims` — raw quantitative claims from the script
- `semantic_claims` — enriched claims with type, rank, direction
- `quality` — quality assessment object (with `bias_risk`, `overall_rating`, `recommended_tool`, etc.)
- `themes` — list of theme assignments

Recompute `stats` from the actual arrays before writing: set `total_quantitative_claims` to the sum of all `claims` array lengths across articles, and `total_semantic_claims` to the sum of all `semantic_claims` array lengths. Also recount `with_claims` as the number of articles where either array is non-empty. Do not trust the values written by `extract_claims_regex` — they reflect pre-enrichment counts.

Normalize `year` to integer for all articles (e.g., `"2010"` → `2010`). If the value cannot be parsed as an integer, keep it as-is.

Print the final statistics: total articles, articles with claims, total claims (quantitative + semantic), quality rating distribution, theme distribution.

## Output Files

All outputs go in `review/` at the project root:

- **`review/extracted_claims.json`** — structured claims, quality assessments, and theme assignments for all included articles

## Output JSON Structure

```json
{
  "stats": {
    "total": 8,
    "with_abstract": 7,
    "with_claims": 6,
    "total_quantitative_claims": 23,
    "total_semantic_claims": 15
  },
  "quality_summary": {
    "low_risk": 2,
    "moderate_risk": 3,
    "high_risk": 1,
    "unclear": 2,
    "tool_recommended": {"RoB 2": 2, "Newcastle-Ottawa": 4, "AMSTAR 2": 1}
  },
  "themes": [
    {"name": "Diabetes and rotator cuff", "article_count": 3},
    {"name": "Smoking and healing outcomes", "article_count": 2}
  ],
  "articles": {
    "Smith_2020": {
      "title": "...",
      "doi": "...",
      "pmid": "...",
      "year": 2020,
      "has_abstract": true,
      "abstract_snippet": "...",
      "claims": [
        {"type": "statistic", "value": "OR 2.1 (95% CI 1.4-3.2)", "verbatim": "..."}
      ],
      "semantic_claims": [
        {
          "claim": "Smoking is independently associated with increased rotator cuff tear risk",
          "claim_type": "risk_factor",
          "rank": "primary",
          "direction": "positive",
          "effect_size": "OR 2.1 (95% CI 1.4-3.2)",
          "population": "adults over 50"
        }
      ],
      "quality": {
        "design": "cohort",
        "sample_size": 450,
        "bias_risk": "moderate",
        "limitations_noted": true,
        "funding": "not reported",
        "overall_rating": "moderate",
        "recommended_tool": "Newcastle-Ottawa"
      },
      "themes": ["Smoking and rotator cuff"]
    }
  }
}
```

## Orchestrated Mode

When called from `litrev` orchestrator, this skill covers Phase 4 (Gate 4). The orchestrator expects:

- Summary table printed (Step 6) with quality ratings and theme assignments
- `review/extracted_claims.json` exists (Step 7)

The orchestrator expects this skill to call the MCP tool `extract_claims_regex` for automated extraction, then enrich with LLM analysis.

## Full-Text Enrichment (Optional)

Claims can be enriched beyond what abstracts provide using `fetch_fulltext` + `get_section` (PMC/Unpaywall/S2 cascade). This is not the default workflow — offer it when:
- Many articles have no abstract
- The user asks for more detailed extraction
- Key effect sizes are missing from abstracts

To enrich: call `fetch_fulltext(doi)` to cache the full text, then `get_section(doi, section="results")` or other sections to retrieve targeted content. Re-read the enriched content and update `semantic_claims` accordingly. When adding claims from full-text, mark them with `"source": "full-text"` (vs `"source": "abstract"` for abstract-derived claims).

