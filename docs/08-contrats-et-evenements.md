# 08 — Contrats d'intégration, API et événements

Le **contrat proposé** est dans `contracts/openapi.yaml` et `contracts/events.md`. Il sert de frontière entre les futurs services KOMPOSE; ce dépôt n'expose aucun serveur.

## Périmètres de sécurité (cible)

| Famille | Qui | Exemples |
|---|---|---|
| lecture publique contrôlée | élève de la séance | catalogue des rôles, missions autorisées |
| opération de séance | élève authentifié | inscription, choix de rôle, demande d'accès, consultation |
| opérations privées | enseignant de cette séance | adaptations, contraintes, publication, remplacement de gardien |
| publication éditoriale | responsable autorisé | soumission, approbation, version de Kristal |
| transport interne | services de KOMPOSE | événements de domaine et lecture projection |

## Idempotence & versions

- Toute commande à effet (choix, octroi d'accès, attribution) reçoit un `idempotency_key` et une version de séance/ressource, avec gestion des accès concurrents.
- Les événements ont `event_id`, `schema_version`, `occurred_at`, `session_id`, `aggregate_id`, `payload` minimal.
- Le contenu documentaire est identifié par `(kristal_id, version)`; ne jamais servir « dernière version » de manière implicite à une séance déjà démarrée.
- Les éventuelles données de relation/adaptation ne figurent ni dans les events publics ni dans les logs applicatifs non protégés.

## Erreurs communes

`401` non authentifié, `403` sans droit, `404` introuvable **ou masqué** pour un autre élève, `409` état incompatible/collision, `422` entrée non conforme, `423` contenu verrouillé ou non publié, `429` limite de débit. Les messages ne doivent pas révéler les contraintes cachées.

## Absorption des contrats

Lorsqu'un module reprend une fonctionnalité, il devient **propriétaire** de son agrégat, garde les identifiants et événements convenus, et publie une traduction si son modèle interne diffère. Voir [12](12-integration-future.md).
