# Run 6 — seconde passe storytelling

Date : **2026-08-18**.

## Acquisition

La skill `youtube-search` du dépôt `achard-arnaud/search-social-networks` a été appliquée selon sa cascade publique : `yt-dlp` puis sous-titres publics, sans fournisseur payant. Les trois vidéos ont fourni des sous-titres automatiques anglais. La revue conserve URL, date, méthode, taille approximative et limites, sans republier les transcriptions complètes.

| Vidéo | Extraction | Apport retenu | Limite appliquée |
|---|---:|---|---|
| [Give me 18min & I'll improve your storytelling skills by 183%](https://www.youtube.com/watch?v=YtkrIaONxu0) | ~3 717 mots | Place + action pour entrer dans une scène | Les paroles et pensées ne sont utilisées que si une source historique les atteste. |
| [The Fastest Way to Become a Master Storyteller](https://www.youtube.com/watch?v=kPlzq2y72UI) | ~688 mots | Pratique répétée de récits courts et humains | Une anecdote relatable ne doit jamais être fabriquée. |
| [Tell Stories So Good You Finally Fix Your Retention](https://www.youtube.com/watch?v=epKEXCHjp4M) | ~16 834 mots | Contexte minimal, mission, progression, payoff, `but/therefore`, une idée à retenir | Pas de faux enjeu, cliffhanger ou hack de rétention dans un lecteur historique long. |

## Benchmarks

- [danjdewhurst/story-skills](https://github.com/danjdewhurst/story-skills) inspire le ledger de promesses/questions/callbacks et la QA déterministe. Les composants fictionnels de personnages, univers et production de chapitres ne sont pas repris.
- [Zzzeen2552/storytelling-mastery-skill](https://github.com/Zzzeen2552/storytelling-mastery-skill) inspire l’attention à la rupture, aux enjeux humains, à la transformation et au concret. Le modèle héros/vilain, le voyage du héros universel et la téléologie sont rejetés.

## Décisions intégrées

1. Nouveau pattern **PACE** : Place, Action, Constraint, Evidence.
2. Arc long : question causale → contexte minimum → mécanismes → progression `but/therefore` → rupture/résolution → réflexion/bridge.
3. Ledger de promesses, questions, callbacks et payoffs.
4. Voix cible : guide analytique, cultivé, adressé à un lecteur précis.
5. Gate non-fiction : aucune invention de dialogue, pensée, motif, détail sensoriel, enjeu ou chronologie.

La version opératoire est dans `skills/storytelling-historical-travel/SKILL.md` ; la traçabilité détaillée est dans `skills/storytelling-historical-travel/references/storytelling-patterns-and-review.md`.
