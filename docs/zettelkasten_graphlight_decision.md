# Décision Zettelkasten / graph-light

## Ce que Zettelkasten améliore
- atomicité des claims ;
- séparation source-note / idée permanente ;
- connexions transversales entre périodes ;
- réutilisation des concepts récurrents ;
- diminution du copier-coller entre chapitres.

## Ce qu'un Zettelkasten pur dégrade dans un voyage
- friction de capture sur le terrain ;
- perte de contexte narratif si chaque panneau devient dix notes ;
- coût de maintenance élevé ;
- risque de confondre densité de liens et qualité historique.

## Décision
**Arc-first + claims atomiques + structure notes + graph-light.**

Les arcs sont la colonne vertébrale temporelle. Les claims deviennent atomiques une fois stabilisés. Le graph ne contient que les relations utiles au raisonnement. La vue de couverture prime sur la visualisation spectaculaire.

## Contrat des liens tagués

Une arête peut référencer `claim_ids`, `source_ids` et `bridge_ids`. Chaque référence doit résoudre dans le projet. Lorsqu'une arête porte un `bridge_id`, ses endpoints doivent être exactement les `from_claim` et `to_claim` du bridge. Le contrôle bloque les tags fantômes, les bridges projetés à l'envers et les duplications `from/relation/to`.

Un nouvel intake sans claim promu ne crée aucun lien. À l'inverse, un bridge stabilisé et réutilisable entre arcs doit être projeté explicitement dans le graph-light.
