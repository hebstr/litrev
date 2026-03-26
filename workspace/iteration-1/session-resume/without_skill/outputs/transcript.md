# Reprise de la review -- Inhibiteurs SGLT2 dans l'insuffisance cardiaque

## Etat des lieux du dossier `review/`

J'ai parcouru l'ensemble des fichiers. Voici ou tu en es.

### Protocole (`protocol.md`)

Review systematique bien definie avec un cadre PICO :
- **Population** : Adultes avec insuffisance cardiaque (HFrEF et HFpEF)
- **Intervention** : Inhibiteurs SGLT2 (dapagliflozine, empagliflozine, canagliflozine, sotagliflozine)
- **Comparateur** : Placebo ou soins standard
- **Outcomes** : Mortalite toutes causes, mortalite cardiovasculaire, hospitalisations pour IC, qualite de vie (KCCQ)
- **Periode** : 2015-2025
- **Bases** : PubMed, Semantic Scholar, OpenAlex

### Recherche (`search_log.md`, `search_results.md`, `combined_results.json`)

**Statut : TERMINEE**

- PubMed : 7 articles
- Semantic Scholar : 3 articles (1 nouveau apres deduplication)
- Total unique : **8 articles**

Les 8 articles sont les grands essais sur le sujet : DAPA-HF (McMurray 2019), EMPEROR-Preserved (Anker 2021), SOLOIST-WHF (Bhatt 2021), EMPEROR-Preserved sous-analyse (Packer 2021), Zelniker 2019 (SR/MA Lancet), DECLARE-TIMI 58 (Wiviott 2019), EMPEROR-Reduced (Packer 2020), Vaduganathan 2022 (MA JACC).

Repartition par type d'etude : 6 RCTs, 1 revue systematique/meta-analyse, 1 meta-analyse.

### Screening (`screening_log.md`, `included_indices.json`)

**Statut : TERMINE**

- Screening titre : 8/8 retenus
- Screening abstract : 8/8 retenus
- **Articles inclus** : 8 (indices 0-7)

Aucune exclusion. Les 8 articles passent les criteres d'inclusion.

## Ce qui reste a faire

Les etapes suivantes dans le pipeline d'une revue systematique sont :

1. **Extraction des donnees** : Extraire les claims quantitatifs et qualitatifs de chaque article inclus (effectifs, HR, IC95%, criteres de jugement, duree de suivi, etc.) et evaluer la qualite methodologique de chaque etude.

2. **Synthese** : Organiser les resultats par themes (par exemple : mortalite toutes causes, hospitalisations pour IC, effets selon le phenotype HFrEF vs HFpEF, securite) et rediger la synthese narrative.

3. **Verification des citations** : Valider les DOI/PMID, generer le fichier BibTeX, verifier les eventuelles retractions.

4. **(Optionnel) Snowballing** : Suivre les references citees par ces 8 articles et les citations ulterieures pour identifier des etudes supplementaires potentiellement manquees par la recherche initiale. La recherche actuelle couvre bien les grands essais, mais une recherche sur seulement 2 bases avec 8 resultats est relativement etroite pour une revue systematique.

## Observations

- La recherche n'a pas interroge OpenAlex (mentionne dans le protocole mais absent du search_log). C'est un ecart par rapport au protocole.
- 8 articles pour une revue systematique sur un sujet aussi etudie, c'est peu. Il manque probablement des etudes importantes (DELIVER, SCORED, CANVAS, etc.). Un complement de recherche ou un snowballing serait pertinent.
- L'article Wiviott 2019 (DECLARE-TIMI 58) porte sur le diabete de type 2, pas specifiquement sur l'insuffisance cardiaque. Selon les criteres d'exclusion du protocole ("Studies on diabetes without HF"), sa place dans la review meriterait d'etre reconsideree, sauf si le sous-groupe IC est utilise.
- L'article Zelniker 2019 est une SR/MA sur la prevention cardiovasculaire dans le diabete de type 2, pas specifiquement sur l'IC -- meme remarque.

## Prochaine etape recommandee

Passer a l'extraction des donnees sur les 8 articles inclus. C'est l'etape naturelle suivante.
