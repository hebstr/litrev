# Robustness Plan — litrev

## Completed: end-to-end validation run (2026-04-02)

`example_v3` (scoping review, corticosteroid infiltrations) — full pipeline test post API key fix. Findings triaged into [ROADMAP.md](ROADMAP.md) priorities A-E.

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

## Micro-audits between phases (not implemented)

Lightweight agent between two phases to verify quality, not just structure. Reserve for systematic/meta-analysis reviews — not needed for narrative/rapid.

| After phase | Checks |
|-------------|--------|
| Search (2) | Queries cover all protocol concepts? Result ratio across DBs balanced? |
| Screening (3) | Exclusions consistent with criteria? No obvious false negatives? |
| Extraction (4) | Claims specific? Quality ratings justified? |
| Synthesis (5) | Every JSON claim in the text? No fabricated claims? All PICO outcomes covered by a section? |
