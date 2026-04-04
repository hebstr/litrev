# Deferred

Findings reportés lors des code reviews. À revisiter périodiquement.

| Date | Finding | Fichier | Raison du report |
|------|---------|---------|-----------------|
| 2026-03-27 | FN-3/GAP-3 : Import path pour corpus pré-existant (PMIDs, BibTeX, PDFs → combined_results.json) | skills/litrev/SKILL.md, skills/litrev-search/SKILL.md | Feature structurelle : nécessite un nouveau chemin dans Phase 1/2 + potentiellement un MCP tool d'import |
| 2026-04-01 | Support umbrella review (review of reviews) — workflow différent : recherche de SR/MA, critères adaptés, qualité via AMSTAR 2 | skills/litrev/SKILL.md Phase 1 | Actuellement flaggé non supporté dans l'orchestrateur |
| 2026-04-02 | Tests unitaires manquants pour 5/10 modules MCP tools (abstracts, openalex_search, pubmed_search, s2_search, snowball) | mcp/tests/ | Effort dédié, 180 tests couvrent gates, audit_claims, process_results, dedup, verify, bibtex, generate_bibliography, patterns |
| 2026-03-31 | F24 — Screen evals: ajouter test edge-case pool vide | skills/litrev-screen/evals/evals.json | Amélioration eval, pas un bug |
| 2026-03-31 | F25 — Extract evals: ajouter test edge-case 0 articles inclus | skills/litrev-extract/evals/evals.json | Amélioration eval, pas un bug |
| 2026-03-31 | F26 — Orchestrator: créer une suite d'evals | skills/litrev/evals/ | Evals absentes, nécessite conception dédiée |
| 2026-03-31 | F27 — Synthesize: créer une suite d'evals | skills/litrev-synthesize/evals/ | Evals absentes, nécessite conception dédiée |
| 2026-04-04 | E2 — `search_scopus` : Elsevier API, dedup-compatible output | mcp/src/litrev_mcp/tools/ | Nécessite clé API institutionnelle (insttoken) ; couverture déjà assurée par OpenAlex |
| 2026-04-04 | E3 — `search_wos` : Clarivate Starter API | mcp/src/litrev_mcp/tools/ | Nécessite abonnement institutionnel + licence API ; couverture déjà assurée par PubMed + OpenAlex + S2 |
| 2026-04-01 | No eval coverage for rapid review + no-abstract path | skills/litrev-screen/evals/ | Requires creating new test data with missing abstracts for a rapid review scenario |
| 2026-04-01 | file_exists assertion checks review/ but eval sandbox writes to outputs/ | skills/litrev-extract/evals/evals.json | Fix depends on eval harness sandbox directory mapping behavior |
