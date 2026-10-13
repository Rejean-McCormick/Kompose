# 20 — Plan de développement et absorption progressive

Statut : **repo de référence exécutable**, non application scolaire en production. Cette checklist est le chemin d'implémentation dans une équipe ou dans des applications clientes.

| Étape | Livrable | Critère d'acceptation | État |
|---|---|---|---|
| A | Domaines et schémas | exemples versionnés cohérents, règles explicites | **documenté / tests de référence** |
| B | Entry Door web | code expirant, SSO scolaire, rate-limit, reprise | à implémenter |
| C | Diagnostic | mesures comparables ou repli sûr, aménagements | à implémenter |
| D | Casting | solveur à contraintes, choix du tiers, explications privées, validation | à implémenter |
| E | Orchestrateur de session | transactions, outbox, versions, pause/reprise | référence pure; serveur à implémenter |
| F | Kristals documentaires | sources validées, gestion de droits, revue éditoriale | lecteur démo; chaîne éditoriale à implémenter |
| G | Interfaces | console enseignant + UI Chromebook/tablette + accessibilité | à implémenter |
| H | Partenaires | adaptateurs KOR ou autres, contrats et tests | manifeste exemple |
| I | Exploitation scolaire | sécurité, législation locale, audits, politique rétention, pilote | à implémenter |

## Définition de « terminé » pour une première classe pilote

Un groupe scolaire réel ne doit être invité que lorsque SSO, autorisations, audit, approbation enseignante, données privées séparées, politiques de rétention, contenu historique vérifié, scénarios de panne et tests d'accessibilité sont réellement disponibles. **Les démonstrations fictives ne remplissent pas ces critères.**

## Absorption par d'autres composants

À chaque migration, inventorier le contrat consommé, fixer une version, reproduire les tests de référence chez le destinataire, documenter le nouvel owner, puis retirer l'implémentation transitoire. Le dépôt KOMPOSE peut rester le registre des invariants et des ADR même lorsque les fonctions seront réparties.
