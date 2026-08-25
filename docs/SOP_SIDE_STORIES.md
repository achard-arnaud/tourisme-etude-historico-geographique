# SOP — Side stories v1.2

## State machine
`candidate → validated → promoted → retired`.

1. **Evidence first.** Sanitize/source underlying material; a side story never creates proof.
2. **Classify** in the closed nomenclature. Use `analytical_focus` only for a semi-analytical site/object focus that needs a long causal comparison but does not deserve its own chronological arc. Use `class=apparatus, scope=book` for front/back-matter method boxes that have no legitimate home arc.
3. **Create.** Normal kinds use `new_side_story.py`; `analytical_focus` starts from `templates/side-stories/analytical-focus.json`; book-level apparatus starts from `templates/apparatus.json`.
4. **Lineage.** Attach claims/sources/bridges/HIL/drift/origin paths. A field note may remain `candidate` with `lineage_quality=field_research` until the home arc/claims exist. A `legacy_fragment` is declaration debt, not evidence lineage.
5. **Analytical-focus contract.** Require question + thesis + ≥2 contrast cards with caveats + mechanisms with evidence status + callback(s) + takeaway + `one_or_two_pager` visual spec. Add fiscal/resources and transregional influence only where they change the causal interpretation.
6. **Visual grammar.** Harvest/adapt **two-pager-nice** rather than clone it: A4 landscape, 11 pt preferred/9 pt floor, white cards, dark mechanism band, bottom callback strip, diagrams over weak prose, tables ≤5 columns. Green/orange/red encode verified/inference/unknown and are not decoration.
7. **Placement.** Resolve `section_anchor` against canonical Markdown from `00_method/output_state.json`. Narrative kinds require a resolvable return target. `method` and book-level `apparatus` keep `return_to: null`; apparatus has no `arc`.
8. **Validate.** `qa_project.py` checks schema, lineage, anchors, return, map flag, analytical-focus structure, retired state and coverage. `legacy_fragment` may never be `promoted`.
9. **Materialize.** `materialize_side_stories.py` consumes the structured source. Normal kinds use `content.body_markdown`; `analytical_focus` can render from `analysis` when body markdown is empty. Any promoted record requires a substantive `takeaway`; a title echo is rejected. `materialization_mode=existing_fragment` is only for already-rendered legacy prose whose canonical anchor is verified.
10. **Promote** only when claim/source lineage and placement are stable. Existing manuscript fragments must first lose `lineage_quality=legacy_fragment`; new material normally carries its marker, while a bounded existing fragment may use the explicit existing-fragment mode.
11. **Reader plan.** `tailoring-reader-profiles` determines eligibility/order; storytelling can simplify wording but cannot reclassify proof or drop required analytical invariants.
12. **Map handoff.** `map_eligible=true` means map curation may start; it does not imply a map exists. Internet candidate → vision review → human approval → historical date/language/fragment → optional reader use.
13. **Retire** by changing state and removing the marker from canonical output.

## Coverage semantics
Coverage has four distinct figures and they must never be recombined into a generic “tracked” number:
- `traced`: discovered manuscript fragment with at least one claim or source lineage entry;
- `declared`: discovered fragment represented by a record but still without claim/source lineage;
- `discovered`: manuscript fragments found by the detector;
- `untracked`: discovered fragments with no corresponding record.

`untracked == 0` is the completeness gate. `declared` is explicit evidence debt and remains visible even when QA is green.

## Legacy retention
`required_in_reader=true` is not evidence. A record with no `claim_ids` and no `source_ids` is rejected unless it is explicitly `lineage_quality=legacy_fragment` and carries a non-empty `legacy_retention_reason`. QA counts these exemptions. They are temporary editorial-retention debt, not corroboration.

## Arc evidence states
A legacy arc shell declares `evidence_status: shell`; it is structure only and is excluded from recap-ready coverage. A bounded vertical slice may declare `evidence_status: partial`; its fully lineaged records can be promoted independently, but the arc itself is not treated as fully researched or recap-ready.

## Schema change
A new class/kind/field semantic requires schema version or explicit compatible contract, validator, CLI/template where relevant, tests, SOP and renderer/reader-plan impact together.
