---
name: storytelling-historical-travel
description: Use when validated historical evidence must become a reader-facing narrative without changing evidence, composition or uncertainty contracts.
---

# Storytelling historical travel

This file is an **orchestrator**, not a prose prompt. Detailed rules live in versioned references and executable scripts. If prose here conflicts with a script/schema/test, the executable contract wins until the inconsistency is resolved.

## Part 0 — Sarah voice constitution is outside runtime

Sarah's voice is a **design-time artefact**, not a runtime search task. The only runtime source of truth is:

`references/sarah_voice_markers.md`

Generation and paragraph review must never recollect, infer, expand or “improve” Sarah's voice from conversation context, memories, LinkedIn conventions or adjacent skills. A voice revision requires an explicit Part 0 exercise, a new contract version and a new hash.

The intended primary source for a future Part 0 revision is an exported memory from the other assistant Sarah uses for writing, imported as data. That primary source is currently marked `not_imported` in the frozen contract. Runtime must not pretend it has been read. The current contract is therefore explicitly frozen from the user-provided Run 25 specification and nothing else.

The stop criterion is discriminative, not quantitative: retain only markers that help distinguish Sarah-like prose from generic well-written prose. Do not pad the contract with vague style adjectives.

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

Frontstage voice comes only from `references/sarah_voice_markers.md`. The distinctive priorities are: exact scope before ease, lived opening + callback when field material exists, and methodological rigor compressed into the sentence instead of moved into meta-commentary. Production language — runs, versions, HIL IDs, baseline/delta, lineage or drafting instructions — never appears in reader prose.

### S3 — review paragraph

Call `scripts/paragraph_review_gate.py` using an explicit arc-context record.

Every review starts with:

```json
{"checklist_reviewed":false,"sarah_style_reviewed":false,"hil_scope_reviewed":false}
```

A flag becomes `true` only after its own gate passes. All three must be true before the paragraph can enter the final manuscript. Any rewrite means a fresh all-false state.

The Sarah gate is **independent from generation**. It must record distinct generation/review pass IDs and context IDs, bind the review to the exact paragraph hash, bind it to the exact frozen voice-contract hash, and leave paragraph-specific verdicts per applicable marker. `passed=true` plus a list of marker names is not a valid review.

Executable contracts:
- `references/paragraph_review_checklist.md`;
- `references/sarah_voice_markers.md`;
- `scripts/sarah_voice_contract.py`.

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
- `references/sarah_voice_markers.md` — frozen Sarah voice contract; no runtime recollection.
- `references/narrative_voice_sarah.md` — deprecated compatibility pointer only.
- `templates/storytelling/child_10_plus.md` — child decomposition; complexity is staged, not deleted.

## Stop conditions

Do not export as final if any of these is true:
- a paragraph review state is incomplete;
- Sarah review is stale, self-certified in the generation pass, bound to another paragraph, or bound to another voice-contract hash;
- selected HIL contains a dimension unsupported by a claim used in that paragraph;
- a required side story/recap/illustration is missing;
- a side-story block has no deterministic visual boundary;
- production metadata leaks into reader prose;
- from-scratch packet manifest shows any previous-reader prose read;
- an evidence state is silently upgraded.
