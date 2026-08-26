# tourisme-etude-historico-geographique

Un **OS réutilisable d’enquête, de composition et de narration historico-géographique**, de la note de terrain aux éditions Markdown, Word et PDF traçables.

## Architecture

**Arc-first + Zettelkasten-lite + graph-light + side-story lineage + promotion explicite.**

- `SKILL.md` : orchestrateur, gates et promotion.
- `skills/` : **18 sous-skills** spécialisées, dont `composing-side-stories`.
- `templates/` : contrats d’artefacts.
- `scripts/` : scaffolding, QA, création de side stories et rendu.
- `docs/` : architecture, SOP, TDD, feedback, manifests et QA.
- `tests/` : tests unitaires, contractuels et fonctionnels.
- `examples/` : corpus grandeur nature.

Les **arcs** portent la chronologie ; les **HIL** les vues analytiques ; le **wiki** les entités durables ; le **graph-light** les relations sourcées ; `09_output/side_stories/` porte désormais la composition latérale traçable.

## Side stories : classe de composition

Une `side_story` n’est pas une nouvelle preuve historique. Elle référence des claims/sources/bridges/HIL/drifts/origins déjà stabilisés et porte : home arc, type normalisé, purpose, raison hors-tronc, payoff, placement, retour au tronc et politique de rendu.

Nomenclature v1 :

| `kind` | Label lecteur |
|---|---|
| `detour` | Petit détour |
| `dezoom` | Dézoom |
| `also` | Mais aussi |
| `method` | Point de méthode |
| `false_lead` | Fausse piste |
| `portrait` | Personnage |
| `object_focus` | Objet / terrain |
| `comparator` | Comparaison |
| `callback` | Fil rouge |

Lifecycle : `candidate → validated → promoted → retired`.

Un `dezoom` ajoute obligatoirement `from/to/return_to` (Z0–Z4), transmission mechanism et local payoff. Toute side story promue possède un marker stable `[SIDE-STORY:<id>]` dans le Markdown. Les markers restent machine-readable mais sont masqués dans le DOCX. Le renderer bloque la perte ou le relabelling d’une side story `required_in_reader`.

SOP complète : `docs/SOP_SIDE_STORIES.md`.

### Créer une instance

```bash
python scripts/new_side_story.py \
  --project examples/sri_lanka_pre_1948 \
  --id SS-PRE-005 \
  --kind portrait \
  --arc A06_voc_coastal_state \
  --title "Willem de Melho" \
  --section-anchor "## 3. Les intermédiaires" \
  --return-to C-PRE-002 \
  --purpose "Humaniser le mécanisme d'intermédiation" \
  --source-ids SNSL-DEMELHO-2020
```

Le CLI crée un **candidate**, jamais un artefact déjà promu.

## Continuité des projets longs

Quatre couches sont suivies séparément :
1. **research** — notes, sources, claims, bridges, drifts, wiki/graph ;
2. **composition** — side stories validées/promues ;
3. **canonical Markdown** — synthèse promue ;
4. **reader export** — Word/PDF.

## HIL, zooms et comparateurs

Les zooms vont de `Z0` objet/site à `Z4` global. Un changement d’échelle exige un mécanisme explicite. Une excursion explicative hors tronc peut devenir un `dezoom`, mais seulement si elle revient à l’échelle locale avec un payoff documenté.

Une comparaison entre dans la causalité seulement si mécanisme, période, unité, confounders et sources sont compatibles et si elle change l’interprétation du cas principal. Sinon elle peut être conservée comme side story `comparator`.

## Source policy

Deux axes : tier épistémique T0–T5 et rôle d’ancrage. Plusieurs `source_register*.json` peuvent coexister avec IDs uniques. `qa_project.py` valide aussi les références utilisées par les side stories ; la composition ne modifie jamais le tier ou la confiance de l’évidence.

## Preuves vidéo YouTube

`extracting-youtube-evidence` récupère d'abord les sous-titres manuels ou automatiques, avec transcription audio explicitement autorisée en dernier recours. Chaque proposition conserve ses timestamps et reste `lead_only` jusqu'à corroboration T0–T2 ; la vidéo est enregistrée comme T5/`lead` et ne peut pas, seule, établir un fait, une métrique ou une causalité historique.

```bash
python scripts/youtube_transcript.py <URL...> --output <project>/00_method/video_evidence
python scripts/video_claim_contract.py --evidence <ledger.json...> --register <propositions.json>
```

## Pipeline de bout en bout

1. Initialiser avec `new_project.py` — y compris `09_output/side_stories/`.
2. Fixer le contrat lecteur.
3. Pour une vidéo, acquérir le transcript horodaté et ses propositions `lead_only`; capturer puis sanitizer sans conclure prématurément.
4. Construire arcs, claims, zooms, HIL et bridges.
5. Stabiliser sources, drifts, wiki/graph.
6. **Composer le hors-tronc utile** avec `composing-side-stories` : lineage + nomenclature + placement + return.
7. Construire le Markdown canonique avec `editing-historical-travel-output` en consommant les records validés/promus.
8. Appliquer éventuellement la passe `storytelling-historical-travel`, non destructive pour le preset advanced.
9. Générer Word/PDF ; contrôler rétention baseline + side stories.
10. Tracer chaque skill/handoff dans le manifest, puis tests/audits/QA avant promotion Git.

## Arborescence

```text
<project>/
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
    └── side_stories/
```

## Worked examples / baseline QA

- `examples/sri_lanka_pre_1948/` : baseline fonctionnelle de référence avec claims typés, ARC/HIL, sources, bridges, wiki/graph et side stories tracées.
- `examples/sri_lanka_post_1948/` : corpus moderne et comparatif.

Run9 a matérialisé le baseline E2E pré-1948. **Run10 ajoute la couche side-story** et son lineage sans remplacer Run9 comme preuve historique : les manifests précédents restent des snapshots historiques.

## Vérifier

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/audit_skill.py .
python scripts/audit_workflow.py docs/RUN10_SIDE_STORIES_MANIFEST.json
python scripts/qa_project.py examples/sri_lanka_pre_1948
python scripts/qa_project.py examples/sri_lanka_post_1948
python scripts/qa_functional_pre1948.py
python scripts/render_full_reader_v3.py --project all
```

`qa_project.py` bloque notamment sources inconnues/dupliquées, claims/bridges invalides, wiki/graph sans provenance, side stories hors schéma ou sans lineage/return, dezoom sans mécanisme et side stories promues sans marker/label canonique.

## Git

`dev` est la branche d’intégration ; `main` la branche promue. Feature → PR `dev` après GREEN ; `dev → main` uniquement après décision de promotion. Les branches head sont supprimées automatiquement après merge.

## Références

- `docs/SOP_SIDE_STORIES.md`
- `docs/skill_workflow_index.md`
- `docs/architecture.md`
- `docs/agent_routing.md`
- `docs/QA_PRE1948_FUNCTIONAL_BASELINE.md`
- `docs/RUN10_SIDE_STORIES_MANIFEST.json`
- `docs/TDD_LOG.md`
- `docs/FEEDBACK_LOG.md`
