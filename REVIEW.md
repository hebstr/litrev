# Review Report — litrev skill

- **Date**: 2026-04-01
- **Reviewer**: skill-adversary (adversarial mode)
- **Target**: `~/.claude/skills/litrev/`
- **Scope**: SKILL.md, agents/audit_fidelity.md, agents/audit_methodology.md, evals/evals.json
- **Walkthrough**: review-walkthrough with author's defense on Important+ findings
- **Context**: personal (path heuristic)
- **Ouroboros**: available, not invoked (all verdicts clear)

## Findings

| # | Severity | Finding | File(s) | Status |
|---|----------|---------|---------|--------|
| 1 | HIGH | `allowed-tools` missing `Skill` — blocks all sub-skill invocations | SKILL.md:5 | ACCEPTED |
| 2 | HIGH | `allowed-tools` missing `Agent` — blocks Phase 8 double audit | SKILL.md:5 | ACCEPTED |
| 3 | HIGH | `verify_dois` output path not explicitly set — Gate 6 could fail | SKILL.md:259-271 | REJECTED |
| 4 | MEDIUM | Step 9b memory persistence embedded in orchestrator — domain logic in sequencer | SKILL.md:488-502 | REJECTED |
| 5 | MEDIUM | `rm -rf review` could follow symlink and delete target | SKILL.md:82-85 | REJECTED |
| 6 | MEDIUM | Session resumption can't distinguish raw vs screened `chaining_candidates.json` | SKILL.md:525-543 | REJECTED |
| 7 | MEDIUM | Re-invoking Phase 4/5 from Phase 7 invalidates downstream Phase 6 artifacts | SKILL.md:309-331 | ACCEPTED |
| 8 | LOW | "Select 10 claims at random" not truly random in LLM execution | agents/audit_fidelity.md:28 | NOTED |
| 9 | LOW | Checklist items 3/10 overlap in audit_methodology (database gap checked twice) | agents/audit_methodology.md:31-83 | NOTED |
| 10 | LOW | Eval 4 missing stats-consistency assertion (Gate 4 `stats` field) | evals/evals.json:65-76 | NOTED |
| 11 | LOW | Phase 9 Timing section depends on inaccessible conversation timestamps | SKILL.md:458-462 | NOTED |

## Summary

- **3 ACCEPTED** (2 HIGH, 1 MEDIUM) — fixes applied
- **4 REJECTED** (1 HIGH, 3 MEDIUM) — false positives or over-defensive
- **4 NOTED** (4 LOW) — valid but low-impact, no action taken
- **0 DEFERRED**

## Fixes Applied

### Fix 1+2: `Skill` and `Agent` added to `allowed-tools` (SKILL.md:5)

```diff
- allowed-tools: Read Write Edit Bash WebFetch WebSearch mcp__litrev-mcp__citation_chain ...
+ allowed-tools: Read Write Edit Bash Skill Agent WebFetch WebSearch mcp__litrev-mcp__citation_chain ...
```

**Rationale**: The orchestrator delegates to sub-skills via the Skill tool (Phases 2-5) and launches audit agents via the Agent tool (Phase 8). Both were missing from the whitelist.

### Fix 3: Phase 7 corrective actions mandate downstream re-verification (SKILL.md:317-318)

```diff
- Item 8: re-invoke `litrev-synthesize` (restructure results)
- Item 9: re-invoke `litrev-extract` (redo quality assessment)
+ Item 8: re-invoke `litrev-synthesize` (restructure results), then re-run Phase 6
+         (verify_dois + generate_bibliography + audit_claims) since the review document changed
+ Item 9: re-invoke `litrev-extract` (redo quality assessment), then re-run audit_claims
+         since extracted_claims.json changed
```

**Rationale**: Re-running Phase 4 or 5 changes files that Phase 6 depends on (`extracted_claims.json`, `<topic>_review.md`). Without re-verification, `references.bib` and `claims_audit.json` go stale.

## Rejection Rationale

| # | Reason |
|---|--------|
| 3 | Auto-generated output path and Gate 6 check both derive from the same `<topic>_review.md` filename — no divergence scenario exists by construction |
| 4 | Step 9b is well-scoped (2 specific memory files, explicit dedup guards, "Do not duplicate" rule). Extracting it would add a sub-skill for 15 lines — over-engineering |
| 5 | `rm -rf review` (no trailing slash) removes the symlink itself, not the target. POSIX semantics. Reviewer's premise incorrect |
| 6 | Resumption already handles this correctly: `screening_log.md` lacking `Status: COMPLETE` triggers re-screening, which is idempotent (same criteria + same candidates = same decisions) |

## Mechanisms

| Mechanism | Invocations | Notes |
|-----------|-------------|-------|
| Author's defense | 7/7 Important+ | 3 held → rejected, 1 partially held → accepted, 3 held → rejected |
| QA auto | 0/11 | No ambiguous verdicts |
| Cross-model L1 | 0/7 Important+ | All clear verdicts, no escalation needed |
| Cross-model L2 | 0/3 HIGH | L1 not triggered, no divergence |
| Lateral think | 0 | No stuck points |
| Evaluate | skipped | < 2 code-file fixes (both edits in same SKILL.md) |
| Drift check | skipped | < 4 fixes |

## Quality Assessment

### Reviewer accuracy

- **True positives**: 3/11 (27%) — findings 1, 2, 7
- **False positives**: 4/11 (36%) — findings 3, 4, 5, 6
- **Low-value true positives**: 4/11 (36%) — findings 8, 9, 10, 11

The skill-adversary produced a high false-positive rate on MEDIUM findings (3/4 rejected). The HIGH tier was more reliable (2/3 accepted). All LOW findings were valid observations but none warranted action.

### False positive patterns

- **Incorrect POSIX assumption** (finding 5): reviewer assumed `rm -rf` follows symlinks — factually wrong
- **Redundant safety** (findings 4, 6): suggesting defensive patterns for scenarios already handled by existing logic
- **Coupling paranoia** (finding 3): flagging a coupling that is structural and can't diverge

### Calibration applied

Prior calibration from `skipped_review_points.md` (15 rules) was injected into the reviewer prompt. No findings contradicted prior calibration — the rules worked as intended to suppress known false positives.
