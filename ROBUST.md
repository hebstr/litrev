# Robustness Plan — litrev

Plan d'amélioration de la robustesse du skill litrev et de ses composants.

## 1. Revues statiques (avant utilisation)

### Bottom-up — composants individuels

Ordre : valider la fondation d'abord, puis remonter.

```
litrev-mcp          ← fondation
  ↑
litrev-search       ← dépend du MCP
litrev-screen       ← dépend du MCP
litrev-extract      ← dépend du MCP
litrev-synthesize   ← LLM pur
  ↑
litrev              ← orchestrateur
  ↑
agents/audit_*      ← post-pipeline
```

| Composant | Skill de review | Cible |
|-----------|----------------|-------|
| litrev-mcp (schemas, tools) | `/mcp-adversary` | Discrimination inter-tools, schemas, discoverabilité |
| litrev-mcp (code) | `/critical-code-reviewer` | Bugs, race conditions httpx, gestion d'erreurs API |
| Chaque sub-skill | `/skill-adversary` | Edge cases trigger, incohérences SKILL.md |
| agents/audit_* | `/blindspot-review` | Circularité (audits dans le même repo que le code audité) |

### Top-down — intégration

| Skill de review | Cible |
|----------------|-------|
| `/full-review` | Repo litrev entier — agents par facette (architecture, interface contracts, error paths) |

### Evals — régression

Après chaque cycle de corrections :
- Relancer les evals existants (`workspace/iteration-N/`)
- Comparer les scores avant/après
- Si régression → la correction a cassé quelque chose

### Workflow par itération

```
Phase 1 — Bottom-up (parallélisable)
  /skill-adversary    sur litrev-search
  /skill-adversary    sur litrev-screen
  /skill-adversary    sur litrev-extract
  /skill-adversary    sur litrev-synthesize
  /mcp-adversary      sur litrev-mcp
  /critical-code-reviewer sur litrev-mcp/src/

Phase 2 — Corrections
  Appliquer les findings, un composant à la fois

Phase 3 — Top-down
  /full-review        sur le repo litrev
  /blindspot-review   sur les agents d'audit

Phase 4 — Régression
  Relancer les evals, comparer avec iteration précédente

Phase 5 — Orchestrateur (en dernier, dépend de tout)
  /skill-adversary    sur litrev
```

---

## 2. Robustesse en conditions réelles (pendant l'utilisation)

Trois couches complémentaires, de la moins chère à la plus riche.

### Couche 1 — Gates mécaniques (validation structurelle)

Scripts qui valident les outputs après chaque phase. Pas contournables, pas de tokens consommés.

| Gate | Fichiers vérifiés | Checks |
|------|------------------|--------|
| Gate 1 | `review/protocol.md` | Existe, contient question + framework + criteria |
| Gate 2 | `combined_results.json`, `search_results.md`, `search_log.md` | Existent, JSON parseable, >= 1 résultat |
| Gate 3a | `screening_log.md`, `included_indices.json` | Existent, JSON parseable, PRISMA counts cohérents |
| Gate 3b | `screening_log.md` section snowballing | Section présente avec `Status: COMPLETE` (ou gate N/A) |
| Gate 4 | `extracted_claims.json` | Existe, >= 1 article avec `semantic_claims` non vide |
| Gate 5 | `*_review.md` | Existe, contient YAML header + sections requises + >= 1 `[@` citation |
| Gate 6 | `references.bib`, `claims_audit.json`, `*_citation_report.json` | Existent, BibTeX parseable |
| Gate 7 | Checklist items | Tous PASS ou UNRESOLVABLE documenté |
| Gate 8 | `audit_fidelity.md`, `audit_methodology.md` | Existent, walkthroughs complétés, 0 CRITICAL non résolu |

Implémentation possible : scripts bash, MCP tool dédié (`validate_gate`), ou hook post-phase.

### Couche 2 — Feedback loop par phase (apprentissage)

Après chaque revue réelle, catégoriser les findings Phase 8 par phase d'origine :

| Finding Phase 8 | Phase d'origine | Action |
|----------------|----------------|--------|
| Claims descriptives (pas de chiffre) | Phase 4 (extract) | Renforcer instructions extraction |
| Requête PubMed trop étroite | Phase 2 (search) | Ajouter check de couverture |
| Faux négatifs screening | Phase 3 (screen) | Ajuster seuils include/exclude |
| Claim inventée dans synthèse | Phase 5 (synthesize) | Renforcer contrainte de traçabilité |

Stocker les patterns récurrents en mémoire (même logique que `feedback_litrev_extraction_patterns.md`).

Fichiers mémoire cibles :
- `feedback_litrev_search_patterns.md`
- `feedback_litrev_screen_patterns.md`
- `feedback_litrev_extraction_patterns.md` (existe déjà)
- `feedback_litrev_synthesis_patterns.md`

### Couche 3 — Micro-audits inter-phases (optionnel, coûteux)

Agent léger entre deux phases pour vérifier la qualité, pas juste la structure.

| Après phase | Vérifie |
|-------------|---------|
| Search (2) | Requêtes couvrent tous les concepts du protocole ? Ratio résultats/DB équilibré ? |
| Screening (3) | Exclusions cohérentes avec critères ? Pas de faux négatifs évidents ? |
| Extraction (4) | Claims spécifiques ? Quality ratings justifiés ? |
| Synthesis (5) | Chaque claim JSON dans le texte ? Pas de claim inventée ? |

Réserver aux revues systematic/meta-analysis. Pas nécessaire pour narrative/rapid.

---

## 3. Priorisation

| Priorité | Action | Effort | Impact |
|----------|--------|--------|--------|
| 1 | `/mcp-adversary` sur litrev-mcp | Faible | Haut — fondation |
| 2 | Couche 1 gates mécaniques | Moyen | Haut — erreurs détectées tôt |
| 3 | `/skill-adversary` sur chaque sub-skill | Faible × 4 | Moyen — edge cases |
| 4 | Couche 2 feedback loop systématisé | Faible | Haut (cumulatif) |
| 5 | `/full-review` intégration | Faible | Moyen — inter-composants |
| 6 | Couche 3 micro-audits | Élevé | Haut mais cher en tokens |
| 7 | Evals itération N+1 | Moyen | Filet de sécurité |
