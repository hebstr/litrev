# Audit factuel — Claims vs Sources

## Résumé

- **64 claims** extraites de **32 articles**
- Audit automatique : 61 VERIFIED, 2 NO_ABSTRACT, 1 UNVERIFIED
- 32 entrées BibTeX, toutes correspondant à un article dans extracted_claims.json (pas de DOI orphelin)
- Aucune entrée BibTeX non utilisée (couverture 1:1 entre .bib et claims)

---

## Findings

### [F-A01] Claim UNVERIFIED Tchicaya2011 — "dentists" vs abstract source — minor

**Détail** : L'audit automatique marque cette claim UNVERIFIED. L'abstract source dans combined_results.json (index 88) est présent et substantiel. Il décrit une étude cas-témoins sur les chirurgiens-dentistes à Abidjan. La claim dit "dentists" alors que l'abstract dit "dentist surgeons" ("chirurgiens-dentistes"). Par ailleurs, la claim dit "in a hospital environment" alors que l'abstract précise "public hospitals and private clinics in Abidjan". L'abstract identifie bien l'ancienneté professionnelle comme facteur de risque (et non l'âge, le sexe ou l'IMC). La claim est globalement fidèle à l'abstract, même si "dentists" simplifie "chirurgiens-dentistes" et le cadre est plus nuancé que "hospital environment".

**Statut** : défendable, mais l'UNVERIFIED semble provenir d'une difficulté de matching textuel automatique avec l'abstract en anglais approximatif. À requalifier en VERIFIED avec note.

**Recommandation** : Requalifier manuellement en VERIFIED. Préciser "dental surgeons" plutôt que "dentists" si la distinction compte.

---

### [F-A02] Claim NO_ABSTRACT Descatha2012 — abstract vide confirmé — minor

**Claim** : "Calcific tendinitis of the shoulder has compensation consequences as an occupational disease in France." (source: title)

**Détail** : L'abstract dans combined_results.json (index 82) est effectivement vide (`"abstract": ""`). La claim est dérivée du titre, qui dit "[Calcific tendinitis of the shoulder and compensation consequences: calcific disorder of tendon or tendinopathy with calcification?]". La claim est fidèle au titre.

**Recommandation** : Acceptable tel quel. Envisager de récupérer le texte intégral pour vérifier si des claims plus riches pourraient être extraites.

---

### [F-A03] Claim NO_ABSTRACT Pribicevic2012 — abstract vide confirmé — minor

**Claim** : "Narrative review synthesizing the epidemiology of shoulder pain from published literature." (source: title)

**Détail** : L'abstract dans combined_results.json (index 99) est vide (`"abstract": ""`). C'est un chapitre de livre (InTech). La claim est purement descriptive et paraphrase le titre. Elle n'apporte aucune information épidémiologique substantielle.

**Recommandation** : Claim à faible valeur informative. Envisager son retrait ou sa relégation en note, car elle ne contribue aucun fait vérifiable.

---

### [F-A04] Clausen2021 — chiffre "nine lost workdays" vs abstract réel — critical

**Claim** : "Loss of workdays is the main societal cost related to shoulder disorders, with nine lost workdays per six months on average."

**Abstract source** (index 49) : "Loss of workdays is the main societal cost related to shoulder disorders with nine lost workdays per six months on average. [...] The mean number of lost workdays per six months was **27 days** (95% CI: 18-40) for patients at risk (n = 66), corresponding to **14 days** on average (95% CI: 9-21 days) for the entire cohort (n = 129). [...] This is **three times higher** than the nine days previously reported for shoulder problems in general."

**Détail** : La claim cite "nine lost workdays per six months on average" comme si c'était le résultat de l'étude. En réalité, les 9 jours sont un chiffre de référence extérieur (issu de la littérature antérieure) que l'étude de Clausen utilise comme comparaison. Le résultat principal de Clausen est **27 jours** pour les patients à risque, soit **3 fois plus** que ces 9 jours de référence. La claim rapporte donc le chiffre de contexte comme si c'était le finding principal, ce qui est trompeur.

**Recommandation** : Corriger la claim pour refléter le résultat réel : "Patients with SIS lost an average of 27 workdays per six months, three times more than the 9 days previously reported for shoulder problems in general."

---

### [F-A05] Tashjian2012 — "more than half in their 80s" — fidèle — info

**Claim** : "The incidence of rotator cuff tears increases with aging, with more than half of individuals in their 80s having a rotator cuff tear."

**Abstract** (index 2) : "The incidence of rotator cuff tears increases with aging with more than half of individuals in their 80s having a rotator cuff tear."

**Détail** : Reproduction quasi-verbatim. Fidèle.

---

### [F-A06] Teunis2014 — chiffres précis dans l'abstract vs claim vague — minor

**Claim** : "Rotator cuff abnormalities become more common with age; prevalence increases steadily from middle age onward."

**Abstract** (index 3) : Prévalence passe de 9.7% (< 20 ans) à 62% (>= 80 ans), OR 15 (95% CI 9.6-24). La claim est correcte mais très vague comparée à l'abstract qui fournit des chiffres précis.

**Détail** : Ce n'est pas une erreur, mais une déperdition d'information. "From middle age onward" est une simplification ; les données montrent une augmentation dès les moins de 20 ans.

**Recommandation** : Envisager d'enrichir la claim avec les chiffres clés (9.7% à 62%).

---

### [F-A07] Tekavec2012 — "approximately 1%" — fidèle — info

**Claim** : "The annual consultation prevalence for shoulder pain conditions is approximately 1%, similar in women and men."

**Abstract** (index 95) : "The annual consultation prevalence for shoulder pain conditions (1%) was similar in women and men."

**Détail** : Fidèle. Le "approximately" est un ajout raisonnable.

---

### [F-A08] Jeong2017 — "486 volunteers (70.4% female)" — fidèle — info

**Claim** : "Prevalence of asymptomatic rotator cuff tears was evaluated in a Korean population sample of 486 volunteers (70.4% female)."

**Abstract** (index 66) : "The study included 486 volunteers (70.4% female; mean age, 53.1; range, 20-82 years)." Résultat : prévalence FTRCT 4.7%.

**Détail** : Les chiffres démographiques sont fidèles. La claim omet le résultat (4.7%), mais c'est un choix de formulation descriptive acceptable.

---

### [F-A09] Khosravi2019 — "500 middle-aged women aged 45-65" — fidèle — info

**Claim** : "Point and lifetime prevalence of shoulder pain were assessed in 500 middle-aged women aged 45-65 years."

**Abstract** (index 37) : "A total of 500 middle-aged women, aged 45-65 years [...] point and lifetime prevalence of shoulder pain were 18.6% and 27.6%."

**Détail** : Fidèle. La claim omet les résultats chiffrés (18.6% / 27.6%) mais les reflète implicitement.

---

### [F-A10] Djade2020 — chiffres disponibles mais non rapportés — minor

**Claim** : "The incidence of shoulder pain in adults aged 40 and over was systematically reviewed."

**Abstract** (index 26) : Fournit des chiffres d'incidence précis : 2.4% annuel (45-64 ans), 17.3/1000 PA (45-64), 12.8/1000 PA (65-74), 6.7/1000 PA (75+).

**Détail** : La claim est purement descriptive ("was systematically reviewed") et ne rapporte aucun résultat. L'abstract contient des données épidémiologiques substantielles non exploitées.

**Recommandation** : Enrichir la claim avec au moins un chiffre clé.

---

### [F-A11] Parikh2021 — chiffres de coûts disponibles mais non rapportés — minor

**Claim** : "Direct and indirect economic burden of rotator cuff tears and repairs was examined using US claims data."

**Abstract** (index 69) : Fournit des chiffres détaillés : 102,488 patients, coûts post-index $32,110 (full-thickness), pertes de productivité $5,843 (absentéisme), coût supplémentaire par retard chirurgical $8,524 (partial-thickness).

**Détail** : Même problème que F-A10 — claim purement descriptive sans résultat.

**Recommandation** : Enrichir avec les chiffres clés.

---

### [F-A12] Pierami2024 — chiffres de coûts disponibles mais non rapportés — minor

**Claim** : "Direct costs of rotator cuff repair surgery were evaluated for both open and arthroscopic techniques."

**Abstract** (index 36) : 362 patients, amélioration clinique significative chez 84.8%, technique arthroscopique 29.2% plus coûteuse, augmentation de 18.9% par jour d'hospitalisation.

**Détail** : Claim descriptive, résultats non rapportés.

**Recommandation** : Enrichir.

---

### [F-A13] Surinterprétation — Dalboege2014 claim sur fraction attribuable — minor

**Claim** : "In the general working population, a substantial fraction of SIS surgeries can be attributed to occupational shoulder exposures."

**Abstract** (index 103) : "a substantial fraction of all first-time operations for SIS could be related to occupational exposures."

**Détail** : La claim dit "can be attributed" alors que l'abstract dit "could be related". La nuance est significative : "attributed" implique une causalité plus forte que "related" (associé). De plus, l'abstract utilise le conditionnel ("could"), soulignant l'incertitude.

**Recommandation** : Revenir au langage de l'abstract : "could be related to."

---

### [F-A14] Surinterprétation — Liang2022 claim sur causalité — minor

**Claim** : "Changes in modern industrial production practices can lead to increased shoulder WRMSDs."

**Détail** : Cette formulation ("can lead to") implique une causalité. L'étude est transversale (cross-sectional), ce qui ne permet pas d'inférer la causalité. Un design transversal ne peut qu'identifier des associations.

**Recommandation** : Reformuler en "are associated with" plutôt que "can lead to".

---

### [F-A15] Couverture bibliographique — Cohorte Pays de la Loire — PRÉSENT

**Détail** : Roquelaure2011 (index 100) et Bodin2012a/2012b (index 97, 98) sont présents. Ce sont les articles de la cohorte Pays de la Loire. Bien représentés dans les claims et la synthèse.

---

### [F-A16] Couverture bibliographique — Données CNAM-TS / Assurance Maladie — ABSENT — major

**Détail** : Aucune référence aux données CNAM-TS, Assurance Maladie, ou système de remboursement français dans combined_results.json. Les rapports annuels de la branche AT-MP de l'Assurance Maladie sont une source incontournable pour les données françaises de reconnaissance en maladie professionnelle (tableau 57). Cette absence est une lacune significative pour une revue qui aborde les maladies professionnelles en France.

**Recommandation** : Ajouter les rapports statistiques AT-MP de l'Assurance Maladie (données tableau 57) comme source complémentaire.

---

### [F-A17] Couverture bibliographique — Enquêtes SUMER — ABSENT — major

**Détail** : Aucune référence aux enquêtes SUMER (Surveillance médicale des expositions des salariés aux risques professionnels) dans combined_results.json ni dans references.bib. SUMER est la principale source française sur les expositions professionnelles. Pour une revue qui inclut le thème "risk_factors_occupational" et cible le contexte français, c'est une lacune notable.

**Recommandation** : Intégrer les publications issues de SUMER (Arnaudo et al., DARES Analyses).

---

### [F-A18] Couverture bibliographique — Méta-analyse Yamamoto — ABSENT — major

**Détail** : Aucune référence à Yamamoto dans combined_results.json ni dans references.bib. Yamamoto et al. (2010, JBJS) ont publié une méta-analyse influente sur la prévalence des ruptures de coiffe asymptomatiques. Cette référence est classiquement citée dans le domaine.

**Recommandation** : Vérifier si Yamamoto et al. 2010 a été capté par la stratégie de recherche. Sinon, l'ajouter manuellement.

---

### [F-A19] Couverture bibliographique — Méta-analyse Teunis — PRÉSENT

**Détail** : Teunis2014 (index 3) est bien présent avec 2 claims extraites.

---

### [F-A20] Couverture bibliographique — Rapports EUROGIP — ABSENT — minor

**Détail** : Aucune référence EUROGIP dans combined_results.json ni references.bib. EUROGIP publie des comparaisons européennes sur la reconnaissance des TMS en maladie professionnelle. Pertinent mais moins critique que CNAM-TS/SUMER car ce sont des rapports institutionnels rarement indexés dans PubMed.

**Recommandation** : À considérer comme source complémentaire hors recherche bibliographique standard.

---

### [F-A21] Couverture bibliographique — Rapports DARES — ABSENT — minor

**Détail** : Aucune référence DARES. Même logique que F-A20 : source institutionnelle française non indexée dans les bases bibliographiques médicales.

**Recommandation** : À intégrer manuellement si le contexte français l'exige.

---

### [F-A22] DOIs orphelins dans references.bib — aucun — info

**Détail** : Les 32 entrées BibTeX correspondent exactement aux 32 articles de extracted_claims.json. Pas d'entrée BibTeX non utilisée.

---

### [F-A23] Doublons sémantiques Bodin2012a / Bodin2012b — partiellement signalés — minor

**Claim Bodin2012a** : "Age was the strongest predictor for incident cases of rotator cuff syndrome in a large French working population."
**Claim Bodin2012b** : "Age was the strongest predictor of incident shoulder pain in both genders in a large French working population."

**Détail** : Ces deux claims sont quasi-identiques (âge = principal prédicteur, même cohorte de 3710 travailleurs). La synthèse les cite conjointement à plusieurs reprises, ce qui est correct. Cependant, la distinction entre les deux (l'un sur le syndrome de la coiffe, l'autre sur la douleur d'épaule) n'est pas explicite dans les claims. Les deux articles proviennent de la même cohorte Pays de la Loire mais étudient des outcomes différents (RCS vs shoulder pain).

**Recommandation** : Ajouter une note dans les claims précisant qu'il s'agit de la même cohorte avec des outcomes différents.

---

### [F-A24] Doublons sémantiques — lésions asymptomatiques — non signalés — minor

**Claim Teunis2014** : "Many rotator cuff abnormalities are asymptomatic, and the presence of an abnormality does not necessarily correlate with symptoms."
**Claim Longo2012** : "Not all rotator cuff tears are symptomatic."
**Claim Sanders2025** : "Rotator cuff imaging abnormalities [...] are prevalent in asymptomatic adult shoulders."

**Détail** : Trois claims de trois articles différents disent essentiellement la même chose (les lésions de la coiffe sont souvent asymptomatiques). La synthèse les regroupe correctement (ligne 154), mais les claims elles-mêmes ne portent aucun marquage de convergence.

**Recommandation** : Considérer un tag "convergent" sur ces claims pour faciliter la synthèse et éviter la surreprésentation d'un même fait.

---

### [F-A25] Doublons sémantiques — "most common musculoskeletal complaint" — non signalés — minor

**Claim Shanahan2011** : "Shoulder pain is among the most common regional musculoskeletal complaints in the work environment."
**Claim DaCosta2015** : "Upper-limb work-related musculoskeletal disorders are among the most common work-related diseases."
**Claim Longo2012** : "Rotator cuff disease is among the most common musculoskeletal disorders..."
**Claim Djade2020** : "Shoulder pain is one of the most frequent musculoskeletal complaints..."
**Claim Lucas2022** : "A significant proportion of the population worldwide experiences shoulder pain daily..."

**Détail** : Cinq claims de cinq articles distincts affirment une variante de "shoulder pain / RC disease is among the most common MSK complaints". C'est une convergence forte mais redondante. Aucun mécanisme de déduplication.

**Recommandation** : Regrouper sous un fait unique avec citations multiples.

---

## Synthèse des findings par sévérité

| Sévérité | Count | Findings |
|----------|-------|---------|
| Critical | 1 | F-A04 |
| Major | 3 | F-A16, F-A17, F-A18 |
| Minor | 11 | F-A01, F-A02, F-A03, F-A06, F-A10, F-A11, F-A12, F-A13, F-A14, F-A23, F-A24, F-A25 |
| Info | 5 | F-A05, F-A07, F-A08, F-A09, F-A15, F-A19, F-A22 |

**Point critique** : F-A04 (Clausen2021) rapporte un chiffre de contexte (9 jours) comme s'il était le résultat de l'étude (27 jours). C'est une erreur factuelle à corriger en priorité.

**Lacunes majeures** : L'absence de Yamamoto (méta-analyse de référence), des données CNAM-TS/AT-MP, et des enquêtes SUMER fragilise la couverture sur les volets "prévalence en population générale" et "maladie professionnelle en France".

**Pattern récurrent** : Beaucoup de claims sont purement descriptives ("X was assessed", "Y was examined") et n'exploitent pas les chiffres disponibles dans les abstracts sources (F-A10, F-A11, F-A12). Cela réduit la valeur ajoutée de l'extraction.
