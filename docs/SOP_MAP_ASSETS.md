# SOP — Historical map assets

State machine: `candidate → vision_validated → human_approved → retired`.

1. Search online only for an arc or `side_story` with `map_eligible=true`.
2. Capture exact image/source URL, publisher, rights, retrieval date and language; save image locally.
3. Vision gate: geography, historical scope/date, label legibility, obvious anachronism.
4. Submit the image and vision note to a human. No automatic approval.
5. After approval, record historical `map_date`/precision and fragment caption (`what_it_shows`, `why_here`, `limits`).
6. Reader-plan resolver accepts only `human_approved` assets and chooses max one per subsection/side-story slot.
7. Default map language is document language; English is allowed fallback.
