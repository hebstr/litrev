# Critique structurelle — Synthèse de la scoping review

## Résumé

La synthèse est globalement bien structurée, lisible et couvre les quatre outcomes définis par le protocole PEO. Elle adopte un ton académique adapté à une scoping review. Cependant, plusieurs écarts significatifs existent entre le protocole et l'exécution, les flux PRISMA sont incohérents, la section "maladie professionnelle" est sous-développée au regard de l'importance du sujet pour le projet PRISE, et les données françaises — pourtant annoncées comme prioritaires — reposent essentiellement sur un seul groupe de recherche. Les limites sont partiellement honnêtes mais omettent des points importants.

## Findings

### [F-B01] Incohérence du flux PRISMA — critical

**Détail** : La synthèse (lignes 59-63) rapporte : 140 identifiés, 140 après déduplication, 140 criblés, 32 inclus, 108 exclus. Or le screening_log (ligne 10) indique **109** exclus, pas 108. De plus, 32 + 109 = 141, pas 140. L'un des deux documents contient une erreur arithmétique. Par ailleurs, 0 doublons sur 140 articles provenant de 2 bases (PubMed: 90, OpenAlex: 50) est hautement improbable — on attendrait un taux de déduplication non nul entre PubMed et OpenAlex sur un sujet aussi large.

**Recommandation** : Vérifier les chiffres bruts, réconcilier les deux documents. Documenter explicitement le nombre de doublons avant déduplication (ex. : "150 identifiés, 10 doublons retirés, 140 uniques criblés").

### [F-B02] Bases de données : Scopus et Google Scholar absents, non documentés — major

**Détail** : Le protocole (lignes 28-31) spécifie trois bases : PubMed/MEDLINE, **Scopus**, et **Google Scholar** (complément). La synthèse (ligne 34) rapporte PubMed et **OpenAlex** — une base qui n'apparaît pas du tout dans le protocole. Scopus et Google Scholar ne sont pas mentionnés dans la synthèse comme ayant été abandonnés. Seul Semantic Scholar est mentionné comme non interrogé (ligne 35), mais Semantic Scholar n'apparaît pas non plus dans le protocole. Le remplacement silencieux de Scopus par OpenAlex et l'abandon de Google Scholar sans justification constituent un écart protocole/exécution non documenté.

**Recommandation** : Ajouter un paragraphe expliquant explicitement pourquoi OpenAlex a remplacé Scopus (accès institutionnel ? choix pragmatique ?), pourquoi Google Scholar n'a pas été utilisé, et corriger la mention de Semantic Scholar si elle ne correspond à rien dans le protocole.

### [F-B03] Section "Maladie professionnelle" sous-dimensionnée — major

**Détail** : L'outcome 3 du PEO est "Reconnaissance en maladie professionnelle". La section correspondante (lignes 124-131) ne comporte que 2 paragraphes, citant essentiellement 4 références (Descatha2012, Roquelaure2011, Dalboege2014, Lewis2022). Descatha2012 est qualifié "low quality" dans le JSON des claims. La section ne fournit aucun chiffre concret sur le nombre de cas reconnus en France, les tendances temporelles, ou les tableaux de maladie professionnelle (le tableau 57 est mentionné mais sans détail). Pour une revue destinée au projet PRISE qui étudie des données SNDS incluant les TMS indemnisés, cette pauvreté est problématique.

**Recommandation** : Enrichir avec des données institutionnelles (rapports Ameli, CNAM, DARES) si disponibles dans les sources. Préciser les critères du tableau 57, donner des chiffres d'évolution. Si la littérature identifiée est réellement pauvre sur ce point, le signaler explicitement comme lacune dans les limites.

### [F-B04] Dominance du groupe Roquelaure/Bodin (cohorte Pays de la Loire) — major

**Détail** : Comptage des citations dans le corps du texte (hors bibliographie) :
- Bodin2012a : 6 occurrences
- Bodin2012b : 4 occurrences
- Roquelaure2011 : 4 occurrences
- Tashjian2012 : 5 occurrences
- Lucas2022 : 5 occurrences
- Teunis2014 : 3 occurrences

Le cluster Roquelaure/Bodin (cohorte Pays de la Loire) totalise **14 citations** sur 3 références, soit une présence très forte. C'est de fait la même cohorte de 3 710 travailleurs citée 3 fois sous des angles différents. Cela ne constitue pas un biais per se — ces travaux sont les principales données françaises — mais la synthèse ne signale pas cette concentration ni le risque de surreprésentation d'une seule région française (Pays de la Loire) comme proxy des données nationales.

**Recommandation** : Ajouter une mention explicite dans les limites : les données françaises proviennent principalement d'une seule cohorte régionale, ce qui peut ne pas refléter les disparités interrégionales.

### [F-B05] Données françaises : faible volume réel — major

**Détail** : Le protocole (ligne 25) précise "Données françaises privilégiées dans la synthèse". Parmi les 32 articles inclus, les articles véritablement français sont : Bodin2012a, Bodin2012b, Roquelaure2011, Descatha2012, Tchicaya2011 — soit **5 articles** sur 32 (16 %). Tchicaya2011 porte sur des chirurgiens-dentistes en milieu hospitalier (sous-groupe très spécifique, normalement critère d'exclusion selon le protocole). Descatha2012 est de qualité "low". Les 27 autres articles sont internationaux (Danemark, Suède, USA, Australie, Chili, Corée, Chine, Iran, etc.). La priorité géographique annoncée n'est pas vraiment réalisable avec le corpus identifié, mais ce constat n'est pas explicite dans les limites.

**Recommandation** : Ajouter dans les limites que les données épidémiologiques françaises récentes au-delà de la cohorte Pays de la Loire sont rares, ce qui justifie précisément le projet PRISE. Évaluer si Tchicaya2011 aurait dû être exclu au regard du critère "sous-groupes occupationnels très spécifiques".

### [F-B06] Absence de snowballing et de littérature grise — minor

**Détail** : La section limites (lignes 163-168) ne mentionne pas l'absence de snowballing (backward/forward citation tracking), qui est une étape standard dans les scoping reviews PRISMA-ScR. Aucun rapport institutionnel (Ameli, CNAM, Santé publique France, DARES, rapports INSEE/IRDES) n'apparaît dans les sources, alors que les critères d'inclusion mentionnent explicitement "rapports institutionnels" (ligne 48).

**Recommandation** : Mentionner explicitement dans les limites l'absence de snowballing et de recherche de littérature grise/rapports institutionnels.

### [F-B07] Extraction abstract-only non signalée — minor

**Détail** : Dans le JSON des claims, tous les champs `source` sont "abstract" ou "title". Aucune claim ne provient du full-text. La synthèse ne mentionne nulle part que l'extraction s'est faite uniquement sur les titres et résumés, ce qui constitue une limitation méthodologique significative (les chiffres précis de prévalence et d'incidence se trouvent généralement dans le corps des articles).

**Recommandation** : Ajouter dans la méthodologie et les limites que l'extraction a porté sur les titres et résumés, sans accès systématique aux textes intégraux.

### [F-B08] Manque de nuances et de contradictions — major

**Détail** : La synthèse présente les résultats de manière largement cumulative ("confirment", "corroborent", "identifient") sans réellement confronter les études entre elles. Exemples :
- Waersted2020 conclut à un niveau de preuve **limité** pour l'association élévation du bras/pathologies de l'épaule (ligne 112), mais Bodin2012a identifie l'abduction comme **le** principal facteur de risque professionnel (ligne 108). Cette tension est mentionnée mais sans discussion approfondie.
- Shanahan2011 note qu'une **faible proportion** des douleurs d'épaule au travail est explicable par les conditions de travail (ligne 105), ce qui contraste avec la tonalité globale de la section "Facteurs de risque professionnels" qui insiste sur le rôle déterminant des contraintes biomécaniques.
- Yanik2020 rapporte que "peu de facteurs de risque ont été fermement établis" (claim JSON), mais la synthèse l'utilise simplement comme source supplémentaire sans relever cette prudence.

**Recommandation** : Ajouter un sous-paragraphe dans la discussion identifiant explicitement les points de divergence entre études, notamment sur le niveau de preuve de l'association entre expositions professionnelles et pathologies de l'épaule.

### [F-B09] Ligne 79 : affirmation sans citation — minor

**Détail** : La ligne 79 ("La prévalence des anomalies de la coiffe des rotateurs augmente régulièrement avec l'âge.") n'a pas de citation Pandoc. La citation apparaît à la phrase suivante (Teunis2014), mais cette première phrase est une affirmation factuelle autonome non sourcée.

**Recommandation** : Déplacer ou dupliquer la citation [@Teunis2014] à la fin de la phrase de la ligne 79, ou fusionner les deux phrases.

### [F-B10] Phrases vagues sans chiffres concrets — minor

**Détail** : Plusieurs passages restent vagues là où des chiffres seraient attendus dans une revue épidémiologique :
- Ligne 72 : "une proportion significative de la population mondiale" — quel range de prévalence ?
- Ligne 89 : "mettant en évidence une incidence élevée" — quelle incidence ?
- Ligne 130 : "une fraction substantielle" — quelle fraction attribuable ?

Ces formulations suggèrent que l'extraction abstract-only n'a pas permis de récupérer les chiffres précis, mais la synthèse ne l'admet pas.

**Recommandation** : Soit récupérer les chiffres concrets dans les articles (si accessible), soit signaler explicitement que la précision des données quantitatives est limitée par l'extraction sur résumés.

### [F-B11] Critère d'exclusion appliqué de façon incohérente — minor

**Détail** : Le protocole (et le screening_log) excluent les "sous-groupes occupationnels très spécifiques sans données généralisables". Pourtant, Tchicaya2011 (chirurgiens-dentistes en milieu hospitalier) est inclus. Le screening_log exclut les neurochirurgiens (index 17), les officiers d'ambulance (index 38), les médecins hospitaliers (index 23) pour cette même raison. L'inclusion de Tchicaya2011 semble incohérente avec ces exclusions.

**Recommandation** : Justifier l'inclusion de Tchicaya2011 ou le retirer du corpus.

### [F-B12] Section Discussion répétitive avec les Résultats — minor

**Détail** : Les trois paragraphes principaux de la Discussion (lignes 152-161) reprennent quasi verbatim les constats des Résultats sans apport interprétatif significatif. Par exemple, "l'âge est le facteur de risque le plus constant et le plus puissant" apparaît à la fois ligne 96 (Résultats) et ligne 157 (Discussion). La Discussion devrait apporter une mise en perspective plus large, pas un résumé des résultats.

**Recommandation** : Restructurer la Discussion pour qu'elle se concentre sur : (a) les implications pour le projet PRISE (déjà présent mais bref), (b) les lacunes identifiées dans la littérature, (c) les contradictions entre études, (d) la comparaison avec d'autres reviews existantes.

### [F-B13] Screening réalisé en un seul jour — minor

**Détail** : Le screening_log indique une date unique (2026-03-27), identique à la date de la review. L'ensemble du processus (recherche, screening, extraction, synthèse) semble avoir été réalisé le même jour. Pour une scoping review, même assistée par LLM, cela mérite d'être mentionné comme une limitation de la rigueur du processus.

**Recommandation** : Documenter la temporalité du processus et signaler le caractère rapide de la revue dans les limites.

---

## Bilan

| Sévérité | Count | Findings |
|----------|-------|---------|
| Critical | 1 | F-B01 |
| Major | 4 | F-B02, F-B03, F-B05, F-B08 |
| Minor | 8 | F-B04, F-B06, F-B07, F-B09, F-B10, F-B11, F-B12, F-B13 |

Les problèmes les plus préoccupants sont l'incohérence PRISMA (F-B01), l'écart non documenté protocole/exécution sur les bases de données (F-B02), et le manque de confrontation critique des sources (F-B08). La synthèse remplit son rôle de cartographie mais manque de rigueur méthodologique sur la transparence des écarts et de profondeur analytique sur les contradictions.
