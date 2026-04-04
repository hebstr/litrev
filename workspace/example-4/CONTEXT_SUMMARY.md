# Prédiction du delirium postopératoire — Contexte

## Contexte et enjeux

Le delirium postopératoire est une complication fréquente et grave chez le patient âgé, avec une incidence de 10 à 50 % selon le type de chirurgie.
Il est associé à une augmentation de la mortalité à 6 mois, un allongement de la durée de séjour, un déclin cognitif accéléré, et une institutionnalisation plus fréquente.
Malgré son impact, le delirium reste sous-diagnostiqué dans la pratique courante.

## Outils existants

Plusieurs scores de prédiction préopératoire ont été proposés :
- Scores cliniques simples (âge, ASA, comorbidités, déficit cognitif préexistant)
- Scores composites validés (e.g. DELPOD, score de Marcantonio)
- Modèles de machine learning dérivés de données EHR (electronic health records)

La performance de ces outils varie considérablement (AUC 0.60-0.85) et leur validation externe reste limitée.

## Questions ouvertes

1. Quels facteurs de risque sont systématiquement identifiés à travers les études ?
2. Quelle est la performance comparative des scores cliniques vs modèles ML ?
3. Les modèles dérivés de données EHR (données de routine) offrent-ils un avantage par rapport aux scores nécessitant une évaluation clinique dédiée ?
4. Quels sont les obstacles à l'implémentation en pratique courante ?

## Intérêt pour le CHU de Lille

Le CHU de Lille dispose de l'EDS INCLUDE avec 13 ans de données hospitalières.
Un modèle prédictif du delirium postopératoire basé sur les données de routine pourrait être déployé en alerting automatique dans le parcours chirurgical.
Cette revue de la littérature vise à cartographier l'existant avant de concevoir un tel modèle sur les données locales.
