---
name: literature-review
description: Conduct systematic reviews, scoping reviews, meta-analyses, and evidence syntheses for medical, clinical, and health research. Also triggers for medical/health topics: state-of-the-art summaries, evidence maps, or requests to summarize/synthesize published studies — including functional descriptions like "what does the evidence say about [medical topic]", "go through all the studies on [treatment/condition]", "combine the results across trials", "find gaps in the literature on [medical topic]", or "revue de la littérature / revue systématique / méta-analyse / synthèse des preuves / état de l'art". Also triggers for informal variants: "lit review on [medical topic]". Searches PubMed/MEDLINE, EMBASE, Cochrane CENTRAL, ClinicalTrials.gov, and other medical databases following PRISMA 2020, Cochrane, and GRADE methodologies. Creates markdown documents with BibTeX references and verified citations. Do NOT trigger for: non-medical systematic reviews or evidence syntheses (software engineering, education, environmental science, etc.), formatting existing manuscripts, writing BibTeX cleanup scripts, drawing PRISMA diagrams in code, or explaining database search methodology.
allowed-tools: Read Write Edit Bash WebFetch WebSearch
---

# Literature Review

Conduct systematic, comprehensive literature reviews following rigorous medical and clinical research methodology. Search multiple medical databases, synthesize findings thematically, verify all citations, and generate professional output documents.

## Execution Tracker

MANDATORY: Copy this tracker into your first message and update it as you complete each phase. Mark each gate as PASSED only after completing ALL requirements. DO NOT proceed past a gate until it is marked PASSED.

If resuming a previous session, check `review/` for existing files and reconstruct tracker state before continuing. File → gate mapping: `combined_results.json` → Gate 2 input ready, `search_results.md` → Gate 2 passed, `screening_log.md` → Phase 3 in progress (check for `## Citation Chaining` section to determine if chaining step was completed), `extracted_claims.json` → Gate 4b passed, `<topic>_review.md` → Phase 5 in progress (verify Gate 5 conditions before proceeding), `references.bib` → Gate 6b passed, `claims_audit.json` → Gate 6c passed.

```
- [ ] Phase 1 Planning
  - [ ] GATE 1: protocol summary printed (question, framework, scope, criteria, databases, search terms)
- [ ] Phase 2 Search
  - [ ] GATE 2: process_results.py executed → review/search_results.md exists
- [ ] Phase 3 Screening, Selection, and Citation Chaining
  - [ ] GATE 3: PRISMA counts printed (initial → deduplicated → title → abstract → chaining → included)
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

All output files go in the `review/` folder at the project root. If `review/` already contains files, ask the user whether to resume an existing review or start fresh. Starting fresh requires explicit user confirmation, then: `rm -rf review && mkdir -p review`.

## Phase 1: Planning and Scoping

1. **Define Research Question** using the appropriate framework:
   - **PICO/PICOS** (intervention): Population, Intervention, Comparison, Outcome (+Study design)
   - **PEO** (etiology/exposure): Population, Exposure, Outcome
   - **SPIDER** (qualitative/mixed): Sample, Phenomenon of Interest, Design, Evaluation, Research type

2. **Establish Scope**: review type (systematic, scoping, narrative, meta-analysis), time period, geographic scope, study types

3. **Develop Search Strategy**: identify 2-4 main concepts, list synonyms/abbreviations, plan Boolean operators (AND, OR, NOT), select minimum 3 databases

4. **Set Inclusion/Exclusion Criteria**: date range, language, publication types, study designs — document all criteria clearly

5. **Review type not specified?** If the user does not specify a review type, ask before proceeding. If their response is ambiguous, default to narrative review (lighter gates apply per Review Type Adaptations) and mention that the scope can be escalated to systematic if needed.

### ═══ GATE 1 — MANDATORY BEFORE PHASE 2 ═══

Print a protocol summary with: research question, framework (PICO/PEO/SPIDER with each component filled), review type, time period, databases (≥ 3), search concepts with synonyms, inclusion criteria, exclusion criteria. Every field must be filled — if any is missing or vague, complete Phase 1 before proceeding.

## Phase 2: Systematic Literature Search

1. **Search minimum 3 databases** appropriate to the domain. For search syntax, read `references/database_strategies.md`.

   Primary: PubMed/MEDLINE (Entrez API), EMBASE (Ovid), Cochrane CENTRAL
   Supplementary: ClinicalTrials.gov, CINAHL, medRxiv, Semantic Scholar, OpenAlex

   If a primary database is inaccessible (e.g., EMBASE without institutional access), substitute a supplementary database to meet the 3-database minimum and document the substitution. If 2+ primary databases are inaccessible, document this as a significant limitation and confirm with the user before proceeding — a search relying mostly on supplementary databases may miss relevant studies.

2. **Document search parameters** for each database: date searched, date range, exact search string, result count

3. **Export and aggregate results**: use `WebFetch` to query database APIs (PubMed, Semantic Scholar, OpenAlex, ClinicalTrials.gov, medRxiv have public APIs; EMBASE, Scopus, Web of Science, CINAHL require institutional portal access — see Institutional Access), export JSON results, normalize each entry to the schema in `references/json_schema.md`, and concatenate all arrays into a single `review/combined_results.json`. Set the `source` field to the database of origin for each entry.

4. **Prioritize high-impact papers** throughout: read `references/paper_prioritization.md` for citation thresholds and journal tiers

### ═══ GATE 2 — MANDATORY BEFORE PHASE 3 ═══

Phase 3 operates on `review/search_results.md`. This file is produced by `process_results.py`. If this file does not exist, Phase 3 CANNOT begin.

```bash
uv run python "$SKILL_DIR/scripts/process_results.py" review/combined_results.json \
  --deduplicate \
  --format markdown \
  --output review/search_results.md \
  --rank citations \
  --top 20 \
  --summary
```

Options: `--rank citations|year|relevance`, `--year-start`/`--year-end`, `--study-type rct,cohort,...`, `--top N` (detail top N most-cited in summary section; full table of all results is always included; default 20), `--format json|markdown|bibtex|ris`.

DO NOT proceed to Phase 3 until `review/search_results.md` exists and summary statistics are reviewed.

## Phase 3: Screening, Selection, and Citation Chaining

1. **Title Screening**: screen titles in `review/search_results.md` table against inclusion/exclusion criteria, exclude irrelevant, document count excluded. If >200 articles remain after title screening, flag to the user that criteria may be too broad and discuss narrowing before proceeding to abstract screening.
2. **Abstract Screening**: extract abstracts for retained titles only, then apply criteria rigorously, document reasons for exclusion
   ```bash
   uv run python "$SKILL_DIR/scripts/extract_abstracts.py" review/combined_results.json \
     --rows <space-separated 0-based row numbers from title screening>
   ```
   Output prints to stdout (read in-session to screen). Use `--output FILE` to save to a file if needed.

   **Row numbering convention**: all `--rows` arguments across all scripts use **0-based** indices matching the `combined_results.json` array. The `#` column in `search_results.md` uses the same 0-based numbering. The `--top N` option only controls the detailed summary section; the full table always lists all results with their original indices.
3. **Full-Text Screening**: detailed review against all criteria, document specific exclusion reasons, record final included count

   If zero articles are retained at any screening step, stop and ask the user whether to broaden inclusion criteria, expand databases/search terms, or report the absence of evidence as a finding.

4. **Citation Chaining**: supplement database searches with backward and forward citation chaining to capture studies missed by keyword-based queries. For background on available tools and APIs, see `references/database_strategies.md` § Citation Chaining. The operational steps are below:

   a. **Select seed papers**: pick the 5–10 most relevant included studies from step 3. If fewer than 5 studies are included, use all of them as seeds

   b. **Run citation chaining**:
      ```bash
      uv run python "$SKILL_DIR/scripts/citation_chaining.py" review/combined_results.json \
        --rows <space-separated 0-based row numbers of seed papers> \
        --direction both \
        --merge
      ```
      Options: `--direction backward|forward|both` (default: both), `--sources s2,openalex` (default: both), `--merge` merges new candidates into `combined_results.json` (recommended). Without `--merge`, candidates are saved to `review/chaining_candidates.json` only.

   c. **Screen new candidates**: apply the same inclusion/exclusion criteria to newly found papers. If `--merge` was used, re-run `process_results.py` (Gate 2 command) to update `review/search_results.md`, then screen the new entries. **Warning**: re-running `process_results.py` may shift row indices. Cross-reference previously retained papers by title/DOI (not row number) against the updated table. Use the new indices for all subsequent `--rows` arguments.

   d. **Document**: append a `## Citation Chaining` section to `review/screening_log.md` with: seed papers used (row numbers), number of backward/forward candidates found, number retained after screening, exclusion reasons. Zero new inclusions is a valid outcome — state it explicitly.

5. **Create PRISMA Flow Diagram** as a Mermaid flowchart in the review document (include citation chaining as a separate identification source)

After each screening step, append decisions to `review/screening_log.md`. Use the format: `## Title Screening` (or `Abstract` / `Full-text` / `Citation Chaining`), then `Retained: 0 3 5 12` and `Excluded: 1 (wrong population), 2 (no outcome), ...`, ending with `Status: COMPLETE`. This file allows resuming screening if the session is interrupted — a section without `Status: COMPLETE` indicates the step was not finished and must be redone.

### ═══ GATE 3 — MANDATORY BEFORE PHASE 4 ═══

Print PRISMA counts (no placeholders): identified → deduplicated → title-screened → abstract-screened → full-text assessed → included from databases + included from citation chaining → total included. Include exclusion reasons with counts at abstract, full-text, and chaining stages. All numbers must be filled before proceeding.

## Phase 4: Data Extraction and Quality Assessment

1. **Extract Key Data** from each included study: metadata, study design, sample size, population, key findings, limitations, funding/conflicts

2. **Assess Study Quality** (select tool by study design):
   - **RCTs**: Cochrane RoB 2 | **Non-randomized**: ROBINS-I | **Observational**: Newcastle-Ottawa | **Diagnostic**: QUADAS-2 | **Reviews**: AMSTAR 2
   - Rate each study using the tool's native scale (RoB 2: Low/Some Concerns/High; ROBINS-I: Low/Moderate/Serious/Critical; Newcastle-Ottawa: 0–9 stars). For the Gate 4a summary table, map to three levels: Low / Moderate / High risk of bias
   - Apply GRADE to rate certainty of evidence across outcomes (high/moderate/low/very low). Consider the 5 downgrading domains (risk of bias, inconsistency, indirectness, imprecision, publication bias) and 3 upgrading domains (large effect, dose-response, residual confounding). See [GRADE handbook](https://gdt.gradepro.org/app/handbook/handbook.html)

3. **Organize by Themes**: identify 3-5 major themes, group studies by theme, note patterns, consensus, and controversies

### ═══ GATE 4a — MANDATORY BEFORE GATE 4b ═══

Print a summary table of ALL included studies with columns: Author (Year), Design, N, Quality Rating (Low/Moderate/High), Key Finding, Theme(s). Then print: quality tool(s) used (one per study design), count per rating level, GRADE certainty per outcome, and list of themes with study counts. Every study must have a quality rating and theme assignment before proceeding.

### ═══ GATE 4b — EXTRACT QUANTITATIVE CLAIMS ═══

Extract all numerical claims from included article abstracts into a structured JSON. This file is the **single source of truth** for numbers that may be cited in the review.

```bash
uv run python "$SKILL_DIR/scripts/extract_data.py" review/combined_results.json \
  --rows <space-separated 0-based row numbers of included articles> \
  --fetch-abstracts \
  --output review/extracted_claims.json
```

Options: `--rows` (0-based indices) or `--dois` to select articles, `--fetch-abstracts` to retrieve missing abstracts from PubMed via PMID (recommended).

Review the output statistics. If many articles lack abstracts, note this — those articles' numbers will require manual full-text verification later.

DO NOT proceed to Phase 5 until `review/extracted_claims.json` exists.

## Phase 5: Synthesis and Analysis

1. **Create Review Document**:
   ```bash
   cp "$SKILL_DIR/assets/review_template.md" review/<topic>_review.md
   cp "$SKILL_DIR/assets/vancouver.csl" review/vancouver.csl
   ```
   `<topic>` is a short snake_case slug derived from the first main concept in the PICO/PEO/SPIDER framework (e.g., `glp1_cardiovascular`, `probiotics_cdiff`, `ssri_adolescents`). Use the same slug consistently in all subsequent commands. When resuming, detect the existing `*_review.md` filename in `review/` rather than re-deriving the slug.

   The template YAML header is Quarto/Pandoc-compatible and can be rendered to HTML/PDF/DOCX directly.

2. **Write Thematic Synthesis** — organize by themes, NOT study-by-study. Synthesize across studies, compare/contrast, identify consensus and controversies. Use Pandoc citation syntax: `[@Key_Year]`, `[@key1; @key2]`, `[-@Key_Year]`.

   **CRITICAL — Constrained writing**: When citing specific numbers (prevalences, OR, HR, percentages, p-values, sample sizes, rates), you MUST only use values that appear in `review/extracted_claims.json` for the corresponding article. Read the extraction file before writing. If a number is not in the extraction (e.g., only in the full-text), either omit it or flag it with `<!-- UNVERIFIED: value from full-text, not in abstract -->` in the markdown.

3. **Critical Analysis**: evaluate methodological strengths/limitations, assess evidence quality and consistency, identify knowledge gaps

4. **Write Discussion**: interpret findings in context, discuss implications, acknowledge review limitations, propose future research directions

5. **Add BibTeX block**: include a `bibtex` fenced code block at the end of the document with all cited references (format: `references/bibtex_format.md`). This block is read by `generate_bib.py` at Gate 6b to produce the authoritative `references.bib`.

For best practices and pitfalls to avoid, read `references/best_practices.md`.

### ═══ GATE 5 — MANDATORY BEFORE PHASE 6 ═══

Verify `review/<topic>_review.md` is complete: YAML header, Introduction, Methods (with search strategy), Results (organized by themes, not study-by-study — all themes from GATE 4 covered), Discussion, Limitations, all `[@citations]` use valid BibTeX keys, BibTeX reference block at end of `.md`. For meta-analyses: Appendix F must be populated (statistical software, model, sensitivity analyses). If any section is missing, complete Phase 5 before proceeding.

## Phase 6: Citation Verification

**STOP. Do NOT skip this phase.** All citations must be verified before Phase 7.

### ═══ GATE 6a — VERIFY ALL CITATIONS ═══

```bash
uv run python "$SKILL_DIR/scripts/verify_citations.py" review/<topic>_review.md \
  --timeout 15
```

Options: `--timeout SECONDS` (default: 10), `--no-retractions` (skip retraction checks — faster but not recommended for systematic reviews), `--output FILE` (JSON report path).

Review the generated `review/<topic>_review_citation_report.json`. For each failed DOI: search for the correct DOI via CrossRef or PubMed. If no DOI exists (e.g., preprint, old publication), remove the `doi` field from the BibTeX entry but keep the citation. Re-run until all resolvable DOIs pass. If a DOI still fails after 2 correction attempts, treat it as unresolvable: remove the `doi` field and keep the citation.

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

**Step 2 — Enrich with full-text**: if many claims are UNVERIFIED, fetch full-text for those articles only (access cascade: PMC → Unpaywall → Publisher → Sci-Hub) and extract additional claims:

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
- **UNVERIFIED**: number NOT found in the abstract. If the claim has a `<!-- UNVERIFIED: ... -->` comment placed during Phase 5, this is expected — verify the number against the full-text source and replace with `<!-- VERIFIED: full-text -->`. If there is no such comment, the number may be hallucinated — check the source article and fix immediately if wrong
- **NO_ABSTRACT**: article had no abstract — manual check required against full-text
- **NO_EXTRACTION**: article missing from extraction — re-run extract_data.py with correct rows

A claim is hallucinated if the number does not appear in the source article at all, or is attributed to the wrong article. Fix all hallucinated claims (correct the number, fix the attribution, or remove the claim) before proceeding. Print the summary counts.

**Maintain a `bibtex` code block** at the end of the `.md` listing all cited references (see `references/bibtex_format.md`). This block is a cross-verification artifact read by `generate_bib.py` — the authoritative bibliography is the external `references.bib` generated at Gate 6b. Keys follow `FirstAuthorLastName_Year` pattern (deduplicated with suffix a, b, c).

## Phase 7: Final Quality Check

### ═══ GATE 7 — FINAL QUALITY CHECK ═══

Print each item below and mark PASS or FAIL. If any item is FAIL, go back and fix it before delivering:

```
1. verify_citations.py executed, all DOIs verified?      [PASS/FAIL]
2. generate_bib.py executed, references.bib exists?      [PASS/FAIL]
3. verify_claims.py executed, claims audit reviewed?     [PASS/FAIL]
4. Citations formatted consistently (Pandoc syntax)?     [PASS/FAIL]
5. PRISMA flow diagram included?                         [PASS/FAIL or N/A for narrative]
6. Search methodology fully documented?                  [PASS/FAIL]
7. Inclusion/exclusion criteria clearly stated?          [PASS/FAIL]
8. Results organized thematically (not study-by-study)?  [PASS/FAIL]
9. Quality assessment completed (RoB/GRADE)?             [PASS/FAIL or N/A]
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
- `review/chaining_candidates.json` — citation chaining candidates (only if `--merge` not used)

## Review Type Adaptations

- **Systematic Review**: Use all phases and gates
- **Meta-Analysis**: Use all phases and gates. Include meta-analysis details in Appendix F (template provided in `assets/review_template.md`: statistical software, model choice, code, sensitivity analyses)
- **Narrative Review**: All gates apply. Relaxations: Gate 3 PRISMA counts may use simplified flow (no formal diagram), Gate 4a quality assessment may use a simplified approach (e.g., Oxford CEBM levels of evidence, or informal Low/Moderate/High rating without a full tool) and may omit GRADE. All other gates (1, 2, 4b, 5, 6a–6c, 7) remain fully mandatory
- **Scoping Review**: Follow PRISMA-ScR. Relaxations: Gate 4a may omit quality assessment and GRADE. All other gates remain fully mandatory including Gates 4b and 6c (claim extraction and verification are independent of quality assessment)
- **Rapid Review**: Streamlined systematic review — use minimum 2 databases (instead of 3), simplified screening (title+abstract in one pass), narrative quality assessment (as per Narrative Review), may omit citation chaining. All verification gates (6a–6c) still apply. Note the methodological shortcuts as limitations in the review document

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
