# Review Walkthrough — litrev-extract

**Date** : 2026-04-01
**Reviewer** : skill-adversary (sans calibration)
**Cible** : `~/.claude/skills/litrev-extract`
**Mode** : adversarial (`--adversary`)
**Contexte** : personal (path ~/.claude/skills/)
**Batch** : inactif (12 findings < 15)

## Mecanismes actifs

| Mecanisme | Declenchements | Detail |
|-----------|---------------|--------|
| Author's defense | 9/9 Important+ | 3 tenues (reject), 6 non tenues (accept) |
| Cross-model L1 | 3/9 Important+ | Agent sonnet, 0 divergence |
| Cross-model L2 | 0 | Pas de divergence L1, pas de Blocking accepte |
| QA auto | 0/12 | Aucun verdict ambigu |
| Lateral think | 0 | Aucun point bloque |
| Evaluate | 1 tentative | Echec runtime Ouroboros |
| Drift | 0 | < 4 fichiers modifies, scope minimal |

## Resultats

| # | Severite | Finding | Status | Fichier(s) modifie(s) |
|---|----------|---------|--------|-----------------------|
| 1 | Blocking | Eval 1 assertion reference mauvais outil | REJECTED | — |
| 2 | Blocking | Stats non recalculees, pas d'assertion | ACCEPTED | evals/evals.json |
| 3 | Important | Year non normalise en integer, pas d'assertion | ACCEPTED | evals/evals.json |
| 4 | Important | file_exists assertion chemin incorrect | DEFERRED | — |
| 5 | Important | Benchmark vide | REJECTED | — |
| 6 | Important | Pas d'assertion sur l'exactitude des claims | ACCEPTED | evals/evals.json |
| 7 | Important | Type inconsistant du champ authors | REJECTED | — |
| 8 | Important | Champ source manquant eval 1 | REJECTED | — |
| 9 | Important | Description SKILL.md trop longue | REJECTED | — |
| 10 | Suggestion | Colonne "Quality" ambigue | ACCEPTED | SKILL.md, evals/evals.json |
| 11 | Suggestion | Pas d'eval pour full-text enrichment | NOTED | — |
| 12 | Suggestion | Logique with_claims ambigue pour title-only | REJECTED | — |

**Bilan** : 4 accepted, 5 rejected, 1 deferred, 1 noted, 1 rejected

## Detail des fixes appliques

### Fix 2 — Assertions de consistance stats (evals.json)

Ajout de 2 assertions par eval (6 au total) :
- `stats.total_quantitative_claims equals the sum of all claims array lengths across articles`
- `stats.total_semantic_claims equals the sum of all semantic_claims array lengths across articles`

**Justification** : SKILL.md Step 7 (ligne 155) ordonne explicitement de recalculer les stats. L'eval 3 avait `total_quantitative_claims: 30` vs 11 reel. Aucune assertion ne detectait cette incoherence.

### Fix 3 — Assertion normalisation year (evals.json, eval 1 uniquement)

Ajout : `All year values in article entries are integers, not strings`

**Justification** : SKILL.md Step 7 (ligne 157) exige la normalisation. Les donnees source du test-case-1 ont des annees en string — c'est le bon endroit pour tester.

### Fix 6 — Spot-checks d'exactitude (evals.json, 1 par eval)

- Eval 1 : `Yamamoto article has a claim or semantic_claim containing 20.7%`
- Eval 2 : `Chen article has a claim or semantic_claim containing SMD -0.42`
- Eval 3 : `Li article has a claim or semantic_claim containing RR 0.55`

**Justification** : Les assertions existantes ne verifient que la structure (tableaux presents, champs requis). Un executeur fabricant des valeurs passerait tous les tests. Ces spot-checks ancrent les assertions a des valeurs verbatim des abstracts sources.

### Fix 10 — Colonne "Quality" renommee "Bias Risk" (SKILL.md + evals.json)

- SKILL.md ligne 139 : `Quality` → `Bias Risk`
- evals.json eval 1 assertion : mise a jour pour correspondre

**Justification** : L'echelle `overall_rating` (low/moderate/high) mesure le risque de biais. "Low" dans une colonne "Quality" est contre-intuitif (low quality vs low risk).

## Rejets — motifs

| # | Motif du rejet |
|---|----------------|
| 1 | Le reviewer a lu eval_metadata.json (snapshot historique) au lieu de evals.json (source de verite) qui a deja l'assertion correcte |
| 5 | Les benchmark.json/md sont produits par le harness skill-creator, pas par litrev-extract. L'agregation n'a pas tourne |
| 7 | L'inconsistance authors (array vs string) est intentionnelle — variabilite reelle de litrev-search. litrev-extract ne traite pas ce champ |
| 8 | Le champ `source` est documente uniquement dans la section Full-Text Enrichment (optionnelle). Le schema de base Step 3 ne l'exige pas |
| 9 | La longueur de la description est justifiee par la desambiguation intra-famille litrev-* et le support bilingue EN/FR |
| 12 | La regle "either array is non-empty" est claire. Le `with_claims: 2` du workspace est une erreur d'execution, pas une ambiguite du spec. Les assertions stats ajoutees au fix 2 couvrent ce cas |

## Qualite du reviewer (skill-adversary)

### Points forts
- Bonne couverture : 12 findings couvrant SKILL.md, evals.json, donnees de test, et workspace
- Identification correcte des gaps d'assertions (findings 2, 3, 6) — les 3 ont ete acceptes
- Finding 10 (colonne Quality) est un vrai probleme d'UX, bien identifie
- Les findings sont bien structures : severite, fichiers, description, fix propose

### Points faibles
- **Finding 1 : erreur factuelle** — le reviewer affirme que evals.json contient `extract_claims.py` alors qu'il contient deja la bonne reference MCP. Confusion entre evals.json et eval_metadata.json (workspace snapshot). Seul finding Blocking, et c'est un faux positif
- **Taux de faux positifs** : 5/12 (42%) rejetes. Pour un reviewer adversarial, c'est acceptable mais perfectible
- **Confusion source de verite vs workspace** : les findings 1 et 5 confondent les artefacts historiques du workspace avec la configuration live
- **Findings 7, 8, 9 : meconnaissance du contexte** — le reviewer ne prend pas en compte l'architecture multi-skills (litrev-*), le workflow optionnel, ni les contraintes bilingues. Injection de calibration + contexte projet reduirait ces faux positifs
- **Pas de finding sur le champ `abstract_snippet`** dans le schema JSON (ligne 190) : il est documente dans le schema de sortie mais jamais mentionne dans les instructions de Step 3 ou Step 7 — un oubli que le reviewer n'a pas detecte

### Metriques

| Metrique | Valeur |
|----------|--------|
| Findings totaux | 12 |
| Taux d'acceptation | 33% (4/12) |
| Faux positifs (REJECTED) | 42% (5/12) |
| Vrais positifs impactants (avec fix) | 4 |
| Severite correcte | ~75% (findings 1 mal classe Blocking, finding 12 sur-estime) |
| Temps reviewer (agent) | ~100s |

### Recommandations pour ameliorer le reviewer

1. **Distinguer source de verite vs snapshots** : avant de signaler une inconsistance, verifier quel fichier est autoritatif (evals.json) vs historique (workspace/eval_metadata.json)
2. **Charger le contexte projet** : injecter les memoires de calibration du projet cible pour eviter les faux positifs lies au contexte (bilingue, architecture multi-skills)
3. **Verifier les claims factuellement** : le finding 1 cite du texte qui n'existe pas dans le fichier reference — une relecture aurait evite ce faux positif
4. **Calibrer la severite** : reserver Blocking aux defauts qui empechent le skill de fonctionner, pas aux inconsistances de workspace

## Persistence

- `DEFERRED.md` cree a la racine du projet (1 item : finding 4)
- `feedback_review_severity.md` cree dans la memoire projet (4 regles de calibration)
- `/sync-files` execute : 0 fichier stale detecte
