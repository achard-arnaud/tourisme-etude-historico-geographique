---
name: storytelling-historical-travel
description: Use when validated historical evidence must become a reader-facing narrative without changing evidence, composition or uncertainty contracts.
---

# Storytelling historical travel

This file is an **orchestrator**, not a prose prompt. Detailed rules live in versioned references and executable scripts. If prose here conflicts with a script/schema/test, the executable contract wins until the inconsistency is resolved.

## Inputs

Required structured inputs:
- claims and arc contracts under `01_arcs/`;
- HIL links under claims/composition records;
- bridges under `06_bridges/`;
- source registers and referenced fragments;
- reader profile / reader plan when the mode uses one;
- side-story, recap, illustration and map artefacts when eligible.

Reader modes: **advanced**, **intermediate**, **child 10+**. For advanced work there is **no maximum length**; use a content-preservation gate instead of compression by budget.

## State machine

### S0 — choose generation mode

`iterative`: start from the current canonical manuscript and apply bounded deltas.

`from_scratch`: run `scripts/build_from_scratch_packets.py`. Previous `report*.md`, reader DOCX/PDF, archives and generated reader prose are forbidden drafting inputs. The packet manifest must report `reader_prose_loaded=false`.

### S1 — build bounded drafting context

Global pass: IDs, topology, counts only.

Draft pass: one arc packet + adjacent bridge endpoints + paragraph-relevant composition records. Never hydrate the full corpus to draft one paragraph.

HIL is **relevance-driven, not quota-driven**. A paragraph may use only dimensions linked to claims/composition records actually used in that paragraph. It need not use every potentially relevant dimension.

### S2 — draft one paragraph

Historical nonfiction invariants:
- source-attested fact/action before mechanism and consequence;
- preserve scope and uncertainty;
- no invented dialogue, thoughts, motives, composite characters, sensory facts or false suspense;
- retain concrete input texture when available;
- direct evidentiary insertion keeps hidden `[claim:<id>]` lineage;
- prefer an active callback over reopening the same evidence repeatedly.

Frontstage voice is defined in `references/narrative_voice_sarah.md`. Production language — runs, versions, HIL IDs, baseline/delta, lineage or drafting instructions — never appears in reader prose.

### S3 — review paragraph

Call `scripts/paragraph_review_gate.py` using an explicit arc-context record.

Every review starts with:

```json
{"checklist_reviewed":false,"sarah_style_reviewed":false,"hil_scope_reviewed":false}
```

A flag becomes `true` only after its own gate passes. All three must be true before the paragraph can enter the final manuscript. Any violation means full-paragraph rewrite and a fresh all-false state.

Executable/details: `references/paragraph_review_checklist.md`.

### S4 — compose side stories and recaps

Side-story eligibility, kind and evidence lineage come from artefacts, never from stylistic improvisation. `materialize_side_stories.py` emits explicit BEGIN/END fences for new materializations. Renderers must use those fences to create one visually closed block; do not infer the end from colour or indentation alone.

`analytical_focus` keeps question → thesis → contrasted positions/caveats → mechanisms/evidence status → callback → payoff. A `method` side story explains historical method to the reader; it is not production-method commentary.

False leads: at most 1–2 per subsection, Socratic question + answer in the same block.

### S5 — illustration pass

Use the illustration contract. Only `reader_eligible` items may render. Preserve observation / canonical text / chronicle tradition / interpretation distinctions. Do not turn a field depiction into historical proof. Actual image embedding remains governed by its dedicated pipeline.

### S6 — reciprocal reconciliation

Run `scripts/reciprocal_coverage_check.py` after scaffold and after drafting. More than two direct citations is a callback-review signal. Density is advisory. Legacy uninstrumented prose is unknown coverage, never fabricated as unused.

### S7 — render and final QA

Renderer must preserve:
- hidden lineage without reader-facing production apparatus;
- explicit side-story visual start/end;
- side-story palette + redundant symbol legend;
- chronology, transitions and callback closure;
- source/uncertainty semantics;
- approved illustration/map constraints.

For iterative advanced readers, baseline retention remains a hard content-preservation gate. For from-scratch readers, compare against evidence coverage and review completion, **not lexical similarity to the archived reader**.

## Commands / executable contracts

- `python scripts/build_from_scratch_packets.py --project <project>` — contamination-safe drafting packets.
- `python scripts/paragraph_review_gate.py --paragraph <p> --claim-json <c> --arc-context-json <ctx>` — three-gate paragraph review.
- `python scripts/materialize_side_stories.py ...` — fenced side-story materialization.
- `python scripts/reciprocal_coverage_check.py ...` — claim/fragment/callback diagnostics.
- `python scripts/qa_composition_pipeline.py <project>` — composition preflight.

## References

- `references/paragraph_review_checklist.md` — exact review transitions and fixtures.
- `references/narrative_voice_sarah.md` — voice markers and non-transferable social-format habits.
- `templates/storytelling/child_10_plus.md` — child decomposition; complexity is staged, not deleted.

## Stop conditions

Do not export as final if any of these is true:
- a paragraph review state is incomplete;
- selected HIL contains a dimension unsupported by a claim used in that paragraph;
- a required side story/recap/illustration is missing;
- a side-story block has no deterministic visual boundary;
- production metadata leaks into reader prose;
- from-scratch packet manifest shows any previous-reader prose read;
- an evidence state is silently upgraded.
