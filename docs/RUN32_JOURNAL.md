# Run 32 — journal de construction

> Artefact backstage append-only. Le document de lecture n'affiche ni claims, ni IDs de bridge, ni IDs de run.

## Étape 1 — diagnostic du Run31
- constat : le from-scratch avait respecté les gates mais avait appauvri le récit ; side stories trop courtes/déplacées et canon trop petit/non chronologique ;
- cause technique : `build_from_scratch_packets.py` n'hydratait que les fragments explicitement référencés par claims/bridges/side stories ; les fragments riches seulement routés par `candidate_arc` étaient absents ;
- décision : claims = control plane ; fragments/intakes = narrative material plane.

## Étape 2 — unification de la pipeline
- `iterative` devient le mode de rédaction principal ;
- `iterative` et `from_scratch` utilisent le même builder et les mêmes étapes de draft/review/composition ; seule la phase de bootstrap diffère ;
- le bypass `legacy_fragment` déjà développé sur la branche est conservé et factorisé dans ce moteur commun.

## Étape 3 — scaffold éditorial
- import des deux DOCX approuvés comme `reader_scaffold.json` ;
- pré-1948 : 356 headings + 21 side stories inline dans le scaffold de référence ;
- post-1948 : 118 headings + 7 side stories inline ;
- `reader_scaffold` ordonne le récit ; `story_scaffold` reste la topologie de preuve/graphe.

## Étape 4 — conservation de la matière
- tous les fragments de capture pertinents par `candidate_arc` deviennent chargeables, même sans lien claim explicite ;
- les intakes archivés pertinents peuvent nourrir la recherche/rédaction sans être promus comme preuve ;
- les claims restent disponibles pour portée, confiance, type, causalité et sourcing, mais ne servent plus d'unité de prose.

## Étape 5 — side stories
- insertion uniquement à une frontière de paragraphe/heading ;
- seuil de densité pour les nouvelles side stories : 90 mots par défaut, 140 pour un focus analytique, 55 pour méthode, sauf exception explicite ;
- aucune galerie finale par défaut ; chaque détour doit avoir une place causale/chronologique et un retour au tronc.

## Étape 6 — frontstage
- retrait des `[claim:*]` et `[bridge:*]` ;
- interdiction des IDs de run et des identifiants techniques d'arc/HIL ;
- maintien possible de labels éditoriaux lisibles (`ARC A03`, `HIL-03`) lorsque le scaffold les utilise ;
- citations visibles : sources/organismes/titres, jamais claims.

## Étape 7 — lecteurs Run32
- pré-1948 : 23 884 mots, 73 pages ;
- post-1948 : 10 192 mots, 33 pages ;
- intégrations majeures repositionnées dans le fil : mudra/Bouddha, défense de Kandy, Siam Nikaya, D'Oyly, Angampora, café→thé, chaîne de valeur thé, Malaiyaha et Kandy contemporain.

## Étape 8 — QA finale
- 106/106 pages rendues et inspectées ;
- nettoyage final de 7 fuites backstage ;
- diff post-nettoyage limité à 5 pages (pré : 56, 60 ; post : 9, 15, 23), toutes réinspectées ;
- 0 `[claim:*]`, 0 `[bridge:*]`, 0 `Run <n>`, 0 ID d'arc technique avec underscore, 0 ID HIL machine dans les readers ;
- tests unitaires locaux Run32 : 4/4 verts ;
- py_compile : vert.
