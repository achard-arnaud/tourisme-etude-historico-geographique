# Intake archive and lineage

This directory stores user-supplied analytical inputs, field-intake bundles and snapshot intakes **verbatim before transformation**.

## Contract

1. Archive the original input under `docs/intakes/` before research or claim promotion.
2. Add one record to `docs/intakes/intake_registry.json`.
3. Add one or more research workstreams to `docs/intakes/intake_research_backlog.json` so unresolved questions cannot disappear after capture.
4. The intake is a requirements/research input, **not historical evidence**. It may generate capture fragments, questions, drift audits, source searches, arcs, bridges or composition candidates, but none of its assertions become proof merely because they were supplied by the user.
5. Where an intake contains rival explanations, materialize the discriminating questions/falsifiers before explanatory synthesis.
6. Where the intake proposes new arc IDs, reconcile against the live arc registry first. Existing canonical IDs win; preserve requested IDs only as aliases/notes.
7. Preserve premise corrections and negative results instead of smoothing them into narrative.
8. Add or extend a run-specific acceptance test when the intake creates a new operational contract.
9. Promote feature → `dev` only after CI. Promote to `main` through a temporary release branch so automatic branch deletion cannot remove `dev`.

## Preservation statuses

- `archived`: original input exists verbatim under `docs/intakes/`.
- `missing_source`: a manifest names the original input, but the source file was not retained. Downstream artefacts are not allowed to masquerade as reconstruction of it.
- `unidentified_legacy`: historical processing is documented, but the original input filename/content is not sufficiently identified to recover safely.

## Research-backlog statuses

- `open`: executable research remains.
- `partially_resolved`: a discriminating sub-question has closed, but the wider mechanism or provenance gate remains.
- `blocked`: progress requires unavailable source identity or another hard dependency.
- `pending_external`: a future publication/event is required; `review_by` is mandatory.
- `resolved`: the workstream is closed and must carry a resolution.
- `abandoned`: a gate/falsifier made the workstream no longer meaningful and a resolution is required.

Every registered intake must have at least one backlog workstream. Each workstream has a priority, explicit blocks and a next action. The audit treats missing research lineage as a contract failure even when the original intake itself is safely archived.

## Current provenance debt

The registry records three named historical intake files that were transformed in Run15–Run17 but are absent from the repo, plus one Run13 bundle whose original attachment identity is not preserved. This is explicit debt, not a reason to synthesize replacement files from downstream outputs.

## Run20 targeted re-research

The first cross-intake research pass deliberately reopened only questions that materially block an arc or correct persisted state. It:

- corrected the Kandy 2024 lifetime-migration metric against the final DCS census report;
- closed the narrow existence-of-plastic-enforcement question while keeping compliance/ecological effect open;
- narrowed the Wilpattu/Yala 1938 designation question without pretending to have recovered the original Gazette facsimile;
- located an archival mirror of the 2005 P-TOMS judgment but kept the official-primary provenance gate open;
- narrowed the Mihintale early-Brahmi chronology while refusing to convert epigraphic monastic evidence into proof of the full Mahinda narrative.

Run:

```bash
python scripts/audit_intake_lineage.py
```

The audit cross-checks manifest references, archived files, registry entries, declared downstream outputs, research-workstream coverage, priorities and pending-external review dates.

## Run22 admission of the video-leads intake

The former Run20 video-leads PR was admitted after Run21. Four typed degraded ledgers preserve the failed acquisition outcome; the proposition register is intentionally empty because no timestamped transcript was available. Research themes remain in the backlog, while claims and graph links remain blocked until evidence-bounded propositions and independent historical sourcing exist.

## Run23 — Ehelepola Wax Museum

`INTAKE_ehelepola_wax_museum_kandy_personages.md` preserves the supplied sitemap, caps the museum at T3/`lead`, records rejected characters and routes only independently corroborated Kandy mechanisms into claims, bridges and candidate side stories.
