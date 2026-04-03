---
name: litrev-synthesize
context: fork
description: Write a constrained thematic synthesis from extracted claims in a literature review. Given extracted claims, quality ratings, and theme assignments from litrev-extract, produces a structured narrative review document organized by themes with Pandoc citations. Use this skill whenever the user wants to write the synthesis, draft the review document, write the results, produce the narrative, synthesize the findings, turn the extracted data into a review, write up the review, write it all up as a paper, put together the final review, turn this into a proper document, or says things like "write the synthesis", "draft the review", "synthesize the findings", "write up the results", "produce the review document", "turn these claims into a narrative", "generate the review text", "write it up", "turn this into a paper", "go from data to text", "make the paper", "create the document from the extracted data", "write the final document", "produce the manuscript", "build the review from the JSON", "turn this into something submittable", "rediger la synthese", "ecrire la revue", "rediger les resultats", "produire le document", "synthetiser les resultats", "passer a la redaction", "ecrire le texte de la revue", "rediger le papier", "mettre en forme la revue", "ecrire le document final", "pondre la revue", "faire le document", "passer de l'extraction au texte", "produire le manuscrit", "transformer les donnees en texte". Also triggers when extraction is complete and the user asks what to do next regarding writing or drafting the review. Do NOT trigger for: extracting claims (use litrev-extract), searching databases (use litrev-search), screening articles (use litrev-screen), merging or deduplicating search results (use litrev-search), citation chaining (handled by orchestrator via MCP `citation_chain`), verifying citations or generating BibTeX (handled by orchestrator via MCP tools), writing review protocols for PROSPERO registration, writing non-review documents (audit reports, clinical reports, grant proposals, patient summaries), statistical analysis or meta-analysis coding in R/Python after extraction (e.g., random-effects models, forest plots, methodology guidance), or qualitative primary research write-ups (thematic analysis of interviews, focus groups) even if the user says "synthesize themes" or "write up findings".
allowed-tools: Read Write Edit Bash
---

# Constrained Thematic Synthesis

## Pre-loaded pipeline state

### Working directory
!`pwd`

### Review artifacts found
!`ls -1 review/ 2>/dev/null || echo "(no review/ directory yet)"`

### Extracted claims summary
!`python3 -c "import json; d=json.load(open('review/extracted_claims.json')); print(f\"{len(d.get('articles',{}))} articles, {len(d.get('themes',[]))} themes\")" 2>/dev/null || echo "(no extracted_claims.json yet)"`

### Review type
!`grep -i 'review type' review/screening_log.md 2>/dev/null || echo "(review type not found)"`

Write a structured narrative review document from extracted claims, quality ratings, and theme assignments. This skill bridges extraction (litrev-extract) and verification (Phase 6, MCP tools) — it turns a structured dataset of claims into a professional review document with Pandoc citations.

## Prerequisites

- `review/extracted_claims.json` — claims, quality assessments, and themes (from litrev-extract)
- `review/screening_log.md` — screening decisions with review type and criteria
- `review/search_results.md` — search results summary (for Methods section)
- `review/combined_results.json` — full article pool (for metadata)
- `review/protocol.md` (optional) — research question, framework, criteria (from litrev orchestrator)

If any of the four required files is missing, stop and tell the user which upstream step needs to be completed first.

After confirming files exist, validate minimal content:
- `extracted_claims.json` must be valid JSON with at least 1 article in `articles`, a non-empty `themes` array, and article keys matching the `LastName_Year` BibTeX pattern. If malformed, stop and tell the user
- `screening_log.md` must contain a review type declaration (systematic, scoping, rapid, narrative, or meta-analysis). If the declared type is not one of these five, treat it as a narrative review and note the adaptation in the Methodology section

If validation fails, stop and tell the user what is missing.

### `extracted_claims.json` schema

```
{
  "stats": { "total", "with_abstract", "with_claims", "total_quantitative_claims", "total_semantic_claims" },
  "quality_summary": { "low_risk", "moderate_risk", "high_risk", "unclear", "tool_recommended": { "<ToolName>": count } },
  "themes": [ { "name": "<theme>", "article_count": N } ],
  "articles": {
    "<BibTeXKey>": {
      "title", "doi", "pmid", "year", "has_abstract", "abstract_snippet",
      "claims": [ { "type": "statistic", "value", "verbatim" } ],
      "semantic_claims": [ { "claim", "claim_type", "rank", "direction", "effect_size", "population" } ],
      "quality": { "design", "sample_size", "bias_risk", "limitations_noted", "funding", "overall_rating", "recommended_tool" },
      "themes": [ "<theme>" ]
    }
  }
}
```

Key points: articles are keyed by BibTeX key (`LastName_Year`). Each article has a `claims` array (quantitative, regex-extracted) and a `semantic_claims` array (LLM-enriched). Theme assignment is per-article via the `themes` list.

### `screening_log.md` schema

Markdown with sections: `## Title Screening` (contains `**Review type**:` declaration and `**Criteria applied**:`), `## Abstract Screening`, `## Full-Text Screening`. Each section has Retained/Excluded lists with article indices and a `Status:` line. PRISMA counts are derived from these sections.

### `combined_results.json` schema

JSON array of article objects. Relevant fields: `title`, `authors` (array), `first_author`, `year`, `doi`, `pmid`, `journal`, `abstract`, `source`, `study_type`. May also include `volume`, `number`, `pages` when available.

## Setup

No Python venv required — this skill is LLM-driven writing with minimal scripting.

## Workflow

### Step 1 — Load context

Read all prerequisite files. Extract:

- **Review type** from `screening_log.md` (systematic, scoping, rapid, narrative, meta-analysis)
- **Research question and framework** (PICO/PEO/SPIDER) from `protocol.md` if it exists; fall back to `screening_log.md`, then `search_results.md`
- **Themes** from `extracted_claims.json` top-level `themes` array
- **Quality summary** from `extracted_claims.json` top-level `quality_summary`
- **All article entries** with their claims, quality, and theme assignments
- **PICO/PEO outcome list** from `protocol.md` framework section. Parse each named outcome (e.g., PICO Outcomes: "(1) Efficacy …; (2) Predictive factors …; (3) Place in care sequence …; (4) Complications …") into a numbered list. For each outcome, count articles in `extracted_claims.json` whose claims or semantic_claims mention keywords from that outcome. Store this as the **outcome coverage map** for use in Steps 4e and 5.

Print a summary: review type, number of articles, number of themes, quality distribution, and the outcome coverage map (outcome name → article count).

### Step 2 — Scaffold the document

Derive a `<topic>` slug from the research question (short snake_case, e.g., `rotator_cuff_comorbidities`, `probiotics_cdiff`, `digital_health_pain`). If `review/` already contains a `*_review.md` file, use its existing slug. If multiple `*_review.md` files exist, ask the user which to resume.

If `review/<topic>_review.md` already exists and is non-empty, do NOT overwrite — resume editing the existing file (skip the `cp` below). Verify its YAML header contains `bibliography: references.bib` and `csl: vancouver.csl`; add them if missing. Only copy the template for a fresh start.

Read `assets/review_template.md` from this skill's directory and write it to `review/<topic>_review.md`.
If `review/vancouver.csl` does not exist, read `assets/vancouver.csl` from this skill's directory and write it to `review/vancouver.csl`.

Update the YAML header with the actual title, subtitle, and date.

### Step 3 — Build BibTeX keys mapping

Use the BibTeX keys already present as article keys in `extracted_claims.json` — do NOT re-derive keys. The extraction file is authoritative for key assignment. Keys follow the `LastName_Year` pattern (e.g., `Yamamoto_2010`, `Cho_2021`); collisions use suffix `a`, `b`, `c`.

Build this mapping once and use it consistently throughout the document. Print the key table:

```
| Key | Author (Year) | PMID |
|-----|---------------|------|
| Yamamoto_2010 | Yamamoto et al. (2010) | 20102345 |
```

### Step 4 — Write the document

Fill in each section of the template. The document structure depends on the review type (see Review Type Adaptations below), but always follows this general order:

#### 4a. Abstract

Structured abstract: Background, Objectives, Methods, Results, Conclusions, Keywords.

#### 4b. Introduction

Background and context, scope and objectives, significance. State the research question with its framework components.

#### 4c. Methodology

- **Search strategy**: databases searched, search strings, dates (from `search_results.md`)
- **Inclusion/exclusion criteria**: from `screening_log.md`
- **Study selection**: PRISMA flow from screening counts
- **Data extraction**: describe the extraction approach
- **Quality assessment**: tools used per study design (from `quality_summary`) — for scoping reviews, shorten or omit per PRISMA-ScR; for rapid reviews, use simplified approach (see Review Type Adaptations)
- **Synthesis approach**: narrative thematic synthesis (or meta-analysis if applicable)

#### 4d. Results — Study Selection

PRISMA flow summary, study characteristics table (from `extracted_claims.json`), quality distribution. Omit the Bibliometric Overview section from the template unless the user specifically performed bibliometric analysis.

#### 4e. Results — Thematic Synthesis

**CRITICAL — This is the core of the skill.**

For each theme identified in `extracted_claims.json`:

1. Write a subsection with the theme name as heading
2. Synthesize findings ACROSS studies assigned to this theme — do NOT write study-by-study summaries. If a theme has only one article, present its findings directly and note the limited evidence base. Articles with no theme assignment (`"themes": []`) should be cited in the most relevant theme based on their claims, or grouped under an "Other findings" subsection if no theme fits.
3. Compare and contrast findings, identify consensus and controversies
4. Cite using Pandoc syntax: `[@Smith_2021]`, `[@Smith_2021; @Jones_2023]`, `[-@Smith_2021]`

**Constrained writing rule**: When citing specific numbers (prevalences, OR, HR, RR, percentages, p-values, sample sizes, confidence intervals, rates), you MUST only use values that appear in `review/extracted_claims.json` for the corresponding article. Check both `claims` (quantitative) and `semantic_claims` arrays. If a number is not in the extraction:
- **Default**: flag it with `<!-- UNVERIFIED: value not in extracted_claims.json -->` so the verification phase (MCP `audit_claims`) can cross-check it
- **Alternative**: omit it if the claim can be fully made without any specific number (e.g., "a large cohort" instead of "n=12,403"). When in doubt, flag rather than omit

**Multi-source citation guard**: When combining two or more studies in a single citation group (e.g., `[@A; @B]`), every specific statistic reported in the sentence must be verifiable in ALL cited sources, not just one. If study A reports "OR = 2.3" and study B does not report a comparable statistic, do not group them in the same citation for that claim. Either cite each study separately with its own finding, or use a qualitative generalization (e.g., "both studies found elevated risk") for the grouped citation.

This constraint applies to ALL sections that cite specific numbers (Results, Discussion, Conclusions), not just the thematic synthesis. In the Discussion, qualitative generalizations (e.g., "the majority of studies suggest...") are permitted when supported by the aggregate pattern in the extraction, but any specific statistic must still come from the extraction file or be flagged.

**PICO outcome gap-fill**: After writing all theme subsections, consult the outcome coverage map from Step 1. For each PICO/PEO outcome with >5 articles that is NOT already covered by an existing theme heading (exact or semantic match), create a new subsection titled after the outcome (e.g., "### Predictive Factors of Response") and synthesize the relevant articles there. This ensures the Results section maps onto the protocol's framework, not only onto the emergent theme clusters. If an outcome has <=5 articles and no matching theme, fold it into the most relevant existing subsection and note it explicitly (e.g., "Regarding predictive factors, the limited evidence suggests…").

#### 4f. Results — Methodological Approaches

Omit this section unless the review includes >=10 studies with heterogeneous designs. When included, derive content exclusively from `quality.design` and `quality.recommended_tool` fields across articles in `extracted_claims.json` — do not generalize beyond what the extraction data supports. Summarize: study design distribution, quality assessment tools used, and any notable methodological patterns.

#### 4g. Results — Knowledge Gaps

Identify gaps in the evidence base: unanswered questions, underrepresented populations, methodological limitations across studies.

#### 4h. Discussion

- Main findings (top 3-5 takeaways, linked to research questions)
- Interpretation in context
- Implications (clinical practice, policy, future research)
- Strengths and limitations of the review itself
- **Required limitation items** (always include all applicable):
  1. **AI-assisted timeline**: state that search, screening, extraction, and synthesis were conducted with AI assistance on a single-day timeline, with the date. Example: "This review was conducted with AI-assisted tools on [date], with human verification at each phase gate."
  2. **Skipped phases**: check `screening_log.md` — if no `## Citation Snowballing` section is present, state that citation chaining (snowballing) was not performed and note this as a coverage limitation. For other skipped optional phases (e.g., full-text screening), apply the same pattern.
  3. **Grey literature coverage**: check `search_log.md` — if the `### Grey literature` section shows "Sources checked by user: none" or no grey literature section exists, state that grey literature and institutional guidelines were not systematically searched.

#### 4i. Conclusions

Concise conclusions addressing each research question. Evidence certainty statement.

#### 4j. BibTeX block

Add a `bibtex` fenced code block in the `# References` section (before the appendices) with entries for all cited references. This block is read by MCP `generate_bibliography` in Phase 6 to produce the authoritative `references.bib`.

Build entries from article metadata in `combined_results.json`. Include `volume`, `number`, and `pages` when available. If metadata is incomplete for an article (e.g., snowball additions with partial fields), build the entry from available fields and add `<!-- INCOMPLETE: missing [field] -->`.

**Do NOT generate DOI fields in BibTeX entries.** DOIs are frequently hallucinated or misattributed when generated by LLMs. Include only PMID-based identifiers. The MCP `generate_bibliography` tool will resolve DOIs from PMIDs during Phase 6.

```bibtex
@article{Key_Year,
  author  = {LastName, FirstName and LastName, FirstName},
  title   = {Article title},
  journal = {Journal Name},
  year    = {2024},
  pmid    = {12345678}
}
```

#### 4k. Appendices

Include relevant appendices based on review type:
- Appendix A: Search strings (from `search_results.md`) — always included
- Appendix B: PRISMA checklist (systematic/scoping only)
- Appendix C: Excluded studies (from `screening_log.md`) — optional for rapid reviews
- Appendix D: Quality assessment details (from `extracted_claims.json`) — optional for narrative/rapid reviews
- Appendix E: Data extraction form — always included as a template placeholder
- Appendix F: Meta-analysis details (meta-analysis only)
- Appendix G: Author contacts — optional, include if contact was attempted

When an appendix is optional and the data exists in the prerequisite files, include it. Otherwise, omit the section entirely (no empty placeholder).

The template also contains `# Declarations`, `# Supplementary Materials`, and `# Review Metadata` sections. Fill these with available information (dates from `search_results.md`, review type, etc.) or leave placeholders for the user to complete manually.

### Step 5 — Self-check

Before declaring done, verify:

1. Every theme from `extracted_claims.json` has a corresponding Results subsection
2. Every included article is cited at least once
3. All numeric claims in the text appear in `extracted_claims.json` for the cited article, or are flagged with `<!-- UNVERIFIED -->`. Report the count of UNVERIFIED flags but do not treat them as failures
4. No study-by-study structure in the thematic synthesis (synthesis ACROSS studies). Exception: single-article themes (per Step 4e) are not flagged
5. Pandoc citation syntax is consistent (`[@LastName_Year]` forms throughout)
6. BibTeX block at the end contains an entry for every cited key
7. YAML header references `references.bib` and includes the CSL file
8. **PICO/PEO outcome coverage** (BLOCKING): if `protocol.md` defines a framework with named outcomes or concepts (e.g., PICO outcomes, PEO exposures), cross-check each outcome from the outcome coverage map (Step 1) against the Results headings. For each outcome with >5 articles and no matching section/subsection: **create the subsection now** (do not just flag it — the gap-fill instruction in Step 4e should have caught this, but this check is the backstop). For outcomes with <=5 articles, verify they are mentioned in an existing subsection. Report the outcome coverage map with PASS/FAIL per outcome
9. **No DOIs in BibTeX block**: verify that no `doi = {` field appears in the embedded BibTeX entries. DOIs are resolved by MCP `generate_bibliography` in Phase 6

For large reviews (>20 articles), perform the numeric claim check (item 3) section by section rather than on the full document at once.

Print the self-check results. If any item fails, fix it before proceeding.

## Review Type Adaptations

### Systematic Review

Full document with all sections. PRISMA checklist in Appendix B. Quality assessment with formal tools. GRADE summary of findings table if enough homogeneous studies.

### Meta-Analysis

Same as systematic, plus:
- Appendix F: statistical software, model choice (random/fixed effects with justification), sensitivity analyses
- Forest plot descriptions in Results (actual plots require R/Python — note this as a manual step)
- Heterogeneity reporting (I², tau², prediction intervals)
- Publication bias assessment (funnel plot description, Egger's test if applicable)

### Scoping Review

Follow PRISMA-ScR. Differences from systematic:
- Quality assessment section shortened or omitted (note: "Per PRISMA-ScR, formal quality assessment is not required for scoping reviews")
- No GRADE table and no per-theme GRADE certainty ratings
- Results focus on mapping the evidence landscape rather than synthesizing effect estimates
- Knowledge gaps section is more prominent

### Narrative Review

Lighter structure:
- PRISMA flow may be simplified (no formal diagram required, but counts still reported)
- Quality assessment may use simplified approach (Oxford CEBM levels or informal Low/Moderate/High)
- No GRADE table and no per-theme GRADE certainty ratings
- More interpretive latitude in discussion
- Appendices B and D optional

### Rapid Review

Same as narrative, plus:
- Note methodological shortcuts as limitations (fewer databases, combined title/abstract screening, simplified quality assessment)
- Shorter document overall
- Appendices optional except search strings (Appendix A)

## Output Files

All outputs go in `review/` at the project root:

- **`review/<topic>_review.md`** — main review document with Pandoc citations and BibTeX block
- **`review/vancouver.csl`** — citation style (copied from assets)

## Orchestrated Mode

When called from `litrev` orchestrator, this skill covers Phase 5 (Gate 5). The orchestrator expects:

- Gate 5: `review/<topic>_review.md` exists with all sections complete, YAML header, thematic synthesis, BibTeX block

The orchestrator's Phase 5 instructions are replaced by this skill's workflow.
