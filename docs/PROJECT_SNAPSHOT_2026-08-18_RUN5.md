# Project snapshot — 2026-08-18 / Run 5

## Repository
`achard-arnaud/tourisme-etude-historico-geographique`

Workflow: `dev` → PR → CI/QA → `main` → resync `dev`.

## Sri Lanka research state
### Pre-1948
- stable historical corpus exists;
- Run 4 Vnext adds Jaffna/VOC social-reproduction layer;
- Run 5 materializes reusable wiki and graph entities for Jaffna, VOC paper-state and caste codification.

### Post-1948
- Run 4 Vnext integrates education/English, language redistribution, caste, Maviddapuram, LTTE/public authority, marriage/diaspora, Tamil Nadu and Indonesia;
- Run 5 adds the deeper development-conversion pass: Jaffna territorial scarring/externalisation, Tamil Nadu institutional package, Indonesia multilingual nation-building and comparator-scale controls;
- new A13 claims and bridges are intended to close the last major comparative research gap before reader-export regeneration.

## Architecture state
- root orchestrator + 16 specialized skills;
- arc-first chronology with vertical HIL threads;
- modular source registers supported;
- source tiers T0–T5 + anchor roles;
- A/B/C/D/U confidence;
- project wiki (`03_wiki`) and graph-light (`04_graph`) now materialized;
- deterministic QA validates claims, sources, bridges, wiki and graph.

## Output-state contract
Three independent layers:
1. research artefacts;
2. promoted Markdown narrative;
3. formatted reader edition (Word/PDF).

Never infer that layer 3 is current because layers 1–2 advanced.

## Remaining gate at snapshot creation
Run fresh unit tests, skill audit and both Sri Lanka project QA in CI; review PR; merge only GREEN; resynchronize `dev`; then update the final status record with the merge commit and reader-export decision.
