---
name: storytelling-historical-travel
description: Use when a validated historical manuscript must be rendered for a specific reader profile, reading context, language, depth, tone, or register without changing evidence or composition contracts.
---

# Storytelling historical travel

## Reader plan first
Consume the deterministic `09_output/reader_plan.json` resolved by `tailoring-reader-profiles`; do not choose side-story eligibility ad hoc. The profile carries audience, language, content temperature, story template, side-story priority, recap style and map policy.

Profiles include **advanced / historian enthusiast**, **intermediate / educated generalist**, and **child 10+**. Content temperature is content density/variety, not model sampling temperature. Historian enthusiasts and children may both receive all side-story kinds: historians prioritize causal/method/comparator richness; children prioritize sourced people, objects and anecdotes before the larger causal explanation.

## Length policy
For advanced work there is **no maximum length**. Start from the complete baseline/canonical state, treat later inputs as deltas unless proven complete, and apply a **content-preservation gate** against silent loss. Intermediate/child may be shorter only under their explicit template/profile.

## Historical nonfiction gate
PACE remains useful: Place → source-attested Action → Constraint → Evidence. Never add invented dialogue, thoughts, motives, composite characters, sensory facts or false suspense. Use `but/therefore` causal transitions and maintain a promise and continuity ledger.

## Composition invariants
A side story's kind, lineage, required status and reader eligibility come from artefacts/profile. Arc recaps may be simplified in wording but not causally rewritten. Only `human_approved` map assets are eligible. Select **at most one map per subsection or side-story slot**; map language is document language or English fallback. Hidden side-story/recap identifiers remain traceable in Markdown but must not appear as reader-facing labels in Word/PDF.

## Child 10+
Use `templates/storytelling/child_10_plus.md`: concrete place/object, protagonists and documented action, obstacle/choice, anecdote, simple because→therefore recap, and a factual question/teaser toward the next arc. Do not simplify by falsifying uncertainty or violence.

## QA
Verify chronology, source-attested action, reader plan compliance, side-story retention, recap closure, map limit/approval, and baseline retention before export.
