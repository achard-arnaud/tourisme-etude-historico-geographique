# Current output status

Checkpoint date: **2026-08-18 — Run 7 V3 intégrale**.

## Research and conversation layers

**Current with explicit gaps.** Run 5 research remains active. Run 7 additionally materializes the eleven recovered Sri Lanka conversation fiches plus four routing fiches for field culture/epigraphy, itinerary, translation and operational context. Coverage and non-promoted items are tracked in `examples/sri_lanka_pre_1948/00_method/conversation_capitalization_register.md`.

The original photos for panels 3, 7 and 9 and one shared-link TODO are not available in the repository; they remain open rather than being reconstructed.

## Canonical manuscript layer

The small `report.md` files are Run 5 deltas, not complete manuscripts. The complete V3 manuscripts are:

- `examples/sri_lanka_pre_1948/09_output/report_v3_full.md`;
- `examples/sri_lanka_post_1948/09_output/report_v3_full.md`.

The archived V1 DOCX and `report_v1_full.md` files are the non-destructive baselines.

## Reader-export layer

**Current.** Run 7 produces:

- origins–1948 V3: **21 236 DOCX words / 68 PDF pages**;
- 1948–2026 V3: **8 624 DOCX words / 29 PDF pages**.

Both are built with `python scripts/render_full_reader_v3.py`. The advanced reader contracts are unconstrained; the build enforces retention against V1 and treats Run 5 content as chronological deltas. Root-cause analysis and QA are documented in `docs/RUN7_V3_FULL_CONSOLIDATION.md`.

## Validation checkpoint

- retention metrics generated in `docs/RUN7_V3_RETENTION_METRICS.json`;
- DOCX → PDF → PNG rendering completed for all 97 pages;
- representative covers, method pages, insertion pages, source apparatus and final pages visually inspected;
- unit, skill, workflow and project audits must be green before merge.

## Current decision point

The next research pass should resolve the missing panel images/shared-link TODO or one of the explicitly listed social/economic evidence gaps. Any shorter edition must be a separately labelled derivative and may not replace the V3 full manuscripts.
