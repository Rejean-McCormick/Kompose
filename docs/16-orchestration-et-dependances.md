# 16 — Orchestration, dépendances et rythme commun

## Responsabilité centrale

Le moteur de KOMPOSE connaît l'**état** et les **règles**; les interfaces partenaires, dont KOR si raccordé, choisissent leur présentation. Les événements du moteur servent aux interfaces, lecteurs de documents, services d'évaluation et notifications.

## États

`brouillon → pret → inscriptions → diagnostic → attribution → validation → aventure → terminee`, avec `suspendue` temporaire et `annulee` terminal. Le contrôleur de référence est `src/kompose/lifecycle.py`.

Chaque commande documentée nécessite l'enseignant autorisé, une version attendue et certaines preuves préalables : `content_ready`, `diagnostics_reviewed`, `plan_checked`, puis validation finale et confirmation des règles fortes, de la couverture des rôles et de l'accessibilité. Ces booléens **ne sont pas des preuves réelles** : les services doivent les calculer et les conserver dans l'audit.

## Phases d'aventure

Une capsule définit ses points communs (`exploration`, `enquete`, `synthese` dans l'exemple). L'enseignant peut passer à la phase suivante lorsque les prérequis pédagogiques sont satisfaits; il peut déroger à un blocage pédagogique avec une justification auditée, **jamais** à une contrainte de sécurité, de confidentialité ou de droits.

## Dépendances

Chaque mission peut avoir `depends_on: [mission_id, ...]`. Le graphe doit être acyclique, valide et résilient aux absences. `ready_missions` révèle les missions dont les prérequis sont accomplis sans accéder aux profils des élèves. Les événements ne transportent pas les commentaires privés de l'enseignant.

Le cas d'un gardien indisponible produit une **proposition** de transfert, sous approbation enseignante; le contenu du Kristal reste identique et aucun droit de lecture n'est automatiquement octroyé.

## Contrat d'exécution requis en production

- Écrire état, numéro de version, événement et trace d'audit **dans une transaction atomique**.
- Traiter des événements dupliqués de façon idempotente; utiliser `event_id`, `session_version`, `correlation_id`.
- Si deux appareils déclenchent la même transition, un seul commit gagne; l'autre reçoit `409`.
- Émettre des événements différés via un **outbox** durable et des consommateurs avec déduplication.
- Projeter deux vues séparées : `student` ne voit que son rôle/mission; `teacher` voit les outils de coordination et seulement les données autorisées.
- En pause, aucune nouvelle progression métier élève n'est enregistrée; les brouillons locaux peuvent être restaurés selon politique.
- Reprendre à partir d'une session versionnée, et non de l'état affiché en cache sur le Chromebook.

## Limites du code inclus

Machine à états, graphe et choix de prompts sont des fonctions pures. Aucun broker, solveur d'affectation, stockage transactionnel, IAM, ou réel ordonnanceur n'est livré. Ne pas déployer comme serveur de production sans implémenter ces ports.
