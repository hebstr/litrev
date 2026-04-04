# Run Report — Scapulalgie Scoping Review

- **Date**: 2026-04-01
- **Topic**: Epidemiology of shoulder pain and rotator cuff pathologies in adults
- **Review type**: Scoping review (PRISMA-ScR)
- **Framework**: PEO
- **Language**: French synthesis
- **Context**: Introduction to PRISE protocol (CHU de Lille, SNDS + EDS INCLUDE)
- **Working directory**: `workspace/example-2/`

## Funnel Metrics

| Stage | N | Ratio |
|-------|---|-------|
| Identified (PubMed + S2) | 3,801 | — |
| After deduplication | 3,801 | 100% (dedup at search time) |
| After title screening | 1,802 | 47.4% |
| After abstract screening | 1,100 | 28.9% |
| After full-text (no-abstract only) | 1,114 | 29.3% |
| With at least one claim | 1,079 | 96.9% of included |
| Quantitative claims extracted | 5,924 | 5.3 per article |
| Semantic claims extracted | 3,503 | 3.1 per article |
| Articles cited in synthesis | ~53 | 4.8% of included |
| Themes identified | 8 | — |

**Key ratio**: 1,114 included from 3,801 identified (29.3%) — high retention, typical for broad scoping review with 4 outcome domains over 16 years.

## Gate Log

| Gate | Status | Notes |
|------|--------|-------|
| G1 Protocol | PASSED | First attempt |
| G2 Search | PASSED | 2 topical databases instead of 3 (OpenAlex off-topic). User chose option (c): proceed with limitation documented |
| G3a Screening | PASSED | First attempt. 1,114 included — user warned about large corpus |
| G3b Snowballing | N/A | Skipped per user decision (marginal value with 1,114 articles). Documented in limitations |
| G4 Extraction | PASSED | First attempt. MCP `extract_claims_regex` failed on custom paths — fell back to Python |
| G5 Synthesis | PASSED | Completed before rate limit hit. All sections present |
| G6 Verification | PASSED | Required DOI fixes (see Corrections below) |
| G7 Quality Check | PASSED | 10/10 items PASS or N/A |
| G8 Double Audit | PASSED | 2 critical + 4 major findings, all ACCEPTED and fixed |

## User Decision Points

| Point | Options presented | User choice | Rationale |
|-------|-------------------|-------------|-----------|
| Database coverage (2 vs 3) | (a) retry OpenAlex, (b) add medRxiv, (c) proceed with 2, (d) manual export | (c) proceed | PubMed coverage sufficient, snowball as safety net |
| Corpus reduction | Tighten criteria vs proceed | Proceed | Extraction naturally filters; reducing risks bias |
| Snowballing | Recommended but optional for scoping | Skip | 1,114 articles already large; marginal value |
| Minor audit findings (batch) | Individual vs batch approval | Batch approval | Efficient for 7 minor findings |

## Corrections Applied (Walkthrough)

### Critical (2)

| Finding | Issue | Fix |
|---------|-------|-----|
| F-FID-01 | 9 BibTeX entries with DOIs pointing to unrelated articles | Removed erroneous DOIs, kept PMID-based entries |
| F-FID-02 | "30-40% des MP" cited to wrong Roquelaure article | Replaced with "87% des MP reconnues" (CNAM data), removed citation |

### Major (4)

| Finding | Issue | Fix |
|---------|-------|-----|
| F-FID-08 | No French institutional reports (CNAM, DARES, INRS) | Expanded limitations section with specific missing sources |
| F-MET-01 | "No deviation" declared despite OpenAlex dropout | Rewrote Deviations section documenting OpenAlex removal |
| F-MET-02 | No deduplication step in PRISMA flow | Added dedup step with explanatory note |
| F-MET-03 | "confirmer" x9, no contradiction analysis | Added divergent-results paragraph in Discussion (Yang vs Sandler, Chester vs De Baets, Yamamoto vs Littlewood) |

### Minor (accepted, 4 fixed)

| Finding | Fix |
|---------|-----|
| F-FID-06 | "directement influencee" → "associee a" |
| F-FID-10 | "la seule contrainte" → "la principale" |
| F-MET-04/05/06 | Added 3 limitations (LLM screening, no snowball, single-day process) |
| F-MET-07 | Removed `<!-- UNVERIFIED -->` tag from final text |

### Minor (noted, no action)

F-FID-03 (French number parsing false positives), F-FID-04 (OR/CI defensible), F-FID-05 (CSA values need manual check), F-FID-09 (semantic duplicates), F-MET-08 (Discussion redundancy — partially addressed by F-MET-03 fix), F-MET-09 (French priority not quantified — addressed by F-FID-08).

## MCP Tool Issues

| Tool | Issue | Severity | Workaround |
|------|-------|----------|------------|
| `extract_claims_regex` | Fails on custom output paths and parallel calls | High | Replicated regex extraction in Python |
| `audit_claims` | French thousand-separator (space) splits numbers into 2 tokens → 45/70 false UNVERIFIED | Medium | Manual triage during walkthrough |
| `generate_bibliography` | 9/56 entries mapped to wrong citation key (upstream: LLM-generated DOIs are wrong) | High | Removed erroneous DOIs, added PMID-based entries manually |
| OpenAlex topical search | Returned off-topic results for shoulder pain queries | Low | Dropped as topical source, used for citation enrichment only |

## Timing

| Phase | Duration | Notes |
|-------|----------|-------|
| Phase 1 Planning | ~2 min | Direct, no iteration |
| Phase 2 Search | ~15 min | PubMed 6 queries, S2 2 queries, OpenAlex enrichment in background |
| Phase 3a Screening | ~10 min | 3,801 articles, title + abstract + full-text (no-abstract subset) |
| Phase 4 Extraction | ~20 min | 1,114 articles, MCP fallback to Python |
| Phase 5 Synthesis | ~15 min | Completed just before rate limit |
| — Rate limit pause | ~1h | Reset at 15h Paris |
| Phase 6 Verification | ~10 min | DOI verify + bibliography + claims audit in parallel |
| Phase 6 corrections | ~8 min | Agent for DOI/BibTeX fixes |
| Phase 8 Audits | ~7 min | Two agents in parallel (background) |
| Phase 8 Walkthroughs | ~10 min | Sequential, 19 findings |
| **Total active** | **~1h 40min** | Excluding rate limit pause |

## Output Files

| File | Size | Content |
|------|------|---------|
| `scapulalgie_epidemiologie_review.md` | ~61 KB | Main review (French, Pandoc/Quarto, ~950 lines) |
| `references.bib` | ~26 KB | 53 BibTeX entries |
| `combined_results.json` | 10.5 MB | 3,801 articles |
| `extracted_claims.json` | 3.6 MB | 1,114 articles, 5,924 quant + 3,503 semantic claims |
| `claims_audit.json` | ~95 KB | 179 claims audited |
| `protocol.md` | ~2 KB | PEO protocol |
| `screening_log.md` | ~284 KB | Full screening decisions |
| `search_log.md` | ~5 KB | Query documentation |
| `search_results.md` | ~695 KB | Ranked results table |
| `audit_fidelity.md` | ~13 KB | 10 findings (2C, 1M, 7m) |
| `audit_methodology.md` | ~8 KB | 9 findings (0C, 3M, 6m) |

## Observations for Skill Improvement

1. **Synthesis cites only 4.8% of included articles** — the extraction-to-synthesis funnel is aggressive. Consider whether litrev-synthesize should report coverage metrics per theme.
2. **DOI hallucination is the #1 quality risk** — 25/56 BibTeX entries had fabricated or misattributed DOIs. PMID-first resolution would eliminate most of these.
3. **Rate limit hit at Phase 5** — for large corpora (>1000 articles), the pipeline should warn upfront that it may span multiple sessions.
4. **Walkthrough batch approval is efficient** — grouping minor findings saved time without losing rigor. Consider making this the default for minors.
5. **OpenAlex topical search is unreliable** — for clinical/medical queries, it consistently returns off-topic results. Consider downgrading it to enrichment-only by default for medical reviews.
