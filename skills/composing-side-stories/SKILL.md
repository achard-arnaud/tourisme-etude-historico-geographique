---
name: composing-side-stories
description: Use when researched material should remain outside the causal trunk but must survive as a traceable detour, dezoom, method note, false lead, portrait, comparator, callback, object focus, or other controlled side story.
---

# Composing side stories

A `side_story` is a **composition artefact**, never a new historical proof. It may only reorganize or expose evidence already represented by claims, sources, bridges, HILs, drift audits, or explicit origin artefacts. Store each record in `09_output/side_stories/<id>.json` using `templates/side-story.json`.

## Closed nomenclature v1
- `detour` → **Petit détour**: useful lateral mechanism or context.
- `dezoom` → **Dézoom**: explicit scale excursion that must return to the motivating place/problem.
- `also` → **Mais aussi**: secondary evidence that enriches the home case.
- `method` → **Point de méthode**: epistemic or source-handling clarification.
- `false_lead` → **Fausse piste**: an intuitive but rejected interpretation worth preserving.
- `portrait` → **Personnage**: sourced human-scale microhistory.
- `object_focus` → **Objet / terrain**: material object/site as an explanatory lens.
- `comparator` → **Comparaison**: bounded alternative mechanism kept outside the main causal spine.
- `callback` → **Fil rouge**: return to a previously introduced vertical thread showing transformation.

Do not invent new labels ad hoc. A new subtype requires a schema-version decision, render label, tests and SOP update.

## Lineage contract
Every validated/promoted record has a home `arc`, stable `id`, `kind`, status, purpose, reason it stays off-trunk, payoff, reader presets, placement, return point and lineage arrays for claims, sources, bridges, HILs, drift paths and origin paths. At least one lineage path must be non-empty. The side story does not duplicate the underlying claim text.

`dezoom` additionally requires `from`, `to`, `return_to`, a transmission mechanism and a local payoff. A Z3/Z4 excursion that does not explain the Z0/Z1 trigger is not a valid dezoom.

## Lifecycle
`candidate → validated → promoted → retired`.

- **candidate**: created with `scripts/new_side_story.py`; may still lack resolved evidence.
- **validated**: lineage references resolve and the editorial purpose is explicit.
- **promoted**: canonical Markdown contains its stable marker and final normalized label.
- **retired**: kept for lineage/history but not required in new readers.

Never promote directly from a raw prompt or field note. First sanitize/source the historical content, then compose it.

## Placement and return
A side story must name the canonical section where it belongs and where the reader returns to the trunk. It may not become an orphan annex. Cross-arc material keeps one home arc and lists other related arcs.

## Rendering and QA
The canonical hidden marker is `[SIDE-STORY:<id>]`. `scripts/qa_project.py` validates structure and lineage; `render_full_reader_v3.py` must fail if a promoted `required_in_reader` item disappears. Storytelling may tune prose around the box but cannot change its kind, lineage, return point or required status without updating the artefact.

Use `docs/SOP_SIDE_STORIES.md` for the operational procedure and subtype-change rules.

## Output
One versioned JSON record per side story under `09_output/side_stories/`, plus the corresponding normalized in-flow box in canonical Markdown.

See also: `SKILL.md` orchestration composition step; `docs/skill_workflow_index.md`.
