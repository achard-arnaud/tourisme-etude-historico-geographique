# RUN55 — V4 visual reader QA and export closure

## Scope

Visual and publication pass over the RUN54 materialized reader. No historical
claim, confidence level, source register, intake status or narrative mechanism
was changed.

Primary targets: Chapters 1–3 and 7, their chapter boundaries, the complete
DOCX/PDF render, and the illustration anchors already selected by the corpus.

## Initial findings

The first V4 export exposed three presentation defects that were invisible in
the Markdown composition checks:

1. nine legacy one-cell callouts were stored as raw HTML tables and rendered as
   visible `<table>`, `<thead>`, `<tbody>` and `<colgroup>` tags;
2. illustration markers appeared as backstage identifiers, even though the
   associated field-photo binaries remain external to the repository;
3. the table of contents overflowed by one line onto an almost empty page and
   repeated `PARTIE I` immediately before a forced chapter page break.

## Corrections

- Added `scripts/render_storytelling_v4.py`, a deterministic presentation-only
  renderer for `report_v4_full.md`.
- Legacy HTML callouts now render as typed, bordered, pastel reader boxes.
- Markdown pipe tables use fixed page-safe geometry and readable column widths.
- All 13 fenced side stories render as single visual containers.
- Four illustration IDs are suppressed from the reader. The two
  `required_in_reader=true` records retain their already-reviewed human captions
  exactly at the related Gal Vihara and coinage paragraphs; no image is invented
  because both source binaries are `external_only`.
- The table of contents now fits on one page. Repeated body-level `PARTIE` labels
  are omitted because the chapter headings and transversal handoffs already
  carry the reader structure.
- Hyperlinks are rendered as readable clickable labels, not raw Markdown.
- The V4 renderer is now exercised by CI after deterministic materialization.
- `output_state.json` points the reader-facing Markdown/DOCX/PDF fields to V4;
  the V3 canonical composition baseline remains unchanged for pipeline safety.

## Visual review result

Final PDF: 68 US Letter pages.

| Reader section | Pages | Result |
|---|---:|---|
| Cover, reading method and contents | 1–3 | clean; contents fit one page |
| Chapter 1 | 4–10 | clean; callouts and source table readable |
| Chapter 2 | 11–20 | clean; long analytical focus remains legible and bounded |
| Chapter 3 | 21–26 | clean; transition to Chapter 4 stays at the true boundary |
| Chapter 4 | 27–32 | clean; Gal Vihara caption remains beside its object-focus box |
| Chapter 5 | 33–37 | clean; coinage caption remains inside its false-lead box |
| Chapter 6 | 38–43 | clean |
| Chapter 7 | 44–49 | clean; comparison and source tables fit the page |
| Chapters 8–10 | 50–62 | clean; no orphaned transition or broken side-story box |
| Epilogue, sources, legend and traceability appendix | 63–68 | clean |

No clipping, overlap, broken table, missing glyph, malformed header/footer,
visible materialization marker or raw HTML remains. Density is high by design
but readable at print scale and with ordinary tablet/phone PDF zoom. The visual
evidence does not justify destructive compression of Chapters 1–3 or 7.

## Reproducibility and QA

- 217 unit tests: green.
- Skill, workflow, context-budget, intake-lineage and run-specific audits: green.
- Both corpus QA and composition preflights: green, with pre-existing declared
  evidence/provenance warnings only.
- Functional pre-1948 QA: 135 claims, 217 sources, 25 bridges, 64 side stories,
  0 untracked side stories, 3/7 required/registered arc recaps rendered.
- Full composed-reader render and post-render QA: green.
- Storytelling materializer byte hash is stable across consecutive runs.
- DOCX semantic ZIP-part hash is stable across consecutive renders. Binary DOCX
  hashes may differ because ZIP entry timestamps are packaging metadata.
- Final V4 DOCX was rendered to PNG and all 68 pages were visually inspected.

## Remaining bounded limitation

The Gal Vihara and Dharmasokadeva images cannot be embedded from this repository:
their records are approved and reader-eligible, but their binaries are preserved
as external-only user assets. V4 therefore ships a clean caption-only treatment,
which is explicitly permitted by both illustration records. Embedding the actual
photos is a separate asset-recovery action, not a reason to block the reader.
