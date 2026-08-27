---
name: storytelling-historical-travel
description: Use when validated historical evidence must become a reader-facing narrative without changing evidence, composition or uncertainty contracts.
---

# Storytelling historical travel

This file is an **orchestrator**, not a prose prompt. Detailed rules live in versioned references and executable scripts. If prose here conflicts with a script/schema/test, the executable contract wins until the inconsistency is resolved.

## Part 0 — Sarah voice constitution is outside runtime

Sarah's voice is a design-time artefact. Runtime source of truth: `references/sarah_voice_markers.md`. Generation and review must not recollect or invent additional voice rules from conversation context.

## Inputs

Required structured inputs:
- claims and arc contracts under `01_arcs/`;
- HIL links under claims/composition records;
- bridges under `06_bridges/`;
- source registers and referenced fragments;
- reader profile / reader plan;
- eligible side-story, recap, illustration and map artefacts.

Reader modes: **advanced**, **intermediate**, **child 10+**. For advanced work there is no maximum length; use content preservation and exhaustive dispositions instead of compression by budget.

## State machine

### S0 — choose generation mode

`iterative`: start from the current canonical manuscript and apply bounded deltas.

`from_scratch`: run `scripts/build_from_scratch_packets.py`. Previous reader prose is forbidden drafting input and the packet manifest must report `reader_prose_loaded=false`.

### S1 — bounded drafting context

Global pass: IDs, topology and counts only. Draft pass: one arc packet + adjacent bridge endpoints + paragraph-relevant composition records. Never hydrate the full corpus to draft one paragraph.

HIL is relevance-driven, not quota-driven. Use only dimensions supported by evidence actually used in the paragraph.

### S2 — draft one paragraph

Historical nonfiction invariants:
- source-attested fact/action before mechanism and consequence;
- preserve scope and uncertainty;
- no invented dialogue, thoughts, motives, composite characters, sensory facts or false suspense;
- retain concrete field texture when available;
- direct evidentiary insertion keeps hidden `[claim:<id>]` lineage;
- prefer callbacks over repetitive reopening of the same evidence.

Production language — runs, versions, HIL IDs, baseline/delta, lineage or drafting instructions — never appears in reader prose.

### S3 — review **and repair**, never silently delete

Call `scripts/paragraph_review_gate.py`. Each review starts with all review flags false; a rewrite invalidates previous review state.

On failure, use `scripts/paragraph_repair_loop.py`:
1. draft/rewrite;
2. run all review gates;
3. feed only typed violations back to the next rewrite;
4. reset review state;
5. stop after three attempts.

Final disposition is exactly one of:
- `included`;
- `included_as_side_story` with a side-story ID;
- `not_selected_for_reader` with an explicit rationale.

A gate failure must never become an invisible omission.

### S4 — compose side stories, callbacks and return targets

Side-story eligibility and evidence lineage come from artefacts. New materializations use explicit BEGIN/END fences.

#### Return-target contract

A `return_to` ID is resolved deterministically before any semantic fallback:
1. look for `[claim:<id>]`, `[bridge:<id>]` or `[arc:<id>]` in canonical Markdown;
2. if present, resolve there;
3. if absent, mark `needs_research` — never fuzzy-match an ID against prose;
4. research the historical proposition, not the identifier;
5. closure normally requires two independent qualified source families, or one directly probative authoritative source for a narrow proposition;
6. supported research binds a reviewed paragraph anchor and materializes the hidden marker;
7. challenged research redirects or retires the side story; it never manufactures the requested marker;
8. a required validated/promoted side story with unresolved return blocks final export.

Executable contract: `scripts/return_target_resolution.py`. Persist research decisions under `08_questions/return_target_research*.json`.

### S5 — illustration pass

Only `reader_eligible` items render. Preserve observation / canonical text / chronicle tradition / interpretation distinctions. A depiction is not evidence of the event depicted.

### S6 — reciprocal reconciliation and exhaustive dispositions

Run `scripts/reciprocal_coverage_check.py` after scaffold and after drafting.

Then run `scripts/evidence_coverage_contract.py`. Aggregate coverage such as “all claims cited once” is insufficient. Produce claim-by-claim depth:
- paragraph IDs and paragraph count;
- gross word count;
- apportioned word count;
- explicit thin-coverage signal;
- final disposition for every eligible claim and promoted field fragment.

`unaccounted` must be empty before closure. Canonical-point population is audited separately by `scripts/audit_canonical_points.py`; it remains warning-only until genuinely populated, then may be activated with `--strict`.

### S7 — render and final QA

Preserve hidden lineage, deterministic side-story boundaries, chronology, callbacks, uncertainty semantics and approved illustration/map constraints.

The objective is **maximization under quality constraint**, not merely “make gates green”. A shorter manuscript is allowed, but every omitted eligible unit needs an explicit disposition. Quality gates constrain inclusion; they must not reward deletion of difficult material.

Final comparison reports both quality and conservation: eligible units accounted for, thin versus substantial coverage, explicit exclusions, side-story routing and residual loss against the comparison baseline.

## Executable contracts

- `python scripts/build_from_scratch_packets.py --project <project>`
- `python scripts/paragraph_review_gate.py ...`
- `scripts/paragraph_repair_loop.py`
- `scripts/return_target_resolution.py`
- `python scripts/materialize_side_stories.py ...`
- `python scripts/reciprocal_coverage_check.py ...`
- `python scripts/evidence_coverage_contract.py --project ... --manuscript ... --run-report ... --output ...`
- `python scripts/audit_canonical_points.py`
- `python scripts/qa_composition_pipeline.py <project>`

## Stop conditions

Do not export final if:
- paragraph review is incomplete or stale;
- a required side-story/recap/illustration is missing;
- a required side-story return remains `needs_research`;
- a challenged return was materialized as supported;
- production metadata leaks into reader prose;
- from-scratch inputs include previous reader prose;
- evidence state is silently upgraded;
- an eligible claim or promoted fragment has no final disposition;
- exhaustive coverage reports non-empty `unaccounted`.
