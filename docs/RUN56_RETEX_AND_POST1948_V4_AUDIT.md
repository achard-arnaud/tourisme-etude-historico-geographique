# RUN56 — Retex runtime critique et V4 post-1948

## Décision

Le retex Claude a correctement identifié plusieurs symptômes, mais mélangeait
par endroits fait observé, interprétation et solution. RUN56 n'en retient que
les corrections additives qui améliorent le runtime sans modifier le contrat
de preuve. Aucun claim, bridge, tier de source ou statut de corroboration n'est
promu automatiquement.

## Lecture critique du retex Claude

| Proposition ou constat | Verdict RUN56 | Traitement |
|---|---|---|
| Le budget de contexte ignore les contrats companion | Confirmé, mais sous-estimé | L'audit suit désormais les références Markdown des skills routées, compte les fichiers runtime explicites et refuse un manifeste antérieur au dernier run. L'ancien `--latest` pouvait auditer RUN50 alors que RUN53–55 existaient. |
| Six side-stories ont été dupliquées en RUN53 | Imprécis | RUN53 portait cinq blocs side-story et trois recaps ; une répétition littérale était avérée, les autres étaient des décisions d'absorption ou de déplacement. Ces huit dispositions deviennent un ledger JSON vérifié, sans inventer un champ prétendument déjà structuré. |
| Relire l'arc entier à chaque passe | Confirmé comme coût évitable | Le skill conserve un seul contrat, avec deux modes internes `draft` et `proofread`. La relecture porte sur un chapitre et ses deux jonctions ; une signature transversale détecte ensuite les répétitions interchapitres. |
| Promouvoir un claim T4/T5 par consensus | Rejeté | La corroboration faible reste utilisable pour qualifier une side-story non porteuse, conformément au contrat existant. Elle ne peut pas promouvoir un claim causal ou transformer plusieurs sources faibles en preuve forte. |
| Créer un nouvel index global des intakes | Non retenu | `intake_registry.json` et les drafting packets couvrent déjà l'agrégation utile. Un second index créerait une nouvelle surface de drift sans bénéfice prouvé. |
| Relancer automatiquement les questions intermédiaires | Qualifié | RUN56 ajoute un audit report-only à horizon maximal de cinq runs. Il rend le backlog visible mais ne lance aucune recherche, ne ferme aucune question et ne modifie aucun statut sans arbitrage humain. |
| Un linter peut éviter la QA visuelle de 68 pages | Rejeté dans cette forme | Le linter bloque les balises, marqueurs et labels backstage détectables. La pagination, les débordements, les pages blanches et la densité restent inspectés visuellement. |
| Scinder storytelling et proofreader en deux skills | Non retenu à ce stade | Deux modes d'entrée internes permettent une relance ciblée avec moins de contexte, sans créer un nouveau contrat de passation du span gelé. |

## Changements runtime et architecture

- Le budget de contexte mesure le contexte réellement routé, y compris les
  contrats companion et les références obligatoires.
- Les dispositions core/side-story/recap de RUN53 sont déclaratives et le
  materializer les applique ; les exclusions ne sont plus codées en dur.
- Les questions intermédiaires ont des champs optionnels `opened_run` et
  `review_after_run`. L'audit RUN56 signale 11 questions stale et 16 non
  planifiées, sans mutation.
- Le graphe post-1948 conserve son gate d'endpoints (20 nœuds, 11 arêtes, zéro
  endpoint/tag non résolu) et produit en plus une densité report-only. Les
  claims orphelins restent une dette de couverture, pas une cause de rejet.
- La CI matérialise et contrôle la V4 post-1948, rend les deux Word V4 et lance
  le lint frontstage avant publication.

## QA de contrôle : arc post-1948

La V4 post-1948 est dérivée de la V3 sans recherche supplémentaire ni
compression automatique. Chacun des huit chapitres commence par sa question
causale et son synopsis. L'inventaire de citations et d'encadrés est conservé,
avec une rétention de caractères comprise entre 98,48 % et 99,28 % selon le
chapitre. Aucun doublon exact de paragraphe long ni label de production interdit
ne subsiste.

Le premier rendu a révélé une page blanche créée par l'interaction entre un
paragraphe de saut de page et une page précédente pleine. Le renderer applique
désormais `page_break_before` au titre de chapitre. Le second rendu comporte 31
pages, toutes inspectées. La V4 pré-1948 a été rerendue avec le même correctif :
68 pages, contrôlées par comparaison binaire des pages inchangées et inspection
visuelle de toutes les pages modifiées.

Résultat final des deux exports : aucun chevauchement, débordement, tableau
cassé, balise HTML brute, marqueur backstage, glyphe manquant ou page blanche.

## Limites conservées

- Le backlog de questions exige un tri humain avant tout nouveau plan de
  recherche.
- La densité du graphe post-1948 révèle une couverture causale encore inégale ;
  le diagnostic ne crée pas de preuve et n'impose pas de réécriture automatique.
- La QA visuelle reste obligatoire même lorsque le lint déterministe est vert.

## Next

Après publication, utiliser l'arc post-1948 comme témoin des nouveaux contrôles.
Ne rouvrir le split en deux skills qu'après plusieurs runs montrant qu'un état
intermédiaire de proofreading doit réellement être partagé indépendamment.
