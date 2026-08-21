# Template visuel — `analytical_focus`

Adaptation libre de la grammaire **two-pager-nice** au cadre historico-géographique. L’artefact JSON reste la structured source ; ce template ne crée aucune preuve.

## Format
- `one_or_two_pager`, A4 paysage ; 11 pt visé, 9 pt minimum ; padding cartes 11 pt visé, 9 pt minimum.
- Bandeau sombre : titre + question causale + takeaway.
- Rangée de 2–3 cartes blanches : positions/institutions comparées, chacune avec son caveat.
- Bandeau sombre « mécanisme » : chaîne causale courte ; les schémas remplacent la prose faible.
- Bloc ressources/fiscalité et bloc circulations extérieures seulement s’ils changent l’explication.
- Bandeau pleine largeur en bas : callback vers l’arc/lieu déjà étudié + payoff de réentrée.
- Tables : 5 colonnes maximum, 3 préférées.

## Code preuve
- **vert / ✓ = verified** : fait suffisamment stabilisé pour l’usage prévu ;
- **orange / △ = inference** : lecture causale ou transfert à conserver explicitement comme tel ;
- **rouge / ? = unknown** : question ouverte, contradiction ou donnée manquante.

## Markdown canonique
```md
**Focus analytique — <titre>**
> **Question** — <question>
**À retenir** — <thèse>
### Contraste institutionnel
- **A** — position
  - *Vigilance* : caveat
- **B** — position
  - *Vigilance* : caveat
> **Mécanisme**
> △ **nom** — explication
### Ressources / fiscalité
...
### Circulations extérieures
...
### Callback
- **cible** — relation
### À ne pas fermer trop vite
- question ouverte
> **Payoff** — retour au tronc
```

## QA visuelle standalone
Pour un export dédié one/two-pager : aucun overlap/overflow/clipping, revue à 100 % et 150 %. La palette sémantique ne doit jamais être utilisée comme décoration : elle encode le statut de preuve.
