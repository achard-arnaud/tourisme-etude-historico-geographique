---
name: storytelling-historical-travel
description: Use when a validated historical manuscript must be rendered for a specific reader profile, reading context, language, depth, tone, register, or approved illustration set without changing evidence or composition contracts.
---

# Storytelling historical travel

## Topology before prose
Consume deterministic `09_output/story_scaffold.json` before `09_output/reader_plan.json`. The scaffold is a compact global projection of arcs, spine claims, bridges, questions and composition queues; it prevents arc-local drafting from silently forgetting material. Do not hydrate the full corpus in one prompt: load the scaffold globally, then only the active arc, its adjacent bridges and its required composition records.

The reader plan carries audience, language, content temperature, story template, side-story priority, recap style, map policy and illustration selection. Do not choose eligibility ad hoc.

Profiles include advanced/historian enthusiast, intermediate/educated generalist and child 10+. Content temperature is density/variety, not model sampling. Historians and children may both receive every side-story kind for different reasons; the profile controls ordering.

## Length policy
For advanced work there is no maximum length. Start from complete baseline/canonical state, treat later inputs as deltas unless proven complete, and apply content-preservation gates. Intermediate/child may be shorter only under explicit profile/template rules.

## Historical nonfiction gate
PACE remains useful: Place → source-attested Action → Constraint → Evidence. Never add **invented dialogue**, thoughts, motives, composite characters, sensory facts or false suspense. Use but/therefore transitions and maintain continuity.

## Composition invariants
A side story's kind, lineage, required status and reader eligibility come from artefacts/profile. `analytical_focus` preserves at minimum its **question → thesis → contrasted positions/caveats → mechanisms/evidence status → callback → payoff**. Storytelling may simplify language or reorder cards for the target reader; it may not flatten the focus into a generic anecdote, turn an inference green, or rewrite a contested binary as fact.

Arc recaps may be simplified in wording but not causally rewritten. Only `human_approved` map assets are eligible, at most one per subsection or side-story slot. Hidden composition IDs remain traceable in Markdown but not reader-facing.

## Dedicated illustration pass
After the narrative has been rendered for the reader profile and **before the final reread**, load `09_output/illustrations/*.json` through the `illustration` contract.

The pass is editorial, not evidentiary:
1. consider only `reader_eligible` illustrations for actual embedding; `vision_validated` records may inform placement/caption planning but remain non-renderable;
2. require at least one resolvable `input_ref`; an illustration must point back to an intake, field fragment, claim, bridge, side story or arc;
3. preserve depiction semantics: `observed_caption`, `canonical_text`, `chronicle_tradition`, `interpretive`;
4. use **depicts / represents / temple tradition presents** rather than **proves**; a field photo never upgrades historical confidence;
5. place an image only where it reduces reader effort, clarifies an object/event, or makes a historiographic distinction visible; do not decorate every subsection;
6. caption in four layers when useful: **what is visible → what episode/theme it represents → why it matters here → epistemic limit**;
7. if the image, its local caption and the manuscript disagree, do not silently harmonize them: retain the manuscript evidence state and flag the mismatch for review;
8. if `source.binary_status=external_only`, keep the illustration trace/caption in the plan but do not pretend the binary is embedded in the repository export.
9. require `placement.target_status=resolved` for selection; a named but absent subsection remains in `illustration_review_queue_ids` and must surface as coverage debt, never as a fabricated location.
10. preserve the hidden `[ILLUSTRATION:<id>]` marker exactly once for every selected illustration so the final render gate can prove coverage.

For Sri Lankan sacred-history scenes, be especially strict about the distinction between a depiction of the Buddha's life and later chronicle traditions that place the Buddha physically in Lanka. The illustration pass must preserve that distinction in captions.

## Final reread
Run the final prose reread **after** illustration placement. Check that image insertion did not break chronology, transitions, paragraph referents, source semantics or the distinction between observation, tradition and historical claim.

## Child 10+
Use `templates/storytelling/child_10_plus.md`. An `analytical_focus` remains eligible, but decompose it around an observable object/place, protagonist/institution, documented action and a simple because→therefore mechanism before the callback. Complexity is staged, not deleted.

Illustrations for children may be selected more frequently when they materially aid comprehension, but captions must still preserve uncertainty and tradition-vs-history semantics.

## QA
Verify scaffold coverage, chronology, source-attested action, reader-plan compliance, side-story retention, analytical-focus evidence semantics, recap closure, map approval/limit, illustration lineage/status/epistemic captioning, final post-illustration continuity and baseline retention before export. The final reconciliation compares every scaffold queue with the rendered output or an explicit deferred/retired decision.
