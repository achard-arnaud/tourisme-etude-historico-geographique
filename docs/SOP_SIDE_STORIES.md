# SOP — Side stories v1.1

## State machine
`candidate → validated → promoted → retired`.

1. **Evidence first.** Sanitize/source the underlying material; a side story never creates proof.
2. **Classify** into the closed 9-kind nomenclature. Set `map_eligible` deliberately.
3. **Create** with `new_side_story.py` or `templates/side-story.json`.
4. **Lineage.** Attach claims/sources/bridges/HIL/drift/origin paths. HIL-07 = regional/global skill; HIL-08 = drift audit.
5. **Placement.** Resolve `section_anchor` against canonical Markdown from `00_method/output_state.json`. Narrative kinds require a resolvable return target. `method` must use `return_to: null` unless it is actually narrative material of another kind.
6. **Validate.** `qa_project.py` checks schema, lineage, anchors, return, map flag, retired state and coverage.
7. **Materialize.** New promoted records use `content.body_markdown` + `materialize_side_stories.py`; marker stays hidden metadata in Markdown.
8. **Promote** only when marker + normalized label exist in the state-resolved canonical manuscript.
9. **Reader plan.** `tailoring-reader-profiles` determines eligibility/order; storytelling cannot override it. `required_in_reader` stays explicit.
10. **Retire** by changing state and removing the marker from canonical output. Retired content is lineage history, not reader inventory.

## Legacy migration
Existing prose boxes are discovered from the real canonical manuscript, not the Run-5 delta. QA publishes `tracked/discovered/untracked`. Legacy candidate records may use `lineage_quality=legacy_fragment` until claims/returns are reconstructed; this is visible debt, not fake completeness.

## Schema change
A new kind/field semantic requires schema version, validator, CLI/template, tests, SOP and renderer/reader-plan impact together.
