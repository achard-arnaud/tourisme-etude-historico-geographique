# Run27 salvage decision

`feat/run27-convergence` is not mergeable as a whole: it diverged before Run28/Run29, mixes superseded historical content with still-useful engineering contracts, and its own PR states that the semantic manuscripts and closure report were never completed.

## Salvaged into the canonical line

- paragraph repair loop with three attempts and explicit final disposition;
- marker-first `return_to` resolution with persisted research fallback and challenge/redirect semantics;
- exhaustive evidence-coverage contract that distinguishes presence from narrative depth and blocks unaccounted eligible material;
- canonical-points migration audit, warning-only until real population exists;
- immutable hash manifest identifying the archived Run26 artefacts;
- corresponding storytelling orchestration rules and focused regression tests.

## Intentionally not salvaged as-is

- Run27 Mihintale/Abhayagiri/iconography claims and side story: later Run28/Run29 evidence work supersedes or overlaps them and they require claim-by-claim reconciliation before reuse;
- `return_target_research_run27.json`: research closures were written against a pre-Run28 manuscript topology and paragraph anchors, so importing them blindly could bind stale targets;
- Run27 final renderer / close scripts / CI publication steps: they are tightly coupled to an unfinished Run27 manuscript generation workflow;
- branch-level changes to Run16 capture/source registers: later canonical runs already modified those artefacts;
- Run27 draft/status documents as active workflow state: retained only in the old branch for archaeology.

## Branch disposition

After the salvage PR is green and merged, `feat/run27-convergence` should be treated as a historical branch, not a release candidate. Any future recovery from it must be file-level and evidence-aware.
