---
name: composing-side-stories
description: Use when researched material should remain outside the causal trunk but survive as a traceable detour, dezoom, method note, false lead, portrait, comparator, callback, object focus, or other controlled side story.
---

# Composing side stories

`side_story` is a composition artefact, never new proof. Use schema `1.1` and store under `09_output/side_stories/`. Closed kinds: `detour`→Petit détour, `dezoom`→Dézoom, `also`→Mais aussi, `method`→Point de méthode, `false_lead`→Fausse piste, `portrait`→Personnage, `object_focus`→Objet / terrain, `comparator`→Comparaison, `callback`→Fil rouge.

## Contract
Validated/promoted narrative items have stable ID, home arc, purpose/payoff, `map_eligible`, lineage to existing claims/sources/bridges/HIL/drifts/origins, resolvable `section_anchor` and resolvable `return_to`. **`method` is the exception:** an epistemic box may be self-contained and must use `return_to: null` rather than a compliance fiction.

A `dezoom` additionally records `from`, `to`, scale `return_to`, transmission mechanism and local payoff. HIL-07 is owned by `analyzing-regional-global-systems`; HIL-08 by the drift-audit skill.

## Lifecycle and canonical state
`candidate → validated → promoted → retired`. Resolve canonical Markdown only through `00_method/output_state.json`. `promoted` means its hidden marker and normalized label exist in that canonical state. A `retired` marker remaining there is an error.

Legacy prose is explicitly inventoried. QA publishes `tracked/discovered/untracked`; a corpus configured for complete coverage fails if `untracked > 0`. Candidate backfills may preserve legacy fragments until full claim-level lineage is reconstructed; they must not masquerade as promoted records.

## Deterministic materialization
For new/promoted artefacts, `content.body_markdown` is the structured source. `scripts/materialize_side_stories.py` inserts it at its resolved section anchor with `[SIDE-STORY:<id>]`. The marker remains in canonical Markdown but is metadata, not reader-facing prose.

## Reader/map policy
`map_eligible` controls whether map curation may be dispatched. Reader eligibility/order comes from the resolved `reader_profile`, not ad-hoc storytelling choices. `required_in_reader` remains explicit per item.

See `docs/SOP_SIDE_STORIES.md`.
