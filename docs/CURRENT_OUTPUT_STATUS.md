# Current output status

## Research layer
**Current:** Run 5 comparative-development research is complete, validated and merged through **PR #11** into `main` on 2026-08-18. Merge commit: `af4e33f12faa22d8b498c12bc175cf513102dfa8`. `dev` was resynchronized with that merge before this final status update.

Run 5 closes the current mandatory evidence-integration cycle: Jaffna ↔ Tamil Nadu ↔ Indonesia, territorial human-capital conversion/externalisation, war-development channels, comparator-scale controls, caste/social reproduction, and the postwar shared-gateway integration framework are now part of the maintained corpus.

## Validation checkpoint
Final GREEN CI: `skill-ci` run **32130831894**.
- 32 unit tests: GREEN;
- skill audit: GREEN;
- pre-1948 QA: **9 claims / 20 sources / 3 wiki pages / 4 graph edges / 0 warnings**;
- post-1948 QA: **30 claims / 48 sources / 7 wiki pages / 10 graph edges / 0 warnings**.

The run included one deliberate RED→GREEN correction cycle: CI first exposed two skill-contract wording regressions; both were fixed before merge.

## Canonical Markdown layer
**Promoted and merged:**
- `examples/sri_lanka_pre_1948/09_output/report.md` — canonical social/geopolitical manuscript including Jaffna/VOC paper-state, caste codification and the education bridge to 1948;
- `examples/sri_lanka_post_1948/09_output/report.md` — canonical Run 5 manuscript integrating language, caste, mobility, war/diaspora, Tamil Nadu, Indonesia and territorial conversion of human capital.

`report_vnext.md` files remain useful research/audit snapshots but are no longer the source of truth for the next reader export.

## Knowledge layer
**Current and validated:**
- `03_wiki/` is materialized in both Sri Lanka worked corpora with durable entities, confidence, provenance and review dates;
- `04_graph/edges.jsonl` is materialized with typed, sourced relations;
- modular `source_register*.json` files are supported and duplicate IDs are blocked by QA;
- QA validates wiki metadata/source references and graph provenance.

## Reader-export layer
Existing Word/PDF reading editions **still predate Run 5** and are therefore stale by design. They must not be described as current.

## Current decision point
**Research integration and Markdown promotion are complete.** The next action is no longer research or another mandatory comparator pass: it is deliberate regeneration of the Word/PDF reader editions from the canonical Markdown, using `editing-historical-travel-output` + `storytelling-historical-travel` and the established reader contract.

This separation is intentional: a research run can be complete and fully merged while the formatted reading edition remains one generation behind.
