# Deferred

Findings DEFERRED lors des code reviews. À revisiter périodiquement.

| Date | Finding | Fichier | Raison du report | Échéance |
|------|---------|---------|-----------------|----------|
| 2026-03-27 | FN-3/GAP-3 : Import path pour corpus pré-existant (PMIDs, BibTeX, PDFs → combined_results.json) | SKILL.md, litrev-search/SKILL.md | Feature structurelle : nécessite un nouveau chemin dans Phase 1/2 + potentiellement un MCP tool d'import | — |
| ~~2026-04-01~~ | ~~Evals manquants pour Phase 4 (extraction) et Phase 5 (synthèse)~~ | ~~evals/~~ | **Résolu 2026-04-01** : fixtures créées (12 articles P4, 8 articles/22 claims P5), evals 4+5 ajoutés dans evals.json | — |
| 2026-04-01 | MCP tools de recherche directe (search_pubmed, search_semantic_scholar, search_openalex) — encapsuler les appels WebFetch actuels pour réduire la taille des SKILL.md | litrev-mcp | Optionnel : la recherche via WebFetch fonctionne, mais les tools MCP seraient plus robustes et testables | — |
| 2026-04-01 | Support umbrella review (review of reviews) — workflow différent : recherche de SR/MA, critères adaptés, qualité via AMSTAR 2 | SKILL.md Phase 1 | Actuellement flaggé non supporté dans l'orchestrateur | — |
