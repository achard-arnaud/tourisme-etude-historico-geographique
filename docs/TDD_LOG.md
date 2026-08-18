# TDD log

Method adapted from `obra/superpowers`: tests first, observe RED, implement minimum behavior, verify GREEN, then refactor.

## Cycle 1 — executable skill OS
Baseline: 8 tests / 8 failures. Implemented orchestrator/sub-skills, templates, project scaffolding, QA and CI. GREEN: 8 tests OK + skill audit.

## Cycle 2 — deep ARC×HIL×ZOOM + bridge integrity
Review found descriptive-only deep artefacts and unchecked bridge references. Tests first: 10 tests / 3 failures. GREEN after `new_arc.py`, deep scaffolding and bridge/source-tier QA.

## Cycle 3 — provenance integrity
PR review found malformed source registers could be silently accepted and resolved bridges could be unsourced/unknown. GitHub Actions run `31787289210` on test-only commit `64af3cb`: 13 tests / 3 failures. GREEN after provenance hardening.

## Cycle 4 — Jaffna/VOC run: reader rendering + institutional corpus routing
### RED A — architectural gaps
The 18 August 2026 field run exposed two architectural gaps: final storytelling was conflated with structural editing, and source importance was conflated with epistemic tier. It also required worked pre/post-1948 corpora rather than abstract architecture only.

Test-only commit `ce49854` added five contracts. GitHub Actions run `32107479318` proved RED:
```text
Ran 18 tests
FAILED (failures=5)
```
Exact missing behaviours: storytelling skill; root routing; specialist-institutional-anchor distinction; dual Sri Lanka examples; Stichting crawl inventory.

### GREEN A
Implementation commit series added the reader-contract storytelling layer, two-axis source policy, systematic discoverable-site inventory and two Sri Lanka worked corpora. GitHub Actions run `32107998725` on `b596e9f` was GREEN; unittest and skill audit passed.

### RED B — request-for-feedback refinement
Formal PR review then found three quality gaps: example corpora had no atomic claims/bridges, two Cambridge anchors used generic homepage URLs, and the post-1948 source register omitted the Presidential Secretariat while naming the current presidency.

Test-only commit `13327bd` encoded those findings. GitHub Actions run `32108098907` returned failure as expected.

### GREEN B
Commit `7ef4c8c` materialized pre/post claims and bridge artefacts, replaced generic Cambridge links with exact resources, and added the current Presidential Secretariat anchor. GitHub Actions run `32108190963` completed successfully; unittest and skill audit both passed.

### Final verification extension
CI now also runs deterministic `qa_project.py` against both worked Sri Lanka example corpora, so future skill changes cannot silently break their provenance/bridge contracts.

## Cycle 5 — Run 6 storytelling review, workflow proof and v2 reader editions
### RED — non-fiction storytelling contract
The second-pass review converted the three requested video transcripts and two external storytelling repositories into bounded method hypotheses. A new test required an explicit historical-nonfiction safety gate, a promise/callback ledger and the PACE vignette structure. The first full run exposed one lexical gap: the skill prohibited fabrication but did not expose the contract phrase `invented dialogue`.

### GREEN — explicit gate and reproducible packaging
The skill wording was corrected without weakening the test. The cycle then added:
- a 16-skill run manifest plus deterministic `audit_workflow.py` coverage;
- the 17-record Polonnaruwa conversation-source inventory and audit note;
- reusable reader contracts and `render_reader_exports.py`;
- two visually inspected DOCX/PDF v2 editions.

Final local gate: **34 tests GREEN**, skill audit GREEN, workflow audit **16/0/16**, both corpus QA runs at zero warnings, valid DOCX archives and valid unencrypted Letter-size PDFs.
