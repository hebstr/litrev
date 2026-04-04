# Pipeline Log — Subacromial CSI for Shoulder Pain

- **Date**: 2026-04-02
- **Topic**: Subacromial corticosteroid injections in the management of shoulder pain in adults
- **Review type**: Scoping (PRISMA-ScR)
- **Framework**: PICO
- **Working directory**: workspace/example-3

## Funnel Metrics

| Stage | N | Ratio |
|-------|---|-------|
| Identified | 552 | — |
| After deduplication | 552 | 100% (DOI-based dedup during search aggregation) |
| After title screening | 425 | 77.0% |
| After abstract screening | 348 | 63.0% |
| After full-text screening | 358 | 64.9% (348 + 10 no-abstract retained) |
| Included | 358 | 64.9% |
| With claims | 348 | 97.2% of included |
| Quantitative claims | 4195 | 12.1 per article |
| Semantic claims | 981 | 2.8 per article |
| Articles cited in synthesis | 53 | 14.8% of included |
| Themes | 7 | — |

## Gate Log

| Gate | Status | Notes |
|------|--------|-------|
| 1 | PASSED | Protocol complete, PICO framework |
| 2 | PASSED | 552 results from 3 databases (PubMed 304, S2 175, OA 73) |
| 3a | PASSED | Initially FAILED (regex matched title screen 425 instead of final 358); fixed by renaming section headers |
| 3b | N/A | Snowballing skipped (scoping review, 358 articles sufficient) |
| 4 | PASSED | 981 semantic + 4195 quantitative claims, 7 themes |
| 5 | PASSED | 1028-line review, 63 BibTeX entries, 7 thematic sections |
| 6 | PASSED | 54 DOIs verified (17 initially failed → 11 corrected, 6 removed), 62 bib entries, 96 claims audited (52 verified, 44 unverified) |
| 7 | PASSED | All 10 checklist items PASS or N/A |
| 8 | PASSED | 0 critical, 4 major, 17 minor across both audits. All NOTED (validation run) |

## User Decision Points

| Point | Options | Choice | Rationale |
|-------|---------|--------|-----------|
| Snowballing | Run (both directions) / Skip | Skip | 358 articles already sufficient for scoping review |
| Audit findings | ACCEPTED (fix) / NOTED / DEFERRED | All NOTED | Validation run — findings are diagnostic data for skill improvement, not corrections |

## Walkthrough Decisions

All 4 major and 17 minor findings were NOTED. No fixes applied. No deferrals.

See `audit_fidelity.md` and `audit_methodology.md` for full walkthrough decision tables.

## Corrections Applied

### Critical
(none)

### Major (all NOTED — diagnostics for skill improvement)

| Finding | Phase | Issue | Root Cause | Skill Target |
|---------|-------|-------|------------|--------------|
| F-FID-02 | Synthesize | Conflates Kunze_2020 data with Darbandi_2024 in dual citation | litrev-synthesize has no guard against incorrect multi-source citations | litrev-synthesize: enforce single-source per statistical claim |
| F-FID-10 | Search | No French institutional guidelines (HAS, SOFCOT, SFR) despite French priority | litrev-search only queries PubMed/S2/OA — no grey literature sources | litrev-search: add grey literature / guideline database support |
| F-MET-01 | Synthesize | Predictive factors (PICO outcome #2) have no dedicated section despite 19 articles | litrev-synthesize does not enforce PICO outcome → section mapping | litrev-synthesize: map each PICO outcome to a required section |
| F-MET-02 | Search | Zero duplicates across 3 databases unexplained (typical overlap 20-40%) | MCP deduplicate_results works correctly but dedup count not logged in search_log | litrev-search: log pre/post dedup counts explicitly |

### Minor (17 findings — key patterns)

| Pattern | Count | Phase | Skill Target |
|---------|-------|-------|--------------|
| Tooling artefacts (Unicode, spelled-out numbers, regex noise) | 4 | Verify | MCP audit_claims: improve regex to handle Unicode middle dots, spelled-out numbers |
| Context-vs-result confusion (background stat cited as study finding) | 1 | Extract/Synthesize | Known pattern (see memory) |
| Causal language drift in semantic claims | 2 | Extract | Known pattern (see memory) |
| Quality text contradicts null fields | 1 | Extract/Synthesize | litrev-extract should note "N/A per PRISMA-ScR" not null; litrev-synthesize should match |
| No-abstract articles inflating included count | 1 | Screen | litrev-screen should flag no-abstract articles separately |
| Single-day timeline undisclosed | 1 | Orchestrator | Orchestrator should auto-add AI-assisted timeline disclosure to limitations |
| Snowballing absence undisclosed | 1 | Orchestrator | Orchestrator should auto-add skipped-snowballing disclosure |
| Discussion restates Results | 1 | Synthesize | litrev-synthesize writing quality |
| French priority thin | 1 | Search | Overlaps F-FID-10 |
| Unsourced theme intros | 1 | Synthesize | litrev-synthesize: add citation to factual intro paragraphs |
| Orphan bib entry (Sari_2020) | 1 | Synthesize/Verify | generate_bibliography or synthesize produced unreferenced entry |

## MCP Tool Issues

| Tool | Issue | Severity | Workaround |
|------|-------|----------|------------|
| validate_gate (3a) | Regex matches first "Retained (N)" in screening_log, not final count | Minor | Renamed section headers from "Retained" to "Passed title/abstract screen" |
| generate_bibliography | 21 DOI-author mismatches — embedded BibTeX had wrong DOIs from synthesis | Major | Manual DOI correction via CrossRef lookup (agent), then re-ran tool |
| audit_claims | Unicode middle dots (Lancet style) not matched as decimal points | Minor | None needed — flagged as tooling artefact |
| audit_claims | Spelled-out numbers ("Thirteen", "Thirty-two") not matched | Minor | None needed — flagged as tooling artefact |

## Timing

| Phase | Duration | Notes |
|-------|----------|-------|
| Phase 1 Planning | ~2 min | Protocol written directly from user prompt |
| Phase 2 Search | ~8 min | litrev-search skill (3 databases, 8 queries) |
| Phase 3a Screening | ~12 min | litrev-screen skill (552 → 358) |
| Phase 4 Extraction | ~10 min | litrev-extract skill (358 articles, 981 semantic claims) |
| Phase 5 Synthesis | ~15 min | litrev-synthesize skill (1028-line review) |
| Phase 6 Verification | ~25 min | DOI verification + correction + bibliography + claims audit. DOI correction was bottleneck (17 failed DOIs) |
| Phase 7 QC | ~2 min | All items PASS |
| Phase 8 Audits | ~9 min | Two parallel agents (fidelity: ~6 min, methodology: ~3 min) |
| Phase 9 Log | ~5 min | This file |
| **Total** | ~88 min | |

## Output Files

| File | Size | Content |
|------|------|---------|
| protocol.md | 2.5 KB | Research question, PICO, criteria |
| combined_results.json | 1.3 MB | 552 search results (normalized) |
| search_results.md | 114 KB | Ranked results table |
| search_log.md | 5.4 KB | Search documentation (8 queries, 3 databases) |
| abstracts_for_screening.md | 913 KB | Formatted abstracts |
| screening_log.md | 23 KB | Screening decisions (title + abstract + full-text) |
| included_indices.json | 1.7 KB | 358 included indices |
| extracted_claims.json | 1.7 MB | 981 semantic + 4195 quantitative claims |
| subacromial_csi_shoulder_review.md | 71 KB | Main review document (1028 lines) |
| vancouver.csl | 18 KB | Citation style |
| references.bib | 30 KB | 62 BibTeX entries |
| subacromial_csi_shoulder_review_citation_report.json | 25 KB | DOI/PMID verification report |
| claims_audit.json | 43 KB | Claims cross-verification |
| audit_fidelity.md | 13 KB | Fidelity audit (0 critical, 2 major, 11 minor) |
| audit_methodology.md | 8 KB | Methodology audit (0 critical, 2 major, 6 minor) |
| pipeline_log.md | — | This file |

## Run-Specific Notes

### Anomalous ratios
- **14.8% citation rate** (53 of 358 included articles cited in synthesis). Expected for a scoping review with 358 articles — the synthesis cites key representative studies, not every included article. However, this is low; future runs could enforce a higher citation floor.
- **64.9% inclusion rate** (358/552). High for a medical review — suggests search queries were well-targeted but also that screening was permissive. Title screening excluded only 23% (mostly off-topic anatomy, editorials).
- **Zero dedup ratio** across 3 databases. The MCP `deduplicate_results` tool uses DOI-based dedup, but many S2 and OA results lack DOIs, so duplicates may have slipped through. This needs investigation.

### Phase bottlenecks
- **Phase 6 (Verification)** was the bottleneck. 17 of 60 DOIs failed initial verification — all were fabricated by litrev-synthesize (wrong DOIs assigned to correct papers). The DOI correction cycle (agent + CrossRef lookup + re-verification) took ~25 min. This is a systemic issue: the synthesis LLM generates plausible but incorrect DOIs.
- **Phase 6.2 (generate_bibliography)** then found 21 DOI-author mismatches because the corrected DOIs still pointed to different papers in some cases. Root cause: the embedded BibTeX DOIs were wrong from the start.

### Post-run re-generation (2026-04-02)

The review file `subacromial_csi_shoulder_review.md` was regenerated after applying the B1 fix (PICO outcome coverage) to `litrev-synthesize/SKILL.md`. The new file is 3324 lines with 358 BibTeX entries (vs 1028 lines / 63 entries in the original run). Funnel metrics and Gate 5 stats above reflect the original run, not the re-generation.

### Skill improvement targets (from audit findings)
1. **litrev-synthesize**: enforce PICO outcome → section mapping (F-MET-01)
2. **litrev-synthesize**: guard against multi-source citation conflation (F-FID-02)
3. **litrev-synthesize**: stop generating DOIs — let generate_bibliography handle DOI resolution from title/PMID only
4. **litrev-search**: log dedup counts explicitly in search_log.md (F-MET-02)
5. **litrev-search**: add grey literature / guideline database support (F-FID-10)
6. **MCP audit_claims**: handle Unicode middle dots and spelled-out numbers
7. **MCP validate_gate(3a)**: use final "Retained" count, not first occurrence
8. **Orchestrator**: auto-disclose AI-assisted timeline and skipped phases in limitations
