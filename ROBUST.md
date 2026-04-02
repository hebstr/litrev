# Robustness Plan — litrev

## Next: end-to-end validation run

Run `example_v3` (scoping review, corticosteroid infiltrations) — first full pipeline test post API key fix (2026-04-02).

Validates:
- 3 new MCP search tools (search_pubmed, search_s2, search_openalex)
- S2 pre-flight check
- Full 9-phase pipeline on a real clinical topic
- Known quality patterns (descriptive claims, causal drift, DOI hallucination)

Post-run: update memory with new bugs/patterns, then decide on further reviews.

---

## Static reviews (after validation run)

Layer 1 adversarial reviews completed 2026-04-01 (6 components, 26 findings accepted out of 75). Fixes applied.

| Action | Priority | Status |
|--------|----------|--------|
| `/full-review` integration | Next (after run) | Not done (unblocked since API key fix 2026-04-02) |
| `/blindspot-review` on agents/audit_* | Optional | Not done |
| `/critical-code-reviewer` on litrev-mcp/src/ | Optional | Not done (3 bugs already found by mcp-adversary) |

---

## Micro-audits between phases (not implemented)

Lightweight agent between two phases to verify quality, not just structure. Reserve for systematic/meta-analysis reviews — not needed for narrative/rapid.

| After phase | Checks |
|-------------|--------|
| Search (2) | Queries cover all protocol concepts? Result ratio across DBs balanced? |
| Screening (3) | Exclusions consistent with criteria? No obvious false negatives? |
| Extraction (4) | Claims specific? Quality ratings justified? |
| Synthesis (5) | Every JSON claim in the text? No fabricated claims? |
