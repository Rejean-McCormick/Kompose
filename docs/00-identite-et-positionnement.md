# 00 — KOMPOSE : identité et positionnement

**KOMPOSE** est une application / capacité indépendante de **conception, validation et simulation locale** de capsules pédagogiques et narratives. L'« orchestration » historique est une **modélisation de référence**, pas une autorité d'exécution opérationnelle Tandem. **Orgo est l'unique propriétaire des tâches, transitions, dispatchs et autorisations opérationnels réels** (voir [ADR 0008](adr/0008-tandem-orgo-operational-authority.md) et [état du code](CURRENT_IMPLEMENTATION_AND_BOUNDARIES.md)). **KOR est une autre application** susceptible de se brancher à KOMPOSE; ce n'est ni un synonyme, ni un sous-module obligatoire.

## Proposition

> KOMPOSE accueille un groupe dans une capsule, calibre son parcours, propose une distribution adaptée des rôles, relie personnes, missions et savoirs documentés, coordonne les étapes communes et donne à l'enseignant le dernier mot.

Les contenus ne doivent pas être indissociables du produit : une capsule de n'importe quel fournisseur qui respecte les contrats peut être montée dans KOMPOSE. Les **Kristals** désignent une famille de savoirs documentaires interactifs, pas l'unique format de ressource possible.

## Les neuf responsabilités

1. **Entry Door** — arrivée, code éphémère, identité validée par un fournisseur scolaire, présentation de la capsule et des rôles.
2. **Diagnostic** — adaptation individuelle, aménagements, contrôles de comparabilité, sans établir une hiérarchie permanente entre enfants.
3. **Casting** — choix éventuel du premier tiers, répartition du reste, préférences et contraintes, validation enseignante.
4. **Coordination simulée** — règles, déclencheurs, événements et progression **locale fictive**; aucune mutation réelle des tâches Orgo.
5. **Kristals** — acquisition, garde transférable, accès et questions/réponses éditées et traçables.
6. **Interactions** — rendez-vous, demandes de savoir et dépendances coopératives; la conversation libre est hors du moteur de règles.
7. **Adaptation continue** — rythme, modalités, accessibilité et parcours alternatifs, sans réévaluation dissimulée.
8. **Supervision** — console pour voir, expliquer, corriger, suspendre et reprendre, avec séparation des accès.
9. **Clôture et continuité** — bilan, restitution des acquis, événements finaux et conservation limitée.

## Choix de langage

- `Capsule` = expérience publiée et versionnée.
- `Session` = une exécution d'une capsule pour un groupe.
- `Participant` = pseudonyme limité à cette session.
- `Role` = responsabilités de jeu; pas une étiquette de valeur personnelle.
- `Kristal` = savoir structuré, questionnable sans génération IA.
- `Custody` = garde d'accès pendant la session; le savoir appartient à la capsule et à ses droits éditoriaux.
- `PromptDefinition` = message rédigé, déclenché par événement.
- `Phase` = point de synchronisation collectif.
- `Event` = changement de domaine observable et versionné.

## Ne fait pas

KOMPOSE ne doit pas être le fournisseur maître d'identités scolaires, un LMS complet, une IA générative, un dossier de profil psychologique, un outil d'évaluation clinique, un répertoire de messages privés, ni un monopole de contenu. Sa valeur est **de relier ces fonctions**, sans les absorber toutes.
