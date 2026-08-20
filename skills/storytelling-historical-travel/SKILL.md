---
name: storytelling-historical-travel
description: Use when a researched historical travel corpus must be rendered for a specific reader, reading context, language, desired depth, tone, register, or target length.
---

# Storytelling historical travel

## Reader contract
Resolve or infer and keep stable: **audience** (advanced/intermediate/child), language/translation policy, tone, register, length policy and reading context. For an advanced consolidation, length is unconstrained unless explicitly abridged.

## Audience presets
### advanced
Preserve historiographic disputes, source families, competing causal models, comparator limits, detours, callbacks, promoted side stories and explicit uncertainty. There is **no maximum length**. Start from the last complete promoted baseline, treat later manuscripts as deltas unless proven complete, and block silent loss.

### intermediate
Keep causal architecture but reduce proper-name density. Explain technical terms inline and surface controversies when they change interpretation.

### child
Use concrete places, objects and human-scale stakes. Never invent dialogue, thoughts, motives, dates or events. Mark uncertainty simply.

## Content-preservation gate
For advanced work:
1. inventory baseline sections, tables, side material, side-story IDs, claims, source families and unresolved questions;
2. route every later addition to chronology or an explicit fiche;
3. compare baseline, delta and candidate export quantitatively;
4. fail on silent loss even if shorter prose is smoother.

## Narrative unit
Prefer: place/object/tension → causal question → 2–4 mechanisms → consequences → bridge forward.

For a short sourced vignette use **PACE**: Place → Action → Constraint → Evidence. For a long arc use causal mission → minimum context → mechanism plan → `but/therefore` progression → rupture/resolution → reflection/bridge. One main takeaway per side box.

## Historical non-fiction safety gate
“Show, do not tell” means material evidence, spatial anchoring and **source-attested** action. It never licenses invented dialogue, inner thoughts, motives, composite characters, sensory detail, chronology, danger or cliffhangers. Direct speech/reported thought require a source; uncertain reconstruction is labelled and normally demoted from the trunk.

## Side-story integrity
Storytelling consumes the already composed `side_story`; it does not create a second uncontrolled taxonomy. It may tune the prose inside a box for reader fit, but must not silently change its `kind`, normalized label, lineage, placement, return point, status or `required_in_reader` flag. `portrait` remains bounded to sourced microhistory; `dezoom` must land back at its contracted local payoff; `false_lead` must remain visibly rejected; `callback` must show transformation rather than repetition.

For advanced readers every promoted required side story must survive into the Markdown reader and formatted export. The hidden marker `[SIDE-STORY:<id>]` remains machine-readable in Markdown and may be suppressed visually in DOCX/PDF.

## Vertical threads / comparators
When caste, language, education, water, trade, religion or migration crosses arcs, use callbacks showing transformation. Comparators illuminate mechanisms, not rankings: home case first, alternative mechanism, then major confounder.

## Cross-reference and continuity
Use a cross-reference only when it saves repetition or activates causality. Maintain a **promise and continuity ledger** for long outputs: opening causal promise, questions introduced, callback location, payoff or unresolved status.

## Story QA
Verify chronology, causal transitions, uncertainty, comparator limits, non-fiction safety, promise/callback closure, side-story retention/labels, applicable length policy, baseline retention, reader fit and a conclusion returning to the causal map.

See `references/storytelling-patterns-and-review.md` for benchmark boundaries.

See also: `SKILL.md` orchestration step 12; `composing-side-stories`; `docs/SOP_SIDE_STORIES.md`.
