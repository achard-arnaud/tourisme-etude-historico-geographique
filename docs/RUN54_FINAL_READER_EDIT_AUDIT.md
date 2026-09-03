# RUN54 — Final reader editorial audit

## Scope

Reader-facing pass only. No new historical claim, no confidence change, no source-register change, no intake promotion.

## Critical finding

RUN53 inserted the two transversal handoffs by anchoring them to `PARTIE II` and `PARTIE IV`. Those labels occur first in the table of contents, so the materializer placed narrative prose inside the sommaire instead of at the actual chapter boundaries.

This is a composition bug, not an evidence bug.

## Correction

- `TRANSITION_CH3_CH4` now anchors directly before the real Chapter 4 heading.
- `TRANSITION_CH7_CH8` now anchors directly before the real Chapter 8 heading.
- A hard guard resolves the table-of-contents range and fails materialization if any `RUN53:TRANSITION-` marker appears there.
- Unit coverage verifies both transitions render exactly once and before their target chapter headings.

## Editorial judgement after transversal reread

### Keep

- Problem-first Chapter 4/5/6/8/9/10 rewrites.
- Typed side stories when they create a genuine change of scale, object focus, false lead or portrait.
- The causal progression: ecology/water -> territorial optimum -> coordination cost -> mobile sovereignty -> nodal maritime rents -> colonial coastal control -> documentary state -> infrastructure-led inversion of mountain value.
- Technical arc recaps in a traceability appendix rather than in the reader flow.

### Do not compress automatically

The remaining density is uneven, especially in Chapters 1-3 and 7, but a destructive global shortening pass is not justified without visual review of the generated PDF/DOCX. Repeated source/guardrail apparatus may be visually acceptable if styling differentiates it from narrative prose. Therefore RUN54 does not delete source lists, confidence labels, methodological boxes or chapter-level guardrails by regex.

### Next visual QA target

Review the generated V4 PDF/DOCX for:

1. page density and long uninterrupted prose blocks;
2. orphan headings and page breaks;
3. side-story spacing and frequency;
4. whether chapter-level source/guardrail apparatus should remain inline or move to endnotes/appendix;
5. illustration proximity to the paragraph that interprets it;
6. table readability on phone/tablet and print.

## Acceptance

RUN54 is accepted when CI passes the full corpus/composition pipeline and the materialized reader contains no narrative handoff inside the sommaire.

The requested visual closure was completed in
`RUN55_V4_VISUAL_READER_QA.md`: the V4 DOCX/PDF exports are now materialized,
rendered and visually checked across all 68 pages.
