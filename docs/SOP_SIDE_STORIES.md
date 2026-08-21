# SOP — Side stories v1.2

## State machine
`candidate → validated → promoted → retired`.

1. **Evidence first.** Sanitize/source underlying material; a side story never creates proof.
2. **Classify** in the closed nomenclature. Use `analytical_focus` only for a semi-analytical site/object focus that needs a long causal comparison but does not deserve its own chronological arc.
3. **Create.** Normal kinds use `new_side_story.py`; `analytical_focus` starts from `templates/side-stories/analytical-focus.json` because its structured source cannot be represented honestly by the short CLI alone.
4. **Lineage.** Attach claims/sources/bridges/HIL/drift/origin paths. A field note may remain `candidate` with `lineage_quality=field_research` until the home arc/claims exist.
5. **Analytical-focus contract.** Require question + thesis + ≥2 contrast cards with caveats + mechanisms with evidence status + callback(s) + takeaway + `one_or_two_pager` visual spec. Add fiscal/resources and transregional influence only where they change the causal interpretation.
6. **Visual grammar.** Harvest/adapt **two-pager-nice** rather than clone it: A4 landscape, 11 pt preferred/9 pt floor, white cards, dark mechanism band, bottom callback strip, diagrams over weak prose, tables ≤5 columns. Green/orange/red encode verified/inference/unknown and are not decoration.
7. **Placement.** Resolve `section_anchor` against canonical Markdown from `00_method/output_state.json`. Narrative kinds require a resolvable return target. `method` keeps `return_to: null`.
8. **Validate.** `qa_project.py` checks schema, lineage, anchors, return, map flag, analytical-focus structure, retired state and coverage.
9. **Materialize.** `materialize_side_stories.py` consumes the structured source. Normal kinds use `content.body_markdown`; `analytical_focus` can render from `analysis` when body markdown is empty. Marker stays hidden metadata.
10. **Promote** only when lineage/placement are stable and marker + normalized label exist in the state-resolved canonical manuscript.
11. **Reader plan.** `tailoring-reader-profiles` determines eligibility/order; storytelling can simplify wording but cannot reclassify proof or drop required analytical invariants.
12. **Map handoff.** `map_eligible=true` means map curation may start; it does not imply a map exists. Internet candidate → vision review → human approval → historical date/language/fragment → optional reader use.
13. **Retire** by changing state and removing the marker from canonical output.

## Legacy migration
Existing prose boxes are discovered from the real canonical manuscript, not a delta. QA publishes `tracked/discovered/untracked`. Legacy candidate records may use `lineage_quality=legacy_fragment` until claims/returns are reconstructed.

## Schema change
A new kind/field semantic requires schema version, validator, CLI/template, tests, SOP and renderer/reader-plan impact together.
