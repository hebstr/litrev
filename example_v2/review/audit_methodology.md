# Methodology Audit — Synthesis Critique

## Summary

La synthèse est structurée, bien documentée et couvre les huit thèmes identifiés lors de l'extraction. Les principaux problèmes méthodologiques concernent une déviation de protocole non documentée sur les bases de données (OpenAlex absent), l'absence d'étape de déduplication dans le flux PRISMA, un langage cumulatif systématique dans la discussion sans confrontation des résultats contradictoires, et plusieurs limites non déclarées (criblage par LLM, revue réalisée en une seule journée, absence de snowballing).

## Findings

### [F-MET-01] OpenAlex prévu au protocole mais non interrogé — déviation non documentée — major

**Detail** : Le protocole (`protocol.md`, section Databases) liste trois bases : PubMed/MEDLINE, Semantic Scholar et OpenAlex. La synthèse (section Méthodologie, l. 65) indique « **Bases de données** : PubMed/MEDLINE, Semantic Scholar » et la section Résultats confirme « Sur 3 801 références identifiées (PubMed : 3 765, Semantic Scholar : 36) ». OpenAlex n'apparaît nulle part dans le document. La section Déviations (l. 62) déclare explicitement « Aucune déviation par rapport au protocole », ce qui est factuellement incorrect.

**Recommendation** : Documenter la suppression d'OpenAlex comme déviation de protocole dans la section Méthodologie. Ajouter cette omission dans les limites. Alternativement, réaliser effectivement la recherche OpenAlex.

---

### [F-MET-02] Absence d'étape de déduplication dans le flux PRISMA — major

**Detail** : Le flux PRISMA passe directement de « Références identifiées : n = 3 801 » à « Criblage par titre : n = 3 801 ». Aucune étape de déduplication n'est rapportée, ni dans `screening_log.md` ni dans la synthèse. Avec deux bases de données (PubMed : 3 765, Semantic Scholar : 36), zéro doublon est hautement improbable — Semantic Scholar indexe la quasi-totalité de PubMed. Le diagramme PRISMA-ScR standard exige une étape « Records after duplicates removed ».

**Recommendation** : Vérifier rétrospectivement le taux de duplication entre les deux sources et ajouter l'étape de déduplication au flux PRISMA. Si la déduplication a bien été réalisée en amont (par l'outil de recherche), le documenter explicitement.

---

### [F-MET-03] Langage exclusivement cumulatif dans la discussion — absence de confrontation — major

**Detail** : La synthèse utilise le verbe « confirmer » ou ses dérivés au moins 9 fois dans le corps du texte (ex. « confirmée par la revue systématique de Littlewood et al. », « a confirmé que le sexe féminin », « Les résultats de cette revue confirment le modèle biopsychosocial »). Aucune contradiction entre études n'est explicitement identifiée ni discutée. Par exemple :
- Yang et al. rapportent que l'obésité augmente le risque de re-rupture (OR = 2,58), tandis que Sandler et al. ne trouvent pas de différence cliniquement significative dans les scores post-opératoires — cette tension est juxtaposée mais pas analysée.
- De Baets et al. n'ont pas confirmé le rôle prédictif de la dépression et de l'anxiété, contredisant partiellement Martinez-Calderon et al. — ce point est mentionné mais la discussion ne revient pas sur cette divergence.

**Recommendation** : Ajouter un paragraphe dans la Discussion confrontant explicitement les résultats contradictoires identifiés, en analysant les différences méthodologiques ou de population qui pourraient les expliquer.

---

### [F-MET-04] Criblage par LLM non déclaré dans les limites de la synthèse — minor

**Detail** : Le `screening_log.md` (section Limitations) indique explicitement : « Screening performed by a single AI reviewer (LLM) using automated keyword-based classification ». La synthèse mentionne une « extraction semi-automatisée » (l. 119) mais ne mentionne nulle part que le criblage (titre et résumé) a été réalisé par un LLM. La section Limites ne mentionne pas cette caractéristique méthodologique.

**Recommendation** : Ajouter dans la section Limites que le criblage par titre et par résumé a été réalisé par un LLM unique sans double lecture humaine.

---

### [F-MET-05] Absence de snowballing non déclarée — minor

**Detail** : Aucune mention de snowballing (backward/forward citation chaining) n'apparaît dans `screening_log.md` ni dans la synthèse. Le protocole ne prévoyait pas explicitement de snowballing, mais pour une scoping review de cette ampleur, l'absence de cette étape est une limitation méthodologique qui devrait être documentée, notamment pour la littérature grise et les données institutionnelles françaises.

**Recommendation** : Ajouter l'absence de snowballing dans la section Limites.

---

### [F-MET-06] Revue réalisée en une seule journée non déclarée — minor

**Detail** : Toutes les dates dans `screening_log.md` (title screening, abstract screening, full-text screening) et dans la synthèse (date de recherche) sont identiques : 2026-04-01. La réalisation de l'ensemble du processus (recherche, criblage, extraction, synthèse) en une seule journée est une limitation méthodologique significative qui n'est pas documentée.

**Recommendation** : Mentionner la temporalité du processus dans les limites, en particulier l'absence de période de maturation entre les étapes.

---

### [F-MET-07] Section « Autres aspects épidémiologiques » hétérogène et sous-exploitée — minor

**Detail** : Le thème « Autres aspects épidémiologiques » (158 articles dans `extracted_claims.json`) est couvert par seulement deux études dans la synthèse (Sundstrup et al. sur l'usage d'antalgiques, Zhang et al. sur la douleur post-AVC). Avec 158 articles disponibles, cette couverture est disproportionnellement mince. De plus, le claim de Zhang et al. est accompagné d'un commentaire `<!-- UNVERIFIED -->` (l. 242), signalant une donnée non vérifiée restée dans le texte final.

**Recommendation** : Enrichir cette section à partir des claims extraits, ou justifier la couverture limitée. Retirer ou vérifier le tag `<!-- UNVERIFIED -->`.

---

### [F-MET-08] Discussion reprend les résultats sans interprétation nouvelle substantielle — minor

**Detail** : La sous-section « Principaux résultats » de la Discussion (cinq constats majeurs) reformule les résultats déjà présentés dans la section Résultats sans apporter d'interprétation véritablement nouvelle. Les points 1-5 reprennent quasi verbatim les données du corps des résultats. La sous-section « Interprétation et implications » apporte davantage de valeur ajoutée mais reste limitée à un seul paragraphe de contextualisation.

**Recommendation** : Restructurer la Discussion pour réduire la redondance avec les Résultats et développer l'interprétation comparative, les implications théoriques (modèle biopsychosocial) et les forces/faiblesses de la littérature analysée.

---

### [F-MET-09] Priorité géographique française : écart non quantifié — minor

**Detail** : Le protocole spécifie « French data prioritized ». La synthèse cite effectivement des études françaises (Bodin et al., Pichon-Houard et al., Godeau et al., Roquelaure et al.), mais ne quantifie pas la proportion d'études françaises dans le corpus de 1 114 articles. La section Discussion note que « les données françaises restent fragmentaires » mais sans chiffrer cet écart par rapport à la priorité géographique définie dans le protocole.

**Recommendation** : Quantifier le nombre d'études françaises parmi les 1 114 incluses et discuter explicitement l'écart entre la priorité géographique du protocole et la réalité du corpus.

---

## Summary table

| Severity | Count | Findings |
|----------|-------|----------|
| Critical | 0 | — |
| Major | 3 | F-MET-01, F-MET-02, F-MET-03 |
| Minor | 6 | F-MET-04, F-MET-05, F-MET-06, F-MET-07, F-MET-08, F-MET-09 |
