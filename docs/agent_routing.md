# Agent routing

1. Field evidence → capture + sanitize.
2. Periodization problem → chronological arcs.
3. Scale problem → geographic zoom.
4. Factual/causal uncertainty → source anchor.
5. Domain mechanism → corresponding analysis sub-skill.
6. Missing causal link → bridge.
7. Narrative or source distortion → drift audit.
8. Repeated entity/claim → wiki/graph.
9. Manuscript architecture → output editor.
10. Reader voice, density and narrative continuity → storytelling.

Never dispatch every sub-skill automatically. Missing HIL coverage can be intentional. For every substantial run, the agent writes a manifest that records:

- state before and after at research, canonical Markdown and reader-export layers;
- each dispatched skill, its reason, inputs, outputs and execution status;
- each skipped skill and the reason it was unnecessary;
- deterministic validations and promotion decision.

`scripts/audit_workflow.py` rejects unknown or duplicated skills, missing evidence paths and an incomplete routing inventory once the manifest is marked `reviewed`. A full-project review may legitimately dispatch every skill; an ordinary research question should not.
