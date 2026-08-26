---
name: storytelling-historical-travel
description: Use when a validated historical manuscript must be rendered for a specific reader profile, reading context, language, depth, tone, register, or approved illustration set without changing evidence or composition contracts.
---

# Storytelling historical travel

The skill has two deliberately separate layers. **Backstage process** governs evidence, coverage, graph topology, drafting and QA. **Frontstage voice** governs what the reader actually reads. Backstage metadata is never reader-facing prose.

# Part I — Backstage process

## 1. Topology before prose
Consume deterministic `09_output/story_scaffold.json` before `09_output/reader_plan.json`. The scaffold is the compact global projection of arcs, spine claims, bridges, questions and composition queues. Do not hydrate the full corpus in one prompt: load the scaffold globally, then only the active arc, adjacent bridges and required composition records.

The reader plan carries audience, language, content temperature, story template, side-story priority, recap style, map policy and illustration selection. Do not choose eligibility ad hoc.

Profiles include advanced/historian enthusiast, intermediate/educated generalist and child 10+. Content temperature is density/variety, not model sampling.

## 2. Run journal — append only
Every run owns `docs/RUN<N>_JOURNAL.md`. It is an append-only execution ledger. Each meaningful step records timestamp, trigger, artefacts touched and cross-consistency result before the next step. Never rewrite or compact earlier entries. This ledger is L0 process evidence and must never be copied into the reader.

Scripts that create transition artefacts should append their result through `scripts/run_journal.py` when a run number is supplied.

## 3. Graph ↔ outline heat map
Before drafting, `scripts/build_heat_map.py` maps graph degree against the scaffold outline. It is L0 and diagnostic only:
- **hot**: average claim degree above global mean + one standard deviation;
- **cold**: average degree <= 1;
- **normal**: between the two;
- **unmapped**: an outline subsection has no explicit claim assignment yet.

The heat map is a prioritization report, never a blocking evidence gate. Do not infer narrative importance from degree alone.

## 4. Reciprocal coverage after scaffold
Run `scripts/reciprocal_coverage_check.py` before paragraph drafting and again before final reconciliation. It checks explicit claim markers, fragment lineage, side-story/spine overlap and density signals without LLM calls.

### Explicit traceability and legacy state
`[claim:<id>]` is the evidentiary insertion marker. New or rewritten paragraphs governed by this skill must preserve it in canonical Markdown, hidden from reader-facing DOCX where applicable. Legacy prose without claim markers is **unknown coverage**, not automatically unused. Never manufacture a false 100% gap report from uninstrumented legacy text.

### Citation count and callback preference
The first `[claim:<id>]` records direct evidentiary insertion. Before a second citation of the same claim, check for an active callback in the arc. If a callback already carries the fact, prefer that narrative callback. More than two direct citations is a review signal; a third citation is rejected when an active callback is available.

Callback continuity follows **promise → question → callback → payoff**. A callback is a light narrative reprise, not another proof-bearing insertion.

### Density is a signal, not a hard gate
Compare source volume (claim + linked fragment) with rendered paragraph volume. A large contraction warns of compression/meta-summary; a large expansion warns of stylistic padding. Neither direction blocks by itself. Narrative necessity and evidence fidelity remain primary.

### Side-story overlap and placement
A claim already carried by the main spine of a subsection must not become the sole evidence base of a side story in that same subsection unless a distinct angle is demonstrable. Use explicit lineage overlap first; entity overlap with the immediate narrative neighborhood is an additional placement signal, not a substitute for evidence review.

### Illustration placeholders
Apply the same reranking discipline to proposed external-image placeholders: at most 1–2 per subsection, and only when a concrete didactic contribution is stated. The actual external-image rights/search and visual embedding pipeline remains a separate dependency.

## 5. Paragraph writing loop
Trigger this loop when a side story is created, a claim is added, or an item enters `coverage_gaps_run<N>.json`.

1. **L0** — load the source claim/fragment, its canonical points if available, and adjacent claims/bridges in the arc. Never load the full manuscript.
2. **L2 bounded** — load only the previous and next paragraph of the same subsection for continuity.
3. **L0** — check active callbacks before adding another direct `[claim:<id>]` citation.
4. **LLM** — draft/rewrite according to Part II.
5. **L1** — run `scripts/paragraph_review_gate.py` and the checklist in `references/paragraph_review_checklist.md`.
6. **L0** — append the result to the run journal and refresh reciprocal coverage.

If the paragraph fails the gate, rewrite the whole paragraph. Do not patch only the failing phrase while leaving a structurally weak paragraph intact.

## 6. Historical nonfiction gate
PACE remains useful backstage: Place → source-attested Action → Constraint → Evidence. Never add invented dialogue, thoughts, motives, composite characters, sensory facts or false suspense. Use but/therefore transitions while preserving evidence state.

## 7. Composition invariants
A side story's kind, lineage, required status and reader eligibility come from artefacts/profile. `analytical_focus` preserves at minimum its **question → thesis → contrasted positions/caveats → mechanisms/evidence status → callback → payoff**. Storytelling may simplify language or reorder cards for the target reader; it may not flatten the focus into a generic anecdote, upgrade an inference, or rewrite a contested binary as fact.

Arc recaps may be simplified in wording but not causally rewritten. Only `human_approved` map assets are eligible, at most one per subsection or side-story slot. Hidden composition IDs remain traceable in canonical Markdown but not reader-facing.

## 8. Length policy
For advanced work there is no maximum length. Start from complete baseline/canonical state, treat later inputs as deltas unless proven complete, and apply content-preservation gates. Intermediate/child may be shorter only under explicit profile/template rules.

## 9. Dedicated illustration pass
After narrative rendering and before the final reread, load `09_output/illustrations/*.json` through the illustration contract.

1. consider only `reader_eligible` illustrations for actual embedding;
2. require at least one resolvable `input_ref`;
3. preserve `observed_caption`, `canonical_text`, `chronicle_tradition`, `interpretive` semantics;
4. use **depicts / represents / temple tradition presents**, never language that upgrades a field photo into historical proof;
5. place an image only when it reduces reader effort or clarifies a distinction;
6. caption as useful through visible content → represented episode/theme → relevance → epistemic limit;
7. never silently harmonize image, local caption and manuscript disagreement;
8. `source.binary_status=external_only` means planning/traceability only, not pretend embedding;
9. require `placement.target_status=resolved` for selection;
10. preserve `[ILLUSTRATION:<id>]` exactly once for each selected illustration.

For Sri Lankan sacred-history scenes, preserve the distinction between depictions of the Buddha's life and later chronicle traditions placing the Buddha physically in Lanka.

## 10. Final reread
Run the final prose reread after illustration placement. Check chronology, transitions, paragraph referents, source semantics, callback closure, observation/tradition/history distinctions and reciprocal scaffold coverage.

# Part II — Frontstage voice

## Voix narrative
Le lecteur reste dans une continuité historico-géographique vivante. Aucune trace de l'appareil de production — versions, runs, HIL, ancres, statuts ou procédé de construction — n'apparaît dans le texte lu. La preuve et l'incertitude vivent dans la phrase, jamais dans un habillage méthodologique adjacent.

### Do
- Raconter le fait avant sa perspective ou sa conséquence : **lieu → action attestée → mécanisme → ce qui en découle**.
- Nommer l'incertitude en clause naturelle : « la tradition du temple veut que… », « les textes les plus anciens ne disent que… ».
- Reprendre tous les points du résumé canonique interne du claim source quand il existe ; aucun point établi ne disparaît à la réécriture.
- Mettre en valeur la texture concrète de l'input brut : lieu précis, date, nom, objet, geste ou institution — pas seulement sa conclusion.
- Préférer une phrase longue et respirée lorsque le lien causal l'exige, sans empiler le jargon.
- Développer toute abréviation ou tout sigle au premier usage.
- Gloser ou franciser tout terme technique étranger dans un texte français ; par exemple *clearing house* devient « chambre de compensation » ou est expliqué au premier usage.
- Préférer un callback narratif à une nouvelle citation évidentielle quand un fait est déjà noué ailleurs dans l'arc.

### Don't
- Aucun intitulé méthodologique dans le corps du texte, notamment : « TL;DR », « Statut canonique », « Ce qu'on ne doit pas en déduire », « Pourquoi l'insérer directement dans notre arc ? ».
- Aucun tableau d'ancres numérotées ou libellé HIL dans le récit.
- Aucune phrase commentant la version, le run ou le processus d'écriture.
- Aucun tableau de synthèse lorsqu'une phrase narrative porte la même information.
- Aucune liste à puces méthodologique séparée de la prose : les enjeux deviennent des phrases du récit.

## Fausses pistes — format socratique léger
Reranker obligatoirement : **1 à 2 fausses pistes maximum par sous-section**, choisies pour leur lien direct avec le fil et leur intérêt didactique. Écarter les hors-sujets même séduisants.

Le contenu prend la forme d'une question naïve ou semi-rhétorique suivie de sa réponse dans le même bloc. Le renderer visuel peut matérialiser ce bloc en pastel jaune pâle ; le Markdown canonique doit conserver une structure stable et identifiable sans dépendre d'une couleur pour porter le sens.

La même limite de 1–2 par sous-section s'applique aux placeholders d'illustration proposés.

## Schémas et frises
Un schéma Mermaid n'illustre qu'un mécanisme complexe qui résiste réellement à la prose : usage rare. Il est rendu en image avant insertion ; si sa largeur dépasse 120% de la largeur utile, il doit être régénéré verticalement.

Les frises récapitulatives sont encouragées en ouverture/transition et en conclusion des parties de premier niveau. Elles servent de repère inductif et ne remplacent jamais le développement causal principal.

## Child 10+
Use `templates/storytelling/child_10_plus.md`. An `analytical_focus` remains eligible, but decompose it around an observable object/place, protagonist/institution, documented action and a simple because→therefore mechanism before the callback. Complexity is staged, not deleted. Illustrations may be more frequent when they materially aid comprehension, but uncertainty and tradition-vs-history semantics remain mandatory.

# QA contract
The paragraph gate reference is `references/paragraph_review_checklist.md`. Tests must include both conforming and non-conforming fixtures. A positive-only gate test is insufficient.

Before export verify: scaffold coverage, chronology, source-attested action, reader-plan compliance, side-story retention, analytical-focus evidence semantics, recap closure, map approval/limit, illustration lineage/status/epistemic captioning, callback preference, frontstage/backstage separation, final post-illustration continuity and baseline retention.
