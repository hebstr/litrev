# Literature Review — Orchestrator Output

## Execution Tracker

```
- [ ] Phase 1 Planning
  - [ ] GATE 1: protocol printed (question, framework, scope, criteria, databases, search terms)
- [ ] Phase 2 Search (litrev-search)
- [ ] Phase 3a Screening (litrev-screen)
- [ ] Phase 3b Snowballing (litrev-snowball)
- [ ] Phase 4 Extraction (litrev-extract)
- [ ] Phase 5 Synthesis (litrev-synthesize)
- [ ] Phase 6 Verification (litrev-verify)
- [ ] Phase 7 Final Quality Check
```

## Session Resumption Check

The `review/` directory already contains files. Checking existing state:

- `review/protocol.md` exists — indicates Gate 1 was previously passed.

### Existing protocol topic

The existing `review/protocol.md` describes a **scoping review on rotator cuff tears and comorbidities**:
- Population: Adults with rotator cuff tears
- Exposure: Comorbidities (diabetes, obesity, smoking, etc.)
- Outcome: Surgical outcomes, healing rates

### Requested topic

The user is asking for a literature review on **l'impact du microbiome intestinal sur la reponse aux immunotherapies dans le cancer du poumon** (the impact of gut microbiome on immunotherapy response in lung cancer).

### Topic Mismatch Detected

These are completely different topics. The existing protocol concerns orthopedic surgery (rotator cuff / comorbidities), while the new request concerns oncology / immuno-oncology (gut microbiome / immunotherapy / lung cancer).

## Action Required — User Decision

Le repertoire `review/` contient deja un protocole pour une revue differente (ruptures de la coiffe des rotateurs et comorbidites). Ta demande porte sur le microbiome intestinal et les immunotherapies dans le cancer du poumon — c'est un sujet completement different.

Deux options :

1. **Repartir a zero** : je supprime le contenu de `review/` et je demarre une nouvelle revue sur le microbiome/immunotherapie/cancer du poumon.
2. **Utiliser un autre repertoire** : je cree un nouveau dossier (par ex. `review-microbiome/`) pour cette revue, en conservant la revue existante intacte.

Que preferes-tu ?
