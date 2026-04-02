# Litrev Skill — Roadmap

Last updated: 2026-04-02

## Priority A: MCP bug fixes (pre-review) — DONE

All 3 fixes implemented and tested. Additional fix (A4) from /full-review.

### A1. validate_gate(3a) — regex matches snowball "Retained" count

Gate 3a PRISMA consistency check used `retained_matches[-1]` which could pick up the snowballing section's `### Retained` count instead of the main screening count.

- **File**: `litrev-mcp/src/litrev_mcp/tools/gates.py`
- **Fix**: restrict regex search to text before `## Citation Snowballing` section
- [x] Fix implemented
- [x] Test added
- [x] Additional fix (2026-04-02): exclude snowball region from retained count search

### A2. audit_claims — Unicode middle dots not matched

Lancet-style abstracts use U+00B7 (`·`) for decimal points. Audit tool only matches ASCII period.

- **File**: `litrev-mcp/src/tools/verify.py`
- **Fix**: normalize `·` to `.` before number matching
- [x] Fix implemented
- [x] Test added

### A3. audit_claims — spelled-out numbers not matched

Abstracts with "Thirteen RCTs" flagged UNVERIFIED when review writes "13 RCTs".

- **File**: `litrev-mcp/src/tools/verify.py`
- **Fix**: add spelled-out → digit normalization in abstract text, or accept both forms
- [x] Fix implemented
- [x] Test added

---

## Priority B: Synthesis quality (highest impact on review quality) — DONE

Structural improvements to litrev-synthesize, identified by double audit. All tested on example_v3 (2026-04-02).

### B1. PICO outcome → section mapping enforcement

litrev-synthesize organizes by data-driven themes but does not check that each PICO outcome has a dedicated section. In the validation run, "Predictive factors" (PICO #2) had 19 articles but no section.

- **Files**: `litrev-synthesize/SKILL.md`
- **Fix**: after synthesis, cross-check each PICO outcome against theme headings. If an outcome has no dedicated section and >5 articles with relevant claims, create one or flag
- **Source**: F-MET-01
- [x] Instruction added to SKILL.md (Step 5, check #8)
- [x] Tested on example_v3 (2026-04-02) — PASS, predictive factors subsection generated

### B2. Multi-source citation guard

litrev-synthesize combines two studies in `[@A; @B]` while reporting data from only one, making it look like both produced the finding.

- **Files**: `litrev-synthesize/SKILL.md`
- **Fix**: add instruction that each specific statistic in a dual citation must be verifiable in both cited abstracts
- **Source**: F-FID-02
- [x] Instruction added to SKILL.md (Step 4e, after constrained writing rule)
- [x] Tested on example_v3 (2026-04-02) — PASS

### B3. Stop generating DOIs in embedded BibTeX

litrev-synthesize fabricates DOIs (16/56 fabricated, 9/56 misattributed in example_v2; 17/60 failed in example_v3). PMIDs from extracted_claims.json are reliable.

- **Files**: `litrev-synthesize/SKILL.md`
- **Fix**: instruct synthesize to emit only PMID-based BibTeX entries. Let `generate_bibliography` resolve DOIs from PMIDs
- **Source**: feedback_litrev_extraction_patterns.md "DOI hallucination"
- [x] Instruction updated in SKILL.md (Step 4j + Step 5 check #9)
- [x] Tested on example_v3 (2026-04-02) — PASS, 0 DOIs in BibTeX

---

## Priority C: Search documentation & coverage

### C1. Log dedup counts in search_log.md

Zero duplicates across 3 databases was suspicious and unexplained. The MCP `deduplicate_results` tool works but doesn't report counts.

- **Files**: `litrev-search/SKILL.md`, possibly `litrev-mcp/src/tools/dedup.py`
- **Fix**: log pre/post dedup counts in search_log.md. If dedup tool returns counts, use them; otherwise count combined_results.json before/after
- **Source**: F-MET-02
- [ ] Instruction added
- [ ] MCP tool returns dedup stats

### C2. Grey literature / guideline database support

No French institutional guidelines (HAS, SOFCOT, SFR, INRS) despite "French data prioritized". Structural limitation of PubMed/S2/OA.

- **Approach**: TBD — options: (a) manual search checklist in protocol, (b) scraping HAS recommandations, (c) dedicated search tool
- **Source**: F-FID-10
- [ ] Approach decided
- [ ] Implemented

---

## Priority D: Orchestrator improvements

### D1. Auto-disclose AI-assisted timeline in limitations

Single-day review timeline not disclosed. The orchestrator should add this automatically.

- **File**: `litrev/SKILL.md` (orchestrator) or `litrev-synthesize/SKILL.md`
- **Fix**: instruct synthesize to include AI-assisted review timeline and date in limitations
- **Source**: F-MET-03
- [ ] Instruction added

### D2. Auto-disclose skipped phases in limitations

Snowballing absence not mentioned in limitations when skipped.

- **File**: `litrev/SKILL.md` (orchestrator)
- **Fix**: when snowballing is skipped, pass this to synthesize as a required limitation item
- **Source**: F-MET-04
- [ ] Instruction added

---

## Priority E: New source integrations (medium-term)

### E1. Full-text retrieval (`fetch_fulltext`)

New MCP tool: given a DOI, retrieve full text via cascade: Unpaywall → PMC → Semantic Scholar → CORE → Sci-Hub.

- Single tool interface: `fetch_fulltext(doi) → {source, url, format, text|path}`
- PDF-to-text extraction (PyMuPDF or pdfplumber)
- Rate-limiting per source
- Env vars: `UNPAYWALL_EMAIL` (required), `SCIHUB_DOMAIN` (optional), `CORE_API_KEY` (optional)
- [ ] Cascade implemented
- [ ] PDF-to-text works
- [ ] Integrates with extract_claims_regex

### E2. Scopus search (`search_scopus`)

New MCP tool: `api.elsevier.com/content/search/scopus`. Requires `SCOPUS_API_KEY`.

- [ ] Returns deduplicated results compatible with process_results
- [ ] Pagination handles >25 results

### E3. Web of Science search (`search_wos`)

New MCP tool: `api.clarivate.com/apis/wos-starter/v1`. Requires `WOS_API_KEY`. Note: Starter API does NOT return abstracts.

- [ ] Returns results compatible with process_results
- [ ] Handles WoS query syntax

### E4. EMBASE (deferred)

No public API. Options: ready-to-paste Ovid query generator, RIS/CSV import tool.

---

## Dependencies & integration

```
search_scopus ──┐
search_wos ─────┤
search_pubmed ──┼──→ deduplicate_results → screen → extract_claims
search_s2 ──────┤                                        ↑
search_openalex ┘                              fetch_fulltext
```

## Execution sequence

```
A (MCP fixes) ✓ → B (synthesis quality) ✓ → /full-review ✓ → C (search doc) → D (orchestrator) → E (new sources)
```

A+B done, /full-review done (2026-04-02). Next: C (search doc improvements).
Do not start E before B+C are stable — new sources compound existing quality issues.
