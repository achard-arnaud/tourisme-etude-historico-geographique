# Run 27 final — semantic generation request

## Goal

Produce the two final **from-scratch** reader manuscripts from the Run27 packet sets, then close them with the deterministic review, coverage, return-target and render contracts. The previous reader prose is comparison material only after generation; it is never drafting input.

## Corpora

1. `examples/sri_lanka_pre_1948` — consume `09_output/from_scratch/run27_packets/` arc by arc.
2. `examples/sri_lanka_post_1948` — consume `09_output/from_scratch/run27_packets/` arc by arc.

The authoritative dynamic counts are currently 84 eligible pre-1948 claims and 98 post-1948 claims; the final preparation step regenerates these counts from the branch state.

## Writing loop — mandatory per narrative unit

1. Hydrate one arc packet plus only the adjacent structured bridge endpoints needed for continuity.
2. Draft from structured evidence; never open `report*.md`, previous DOCX/PDF or `09_output/archive/` as drafting input.
3. Keep hidden `[claim:<id>]` markers on direct evidentiary insertions.
4. HIL selection is relevance-only: normally one dimension, exceptionally two; three or more requires explicit justification/rewrite.
5. Initialize `checklist_reviewed=false`, `sarah_style_reviewed=false`, `hil_scope_reviewed=false` for every new/re-written paragraph.
6. Run the mechanical checklist, independent Sarah-style review and HIL-scope review. Each flag becomes true only after its own review.
7. On failure use `paragraph_repair_loop.py`: at most three attempts. After three failures use explicit `not_selected_for_reader` with rationale; never silently omit the unit.
8. Use side stories only when they add an angle distinct from the trunk. Preserve explicit BEGIN/END fences and the kind-specific palette contract.

## Return-target rule

For every required side-story `return_to`:

- resolve an ID first through `[claim:ID]`, `[bridge:ID]` or `[arc:ID]` in the canonical paragraph;
- if the marker is absent, mark `needs_research` and research the **historical proposition**, not the ID;
- research must actively test the proposition: support it, qualify it, challenge it or redirect it;
- closure requires **sufficient evidence**, not a mechanical source count: for an interpretive/general proposition the default is at least two independent qualified source families; a narrow proposition may also close from one directly probative authoritative source only when the research record explicitly marks `directly_closes_proposition=true` and `scope_fit=direct`;
- if supported, bind the reviewed research record to an appropriate canonical paragraph and materialise the hidden marker;
- if challenged or materially qualified, rewrite/reroute/retire the side story rather than manufacturing the requested marker against the evidence.

Persist decisions under `08_questions/return_target_research*.json`. The renderer itself never browses.

## Required outputs

Pre-1948 under `examples/sri_lanka_pre_1948/09_output/from_scratch/`:
- `Sri_Lanka_pre_1948_run27_from_scratch.md`
- `review_ledger_run27_pre.json`
- `run27_report_pre.json`
- `run27_coverage_pre.json`
- `Sri_Lanka_pre_1948_run27_from_scratch.docx`

Post-1948 under `examples/sri_lanka_post_1948/09_output/from_scratch/`:
- `Sri_Lanka_post_1948_run27_from_scratch.md`
- `review_ledger_run27_post.json`
- `run27_report_post.json`
- `run27_coverage_post.json`
- `Sri_Lanka_post_1948_run27_from_scratch.docx`

## Closure commands

After semantic drafting/review:

```bash
python scripts/close_run27_final.py --project all
```

This command blocks unless:
- both review ledgers are complete;
- every required return target resolves after any persisted research fallback;
- every eligible claim/promoted fragment has an allowed disposition;
- `coverage_completeness.unaccounted == []` in both corpora;
- fresh Run27 DOCX rendering succeeds.

Then compare Run25 iterative vs Run27 from-scratch **claim by claim**, including paragraph IDs and apportioned word depth. A residual length gap is acceptable only when fully explained by explicit dispositions or documented unpromoted corpus debt. Do not promote Run27 as new canon before that comparison closes.

## Non-negotiable epistemic constraints

- Do not fake `human_review` for illustrations. Pending assets remain non-renderable.
- Do not promote the uncertain Kusa Jātaka panel identification without the missing primary piece.
- `canonical_points` remains warning-only until genuinely populated; do not synthesize fake canonical points to make the gate green.
- No production language (run/version/HIL/lineage/baseline) in reader-facing prose.
