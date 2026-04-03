# Plan : Migration litrev vers plugin Claude Code unifie

## Contexte

Les 6 composants litrev (orchestrateur, 4 sous-skills, serveur MCP) sont eparpilles dans `~/.claude/skills/` en tant que dossiers independants. Seuls 2 sur 6 ont un repo git. L'objectif est de les fusionner dans le repo existant `hebstr/litrev` en un plugin Claude Code unique, suivant le modele ouroboros.

## Decisions d'architecture

- **Monorepo** : le serveur MCP rejoint le repo (sous `mcp/`) -- couplage fort avec les skills, pas de publication PyPI prevue
- **Lancement MCP** : via `uv run --directory ./mcp litrev-mcp` (pas de changement de mecanisme, juste le chemin)
- **Tracking docs** (ROADMAP, DEFERRED, README, ROBUST, CONTINUATION-PROMPT) : a la racine du repo. PROMPT_RECOS reste dans `skills/litrev/` (specifique a l'orchestrateur)

## Structure cible

```
~/.claude/skills/litrev/          # = repo hebstr/litrev
├── .claude-plugin/
│   ├── marketplace.json
│   ├── plugin.json
│   └── .mcp.json
├── skills/
│   ├── litrev/                   # orchestrateur
│   │   ├── SKILL.md
│   │   ├── agents/
│   │   ├── evals/
│   │   ├── example_v1-v3/
│   │   └── PROMPT_RECOS.md
│   ├── litrev-search/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── evals/
│   ├── litrev-screen/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── evals/
│   ├── litrev-extract/
│   │   ├── SKILL.md
│   │   └── evals/
│   └── litrev-synthesize/
│       ├── SKILL.md
│       ├── assets/
│       └── evals/
├── mcp/                          # ex litrev-mcp
│   ├── src/litrev_mcp/
│   ├── tests/
│   ├── docs/
│   ├── pyproject.toml
│   ├── uv.lock
│   └── README.md
├── ROADMAP.md
├── DEFERRED.md
├── README.md
├── ROBUST.md
├── CONTINUATION-PROMPT.md
└── .gitignore
```

## Etapes d'implementation

### Phase 1 — Scaffold plugin (commit 1)

- [x] Creer `.claude-plugin/marketplace.json`, `plugin.json`, `.mcp.json`
- [x] Creer le dossier `skills/litrev/`
- [x] Deplacer dans `skills/litrev/` : SKILL.md, agents/, evals/, example_v1-v3/, PROMPT_RECOS.md
- [x] Creer les dossiers `skills/litrev-{search,screen,extract,synthesize}/`

Fichiers a creer :
- `.claude-plugin/marketplace.json` (modele ouroboros, name=litrev, owner=hebstr)
- `.claude-plugin/plugin.json` (name=litrev, version=0.1.0, skills=./skills/, mcpServers=./.mcp.json)
- `.claude-plugin/.mcp.json` (server litrev-mcp, command=uv run --directory ./mcp litrev-mcp)

### Phase 2 — Copier les sous-skills (commit 2)

- [x] Copier `~/.claude/skills/litrev-search/{SKILL.md,references/,evals/}` → `skills/litrev-search/`
- [x] Copier `~/.claude/skills/litrev-screen/{SKILL.md,references/,evals/}` → `skills/litrev-screen/`
- [x] Copier `~/.claude/skills/litrev-extract/{SKILL.md,evals/}` → `skills/litrev-extract/`
- [x] Copier `~/.claude/skills/litrev-synthesize/{SKILL.md,assets/,evals/}` → `skills/litrev-synthesize/`
- [x] Ne PAS copier les `workspace/` (donnees de dev)

### Phase 3 — Absorber litrev-mcp (commit 3)

- [x] Copier dans `mcp/` : src/, tests/, docs/, pyproject.toml, uv.lock, README.md (exclure .git, .venv, __pycache__, .ruff_cache, .pytest_cache, review/)
- [x] Consolider les DEFERRED.md (litrev-mcp, litrev-screen, litrev-extract → racine)
- [x] Supprimer les DEFERRED.md des sous-skills apres consolidation (N/A — sous-skills source non modifies, seront supprimes en Phase 8)
- [x] `cd mcp && uv sync && uv run pytest tests/ -v` pour verifier — 180 passed

### Phase 4 — Corriger les chemins (commit 4) ✓ DONE

Corrections dans les SKILL.md :

| Fichier | Ligne | Avant | Apres |
|---|---|---|---|
| `skills/litrev-screen/SKILL.md` | 69 | `~/.claude/skills/litrev-screen/references/screening_criteria.md` | `references/screening_criteria.md` |
| `skills/litrev-synthesize/SKILL.md` | ~74 | `SKILL_DIR=~/.claude/skills/litrev-synthesize` | Supprimer, remplacer les `cp "$SKILL_DIR/assets/..."` par des instructions Read/Write depuis le dossier du skill |
| `skills/litrev/SKILL.md` | agent paths | Verifier que `agents/audit_fidelity.md` etc. resolvent correctement depuis `skills/litrev/` |

Corrections dans les docs de tracking :

| Fichier | Changement |
|---|---|
| ROADMAP.md | `litrev-mcp/src/` → `mcp/src/`, `litrev-search/` → `skills/litrev-search/`, etc. |
| DEFERRED.md | Memes substitutions de chemins |
| ROBUST.md | Idem |
| CONTINUATION-PROMPT.md | Idem |
| README.md | Idem |

### Phase 5 — Mettre a jour .gitignore

- [x] Fusionner les .gitignore existants en un seul a la racine :
  ```
  __pycache__/
  *.pyc
  .venv/
  .pytest_cache/
  *.egg-info/
  dist/
  build/
  workspace/
  .ruff_cache/
  mcp/.venv/
  ```

### Phase 6 — Mettre a jour la config MCP utilisateur

- [x] Editer `~/.claude/.mcp.json` : changer le chemin de `/home/julien/.claude/skills/litrev-mcp/run.sh` vers `/home/julien/.claude/skills/litrev/mcp` avec `uv run --directory`
- [x] Verifier que le serveur MCP demarre correctement — OK, 12 tools disponibles

### Phase 7 — Verification

- [x] Tests MCP : `cd mcp && uv run pytest tests/ -v` — 180 passed
- [x] Verifier les noms de skills inchanges dans le frontmatter — OK (litrev, litrev-search, litrev-screen, litrev-extract, litrev-synthesize)
- [x] Nouvelle session Claude Code : verifier que les outils `mcp__litrev-mcp__*` sont accessibles — OK, 12 tools disponibles, prefix inchange
- [x] Deep consistency scan (allowed-tools vs registered tools, asset paths, plugin manifests) — 0 issues
- [ ] Tester `/litrev-screen` standalone : verifie la resolution de `references/screening_criteria.md` — deferred to post-cleanup
- [ ] Tester `/litrev-synthesize` standalone : verifie l'acces a `assets/review_template.md` — deferred to post-cleanup
- [ ] Tester `/litrev` avec un prompt simple : verifie la delegation aux sous-skills — deferred to post-cleanup

### Phase 8 — Nettoyage (apres verification uniquement)

- [ ] Supprimer `~/.claude/skills/litrev-search/`
- [ ] Supprimer `~/.claude/skills/litrev-screen/`
- [ ] Supprimer `~/.claude/skills/litrev-extract/`
- [ ] Supprimer `~/.claude/skills/litrev-synthesize/`
- [ ] Supprimer `~/.claude/skills/litrev-mcp/`
- [ ] Retirer l'entree litrev-mcp de `~/.claude/.mcp.json` si le plugin gere le serveur

## Risques et mitigations

| Risque | Impact | Mitigation |
|---|---|---|
| Prefix MCP change sous plugin system (`mcp__plugin_...` au lieu de `mcp__litrev-mcp__`) | Haut -- casse les `allowed-tools` | Tester en Phase 7 avant de supprimer les anciens dossiers |
| Chemins relatifs dans les blocs `!` du SKILL.md (s'executent dans le CWD, pas le dossier skill) | Moyen | Remplacer les `cp` shell par des instructions Read/Write pour le LLM |
| Historique git de litrev-mcp perdu dans le monorepo | Faible | Backup fait, historique preserve sur GitHub |

## Fichiers critiques a modifier

- `~/.claude/skills/litrev/SKILL.md` → deplace vers `skills/litrev/SKILL.md`
- `~/.claude/skills/litrev-screen/SKILL.md:69` → chemin absolu a corriger
- `~/.claude/skills/litrev-synthesize/SKILL.md:74,101-102` → SKILL_DIR et cp a remplacer
- `~/.claude/.mcp.json` → chemin MCP a mettre a jour
- `~/.claude/skills/litrev/DEFERRED.md` → cible de consolidation
