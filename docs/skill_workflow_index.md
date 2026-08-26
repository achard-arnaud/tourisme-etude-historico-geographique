# Skill / workflow / artifact index

| Stage | Skill/capability | Durable artefact | Mechanical gate / consumer |
|---|---|---|---|
| Video evidence | `extracting-youtube-evidence` | `video-evidence/v1` ledgers + lead-only proposition register | video claim contract / sanitizer |
| Evidence | `capturing-field-evidence` | field/session record | sanitizer/source layer |
| Claims | `sanitizing-historical-claims` | typed claim | project QA |
| Chronology | `structuring-chronological-arcs` | `ARC.md` | recap/editor |
| Scale | `zooming-geographic-scales` | Z0–Z4 claim/HIL placement | side-story dezoom |
| Sources | `sourcing-historical-anchors` | source registers | project QA |
| HIL-01..06 | six `analyzing-*` domain skills | claim/HIL baselines | bridge/composition |
| HIL-07 | `analyzing-regional-global-systems` | regional/global analysis | dezoom/bridge |
| HIL-08 | `auditing-historiography-and-drifts` | drift audit | false-lead/method composition |
| Causality | `building-causal-bridges` | `06_bridges/*.json` | recap/editor |
| Knowledge | `maintaining-wiki-and-graph` | wiki + nodes/edges | **graph-link preflight** |
| Side composition | `composing-side-stories` | `09_output/side_stories/*.json` | side-story validator/materializer |
| Arc close | `composing-arc-recaps` | `09_output/arc_recaps/*.json` | recap validator/editor |
| Maps | `curating-historical-map-assets` | `09_output/map_assets/*.json` + image | vision + human gate |
| Audience | `tailoring-reader-profiles` | reader profile + `reader_plan.json` | deterministic selector |
| Editing | `editing-historical-travel-output` | state-resolved canonical Markdown | composition preflight |
| Storytelling | `storytelling-historical-travel` | reader export | retention + reader-plan/map gates |
| Workflow | orchestrator | latest `RUN*_MANIFEST.json` | `audit_workflow.py --latest` |

A durable claim is not equivalent to a side story; a side story is not evidence; a map is not automatically admissible because it is visually plausible. Passing QA means the declared artefact contracts are mechanically satisfied for the paths the pipeline actually owns.
