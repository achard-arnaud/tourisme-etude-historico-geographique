# Skill / workflow / artifact index

Current orchestration index. It links each judgment-heavy skill to its durable artefact/handoff and must stay synchronized with `SKILL.md`, `docs/agent_routing.md` and the current reviewed run manifest.

| Step | Skill | Primary artifact / handoff | Durable contract | Consumed by |
|---|---|---|---|---|
| 1 | `capturing-field-evidence` | raw observation + origin/source ID + provisional ARC/HIL/ZOOM + optional side-story candidate hint | session ledger / source note | sanitize, source, arc |
| 2 | `sanitizing-historical-claims` | typed statement | `templates/claim.md` | arcs, HILs, composition lineage |
| 3 | `structuring-chronological-arcs` | rupture-bounded chronology + home-arc decisions | `templates/arc.md` / `ARC.md` when materialized | all downstream |
| 4 | `zooming-geographic-scales` | Z0–Z4 placement + transmission mechanism | claim/HIL placement; dezoom candidate handoff | HILs, bridges, composition |
| 5 | `sourcing-historical-anchors` | source register entry | `05_sources/source_register*.json` | all evidence consumers + side stories |
| 6 | `analyzing-institutions-and-power` | HIL-01 claim candidates / side-story candidate hints | canonical claims; HIL artefact only when actually persisted | bridges, composition |
| 6 | `analyzing-geography-and-environment` | HIL-02 claim candidates / dezoom-object hints | same | same |
| 6 | `analyzing-economy-and-infrastructure` | HIL-03 claim candidates / lateral examples | same | same |
| 6 | `analyzing-society-and-demography` | HIL-04 claim candidates / portrait-callback hints | same | same |
| 6 | `analyzing-religion-culture-legitimacy` | HIL-05 claim candidates / object-portrait hints | same | same |
| 6 | `analyzing-security-and-geopolitics` | HIL-06 claim candidates / dezoom-false-lead hints | same | same |
| 7 | `building-causal-bridges` | bridge record A/B/C/D/U | `06_bridges/*.json` | drift, composition, editor |
| 8 | `auditing-historiography-and-drifts` | drift/correction ledger | `07_drifts/*.md` | composition, editor |
| 9 | `maintaining-wiki-and-graph` | reusable entities + typed relations | `03_wiki/**/*.md`, `04_graph/*.jsonl` | recall/composition |
| 10 | `composing-side-stories` | normalized off-trunk composition record with lineage/placement/return | `templates/side-story.json` → `09_output/side_stories/*.json` | editor, storytelling, QA, renderer |
| 11 | `editing-historical-travel-output` | chronological canonical manuscript consuming promoted/validated side stories | `templates/output-outline.md` → `09_output/*.md` | storytelling/export |
| 12 | `storytelling-historical-travel` | optional non-destructive reader pass | canonical side-story identity retained; Markdown markers preserved | reader export |
| 13 | orchestrator | dispatched/skipped skills + evidence paths | `templates/run-manifest.json` | `audit_workflow.py` |
| 14 | orchestrator | final state/promotion checkpoint | project/run status | next run |

## Contract boundaries

- HIL analysis is not durable merely because a skill ran; only actually persisted claim/HIL artefacts count as state.
- `side_story` is the first durable **composition** artefact. It is not historical evidence and cannot upgrade the confidence/tier of its lineage.
- Validated/promoted side stories require one home arc, lineage, a stable placement, `return_to`, normalized `kind → label`, and for `dezoom` a Z-path/mechanism/local payoff.
- Candidate hints emitted by upstream skills are not side-story records until `composing-side-stories` creates/validates the JSON artefact.
- `qa_project.py` validates evidence integrity plus side-story lineage; the reader renderer independently enforces survival of promoted `required_in_reader` side stories.
- Mechanical GREEN does not prove historical truth; semantic review remains required.

See `docs/SOP_SIDE_STORIES.md`, `docs/architecture.md`, `docs/agent_routing.md`.
