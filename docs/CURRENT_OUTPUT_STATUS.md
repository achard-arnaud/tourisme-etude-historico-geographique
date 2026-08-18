# Current output status

## Research layer
**Current on `dev`:** Run 5 comparative-development research is complete and staged for PR validation. It deepens Jaffna ↔ Tamil Nadu ↔ Indonesia, adds territorial human-capital conversion/externalisation, war-development channels, comparator-scale controls, and materializes wiki/graph layers for both Sri Lanka corpora.

## Canonical Markdown layer
Promotion is staged in this Run 5 PR:
- `examples/sri_lanka_pre_1948/09_output/report.md` — promoted social/geopolitical manuscript, including Jaffna/VOC paper-state, caste codification and the education bridge to 1948;
- `examples/sri_lanka_post_1948/09_output/report.md` — promoted Run 5 manuscript integrating language, caste, mobility, war/diaspora, Tamil Nadu, Indonesia and territorial conversion of human capital;
- `report_vnext.md` files are retained as research/audit snapshots rather than the reader-export source of truth after merge.

## Knowledge layer
- `03_wiki/` is now materialized in both worked corpora with durable entities, provenance, confidence and review dates;
- `04_graph/edges.jsonl` is now materialized with typed, sourced relations;
- project QA now validates modular source registers, wiki metadata/source references and graph provenance.

## Reader-export layer
Existing Word/PDF reading editions **still predate Run 5**. They must not be described as current. After this PR merges GREEN, the next editorial task is regeneration from the promoted canonical Markdown using `editing-historical-travel-output` + `storytelling-historical-travel` and the established reader contract.

## Promotion rule
1. research artefacts + drifts complete;
2. wiki/graph refreshed;
3. deterministic tests + skill audit + both project QA GREEN;
4. PR review/merge into `main`;
5. resynchronize `dev`;
6. record merge/CI checkpoint;
7. regenerate Word/PDF deliberately.

## Current decision point
No additional evidence-integration pass is mandatory for the current Sri Lanka edition. **The only remaining gate before reader-export regeneration is fresh PR CI/QA and merge.**

This file is deliberately updated again after merge with the exact PR, merge commit and CI result so “research complete”, “Markdown promoted” and “reader export current” cannot be conflated.
