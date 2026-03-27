# litrev → Architecture hybride Skills + MCP

Document de travail — dernière mise à jour 2026-03-27.

## Constat initial

Le skill litrev était composé de 7 sub-skills autonomes (orchestrateur + 6 phases).
Chaque sub-skill embarquait son propre SKILL.md, scripts Python, pyproject.toml, .venv.
Problèmes identifiés :
- Duplication de code (http_utils.py, bibtex_keys.py, claim_patterns.py copiés dans 4-5 skills)
- Duplication de dépendances (5 pyproject.toml, 5 .venv)
- SKILL.md longs injectés dans le contexte → consommation de tokens élevée
- Construction de commandes Bash à la main → erreurs d'exécution fréquentes
- Pas de validation structurée des inputs/outputs

## Décision : architecture hybride

### Ce qui reste SKILL (raisonnement LLM)

| Skill | Rôle |
|-------|------|
| `litrev` | Orchestrateur : séquencement, quality gates, reprise de session, choix du type de revue |
| `litrev-search` | Stratégie de recherche (choix des termes, MeSH, adaptation par DB). Allégé : délègue l'exécution au MCP |
| `litrev-screen` | Logique de screening (application des critères, décisions include/exclude). Délègue le fetch d'abstracts au MCP |
| `litrev-extract` | Enrichissement LLM : claims sémantiques, quality assessment, thèmes. Délègue l'extraction regex au MCP |
| `litrev-synthesize` | Rédaction LLM pure — inchangé |

### Ce qui devient MCP (exécution déterministe)

**Un seul MCP server `litrev-mcp`** — 8 tools implémentés :

| Tool | Ex-skill | Fonction |
|------|----------|----------|
| `process_results` | litrev-search | Déduplique, classe, filtre, formate les résultats (markdown/json/bibtex/ris) |
| `deduplicate_results` | litrev-search | Déduplique combined_results.json par PMID/DOI/titre |
| `fetch_abstracts` | litrev-screen | Récupère abstracts manquants depuis PubMed, formate pour screening |
| `extract_claims_regex` | litrev-extract | Extraction quantitative par regex depuis les abstracts |
| `citation_chain` | litrev-snowball | Backward/forward citation chaining via S2 + OpenAlex |
| `verify_dois` | litrev-verify | Validation DOIs/PMIDs via CrossRef + check retractions PubMed |
| `generate_bibliography` | litrev-verify | Génère references.bib (résolution DOI 3 niveaux : doi.org → CrossRef → PubMed) |
| `audit_claims` | litrev-verify | Cross-vérifie chiffres du review vs extracted_claims.json |

### Ce qui disparaîtra en tant que skill

| Ex-skill | Raison |
|----------|--------|
| `litrev-snowball` | Logique scriptable → absorbé par le MCP (tool `citation_chain`) + screening géré par litrev-screen |
| `litrev-verify` | Logique scriptable → absorbé par le MCP (tools `verify_dois`, `generate_bibliography`, `audit_claims`) |

## État d'implémentation

### MCP server : FAIT

```
~/.claude/skills/litrev-mcp/
├── pyproject.toml                # deps: mcp>=1.0, httpx>=0.27
├── src/litrev_mcp/
│   ├── __init__.py
│   ├── server.py                 # FastMCP, 8 tools enregistrés
│   ├── tools/
│   │   ├── search.py             # process_results, deduplicate_results
│   │   ├── abstracts.py          # fetch_abstracts
│   │   ├── claims.py             # extract_claims_regex
│   │   ├── snowball.py           # citation_chain
│   │   └── verify.py             # verify_dois, generate_bibliography, audit_claims
│   └── lib/
│       ├── http.py               # httpx client, NCBI/CrossRef/S2 rate limiting, retry
│       ├── bibtex.py             # BibTeX key management, DOI extraction, entry building
│       ├── patterns.py           # regex claim extraction (stats, numbers, percentages)
│       └── dedup.py              # deduplicate_simple + deduplicate_merge
└── .venv/                        # installé avec uv
```

Tests passés :
- 8/8 tools enregistrés et importables
- `process_results` testé sur example data (1664 résultats, dedup, markdown OK)
- `extract_claims_regex` testé (3 articles, extraction OK)
- `audit_claims` testé sur example review (204 claims, 73 verified, 127 unverified)

### Configuration : FAIT

`~/.claude/.mcp.json` configuré :
```json
{
  "litrev-mcp": {
    "type": "stdio",
    "command": "/home/julien/.claude/skills/litrev-mcp/.venv/bin/python",
    "args": ["-m", "litrev_mcp.server"]
  }
}
```

### Allègement des SKILL.md : FAIT

Les SKILL.md de litrev-search, litrev-screen, litrev-extract utilisent les tools MCP :
- litrev-search Step 3 : `deduplicate_results`, Step 5 : `process_results`
- litrev-screen Step 2a : `fetch_abstracts`
- litrev-extract Step 2 : `extract_claims_regex`
- Orchestrateur Phase 3b : `citation_chain`, Phase 6 : `verify_dois`, `generate_bibliography`, `audit_claims`

Tests obsolètes et scripts dupliqués supprimés des 3 sub-skills.
Toutes les références à `litrev-snowball` et `litrev-verify` nettoyées dans les SKILL.md.

### Suppression des anciens sub-skills : FAIT

- litrev-snowball/ : supprimé (remplacé par MCP `citation_chain` + screening inline dans l'orchestrateur)
- litrev-verify/ : supprimé (remplacé par MCP `verify_dois`, `generate_bibliography`, `audit_claims`)

## Principe d'autonomie

L'autonomie se déplace : au lieu de skills autonomes (gros blocs prompt + scripts + deps), on a des tools autonomes (petites fonctions appelables indépendamment).

Chaque phase reste invocable indépendamment :
- `/litrev-search` → le skill guide le LLM, qui appelle les tools MCP
- Un tool MCP peut être appelé directement si besoin

## Interface contracts (inchangés)

Les fichiers dans `review/` restent le contrat entre les phases :
- `protocol.md`, `combined_results.json`, `search_results.md`, `search_log.md`
- `screening_log.md`, `included_indices.json`
- `chaining_candidates.json`
- `extracted_claims.json`
- `<topic>_review.md`, `vancouver.csl`
- `references.bib`, `claims_audit.json`, `<topic>_review_citation_report.json`

## Modules lib/ unifiés (diff vs originaux)

| Module | Origine | Changements lors de la migration |
|--------|---------|--------------------------------|
| `lib/http.py` | verify/http_utils.py (version la plus complète) | `requests` → `httpx`, `s2_throttle()` ajouté (était dans snowball), sessions globales |
| `lib/bibtex.py` | verify/bibtex_keys.py | Ajout `make_bibtex_key()` et `deduplicate_keys()` (depuis extract) |
| `lib/patterns.py` | verify/claim_patterns.py | Aucun changement (version verify était déjà la plus robuste) |
| `lib/dedup.py` | Nouveau | Deux variantes : `deduplicate_simple` (snowball) + `deduplicate_merge` (search) |

## Prochaines étapes

1. ~~**Valider end-to-end** une revue complète avec les tools MCP~~ → FAIT (2026-03-27, example_new/, scoping review épaule/coiffe, 3432 résultats → 80 inclus, double audit + walkthrough, GATE 8 PASS)
2. **Optionnel** : ajouter les tools de recherche directe (`search_pubmed`, `search_semantic_scholar`, `search_openalex`) — actuellement la recherche est faite via WebFetch par le LLM, ces tools pourraient l'encapsuler et réduire encore la taille des SKILL.md
3. **Optionnel** : support umbrella review (review of reviews) — workflow différent (recherche de SR/MA, critères adaptés, qualité via AMSTAR 2). Actuellement flaggé non supporté dans l'orchestrateur Phase 1
4. **Reporté** : import path pour corpus pré-existant (PMIDs, BibTeX, PDFs → combined_results.json) — voir DEFERRED.md
