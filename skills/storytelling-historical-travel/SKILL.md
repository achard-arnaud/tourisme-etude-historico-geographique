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
- canonical scaffold / chronological manuscript structure;
- claims and arc contracts under `01_arcs/` as evidence spine, not prose units;
- capture/input fragments as narrative material when lineage permits;
- HIL links under claims/composition records;
- bridges under `06_bridges/` as transition instructions;
- source registers;
- reader profile / reader plan;
- eligible side-story, recap, illustration and map artefacts.

Reader modes: **advanced**, **intermediate**, **child 10+**. For advanced work there is no maximum length; use a **content-preservation gate** and exhaustive dispositions instead of compression by budget.

Reader-facing prose must use normal source references only. Claim IDs, bridge IDs, legacy types, HIL IDs and other production metadata remain hidden backstage.

## State machine

### S0 — choose generation mode

The two modes share the same composition engine. The difference is only the bootstrap state.

`iterative` — **default/main writing mode**: start from the current canonical manuscript/scaffold and its append-only construction journal. Preserve chronology, section placement, existing side stories, density and useful narrative texture; apply bounded additions/rewrites.

`from_scratch` — bootstrap an empty manuscript from the structured topology, but then use the same drafting packets, placement rules, side-story composition and QA. Previous reader prose remains forbidden as generation input for this mode.

Both modes use `scripts/build_drafting_packets.py`. The legacy-fragment overlay is shared by both modes.

### S1 — bounded drafting context

Global pass: scaffold headings, chronology, IDs, topology and counts only.

Draft pass: one chronological section/arc packet + adjacent bridge endpoints + relevant input fragments + paragraph-relevant composition records. Claims define what must remain true and sourced; **fragments/inputs provide the richer material from which prose is written**.

A claim is an evidence skeleton, not a target paragraph. Do not paraphrase claim records one after another to manufacture a chapter.

`legacy_fragment` virtual statements are a finite migration bypass for explicitly allowlisted old, unsourced fragments. They may preserve/reposition old narrative or seed research, but cannot establish a new fact or satisfy a sourcing gate.

HIL is relevance-driven, not quota-driven. Use only dimensions supported by evidence actually used in the paragraph.

### S2 — draft one paragraph or one side story in place

Historical nonfiction invariants:
- source-attested fact/action before mechanism and consequence;
- preserve scope and uncertainty;
- no invented dialogue, thoughts, motives, composite characters, sensory facts or false suspense;
- retain concrete field/input texture when available;
- keep claim/fragment lineage backstage, never in final prose;
- cite simple reader-facing sources, not claim IDs;
- prefer callbacks over repetitive reopening of the same evidence.

Side stories are not a gallery or appendix by default. They must be drafted at the chronological/causal point where the excursion pays off, then return explicitly to the trunk. Their length is determined by explanatory value, not by a fixed mini-card budget.

Production language — runs, versions, HIL IDs, baseline/delta, lineage, claim IDs, bridge IDs, `legacy_fragment` or drafting instructions — never appears in reader prose.

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

Side-story eligibility and evidence lineage come from artefacts. New materializations use explicit BEGIN/END fences backstage, but the visible reader receives a normal in-flow encadré.

#### Return-target contract

A `return_to` ID is resolved deterministically before any semantic fallback:
1. resolve the side story against the canonical chronological section/scaffold first;
2. use claim/bridge/arc IDs only as backstage lineage aids;
3. if no valid narrative return exists, mark `needs_research` — never append the story to a catch-all gallery just to satisfy coverage;
4. research the historical proposition, not the identifier;
5. closure normally requires two independent qualified source families, or one directly probative authoritative source for a narrow proposition;
6. supported research binds a reviewed paragraph/section anchor;
7. challenged research redirects or retires the side story;
8. a required validated/promoted side story with unresolved return blocks final export.

Executable contract: `scripts/return_target_resolution.py`. Persist research decisions under `08_questions/return_target_research*.json`.

### S5 — illustration pass

Only `reader_eligible` items render. Preserve observation / canonical text / chronicle tradition / interpretation distinctions. A depiction is not evidence of the event depicted.

### S6 — reciprocal reconciliation and exhaustive dispositions

Run `scripts/reciprocal_coverage_check.py` after scaffold and after drafting.

Then run `scripts/evidence_coverage_contract.py`. Coverage is backstage QA, not visible reader apparatus. Produce claim/fragment depth internally:
- paragraph IDs and paragraph count;
- gross word count;
- apportioned word count;
- explicit thin-coverage signal;
- final disposition for every eligible claim, promoted field fragment and allowlisted legacy fragment.

`unaccounted` must be empty before closure. A legacy fragment may close as `preserved_legacy_context` without being upgraded to sourced evidence.

Canonical-point population is audited separately by `scripts/audit_canonical_points.py`; it remains warning-only until genuinely populated, then may be activated with `--strict`.

### S7 — render and final QA

Preserve scaffold chronology, in-flow side-story placement, callbacks, uncertainty semantics, approved illustration/map constraints and simple source references.

The objective is **maximization under quality constraint**, not merely “make gates green”. A shorter manuscript is allowed, but every omitted eligible unit needs an explicit backstage disposition. Quality gates constrain inclusion; they must not reward deletion of difficult material.

Final comparison reports both quality and conservation: eligible units accounted for, thin versus substantial coverage, explicit exclusions, side-story routing and residual loss against the comparison baseline.

## Executable contracts

- `python scripts/build_drafting_packets.py --project <project>`
- `python scripts/build_from_scratch_packets.py --project <project>` — low-level bootstrap only; do not use directly for final drafting
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
- chronological scaffold ordering has been lost;
- a required side-story/recap/illustration is missing or displaced into a catch-all gallery without an explicit editorial reason;
- a required side-story return remains `needs_research`;
- a challenged return was materialized as supported;
- production metadata leaks into reader prose;
- from-scratch inputs include previous reader prose;
- evidence state is silently upgraded;
- a new unsourced fragment entered through the legacy bypass;
- an eligible claim or promoted fragment has no final backstage disposition;
- exhaustive coverage reports non-empty `unaccounted`.
