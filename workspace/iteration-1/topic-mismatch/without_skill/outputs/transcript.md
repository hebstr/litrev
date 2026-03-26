# Analyse de la demande

## Probleme detecte : incoherence entre le protocole existant et le sujet demande

J'ai examine le fichier `review/protocol.md` et il porte sur un sujet completement different de ce que vous demandez :

- **Protocole existant** : Scoping review sur les dechirures de la coiffe des rotateurs et les comorbidites (diabete, obesite, tabac, etc.) et leur influence sur les resultats chirurgicaux.
- **Votre demande** : Impact du microbiome intestinal sur la reponse aux immunotherapies dans le cancer du poumon.

Il n'y a aucun chevauchement entre ces deux sujets. Le protocole existant ne peut pas etre reutilise, adapte, ou servir de base pour cette nouvelle revue.

## Ce qu'il faudrait faire

Pour lancer votre revue sur microbiome/immunotherapie/cancer du poumon, il faudrait **ecrire un nouveau protocole from scratch**. Voici les elements que je proposerais :

### Ebauche de protocole

**Question de recherche** : Quel est l'impact du microbiome intestinal sur la reponse aux inhibiteurs de checkpoint immunitaire (ICI) chez les patients atteints de cancer du poumon ?

**Framework PICO** :
- **Population** : Patients adultes avec cancer du poumon (NSCLC principalement, SCLC eventuellement)
- **Intervention/Exposition** : Composition ou modulation du microbiome intestinal (diversite, taxons specifiques, antibiotiques, probiotiques, transplantation fecale)
- **Comparateur** : Repondeurs vs non-repondeurs, ou patients avec/sans dysbiose
- **Outcomes** : Taux de reponse objective, survie sans progression, survie globale, toxicite immune

**Type de revue** : Revue systematique (ou scoping review si la litterature est trop heterogene)

**Concepts de recherche** :
1. Microbiome : gut microbiome, gut microbiota, intestinal microbiome, intestinal flora, dysbiosis, Akkermansia, Faecalibacterium, fecal microbiota
2. Immunotherapie : immune checkpoint inhibitor, anti-PD-1, anti-PD-L1, nivolumab, pembrolizumab, atezolizumab, durvalumab, anti-CTLA-4, ipilimumab
3. Cancer du poumon : lung cancer, non-small cell lung cancer, NSCLC, small cell lung cancer, SCLC, lung neoplasm

**Criteres d'inclusion** :
- Etudes cliniques (essais, cohortes, transversales) chez l'humain
- Patients avec cancer du poumon traites par ICI
- Analyse du microbiome intestinal (16S rRNA, metagenomique, metabolomique)
- Lien rapporte entre microbiome et reponse/outcome

**Criteres d'exclusion** :
- Etudes exclusivement animales (murines) sans validation humaine
- Editoriaux, commentaires, lettres sans donnees originales
- Etudes sur d'autres types de cancer sans donnees specifiques au poumon

## Prochaines etapes

Vous avez deux options :

1. **Remplacer le protocole** : je supprime `review/protocol.md` et j'ecris le nouveau protocole ci-dessus a la place.
2. **Garder les deux** : si la revue coiffe des rotateurs est toujours en cours ailleurs, je cree le nouveau protocole dans un dossier separe.

Qu'est-ce que vous preferez ?
