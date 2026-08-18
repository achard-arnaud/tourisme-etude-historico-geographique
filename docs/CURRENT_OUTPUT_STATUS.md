# Current output status

## Research layer
**Current:** Run 4 social-reproduction/caste/comparator artefacts are materialized on `dev` pending PR merge.

## Canonical Markdown layer
- `examples/sri_lanka_pre_1948/09_output/report.md` — stable baseline.
- `examples/sri_lanka_pre_1948/09_output/report_vnext.md` — current integrated candidate.
- `examples/sri_lanka_post_1948/09_output/report.md` — stable baseline through language/non-alignment work.
- `examples/sri_lanka_post_1948/09_output/report_vnext.md` — current integrated candidate including caste/social mobility/Tamil Nadu/Indonesia.

## Reader-export layer
Existing Word/PDF reading editions predate the current Vnext research. They must **not** be described as current until regenerated from promoted Vnext Markdown.

## Promotion rule
1. research artefacts + drifts complete;
2. deterministic QA green;
3. PR review/merge into `main`;
4. explicit Vnext promotion decision;
5. regenerate Word/PDF using storytelling/editing skills and reader contract.

This separation prevents a field-research iteration from silently overwriting the last known reading edition.