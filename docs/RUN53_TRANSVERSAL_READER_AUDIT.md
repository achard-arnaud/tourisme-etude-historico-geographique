# RUN53 — audit transversal du reader V4

## Objet

Lecture continue du manuscrit V4 après RUN47–RUN52 afin de contrôler : répétitions inter-chapitres, transitions, rythme des side stories, progression de la thèse géographique et artefacts introduits par la conservation automatique des anciens blocs typés.

## Diagnostic global

La structure problem-first fonctionne désormais sur l’ensemble du manuscrit. Les chapitres 1–3 et 7 n’ont pas besoin d’une réécriture form-global supplémentaire ; RUN51/RUN52 ont corrigé 4–6 et 8 ; RUN47 couvre 9–10.

La thèse géographique progresse correctement plutôt que de rester identique :

1. **Ch. 1–2** — géographie comme contrainte écologique, hydraulique et comme condition de circulation ;
2. **Ch. 3–4** — géographie comme choix d’un nouvel optimum politique et administratif ;
3. **Ch. 5** — géographie + coûts institutionnels comme problème de résilience ;
4. **Ch. 6–7** — plusieurs optimums alternatifs : forteresse/relique, ports du sud-ouest, Palk–Mannar ;
5. **Ch. 8–9** — géographie comme asymétrie de souveraineté entre nœuds côtiers et intérieur ;
6. **Ch. 10** — infrastructure comme capacité à renverser la valeur historique du relief : la montagne défensive devient espace productif impérial.

Aucune nouvelle thèse historique n’est ajoutée par RUN53 : il s’agit exclusivement de composition.

## Corrections nécessaires

### T1 — transition 3 → 4

Le chapitre 3 terminait sur les Vēḷaikkāra et la continuité des personnels/institutions après la reconquête, puis le chapitre 4 repartait directement sur Polonnaruwa comme nouvel optimum. Le raccord causal était implicite.

**Action :** ajouter un handoff court : la reconquête ne restaure pas simplement Anuradhapura ; elle hérite d’un centre, de personnels et d’une géographie transformés par la conquête. Le chapitre 4 peut alors répondre à la question : comment cet héritage devient-il un apogée ?

### T2 — transition 7 → 8

Le chapitre 7 se terminait par un tableau comparatif Jaffna/Rajarata et une bibliographie, puis le chapitre 8 repartait depuis Colombo. Cela risquait de recréer un biais colombo-centrique.

**Action :** expliciter que le Portugal entre dans une île où plusieurs optimums territoriaux coexistent : Kotte/sud-ouest, Jaffna/Palk–Mannar, Kandy/hautes terres.

### T3 — artefact de conservation en chapitre 8

`SS-PRE-004` était automatiquement ajouté après les guardrails du nouveau chapitre 8, alors que son mécanisme Mannar/Jaffna est déjà intégré au core.

**Disposition :** `absorbed_into_core_ch8`. Le fragment reste traçable dans le corpus, mais ne doit plus être rendu une seconde fois en queue de chapitre.

### T4 — artefacts de conservation en chapitre 9

Le renderer V4 conservait des blocs legacy non fermés en les ajoutant après la conclusion RUN47. Cela produisait :

- `SS-R23-KDY-SIAM-DEZOOM-001` rendu deux fois ;
- `SS-PRE-003` après que le mécanisme *paper state / caste* a déjà été intégré au core ;
- `SS-PRE-001` après que la contraction des contrepoids européens a déjà été racontée dans le core ;
- `SS-PRE-002` (1815) à l’intérieur du chapitre VOC alors que le mécanisme est désormais développé dans le chapitre britannique ;
- trois `ARC-RECAP` successifs après la conclusion narrative.

**Dispositions :**

- `SS-R23-KDY-SIAM-DEZOOM-001` → conserver uniquement la version RUN47, correctement située après le dézoom sur les guerres européennes ;
- `SS-PRE-003` → `absorbed_into_core_ch9` ;
- `SS-PRE-001` → `absorbed_into_core_ch9` ;
- `SS-PRE-002` → `absorbed_into_core_ch10` ;
- `RECAP-A06`, `RECAP-A07`, `RECAP-A08` → conserver intégralement mais déplacer dans une **annexe de traçabilité causale** après l’épilogue, afin qu’ils ne cassent plus le rythme du reader.

Aucun de ces changements ne modifie les claims ou la force des preuves.

## Rythme des side stories

Après correction :

- Ch. 4 : 1 focus objet, bien inséré dans la démonstration ;
- Ch. 5 : 3 détours/faux leads, chacun répondant à une hypothèse causale différente ;
- Ch. 6 : 5 dézooms répartis le long du changement d’échelle, densité élevée mais justifiée par la période de recomposition régionale ;
- Ch. 8 : portrait Dona Catherina uniquement, Mannar reste dans le core ;
- Ch. 9 : dézoom Siam unique ;
- Ch. 10 : portrait D’Oyly, tandis que le dézoom impérial de 1815 est désormais core.

Le principe appliqué est celui du contrat RUN46 : lorsqu’un fragment devient nécessaire à la chaîne causale principale, il doit être absorbé dans le core plutôt que conservé artificiellement comme side story.

## Résultat attendu

Le reader doit désormais progresser comme une seule démonstration :

**écologies et corridors → État hydraulique → déplacement de l’optimum → coût de coordination → souveraineté mobile et portuaire → modèles régionaux concurrents → contrôle européen des nœuds → État côtier lisible → intégration territoriale britannique → inversion de la fonction historique de la montagne.**
