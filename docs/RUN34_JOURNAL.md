# Run 34 — journal d’exécution

## 1. Scope et règle de promotion

Branche de travail : `run34-mudra-sasana-backlog`, issue de `dev`.

Chaîne imposée : `run34-mudra-sasana-backlog → dev → main`. Aucun saut direct feature → main.

Le run ne décide pas de la création d’un arc Gampola/Kotte/Sitawaka. Les deux bridges exploratoires restent bloqués sans sourcing T1/T2 explicite. L’ambiguïté de doublon Abhaya 03/05/08 n’est pas tranchée sans preuve suffisante.

## 2. Fragments mudrā et illustrations

- `GF-MUDRA-01..08` : enregistrés comme `iconographic_observation`, `promotes_to:""`; aucune promotion en claim.
- `ILL-MUDRA-2026-08` : 8 illustrations, `source.binary_status=external_only`, `human_review.status=pending`.
- `ILL-MUDRA-04` : `depiction.evidence_status=interpretive`; Bhūmisparśa reste proposé, non établi par plaque visible.
- `ILL-MUDRA-03/05/08` : trois vues Abhaya conservées avec ambiguïté de doublon explicitement non résolue ; aucune déduplication arbitraire.

## 3. Décisions explicites sur le backlog MIH / ABH

| Fragment | Décision | Qualification | Cible | Motif borné |
|---|---|---|---|---|
| GF-MIH-01 | promote_to_claim | chronicle_tradition | C-R34-MIH-COUNCIL-TRAD-001 | La stèle moderne atteste la transmission de la séquence chroniquée, pas la vérification indépendante des événements antiques. |
| GF-MIH-03 | promote_to_claim | chronicle_tradition | C-R34-MIH-AMBAS-TRAD-001 | L’inscription de terrain suffit pour enregistrer le récit Poson/Ambasthala comme tradition transmise. |
| GF-MIH-04 | promote_to_claim | chronicle_tradition | C-R34-MIH-MAHAVIHARA-TRAD-001 | La stèle porte une tradition de fondation/ordination ; l’épigraphie tardive reste distincte de l’événement ancien. |
| GF-MIH-05 | promote_to_claim | chronicle_tradition | C-R34-MIH-BODHI-BHIKKHUNI-TRAD-001 | La séquence Thuparama/Sanghamitta/Bodhi/bhikkhuni est conservée explicitement comme tradition transmise. |
| GF-MIH-06 | promote_to_claim | chronicle_tradition | C-R34-MIH-RELIC-STUPA-TRAD-001 | L’inscription atteste une tradition commémorative et sa convention chronologique, non une datation archéologique indépendante. |
| GF-MIH-09 | promote_to_claim | source_fact | C-R34-MIH-CROWD-METRIC-001 | La date 2024 est directement inscrite ; le chiffre ~100 000 reste attribué au texte de commande, non traité comme mesure d’affluence. |
| GF-ABH-02 | promote_to_claim | source_fact | C-R34-ABH-SIGNIFICANCE-QUOTE-001 | Le superlatif reste une déclaration attribuée au responsable du projet de fouille. |
| GF-ABH-04 | promote_to_claim | source_fact | C-R34-ABH-ANALYSIS-INTENT-001 | L’annonce atteste une intention d’analyse/publication, pas leur achèvement. |
| GF-ABH-06 | promote_to_claim | source_fact | C-R34-ABH-TRANSBUDDHIST-FRAME-001 | Le cadrage de l’annonce est enregistré comme fait de source sans fermer l’interprétation doctrinale. |

Aucun des neuf fragments n’a de troisième statut implicite.

## 4. Side stories

### SS-R34-MUDRA-DETOUR-001 — detour

- Ancrage : sous-section `2. Valagamba et Abhayagiri : le Saṅgha n’est pas monolithique`, précédée dans le patch lecteur d’un paragraphe sur les dix-sept statues du Bouddha découvertes à Abhayagiri.
- Retour : `C-R16-ABH-DATE-001`, résolution exigée par marqueur réel `[claim:C-R16-ABH-DATE-001]` dans l’artefact instrumenté.
- Gate : état initial mécanique/Sarah/HIL = `false`; `paragraph_review_gate.py` est exécuté par `scripts/qa_run34.py` avant que les trois états finaux soient acceptés à `true`.

### SS-R34-BUDDHIST-ICONOGRAPHY-METHOD-001 — method

- Sources : Snodgrass, Saunders, Coomaraswamy, toutes enregistrées T1 comme monographies académiques.
- Ne dépend pas de l’identification des panneaux 7/9/3 ni du *Kusa Jātaka*.
- Callback : réutilise `SS-R34-MUDRA-DETOUR-001`.
- Retour : `C-R34-ICON-STUPA-001`, résolution exigée par marqueur réel `[claim:C-R34-ICON-STUPA-001]` dans l’artefact instrumenté.

### Séparation reader / QA instrumentée

La finalisation reader supprime volontairement les identifiants techniques `[claim:*]`. Run34 matérialise donc :

1. `report_v3_full.md` : reader frontstage propre, sans IDs de claims ;
2. `report_v3_full_run34_instrumented.md` : copie de QA avec les marqueurs réels nécessaires aux contrôles de retour et de couverture.

Cela évite le faux-vert « l’ID du claim existe donc le retour est résolu » sans exposer les identifiants techniques au lecteur.

## 5. Bridges explicitement bloqués

- `B-R34-CREOLISATION-MEDITATION-DRAFT-001` : `draft_blocked_pending_sourcing`, `source_ids: []`, aucun `mechanism`, aucun texte lecteur.
- `B-R34-RED-GOD-KATARAGAMA-NALLUR-DRAFT-001` : `draft_blocked_pending_sourcing`, `source_ids: []`, aucun `mechanism`, aucun texte lecteur.

Le second n’hérite pas automatiquement du sourcing du bridge Run29 déjà borné sur la divinité partagée.

## 6. QA et promotion

### Gate feature → dev

Commandes intégrées au CI :

- `python scripts/qa_run34.py`
- suite CI complète du repo
- `python scripts/render_composed_reader.py --project all`
- `python scripts/qa_run34.py --post-render`

Le post-render exige : retours marker-first résolus, aucun bridge bloqué dans le reader, aucun `[claim:*]` visible dans le reader frontstage, fill continu et bordure finale sur les deux encadrés DOCX.

**Résultat de référence avant journal final :** workflow GitHub Actions `skill-ci` Run `#608`, run id `33155080886`, sur SHA `f162ec7fc81dce9bf7beee1ff5a79d9cf082e974` : **SUCCESS**. La suite unitaire complète, `qa_run34.py`, la couverture réciproque Run34, le build composé `--project all` et `qa_run34.py --post-render` ont tous passé. Les artefacts complets ont été publiés par le workflow.

Le présent commit de journal est postérieur à ce SHA et doit donc repasser la même CI avant ouverture de la PR feature → dev.

### Gate dev → main

Après merge feature → dev seulement : build complet pré-1948, couverture complète du corpus selon le contrat Run27, puis seconde PR distincte `dev → main`. Le présent journal sera mis à jour avec les PRs, SHAs et résultats effectifs avant publication finale.
