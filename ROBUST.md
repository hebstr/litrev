# Robustness Plan — litrev

Plan d'amélioration de la robustesse du skill litrev et de ses composants.

## 1. Revues statiques (avant utilisation)

**Statut : Layer 1 complétée le 2026-04-01.**

### Résultats Layer 1

| Composant | Reviewer | Findings | Accepted | FP rate | Rapport |
|-----------|----------|----------|----------|---------|---------|
| litrev-mcp | `/mcp-adversary` | 12 | 3 | 58% | (rapport archivé, session antérieure) |
| litrev-search | `/skill-adversary` | 16 | 6 | 63% | (rapport archivé, session antérieure) |
| litrev-screen | `/skill-adversary` | 13 | 6 | 31% | (rapport archivé, session antérieure) |
| litrev-extract | `/skill-adversary` | 12 | 4 | 42% | (rapport archivé, session antérieure) |
| litrev-synthesize | `/skill-adversary` | 11 | 4 | 45% | (rapport archivé, session antérieure) |
| litrev (orchestrateur) | `/skill-adversary` | 11 | 3 | 36% | `REVIEW.md` |
| **Total** | | **75** | **26** | **44%** | |

### Patterns corrigés

1. **`allowed-tools` incomplet** — trouvé dans 3/4 sous-skills + orchestrateur, corrigé partout
2. **Résidus pré-MCP** (refs à `.py` stales) — nettoyés dans search + screen
3. **Evals structurels sans ancrage factuel** — spot-checks de valeurs + assertions stats ajoutés (extract)
4. **Contradictions internes** — `UNVERIFIED` vs self-check (synthesize), seuils evals incohérents (search)
5. **Renommages paramètres MCP** — 3 mismatches API publique vs implémentation (mcp)

### Restant (Layer 1)

| Action | Statut | Note |
|--------|--------|------|
| `/skill-adversary` sur litrev (orchestrateur) | **Fait** (2026-04-01) | 11 findings, 3 accepted (2 HIGH allowed-tools, 1 MEDIUM Phase 7 downstream), FP 36% |
| `/critical-code-reviewer` sur litrev-mcp/src/ | Non fait | Optionnel — les 3 bugs trouvés par mcp-adversary étaient les plus impactants |
| `/full-review` intégration | Non fait | Prochaine étape — orchestrateur terminé |
| `/blindspot-review` sur agents/audit_* | Non fait | Prochaine étape — orchestrateur terminé |
| ~~Fixtures de test Phase 4 + Phase 5~~ | **Fait** | cf. DEFERRED.md |

### Observations sur les reviewers

- FP moyen 47% — acceptable pour du review adversarial, mais les LOW findings sont quasi toujours du bruit (0% d'acceptance)
- skill-adversary ne connaît pas les conventions Claude Code skills (`!`command``, description longue, `$SKILL_DIR`)
- Cross-model L1 (sonnet) a ajouté de la valeur sur le calibrage de sévérité, pas sur la détection
- Bug identifié : review-walkthrough appelle `ouroboros_evaluate` au lieu de `ouroboros_qa` quand pas de session Ouroboros

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
| Gate 9 | `pipeline_log.md` | Existe, contient Funnel Metrics + Gate Log + Run-Specific Notes |

**Statut : Implémenté le 2026-04-01.** MCP tool `validate_gate(gate, review_dir)` dans litrev-mcp. 10 gates, 26 tests unitaires. SKILL.md mis a jour pour appeler `validate_gate` a chaque gate.

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

| Priorité | Action | Effort | Impact | Statut |
|----------|--------|--------|--------|--------|
| 1 | `/mcp-adversary` sur litrev-mcp | Faible | Haut — fondation | **Fait** (2026-04-01) |
| 2 | `/skill-adversary` sur chaque sub-skill | Faible × 4 | Moyen — edge cases | **Fait** (2026-04-01) |
| 3 | Fixtures de test Phase 4 + Phase 5 | Moyen | Filet de sécurité | **Fait** (2026-04-01) : 12 articles P4, 8 articles/22 claims P5, evals 4+5 dans evals.json |
| 4 | Test terrain (revue réelle) + feedback Phase 8 | Moyen | Haut — patterns réels | **Fait** (2026-04-01, scapulalgie scoping) |
| 4b | Corriger bugs MCP (extract_claims_regex, audit_claims, generate_bibliography) | Moyen | Haut — bloque les evals | **Fait** (2026-04-01) : path resolution, French thousands, title cross-verification |
| 5 | `/skill-adversary` sur orchestrateur litrev | Faible | Moyen — contextualisé par terrain | **Fait** (2026-04-01) : 11 findings, 3 accepted, FP 36%. Rapport : `REVIEW.md` |
| 6 | Couche 1 gates mécaniques | Moyen | Haut — erreurs détectées tôt | Prochaine étape |
| 7 | Couche 2 feedback loop systématisé | Faible | Haut (cumulatif) | **Fait** (2026-04-01, Step 9b dans SKILL.md) |
| 8 | `/full-review` intégration | Faible | Moyen — inter-composants | Après #5 |
| 9 | Couche 3 micro-audits | Élevé | Haut mais cher en tokens | Optionnel |
