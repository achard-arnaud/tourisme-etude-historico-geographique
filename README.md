# tourisme-etude-historico-geographique

Un **OS d'enquête historico-géographique** pour transformer notes de terrain, sources et questions en arcs chronologiques causaux, artefacts réutilisables et rapport de lecture.

## Architecture
**Arc-first + Zettelkasten-lite + graph-light.**

- `SKILL.md` : orchestrateur court et découvrable.
- `skills/` : sous-skills spécialisées par étape et dimension.
- `templates/` : contrats d'artefacts.
- `scripts/` : scaffolding et QA déterministe.
- `docs/` : décisions d'architecture, sourcing, TDD et QA.
- `tests/` : tests de contrat de la skill et des outils.

Le **wiki** porte les entités durables ; les **arcs** portent le contexte temporel ; les **HIL** portent les vues analytiques ; le **graph-light** porte uniquement les relations typées et sourcées.

## HIL et zooms
Chaque arc active seulement les dimensions utiles : institutions, géographie, économie, société, religion/culture, sécurité, système régional/global, historiographie/biais.

Les zooms vont de `Z0` objet/site à `Z4` global/systémique. Un changement d'échelle doit être relié par un mécanisme explicite.

## Source policy
Tiering par rôle épistémique : `T0` primaire/matériel, `T1` académique, `T2` institutionnel, `T3` navigation/encyclopédie, `T4` médiation terrain, `T5` piste exploratoire. Voir `docs/source_policy.md`.

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
- `docs/TDD_LOG.md`
