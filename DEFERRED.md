# Deferred

Findings DEFERRED lors des code reviews. À revisiter périodiquement.

| Date | Finding | Fichier | Raison du report | Échéance |
|------|---------|---------|-----------------|----------|
| 2026-03-27 | FN-3/GAP-3 : Import path pour corpus pré-existant (PMIDs, BibTeX, PDFs → combined_results.json) | SKILL.md, litrev-search/SKILL.md | Feature structurelle : nécessite un nouveau chemin dans Phase 1/2 + potentiellement un MCP tool d'import | — |
| ~~2026-04-01~~ | ~~MCP tools de recherche directe (search_pubmed, search_s2, search_openalex)~~ | ~~litrev-mcp~~ | **Promoted 2026-04-02**: env/API key delivery fix (completed) | — |
| 2026-04-01 | Support umbrella review (review of reviews) — workflow différent : recherche de SR/MA, critères adaptés, qualité via AMSTAR 2 | SKILL.md Phase 1 | Actuellement flaggé non supporté dans l'orchestrateur | — |
| 2026-04-02 | `generate_bibliography` ne résout que via DOI, mais la synthèse n'inclut pas de DOIs — produit un .bib vide sans le fallback orchestrateur | verify.py, litrev-synthesize/SKILL.md | Nécessite ajout d'un resolver PMID→DOI dans generate_bibliography | — |
| 2026-04-02 | Tests unitaires manquants pour 7/10 modules MCP tools (search, claims, abstracts, snowball, verify entry points) | litrev-mcp/tests/ | Effort dédié, priorité : process_results, audit_claims, generate_bibliography | — |
| 2026-04-02 | Pas d'eval pour Phase 6 (verification) ou Phase 8 (audit) — phases où les bugs MCP connus se concentrent | litrev/evals/ | À créer après les tests unitaires manquants | — |
