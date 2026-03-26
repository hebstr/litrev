---
name: litrev
context: fork
description: Conduct systematic reviews, scoping reviews, meta-analyses, and evidence syntheses for medical, clinical, and health research. Also triggers for medical/health topics: state-of-the-art summaries, evidence maps, clinical practice guidelines, or requests to summarize/synthesize published studies — including functional descriptions like "what does the evidence say about [medical topic]", "what do we know about [medical topic]", "what does the science say about [medical topic]", "what have studies found on [medical topic]", "summarize the research on [medical topic]", "go through all the studies on [treatment/condition]", "combine the results across trials", "find gaps in the literature on [medical topic]", "pull together the evidence on [medical topic]", "what's been published on [medical topic]", "pooled estimates", "pooled analysis", "pooled data", or "revue de la littérature / revue systématique / méta-analyse / synthèse des preuves / état de l'art / état des connaissances / guide de pratique clinique / passer en revue les études sur / aperçu de ce qui a été publié sur / résumer les études sur". Also triggers for informal variants: "lit review on [medical topic]". Searches PubMed/MEDLINE, EMBASE, Cochrane CENTRAL, ClinicalTrials.gov, and other medical databases following PRISMA 2020, Cochrane, and GRADE methodologies. Creates markdown documents with BibTeX references and verified citations. Do NOT trigger for: non-medical domains (software engineering, education, environmental science, social sciences, etc.) even if using review methodology vocabulary, formatting existing manuscripts, writing BibTeX cleanup scripts, drawing PRISMA diagrams in code, explaining database search methodology, explaining PRISMA/Cochrane/GRADE methodology without conducting a review, or brief factual summaries on medical topics when the user explicitly declines a structured review.
allowed-tools: Read Write Edit Bash WebFetch WebSearch
---

# Literature Review — Orchestrator

## Pre-loaded pipeline state

### Working directory
!`pwd`

### Review artifacts found
!`ls -1 review/ 2>/dev/null || echo "(no review/ directory yet)"`

### Protocol (if exists)
!`head -30 review/protocol.md 2>/dev/null || echo "(no protocol yet)"`

### Git status of review/
!`git log --oneline -5 -- review/ 2>/dev/null || echo "(no git history for review/)"`

Sequence six sub-skills into a complete literature review pipeline. This skill contains **no domain-execution logic** — it handles planning, sequencing, gates, and error recovery. All domain work is delegated to sub-skills.

## Pipeline

```
Planning → litrev-search → litrev-screen → litrev-snowball (optional) → litrev-extract → litrev-synthesize → litrev-verify → Final QC
```

## Sub-skills

| Phase | Skill | Purpose |
|-------|-------|---------|
| 2 | `litrev-search` | Multi-database search + aggregation |
| 3a | `litrev-screen` | Title / abstract / full-text screening |
| 3b | `litrev-snowball` | Citation chaining (backward + forward) |
| 4 | `litrev-extract` | Claim extraction + quality assessment |
| 5 | `litrev-synthesize` | Constrained thematic writing |
| 6 | `litrev-verify` | Citation verification, BibTeX, claims audit |

Each sub-skill can be invoked independently (standalone mode) or by this orchestrator (orchestrated mode). In orchestrated mode, sub-skills read their inputs from the conversation context and `review/` files — they do not re-ask the user for information already established.

## Invoking Sub-skills

Use the **Skill tool** to invoke each sub-skill by name (e.g., `skill: "litrev-search"`). The sub-skill loads its own SKILL.md and executes within the current conversation — it has access to the full conversation context and the `review/` directory. Do not attempt to read or execute sub-skill instructions directly; let the Skill tool handle loading.

## Execution Tracker

MANDATORY: Copy this tracker into your first message and update it as you complete each phase. Mark each gate as PASSED only after verifying ALL conditions listed.

If resuming a previous session, check `review/` for existing files and reconstruct tracker state before continuing (see Session Resumption).

```
- [ ] Phase 1 Planning
  - [ ] GATE 1: protocol printed (question, framework, scope, criteria, databases, search terms)
- [ ] Phase 2 Search (litrev-search)
  - [ ] GATE 2: review/combined_results.json + review/search_results.md + review/search_log.md exist
- [ ] Phase 3a Screening (litrev-screen)
  - [ ] GATE 3a: review/screening_log.md + review/included_indices.json exist, PRISMA counts printed
- [ ] Phase 3b Snowballing (litrev-snowball) — optional per review type
  - [ ] GATE 3b: Citation Snowballing section in screening_log.md with Status: COMPLETE
- [ ] Phase 4 Extraction (litrev-extract)
  - [ ] GATE 4: review/extracted_claims.json exists, summary table + quality ratings printed
- [ ] Phase 5 Synthesis (litrev-synthesize)
  - [ ] GATE 5: review/<topic>_review.md exists with all sections, BibTeX block present
- [ ] Phase 6 Verification (litrev-verify)
  - [ ] GATE 6: review/references.bib + review/claims_audit.json exist, verification summary printed
- [ ] Phase 7 Final Quality Check
  - [ ] GATE 7: quality checklist printed, all items PASS
```

## Setup

```bash
mkdir -p review
```

All output files go in `review/` under the current working directory. If `review/` already contains files, ask the user whether to resume an existing review or start fresh. When resuming, verify the topic in any existing `*_review.md` matches the current request — if mismatch, ask fresh-or-different-directory. Starting fresh requires explicit user confirmation, then: `rm -rf review && mkdir -p review`.

## Phase 1: Planning and Scoping

This is the only phase handled directly by the orchestrator (not delegated).

1. **Define Research Question** using the appropriate framework. Selection rule: use **PICO/PICOS** when the question is about an intervention or treatment effect; use **PEO** when investigating an exposure, risk factor, or etiology without an explicit intervention; use **SPIDER** for qualitative or mixed-methods questions. When a question straddles two frameworks, prefer PEO for etiological questions and PICO only when an explicit intervention is being evaluated.
   - **PICO/PICOS**: Population, Intervention, Comparison, Outcome (+Study design)
   - **PEO**: Population, Exposure, Outcome
   - **SPIDER**: Sample, Phenomenon of Interest, Design, Evaluation, Research type

2. **Establish Scope**: review type (systematic, scoping, narrative, meta-analysis, rapid), time period, geographic scope, study types. If the user requests an umbrella review (review of reviews), inform them this type is not yet supported and suggest a systematic review of primary studies instead.

3. **Develop Search Strategy**: 2-4 main concepts, synonyms/abbreviations, Boolean operators, minimum 3 databases (2 for rapid). If the user insists on fewer, warn that the search may be insufficient, document the limitation in the protocol, and proceed if they confirm.

4. **Set Inclusion/Exclusion Criteria**: date range, language, publication types, study designs

5. **Review type not specified?** Ask before proceeding. If the user's response does not map to one of the five review types (systematic, scoping, narrative, meta-analysis, rapid), default to narrative review and mention that the scope can be escalated later.

### === GATE 1 ===

Print a protocol summary with: research question, framework (with each component filled), review type, time period, databases (>= 3, or >= 2 for rapid), search concepts with synonyms, inclusion criteria, exclusion criteria. Every field must be filled before proceeding.

**Persist the protocol**: write the protocol summary to `review/protocol.md` so it survives session boundaries. On session resumption, read `review/protocol.md` to restore the research question, framework, review type, criteria, and search strategy.

## Phase 2: Search

Invoke `litrev-search` in orchestrated mode. The protocol from Phase 1 provides all required inputs.

### === GATE 2 ===

Verify these files exist and are non-empty:
- `review/combined_results.json` — at least 1 article
- `review/search_results.md` — contains a results table
- `review/search_log.md` — documents search attempts

If any is missing, the search phase did not complete — diagnose and re-invoke `litrev-search`.

## Phase 3a: Screening

Invoke `litrev-screen` in orchestrated mode. Pass the inclusion/exclusion criteria from Phase 1.

### === GATE 3a ===

Verify:
- `review/screening_log.md` exists with all applicable steps marked `Status: COMPLETE`
- `review/included_indices.json` exists and is a valid JSON array
- PRISMA counts are printed. For systematic/meta-analysis/scoping: identified → deduplicated → title-screened → abstract-screened → included. For narrative/rapid (simplified): identified → deduplicated → screened → included
- Counts are arithmetically consistent

Zero-result detection: check `review/included_indices.json` — if empty array `[]`, screening returned zero articles. Do not proceed to Phase 3b — discuss with the user (broaden criteria, expand search, or report absence of evidence).

If the user chooses to report absence of evidence: skip Phases 3b, 4, and 6. Invoke `litrev-synthesize` (Phase 5) with the instruction to produce a short review documenting the null result — search strategy, screening outcome, and conclusion that no eligible studies were found. In Phase 7, mark items 1-4, 8, and 9 as N/A (no citations, no bibliography, no claims, no thematic organization needed).

If fewer than 5 articles are included, warn the user that the evidence base is thin before proceeding.

## Phase 3b: Snowballing (optional)

Consult the review type routing table. For systematic and meta-analysis reviews, invoke `litrev-snowball` automatically. For scoping, narrative, and rapid reviews, recommend it to the user and invoke only if they accept. When offering, specify the variant from the routing table (both directions for scoping, backward only for narrative, forward only capped at 5 seeds for rapid).

### === GATE 3b ===

Verify:
- `review/screening_log.md` contains a `## Citation Snowballing` section with `Status: COMPLETE`
- If candidates were merged, `review/included_indices.json` has been updated

If snowballing was skipped, mark GATE 3b as N/A and proceed.

## Phase 4: Extraction

Invoke `litrev-extract` in orchestrated mode.

### === GATE 4 ===

Verify:
- `review/extracted_claims.json` exists and is valid JSON with at least 1 article in `articles`
- Summary table was printed with columns: Author (Year), Design, N, Quality, Key Finding, Theme(s)
- Quality ratings and theme assignments are present (quality may be null for scoping reviews). See `litrev-extract` for quality assessment details per review type.

## Phase 5: Synthesis

Invoke `litrev-synthesize` in orchestrated mode.

### === GATE 5 ===

The `<topic>` slug is determined by `litrev-synthesize`. The orchestrator detects existing review files by glob pattern `review/*_review.md`.

Verify `review/<topic>_review.md` exists and contains:
- YAML header declaring `bibliography: references.bib` (the file itself is created in Phase 6 — do not check for its existence here)
- Introduction, Methodology, Results (organized by themes), Discussion, Conclusions
- At least one `[@` Pandoc citation
- A `bibtex` fenced code block with draft reference entries (consumed by `litrev-verify` in Phase 6 to produce the authoritative `references.bib`)

## Phase 6: Verification

Invoke `litrev-verify` in orchestrated mode.

### === GATE 6 ===

Verify:
- `review/references.bib` exists with at least 1 entry
- `review/claims_audit.json` exists
- `review/<topic>_review_citation_report.json` exists
- Verification summary was printed (DOIs verified/failed, claims verified/unverified)

## Phase 7: Final Quality Check

Print each item and mark PASS or FAIL. If any item is FAIL, fix it using the corrective action below. If not resolved after 2 attempts (2 distinct corrective actions), mark FAIL (UNRESOLVABLE), document the reason, and proceed.

Corrective actions by item:
- Items 1-3: re-invoke `litrev-verify`
- Item 4: edit `review/<topic>_review.md` directly (fix citation syntax)
- Items 5-7: edit `review/<topic>_review.md` directly (add missing sections)
- Item 8: re-invoke `litrev-synthesize` (restructure results)
- Item 9: re-invoke `litrev-extract` (redo quality assessment)
- Item 10: edit `review/<topic>_review.md` directly (add limitations)

```
1. All resolvable DOIs verified?                            [PASS/FAIL]
2. references.bib exists and referenced in YAML header?     [PASS/FAIL]
3. Claims audit completed, hallucinated claims fixed?       [PASS/FAIL]
4. Citations use consistent Pandoc syntax?                  [PASS/FAIL]
5. PRISMA flow documented?                                  [PASS/FAIL or N/A]
6. Search methodology fully documented?                     [PASS/FAIL]
7. Inclusion/exclusion criteria clearly stated?             [PASS/FAIL]
8. Results organized thematically (not study-by-study)?     [PASS/FAIL]
9. Quality assessment completed?                            [PASS/FAIL or N/A]
10. Limitations acknowledged?                               [PASS/FAIL]
```

## Review Type Routing

Each sub-skill handles its own adaptations internally. The orchestrator's role is to route correctly:

| Review Type | Databases | Screening | Snowballing | Quality | PRISMA |
|-------------|-----------|-----------|-------------|---------|--------|
| Systematic | >= 3 | Title + Abstract + Full-text | Recommended (both) | Full (RoB/GRADE) | Full PRISMA 2020 |
| Meta-analysis | >= 3 | Title + Abstract + Full-text | Recommended (both) | Full (RoB/GRADE) | Full PRISMA 2020 |
| Scoping | >= 3 | Title + Abstract + Optional FT | Recommended (both) | Optional (PRISMA-ScR) | PRISMA-ScR |
| Narrative | >= 2 | Title + Abstract + Optional FT | Optional (backward) | Simplified | Simplified |
| Rapid | >= 2 | Combined title/abstract | Optional (forward, cap 5) | Simplified | Simplified |

Gate adjustments by review type:
- **Gate 3b**: N/A when snowballing is skipped
- **Gate 4 quality**: may be null for scoping reviews
- **Gate 5 PRISMA**: simplified flow acceptable for narrative/rapid
- **Gate 7 items 5 and 9**: N/A where indicated above

## Session Resumption

When `review/` already contains files, reconstruct the pipeline state:

| File | Indicates |
|------|-----------|
| `protocol.md` | Gate 1 passed — read to restore research question, framework, review type, criteria, search strategy |
| `combined_results.json` | Gate 2 input ready |
| `search_results.md` + `search_log.md` | Gate 2 passed |
| `screening_log.md` (check for `Status: COMPLETE` on each section) | Gate 3a progress |
| `included_indices.json` | Gate 3a passed |
| `screening_log.md` with `## Citation Snowballing` + `Status: COMPLETE` | Gate 3b passed |
| `extracted_claims.json` | Gate 4 passed |
| `*_review.md` (glob `review/*_review.md`) | Gate 5 in progress or passed (check for all sections). If missing required sections, re-invoke `litrev-synthesize` — it detects existing files and resumes. If multiple files match, ask the user which to use. |
| `references.bib` | Gate 6 partially passed (bibliography generated) |
| `claims_audit.json` + `*_review_citation_report.json` | Gate 6 passed (all three outputs present) |

Resume from the first incomplete gate. Tell the user which phases are already done.

## Error Recovery

If a sub-skill fails:

1. **Missing input file**: identify which upstream phase produces the missing file (see Interface Contracts below) and re-run that phase
2. **Gate not passed**: re-invoke the sub-skill for that phase — do not skip the gate
3. **Zero results at screening**: discuss with the user (broaden criteria, expand search, or report absence)
4. **API failures during search/verify**: the sub-skills handle retries internally — if still failing, document the failure and ask the user whether to proceed with partial results or retry later

## Interface Contracts

| Skill | Reads | Writes |
|-------|-------|--------|
| litrev-search | Protocol from conversation | `combined_results.json`, `search_results.md`, `search_log.md` |
| litrev-screen | `search_results.md`, `combined_results.json`, criteria | `screening_log.md`, `included_indices.json` |
| litrev-snowball | `combined_results.json`, `included_indices.json`, criteria | `chaining_candidates.json`, updates `combined_results.json` + `included_indices.json` on merge |
| litrev-extract | `combined_results.json`, `included_indices.json` | `extracted_claims.json` |
| litrev-synthesize | `extracted_claims.json`, `screening_log.md`, `search_results.md`, `combined_results.json` | `<topic>_review.md`, `vancouver.csl` |
| litrev-verify | `<topic>_review.md`, `extracted_claims.json` | `references.bib`, `claims_audit.json`, `<topic>_review_citation_report.json` |

## Output Files

- `review/protocol.md` — persisted protocol (question, framework, review type, criteria, search strategy)
- `review/<topic>_review.md` — main review document
- `review/references.bib` — BibTeX bibliography
- `review/combined_results.json` — aggregated search results
- `review/search_results.md` — ranked search results table
- `review/search_log.md` — search documentation
- `review/screening_log.md` — screening decisions
- `review/included_indices.json` — included article indices
- `review/extracted_claims.json` — structured claims + quality + themes
- `review/claims_audit.json` — claims cross-verification report
- `review/<topic>_review_citation_report.json` — citation verification report
- `review/vancouver.csl` — citation style file
