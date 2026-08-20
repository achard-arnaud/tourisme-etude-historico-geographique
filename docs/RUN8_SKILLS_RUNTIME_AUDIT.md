# Run 8 — Revue skills, liens d'orchestration et socle technique

Date : **2026-08-19**. Portée : relecture/optimisation de structure et de lisibilité des
16 sous-skills et de l'orchestrateur `SKILL.md`, de leurs liens vers exemples/artefacts/
contrats d'output et étapes de workflow, plus un audit du socle technique (runtime,
authentification, logs, try/except, typage d'erreurs, mode debug) et une revue de code des
scripts. Le fond méthodologique des skills n'a pas été modifié.

## 1. Résumé exécutif

Le système est solide sur le fond (16 skills, contrats d'artefacts, QA déterministe,
40 tests verts). Les manques identifiés sont structurels et opérationnels, pas
méthodologiques : absence de contrat de sortie explicite dans 15/16 skills, aucun lien
texte entre les sous-skills et `SKILL.md`/les templates, une dépendance runtime
(`python-docx`) non déclarée et jamais exercée en CI, des erreurs envoyées sur stdout au
lieu de stderr, et aucun mode debug. Ce run corrige tout ce qui est mécanique et sans
risque, et documente ci-dessous ce qui reste à trancher.

**Découverte importante à traiter en premier** : voir §6.

## 2. Corrections appliquées dans cette passe

### 2.1 Structure et liens des skills
- **`docs/skill_workflow_index.md`** (nouveau) : table unique skill → étape d'orchestration
  → artefact primaire → template/schéma → consommateur en aval. C'est le point d'entrée
  qui manquait pour répondre à « quelle skill produit quoi, avec quel gabarit, pour qui ».
- **`SKILL.md`** : une ligne ajoutée sous `## Orchestration` pointant vers cet index
  (le fichier reste à 646/650 mots — la marge est désormais quasi nulle, voir §7).
- **15 des 16 sous-skills** (`capturing-field-evidence` et `storytelling-historical-travel`
  avaient déjà un contrat de sortie/QA propre) ont reçu une section **`## Output`** compacte
  énonçant l'artefact produit et le template/chemin cible, dérivée du contenu déjà présent
  dans chaque fichier — aucune règle nouvelle n'a été inventée.
- **Chacune des 16 skills** porte désormais une ligne `See also: SKILL.md orchestration
  step N; docs/skill_workflow_index.md` en fin de fichier — navigation bidirectionnelle
  orchestrateur ↔ skill, absente jusqu'ici.

### 2.2 Socle technique
- **`requirements.txt`** (nouveau) : déclare `python-docx>=1.1,<2`, seule dépendance
  runtime du dépôt, avec commentaire précisant qu'elle ne concerne que le pipeline de
  publication.
- **`.github/workflows/ci.yml`** : ajoute `pip install -r requirements.txt` puis
  `python scripts/render_full_reader_v3.py --project all` comme étape de fumée. La CI ne
  couvrait jusqu'ici que la QA structurelle (tests, audits, `qa_project.py`) — jamais la
  chaîne de rendu DOCX réellement utilisée pour publier. Vérifié localement : la commande
  s'exécute proprement une fois la dépendance installée, sans modifier le Markdown généré
  (seuls les métadonnées internes du `.docx` changent d'un run à l'autre — non commité).
- **`README.md`** : section « Runtime et dépendances » ajoutée ; commande `pip install`
  ajoutée aux deux blocs de vérification (README + `SKILL.md`).

### 2.3 Logs, erreurs, mode debug
- `scripts/audit_skill.py`, `scripts/audit_workflow.py`, `scripts/qa_project.py` :
  tous les messages `ERROR:`/`WARN:` vont désormais sur **stderr** ; seule la ligne de
  statut finale (`SKILL AUDIT OK`, `QA OK: …`) reste sur stdout. Convention CLI standard,
  utile dès qu'un appelant veut distinguer un échec verbeux d'un succès parseable.
- **Mode debug** : variable d'environnement `SKILL_DEBUG=1` ajoutée à `audit_workflow.py`
  et `qa_project.py`. Par défaut, une exception de parsing (JSON/YAML malformé) est avalée
  dans un message `ERROR:` compact ; avec `SKILL_DEBUG=1` elle est re-levée avec sa trace
  complète. Testé manuellement avec un JSON invalide (voir transcript de session) : le
  comportement par défaut ne change pas, le mode debug affiche la trace attendue.

Aucun de ces changements ne modifie une sortie fonctionnelle : 40/40 tests, les deux
audits et les deux QA de projet restent verts après application.

## 3. Audit — skills (structure et lisibilité)

| Constat | Détail |
|---|---|
| Longueur très hétérogène | 19 à 38 lignes pour 14 skills, 73 lignes pour `storytelling-historical-travel` (complexité assumée), aucune limite ailleurs que `SKILL.md` (650 mots, imposé par `audit_skill.py` et un test). Pas un problème en soi, mais aucune skill n'explique pourquoi elle échappe à cette contrainte — à documenter une fois, pas à corriger fichier par fichier. |
| Aucun lien retour vers l'orchestrateur | Corrigé (§2.1). |
| Aucun lien vers `templates/` | Corrigé pour les 9 skills qui produisent un artefact templatable ; les 6 skills d'analyse HIL n'ont pas de template dédié (leur sortie alimente `templates/claim.md`), documenté explicitement dans l'index plutôt que laissé implicite. |
| Aucun renvoi vers `examples/` | **Non corrigé — à trancher.** Aucune skill ne pointe vers `examples/sri_lanka_pre_1948` ou `_post_1948` comme cas travaillé. Le pattern trouvé chez `search-social-networks` est d'éviter les exemples narratifs au profit d'une commande exécutable unique par skill ; ici l'équivalent serait un chemin concret du corpus Sri Lanka illustrant le contrat (ex. un claim réel, un bridge réel). Décision à prendre : vaut-il la peine d'ancrer chaque skill sur un exemple concret, ou l'index (§2.1) suffit-il ? |
| Contrat de sortie absent | Corrigé pour 15/16 skills (§2.1). |
| Étapes de workflow où une skill peut intervenir | Rendu explicite via `docs/skill_workflow_index.md`, qui documente aussi pourquoi les 6 skills d'analyse HIL partagent une seule étape (dispatch sélectif, jamais automatique — cf. `docs/agent_routing.md`). |

## 4. Audit — runtime et socle technique

Ce dépôt **n'est pas une application avec authentification** : c'est un système de
skills Markdown + scripts Python locaux (scaffolding, QA, rendu DOCX), sans serveur,
sans API, sans secret. Le point « authentification » de la demande initiale ne s'applique
donc à rien ici — je le documente plutôt que de forcer un mécanisme qui n'a pas lieu
d'être. Le seul repo comparable qui manipule des secrets est `search-social-networks`
(clés API optionnelles, jamais journalisées, gate `--allow-commercial` explicite) — motif
à réutiliser **si** ce dépôt acquiert un jour un script réseau, pas avant.

Ce qui, en revanche, relevait bien du socle technique et a été trouvé manquant :
- **Dépendance non déclarée** : `render_full_reader_v3.py` et `render_reader_exports.py`
  importent `docx` (`python-docx`) sans qu'aucun fichier du dépôt ne le déclare. Le module
  n'était pas installé dans cet environnement avant cette passe. Corrigé (§2.2).
- **Aucune couverture CI du pipeline de publication** : les 40 tests et les 3 audits ne
  chargent jamais `render_full_reader_v3.py`/`render_reader_exports.py` (vérifié : aucun
  test n'importe ces modules, seuls les fichiers `.docx` déjà générés sont inspectés comme
  des archives ZIP). Une régression dans la génération DOCX ne serait donc détectée qu'au
  rendu manuel. Corrigé en ajoutant l'étape de rendu à la CI (§2.2).

## 5. Audit — logs, try/except, typage d'erreurs, mode debug

- **Logging** : aucun module `logging` nulle part dans `scripts/`, uniquement des
  `print()`. Pour des scripts CLI courts et synchrones exécutés une fois par run CI, ce
  n'est pas un défaut en soi ; le vrai problème était le canal (stdout au lieu de stderr),
  corrigé. Passer à `logging` n'apporterait rien tant qu'il n'y a ni niveaux de verbosité
  différenciés à l'exécution, ni sortie structurée consommée ailleurs — **décision à
  trancher** si un futur script tourne en tâche longue ou consomme ses propres logs.
- **try/except** : 6 blocs, tous `except Exception` génériques plutôt que des exceptions
  typées (`json.JSONDecodeError`, `OSError`). Le choix générique est défendable ici — ces
  scripts transforment systématiquement toute erreur de parsing en message `ERROR:`
  actionnable pour l'auteur du projet, peu importe sa nature exacte — mais il masquait
  jusqu'ici les vraies traces. Le mode `SKILL_DEBUG=1` (§2.3) restaure l'accès à la trace
  sans changer le comportement par défaut.
- **Typage d'erreurs** : aucune exception custom (`class SourceRegisterError(Exception)`,
  etc.) nulle part. Compte tenu du volume (6 sites d'erreur, tous dans des scripts CLI
  courts, jamais importés comme bibliothèque par un tiers), introduire une hiérarchie
  d'exceptions typées serait de la sur-ingénierie actuellement — **à revisiter seulement
  si** ces scripts deviennent une bibliothèque important ailleurs.
- **Mode debug** : absent avant cette passe, ajouté (§2.3), volontairement minimal
  (variable d'environnement plutôt qu'un flag `--debug` par script, pour ne pas toucher au
  parsing positionnel de `sys.argv` déjà en place et casser les appels existants dans la
  CI, les tests et `SKILL.md`).

## 6. Découverte critique — divergence de branche sur `storytelling-historical-travel`

Le message reçu contenait un fichier joint (`SKILL_1.md`) présenté comme la version
courante de la skill storytelling, avec les gates de couverture de sources, le
zettelkasten de fragments, la charte de couleurs à 6 encarts, etc. **Ce contenu n'est pas
celui présent dans ce dépôt cloné depuis `origin`** : la version réellement présente sur
`origin/main` (et donc sur la branche de travail de cette session) est encore la version
« Run 6 » (73 lignes, sans gates de couverture ni zettelkasten de fragments).

Le message de statut joint le confirme explicitement : *« main local : fusionné par
fast-forward, 7 commits devant origin/main — aucun push effectué »*. Le travail de refonte
V3/V4 (commits `3cfa8e5`, `acefa94`) existe donc dans une session Codex locale distincte,
jamais poussée vers `origin`. Cette session n'y a pas accès et ne peut ni le vérifier ni
le fusionner.

**Conséquences pratiques :**
1. Les correctifs structurels appliqués ici à `skills/storytelling-historical-travel/SKILL.md`
   (§2.1) portent sur la version Run 6 réellement présente dans ce dépôt, pas sur la
   refonte décrite dans le feedback. Ils devront être réappliqués (ou vérifiés comme déjà
   couverts) une fois cette refonte poussée.
2. **Rien dans le feedback storytelling n'a été traité comme une instruction à exécuter
   dans cette session** — il s'agit d'arbitrages déjà actés et commités ailleurs par
   Codex, hors du fond que cette passe devait laisser intact.
3. **À trancher en priorité** : la session Codex doit pousser ses 7 commits vers
   `origin/main` (ou une branche dédiée) pour que ce travail existe hors d'un poste local
   et redevienne auditable/mergeable. Tant que ce n'est pas fait, deux versions du même
   OS de skills évoluent en parallèle sans convergence possible.

## 7. Patterns empruntés aux deux dépôts de référence

### `achard-arnaud/search-social-networks`
- Contrat de sortie en langage clair (`## Sortie attendue`) adossé à une structure
  (`Result`/`SourceRun`) qui porte exactement les mêmes champs — le contrat est
  vérifiable, pas seulement déclaratif. Pattern repris ici via `## Output` (§2.1), en
  version allégée car ce dépôt n'a pas de dataclass équivalente à faire correspondre.
- Erreurs capturées comme **champs typés** plutôt que comme crashs (`SourceRun(...,
  "error", ..., f"{type(exc).__name__}: {exc}", ...)`) et code de sortie reflétant l'état
  global. Directement transposable si `qa_project.py`/`audit_workflow.py` devaient un jour
  exposer un résumé JSON en plus des lignes `ERROR:`.
- Sous-commande `--doctor` qui rapporte l'état de l'environnement (dépendances présentes,
  clés configurées — jamais leur valeur) sans rien exécuter d'autre. **Candidat direct**
  pour ce dépôt : un `--doctor` sur `qa_project.py` ou un script dédié qui vérifierait
  `python-docx` installé, structure `05_sources/` présente, etc. Non implémenté dans cette
  passe (périmètre : structure/lisibilité, pas nouvelle fonctionnalité) — proposé en §8.
- Gestion des clés API : variable d'environnement, jamais journalisée, gate explicite
  (`--allow-commercial`). Sans objet ici tant qu'aucun script ne fait d'appel réseau
  (cf. §4).

### `achard-arnaud/skills-sdlc-superpower`
- `profiles/ai-maturity-diagnostic/PROFILE.md` + `loop.yaml` : séquence numérotée
  d'étapes, chacune avec `id`, `skill`, `required_outputs`, `gate`. C'est exactement le
  manque identifié en §3 (« étapes du workflow où une skill peut intervenir ») — modélisé
  ici avec `docs/skill_workflow_index.md`, en plus léger car ce dépôt route les skills
  dynamiquement (`docs/agent_routing.md`) plutôt que par séquence fixe.
- `stop_conditions` (ex. `hard_gate_bypassed`, `execution_claim_without_executor`) :
  pattern d'échec explicite par étape. Ce dépôt a un équivalent partiel via
  `scripts/audit_workflow.py` (statuts `executed`/`verified` obligatoires, raisons de
  dispatch/skip obligatoires) mais rien d'aussi nommé pour un abus du type « skill
  marquée exécutée sans artefact vérifiable ». `audit_workflow.py` couvre déjà ce cas
  précis (`missing output evidence for {name}`), donc le pattern est déjà appliqué en
  substance sous un autre nom.

## 8. Décisions à trancher (liste priorisée)

1. **Pousser la refonte storytelling Codex vers `origin`** (§6) — bloquant pour toute
   convergence ultérieure ; sans ça, cette session et Codex continuent de diverger.
2. **Exemples ancrés par skill** (§3) : ajouter un chemin concret d'`examples/` à chaque
   skill, ou considérer que l'index suffit ?
3. **`--doctor` / self-check d'environnement** (§7) : vaut-il la peine d'ajouter un script
   qui vérifie `python-docx`, la structure de projet et les registres avant un run long,
   plutôt que de découvrir un `ModuleNotFoundError` en cours de publication ?
4. **Marge du budget de mots de `SKILL.md`** : à 646/650 mots, la marge est quasiment
   épuisée. Toute future addition à l'orchestrateur nécessitera de couper ailleurs — faut-il
   desserrer la limite (actuellement en dur dans `audit_skill.py` et un test), ou déplacer
   davantage de contenu vers `docs/` comme cela vient d'être fait pour l'index ?
5. **Passage à `logging`** : à envisager seulement si un script tourne en tâche longue ou
   si une sortie structurée (JSON) devient nécessaire en plus des lignes `ERROR:`/`WARN:`.

## 9. Vérification exécutée

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v      # 40/40 OK
python scripts/audit_skill.py .              # SKILL AUDIT OK (646/650 mots)
python scripts/audit_workflow.py docs/RUN7_WORKFLOW_MANIFEST.json   # OK
python scripts/qa_project.py examples/sri_lanka_pre_1948   # OK, 0 warning
python scripts/qa_project.py examples/sri_lanka_post_1948  # OK, 0 warning
python scripts/render_full_reader_v3.py --project all      # OK, rétention 110.2%/163.7%
```

Testé manuellement : `SKILL_DEBUG=1` restaure la trace complète sur un JSON malformé sans
changer le comportement par défaut (§2.3). Les `.docx` régénérés localement pour ce test
n'ont pas été commités — seules leurs métadonnées internes changent d'un run à l'autre,
le Markdown produit est identique.
