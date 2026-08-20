# QA fonctionnelle — baseline Sri Lanka pré-1948

## But

Cette fixture sert de **référence de tests fonctionnels** à un agent QA. Elle rejoue le système sur le corpus pré-1948 déjà sourcé et promu. Elle ne constitue pas une nouvelle recherche historique et n'autorise aucune invention pour « remplir » une couche vide.

Commande canonique :

```bash
python scripts/qa_functional_pre1948.py
```

## Baseline attendue

| Couche | Invariant |
|---|---|
| Projet | scaffold canonique complet + `project.json` |
| Arcs | 3 ARC matérialisés |
| Claims | 9 records typés, arc-bound, source-linked |
| Sources | 37 IDs uniques, rôles d'ancrage dans le vocabulaire fermé |
| HIL | 8 indexes durables, y compris les non-findings |
| Bridges | 3 relations causales sourcées |
| Drifts | audits de l'exposition néerlandaise et de la chronologie des guerres européennes |
| Wiki | 3 pages métier |
| Graph | 4 edges |
| Questions | backlog QA persisté |
| Manuscrit | `report_v3_full.md` |
| Reader | V3 DOCX régénérable sans compression de la V1 |

## Parcours fonctionnel couvert

1. **Capture terrain/conversation** : le corpus et le registre de capitalisation restent des entrées, pas des preuves auto-promues.
2. **Sanitization** : les 9 claims persistants portent désormais explicitement `type` et `arc`.
3. **Chronologie** : chaque groupe de claims possède un `ARC.md` avec rupture d'entrée, question causale et bridge de sortie.
4. **Zoom** : les placements Z1–Z3 sont relus dans des indexes HIL durables.
5. **Sourcing** : tiers, IDs et rôles d'ancrage sont vérifiés.
6. **HIL** : les six analyses spécialisées sont rejouées contre les claims promus ; les dimensions sans claim autonome conservent un `non_finding`.
7. **Bridges** : endpoints, résultats et sources des trois bridges restent valides.
8. **Drift audit** : les anti-raccourcis historiographiques restent matérialisés.
9. **Wiki/graph** : provenance et métadonnées sont contrôlées par `qa_project.py`.
10. **Édition** : le manuscrit long reste la source canonique.
11. **Storytelling/reader** : la contrainte testée est non destructive ; la V3 ne peut pas devenir un résumé du delta.
12. **Manifest** : les 16 skills sont routées, aucune n'est silencieusement omise.
13. **Promotion** : GREEN fonctionnel avant merge.

## RED de référence

Le premier test exécutable de cette fixture a volontairement échoué sur le run GitHub Actions **#214** :

- 46 tests lancés ;
- 40 anciens tests verts ;
- **5 failures + 1 error** sur la nouvelle baseline ;
- causes : `project.json` absent, `ARC.md` absents, `type` absent des claims, runner E2E absent, couche questions/manifest absente, rôle `corroborating anchor` hors vocabulaire.

Ce RED démontre que la CI historique pouvait être verte sans prouver le workflow fonctionnel complet.

## Tests négatifs déjà couverts

La suite existante rejette notamment :

- claim causal majeur non sourcé ;
- source register JSON malformé ;
- bridge orphelin ;
- source de bridge inconnue ;
- bridge résolu non sourcé ;
- compression silencieuse d'un reader avancé ;
- perte de paragraphes/tables de la baseline V1.

## Limite assumée

Les skills analytiques/éditoriales sont des capacités agentiques, pas des fonctions Python ré-exécutables de manière déterministe. La fixture **rejoue et vérifie leurs artefacts persistés**, puis exécute tous les gates mécaniques et le renderer. Un agent QA peut ajouter des tests sémantiques, mais ne doit jamais considérer « le script est vert » comme preuve qu'une nouvelle affirmation historique est vraie.
