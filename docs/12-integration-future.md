# 12 — Migration et intégrations futures

KOMPOSE est un **point de référence indépendant**. **Pour Tandem, la propriété des opérations réelles Case/Task/Signal est déjà décidée : Orgo, conformément à l’[ADR 0008](adr/0008-tandem-orgo-operational-authority.md).** Les autres propriétaires proposés restent à qualifier; voir [l’état du code](CURRENT_IMPLEMENTATION_AND_BOUNDARIES.md). Si les capacités sont réparties plus tard entre plusieurs produits et services, ne pas déplacer les informations privées ou les responsabilités de sécurité avec la seule logique de narration.

## Contrats à préserver

| Capacité | Futur système propriétaire possible | Invariant à conserver |
|---|---|---|
| Entry Door | passerelle école / IAM | code de capsule ≠ authentification |
| Diagnostic | service pédagogique | scores non publics, comparabilité contrôlée |
| Casting | service d'attribution | contraintes fortes, décisions explicables, validation |
| Orchestration **réelle** | **Orgo** (décision adoptée pour Tandem) | version, événements, pause/reprise et idempotence; aucun second runtime KOMPOSE |
| Kristals | registre de contenu et lecteur | sources, droits, garde distincte du savoir |
| Missions | moteur narratif | dépendances sans cycles et accès autorisé |
| Console | application enseignant | contrôle et données minimisées |
| Interfaces | KOR ou autre client | n'afficher que les projections autorisées |

## Méthode de migration

1. Versionner le contrat et consigner un ADR.
2. Fournir un adaptateur qui traduit les identifiants et les événements sans exposer de données privées.
3. Exécuter les tests de conformité sur l'ancien et le nouveau consommateur.
4. Migrer l'état de session et les versions épinglées avec stratégie de rollback.
5. Mettre à jour la matrice de responsabilité et archiver le comportement retiré.

Voir [18-architecture-ports-adapters.md](18-architecture-ports-adapters.md) et [20-plan-d-integration.md](20-plan-d-integration.md).
