# Sarah voice markers — contrat figé

## Statut et provenance

Ce fichier est **l’unique source de vérité de runtime** pour la voix Sarah. La génération et la relecture le lisent ; elles ne recherchent, ne synthétisent et ne complètent jamais la voix au moment d’un run.

- **Statut actuel** : `frozen_from_user_run25_spec`.
- **Source effectivement disponible pour cette version** : spécification Run 25 fournie explicitement par l’utilisateur le 27 août 2026.
- **Source primaire prévue par la Partie 0** : export de la mémoire de l’autre assistant utilisé par Sarah, importé comme donnée via le mécanisme `import-memory` lorsqu’il sera disponible.
- **État de cette source primaire** : `not_imported`. Aucun marqueur ci-dessous n’est présenté comme provenant de cette mémoire tant que son export n’a pas été réellement ingéré et synthétisé.
- **Révision** : uniquement par une nouvelle exécution explicite de la Partie 0. Une révision incrémente `contract_version` et invalide les anciennes revues de style par changement de hash. Le runtime ne modifie jamais ce fichier.

Le critère d’arrêt reste qualitatif : les marqueurs doivent permettre de distinguer une prose Sarah d’une prose générique bien écrite. Les marqueurs vagues ne sont pas accumulés pour atteindre un quota.

## Contrat machine-readable

<!-- SARAH_VOICE_CONTRACT_BEGIN -->
```json
{
  "contract_id": "sarah-voice-run25-v1",
  "contract_version": 1,
  "status": "frozen_from_user_run25_spec",
  "primary_source_status": "not_imported",
  "mandatory_markers": ["scope_precision"],
  "minimum_signature_passes": 1,
  "markers": [
    {
      "id": "scope_precision",
      "kind": "core",
      "applicability": "always",
      "description": "La précision de portée d’une affirmation ne se sacrifie jamais à la fluidité : qui, où, quand et avec quel niveau d’incertitude restent exacts."
    },
    {
      "id": "lived_opening_callback",
      "kind": "signature",
      "applicability": "section_or_sequence_opening_with_field_material",
      "description": "Quand une matière de terrain vécue existe, l’ouverture privilégie cette prise incarnée plutôt qu’un cadre conceptuel abstrait ; elle devient une promesse narrative reprise ensuite par callback. Un simple lieu générique ne suffit pas à valider ce marqueur."
    },
    {
      "id": "rigor_compressed_in_sentence",
      "kind": "signature",
      "applicability": "uncertainty_or_methodological_reserve_present",
      "description": "La rigueur méthodologique n’est pas supprimée pour fluidifier : elle est comprimée en une clause courte et naturelle dans la phrase, sans boîte méta ni commentaire de fabrication."
    },
    {
      "id": "concrete_texture_before_abstraction",
      "kind": "supporting",
      "applicability": "source_contains_concrete_texture",
      "description": "Le texte fait sentir d’abord la matière disponible — lieu, date, nom, objet, geste, institution — avant de formuler la conclusion analytique."
    },
    {
      "id": "continuous_prose_not_social_format",
      "kind": "negative",
      "applicability": "always",
      "description": "La voix n’imite pas les conventions LinkedIn : pas de sous-titres gras systématiques, listes de scannabilité, signature sociale ou question finale automatique."
    }
  ]
}
```
<!-- SARAH_VOICE_CONTRACT_END -->

## Lecture éditoriale des marqueurs

### 1. Précision avant légèreté

Une phrase peut rester ample si c’est le prix d’une portée exacte. On ne transforme pas un cas borné en règle générale, une tradition en fait attesté, une contribution en cause unique ou une observation locale en propriété du pays entier pour gagner quelques mots.

### 2. Ouverture incarnée quand le terrain le permet

Le marqueur distinctif n’est pas « commencer par quelque chose de concret » au sens large. Lorsqu’une observation vécue, une visite, un objet rencontré ou une anomalie de terrain est disponible, cette expérience donne la prise d’entrée. Elle doit pouvoir être rappelée plus loin et produire un payoff. En l’absence de matière vécue, une ouverture concrète reste préférable à une définition abstraite, mais elle ne suffit pas à elle seule à revendiquer ce marqueur signature.

### 3. Rigueur intégrée à la phrase

La réserve méthodologique ne disparaît pas. Elle prend la forme d’une clause brève : « la tradition rapporte… », « les sources disponibles permettent surtout de… », « cela contribue à expliquer, sans suffire à… ». Le lecteur reçoit l’incertitude au même endroit que l’affirmation, pas dans un appareil technique adjacent.

### 4. Matière avant conclusion

Quand la source fournit une date, un geste, une personne, un objet, une institution ou une topographie précise, cette texture entre dans la prose avant la généralisation qui en découle. Le texte ne se contente pas de résumer la conclusion du claim.

### 5. Prose continue, pas imitation du format social

Les habitudes utiles à un post social ne sont pas des marqueurs de voix transposables automatiquement au livre. La narration reste continue ; listes, sous-titres et questions sont utilisés seulement quand la structure du récit l’exige.

## Règles de gate

Une revue Sarah valide un paragraphe uniquement si :

1. elle est effectuée dans une passe de revue distincte de la passe de génération ;
2. elle est liée par hash au texte exact du paragraphe et à cette version exacte du contrat de voix ;
3. `scope_precision` est explicitement passé ;
4. au moins un marqueur `signature` applicable est passé, **ou**, lorsqu’aucun marqueur signature n’est applicable à cette unité, la revue l’explique explicitement et passe au moins un marqueur de soutien applicable ;
5. aucun marqueur applicable n’est marqué `fail` ;
6. chaque verdict `pass` ou `not_applicable` contient une justification courte et spécifique au paragraphe.

Le gate ne peut donc plus être satisfait par `passed=true` + une liste de noms de marqueurs. Il doit laisser une trace liée au texte, au contrat et à une passe indépendante.
