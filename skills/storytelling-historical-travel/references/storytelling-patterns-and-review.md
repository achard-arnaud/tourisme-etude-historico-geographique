# Storytelling review — Run 6

## Evidence protocol

Review date: **2026-08-18**. The three YouTube sources were processed with the repository-native `youtube-search` workflow from `achard-arnaud/search-social-networks`: public-first extraction with `yt-dlp`, English auto-captions, URL/date/method/limitations retained. The full transcripts are not redistributed; this file stores only a bounded synthesis. Auto-captions can mistranscribe names and punctuation, so the review uses them for technique extraction, not historical facts.

| Source | Public extraction | Relevant pattern | Historical adaptation |
|---|---|---|---|
| [Philipp Humm — “Give me 18min…”](https://www.youtube.com/watch?v=YtkrIaONxu0) | English auto-captions; ~3,717 words | PAST: Place, Action, Speech, Thoughts | Retain place/action; replace unsourced speech/thought with Constraint + Evidence (PACE). |
| [Vinh Giang — “The Fastest Way…”](https://www.youtube.com/watch?v=kPlzq2y72UI) | English auto-captions; ~688 words | Practise short, relatable stories repeatedly | Use short sourced vignettes to test clarity and human scale; do not invent a relatable anecdote. |
| [Full storytelling course](https://www.youtube.com/watch?v=epKEXCHjp4M) | English auto-captions; ~16,834 words | CAT; mission/progression/payoff; `but/therefore`; one takeaway; guide-like delivery | Use causal question, minimal context, evidence progression and reflection. Reject manufactured stakes, cliffhangers and retention hacks. |

## Benchmark repositories

### `danjdewhurst/story-skills`

The useful contribution is operational continuity: outline first, story bible, registries, timeline, open promises/questions, post-write updates and deterministic doctor checks. The historical-travel adaptation is the **promise and continuity ledger** plus QA that can fail. Fiction-specific character, worldbuilding and chapter-production mechanics are not copied.

Reference: [danjdewhurst/story-skills](https://github.com/danjdewhurst/story-skills).

### `Zzzeen2552/storytelling-mastery-skill`

The useful contribution is the insistence on disruption, conflict, structure, transformation, emotional truth and concrete demonstration. The adaptation keeps human stakes, disruption and transformation only when evidence supports them. It rejects heroic monocausality, villain framing, a mandatory hero journey, teleology and unverified authority quotations.

Reference: [Zzzeen2552/storytelling-mastery-skill](https://github.com/Zzzeen2552/storytelling-mastery-skill).

## Resulting patterns

- **Short vignette:** PACE — Place, Action, Constraint, Evidence.
- **Side box:** minimal context → tension/adversity → one takeaway, all sourced.
- **Long arc:** causal question → minimal context → mechanisms → `but/therefore` progression → rupture/resolution → reflection/bridge.
- **Continuity:** promise → questions → callbacks → payoff or unresolved label.
- **Voice:** educated, analytical guide speaking to one reader.
- **Safety:** no invented dialogue, thought, motive, sensory detail, stakes or chronology.

## Run24 architecture review — volume and completeness

Purely iterative arc-by-arc drafting is no longer sufficient at current corpus volume. It has four predictable blind spots: a claim can be valid but absent from Graph Light; a bridge can be discovered after its source arc was drafted; candidate composition records can remain outside the active prompt; and an image can name a subsection that does not exist in the canonical manuscript.

The required strategy is:

1. **Global topology pass, low-token** — build `story_scaffold.json` from every claim, bridge, Graph Light edge, side story, recap, question, map and illustration. Consume IDs, counts, roles and status only; do not hydrate full prose.
2. **Human visual check** — inspect `story_scaffold.mmd` for clusters, false links, bridge bottlenecks and unexpected isolation. The Mermaid file is a review surface, not an LLM retrieval payload.
3. **Arc-local drafting** — hydrate one arc's spine claims, adjacent bridges, required/candidate composition records and bounded questions. Draft the causal movement, not a bag of facts.
4. **Cross-arc stitch** — resolve promises, callbacks, chronology and bridge hand-offs after local drafts exist.
5. **Illustration pass** — embed only approved/resolved assets; preserve all other assets in the review queue.
6. **Coverage reconciliation** — every scaffold item must be rendered, explicitly deferred, bounded, retired or left as an open question. Silence is not a state.

Graph Light is a selective relationship layer, not the inventory of truth. The scaffold therefore starts from the complete claim registry and reports graph-orphan claims instead of dropping them. This is essential: a sparse graph may be correct, while a story scaffold built only from graph-connected nodes would be incomplete.

### Token economics

- Global pass: IDs and topology only.
- Draft pass: one arc plus immediate bridge neighbourhood.
- Stitch pass: bridge/callback summaries, not all underlying sources.
- Final pass: hydrate only unresolved coverage debt.

This replaces repeated whole-corpus rereads with deterministic retrieval packs. The gain grows with corpus size while preserving an auditable global view.
