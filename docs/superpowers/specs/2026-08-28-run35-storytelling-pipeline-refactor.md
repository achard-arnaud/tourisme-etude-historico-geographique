# RFC — Run35 storytelling pipeline refactor

## Goal

Make the technical pipeline reproduce the functional behavior validated by Run33/Run34 instead of relying on manual editorial recovery.

## Current source of truth

- Functional reader baseline: Run34 on `main`.
- Reader path contract: `00_method/output_state.json`.
- Evidence control: claims/bridges/source registers.
- Narrative material: capture fragments + qualified archived intakes.
- Composition: promoted side stories + reader scaffold.

## Non-negotiable invariants

1. Run34 content is immutable during this refactor.
2. Claims remain backstage control/evidence contracts, never prose units.
3. Fragments/sources are the primary narrative material.
4. `reader_scaffold` controls chronology and placement; `story_scaffold` does not reorder the book.
5. Iterative and from-scratch modes share the evidence/material engine; only bootstrap differs.
6. Iterative bootstrap must load the canonical reader resolved by `output_state`, never a hard-coded filename.
7. Every promoted required side story resolves to a reader boundary and has sufficient narrative material or an explicit existing-fragment disposition.
8. Frontstage exports contain no claim/bridge/run/machine-HIL metadata.
9. No silent compression of an advanced reader relative to its resolved baseline.

## Proposed change

### A. Canonical-reader resolver
Refactor drafting and retention logic to resolve canonical/baseline Markdown through `output_state`.

### B. Paragraph review work plan
Add a deterministic builder emitting paragraph-level work items with reader anchor, side stories, claim controls, narrative fragments and sources.

### C. Side-story readiness gate
Promoted required stories must be substantial structured narrative material or an explicit resolvable `existing_fragment`.

### D. Retention/frontstage gates
Retention uses the resolved baseline; frontstage remains the final export gate.

## Explicit exclusions

- No rewrite of Run34 historical content.
- No change to evidence confidence/status.
- No new historical research.
- No DOCX visual redesign.

## Acceptance criteria

1. Iterative bootstrap path equals `canonical_markdown_path(project)`.
2. From-scratch still loads no prior reader prose.
3. Paragraph review plan covers every promoted `required_in_reader` side story with an explicit disposition.
4. Review items expose fragments as narrative material and claims as control.
5. Advanced retention compares against `baseline_markdown` from output state.
6. Existing test suite remains green.
7. New tests are observed failing before implementation, then green.
8. Merge feature → dev → main only after full CI.

## Rollback

Revert the Run35 merge; Run34 crystal remains intact in history.
