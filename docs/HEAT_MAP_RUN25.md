# Heat map — Run 25

Projet : `sri_lanka_pre_1948`

Diagnostic L0 uniquement. `hot/cold` indique la connectivité du graphe, pas l'importance historique intrinsèque.
Les sous-sections sans `claim_ids` restent `unmapped` : le script refuse d'inventer un mapping à partir des seuls titres.

Degré moyen global : **0.284** — écart-type : **0.568** — seuil hot : **0.852**

| Section | Niveau | Claims mappés | Degré moyen | Statut |
|---|---:|---:|---:|---|
| A01 — Settlement and early polity | 1 | 0 | — | unmapped |
| Entry rupture | 2 | 0 | — | unmapped |
| Causal question | 2 | 0 | — | unmapped |
| Exit rupture / bridge forward | 2 | 0 | — | unmapped |
| Shell guardrail | 2 | 0 | — | unmapped |
| A02 — Ancient Indian Ocean exchange | 1 | 9 | 0.00 | cold |
| A02b — Anuradhapura hydraulic order | 1 | 0 | — | unmapped |
| Entry rupture | 2 | 0 | — | unmapped |
| Causal question | 2 | 0 | — | unmapped |
| Exit rupture / bridge forward | 2 | 0 | — | unmapped |
| Shell guardrail | 2 | 0 | — | unmapped |
| A02c — Anuradhapura, Mihintale and the Mahavihara | 1 | 11 | 0.45 | cold |
| Causal question | 2 | 0 | — | unmapped |
| Evidence rule | 2 | 0 | — | unmapped |
| Run16 state | 2 | 0 | — | unmapped |
| Run24 — reliefs de Bahirawakanda et couches textuelles | 2 | 0 | — | unmapped |
| A03 — Indian Ocean and regional systems | 1 | 0 | — | unmapped |
| Entry rupture | 2 | 0 | — | unmapped |
| Causal question | 2 | 0 | — | unmapped |
| Exit rupture / bridge forward | 2 | 0 | — | unmapped |
| Shell guardrail | 2 | 0 | — | unmapped |
| A04 — Chola interlude and Polonnaruwa | 1 | 4 | 0.25 | cold |
| Entry rupture | 2 | 0 | — | unmapped |
| Causal question | 2 | 0 | — | unmapped |
| Evidence slice in Run 14 | 2 | 0 | — | unmapped |
| Exit rupture / bridge forward | 2 | 0 | — | unmapped |
| Partial guardrail | 2 | 0 | — | unmapped |
| A05 — Colonial conservation and the 1937 ordinance | 1 | 4 | 0.00 | cold |
| A05b — Dry-zone collapse and mobile capitals | 1 | 0 | — | unmapped |
| Entry rupture | 2 | 0 | — | unmapped |
| Causal question | 2 | 0 | — | unmapped |
| Exit rupture / bridge forward | 2 | 0 | — | unmapped |
| Shell guardrail | 2 | 0 | — | unmapped |
| A06 — VOC coastal state | 1 | 2 | 0.00 | cold |
| Entry rupture | 2 | 0 | — | unmapped |
| Causal question | 2 | 0 | — | unmapped |
| TL;DR | 2 | 0 | — | unmapped |
| Drivers / amplifiers / consequences / non-causes | 2 | 0 | — | unmapped |
| What changes the optimum? | 2 | 0 | — | unmapped |
| Exit rupture / bridge forward | 2 | 0 | — | unmapped |
| A06b — Portuguese maritime violence | 1 | 0 | — | unmapped |
| Entry rupture | 2 | 0 | — | unmapped |
| Causal question | 2 | 0 | — | unmapped |
| Exit rupture / bridge forward | 2 | 0 | — | unmapped |
| Shell guardrail | 2 | 0 | — | unmapped |
| A07 — European wars and regional reordering | 1 | 4 | 0.00 | cold |
| Entry rupture | 2 | 0 | — | unmapped |
| Causal question | 2 | 0 | — | unmapped |
| TL;DR | 2 | 0 | — | unmapped |
| Drivers / amplifiers / consequences / non-causes | 2 | 0 | — | unmapped |
| What changes the optimum? | 2 | 0 | — | unmapped |
| Exit rupture / bridge forward | 2 | 0 | — | unmapped |
| A07b — Kandyan kingdom and the defensive interior | 1 | 21 | 0.62 | cold |
| Causal spine | 2 | 0 | — | unmapped |
| Findings closed in Run17 | 2 | 0 | — | unmapped |
| Run18 field detour — invasion and defence | 2 | 0 | — | unmapped |
| Findings deliberately not closed | 2 | 0 | — | unmapped |
| Run23 museum-personage qualification | 2 | 0 | — | unmapped |
| A07c — Coffee collapse and tea conversion | 1 | 6 | 0.00 | cold |
| Causal question | 2 | 0 | — | unmapped |
| Gate | 2 | 0 | — | unmapped |
| A08 — Jaffna caste and colonial codification | 1 | 3 | 0.00 | cold |
| Entry rupture | 2 | 0 | — | unmapped |
| Causal question | 2 | 0 | — | unmapped |
| TL;DR | 2 | 0 | — | unmapped |
| Drivers / amplifiers / consequences / non-causes | 2 | 0 | — | unmapped |
| What changes the optimum? | 2 | 0 | — | unmapped |
| Exit rupture / bridge forward | 2 | 0 | — | unmapped |
| A09 — British unification and the 1833 administrative order | 1 | 0 | — | unmapped |
| Entry rupture | 2 | 0 | — | unmapped |
| Causal question | 2 | 0 | — | unmapped |
| Exit rupture / bridge forward | 2 | 0 | — | unmapped |
| Shell guardrail | 2 | 0 | — | unmapped |
| A09b — Plantation labour system | 1 | 3 | 0.00 | cold |
| Causal question | 2 | 0 | — | unmapped |
| TL;DR | 2 | 0 | — | unmapped |
| Separations | 2 | 0 | — | unmapped |
| Candidate mechanisms to test | 2 | 0 | — | unmapped |
| Required evidence before promotion | 2 | 0 | — | unmapped |
| Exit rupture / bridge forward | 2 | 0 | — | unmapped |

## Lecture
- **hot** : degré moyen > moyenne globale + 1 écart-type ; priorité sur `cold` si les seuils se chevauchent.
- **cold** : hors zone hot, degré moyen <= 1 ; zone orpheline ou quasi-orpheline à inspecter.
- **unmapped** : section présente au scaffold sans mapping explicite de claim ; dette de structuration, pas preuve d'absence de matière.
