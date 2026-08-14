# tourisme-etude-historico-geographique

## Ce que cette skill fait
Un petit **OS d'enquête historico-géographique** destiné aux voyages : capture de terrain, recherche critique, knowledge base réutilisable, puis rapport lisible.

Elle est issue d'un retour d'expérience : une enquête Sri Lanka a commencé par des questions sur Polonnaruwa et s'est transformée en fresque du Rāmāyaṇa au XXe siècle. La méthode formalise ce qui a fonctionné et corrige ce qui a coûté du temps : duplication entre fichiers, bridges découverts tard, annexes jamais lues, glissement entre chroniques et faits, et surpoids des monuments visibles.

## Décision d'architecture
**Arc-first + Zettelkasten-lite + graph-light.**

Le Zettelkasten pur aurait amélioré la réutilisation des idées et évité de recopier les mêmes thèmes dans plusieurs chapitres. Mais l'atomisation intégrale dès la visite aurait ralenti la capture et fragmenté le récit. Le compromis retenu :
1. les notes de terrain restent rapides ;
2. les claims stables deviennent atomiques ;
3. les arcs gardent le contexte chronologique ;
4. le graph-light gère les relations transversales ;
5. la sortie finale est un récit, pas un graphe.

## Structure recommandée d'un projet
```text
<voyage>/
├── README.md
├── 00_method/
│   ├── causal_map.md
│   ├── source_policy.md
│   └── vocabulary.md
├── 01_arcs/
│   ├── A01_<slug>/
│   │   ├── ARC.md
│   │   ├── claims/
│   │   └── evidence/
│   └── ...
├── 02_hil/
│   ├── HIL-01_institutions/
│   ├── HIL-02_geography/
│   └── ... HIL-08
├── 03_wiki/
│   ├── people/
│   ├── places/
│   ├── institutions/
│   ├── concepts/
│   ├── commodities/
│   └── artifacts/
├── 04_graph/
│   ├── nodes.jsonl
│   ├── edges.csv
│   └── coverage.csv
├── 05_sources/
│   ├── anchors/
│   ├── literature_notes/
│   └── source_register.csv
├── 06_bridges/
├── 07_drifts/
├── 08_questions/
└── 09_output/
    ├── report.md
    └── report.docx
```

## Comment utiliser l'arborescence agentique
`SKILL.md` orchestre. Les sous-skills sont spécialisées : sourcing, sanitize, arcs, zooms, économie, religion, sécurité, biais, bridges, wiki, graph, édition.

Le **wiki** détient les objets durables. Les **arcs** détiennent le contexte temporel. Les **HIL** détiennent les vues transversales. Le **graph** détient uniquement les relations structurées : il ne remplace aucun de ces trois niveaux.

## HIL
HIL signifie ici **Historical Intelligence Layer**, terme interne à la méthode et non standard académique.

Les 8 HIL sont documentées dans le `SKILL.md`.

## Qualité
Une enquête est prête pour output lorsque :
- chaque arc a une rupture d'entrée et une rupture de sortie ;
- chaque claim causal majeur possède une source d'ancrage ;
- les contradictions sont visibles ;
- les bridges sont clos ou explicitement U ;
- la matrice ARC×HIL×ZOOM montre les trous volontaires et involontaires ;
- l'audit de drift a été passé ;
- les notes annexes ont été soit intégrées comme encadrés, soit supprimées du fil de lecture.
