---
name: storytelling-historical-travel
description: Use when historical evidence must become a reader-facing narrative without changing evidence strength, reader-scaffold order or uncertainty contracts.
---

# Storytelling historical travel

This file is an **orchestrator**, not a prose prompt. Executable contracts win over prose if they conflict.

## Core architecture — one composition engine, two bootstraps

Run32 removed the false split between an “iterative writer” and a “from-scratch writer”. Run41 fixes the editing order: **the chronological core is drafted and reread before new side stories are placed**. The default placement is now explicit: **a side story lives inside the logical paragraph that needs it**, at a safe sentence boundary after its trigger. Inter-paragraph placement is a density/structure fallback, not the normal case.

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
   - a side story must never hide a weak core transition that should have been repaired here.

6. **Qualify and repair side stories**
   - recover the richest relevant source/field fragments before compressing them into a side story;
   - use `templates/side-stories/type_profiles.json` for type-specific length, structure and storytelling rules;
   - reject a title + takeaway shell when richer material exists;
   - `candidate` is an evidence status, not a reader ban: a museum-origin candidate independently corroborated by another source may be reader-eligible while remaining `candidate`.

7. **Post-review side-story placement — host paragraph first**
   - resolve the **reviewed host paragraph** whose event, object, inference or mechanism makes the story necessary;
   - default to `embedded_in_host_paragraph`: choose a safe sentence boundary after the trigger, preserve meaningful prose before and after, then visually insert the side-story block between the two segments of the same logical paragraph;
   - never split a sentence, quotation, table cell or atomic list item;
   - maximum **one embedded side story per host paragraph**;
   - when several stories compete for one host, keep embedded the one most dependent on that paragraph; reroute the others to a semantically equivalent paragraph or to a valid local interstitial boundary;
   - apply the **three-paragraph density rule**: if previous/current/next paragraphs would each contain an embedded side story, keep two inside their paragraphs and move the story most naturally autonomous/interstitial to one boundary between paragraphs;
   - choose the interstitial story first by the type's `interstitial_affinity`, then by transition fit and chronological coherence; density never authorizes deletion;
   - maximum **one interstitial side story per boundary**;
   - if a host is unsplittable, use a local interstitial fallback rather than breaking sentence integrity;
   - paragraph/fragment length is only a tie-breaker after semantic and chronological equivalence;
   - never append an unresolved story at book end and never move one across a chronological rupture merely for layout.

8. **Local continuity reread after stitching**
   - reread: preceding paragraph → first segment of host paragraph → side story → resumed host paragraph → following paragraph;
   - verify that the trigger precedes the excursion, the resumed sentence flow is grammatical, chronology remains legible, and the story does not duplicate adjacent prose;
   - for an interstitial density fallback, reread both adjacent paragraphs and confirm that the story genuinely bridges or pauses between them rather than merely occupying spare space;
   - a failed local stitch is repaired or relocated; sourced content is not silently dropped.

9. **Frontstage / export**
   - reader prose contains simple source citations;
   - `[claim:<id>]`, bridge IDs, machine HIL identifiers, run IDs and lineage remain backstage;
   - a separate placement ledger binds paragraph/side-story/source lineage and records host paragraph, sentence split or interstitial boundary, density decision and fallback reason.

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

For advanced work there is **no maximum length** for the manuscript. Side-story type profiles use a hard minimum, a normal target range and a **soft upper review threshold**. Crossing the soft upper threshold triggers splitting, promotion into the trunk or retyping; it never authorizes truncation of sourced matter.

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

- `reader_scaffold.json` controls reader order and the search envelope for the host paragraph;
- `story_scaffold.json` helps retrieval and cross-arc coverage;
- an evidence arc may map into several reader sections;
- several evidence arcs may be narrated in one chronological reader chapter;
- `placement.section_anchor` narrows the search, but final placement resolves to a **reviewed host paragraph plus a sentence boundary**; only the density/unsplittable fallback resolves to an inter-paragraph boundary.

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

This path **does not promote the underlying claim**. It recognizes that a side story can be a bounded narrative object with a lower evidential threshold than a causal-spine claim.

## Type profiles and anti-loss rule

The executable/editorial profile for each kind lives in `templates/side-stories/type_profiles.json`. Each profile now defines:

- narrative job;
- mandatory beats;
- differentiated storytelling rules;
- hard minimum visible words;
- normal target range;
- soft upper review threshold;
- default embedded position;
- interstitial affinity for density arbitration.

The anti-loss rule is mandatory: if an intake or capture contains a richer fragment than the side-story body, the disposition must say why omitted material is redundant, out of scope or evidentially unsafe. Metadata fields such as `purpose`, `takeaway`, `zoom_excursion`, `analysis` or `payoff` **do not count as narrative conservation** when reader-facing prose is missing.

## Placement algorithm contract

The post-review planner may use explicit `placement.match_terms`, chronology, claim/bridge text and section headings to rank host paragraphs. Priority is:

1. exact event/object/mechanism match;
2. chronological compatibility;
3. causal/bridge match;
4. type-specific paragraph dependence and availability of a safe sentence split;
5. density contract;
6. paragraph/fragment richness as final tie-breaker.

The planner must emit a ledger entry with:
- host paragraph excerpt/ordinal;
- placement mode `embedded` or `interstitial`;
- sentence split position when embedded;
- semantic/chronological/mechanism matches;
- same-host and three-paragraph density decisions;
- interstitial-affinity comparison when a story is displaced;
- whether the longest-fragment fallback was used.

## Claims and sources in the final reader

Claims remain backstage. During drafting they constrain factual scope, identify source lineage, carry confidence/type/causal role and support coverage accounting. During export, strip machine markers and keep the full claim→paragraph/side-story→source mapping in the QA ledger.

A “100% claims present” statement is not a reader-quality objective. The objective is **historical matter preserved and sourced**, with claims accounted for backstage.

## Review and conservation

Every final eligible historical unit gets one disposition: `included`, `included_as_side_story`, or `not_selected_for_reader` with rationale. Coverage includes promoted fragments and rich intakes/capture units, not claims alone. A claim referenced once by a thin sentence does not prove narrative conservation.

## Stop conditions

Do not export final if:
- reader scaffold order is violated;
- an iterative run silently drops baseline material;
- an eligible new side story has no valid host paragraph or local interstitial fallback;
- more than one side story is embedded in the same logical paragraph;
- three consecutive paragraphs all retain embedded side stories instead of applying the density fallback;
- more than one interstitial story occupies the same paragraph boundary;
- an automatic placement falls back to the end of the book;
- a sentence/table/list atom is split to make room for a story;
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
- `scripts/post_review_side_story_placement.py`
- `scripts/materialize_side_stories.py` (legacy/direct materialization compatibility)
- `scripts/side_story_contract.py`
- `scripts/paragraph_review_gate.py`
- `scripts/paragraph_repair_loop.py`
- `scripts/reciprocal_coverage_check.py`
- `scripts/evidence_coverage_contract.py`
- `scripts/frontstage_reader_contract.py`
