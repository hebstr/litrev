# Deferred

Findings DEFERRED lors des code reviews. A revisiter periodiquement.

| Date | Finding | Fichier | Raison du report | Echeance |
|------|---------|---------|-----------------|----------|
| 2026-03-27 | FN-3/GAP-3 : Import path pour corpus pre-existant (PMIDs, BibTeX, PDFs → combined_results.json) | skills/litrev/SKILL.md, skills/litrev-search/SKILL.md | Feature structurelle : necessite un nouveau chemin dans Phase 1/2 + potentiellement un MCP tool d'import | — |
| ~~2026-04-01~~ | ~~MCP tools de recherche directe (search_pubmed, search_s2, search_openalex)~~ | ~~mcp/~~ | **Promoted 2026-04-02**: env/API key delivery fix (completed) | — |
| 2026-04-01 | Support umbrella review (review of reviews) — workflow different : recherche de SR/MA, criteres adaptes, qualite via AMSTAR 2 | skills/litrev/SKILL.md Phase 1 | Actuellement flagge non supporte dans l'orchestrateur | — |
| ~~2026-04-02~~ | ~~`generate_bibliography` ne resout que via DOI, mais la synthese n'inclut pas de DOIs — produit un .bib vide sans le fallback orchestrateur~~ | ~~mcp/src/litrev_mcp/tools/verify.py, skills/litrev-synthesize/SKILL.md~~ | **Done**: PMID→DOI resolver ajoute (`_resolve_pmids_to_dois` + `extract_pmid_entries`) | — |
| 2026-04-02 | Tests unitaires manquants pour 5/10 modules MCP tools (abstracts, openalex_search, pubmed_search, s2_search, snowball) | mcp/tests/ | Effort dedie, 180 tests couvrent gates, audit_claims, process_results, dedup, verify, bibtex, generate_bibliography, patterns | — |
| ~~2026-04-02~~ | ~~Pas d'eval pour Phase 6 (verification) ou Phase 8 (audit) — phases ou les bugs MCP connus se concentrent~~ | ~~skills/litrev/evals/~~ | **Done** (2026-04-03): eval #6 (Phase 6 verification) et eval #7 (Phase 8 audit) ajoutes avec fixtures | — |
| 2026-03-31 | F24 — Screen evals: ajouter test edge-case pool vide | skills/litrev-screen/evals/evals.json | Amelioration eval, pas un bug | — |
| 2026-03-31 | F25 — Extract evals: ajouter test edge-case 0 articles inclus | skills/litrev-extract/evals/evals.json | Amelioration eval, pas un bug | — |
| 2026-03-31 | F26 — Orchestrator: creer une suite d'evals | skills/litrev/evals/ | Evals absentes, necessite conception dediee | — |
| 2026-03-31 | F27 — Synthesize: creer une suite d'evals | skills/litrev-synthesize/evals/ | Evals absentes, necessite conception dediee | — |
| 2026-04-01 | No eval coverage for rapid review + no-abstract path | skills/litrev-screen/evals/ | Requires creating new test data with missing abstracts for a rapid review scenario | — |
| 2026-04-01 | file_exists assertion checks review/ but eval sandbox writes to outputs/ | skills/litrev-extract/evals/evals.json | Fix depends on eval harness sandbox directory mapping behavior | — |
