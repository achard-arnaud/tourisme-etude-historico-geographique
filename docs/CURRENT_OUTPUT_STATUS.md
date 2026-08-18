# Current output status

Checkpoint date: **2026-08-18 — Run 6**.

## Research layer
**Current.** Run 5 comparative-development research remains the canonical evidence base. Run 6 adds the audited Polonnaruwa conversation-source inventory: **17 recovered source records**, including the correction that UNESCO document `163318` concerns Anuradhapura rather than Polonnaruwa.

The three requested YouTube transcripts and the two external storytelling repositories were used as **method inputs**, not as historical evidence. Their extraction and adoption/rejection decisions are recorded in `docs/RUN6_STORYTELLING_REVIEW.md` and `skills/storytelling-historical-travel/references/storytelling-patterns-and-review.md`.

## Validation checkpoint
Fresh local Run 6 gate:
- **34/34 unit tests GREEN** after one deliberate RED→GREEN wording correction;
- skill audit: GREEN;
- workflow-manifest audit: **16 dispatched / 0 skipped / 16 known skills**;
- pre-1948 QA: **9 claims / 37 sources / 3 wiki pages / 4 graph edges / 0 warnings**;
- post-1948 QA: **30 claims / 48 sources / 7 wiki pages / 10 graph edges / 0 warnings**;
- both DOCX packages and both PDF exports verified.

GitHub CI remains the merge gate; run identifiers are recorded in the final pull requests rather than frozen in this status file.

## Canonical Markdown layer
**Current.** The two canonical reports are:
- `examples/sri_lanka_pre_1948/09_output/report.md`;
- `examples/sri_lanka_post_1948/09_output/report.md`.

Their Run 6 banners point to the source audit, storytelling review and reproducible reader-export script.

## Knowledge layer
**Current and validated.** Wiki entities, graph edges, modular source registers and provenance checks remain active. The conversation inventory is isolated in `source_register_polonnaruwa_conversation.json`, so it can be audited independently without changing claim provenance silently.

## Reader-export layer
**Current.** Run 6 regenerates and packages the two v2 reading editions from the canonical Markdown:
- pre-1948: Word + PDF, 8 rendered pages;
- 1948–2026: Word + PDF, 14 rendered pages.

Each edition follows an explicit reader contract and contains a reading map, continuous page furniture, causal callouts and a linked source appendix. The canonical regeneration command is `python scripts/render_reader_exports.py`.

## Current decision point
The research, Markdown, workflow evidence and reader exports are aligned. The next substantive cycle should begin with a new field question or evidence gap, not with another formatting catch-up pass.
