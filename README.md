# tourisme-etude-historico-geographique

Un **OS réutilisable d’enquête et de narration historico-géographique**, de la note de terrain aux éditions Markdown, Word et PDF traçables.

## Architecture
**Arc-first + Zettelkasten-lite + graph-light + promotion explicite.**

- `SKILL.md` : orchestrateur ; checkpoint d'état, routing, comparative gate et promotion.
- `skills/` : **16 sous-skills** spécialisées par étape et dimension.
- `templates/` : contrats d'artefacts.
- `scripts/` : scaffolding et QA déterministe.
- `docs/` : décisions d'architecture, sourcing, TDD, feedback, snapshots et QA.
- `tests/` : tests de contrat de la skill, des outils et des raffinements de méthode.
- `examples/` : corpus travaillés servant de tests grandeur nature de la méthode.

Le **wiki** (`03_wiki`) porte les entités durables ; les **arcs** portent le contexte temporel ; les **HIL** portent les vues analytiques ; le **graph-light** (`04_graph`) porte uniquement les relations typées et sourcées. Depuis Run 5, wiki et graph sont **matérialisés dans les deux corpus Sri Lanka**, plus seulement décrits dans l'architecture.

## Continuité des projets longs
Trois couches sont suivies séparément :
1. **research layer** — notes, sources, claims, bridges, drifts, wiki/graph ;
2. **canonical Markdown layer** — dernière synthèse promue ;
3. **reader-export layer** — Word/PDF ou autre édition mise en forme.

Le fichier `docs/CURRENT_OUTPUT_STATUS.md` enregistre le point d'arrêt et empêche de confondre une fiche de lecture récemment intégrée avec une édition lecteur déjà régénérée.

## HIL et zooms
Chaque arc active seulement les dimensions utiles : institutions, géographie, économie, société, religion/culture, sécurité, système régional/global, historiographie/biais.

Les zooms vont de `Z0` objet/site à `Z4` global/systémique. Un changement d'échelle doit être relié par un mécanisme explicite. Les comparaisons inter-cas normalisent désormais aussi l'**unité institutionnelle** : péninsule, province, État fédéré et État souverain ne sont pas des conteneurs interchangeables.

## Source policy
Le système utilise deux axes :
1. tiering épistémique (`T0` primaire/matériel, `T1` académique, `T2` institutionnel, `T3` navigation/encyclopédie, `T4` médiation terrain, `T5` piste exploratoire) ;
2. rôle dans l'enquête : canonical anchor, specialist institutional anchor, corroborating bridge, lead.

Les projets peuvent répartir un grand corpus entre plusieurs `source_register*.json`. `qa_project.py` charge tous les registres, interdit les IDs dupliqués et contrôle les références des claims, bridges, wiki et graph.

## Comparative gate
Une comparaison n'entre dans la causalité que si :
- le mécanisme est défini de la même façon des deux côtés ;
- période, échelle et niveau institutionnel sont bornés ;
- guerre, marché, fédéralisme, migration et autres confounders structurants sont explicités ;
- les deux côtés sont correctement sourcés ;
- la comparaison modifie réellement l'interprétation du cas principal.

Le bridge distingue désormais ce qui est transportable : **instrument → mécanisme → package institutionnel → outcome**. Plus on va vers l'outcome, moins la transportabilité peut être présumée.

## Storytelling et promotion
`editing-historical-travel-output` construit le manuscrit chronologique ; `storytelling-historical-travel` peut ensuite régler la voix et la navigation. Pour le preset avancé, la longueur est sans plafond : la baseline complète est conservée, les ajouts sont traités comme des deltas et un contrôle quantitatif bloque toute compression silencieuse.

Le lifecycle d'un output est explicite : `baseline` → `vnext` → `promoted/canonical` → `reader-export`. Une nouvelle recherche ne rend jamais silencieusement un ancien Word/PDF « à jour ».

## Démarrer un nouveau voyage
```bash
python scripts/new_project.py --name "Nom du voyage" --output ./projects/mon-voyage
```

### Créer une nouvelle fresque, de bout en bout

1. **Initialiser** le projet avec `new_project.py`. Le script crée l’arborescence, le contrat lecteur et un manifeste d’exécution en brouillon.
2. **Fixer le contrat** dans `00_method/reader_contract.json` : audience, langue, ton, registre, longueur et contexte de lecture.
3. **Capturer sans conclure** : placer notes, panneaux, images ou témoignages dans la couche terrain, puis séparer faits, traditions, inférences, comparaisons et questions.
4. **Construire la colonne vertébrale** : arcs bornés par ruptures, claims sourcés, zooms Z0–Z4, HIL pertinents et bridges causaux minimaux.
5. **Stabiliser** : registres de sources, audit historiographique, wiki et graph-light. Les skills sont routées selon le problème ; elles ne sont jamais toutes appelées par réflexe.
6. **Tracer le workflow** : compléter le manifeste avec chaque skill appelée ou écartée, sa raison, ses entrées, ses sorties et son statut. Le contrôler avec `audit_workflow.py`.
7. **Promouvoir le Markdown** : `editing-historical-travel-output` structure le manuscrit ; pour un public avancé, conserver d'abord l'intégralité de la baseline et n'utiliser `storytelling-historical-travel` que comme passe non destructive de voix/navigation.
8. **Éditer le lecteur** : générer Word/PDF seulement depuis le Markdown promu, effectuer la QA visuelle et mettre à jour `CURRENT_OUTPUT_STATUS.md`.
9. **Publier** : tests + audits + QA des projets, PR vers `dev`, puis PR de promotion vers `main`.

Contrôle d’un manifeste finalisé :

```bash
python scripts/audit_workflow.py docs/RUN6_WORKFLOW_MANIFEST.json
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
- `examples/sri_lanka_pre_1948/` — longue durée ; Jaffna/Palk, VOC, paper-state, caste/codification, géopolitique européenne et bridge éducatif vers 1948.
- `examples/sri_lanka_post_1948/` — État/langue, éducation/anglais, caste et reproduction sociale, guerre/diaspora, patrimoine, puis Run 5 de comparaison **Jaffna ↔ Tamil Nadu ↔ Indonésie** et conversion territoriale du capital humain.

La passe Run 6 avait produit deux éditions lecteur v2 à partir des seuls deltas `report.md`, ce qui a comprimé le premier volume de 61 à 8 pages. Run 7 restaure les V1 longues comme baselines, matérialise les fiches de conversation, supprime le plafond avancé et produit les V3 par ajout conservatif.

## Vérifier
```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/audit_skill.py .
python scripts/audit_workflow.py docs/RUN6_WORKFLOW_MANIFEST.json
python scripts/qa_project.py examples/sri_lanka_pre_1948
python scripts/qa_project.py examples/sri_lanka_post_1948
python scripts/render_full_reader_v3.py --project all
```

`qa_project.py` bloque notamment : claims causaux majeurs A/B non sourcés, sources inconnues ou dupliquées, wiki sans métadonnées de provenance et graph edges interprétatifs non sourcés. `render_full_reader_v3.py` exerce la chaîne de publication réelle (génération DOCX + porte de rétention) ; c'est désormais aussi une étape de la CI, pas seulement une commande manuelle.

## Runtime et dépendances
Les scripts d'échafaudage et de QA (`new_project.py`, `new_arc.py`, `qa_project.py`, `audit_skill.py`, `audit_workflow.py`) sont **stdlib-only** — aucune clé, aucun réseau, aucune authentification. Seule la chaîne de publication (`render_full_reader_v3.py`, `render_reader_exports.py`) dépend de `python-docx`, déclarée dans `requirements.txt` et installée en CI avant la passe de rendu. Les scripts d'audit acceptent la variable d'environnement `SKILL_DEBUG=1` pour laisser remonter la trace complète d'une exception au lieu de l'avaler dans un message `ERROR:` ; les messages `ERROR:`/`WARN:` vont sur stderr, la ligne de statut finale sur stdout.

## Workflow Git
`dev` porte les changements ; `main` reçoit uniquement les PR revues et vérifiées. Après merge, `dev` est resynchronisée avec le merge commit et l'état d'output est sauvegardé.

## Méthode
La chronologie reste la colonne vertébrale humaine. Les claims ne deviennent atomiques qu'après stabilisation. Les thèmes verticaux — eau, caste, langue, éducation, commerce, migration — traversent les arcs sans remplacer la chronologie. Les annexes utiles sont réinjectées dans le récit sous forme de `Mais aussi`, `Petit détour`, `Point de méthode` ou `Fausse piste`.

Voir notamment :
- `docs/skill_workflow_index.md`
- `docs/RUN8_SKILLS_RUNTIME_AUDIT.md`
- `docs/architecture.md`
- `docs/agent_routing.md`
- `docs/zettelkasten_graphlight_decision.md`
- `docs/source_policy.md`
- `docs/CURRENT_OUTPUT_STATUS.md`
- `docs/PROMPT_REVIEW_RUN5.md`
- `docs/RUN5_COMPARATIVE_DEVELOPMENT_LOG.md`
- `docs/SOURCE_AUDIT_POLONNARUWA_CONVERSATION.md`
- `docs/RUN6_STORYTELLING_REVIEW.md`
- `docs/RUN6_WORKFLOW_MANIFEST.json`
- `docs/TDD_LOG.md`
- `docs/FEEDBACK_LOG.md`
