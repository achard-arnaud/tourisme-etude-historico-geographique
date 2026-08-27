# Legacy fragment bypass

## Decision

Legacy capture fragments created before the claim/source contract are not migrated one by one into persisted claim files.

At drafting time, an unclaimed legacy fragment is exposed as a **virtual statement** with `type=legacy_fragment`.

## Safety contract

A `legacy_fragment`:

- is a preservation/migration device, not an evidentiary upgrade;
- keeps the original fragment id and candidate arc;
- may seed or preserve narrative already present in the canonical iterative reader;
- may be used to formulate a research lead or bounded contextual sentence;
- MUST NOT establish a new factual assertion solely because it was wrapped as a virtual statement;
- MUST NOT satisfy a sourcing gate for an A/B factual or causal claim;
- MUST retain `legacy_unsourced=true` when no registered source is attached;
- disappears from reader-facing prose as a technical type: only normal narrative and simple source references render.

## Scope

This bypass is intentionally limited to legacy capture debt. New inputs must continue through normal fragment -> sourced claim -> composition contracts.

## Rationale

Early project fragments predate the claim contract and often predate systematic source registration. Reconstructing a claim file for every old fragment would create migration work without improving the reader. Treating them as virtual legacy statements preserves narrative richness while preventing silent evidentiary promotion.
