---
name: composing-side-stories
description: Use when researched material should remain outside the causal trunk but survive as a traceable detour, dezoom, method note, false lead, portrait, comparator, callback, object focus, or semi-analytical focus.
---

# Composing side stories

`side_story` is a composition artefact, never new proof. Current schema is `1.2`; the validator remains backward-compatible with `1.1`. Store records under `09_output/side_stories/`.

Closed kinds: `detour`→Petit détour, `dezoom`→Dézoom, `also`→Mais aussi, `method`→Point de méthode, `false_lead`→Fausse piste, `portrait`→Personnage, `object_focus`→Objet / terrain, `comparator`→Comparaison, `callback`→Fil rouge, `analytical_focus`→Focus analytique.

## Core contract
Validated/promoted narrative items have stable ID, home arc, purpose/payoff, `map_eligible`, lineage to existing claims/sources/bridges/HIL/drifts/origins, resolvable `section_anchor` and resolvable `return_to`. `method` is the exception: a self-contained epistemic box uses `return_to: null` rather than a compliance fiction. A `dezoom` additionally records scale from/to/return, transmission mechanism and local payoff.

## `analytical_focus` — long semi-analytical side story
Use when a site/object opens a question too complex for an anecdotal box but too narrow to justify a new chronological arc. It is a **one_or_two_pager** composition with a structured source in JSON, not a prose free-for-all.

Required: `analysis.core_question`, thesis, at least two contrasted positions with caveats, causal mechanisms with explicit evidence status, at least one callback, a takeaway, and the historical-focus visual contract. Optional resource/fiscal and transregional sections become required in practice when they materially change the explanation. `map_eligible` must still be decided explicitly.

The visual grammar is harvested/adapted from **two-pager-nice**: A4 landscape, dense but readable cards, hero question, contrast cards, dark mechanism band, bottom callback strip, diagrams before weak prose, tables ≤5 columns, and semantic proof coding (verified/inference/unknown). Presentation never upgrades evidence.

## Lifecycle and canonical state
`candidate → validated → promoted → retired`. Resolve canonical Markdown only through `00_method/output_state.json`. `promoted` means its hidden marker and normalized label exist in that canonical state. A `retired` marker remaining there is an error. A field-research analytical focus may remain `candidate` while its home arc or claim-level lineage is not yet materialized; this is honest debt, not a reason to invent IDs.

Legacy prose is inventoried. QA publishes `tracked/discovered/untracked`; complete-coverage corpora fail if `untracked > 0`.

## Deterministic materialization
For normal new/promoted artefacts, `content.body_markdown` is the structured source. For `analytical_focus`, `analysis` + `visual` + `content.takeaway` are the structured source and `materialize_side_stories.py` deterministically renders the canonical Markdown when `body_markdown` is empty. Hidden `[SIDE-STORY:<id>]` lineage remains metadata, not reader-facing prose.

## Reader/map policy
Reader eligibility/order comes from the resolved `reader_profile`, never ad-hoc storytelling. `required_in_reader` remains explicit. `map_eligible=true` only authorizes the separate map-asset search/vision/human-approval lifecycle.

See `docs/SOP_SIDE_STORIES.md`.
