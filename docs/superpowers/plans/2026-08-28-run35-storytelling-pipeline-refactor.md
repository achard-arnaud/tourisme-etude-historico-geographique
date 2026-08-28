# Run35 implementation plan

## Task 1 — Canonical resolution tests
Add failing tests using nonstandard `canonical_markdown` and prove iterative bootstrap follows output state while from-scratch does not.

## Task 2 — Iterative bootstrap
Import `canonical_markdown_path`; remove hard-coded `report_v3_full.md` / `report.md` lookup. Keep a narrow compatibility fallback only for fixtures without output state.

## Task 3 — Retention
Resolve `baseline_markdown` through output state; retain a narrow legacy fixture fallback.

## Task 4 — Paragraph review plan
Create `scripts/build_paragraph_review_plan.py`: load canonical reader, promoted side stories and drafting packets; resolve anchors; collect claim/source lineage and claim-linked fragments; emit deterministic JSON and dispositions.

## Task 5 — Side-story readiness
Expose a readiness check reusing narrative-depth validation; required promoted stories must be materializable or valid existing fragments.

## Task 6 — Contract docs
Update storytelling and composing-side-stories skills with the review-plan orchestration surface and Run34 functional baseline invariant.

## Task 7 — Review / verify / release
Full CI, spec review, quality review, feature → dev, dev CI, dev → main, main CI.
