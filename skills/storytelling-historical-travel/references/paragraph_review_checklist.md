# Paragraph review checklist — storytelling historical travel

This checklist is a backstage QA artefact. It must never be rendered into the reader.

## Fond

1. **Couverture canonique** — tous les `canonical_points` structurés du claim source sont repris. Pour les claims legacy sans `canonical_points`, le gate signale l'absence de cette structure mais ne fabrique pas une couverture sémantique à partir d'un simple comptage de mots.
2. **Texture de l'input** — le paragraphe contient au moins un élément concret de l'input : lieu, date, personne, institution, objet ou geste. Ce point peut nécessiter une revue ciblée si les métadonnées structurées ne suffisent pas.
3. **Ordre narratif** — fait/action avant mécanisme, mécanisme avant perspective/conséquence. Une conséquence ne doit pas servir d'ouverture puis reléguer l'action dans une subordonnée rétrospective.
4. **Citation et callback** — plus de deux citations directes `[claim:<id>]` est un signal de revue. Si un callback actif existe pour ce claim, une troisième citation directe est non conforme.
5. **Densité** — l'écart fort entre volume source et volume rendu est un avertissement, jamais un rejet automatique.

## Forme

6. **Aucune fuite méthodologique** — pas de `TL;DR`, `Statut canonique`, HIL, run/version, commentaire de construction, table d'ancres ou consigne de rédaction.
7. **Sigles explicités** — tout sigle ou acronyme reader-facing est développé au premier usage. Les identifiants cachés de traçabilité ne comptent pas comme prose lecteur.
8. **Termes techniques étrangers glosés** — un terme comme *clearing house* doit être francisé ou expliqué au premier usage.
9. **Ton de l'arc** — cohérent avec le paragraphe précédent et suivant ; revue L2 ciblée si nécessaire, jamais chargement du manuscrit complet.
10. **Fausses pistes** — 1–2 maximum par sous-section, sous forme question naïve/semi-rhétorique + réponse dans le même bloc identifié. La couleur pastel relève du renderer ; le sens ne doit pas dépendre de la couleur.

## Décision

- Une violation de fond ou de forme => **réécriture complète du paragraphe**.
- Un avertissement de densité/legacy/tone => revue ciblée ; ne pas transformer automatiquement l'avertissement en échec.
- Les tests doivent comporter des fixtures positives et négatives.

## Cas non conformes

### Fuite méthodologique

> TL;DR : ce claim établit un statut canonique fort pour la relique.

Rejet : le lecteur voit l'appareil de production.

### Terme étranger non glosé

> Le clearing house régional organisait les échanges du port.

Rejet : `clearing house` n'est ni francisé ni expliqué.

### Couverture canonique incomplète

Claim à trois points : visite du site ; construction du temple ; nouvelle relation politique avec le monastère.

> Le roi fit construire un temple.

Rejet : deux points structurés disparaissent.

### Ordre inversé

> Cela eut pour conséquence un renforcement du pouvoir royal, après que le roi eut visité le site.

Rejet : la conséquence précède l'action attestée.

### Troisième citation malgré callback

Le claim est déjà cité deux fois et un callback actif existe ; le paragraphe contient une nouvelle occurrence `[claim:C-X]`.

Rejet : reprendre le callback plutôt que réouvrir la preuve.

## Cas conforme

> Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple veut qu'il y ait rencontré les responsables du sanctuaire. Ce geste, d'abord local, renforça ensuite la relation politique entre la cour et l'institution religieuse.

Acceptation : fait concret avant conséquence, incertitude intégrée à la phrase, pas de méta-récit.
