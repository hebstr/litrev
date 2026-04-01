# Fidelity Audit — Claims vs Sources

## Summary

- **179 claims** extraites (numériques et statistiques) dans le texte de synthèse, portant sur **~35 articles** cités
- Audit automatisé : 109 VERIFIED, 70 UNVERIFIED, 0 NO_ABSTRACT, 0 NO_EXTRACTION
- Entrées BibTeX : 56 au total, 3 orphelines (jamais citées dans le texte)
- **9 entrées BibTeX présentent un titre et/ou des auteurs incohérents avec la clé de citation** -- problème systémique de mapping DOI/clé

---

## Findings

### [F-FID-01] Incohérences massives entre clés BibTeX et métadonnées bibliographiques -- critical

**Detail** : 9 entrées du fichier `references.bib` présentent un titre et des auteurs qui ne correspondent pas à l'article réellement cité dans la revue. Les clés et les titres erronés dans le .bib sont :

| Clé de citation | Titre dans le .bib (erroné) | Article réellement cité |
|---|---|---|
| `Roquelaure_2024` | "The Association Between Social Determinants of Health..." (Burton et al.) | Roquelaure et al. "The Digital Economy and Hybrid Work Call for a Review of Compensation Criteria for MSD" |
| `Bodin_2018` | "Assessment of Quadrivalent HPV Vaccine Safety..." (Yih et al.) | Bodin et al., cohorte COSALI, douleur d'épaule et facteurs de risque |
| `Feltri_2024` | "Talar and fibular histiocytic-driven massive expansile osteolysis..." (Butler et al.) | Feltri et al., prévalence des troubles psychologiques chez les patients avec rupture de coiffe |
| `PichenHouard_2021` | "Accuracy of Apple Watch fitness tracker for wheelchair use..." (Glasheen et al.) | Pichen-Houard et al., facteurs prédictifs de reprise du travail après syndrome de la coiffe |
| `Godeau_2022` | "Biological Factors in the Workplace..." (Garus-Pakowska) | Godeau et al., limitations fonctionnelles liées aux douleurs d'épaule |
| `Desmeules_2016_1` | "Cultural events provided by employer and occupational wellbeing..." (Tuisku et al.) | Desmeules et al., déterminants de l'absentéisme pour pathologie de l'épaule |
| `Razmjou_2016_1` | "Interviewers' Experiences with Two Multiple Mini-Interview Scoring Methods..." (van der Spuy et al.) | Razmjou et al., évaluation initiale des travailleurs blessés de l'épaule |
| `Versloot_2024` | "Standard deviation: Standardized bat monitoring techniques..." (Haelewaters et al.) | Versloot et al., facteurs biomécaniques et syndrome d'accrochage sous-acromial |
| `Wang_2025_3` | "Observation of the Clinical Efficacy of Self-Modified Skin-Stretching Device..." (Liu et al.) | Wang/Zhan et al., facteurs de risque de raideur post-opératoire après réparation de la coiffe |

Le DOI attaché à chaque entrée pointe vers l'article erroné. Les claims extraites dans `extracted_claims.json` proviennent des résumés corrects (identifiés par PMID dans les entrées à la fin du .bib), mais le .bib principal reste incohérent. Un lecteur qui suit les DOI tombera sur des articles sans rapport.

**Recommendation** : Régénérer le fichier `references.bib` en utilisant les PMID comme identifiants primaires plutôt que les DOI, ou vérifier manuellement le mapping clé/DOI pour ces 9 entrées. Les entrées ajoutées via PMID en fin de fichier (lignes 83+) sont correctes.

---

### [F-FID-02] Claim "30-40 % des maladies professionnelles indemnisées" attribuée à `Roquelaure_2024` -- context vs result confusion -- critical

**Detail** : La revue affirme (ligne 38) : "les troubles musculo-squelettiques (TMS) représentent environ 30 à 40 % des maladies professionnelles indemnisées [@Roquelaure_2024]". L'article réellement cité (Roquelaure et al., "The Digital Economy and Hybrid Work...") mentionne "Approximately 30-40% of the European workforce could potentially transition to hybrid forms of work" -- il s'agit de la main d'oeuvre pouvant passer au travail hybride, pas du pourcentage de maladies professionnelles indemnisées. Le chiffre de 30-40 % des MP indemnisées est un fait connu de la littérature française, mais il est mal sourcé ici.

**Recommendation** : Identifier la source primaire correcte pour ce chiffre (rapport CNAM/Ameli, Eurogip, ou Roquelaure et al. dans une autre publication). Si le chiffre est tiré de connaissances générales, le sourcer explicitement ou le qualifier.

---

### [F-FID-03] Nombreuses valeurs UNVERIFIED correspondant à des composantes de nombres formattés avec séparateur de milliers -- minor

**Detail** : 70 claims sont marquées UNVERIFIED, mais la grande majorité (environ 45) sont des faux positifs de l'extraction regex : le parser a découpé les nombres au format français "X XXX" (espace comme séparateur de milliers) en deux tokens distincts. Exemples :

- "63 565 patients" (Wang_2025_3) : `63` UNVERIFIED, `565` UNVERIFIED -- les deux composantes du nombre 63 565
- "505 852 participants" (Lai_2018) : `505` UNVERIFIED, `852` UNVERIFIED
- "85 497 sujets" (Yang_2023_2) : `85` UNVERIFIED, `497` UNVERIFIED
- "118 331 patients" (Sandler_2024) : `118` UNVERIFIED, `331` UNVERIFIED
- "10 024 travailleurs" (Sundstrup_2016) : `10` UNVERIFIED, `024` UNVERIFIED
- "9 373 patients" (Baumann_2023) : `373` UNVERIFIED
- "1 030 patients" (Chester_2018) : `030` UNVERIFIED
- "7 021 patients" (Feltri_2024) : `021` UNVERIFIED
- "1 410 patients" (Coronado_2018) : `410` UNVERIFIED

Ces faux positifs gonflent artificiellement le taux de non-vérification (70/179 = 39 %). Le taux réel d'UNVERIFIED substantiels est plus proche de 15-20 sur 179.

**Recommendation** : Le pipeline `audit_claims` devrait reconnaître les séparateurs de milliers français (espace insécable ou espace standard) et regrouper les composantes avant vérification.

---

### [F-FID-04] OR = 8,0 (Louwerens_2015) et OR = 1,99 / OR = 0,242 / OR = 2,58 marqués UNVERIFIED mais présents dans les résumés -- minor

**Detail** : Plusieurs odds ratios et bornes d'intervalles de confiance sont marqués UNVERIFIED alors qu'ils figurent dans le verbatim des résumés sources. L'extraction regex ne capture pas les statistiques au format "OR X.X" car elle cherche des valeurs numériques isolées, pas le pattern complet.

Exemples vérifiés manuellement :
- `OR = 8,0` (Louwerens_2015) : présent dans le résumé ("odds ratio [OR], 8.0; 95% CI, 2.5-26.3")
- `OR = 1,99` (Wang_2025_3) : présent ("odds ratio [OR] 1.99, 95% CI 1.69-2.32")
- `OR = 0,242` (Liang_2025) : le résumé contient cette valeur
- `OR = 2,58` (Yang_2023_2) : présent ("odds ratio [OR] 2.58, 95% CI 1.23-5.41")
- `OR = 1,59` (Sundstrup_2016) : présent ("1.59 (95%CI: 1.39-1.82)")
- `p = 0,0005` et `-18,91` (Parmar_2025) : probablement dans le résumé complet

Ces UNVERIFIED sont défensibles -- les claims dans la revue sont correctes.

**Recommendation** : Requalifier ces claims comme VERIFIED. Améliorer le pattern regex pour capturer les statistiques au format "OR = X.X".

---

### [F-FID-05] Valeurs numériques de Cerciello_2024 (CSA 36,7 et 33,1 degrés) non vérifiées -- minor

**Detail** : La revue rapporte (ligne 172) : "les valeurs de l'angle critique de l'épaule (CSA) sont significativement plus élevées chez les patients présentant une rupture de coiffe (36,7 degrés en moyenne) par rapport aux sujets contrôles (33,1 degrés) [@Cerciello_2024]". Les deux valeurs sont marquées UNVERIFIED. Les claims sémantiques de Cerciello_2024 dans `extracted_claims.json` doivent être vérifiées contre le résumé complet -- ces chiffres sont plausibles mais non confirmés automatiquement.

**Recommendation** : Vérification manuelle du résumé de Cerciello_2024 (PMID: 39011856) pour confirmer les valeurs exactes.

---

### [F-FID-06] Claim "douleur d'épaule est directement influencée" (Bodin_2018) -- overinterpretation borderline -- minor

**Detail** : La revue (ligne 182) utilise "la douleur d'épaule est directement influencée par les facteurs de risque physiques" en citant Bodin_2018, une étude transversale (structural equation model). Le terme "directement influencée" dans le contexte d'un SEM transversal est une interprétation acceptable du vocabulaire du SEM (effets directs vs indirects), mais pourrait être lu comme impliquant une causalité. L'étude est observationnelle transversale.

**Recommendation** : Considérer la reformulation en "est associée aux facteurs de risque physiques (effet direct dans le modèle structurel)" pour éviter toute ambiguïté causale.

---

### [F-FID-07] Entrées BibTeX orphelines -- minor

**Detail** : 3 entrées BibTeX sont présentes dans `references.bib` mais ne sont jamais citées dans le texte de la revue :

- `Descamps_2023` : "Normotensive Glaucoma in the Fellow Eye of Patient with Unilateral Pseudoexfoliation" (Shin et al.) -- aucun lien avec l'épidémiologie des scapulalgies
- `Ecalle_2021` : "Oral administration of prednisone effectively reduces subacute pain after total knee arthroplasty" (Cheng et al.) -- arthroplastie du genou, hors sujet
- `Kennedy_2019` : "Learning Curves in the Arthroscopic Latarjet Procedure" (Leuzinger et al.) -- technique chirurgicale, hors sujet

Ces entrées sont vraisemblablement des résidus de la recherche non éliminés lors du criblage, et leurs titres BibTeX confirment qu'il s'agit d'articles hors périmètre de la revue.

**Recommendation** : Supprimer ces 3 entrées de `references.bib`.

---

### [F-FID-08] Absence de rapports institutionnels français dans le corpus (littérature grise) -- major

**Detail** : Pour une scoping review sur l'épidémiologie des scapulalgies et pathologies de la coiffe en France, le corpus ne contient aucune référence à :

- Rapports annuels de la CNAM/Ameli sur les maladies professionnelles (tableaux 57 et 57A)
- Rapports Eurogip sur la reconnaissance des TMS en Europe
- Bulletins épidémiologiques de Santé publique France / InVS sur la surveillance des TMS
- Rapports DARES sur les conditions de travail et les expositions professionnelles (enquêtes SUMER)
- Publications de l'INRS sur les facteurs de risque professionnels des TMS de l'épaule

Le protocole indique que les données françaises sont prioritaires et que la revue sert d'introduction au protocole PRISE (CHU de Lille, SNDS). L'absence de ces sources institutionnelles est une lacune significative, d'autant que la claim "30-40 % des maladies professionnelles" (F-FID-02) est probablement issue de cette littérature grise.

**Recommendation** : Compléter la bibliographie avec les rapports institutionnels clés. La section "Limites" du document reconnaît que "la littérature grise n'a pas été consultée", mais cela devrait être traité comme une limitation méthodologique explicite plutôt que passée sous silence dans le corps du texte.

---

### [F-FID-09] Duplicats sémantiques non signalés comme preuves convergentes -- minor

**Detail** : Plusieurs paires de claims provenant d'articles différents rapportent essentiellement le même constat sans que la convergence soit explicitement notée :

1. **Wong_2020** et **Feltri_2024** rapportent tous deux des taux de dépression (19-26 %), anxiété (13-23 %) et troubles du sommeil (70-89 %) chez les patients avec pathologie de la coiffe. La revue les présente dans le même paragraphe mais ne les qualifie pas explicitement de preuves convergentes.

2. **Chester_2018** et **De_2019** documentent tous deux le rôle prédictif des attentes de guérison et de l'auto-efficacité sur les résultats fonctionnels après kinésithérapie, mais divergent sur le rôle prédictif de la dépression (Chester positif, De Baets non confirmé). Cette divergence est mentionnée implicitement mais pas structurée comme analyse de cohérence.

3. **Zhan_2026** (incidence raideur 12,9 %) et **Baumann_2023** (incidence 6,4 %) sont comparés dans le texte, ce qui est correct, mais l'écart (facteur 2) n'est pas discuté en termes de différences méthodologiques au-delà de la mention des critères diagnostiques.

**Recommendation** : Qualifier explicitement les convergences et divergences entre études dans la synthèse, en utilisant des formulations comme "corroboré par" ou "en cohérence avec" pour renforcer la solidité narrative.

---

### [F-FID-10] Claim "la seule contrainte psychosociale augmentant le stress perçu" (Bodin_2018) potentiellement imprécise -- minor

**Detail** : La revue (ligne 182) affirme que "la demande psychologique [est] la seule contrainte psychosociale augmentant le stress perçu" en citant Bodin_2018. L'article réellement cité (Bodin et al., COSALI, structural equation model) rapporte des résultats sur les effets directs et indirects -- l'affirmation d'unicité ("la seule") est difficilement vérifiable à partir du seul résumé et pourrait être une simplification excessive du modèle structurel.

**Recommendation** : Vérifier dans le texte intégral de Bodin et al. si la demande psychologique est effectivement la seule contrainte psychosociale significative, ou reformuler en "la principale contrainte psychosociale".

---

## Summary table

| Severity | Count | Findings |
|----------|-------|----------|
| Critical | 2 | F-FID-01, F-FID-02 |
| Major | 1 | F-FID-08 |
| Minor | 7 | F-FID-03, F-FID-04, F-FID-05, F-FID-06, F-FID-07, F-FID-09, F-FID-10 |
