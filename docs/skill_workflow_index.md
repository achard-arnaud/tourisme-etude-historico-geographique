# Skill / workflow / artifact index

Navigation hub linking every sub-skill to its place in `SKILL.md`'s orchestration
list, its primary artifact, and the template that gives that artifact a stable
shape. This file is read-only reference material generated from the current
skill contracts; it does not add new rules and must stay in sync with
`SKILL.md` § Orchestration and `docs/agent_routing.md`.

| Step | Skill | Primary artifact | Template / schema | Consumed by |
|---|---|---|---|---|
| 1 | `capturing-field-evidence` | session ledger entry (raw observation, source/artefact ID, provisional ARC/HIL/ZOOM) | — (feeds `templates/source-note.md` once corroborated) | `sourcing-historical-anchors`, `structuring-chronological-arcs` |
| 2 | `sanitizing-historical-claims` | typed statement (`source_fact`/`claim`/`inference`/…) | `templates/claim.md` | `structuring-chronological-arcs`, all `analyzing-*` skills |
| 3 | `structuring-chronological-arcs` | arc metadata / chronological structure | `templates/arc.md` (runtime materialization remains incomplete) | every downstream skill |
| 4 | `zooming-geographic-scales` | zoom-labelled analysis placement (`Z0`–`Z4`) | `02_hil/` is a scaffold/planned layer, not guaranteed persisted output | `analyzing-*` skills, `building-causal-bridges` |
| 5 | `sourcing-historical-anchors` | source register entry (tier + anchor role) | `templates/source-note.md` → `05_sources/source_register*.json` | `qa_project.py`, all claim/bridge/wiki/graph consumers |
| 6 | `analyzing-institutions-and-power` | HIL-01 analysis → evidence-backed claim candidates | current runtime: canonical claim layer; no guaranteed standalone HIL file | `structuring-chronological-arcs`, `building-causal-bridges` |
| 6 | `analyzing-geography-and-environment` | HIL-02 analysis → evidence-backed claim candidates | current runtime: canonical claim layer; no guaranteed standalone HIL file | same |
| 6 | `analyzing-economy-and-infrastructure` | HIL-03 analysis → evidence-backed claim candidates | current runtime: canonical claim layer; no guaranteed standalone HIL file | same |
| 6 | `analyzing-society-and-demography` | HIL-04 analysis → evidence-backed claim candidates | current runtime: canonical claim layer; no guaranteed standalone HIL file | same |
| 6 | `analyzing-religion-culture-legitimacy` | HIL-05 analysis → evidence-backed claim candidates | current runtime: canonical claim layer; no guaranteed standalone HIL file | same |
| 6 | `analyzing-security-and-geopolitics` | HIL-06 analysis → evidence-backed claim candidates | current runtime: canonical claim layer; no guaranteed standalone HIL file | same |
| 7 | `building-causal-bridges` | bridge record, closed `A/B/C/D/U` | `templates/bridge.md` → `06_bridges/*.json` | `auditing-historiography-and-drifts`, `editing-historical-travel-output` |
| 8 | `auditing-historiography-and-drifts` | drift audit + correction ledger | `templates/drift-audit.md` → `07_drifts/*.md` | `editing-historical-travel-output` |
| 9 | `maintaining-wiki-and-graph` | wiki entity page + graph edge | `templates/wiki-entity.md` → `03_wiki/**/*.md`, `04_graph/*.jsonl` | every skill needing cross-arc recall |
| 10 | `editing-historical-travel-output` | structured chronological manuscript | `templates/output-outline.md` → `09_output/*.md` | `storytelling-historical-travel` |
| 11 | `storytelling-historical-travel` | reader-voice pass over the promoted manuscript (optional, non-destructive) | `skills/storytelling-historical-travel/references/*` | reader export (`render_full_reader_v3.py`, `render_reader_exports.py`) |
| 12 | (orchestrator) | run manifest (dispatched/skipped skills, reasons, artefact paths) | `templates/run-manifest.json` | `scripts/audit_workflow.py` |

## Reading this table

- **HIL skills (step 6)** share one step because the orchestrator dispatches only the dimensions relevant to the run. Their analytical output is useful, but the current repository does **not** yet guarantee a persisted structured HIL artefact. A skill must not claim that `02_hil/` was written unless a corresponding file actually exists.
- `02_hil/` and arc templates express a target architecture that is only partially materialized in the worked corpora. Treat template presence and scaffold intent separately from persisted evidence.
- A skill with **no guaranteed persisted artifact** produces a routing/classification/analysis result that must be promoted into an actually stored downstream record before it can be treated as durable project state.
- `scripts/qa_project.py` and `scripts/audit_workflow.py` are mechanical backstops, but their current coverage is narrower than the complete epistemic contracts; passing QA must not be interpreted as proof that every declared artifact contract is materialized.

See also `docs/architecture.md` (system-level model) and
`docs/agent_routing.md` (dispatch rules).