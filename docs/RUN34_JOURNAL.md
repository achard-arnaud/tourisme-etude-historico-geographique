# Run 34 — journal d’exécution

## 1. Scope et règle de promotion

Run34 a été intégré dans `dev` via PR #80. La fermeture forcée des pendings de sourcing est traitée sur `run34-force-blocked-sourcing`, issue de `dev`, avant promotion finale `dev → main`.

Le run ne décide pas de la création d’un arc Gampola/Kotte/Sitawaka. L’ambiguïté de doublon Abhaya 03/05/08 n’est pas tranchée sans preuve suffisante.

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

## 4. Side stories et reader

### SS-R34-MUDRA-DETOUR-001 — detour

- Ancrage : sous-section `2. Valagamba et Abhayagiri : le Saṅgha n’est pas monolithique`.
- Retour : `C-R16-ABH-DATE-001`, résolution par marqueur réel `[claim:C-R16-ABH-DATE-001]` dans l’artefact instrumenté.
- Gate : état initial mécanique/Sarah/HIL = `false`; `paragraph_review_gate.py` est exécuté par `scripts/qa_run34.py` avant acceptation des états finaux.

### SS-R34-BUDDHIST-ICONOGRAPHY-METHOD-001 — method

- Sources : Snodgrass, Saunders, Coomaraswamy, T1.
- Indépendant des panneaux 7/9/3 et du *Kusa Jātaka*.
- Callback : réutilise `SS-R34-MUDRA-DETOUR-001`.
- Retour : `C-R34-ICON-STUPA-001`, résolu par marqueur réel dans l’artefact instrumenté.

Le reader frontstage reste sans IDs `[claim:*]`; `report_v3_full_run34_instrumented.md` conserve les marqueurs nécessaires à la QA.

## 5. Fermeture forcée de tous les `draft_blocked_pending_sourcing`

Décision utilisateur du 28 août 2026 : fermer tous les pendings de ce statut et finaliser la publication.

### 5.1 Méditation śaiva / bouddhique + Buddha avatāra de Viṣṇu

Le draft `B-R34-CREOLISATION-MEDITATION-DRAFT-001` passe à `resolved_promoted_split`.

Sources T1 admises :
- Gavin Flood, Oxford Handbook — méditation dans les grandes traditions tantriques centrées sur Śiva ;
- Sarah Shaw, Oxford Handbook — méditation Theravāda, incluant Sri Lanka ;
- Bradley S. Clough, *Journal of Hindu Studies* — histoire variable du Buddha comme avatāra de Viṣṇu dans la réception vaiṣṇava.

Artefacts promus :
- `C-R34-FORCE-THERAVADA-MEDITATION-001` ;
- `C-R34-FORCE-SHAIVA-TANTRA-MEDITATION-001` ;
- `C-R34-FORCE-BUDDHA-VISHNU-AVATAR-001` ;
- `B-R34-SHAIVA-BUDDHIST-MEDITATION-001`.

Le terme de « créolisation » n’est **pas** promu comme mécanisme historique : les sources permettent un comparatif de répertoires contemplatifs, pas une preuve de borrowing ou de système doctrinal fusionné. La tradition Buddha-avatāra est conservée comme proposition vaiṣṇava séparée.

### 5.2 « Dieu rouge » Kataragama / Nallur

Le draft `B-R34-RED-GOD-KATARAGAMA-NALLUR-DRAFT-001` passe à `resolved_promoted`.

Sources admises :
- Carl Vadivella Belle, chapitre académique sur Murugan : red symbolism et Ceyon/Seyon, « The Red One » ;
- S. Pathmanathan : complexe sri-lankais Skanda-Murukan/Kataragama ;
- ancres institutionnelles Run29 Kandy/Nallur déjà qualifiées.

Artefacts promus :
- `C-R34-FORCE-MURUGAN-RED-ONE-001` ;
- `B-R34-RED-GOD-KATARAGAMA-NALLUR-001`.

La couleur rouge est un callback historique de nom/généalogie, **pas** un mécanisme rituel démontré commun à la Perahera de Kandy et au festival de Nallur.

### 5.3 Gate ajouté

`scripts/qa_run34.py` exige désormais :
- `pending_count == 0` ;
- aucun statut `draft_blocked_pending_sourcing` ;
- sources non vides sur chaque résolution ;
- bridge promu effectivement présent dans `06_bridges` avec `mechanism` et `bounded_by` ;
- sources forcées T1/T2 ;
- aucune fuite de statut pending dans le reader.

## 6. QA et promotion

Run34 initial : workflow `skill-ci` #608 sur `f162ec7fc81dce9bf7beee1ff5a79d9cf082e974` — SUCCESS. PR #80 a ensuite intégré Run34 dans `dev` au SHA `727a69d698cef1cd40fd0fa67fa0cca52e9b4318`.

La fermeture forcée est soumise à un nouveau CI sur `run34-force-blocked-sourcing`, puis à une PR vers `dev`. Après vert sur `dev`, une PR distincte `dev → main` publiera l’état final. Les SHAs et PRs de publication seront consignés après exécution effective.
