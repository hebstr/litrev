---
name: literature-review
description: Conduct systematic reviews, meta-analyses, and evidence syntheses for medical and clinical research. Searches PubMed/MEDLINE, EMBASE, Cochrane CENTRAL, ClinicalTrials.gov, and other medical databases following PRISMA 2020, Cochrane, and GRADE methodologies. Creates markdown documents with BibTeX references and verified citations.
allowed-tools: Read Write Edit Bash WebFetch WebSearch
---

# Literature Review

Conduct systematic, comprehensive literature reviews following rigorous medical and clinical research methodology. Search multiple medical databases, synthesize findings thematically, verify all citations, and generate professional output documents.

## Execution Tracker

MANDATORY: Copy this tracker into your first message and update it as you complete each phase. Mark each gate as PASSED only after completing ALL requirements. DO NOT proceed past a gate until it is marked PASSED.

If resuming a previous session, check `review/` for existing files and reconstruct tracker state before continuing.

```
- [ ] Phase 1 Planning
  - [ ] GATE 1: protocol summary printed (question, framework, scope, criteria, databases, search terms)
- [ ] Phase 2 Search
  - [ ] GATE 2: process_results.py executed → review/search_results.md exists
- [ ] Phase 3 Screening
  - [ ] GATE 3: PRISMA counts printed (initial → deduplicated → title → abstract → included)
- [ ] Phase 4 Extraction
  - [ ] GATE 4a: study summary table + quality ratings printed
  - [ ] GATE 4b: extract_data.py executed → review/extracted_claims.json exists
- [ ] Phase 5 Synthesis
  - [ ] GATE 5: review document written → review/<topic>_review.md exists with all sections
- [ ] Phase 6 Verification
  - [ ] GATE 6a: verify_citations.py executed → all DOIs pass
  - [ ] GATE 6b: generate_bib.py executed → review/references.bib exists
  - [ ] GATE 6c: verify_claims.py executed → review/claims_audit.json exists, UNVERIFIED claims reviewed
- [ ] Phase 7 Final Quality Check
  - [ ] GATE 7: quality checklist printed and all items PASS
```

## Setup

```bash
SKILL_DIR=~/.claude/skills/literature-review
mkdir -p review
```

All output files go in the `review/` folder at the project root.

## Phase 1: Planning and Scoping

1. **Define Research Question** using the appropriate framework:
   - **PICO/PICOS** (intervention): Population, Intervention, Comparison, Outcome (+Study design)
   - **PEO** (etiology/exposure): Population, Exposure, Outcome
   - **SPIDER** (qualitative/mixed): Sample, Phenomenon of Interest, Design, Evaluation, Research type

2. **Establish Scope**: review type (systematic, scoping, narrative, meta-analysis), time period, geographic scope, study types

3. **Develop Search Strategy**: identify 2-4 main concepts, list synonyms/abbreviations, plan Boolean operators (AND, OR, NOT), select minimum 3 databases

4. **Set Inclusion/Exclusion Criteria**: date range, language, publication types, study designs — document all criteria clearly

### ═══ GATE 1 — MANDATORY BEFORE PHASE 2 ═══

Print a protocol summary with: research question, framework (PICO/PEO/SPIDER with each component filled), review type, time period, databases (≥ 3), search concepts with synonyms, inclusion criteria, exclusion criteria. Every field must be filled — if any is missing or vague, complete Phase 1 before proceeding.

## Phase 2: Systematic Literature Search

1. **Search minimum 3 databases** appropriate to the domain. For search syntax, read `references/database_strategies.md`.

   Primary: PubMed/MEDLINE (Entrez API), EMBASE (Ovid), Cochrane CENTRAL
   Supplementary: ClinicalTrials.gov, CINAHL, medRxiv, Semantic Scholar, OpenAlex

2. **Document search parameters** for each database: date searched, date range, exact search string, result count

3. **Export and aggregate results**: export JSON from each database, combine into `review/combined_results.json` (schema: `references/json_schema.md`)

4. **Prioritize high-impact papers** throughout: read `references/paper_prioritization.md` for citation thresholds and journal tiers

### ═══ GATE 2 — MANDATORY BEFORE PHASE 3 ═══

Phase 3 operates on `review/search_results.md`. This file is produced by `process_results.py`. If this file does not exist, Phase 3 CANNOT begin.

```bash
python "$SKILL_DIR/scripts/process_results.py" review/combined_results.json \
  --deduplicate \
  --format markdown \
  --output review/search_results.md \
  --rank citations \
  --top 20 \
  --summary
```

Options: `--rank citations|year|relevance`, `--year-start`/`--year-end`, `--study-type rct,cohort,...`, `--top N` (detail top N most-cited, default 20), `--format json|markdown|bibtex|ris`.

DO NOT proceed to Phase 3 until `review/search_results.md` exists and summary statistics are reviewed.

## Phase 3: Screening and Selection

1. **Title Screening**: screen titles in `review/search_results.md` table against inclusion/exclusion criteria, exclude irrelevant, document count excluded
2. **Abstract Screening**: extract abstracts for retained titles only, then apply criteria rigorously, document reasons for exclusion
   ```bash
   python "$SKILL_DIR/scripts/extract_abstracts.py" review/combined_results.json \
     --rows <space-separated row numbers from title screening>
   ```
3. **Full-Text Screening**: detailed review against all criteria, document specific exclusion reasons, record final included count
4. **Create PRISMA Flow Diagram**

After each screening step, append decisions to `review/screening_log.md` (retained row numbers, excluded row numbers with reasons). This file allows resuming screening if the session is interrupted.

### ═══ GATE 3 — MANDATORY BEFORE PHASE 4 ═══

Print PRISMA counts (no placeholders): identified → deduplicated → title-screened → abstract-screened → full-text assessed → included. Include exclusion reasons with counts at abstract and full-text stages. All numbers must be filled before proceeding.

## Phase 4: Data Extraction and Quality Assessment

1. **Extract Key Data** from each included study: metadata, study design, sample size, population, key findings, limitations, funding/conflicts

2. **Assess Study Quality** (select tool by study design):
   - **RCTs**: Cochrane RoB 2 | **Non-randomized**: ROBINS-I | **Observational**: Newcastle-Ottawa | **Diagnostic**: QUADAS-2 | **Reviews**: AMSTAR 2
   - Rate each study: Low, Some Concerns, or High risk of bias
   - Apply GRADE to rate certainty of evidence across outcomes (high/moderate/low/very low)

3. **Organize by Themes**: identify 3-5 major themes, group studies by theme, note patterns, consensus, and controversies

### ═══ GATE 4a — MANDATORY BEFORE GATE 4b ═══

Print a summary table of ALL included studies with columns: Author (Year), Design, N, Quality Rating (Low/Some Concerns/High), Key Finding, Theme(s). Then print: quality tool used, count per rating level, GRADE certainty per outcome, and list of themes with study counts. Every study must have a quality rating and theme assignment before proceeding.

### ═══ GATE 4b — EXTRACT QUANTITATIVE CLAIMS ═══

Extract all numerical claims from included article abstracts into a structured JSON. This file is the **single source of truth** for numbers that may be cited in the review.

```bash
uv run python "$SKILL_DIR/scripts/extract_data.py" review/combined_results.json \
  --rows <space-separated row numbers of included articles> \
  --fetch-abstracts \
  --output review/extracted_claims.json
```

Options: `--rows` or `--dois` to select articles, `--fetch-abstracts` to retrieve missing abstracts from PubMed via PMID (recommended).

Review the output statistics. If many articles lack abstracts, note this — those articles' numbers will require manual full-text verification later.

DO NOT proceed to Phase 5 until `review/extracted_claims.json` exists.

## Phase 5: Synthesis and Analysis

1. **Create Review Document**:
   ```bash
   cp "$SKILL_DIR/assets/review_template.md" review/<topic>_review.md
   cp "$SKILL_DIR/assets/vancouver.csl" review/vancouver.csl
   ```
   The template YAML header is Quarto/Pandoc-compatible and can be rendered to HTML/PDF/DOCX directly.

2. **Write Thematic Synthesis** — organize by themes, NOT study-by-study. Synthesize across studies, compare/contrast, identify consensus and controversies. Use Pandoc citation syntax: `[@Key_Year]`, `[@key1; @key2]`, `[-@Key_Year]`.

   **CRITICAL — Constrained writing**: When citing specific numbers (prevalences, OR, HR, percentages, p-values, sample sizes, rates), you MUST only use values that appear in `review/extracted_claims.json` for the corresponding article. Read the extraction file before writing. If a number is not in the extraction (e.g., only in the full-text), either omit it or flag it with `<!-- UNVERIFIED: value from full-text, not in abstract -->` in the markdown.

3. **Critical Analysis**: evaluate methodological strengths/limitations, assess evidence quality and consistency, identify knowledge gaps

4. **Write Discussion**: interpret findings in context, discuss implications, acknowledge review limitations, propose future research directions

For best practices and pitfalls to avoid, read `references/best_practices.md`.

### ═══ GATE 5 — MANDATORY BEFORE PHASE 6 ═══

Verify `review/<topic>_review.md` is complete: YAML header, Introduction, Methods (with search strategy), Results (organized by themes, not study-by-study — all themes from GATE 4 covered), Discussion, Limitations, all `[@citations]` use valid BibTeX keys, BibTeX reference block at end of `.md`. If any section is missing, complete Phase 5 before proceeding.

## Phase 6: Citation Verification

**STOP. Do NOT skip this phase.** All citations must be verified before Phase 7.

### ═══ GATE 6a — VERIFY ALL CITATIONS ═══

```bash
uv run python "$SKILL_DIR/scripts/verify_citations.py" review/<topic>_review.md \
  --timeout 15 --no-retractions
```

Options: `--timeout SECONDS` (default: 10), `--no-retractions` (skip retraction checks), `--output FILE` (JSON report path).

Review the generated `review/<topic>_review_citation_report.json`. Fix any failed DOIs and re-run until all pass.

### ═══ GATE 6b — GENERATE BIBLIOGRAPHY ═══

Phase 7 requires `review/references.bib`. This file is produced by `generate_bib.py`. If this file does not exist, Phase 7 CANNOT begin.

```bash
uv run python "$SKILL_DIR/scripts/generate_bib.py" review/<topic>_review.md \
  --output review/references.bib
```

Review cross-verification output: fix any mismatches between markdown references and generated BibTeX entries.

### ═══ GATE 6c — VERIFY NUMERICAL CLAIMS ═══

Cross-verify all numerical claims in the review against the extracted data from abstracts.

**Step 1 — First verification pass:**

```bash
uv run python "$SKILL_DIR/scripts/verify_claims.py" review/<topic>_review.md \
  --claims review/extracted_claims.json \
  --output review/claims_audit.json
```

**Step 2 — Enrich with full-text**: if many claims are UNVERIFIED, fetch full-text articles (PMC → Unpaywall → Sci-Hub) to extract additional claims:

```bash
uv run python "$SKILL_DIR/scripts/fetch_fulltext.py" review/claims_audit.json \
  --extraction review/extracted_claims.json \
  --bib review/references.bib \
  --output review/extracted_claims.json
```

This tries open-access sources first (PMC, Unpaywall), then Sci-Hub as fallback for UNVERIFIED articles. Extracted claims are merged into `extracted_claims.json`.

**Step 3 — Re-verify** with enriched data:

```bash
uv run python "$SKILL_DIR/scripts/verify_claims.py" review/<topic>_review.md \
  --claims review/extracted_claims.json \
  --output review/claims_audit.json
```

Review the audit report. For each status:
- **VERIFIED**: number confirmed in the article's abstract — no action needed
- **UNVERIFIED**: number NOT found in the abstract — either correct from full-text (add `<!-- VERIFIED: full-text -->` comment) or hallucinated (fix immediately)
- **NO_ABSTRACT**: article had no abstract — manual check required against full-text
- **NO_EXTRACTION**: article missing from extraction — re-run extract_data.py with correct rows

Fix all hallucinated claims before proceeding. Print the summary counts.

**Maintain a `bibtex` code block** at the end of the `.md` listing all cited references (see `references/bibtex_format.md`). Keys follow `FirstAuthorLastName_Year` pattern (deduplicated with suffix a, b, c).

## Phase 7: Final Quality Check

### ═══ GATE 7 — FINAL QUALITY CHECK ═══

Print each item below and mark PASS or FAIL. If any item is FAIL, go back and fix it before delivering:

```
1. verify_citations.py executed, all DOIs verified?      [PASS/FAIL]
2. generate_bib.py executed, references.bib exists?      [PASS/FAIL]
3. verify_claims.py executed, claims audit reviewed?     [PASS/FAIL]
4. Citations formatted consistently (Pandoc syntax)?     [PASS/FAIL]
5. PRISMA flow diagram included?                         [PASS/FAIL or N/A]
6. Search methodology fully documented?                  [PASS/FAIL]
7. Inclusion/exclusion criteria clearly stated?          [PASS/FAIL]
8. Results organized thematically (not study-by-study)?  [PASS/FAIL]
9. Quality assessment completed (RoB/GRADE)?             [PASS/FAIL]
10. Limitations acknowledged?                            [PASS/FAIL]
11. references.bib referenced in YAML header?            [PASS/FAIL]
```

### Output Files

- `review/<topic>_review.md` — main review document
- `review/references.bib` — generated BibTeX bibliography
- `review/search_results.md` — processed search results
- `review/extracted_claims.json` — structured numerical claims from abstracts (source of truth)
- `review/<topic>_review_citation_report.json` — citation verification report
- `review/claims_audit.json` — cross-verification audit report (claims vs abstracts)
- `review/screening_log.md` — screening decisions (for session resumption)

## Review Type Adaptations

- **Systematic Review**: Use all phases and gates
- **Meta-Analysis**: Include Synthesis and Analysis section, Appendix F
- **Narrative Review**: May simplify methodology detail, all gates still apply
- **Scoping Review**: Follow PRISMA-ScR, may omit quality assessment

## Reference Files

- `references/database_strategies.md` — Database search syntax and strategies
- `references/bibtex_format.md` — BibTeX formatting guide
- `references/json_schema.md` — JSON schema for search results
- `references/paper_prioritization.md` — Citation thresholds, journal tiers, author assessment
- `references/best_practices.md` — Best practices and common pitfalls
- `references/resources.md` — Scripts inventory, external resources, dependencies

## Institutional Access

If the user has institutional access (university), two mechanisms are supported:

**VPN (recommended)**: Connect to the university VPN before running the skill. No configuration needed — `fetch_fulltext.py` will automatically access publisher PDFs via the DOI resolver. The cascade becomes: PMC → Unpaywall → **Publisher** → Sci-Hub.

**Database access (Phase 2)**: With VPN active, the user can search EMBASE/Ovid, Web of Science, Scopus, and CINAHL via their institution's web portal — search strategies are documented in `references/database_strategies.md`.

Without VPN, the skill works with free sources only (PubMed, PMC, Unpaywall, Semantic Scholar, OpenAlex, Sci-Hub). The publisher source is still attempted but will fail for paywalled articles.

## Dependencies

- **Python** >= 3.11
- **uv** (manages dependencies via `pyproject.toml`; run `uv sync` to install)
- **pdftotext** (from `poppler-utils`, used by `fetch_fulltext.py`)
