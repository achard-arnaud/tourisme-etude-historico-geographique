---
name: maintaining-wiki-and-graph
description: Use when stabilized claims, people, places, institutions, commodities, policies, sources, or repeated relationships need reusable cross-arc storage and resolvable graph-light links.
---

# Maintaining wiki and graph

Wiki stores durable entities; arcs temporal context; HILs analytic views. Graph-light stores typed relations, not prose.

Every edge endpoint must resolve to an explicit graph node, wiki slug, claim, bridge or supported composition fragment. Maintain `04_graph/nodes.jsonl` for concept fragments that are not first-class wiki/claim objects. Do not create ghost endpoints merely because a label appears in prose.

## Pre-edit invariant
`python scripts/graph_link_audit.py <project>` is mandatory before composition/editing. **Zero unresolved endpoints** is the only passing state. Editing cannot rename or infer unresolved fragments silently.

Causal/interpretive edges require provenance and confidence. After substantial research, update entities/edges, resolve contradictions, run graph-link audit, then release the project to composition.
