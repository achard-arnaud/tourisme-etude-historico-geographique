# Run 7 — V3 intégrale Sri Lanka 2026

## Verdict sur l'échec V2

Le premier document est passé de **61 pages en V1 à 8 pages en V2**, soit une réduction de **86,9 % des pages**. Le contenu textuel est passé d'environ 16,7 k mots dans les paragraphes de la V1 à 1,95 k mots dans la V2, soit environ **88,3 % de perte**.

La cause est une chaîne de trois erreurs :

1. `scripts/render_reader_exports.py` lisait exclusivement `09_output/report.md`, un delta Run 5 de 1 447 mots, au lieu de la V1 complète ;
2. les deux contrats lecteur combinaient contradictoirement `audience: advanced` et `length_budget: quick` ;
3. la passe storytelling possédait des bandes de longueur par défaut, sans contrôle de rétention contre le document précédent.

Le résultat n'était donc pas une V2 de la fresque, mais la mise en page d'un delta condensé sous le nom du document complet.

## Correction V3

- Les deux DOCX V1 sont archivés comme baselines binaires dans `09_output/archive/`.
- Leur extraction texte complète est versionnée dans `report_v1_full.md`.
- Les `report.md` de Run 5 sont désormais explicitement traités comme des **deltas**.
- `render_full_reader_v3.py` insère chaque section du delta à un emplacement chronologique de la V1, puis ajoute l'appareil de sources propre aux compléments.
- Le build échoue si le volume V3 ne dépasse pas la baseline plus 90 % du delta.
- Le renderer V2 refuse désormais la compression silencieuse, sauf demande explicite d'un dérivé abrégé.
- Le preset avancé et les deux contrats lecteur sont sans plafond de longueur.

## Capitalisation conversationnelle

Les onze fiches historiques/méthodologiques récupérées du dossier de conversation sont matérialisées dans `examples/sri_lanka_pre_1948/05_sources/conversation_corpus/`. Quatre fiches supplémentaires conservent les échanges de terrain, d'itinéraire, de traduction et de logistique. Le registre `conversation_capitalization_register.md` route chaque séquence vers la fresque, une fiche ou un contexte explicitement hors tronc.

Les fiches de conversation sont des matériaux de cadrage et de terrain, non des preuves autonomes. Les photos absentes et le lien partagé restant sont signalés au lieu d'être simulés.

## Mesures V3

| Volume | Baseline DOCX | Delta Run 5 | V3 DOCX | Gain vs baseline | PDF |
|---|---:|---:|---:|---:|---:|
| Origines–1948 | 19 274 mots | 1 381 mots | 21 236 mots | +10,2 % | 68 pages |
| 1948–2026 | 5 269 mots | 1 886 mots | 8 624 mots | +63,7 % | 29 pages |

Le comptage DOCX inclut les tableaux, d'où l'écart avec un comptage limité aux seuls paragraphes. Les métriques machine sont dans `RUN7_V3_RETENTION_METRICS.json`.

## QA

- rendu LibreOffice DOCX → PDF puis PNG de chaque page ;
- inspection visuelle des couvertures, notes de méthode, points d'insertion Run 5, appareils de sources et dernières pages ;
- format Letter et pagination continus conservés ;
- correction d'une continuation automatique de liste (`35–38`) remplacée par une numérotation littérale `1–4` ;
- titres des ajouts rétrogradés en `Complément V3` pour préserver la numérotation maîtresse de la V1.

## Reliquats / prochaines étapes

1. rattacher les photos originales des panneaux 3, 7 et 9 et vérifier l'identification au *Kusa Jātaka* ;
2. résoudre le TODO du lien partagé conservé dans `05_questions_a_repondre.md` ;
3. prolonger les lacunes de l'audit sur travail, maintenance, fiscalité réelle, démographie et groupes sociaux sous-documentés ;
4. après gel du contenu, ajouter si utile une navigation Word/PDF plus riche sans réécriture ni compression du texte.
