---
name: storytelling-historical-travel
description: Use when a validated historical manuscript must be rendered for a specific reader profile, reading context, language, depth, tone, or register without changing evidence or composition contracts.
---

# Storytelling historical travel

## Reader plan first
Consume deterministic `09_output/reader_plan.json`; do not choose side-story eligibility ad hoc. The profile carries audience, language, content temperature, story template, side-story priority, recap style and map policy.

Profiles include advanced/historian enthusiast, intermediate/educated generalist and child 10+. Content temperature is density/variety, not model sampling. Historians and children may both receive every side-story kind for different reasons; the profile controls ordering.

## Length policy
For advanced work there is no maximum length. Start from complete baseline/canonical state, treat later inputs as deltas unless proven complete, and apply content-preservation gates. Intermediate/child may be shorter only under explicit profile/template rules.

## Historical nonfiction gate
PACE remains useful: Place → source-attested Action → Constraint → Evidence. Never invent dialogue, thoughts, motives, composite characters, sensory facts or false suspense. Use but/therefore transitions and maintain continuity.

## Composition invariants
A side story's kind, lineage, required status and reader eligibility come from artefacts/profile. `analytical_focus` preserves at minimum its **question → thesis → contrasted positions/caveats → mechanisms/evidence status → callback → payoff**. Storytelling may simplify language or reorder cards for the target reader; it may not flatten the focus into a generic anecdote, turn an inference green, or rewrite a contested binary as fact.

Arc recaps may be simplified in wording but not causally rewritten. Only `human_approved` map assets are eligible, at most one per subsection or side-story slot. Hidden composition IDs remain traceable in Markdown but not reader-facing.

## Child 10+
Use `templates/storytelling/child_10_plus.md`. An `analytical_focus` remains eligible, but decompose it around an observable object/place, protagonist/institution, documented action and a simple because→therefore mechanism before the callback. Complexity is staged, not deleted.

## QA
Verify chronology, source-attested action, reader-plan compliance, side-story retention, analytical-focus evidence semantics, recap closure, map approval/limit and baseline retention before export.
