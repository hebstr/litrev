# Deferred

Findings DEFERRED lors des code reviews. À revisiter périodiquement.

| Date | Finding | Fichier | Raison du report | Échéance |
|------|---------|---------|-----------------|----------|
| 2026-03-27 | FN-3/GAP-3 : Import path pour corpus pré-existant (PMIDs, BibTeX, PDFs → combined_results.json) | SKILL.md, litrev-search/SKILL.md | Feature structurelle : nécessite un nouveau chemin dans Phase 1/2 + potentiellement un MCP tool d'import | — |
| ~~2026-04-01~~ | ~~MCP tools de recherche directe (search_pubmed, search_s2, search_openalex)~~ | ~~litrev-mcp~~ | **Promoted 2026-04-02**: env/API key delivery fix (completed) | — |
| 2026-04-01 | Support umbrella review (review of reviews) — workflow différent : recherche de SR/MA, critères adaptés, qualité via AMSTAR 2 | SKILL.md Phase 1 | Actuellement flaggé non supporté dans l'orchestrateur | — |
| ~~2026-04-02~~ | ~~`generate_bibliography` ne résout que via DOI, mais la synthèse n'inclut pas de DOIs — produit un .bib vide sans le fallback orchestrateur~~ | ~~verify.py, litrev-synthesize/SKILL.md~~ | **Done**: PMID→DOI resolver ajouté (`_resolve_pmids_to_dois` + `extract_pmid_entries`) | — |
| 2026-04-02 | Tests unitaires manquants pour 5/10 modules MCP tools (abstracts, openalex_search, pubmed_search, s2_search, snowball) | litrev-mcp/tests/ | Effort dédié, 180 tests couvrent gates, audit_claims, process_results, dedup, verify, bibtex, generate_bibliography, patterns | — |
| ~~2026-04-02~~ | ~~Pas d'eval pour Phase 6 (verification) ou Phase 8 (audit) — phases où les bugs MCP connus se concentrent~~ | ~~litrev/evals/~~ | **Done** (2026-04-03): eval #6 (Phase 6 verification) et eval #7 (Phase 8 audit) ajoutés avec fixtures | — |
