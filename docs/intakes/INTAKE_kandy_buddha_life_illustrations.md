# Intake — Kandy Buddha-life reliefs as illustrations

## Context

Field visit, 2026-08-26, Sri Maha Bodhi Viharaya / Bahirawakanda (the giant Buddha overlooking Kandy). Ten user-supplied photographs document reliefs on the first-floor narrative circuit.

The user hypothesis is substantially correct: much of the circuit is a **visual biography of Siddhattha Gautama / the Buddha**, including birth, the palace crisis, renunciation and awakening. However, the sequence then extends beyond the pan-Buddhist biography into **specifically Sri Lankan sacred-history traditions**, including the first and second visits of the Buddha to Lanka. Those scenes must be captioned as chronicle/temple tradition, not as independently established lifetime itinerary.

## Routing decision

These photographs are registered as composition artefacts with `class: illustration`, not as historical claims. Raw observations live in:

`examples/sri_lanka_pre_1948/00_method/capture/run23_kandy_buddha_illustration_fragments.json`

Reader-facing illustration metadata lives in:

`examples/sri_lanka_pre_1948/09_output/illustrations/ILL-KANDY-BUDDHA-LIFE-2026-08.json`

The original binaries remain external to the repository; filenames and SHA-256 hashes preserve identity. The illustration records therefore use `source.binary_status: external_only`.

## Photo → input → illustration linkage

| Photo | Field input | Illustration | Working identification | Confidence / evidence semantics |
|---|---|---|---|---|
| `1000033394.jpg` | `GF-KANDY-ILL-01` | `ILL-KANDY-01` | Siddhattha awake among sleeping palace women; disillusionment before renunciation | medium — interpretive |
| `1000033395.jpg` | `GF-KANDY-ILL-02` | `ILL-KANDY-02` | one/compressed set of the four sights | medium — interpretive |
| `1000033396.jpg` | `GF-KANDY-ILL-03` | `ILL-KANDY-03` | birth of Prince Siddhattha at Lumbini | high — Buddhist biographical tradition |
| `1000033397.jpg` | `GF-KANDY-ILL-04` | `ILL-KANDY-04` | Great Renunciation / departure on Kanthaka | high — Buddhist biographical tradition |
| `1000033398.jpg` | `GF-KANDY-ILL-05` | `ILL-KANDY-05` | Buddha meditating under a tree; awakening/Bodhi symbolism | medium — iconographic interpretation |
| `1000033399.jpg` | `GF-KANDY-ILL-06` | `ILL-KANDY-06` | forest/ascetic episode unresolved from current angle | low — observation only |
| `1000033400.jpg` | `GF-KANDY-ILL-07` | `ILL-KANDY-07` | narrative scene with robed figure, woman and kneeling elder; unresolved | low — observation only |
| `1000033401.jpg` | `GF-KANDY-ILL-08` | `ILL-KANDY-08` | traditional Nalagiri elephant episode | medium — interpretive/tradition |
| `1000033405.jpg` | `GF-KANDY-ILL-09` | `ILL-KANDY-09` | first visit to Lanka; yakkhas at Mahiyangana | high — **chronicle tradition** |
| `1000033403.jpg` | `GF-KANDY-ILL-10` | `ILL-KANDY-10` | second visit to Lanka; Cūlodara/Mahodara at Nāgadīpa | high — **chronicle tradition** |

## Storytelling requirement

The storytelling skill now runs a dedicated illustration pass **after reader-specific narrative rendering and before the final reread**. It must:

1. preserve the input linkage;
2. distinguish visible object, represented episode, narrative function and epistemic limit;
3. never use an illustration to increase historical confidence;
4. explicitly distinguish the Buddha biography from Sri Lankan chronicle sacred geography;
5. flag unresolved scenes rather than invent an identification;
6. perform the final prose reread only after illustration placement.

## Research / sourcing targets

For later source hardening:

- early Buddhist sources for birth, renunciation and awakening, with the usual distinction between early textual strata and later elaborated biography;
- the Nalagiri episode in Buddhist narrative tradition;
- *Mahāvaṃsa* chapter 1 for the three traditional visits to Lanka, with a historiographic warning that these are part of Sri Lankan sacred history and not independently corroborated as a historical itinerary;
- modern temple provenance for the Bahirawakanda relief cycle itself.
