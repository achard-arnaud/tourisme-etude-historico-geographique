# QA functional baseline — Sri Lanka pre-1948

This fixture is the mechanical reference corpus for end-to-end regression. It is not a claim that every historical topic is complete.

## Stable structural baseline
- 9 materialized typed claims under 3 fixture arcs.
- 3 causal bridges.
- 3 wiki pages.
- 4 graph edges with resolvable graph-light nodes.
- 8 HIL baselines, including explicit non-findings.
- 3 materialized arc recaps.
- state-resolved canonical reader and deterministic composition preflight.

## Source baseline evolution
Run 9 established **37** registered sources. Run 12 deliberately extends the same fixture with **7** Jetavana/Saṅgha anchors, so current expected count is **44**. The count is a regression fixture, not a target quota.

## Side-story baseline evolution
Run 11 established 25 pre-1948 side-story records with zero untracked legacy boxes. Run 12 adds `SS-PRE-JETAVANA-001`, a schema-1.2 `analytical_focus` field-research candidate. Current minimum inventory is **26**; legacy coverage must remain 0 untracked.

The Jetavana record remains candidate until the Anuradhapura home arc and claim-level lineage are materialized. QA must not convert absence of an arc into invented IDs merely to promote it.

## Mandatory regression command
```bash
python scripts/qa_functional_pre1948.py
```

It must transitively pass skill/workflow/context audits, project QA, composition preflight and the lossless composed-reader render.
