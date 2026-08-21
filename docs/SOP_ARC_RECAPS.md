# SOP — Arc recaps

1. Stabilize arc claims/bridges and pass graph-link preflight.
2. Create `09_output/arc_recaps/<id>.json` from `templates/arc-recap.json`.
3. Populate causal roles only from existing claims.
4. Add protagonist objective/constraint/options with claim lineage.
5. Add 2–4 `prepares_next` bullets tied to next arc/bridge where available.
6. Declare `placement.before_anchor`: the stable heading that begins the next arc/section. This is the mechanical definition of “end of arc”.
7. Validate with `arc_recap_contract.py` / project QA. The placement anchor must resolve in canonical Markdown.
8. Run `materialize_arc_recaps.py --project <project> --source <markdown> --output <markdown>` before the editing/storytelling pass. The operation is idempotent and uses marker-delimited blocks.
9. Storytelling may simplify wording for the selected reader profile but may not alter the causal graph, protagonist lineage, or forward bridge without changing the structured recap.
