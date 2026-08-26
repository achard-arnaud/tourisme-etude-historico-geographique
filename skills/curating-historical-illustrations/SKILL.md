---
name: curating-historical-illustrations
description: Use when field photos or other images should become reader-facing illustrations linked to existing inputs without being promoted into historical proof.
---

# Curating historical illustrations

## Contract
`illustration` is a composition asset, not a claim class. It may point to an intake, field fragment, claim, bridge, side story or arc. The image can illustrate an already supported proposition or document a modern representation, but it **never upgrades confidence** and never substitutes for sourcing.

Each record uses `templates/illustration.json` and lives in `09_output/illustrations/`.

## Field-photo rule
For user-supplied photos preserve filename, SHA-256, capture context/location, visible caption where legible, and uncertainty. Keep the binary status explicit. If the repository does not contain the binary, use `external_only`; storytelling may still use the metadata/caption but must not pretend the image is embedded.

## Depiction semantics
Always distinguish:
- `observed_caption`: what the photographed temple/museum itself labels;
- `canonical_text`: scene securely identified from an early/canonical Buddhist source;
- `chronicle_tradition`: Sri Lankan chronicle or temple tradition, including legendary visits of the Buddha to Lanka;
- `interpretive`: iconographic identification inferred from the scene.

Write captions with **depicts / represents / temple tradition presents**, not **proves**, unless the image itself is the historical object under study.

## Placement
Attach every illustration to at least one existing input path or ID. Prefer one illustration where it materially improves comprehension of a scene, object, geography or doctrinal distinction. Avoid decorative repetition.

## Review sequence
1. preserve field photo and provenance;
2. identify visible scene/caption with confidence and uncertainty;
3. link to source inputs and evidence status;
4. write caption, what-it-shows, why-here and limits;
5. explicit human approval before `reader_eligible`;
6. hand off to `storytelling-historical-travel` for the dedicated illustration pass before final reread.
