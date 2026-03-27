# Recommandations pour le prompt litrev — PRISE épidémiologie

## Prompt analysé

Le prompt dans PROMPT.md est utilisable tel quel. Les recommandations ci-dessous sont des optimisations pour affiner les résultats si besoin.

## 1. Fournir les critères d'exclusion d'emblée

Suggestion : pédiatrie, traumatologie aiguë (luxations, fractures), pathologies tumorales, capsulite rétractile isolée (si hors scope).

## 2. Séparer les concepts de recherche

Les outcomes mélangent deux niveaux :
- Épidémiologie descriptive : prévalence, incidence, facteurs de risque
- Poids socio-économique : maladies professionnelles, coûts, arrêts de travail

Les séparer clairement facilite la stratégie de recherche et évite des requêtes trop larges.

## 3. Clarifier "données françaises en priorité"

Ambigu pour le screening : est-ce un critère d'inclusion (exclure sans données FR) ou une préférence de classement (inclure tout, mettre en avant FR) ?
Pour une scoping review, la seconde interprétation est correcte — le préciser évite un screening trop restrictif.

## 4. Limiter le contexte projet injecté

Le CONTEXT_SUMMARY.md fait 260 lignes. Seuls les §§ "Contexte et enjeux" et "Population étudiée" sont utiles à la revue. Le reste (méthode stat, NLP, calendrier, équipe) consomme du contexte sans valeur ajoutée pour la recherche bibliographique.

## Prompt optimisé (référence)

```markdown
Lis example/CONTEXT_SUMMARY.md §§ "Contexte et enjeux" et "Population étudiée" pour le contexte du projet PRISE. Puis lance /litrev :

Épidémiologie des scapulalgies et pathologies de la coiffe des rotateurs chez l'adulte :
prévalence, incidence, facteurs de risque, et poids socio-économique.

Framework PEO :
- Population : adultes (≥18 ans)
- Exposition : scapulalgies, pathologies de la coiffe des rotateurs
- Outcomes : (1) prévalence et incidence, (2) facteurs de risque (âge, sexe, activité
  professionnelle, comorbidités), (3) reconnaissance en maladie professionnelle,
  (4) impact socio-économique (coûts directs/indirects, arrêts de travail)

Cadrage :
- Type : scoping review (état des lieux pour l'introduction du protocole PRISE, CHU de Lille)
- Période : 2010–2026
- Priorité géographique : données françaises privilégiées dans la synthèse,
  données internationales incluses pour compléter
- Exclusions : pédiatrie, traumatologie aiguë, pathologies tumorales
```
