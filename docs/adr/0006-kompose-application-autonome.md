# ADR 0006 — KOMPOSE autonome, KOR comme intégration facultative

**Décision : acceptée le 2026-10-12.**

## Contexte

Le prototype « capsules, rôles, Kristals » était nommé comme une couche de KOR. L'orientation produit est désormais **KOMPOSE**, nom propre d'un orchestrateur autonome. KOR désigne une application distincte.

## Choix

Les contrats métier, identifiants de packages, schémas et événements portent KOMPOSE. Un adaptateur KOR demeure possible mais n'est pas un prérequis. Les fonctionnalités pourront migrer vers différents services tant que les invariants, versions et tests de contrat sont conservés.

## Conséquences

- Pas d'URL/identité d'API KOR codée comme dépendance obligatoire.
- Interfaces et IAM remplaçables via ports.
- Documentation des dépendances, des responsabilités et du transfert de propriété.
