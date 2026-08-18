# tourisme-etude-historico-geographique

Un **OS d'enquête historico-géographique** pour transformer notes de terrain, sources et questions en arcs chronologiques causaux, artefacts réutilisables et rapports adaptés au lecteur.

## Architecture
**Arc-first + Zettelkasten-lite + graph-light.**

- `SKILL.md` : orchestrateur court et découvrable.
- `skills/` : sous-skills spécialisées par étape et dimension.
- `templates/` : contrats d'artefacts.
- `scripts/` : scaffolding et QA déterministe.
- `docs/` : décisions d'architecture, sourcing, TDD, feedback et QA.
- `tests/` : tests de contrat de la skill et des outils.
- `examples/` : corpus travaillés servant de tests grandeur nature de la méthode.

Le **wiki** porte les entités durables ; les **arcs** portent le contexte temporel ; les **HIL** portent les vues analytiques ; le **graph-light** porte uniquement les relations typées et sourcées.

## HIL et zooms
Chaque arc active seulement les dimensions utiles : institutions, géographie, économie, société, religion/culture, sécurité, système régional/global, historiographie/biais.

Les zooms vont de `Z0` objet/site à `Z4` global/systémique. Un changement d'échelle doit être relié par un mécanisme explicite.

## Source policy
Le système utilise désormais **deux axes** :
1. tiering épistémique (`T0` primaire/matériel, `T1` académique, `T2` institutionnel, `T3` navigation/encyclopédie, `T4` médiation terrain, `T5` piste exploratoire) ;
2. rôle dans l'enquête : canonical anchor, specialist institutional anchor, corroborating bridge, lead.

Un excellent corpus institutionnel reste T2 ; son importance comme ancre ne le transforme pas artificiellement en T1. Voir `docs/source_policy.md`.

## Storytelling
`editing-historical-travel-output` construit le manuscrit chronologique ; `storytelling-historical-travel` le rend pour un lecteur donné. Le reader contract contrôle :
- audience `advanced` / `intermediate` / `child` ;
- langue ;
- ton et registre ;
- length budget / contexte de lecture ;
- densité de cross-references et d'appareil historique.

Le mode enfant peut être plus romanesque dans le rythme mais ne peut jamais inventer faits, dialogues ou motivations.

## Démarrer un nouveau voyage
```bash
python scripts/new_project.py --name "Nom du voyage" --output ./projects/mon-voyage
```

Arborescence créée :
```text
<project>/
├── README.md
├── project.json
├── 00_method/
├── 01_arcs/
├── 02_hil/
├── 03_wiki/
├── 04_graph/
├── 05_sources/
├── 06_bridges/
├── 07_drifts/
├── 08_questions/
└── 09_output/
```

## Worked examples
- `examples/sri_lanka_pre_1948/` — longue durée, avec affinage VOC/Jaffna du run terrain 2026-08-18.
- `examples/sri_lanka_post_1948/` — histoire moderne, avec HIL mémoire/patrimoine/restitution borné au sein de la causalité politique et économique.

## Vérifier
```bash
python -m unittest discover -s tests -v
python scripts/audit_skill.py .
python scripts/qa_project.py <project>
```

`qa_project.py` bloque notamment les claims causaux majeurs A/B non sourcés et les références à des sources inconnues.

## Workflow Git
`dev` porte les changements ; `main` reçoit uniquement les PR revues et vérifiées.

## Méthode
La chronologie reste la colonne vertébrale humaine. Les claims ne deviennent atomiques qu'après stabilisation. Les annexes utiles sont réinjectées dans le récit sous forme de `Mais aussi`, `Petit détour`, `Point de méthode` ou `Fausse piste` plutôt que laissées dans des annexes jamais lues.

Voir :
- `docs/architecture.md`
- `docs/agent_routing.md`
- `docs/zettelkasten_graphlight_decision.md`
- `docs/source_policy.md`
- `docs/TDD_LOG.md`
- `docs/FEEDBACK_LOG.md`
