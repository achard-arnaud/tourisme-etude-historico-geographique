---
name: editing-historical-travel-output
description: Use when a researched travel-history corpus must become a chronological readable manuscript while preserving output state, composition lineage, and causal integrity.
---

# Editing historical travel output

Editing owns structure, not evidence or audience selection.

## Mandatory pre-edit gate
Before any editing run execute `scripts/qa_composition_pipeline.py <project>`. It blocks editing if graph-light endpoints are unresolved, canonical state cannot be resolved, side-story coverage/anchors fail, required arc recaps are missing, reader profile is invalid, or map lifecycle is inconsistent. A prose pass never repairs identifiers implicitly.

## Inputs
Resolve canonical/baseline/delta through `00_method/output_state.json`. Consume validated/promoted side stories and arc recaps plus deterministic reader plan. New ordinary side stories use `materialize_side_stories.py`; do not hand-copy a second divergent box.

For `analytical_focus`, the JSON analysis/visual contract is the structured source. Materialize it deterministically; editing may adjust placement only by updating the artefact. Do not manually rewrite its contrast cards, evidence status or callback in a parallel prose copy.

Keep chronology as spine. Side stories remain in-flow. At every materialized arc close, place the `arc_recap`: principal drivers/amplifiers/constraints/consequences, protagonist objectives/options, what changed, then prepares-next bullets.

## Form-global storytelling changes

When the active storytelling contract changes the **shape of narration** rather than the evidence — for example problem-first framing, event-before-consequence ordering, causal dezoom placement or 360 viewpoint handling — iterative editing must not behave as append-only inside the selected scope.

For each impacted arc/chapter span:
- load the complete current prose span;
- freeze factual propositions, uncertainty, citations and required material as the retention baseline;
- mark every paragraph as style/structure-review eligible;
- allow paragraph split, merge, local reorder and transition rewrite inside the same chronological rupture;
- preserve or explicitly disposition every historical unit;
- rerun continuity review across the whole impacted span, including paragraphs whose factual content did not change.

A form-global pass therefore invalidates **paragraph-shape approval**, not evidentiary approval. It must never use the new style contract as a reason to drop sourced matter.

## Promotion
States are explicit: baseline → vnext → canonical/promoted → reader export. Hidden lineage markers remain in Markdown and are stripped/hidden in formatted readers.

Output is the state-resolved canonical Markdown handed to `storytelling-historical-travel`.
