# Intake archive and lineage

This directory stores user-supplied analytical inputs, field-intake bundles and snapshot intakes **verbatim before transformation**.

## Contract

1. Archive the original input under `docs/intakes/` before research or claim promotion.
2. Add one record to `docs/intakes/intake_registry.json`.
3. The intake is a requirements/research input, **not historical evidence**. It may generate capture fragments, questions, drift audits, source searches, arcs, bridges or composition candidates, but none of its assertions become proof merely because they were supplied by the user.
4. Where an intake contains rival explanations, materialize the discriminating questions/falsifiers before explanatory synthesis.
5. Where the intake proposes new arc IDs, reconcile against the live arc registry first. Existing canonical IDs win; preserve requested IDs only as aliases/notes.
6. Preserve premise corrections and negative results instead of smoothing them into narrative.
7. Add or extend a run-specific acceptance test when the intake creates a new operational contract.
8. Promote feature → `dev` only after CI. Promote to `main` through a temporary release branch so automatic branch deletion cannot remove `dev`.

## Preservation statuses

- `archived`: original input exists verbatim under `docs/intakes/`.
- `missing_source`: a manifest names the original input, but the source file was not retained. Downstream artefacts are not allowed to masquerade as reconstruction of it.
- `unidentified_legacy`: historical processing is documented, but the original input filename/content is not sufficiently identified to recover safely.

## Current provenance debt

The registry records three named historical intake files that were transformed in Run15–Run17 but are absent from the repo, plus one Run13 bundle whose original attachment identity is not preserved. This is explicit debt, not a reason to synthesize replacement files from downstream outputs.

Run:

```bash
python scripts/audit_intake_lineage.py
```

The audit cross-checks manifest references, archived files, registry entries and declared downstream outputs.
