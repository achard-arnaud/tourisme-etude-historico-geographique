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
| 3 | `structuring-chronological-arcs` | `ARC.md` per period + vertical-thread IDs | `templates/arc.md` | every downstream skill; `01_arcs/<arc>/ARC.md` |
| 4 | `zooming-geographic-scales` | zoom-labelled claim/HIL placement (`Z0`–`Z4`) | `02_hil/<HIL-id>/Z<n>/` (created by `scripts/new_arc.py`) | `analyzing-*` skills, `building-causal-bridges` |
| 5 | `sourcing-historical-anchors` | source register entry (tier + anchor role) | `templates/source-note.md` → `05_sources/source_register*.json` | `qa_project.py`, all claim/bridge/wiki/graph consumers |
| 6 | `analyzing-institutions-and-power` | HIL-01 analytic notes / access-architecture claims | feeds `templates/claim.md` | `structuring-chronological-arcs`, `building-causal-bridges` |
| 6 | `analyzing-geography-and-environment` | HIL-02 analytic notes | feeds `templates/claim.md` | same |
| 6 | `analyzing-economy-and-infrastructure` | HIL-03 analytic notes | feeds `templates/claim.md` | same |
| 6 | `analyzing-society-and-demography` | HIL-04 analytic notes | feeds `templates/claim.md` | same |
| 6 | `analyzing-religion-culture-legitimacy` | HIL-05 analytic notes | feeds `templates/claim.md` | same |
| 6 | `analyzing-security-and-geopolitics` | HIL-06 analytic notes | feeds `templates/claim.md` | same |
| 7 | `building-causal-bridges` | bridge record, closed `A/B/C/D/U` | `templates/bridge.md` → `06_bridges/*.json` | `auditing-historiography-and-drifts`, `editing-historical-travel-output` |
| 8 | `auditing-historiography-and-drifts` | drift audit + correction ledger | `templates/drift-audit.md` → `07_drifts/*.md` | `editing-historical-travel-output` |
| 9 | `maintaining-wiki-and-graph` | wiki entity page + graph edge | `templates/wiki-entity.md` → `03_wiki/**/*.md`, `04_graph/*.jsonl` | every skill needing cross-arc recall |
| 10 | `editing-historical-travel-output` | structured chronological manuscript | `templates/output-outline.md` → `09_output/*.md` | `storytelling-historical-travel` |
| 11 | `storytelling-historical-travel` | reader-voice pass over the promoted manuscript (optional, non-destructive) | `skills/storytelling-historical-travel/references/*` | reader export (`render_full_reader_v3.py`, `render_reader_exports.py`) |
| 12 | (orchestrator) | run manifest (dispatched/skipped skills, reasons, artefact paths) | `templates/run-manifest.json` | `scripts/audit_workflow.py` |

## Reading this table

- **HIL skills (step 6)** share one step because the orchestrator dispatches
  only the HILs relevant to the run (`docs/agent_routing.md` — "Never dispatch
  every sub-skill automatically"); none of them owns a dedicated template
  because their output is analytic content that lands inside `claim.md`
  records, not a standalone file type.
- A skill with **no template column entry** produces a routing decision or
  in-conversation classification rather than a persisted artefact; its
  contract is enforced by the receiving skill/script instead (e.g.
  `capturing-field-evidence`'s ledger is validated once promoted to a source
  note, not on capture).
- `scripts/qa_project.py` and `scripts/audit_workflow.py` are the mechanical
  backstops for this table: they reject unsourced claims/bridges, duplicate
  wiki slugs, unsourced interpretive graph edges, and manifest entries that
  name a skill missing from this index.

See also `docs/architecture.md` (system-level model) and
`docs/agent_routing.md` (dispatch rules).
