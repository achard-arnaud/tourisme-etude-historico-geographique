# Run46 — audit ciblé de la skill storytelling

## Objet

Capitaliser les retours éditoriaux issus du passage d’un récit colonial chronologique à un récit analytique géographico-sociétal, sans modifier les contrats de preuve.

## Forces déjà présentes dans la skill

La skill `storytelling-historical-travel` possède déjà des garanties fortes :

- core rédigé avant side stories ;
- fait/texture sourcée avant mécanisme ;
- relecture indépendante du core ;
- conservation anti-loss ;
- placement sémantique des side stories ;
- distinction preuve / composition ;
- scaffold lecteur séparé du graphe de preuve ;
- contrôle de l’incertitude et de la lineage.

Ces éléments restent valides.

## Gaps identifiés

### G1 — le core pouvait rester chronologique sans problématique

La skill définissait bien l’ordre du core, mais pas explicitement la **question analytique** qui donne au chapitre sa tension. Résultat possible : suite de faits correctement sourcés mais faiblement hiérarchisés.

**Correction R46 :** chaque grande section est cadrée par une problématique bornée dérivée du graphe : ce qui change, mécanismes concurrents, acteurs, géographie et coût.

### G2 — “fait avant mécanisme” ne suffisait pas à régler le dézoom

Le contrat disait de partir du fait, mais ne fixait pas complètement l’ordre : événement → mécanisme local → conséquence → dézoom causal → retour terrain.

**Correction R46 :** ordre obligatoire lorsque le dézoom explique une conséquence. On ne commence plus par une conclusion mondiale avant d’avoir raconté les éléments qui la rendent nécessaire.

### G3 — le changement d’échelle pouvait être surtypé en side story

La pipeline possède un système riche de `dezoom` en side story. Risque : envoyer hors-tronc un changement d’échelle qui est en réalité indispensable à la causalité principale.

**Correction R46 :** un dézoom nécessaire à mobilisation, légitimité, coût de gouvernement/défense, flux, reproduction sociale ou changement de régime reste dans le core. Le type `dezoom` est réservé à l’excursion autonome.

### G4 — le graphe était surtout utilisé pour retrieval/coverage, moins pour générer la problématique

Les bridges indiquaient des relations mais la skill n’imposait pas de transformer le voisinage causal en question éditoriale.

**Correction R46 :** dériver la problématique de la variable à expliquer, des mécanismes, confounders, acteurs et échelles du sous-graphe pertinent.

### G5 — manque d’un patron explicite pour les effets non intentionnels

Le corpus contient de nombreux exemples : déplacement de réseaux musulmans, documents coloniaux réutilisés par les habitants, infrastructures coloniales aux effets ultérieurs.

**Correction R46 :** patron `intention → instrument → friction → adaptation → effet non intentionnel`.

### G6 — 360 présent dans les arc recaps mais pas assez obligatoire dans la rédaction du core

Les protagonistes étaient déjà formalisés, mais la prose pouvait rester centrée sur la puissance dominante.

**Correction R46 :** test de quatre points de vue quand ils changent l’explication : pouvoir extérieur, souverain/élite locale, intermédiaires, groupes affectés. Pas de symétrie artificielle ni d’invention de motifs.

### G7 — la géographie pouvait rester descriptive

La skill multi-échelles existait, mais l’écriture n’exigeait pas explicitement que relief, port, lagune ou mousson modifient les options d’acteurs.

**Correction R46 :** une donnée géographique n’entre au tronc que si elle change coûts de transport, surveillance, défense, saisonnalité, production, taxation, contrebande, migration ou alliances.

### G8 — absence de typologie fonctionnelle des ports

Une carte de forts pouvait conduire à raconter Colombo, Mannar, Batticaloa et Trincomalee comme des points équivalents.

**Correction R46 :** classifier d’abord la fonction historique du port : transdétroit, extractif/administratif, naval-stratégique, lagunaire/interne, religieux, saisonnier. Les catégories peuvent se chevaucher.

### G9 — changements de régime racontés comme ruptures plus que comme héritages

La skill vérifie la chronologie mais ne demandait pas systématiquement : qu’est-ce qui est détruit, conservé, requalifié ou réutilisé ?

**Correction R46 :** test d’héritage obligatoire sur forts, droit, registres, catégories, communautés, compétences, religions, travail et infrastructures.

### G10 — manque d’un heuristique explicite de coût de souveraineté

Pour Kandy, « difficile à conquérir » ne suffit pas. Il faut comparer qualitativement valeur stratégique/revenus et coûts de garnison, logistique, administration et rébellion.

**Correction R46 :** heuristique ROI de souveraineté, strictement qualitative sauf séries historiques réellement comparables.

## Effet sur l’itératif

Les runs ne doivent jamais structurer le lecteur. Pour chaque passe itérative :

1. partir de la dernière baseline narrative stable ;
2. recenser tous les nouveaux claims/bridges/intakes/questions/illustrations depuis cette baseline ;
3. regrouper par **problème lecteur**, pas par run ;
4. réparer le core ;
5. introduire les dézooms causaux nécessaires ;
6. typer ensuite les excursions réellement autonomes ;
7. donner une disposition à chaque fragment éligible.

## Application immédiate R46

Les nouveaux éléments Batticaloa et Burghers ont été classés core-compatible :

- Batticaloa sert le mécanisme « géographie fonctionnelle → port → fortification → souveraineté » ;
- Burghers sert le mécanisme « communautés/compétences produites sous un régime → réutilisation par le suivant ».

Ils ne sont donc pas réduits à des side stories. Des portraits, pratiques linguistiques ou microhistoires pourront être typés ultérieurement en `portrait`/`detour` si leur autonomie narrative le justifie.

## Contrat produit

`skills/storytelling-historical-travel/PROBLEM_FIRST_CAUSAL_DEZOOM_CONTRACT.md`

Le SKILL racine rend désormais sa consommation obligatoire à l’étape storytelling avancée.
