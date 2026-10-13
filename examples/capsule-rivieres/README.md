# Capsule fictive « La rivière des témoignages »

> **DÉMONSTRATION SEULEMENT — NON HISTORIQUE — NON VALIDÉE.** Les noms de rôles, les questions et les réponses illustrent la structure du système. Cette capsule ne contient aucune source historique publiée ni témoignage d'une nation autochtone. Elle **ne peut pas** être ouverte à des élèves dans un environnement de production.

## Contenu

- `capsule.json` : métadonnées et politique `ceil(n/3)` avec approbation obligatoire.
- `roles.json` : **20 rôles unitaires** et compétences sollicitées.
- `kristals.json` : **2 Kristals** de simulation (`demo`) avec questions et réponses exactes; sources marquées non vérifiées.
- `missions.json` : quatre missions et alternatives d'accessibilité.
- `prompts.json` : cinq messages scénarisés et leurs déclencheurs.
- `diagnostic.json` : blueprint conceptuel, **pas d'items ni de scores psychométriques réels**.
- `session.example.json` : 20 participants purement fictifs (`P-001` à `P-020`) et versions épinglées.
- `allocation.preview.example.json` : 20 affectations simulées (7 choix, 13 propositions), **non publiables**, sans score calculé.
- `teacher-constraints.PRIVE-DEMO.json` : deux contraintes **fictives et privées** pour illustrer leur emplacement; jamais livrer ce fichier au client élève.

## Tester

Depuis la racine :

```bash
PYTHONPATH=src python3 -m kompose.cli validate examples/capsule-rivieres
PYTHONPATH=src python3 -m kompose.cli quota 20
PYTHONPATH=src python3 -m kompose.cli read examples/capsule-rivieres/kristals.json KR-ARCHIVES TERRITOIRE OCCUPANTS --demo
PYTHONPATH=src python3 -m kompose.cli trigger examples/capsule-rivieres/prompts.json kristal.acces_accorde --audience demandeur --demo
```

Sans `--demo`, la consultation est refusée. Le `CLI` n'authentifie pas un enfant et sert uniquement à illustrer la résolution documentaire.

## Transition vers du contenu réel

Créer un corpus documenté; préciser période, région et nations concernées; obtenir validations et permissions appropriées; remplir les références des sources et l'examen éditorial; mettre le Kristal en `published` uniquement après approbation; ajouter contrôles d'accès scolaires, outils d'accessibilité et tests de biais.

## KOMPOSE 0.2 : scénario complet et phases

- `phases.json` : trois phases, prérequis et alternatives accessibles.
- `missions.json` : `depends_on` explicite sans cycle.
- `event.example.json` : enveloppe événementielle minimale.
- `session.example.json` : session fictive en brouillon avec `version: 0` et phase initiale.
- `allocation.preview.example.json` : fixture **non publiable**, pas un solveur d'attribution.

```bash
PYTHONPATH=src python3 -m kompose.cli demo-flow examples/capsule-rivieres
PYTHONPATH=src python3 -m kompose.cli ready-missions examples/capsule-rivieres/missions.json --completed MIS-RECHERCHE MIS-DEMANDE
```

KOMPOSE est indépendant de KOR. L'adaptateur d'exemple facultatif est dans `examples/integrations/`.
