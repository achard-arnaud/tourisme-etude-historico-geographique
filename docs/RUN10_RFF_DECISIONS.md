# Run 10/11 — Request-for-feedback decisions

Accepted 2026-08-20:
1. Side-story 9-kind nomenclature accepted.
2. Lineage markers stay in canonical Markdown and are hidden from Word/PDF reader-facing content.
3. `required_in_reader` remains explicit per side story.
4. Structured side-story content must support deterministic insertion rather than permanent hand-maintained duplication.

Blocking audit feedback incorporated in Run11:
- canonical path resolved by output state, not `report.md`;
- legacy coverage measured and backfilled with `tracked/untracked`;
- `method` has no fake return target;
- section/return anchors resolve mechanically;
- marker/label check is block-scoped;
- HIL-07/HIL-08 ownership is explicit;
- `retired` cannot remain in canonical state;
- brittle lexical tests replaced by behavioral contracts;
- workflow/context audits use `--latest` and routed context budget.
