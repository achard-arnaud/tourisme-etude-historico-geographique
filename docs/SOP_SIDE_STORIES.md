# SOP — Side stories

## 1. Purpose

`side_story` is the controlled composition layer between stabilized research and final reader output. It covers lateral material that should survive the investigation without being promoted into the causal trunk merely because it is interesting.

Canonical path: `09_output/side_stories/<SIDE_STORY_ID>.json`.

The artefact carries **lineage and editorial intent**; historical truth remains owned by claims, sources, bridges, HILs and drift audits.

## 2. Nomenclature v1

| `kind` | Reader label | Use |
|---|---|---|
| `detour` | Petit détour | lateral mechanism/context |
| `dezoom` | Dézoom | Z0/Z1 → Z2/Z3/Z4 excursion with explicit return |
| `also` | Mais aussi | secondary evidence that enriches the home case |
| `method` | Point de méthode | epistemic/source/method correction |
| `false_lead` | Fausse piste | rejected intuitive explanation worth preserving |
| `portrait` | Personnage | sourced microhistory/human-scale case |
| `object_focus` | Objet / terrain | material object/site used as explanatory lens |
| `comparator` | Comparaison | bounded alternative mechanism outside the causal spine |
| `callback` | Fil rouge | transformed return to a vertical thread |

Do not create synonyms such as `aside`, `sidebar`, `zoomout`, `character`, `fun_fact` or arbitrary visual labels.

## 3. State machine

`candidate → validated → promoted → retired`

1. **Candidate** — create with `python scripts/new_side_story.py ...`. It can exist before all lineage references are resolved.
2. **Validated** — home arc exists; all claims/sources/bridges/HIL/path references resolve; purpose/off-trunk reason/payoff/placement/return are explicit.
3. **Promoted** — canonical `09_output/report.md` contains `[SIDE-STORY:<id>]` next to a box using the normalized reader label.
4. **Retired** — keep the JSON for history/lineage; remove its reader requirement and, in a deliberate editorial change, its rendered box.

Status changes are code/content changes and go through tests + QA.

## 4. Detection and classification

A side-story candidate exists when material is useful but fails the causal-trunk gate, or when a cross-scale/cross-arc explanation is better handled as a bounded reader excursion.

Typical producers:
- field evidence → `object_focus`, `portrait`, `also` candidate;
- sanitizer → comparator / discarded-lead material that later becomes `comparator` or `false_lead`;
- zoom skill → `dezoom` candidate;
- HIL analysis → `detour`, `also`, `callback` candidate;
- bridge research → resolved contextual mechanism that is useful but not causal-spine material;
- drift audit → `false_lead` or `method` candidate;
- wiki/graph → reusable entity/thread suitable for `portrait`, `object_focus` or `callback`.

No producing skill may mark the item `promoted`. Promotion belongs to composition/editing after evidence is stabilized.

## 5. Required lineage

For `validated` or `promoted`, at least one of these must be populated:
- `lineage.claim_ids`;
- `lineage.source_ids`;
- `lineage.bridge_ids`;
- `lineage.drift_paths`;
- `lineage.origin_paths`.

`hil_ids` gives analytical provenance but does not replace evidence. Cross-arc boxes have one `arc` home and list `related_arcs`.

Never copy a claim into the side-story JSON as a new fact. `content.takeaway` is an editorial summary only.

## 6. Placement contract

Every item records:
- `placement.section_anchor` — stable heading in canonical Markdown;
- `placement.return_to` — claim, arc or stable section anchor that resumes the causal trunk;
- `purpose` — why the reader needs the excursion;
- `reason_off_trunk` — why it is not a causal-spine step/new arc;
- `payoff` — what changes in the reader's interpretation on return.

A side story without a return point is an orphan annex and fails QA.

## 7. Special contract for `dezoom`

`zoom_excursion` is mandatory:
- `from`: motivating scale;
- `to`: highest explanatory scale;
- `return_to`: scale at which the narrative lands again;
- `mechanism`: transmission channel that licenses the scale move;
- `local_payoff`: what the higher-scale explanation clarifies locally.

The three scale fields must be `Z0`–`Z4`. A generic geopolitical paragraph without local payoff is not a dezoom.

## 8. Rendering contract

Canonical marker: `[SIDE-STORY:<id>]`.

Recommended Markdown pattern:

```markdown
<!-- [SIDE-STORY:SS-XXX-001] -->
**Petit détour — Title.** Reader-facing prose...
```

The marker is lineage metadata and should be hidden/ignored by formatted-reader rendering. The visible label comes from the closed kind→label mapping. `required_in_reader=true` makes disappearance a blocking rendering defect.

Storytelling may adjust sentence rhythm or density, but it cannot silently change the kind, lineage, placement, return point, status or reader requirement.

## 9. QA commands

```bash
python -m unittest discover -s tests -v
python scripts/audit_skill.py .
python scripts/audit_workflow.py docs/RUN10_SIDE_STORIES_MANIFEST.json
python scripts/qa_project.py examples/sri_lanka_pre_1948
python scripts/qa_functional_pre1948.py
python scripts/render_full_reader_v3.py --project all
```

`qa_project.py` checks side-story IDs, schema/class/kind/status, lineage references, arc/HIL/zoom vocabulary, placement/return and canonical marker. The renderer repeats the retention gate after composition.

## 10. Adding a new instance

Example:

```bash
python scripts/new_side_story.py \
  --project examples/sri_lanka_pre_1948 \
  --id SS-PRE-005 \
  --kind portrait \
  --arc A06_voc_coastal_state \
  --title "Willem de Melho" \
  --section-anchor "## 3. Les intermédiaires" \
  --return-to C-PRE-002 \
  --purpose "Humanize the intermediary mechanism without turning one life into a population claim" \
  --source-ids SNSL-DEMELHO-2020
```

Then resolve lineage, set `validated`, place the marked box in `report.md`, review semantics, set `promoted`, run the full gates and regenerate readers.

## 11. Adding or changing a subtype

A subtype change is a **contract change**, not normal content editing. It requires, in the same PR:
1. explicit schema-version decision;
2. update to `KINDS` and `RENDER_LABELS` in `scripts/side_story_contract.py`;
3. update to `composing-side-stories`;
4. update to this SOP and `templates/side-story.json` if fields differ;
5. positive and negative tests;
6. review of editor/storytelling rendering semantics;
7. Run manifest + QA evidence.

Do not reuse an old `kind` with a new semantic meaning.

## 12. SOPs / contracts impacted by side stories

- root orchestration and causal gate (`SKILL.md`);
- field capture and sanitization handoff;
- arc / zoom / HIL / bridge / drift handoffs;
- wiki/graph reuse boundaries;
- output editing and reader storytelling;
- `new_project.py` project scaffold;
- `qa_project.py` generic structural QA;
- pre-1948 functional regression runner;
- reader retention/export pipeline;
- workflow manifests and current-skill inventory;
- TDD/feedback/change-management documentation.
