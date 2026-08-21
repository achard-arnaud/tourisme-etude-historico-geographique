# QA fonctionnelle — baseline Sri Lanka pré-1948

## But

Cette fixture sert de **référence de tests fonctionnels** à un agent QA. Elle rejoue le système sur le corpus pré-1948 déjà sourcé et promu. Elle ne constitue pas une nouvelle recherche historique et n'autorise aucune invention pour « remplir » une couche vide.

Commande canonique :

```bash
python scripts/qa_functional_pre1948.py
```

## Baseline attendue — état courant Run 12

| Couche | Invariant |
|---|---|
| Projet | scaffold canonique complet + `project.json` |
| Arcs | 3 ARC matérialisés dans la fixture mécanique |
| Claims | 9 records typés, arc-bound, source-linked |
| Sources | **44 IDs uniques** : 37 baseline Run 9 + 7 ancres Jetavana/Saṅgha Run 12 |
| HIL | 8 indexes durables, y compris les non-findings |
| Bridges | 3 relations causales sourcées |
| Drifts | audits historiographiques persistés |
| Wiki | 3 pages métier |
| Graph | 4 edges, endpoints résolus |
| Questions | backlog QA persisté |
| Side stories | **26 records**, dont 25/25 encarts legacy tracés et 1 `analytical_focus` terrain Run 12 |
| Arc recaps | 3 récapitulatifs matérialisés/rendables |
| Manuscrit | canonique résolu par `00_method/output_state.json` |
| Reader | V3 DOCX régénérable sans compression de la V1 |

## Parcours fonctionnel couvert

1. **Capture terrain/conversation** : le corpus et le registre de capitalisation restent des entrées, pas des preuves auto-promues.
2. **Sanitization** : les claims persistants portent explicitement `type` et `arc`.
3. **Chronologie** : chaque groupe de claims matérialisé possède un `ARC.md` avec rupture d'entrée, question causale et bridge de sortie.
4. **Zoom** : les placements Z1–Z3 sont relus dans des indexes HIL durables.
5. **Sourcing** : tiers, IDs et rôles d'ancrage sont vérifiés.
6. **HIL** : les analyses spécialisées sont rejouées contre les claims promus ; les dimensions sans claim autonome conservent un `non_finding`.
7. **Bridges** : endpoints, résultats et sources des bridges restent valides.
8. **Drift audit** : les anti-raccourcis historiographiques restent matérialisés.
9. **Wiki/graph** : provenance, métadonnées et résolution des liens sont contrôlées avant édition.
10. **Composition** : side stories, `analytical_focus`, arc recaps, maps et reader profile passent le preflight avant édition.
11. **Édition** : le manuscrit long reste la source canonique résolue par état.
12. **Storytelling/reader** : la contrainte testée est non destructive ; la V3 ne peut pas devenir un résumé du delta.
13. **Workflow** : le manifeste `--latest` doit router toutes les skills connues ; le budget est contrôlé au niveau du contexte routé.
14. **Promotion** : GREEN fonctionnel avant merge.

## RED de référence — Run 9

Le premier test exécutable de cette fixture a volontairement échoué sur le run GitHub Actions **#214** :

- 46 tests lancés ;
- 40 anciens tests verts ;
- **5 failures + 1 error** sur la nouvelle baseline ;
- causes : `project.json` absent, `ARC.md` absents, `type` absent des claims, runner E2E absent, couche questions/manifest absente, rôle `corroborating anchor` hors vocabulaire.

Ce RED démontre que la CI historique pouvait être verte sans prouver le workflow fonctionnel complet.

## GREEN de référence — Run 9

Le run GitHub Actions **#216** a fermé la première boucle fonctionnelle :

- **46/46 tests** verts ;
- `SKILL AUDIT OK` ;
- Run 7 historique toujours auditable ;
- QA pré-1948 : **9 claims / 37 sources / 3 wiki / 4 graph edges / 0 warning** ;
- QA post-1948 inchangée et verte : **30 claims / 48 sources / 7 wiki / 10 graph edges / 0 warning** ;
- runner fonctionnel : **9 claims / 37 sources / 3 bridges / 3 wiki / 4 graph edges / 8 HIL** ;
- reader pré-1948 : **19 274 → 21 236 mots**, soit **110,2 % de rétention** de la baseline longue ;
- rendu complet pré + post vert.

Ces chiffres restent conservés comme **snapshot historique**, pas comme compteurs courants à maintenir artificiellement.

## Évolution Run 11

Run 11 a industrialisé la composition : side stories normalisées, coverage `tracked/discovered/untracked`, graph-light preflight, `arc_recap`, reader profiles, maps et renderer composé. Le corpus pré-1948 est passé à **25 side stories tracées, 0 untracked**, avec **3 arc recaps** et **113,0 %** de rétention sur le reader composé.

## Extension Run 12 — Jetavana / Saṅgha

Run 12 ajoute :

- **7 sources** d'ancrage dédiées au conflit monastique d'Anuradhapura, à l'économie des monastères et au callback de 1165 ;
- `SS-PRE-JETAVANA-001`, premier `side_story.kind=analytical_focus` schema **1.2** ;
- un contrat long `one_or_two_pager` : question, thèse, contrastes + caveats, mécanismes avec statut de preuve, fiscalité/ressources si pertinente, circulations transrégionales, callback, questions ouvertes, payoff ;
- intégration déterministe dans les profils lecteurs, l'édition et le storytelling ;
- compatibilité conservée avec les side stories schema 1.1.

Le focus Jetavana reste **`candidate`** tant que l'arc Anuradhapura et son lineage de claims ne sont pas matérialisés dans la fixture. La QA ne doit jamais convertir cette absence en faux IDs pour obtenir un statut `validated`.

État GREEN Run 12 (#278) : **61/61 tests**, **44 sources**, **26 side stories**, **25/25 legacy tracked**, **0 untracked**, graph **0 unresolved**, **3/3 arc recaps rendus**, rétention pré-1948 **113,0 %**.

## Tests négatifs déjà couverts

La suite rejette notamment :

- claim causal majeur non sourcé ;
- source register JSON malformé ;
- bridge orphelin ;
- source de bridge inconnue ;
- bridge résolu non sourcé ;
- compression silencieuse d'un reader avancé ;
- perte de paragraphes/tables de la baseline V1 ;
- side story promue sans lineage/placement résolu ;
- encart legacy non tracé lorsque la couverture complète est exigée ;
- arc recap non matérialisable ;
- `analytical_focus` incomplet ou palette de preuve incohérente.

## Limite assumée

Les skills analytiques/éditoriales sont des capacités agentiques, pas des fonctions Python ré-exécutables de manière déterministe. La fixture **rejoue et vérifie leurs artefacts persistés**, puis exécute tous les gates mécaniques et le renderer. Un agent QA peut ajouter des tests sémantiques, mais ne doit jamais considérer « le script est vert » comme preuve qu'une nouvelle affirmation historique est vraie.
