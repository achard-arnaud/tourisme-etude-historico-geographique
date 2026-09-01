---
name: storytelling-historical-travel
description: Use when historical evidence must become a reader-facing narrative without changing evidence strength, reader-scaffold order or uncertainty contracts.
---

# Storytelling historical travel

This file is an **orchestrator**, not a prose prompt. Executable contracts win over prose if they conflict.

## Core architecture — one composition engine, two bootstraps

Run32 removed the false split between an “iterative writer” and a “from-scratch writer”. Run41 fixes the editing order: **the chronological core is drafted and reread before new side stories are placed**. A side story is therefore a post-review editorial stitch, not a section appended after the book and not material that competes with the core during first drafting.

### Shared composition layers — mandatory order

1. **Reader scaffold — authoritative editorial topology**
   - ordered parts, chapters and subsections;
   - imported from an approved reader DOCX when a human scaffold exists;
   - never rebuilt by sorting evidence arcs alphabetically;
   - `reader_scaffold.json` controls the chronological trunk.

2. **Evidence control plane**
   - claims, bridges, questions, source registers, uncertainty and HIL;
   - claims are an **ossature / contract**, not the prose unit;
   - bridge records are relationship instructions, not paragraphs.

3. **Narrative material plane**
   - all relevant capture/field fragments, including candidate-arc fragments not yet referenced by a claim;
   - preserved archived intakes when relevant to the arc;
   - source-attested texture is preferred over claim paraphrase;
   - side-story candidates are collected here but are **not inserted yet**.

4. **Draft the core story**
   - write the chronological/causal trunk first;
   - source-attested fact or observed texture before mechanism;
   - preserve scope and uncertainty;
   - no invented dialogue, thoughts, motives, composite characters or fabricated sensory facts.

5. **Independent core reread / repair, then freeze**
   - run paragraph factual, HIL/scope and style review on the core without new side stories;
   - repair weak transitions, chronology and causal overload;
   - freeze this reviewed core as the placement substrate;
   - a side-story materializer must never be used to hide a weak core transition that should have been repaired here.

6. **Qualify and repair side stories**
   - recover the richest relevant source/field fragments before compressing them into a side story;
   - use the type profile in `templates/side-stories/type_profiles.json`;
   - reject a title + takeaway shell when richer material exists;
   - `candidate` is an evidence status, not a reader ban: a museum-origin candidate independently corroborated by another source may be reader-eligible while remaining `candidate`.

7. **Post-review side-story placement and stitching**
   - place each eligible story beside the **reviewed paragraph that gives it chronological or causal meaning**, or between the two paragraphs it connects;
   - placement is a paragraph-boundary operation: never split a sentence or a table cell;
   - prefer the paragraph containing the strongest direct event/mechanism match; use the surrounding section only as a search envelope;
   - apply a strong density penalty if the previous, current or following paragraph already contains a side story; do not create a wall of boxes;
   - if several placements are historically equivalent, prefer the **longer source-attested paragraph/fragment**, because it provides a safer callback and reduces content loss;
   - a story may be moved one or more paragraph boundaries away to avoid overload, but never across a chronological rupture that changes its meaning;
   - no automatic book-end side-story gallery and no fallback to “append at end”. Failure to find a valid local stitch is a QA failure, not permission to append.

8. **Local continuity reread**
   - reread the paragraph before the story, the story, and the paragraph after it as one unit;
   - verify that the departure is motivated, the return is explicit or naturally resumed, chronology remains legible and the story did not duplicate adjacent prose;
   - if the story overloads the section, relocate it to the next valid low-density boundary rather than deleting source-attested content.

9. **Frontstage / export**
   - reader prose contains simple source citations;
   - `[claim:<id>]`, bridge IDs, machine HIL identifiers, run IDs and lineage remain backstage;
   - a separate ledger binds paragraphs and side stories to claims/sources and records the chosen placement.

### The only mode-specific layer: bootstrap

`iterative`
- load the approved canonical manuscript and append-only construction journal;
- preserve the approved reader scaffold;
- apply bounded, chronologically placed deltas;
- retention against the baseline is a hard concern.

`from_scratch`
- load **no previous reader prose**;
- use the same reader scaffold topology where one is approved;
- use the same evidence/material packets and the same drafting/review/placement engine;
- the packet manifest must report `reader_prose_loaded=false`.

Executable entry point:

`python scripts/build_drafting_packets.py --project <project> --mode iterative|from_scratch`

Compatibility:

`python scripts/build_from_scratch_packets.py --project <project>`

## Reader profiles and preservation contract

Supported reader profiles remain **advanced**, **intermediate** and **child**. The reader plan selects one profile and controls presentation, never evidence strength.

For advanced work there is **no maximum length**. Use the content-preservation gate and explicit dispositions instead of compression by budget. Intermediate and child modes may simplify structure and vocabulary, but they may not silently delete required evidence or uncertainty.

The reader plan, paragraph review state and Sarah-voice review remain deterministic inputs to composition QA. A profile changes exposition; it does not authorize invented dialogue, motives, source inflation or claim loss.

## Input priority for prose generation

When constructing the core or a side story, use this order:

1. source-attested fragments / field material;
2. relevant archived intake as a **research/narrative prompt only**, never as evidence by itself;
3. source records and quotations/notes within allowed scope;
4. claim canonical points and uncertainty as a control check;
5. bridge relation for causal stitching.

Never turn a short claim into the maximum amount of prose available. A short claim can control a paragraph supported by several richer fragments and sources.

### Legacy-fragment migration bypass

`legacy_fragment` is a finite migration bypass, shared by both modes, for explicitly allowlisted old fragments that predate full sourcing/lineage instrumentation. It is virtual drafting context only: it may preserve or reposition already-existing narrative and may seed a research question, but it **cannot establish a new fact, satisfy a sourcing gate, or silently upgrade evidence**. New or sourced fragments must use the normal evidence path. The type never renders in the reader.

## Reader scaffold contract

`story_scaffold.json` is the evidence/graph topology. `reader_scaffold.json` is the narrative topology. They are not interchangeable.

- `reader_scaffold.json` controls reader order and section search envelopes.
- `story_scaffold.json` helps retrieval and cross-arc coverage.
- an evidence arc may map into several reader sections;
- several evidence arcs may be narrated in one chronological reader chapter;
- `placement.section_anchor` narrows the search, but the final insertion point is a **reviewed paragraph boundary selected after the core reread**, not automatically the heading itself.

## Side stories — evidence state versus reader eligibility

A side story is an excursion with a return, not a label + takeaway. Its **evidence status** and its **reader eligibility** are separate decisions.

### Normal path

`candidate → validated → promoted` remains available for material that is itself evidentially important or whose causal wording needs full closure.

### Museum + corroboration path

A side story may remain `candidate` and still be forced into the reader-placement queue when all of the following hold:

- a museum/institutional field intake or museum source is explicitly recorded;
- at least one independent source corroborates the factual core used in the story;
- the corroborating source is not merely a syndication/repetition of the museum wording;
- unresolved details are bounded inside the prose rather than silently upgraded;
- a substantial `content.body_markdown` or structured analytical body exists;
- `reader_eligibility.basis = museum_plus_independent_corroboration` and `forced_pipeline = true` are recorded.

This path **does not promote the underlying claim**. It recognizes that a side story can be a bounded narrative object with a lower evidential threshold than a causal spine claim.

## Type profiles and anti-loss rule

The executable/editorial profile for each kind lives in `templates/side-stories/type_profiles.json`. Profiles were retro-analysed from the repository’s actual stories, including rich and degraded examples.

The anti-loss rule is mandatory: if an intake or capture contains a richer fragment than the side-story body, the disposition must say why the omitted material is redundant, out of scope or evidentially unsafe. Metadata fields such as `purpose`, `takeaway`, `zoom_excursion`, `analysis` or `payoff` **do not count as narrative conservation** when reader-facing prose is missing.

## Placement algorithm contract

The post-review planner may use explicit `placement.match_terms`, chronology, claim/bridge text and section headings to rank paragraph boundaries. Scoring must preserve this priority:

1. exact event/mechanism match;
2. chronological compatibility;
3. causal/bridge match;
4. absence of a side story in the previous/current/next paragraph;
5. paragraph/fragment richness as fallback tie-breaker.

A long paragraph never outranks a clearly better chronological or causal match; length is a **fallback**, not the primary semantic signal.

Every automatic placement produces a ledger entry containing chosen boundary, nearby paragraph excerpt, score/reason, density penalty and whether the longest-fragment fallback was used. Human-specified exact placements may bypass scoring but still require local continuity QA.

## Claims and sources in the final reader

Claims remain backstage. During drafting they constrain factual scope, identify source lineage, carry confidence/type/causal role and support coverage accounting. During export, strip machine markers and keep the full claim→paragraph/side-story→source mapping in the QA ledger.

A “100% claims present” statement is not a reader-quality objective. The objective is **historical matter preserved and sourced**, with claims accounted for backstage.

## Review and conservation

Every final eligible historical unit gets one disposition: `included`, `included_as_side_story`, or `not_selected_for_reader` with rationale. Coverage includes promoted fragments and rich intakes/capture units, not claims alone. A claim referenced once by a thin sentence does not prove narrative conservation.

## Stop conditions

Do not export final if:
- reader scaffold order is violated;
- an iterative run silently drops baseline material;
- an eligible new side story has no valid chronological/causal paragraph stitch;
- an automatic placement falls back to the end of the book;
- adjacent side stories create avoidable paragraph-level overload when another valid boundary exists;
- a new side story is only a title/takeaway while richer source material exists;
- a museum-derived reader-eligible candidate lacks independent corroboration or an explicit uncertainty boundary;
- claim/bridge/run metadata or machine HIL identifiers leak into frontstage;
- a from-scratch run reads previous reader prose;
- an evidence state is silently upgraded;
- a new or sourced fragment enters through the legacy bypass;
- eligible narrative material has no disposition.

## Executable contracts

- `scripts/import_reader_scaffold.py`
- `scripts/build_drafting_packets.py`
- `scripts/build_from_scratch_packets.py`
- `scripts/materialize_side_stories.py`
- `scripts/side_story_contract.py`
- `scripts/paragraph_review_gate.py`
- `scripts/paragraph_repair_loop.py`
- `scripts/reciprocal_coverage_check.py`
- `scripts/evidence_coverage_contract.py`
- `scripts/frontstage_reader_contract.py`
