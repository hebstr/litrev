# Robustness Plan — litrev

## Completed: end-to-end validation run (2026-04-02)

`example_v3` (scoping review, corticosteroid infiltrations) — full pipeline test post API key fix. Findings triaged into [ROADMAP.md](ROADMAP.md) priorities A-F.

Validated:
- 3 MCP search tools (search_pubmed, search_s2, search_openalex)
- S2 pre-flight check
- Full 9-phase pipeline on a real clinical topic
- Known quality patterns (descriptive claims, causal drift, DOI hallucination)

---

## Static reviews

Layer 1 adversarial reviews completed 2026-04-01 (6 components, 26 findings accepted out of 75). Fixes applied.

| Action | Priority | Status |
|--------|----------|--------|
| `/full-review` integration | Done | litrev-mcp clean (2 micro-fixes: regex perf + type annotation), 180/180 tests OK. B1/B2/B3 instructions added to litrev-synthesize. |
| `/blindspot-review` on agents/audit_* | Optional | Not done |
| `/critical-code-reviewer` on litrev-mcp/src/ | Optional | Covered by `/full-review` — clean, no blocking issues |

---

## Micro-audits between phases (implemented 2026-04-03)

Lightweight inline checks after each gate for systematic/meta-analysis reviews only. Not full agents — 3-line summaries printed by the orchestrator. Skipped for scoping, narrative, and rapid reviews.

| After phase | Micro-audit | Checks |
|-------------|-------------|--------|
| Search (2) | Micro-audit 2 | Concept coverage, DB balance, failed searches |
| Screening (3a) | Micro-audit 3a | Exclusion consistency, inclusion rate plausibility |
| Extraction (4) | Micro-audit 4 | Claim specificity, quality calibration, theme accuracy |
| Synthesis (5) | Micro-audit 5 | Claim traceability (5-sample), fabrication risk, PICO coverage |
