# Run 26 — Delta Sarah voice vs spécification Run 25

## TL;DR

L’implémentation Run 26 initiale avait bien séparé la revue Sarah du checklist mécanique, mais elle restait trop déclarative : `passed=true` + une liste de noms de marqueurs suffisait. Elle avait également élargi trois marqueurs distinctifs de la spec en huit préférences plus génériques et attribué au profil plusieurs provenances que le repo ne pouvait pas auditer.

Le patch rend la voix **figée hors runtime**, explicite la provenance réellement disponible, supprime la double source de vérité et lie chaque revue Sarah au texte exact + au contrat exact + à une passe de revue distincte.

## Écarts constatés et résolution

| Sujet | Implémentation avant patch | Exigence Run 25 | Résolution Run 26 |
|---|---|---|---|
| Artefact de voix | `narrative_voice_sarah.md` | `sarah_voice_markers.md`, sortie figée Partie 0 | nouveau `sarah_voice_markers.md` devient source unique ; ancien fichier déprécié |
| Provenance primaire | plusieurs sources présentées comme consolidées | mémoire exportée de l’autre IA comme source primaire ; signaler si inaccessible | source primaire marquée `not_imported`; aucune provenance non auditée n’est revendiquée |
| Runtime | la skill pouvait simplement citer un profil déjà écrit, mais le contrat n’interdisait pas assez explicitement la recollecte | aucune recherche/recollecte au runtime | interdiction explicite dans `SKILL.md` et contrat statique hashé |
| Marqueurs | 8 marqueurs, plusieurs génériques | peu de marqueurs réellement discriminants | 3 axes centraux conservés : portée exacte ; ouverture vécue+callback quand applicable ; rigueur comprimée dans la phrase ; 2 marqueurs de soutien seulement |
| Social format | exclusions documentées | ne pas transférer mécaniquement LinkedIn | marker négatif `continuous_prose_not_social_format` toujours évalué |
| Gate Sarah | `passed=true`, `evaluator`, `markers=[...]` | jugement indépendant, distinct du passage générateur | `generation_pass_id != review_pass_id` et context IDs distincts |
| Stale review | une revue pouvait survivre à une réécriture | réécriture => état false et nouvelle revue | hash du paragraphe exact obligatoire ; toute modification invalide la revue |
| Voice drift | marqueurs hardcodés dans Python | Partie 2 cite un résultat figé de Partie 0 | marker IDs chargés depuis le contrat Markdown machine-readable, plus de liste Python parallèle |
| Contract drift | aucune liaison à la version de voix | révision explicite uniquement | `voice_contract_id` + SHA-256 du fichier obligatoires ; modification du contrat invalide les revues |
| Marker box-ticking | deux noms de marqueurs suffisaient | style non réductible à un compte | résultats structurés `pass/fail/not_applicable` + justification par marker ; les deux markers signature sont toujours explicitement évalués |
| Portée | `scope_precision` déjà obligatoire | précision jamais sacrifiée | conservée comme marker mandatory hard-gated |

## Contrat de voix retenu

### Core obligatoire

`scope_precision` — qui, où, quand, portée et niveau d’incertitude restent exacts, même si la phrase devient plus ample.

### Signature 1

`lived_opening_callback` — lorsqu’une matière de terrain vécue existe et que l’unité ouvre une séquence, elle fournit la prise d’entrée et peut être rappelée ensuite. Une simple mention de lieu générique ne suffit pas à valider ce marqueur.

### Signature 2

`rigor_compressed_in_sentence` — lorsqu’une réserve méthodologique ou une incertitude existe, elle reste dans la phrase sous forme courte et naturelle ; elle n’est ni supprimée ni exportée dans un appareil méta.

### Soutien

`concrete_texture_before_abstraction` — matière concrète avant conclusion analytique, lorsque la source la fournit.

### Négatif toujours évalué

`continuous_prose_not_social_format` — pas d’imitation mécanique du format LinkedIn.

## Nouvelle preuve de revue

Une revue Sarah valide doit désormais enregistrer :

- le rôle `independent_style_gate` ;
- l’évaluateur ;
- un ID de passe de génération ;
- un ID de passe de revue différent ;
- un contexte de génération ;
- un contexte de revue différent ;
- le SHA-256 du paragraphe visible exact ;
- l’ID et le SHA-256 du contrat de voix ;
- un verdict et une justification par marker évalué.

Un simple booléen n’est plus une preuve de revue.

## Limite restante, assumée

Le repo peut prouver que la revue **déclare et matérialise** une passe/context distincts et qu’elle est liée à un packet/texte précis. Il ne peut pas, à lui seul, prouver cryptographiquement que le fournisseur LLM a réellement utilisé une conversation séparée. Une évolution ultérieure peut isoler la revue Sarah dans un worker/context dédié et faire signer son packet d’entrée. Cette limite est préférable à une fausse promesse de déterminisme sémantique.

## Validation

Le patch ajoute des cas négatifs pour :

- revue Sarah absente ;
- même passe génération/revue ;
- revue obsolète après réécriture ;
- simple box-ticking de noms de markers ;
- ledger final portant une revue liée à l’ancien texte.

Le workflow `skill-ci` passe après correction du dernier test legacy de side-story method.
