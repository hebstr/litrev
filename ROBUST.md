# Robustness Plan — litrev

## Static reviews — Layer 1 results (2026-04-01)

| Component | Reviewer | Findings | Accepted | FP rate | Report |
|-----------|----------|----------|----------|---------|--------|
| litrev-mcp | `/mcp-adversary` | 12 | 3 | 58% | (archived, prior session) |
| litrev-search | `/skill-adversary` | 16 | 6 | 63% | (archived, prior session) |
| litrev-screen | `/skill-adversary` | 13 | 6 | 31% | (archived, prior session) |
| litrev-extract | `/skill-adversary` | 12 | 4 | 42% | (archived, prior session) |
| litrev-synthesize | `/skill-adversary` | 11 | 4 | 45% | (archived, prior session) |
| litrev (orchestrator) | `/skill-adversary` | 11 | 3 | 36% | `REVIEW.md` |
| **Total** | | **75** | **26** | **44%** | |

### Reviewer observations

- Average FP 47% — acceptable for adversarial review, but LOW findings are almost always noise (0% acceptance)
- skill-adversary doesn't know Claude Code skill conventions (`!`command``, long description, `$SKILL_DIR`)
- Cross-model L1 (sonnet) added value on severity calibration, not on detection
- Bug found: review-walkthrough calls `ouroboros_evaluate` instead of `ouroboros_qa` when no Ouroboros session exists

### Remaining static reviews

| Action | Status |
|--------|--------|
| `/critical-code-reviewer` on litrev-mcp/src/ | Not done (optional — 3 bugs found by mcp-adversary were the most impactful) |
| `/full-review` integration | Not done → after API key fix ([roadmap_env_fix.md](roadmap_env_fix.md)) |
| `/blindspot-review` on agents/audit_* | Not done |

---

## Micro-audits between phases (not implemented)

Lightweight agent between two phases to verify quality, not just structure. Reserve for systematic/meta-analysis reviews — not needed for narrative/rapid.

| After phase | Checks |
|-------------|--------|
| Search (2) | Queries cover all protocol concepts? Result ratio across DBs balanced? |
| Screening (3) | Exclusions consistent with criteria? No obvious false negatives? |
| Extraction (4) | Claims specific? Quality ratings justified? |
| Synthesis (5) | Every JSON claim in the text? No fabricated claims? |
