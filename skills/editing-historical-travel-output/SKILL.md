---
name: editing-historical-travel-output
description: Use when a researched travel-history corpus must become a chronological readable manuscript while preserving output state, composition lineage, and causal integrity.
---

# Editing historical travel output

Editing owns structure, not evidence or audience selection.

## Mandatory pre-edit gate
Before any editing run execute `scripts/qa_composition_pipeline.py <project>`. It blocks editing if graph-light edge endpoints are unresolved, canonical state cannot be resolved, side-story coverage/anchors fail, required arc recaps are missing or cannot resolve their end-of-arc anchor, reader profile is invalid, or map lifecycle is inconsistent. A prose pass must never repair graph identifiers implicitly.

## Inputs
Resolve canonical/baseline/delta through `00_method/output_state.json`. Consume validated/promoted `side_story` and `arc_recap` artefacts plus the deterministic reader plan. Materialize structured composition with `materialize_side_stories.py` and `materialize_arc_recaps.py`; do not hand-copy a second divergent box.

Keep chronology as spine. Side stories remain in-flow. At every materialized arc close, the recap is inserted immediately before its declared next-arc anchor: principal drivers/amplifiers/constraints/consequences, protagonist objectives/options, what changed, then 2–4 `prepares_next` bullets.

## Promotion
States are explicit: baseline → vnext → canonical/promoted → reader export. The editor may move or rephrase a box only by updating its structured placement/content contract. Hidden lineage markers remain in Markdown and are stripped/hidden in formatted readers.

Output is the state-resolved canonical Markdown handed to `storytelling-historical-travel`.
