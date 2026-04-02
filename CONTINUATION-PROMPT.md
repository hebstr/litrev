# Session handoff — litrev stabilisation: B1 validation + full-review + bug fixes

## Context
Stabilising the `litrev` skill suite (6 components: orchestrator, 4 sub-skills, 1 Python MCP server). The suite conducts systematic literature reviews via Claude Code. This session validated a previously-applied fix (B1: PICO outcome coverage enforcement in litrev-synthesize), then ran `/full-review` across the entire suite, walked through all 18 findings, and applied fixes.

## Key decisions
- **B1 fix validated** by deleting `review/subacromial_csi_shoulder_review.md` and re-running `/litrev-synthesize`. The "Predictive Factors of Response" outcome now gets a dedicated subsection (line 271, 82 articles). All 3 guards (B1/B2/B3) PASS.
- **Install instructions aligned to `uv sync`** (litrev/README.md). The old `uv pip install -e .` approach was contradicting the litrev-mcp README's `uv sync` approach. Chose `uv sync` as canonical because `uv.lock` exists.
- **Gate 3a fix**: restricted retained-count regex to text *before* `## Citation Snowballing` section, not using `[-1]` which could pick up snowball counts. This is the correct fix — the alternative (dedicated summary section) would require changes to litrev-screen's output format.
- **Comma-thousands fix**: inserted `re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", value)` *before* the comma-to-period conversion in `_normalize_number`. This strips English thousand separators (12,403 -> 12403) before French decimal conversion (2,8 -> 2.8).
- **GATE 7 marker added** to orchestrator SKILL.md (found by deep sync). Was the only gate without a `### === GATE N ===` + `validate_gate` call.
- **DOI gap in generate_bibliography DEFERRED**: the tool only resolves via DOI, but the synthesis intentionally omits DOIs from BibTeX (to avoid hallucination). Fix requires adding a PMID->DOI resolver — too large for this session.
- **Review calibration memory created** (`feedback_review_severity.md`): suppresses packaging polish, sub-skill READMEs, and example doc findings in future reviews (personal use context).
- **Step 5 of plan (blindspot-review) skipped** — diminishing returns after full-review.

## Current state

### Files modified (uncommitted, user manages git)

**Bug fixes (Python):**
- `litrev-mcp/src/litrev_mcp/tools/verify.py:607` — comma-thousands stripping before decimal conversion
- `litrev-mcp/src/litrev_mcp/tools/gates.py:137-140` — Gate 3a restricted to pre-snowball region

**Skill definitions:**
- `litrev/SKILL.md:564` — interface contract: added `protocol.md (optional)` for litrev-synthesize
- `litrev/SKILL.md:333-335` — added GATE 7 marker with `validate_gate` call
- `litrev/README.md:88-108` — install instructions aligned to `uv sync` + MCP config updated
- `litrev/README.md:119` — S2_API_KEY warning strengthened (near-required, orchestrator halts)
- `litrev/ROADMAP.md` — A1 description updated, B1/B2/B3 marked tested, execution sequence updated
- `litrev/ROBUST.md` — B1 fix (from prior session, unchanged this session)
- `litrev/DEFERRED.md` — 3 new deferred items added

**Documentation:**
- `litrev-mcp/README.md:28-30` — added 3 missing search tools to tool table (now 12/12)

**Regenerated output:**
- `example_v3/review/subacromial_csi_shoulder_review.md` — re-synthesized with B1 fix active
- `example_v3/review/pipeline_log.md` — updated by synthesize run

**Memory (outside git):**
- `project_synthesize_guards_2026q2.md` — B1 re-test PASS
- `project_plan_2026q2.md` — steps 1-4 DONE, next action updated
- `feedback_review_severity.md` — NEW: 3 calibration rules for future reviews
- `MEMORY.md` — index updated with calibration entry

### Tests verified
- `litrev-mcp/tests/test_verify_matching.py` — 16/16 PASS (after verify.py change)
- `litrev-mcp/tests/test_gates.py` — 27/27 PASS (after gates.py change)

## Open items

1. **PMID resolver in `generate_bibliography`** (DEFERRED, highest priority) — `litrev-mcp/src/litrev_mcp/tools/verify.py:371-425`. Currently resolves only via DOI (`extract_doi_matches`). Since litrev-synthesize now intentionally omits DOIs from BibTeX (Step 4j), `generate_bibliography` finds 0 DOIs and produces an empty `.bib`. The orchestrator Step 6.2 fallback (copy from embedded BibTeX) catches this, but no CrossRef/PubMed enrichment happens. Fix: add a PMID->DOI resolution step (PubMed ID converter API or ESearch) before the DOI resolver cascade.

2. **Unit tests for MCP tool entry points** (DEFERRED) — `litrev-mcp/tests/`. Only lib helpers and gates are tested. Priority targets: `search.py:process_results` (dedup/ranking logic), `tools/claims.py:audit_claims` (matching), `tools/verify.py:generate_bibliography` (entry assembly). These are deterministic and testable without HTTP mocks.

3. **Eval fixtures for Phase 6/8** (DEFERRED, after #2) — `litrev/evals/`. No eval for verification or audit phases — the exact phases where known MCP bugs concentrate.

4. **Plan step 6: micro-audits** — inter-phase quality checkpoints for systematic/meta-analysis reviews. Not yet specified in detail.

## Continuation prompt

```
I'm stabilising the litrev skill suite. Last session completed: B1 fix validation (PASS), /full-review (18 findings, 7 accepted, 3 deferred), and /sync-files --deep. Steps 1-4 of the plan are DONE.

Priority for this session: implement the PMID resolver in `generate_bibliography` (DEFERRED item #1). The problem: `generate_bibliography` in `litrev-mcp/src/litrev_mcp/tools/verify.py:371-425` only resolves references via DOI, but litrev-synthesize intentionally omits DOIs from BibTeX (to prevent hallucination). Result: the tool finds 0 DOIs and produces an empty .bib. The orchestrator fallback copies raw LLM-generated BibTeX without CrossRef/PubMed enrichment.

Fix approach: add a PMID->DOI resolution path. The BibTeX entries already contain `pmid = {12345678}` fields. Use NCBI ID converter API or ESearch to resolve PMIDs to DOIs, then feed those DOIs into the existing resolver cascade.

After the PMID resolver, write unit tests for `generate_bibliography` entry assembly and `search.py:process_results` dedup logic.

Key files:
- `litrev-mcp/src/litrev_mcp/tools/verify.py` (generate_bibliography at line 371)
- `litrev-mcp/src/litrev_mcp/lib/bibtex.py` (extract_doi_matches, parse_bib_keys_to_doi)
- `litrev-mcp/src/litrev_mcp/lib/http.py` (request_with_retry, ncbi_params)
- `litrev-mcp/src/litrev_mcp/lib/pubmed.py` (existing PubMed helpers)
- `litrev-mcp/tests/` (test files to add)
- Memory: project_plan_2026q2.md, DEFERRED.md at litrev root

Constraints: user manages all git operations (never run git write commands). Existing tests must keep passing. The `_normalize_number` fix (comma-thousands) and Gate 3a fix (snowball exclusion) were applied this session — don't revert them.
```
