# TDD log

Method adapted from `obra/superpowers`: tests first, observe RED, implement minimum behavior, verify GREEN, then refactor.

## Cycle 1 — executable skill OS
### RED
Baseline contained only root `SKILL.md`, `README.md`, and the graph-light design note.

Command:
```bash
python -m unittest discover -s tests -v
```
Observed: **8 tests / 8 failures**.

### GREEN
Implemented the orchestrator/sub-skill split, templates, project scaffolding, QA scripts and CI.

Observed locally: 8 tests OK, `SKILL AUDIT OK`.

## Cycle 2 — feedback hardening: deep ARC×HIL×ZOOM + bridge integrity
### RED
Review identified that the architecture described deep HIL/zoom artefacts but did not materialize them, and that bridge references were not checked. Added tests first: 10 tests, 3 failures.

### GREEN
Implemented deep arc scaffolding and bridge/source-tier QA: 10 tests OK, `SKILL AUDIT OK`.

## Cycle 3 — PR review: provenance integrity
### RED
PR review found that malformed source registers were silently accepted and resolved bridges could be unsourced or cite unknown sources. GitHub Actions run `31787289210` on test-only commit `64af3cb` proved RED: 13 tests / 3 failures.

### GREEN
`qa_project.py` now treats malformed/duplicate source metadata as errors and validates sources for resolved bridges. Final GREEN is recorded in `QA_LOG.md`.

## Cycle 4 — Jaffna/VOC run: reader rendering + institutional corpus routing
### RED
The 18 August 2026 field run exposed two architectural gaps: final storytelling was conflated with structural editing, and source importance was conflated with epistemic tier. It also required worked pre/post-1948 corpora rather than abstract architecture only.

Test-only commit `ce49854` added five contracts. GitHub Actions run `32107479318` proved the expected RED state:
```text
Ran 18 tests
FAILED (failures=5)
```
The failures were exactly: no storytelling skill; no root routing to it; no specialist-institutional-anchor distinction; no dual Sri Lanka examples; no materialized Stichting crawl inventory.

### GREEN target
Implementation adds the reader-contract storytelling layer, two-axis source policy, systematic discoverable-site inventory, and two Sri Lanka worked corpora. Fresh CI evidence is required before merge and will be recorded on the PR/QA log.
