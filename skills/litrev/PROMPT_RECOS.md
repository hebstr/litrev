# Recommandations pour rédiger un prompt litrev

## 1. Fournir les critères d'exclusion d'emblée

Le skill va les demander, mais les fournir dans le prompt évite un aller-retour.

## 2. Séparer les concepts de recherche

Si les outcomes mélangent plusieurs niveaux (ex. épidémiologie descriptive + poids socio-économique), les séparer explicitement facilite la stratégie de recherche et évite des requêtes trop larges.

## 3. Distinguer critère d'inclusion vs préférence de classement

Si le prompt mentionne une priorité géographique ou thématique (ex. "données françaises en priorité"), préciser s'il s'agit d'un critère d'inclusion (exclure ce qui ne correspond pas) ou d'une préférence de classement (tout inclure, prioriser dans la synthèse). Sans précision, le screening risque d'être trop restrictif.

## 4. Limiter le contexte projet injecté

Si un document de contexte projet est fourni, ne pointer que les sections pertinentes pour la revue (question de recherche, population, contexte clinique). Le reste (méthode stat, planning, équipe) consomme du contexte sans valeur ajoutée pour la recherche bibliographique.

## 5. Préciser le type de revue

Le skill va le demander si absent. Fournir d'emblée un des 5 types (systematic, scoping, narrative, meta-analysis, rapid) évite un aller-retour et conditionne le pipeline (nombre de bases, screening, snowballing, qualité).

## 6. Préciser le framework

Spécifier PICO (intervention), PEO (exposition/facteur de risque) ou SPIDER (qualitatif) avec chaque composant rempli. Le skill peut le dériver de la question, mais le fournir réduit les ambiguïtés et garantit que la stratégie de recherche couvre tous les axes.

## 7. Signaler les sources de littérature grise attendues

Le pipeline interroge PubMed, Semantic Scholar et OpenAlex — pas les rapports institutionnels (CNAM-TS, DARES, EUROGIP, Santé publique France, etc.). Si ces sources sont pertinentes pour la revue, le mentionner dans le prompt permet de les documenter comme limite dès le départ plutôt que de les découvrir à l'audit.
