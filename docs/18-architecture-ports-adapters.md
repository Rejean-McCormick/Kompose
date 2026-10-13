# 18 — Architecture indépendante : ports et adaptateurs

KOMPOSE **n'est pas KOR**. C'est un moteur de coordination qui doit pouvoir fonctionner avec divers fournisseurs de contenus, d'identité et d'interfaces. Un partenaire peut ultérieurement reprendre ses contrats et invariants dans ses propres modules; cela constitue une **intégration/migration contrôlée**, pas une identité de marque commune.

## Ports entrants

- `TeacherConsolePort` : configurer, approuver, suspendre, reprendre, clore.
- `StudentEntryPort` : demander la jonction avec code + identité externe validée.
- `ExperiencePort` : consulter rôles, missions, Kristals et état autorisés; recevoir événements rendus.

## Ports sortants

- `IdentityProviderPort` : vérifier élève/enseignant et droits scolaires.
- `DiagnosticPort` : obtenir mesures et comparabilité (privé), aménagements (privé).
- `AssignmentPort` : produire des propositions sous contraintes, preuves et explications privées.
- `ContentRegistryPort` : accéder à des contenus et sources versionnés / droits validés.
- `EventTransportPort` : événement outbox, idempotence et abonnements.
- `PersistencePort` : session, version, historique et projections.
- `AuditPort` : actions enseignantes, corrections et motifs autorisés.
- `PresentationPort` : messages et vues sur Chromebook/tablette (KOR possible).

## Matrice de propriété

| Objet | Propriétaire logique | Ce que KOMPOSE conserve |
|---|---|---|
| Identité scolaire | fournisseur IAM / établissement | référence opaque par session |
| Diagnostic détaillé | service d'évaluation | statut, version, résultat synthétique privé si nécessaire |
| Règles/attributions | moteur de rôles | commandes, décisions finales et trace d'audit |
| Documents historiques | registre éditorial | identifiant et version épinglée, permissions |
| Rendu de prompts | application cliente | définition, événement de déclenchement, destinataire autorisé |
| États de session/mission | KOMPOSE | version et progression minimale |

## Intégration possible à KOR

Un adaptateur peut transformer `session.roles_publies` en notification KOR, rendre un lecteur de Kristal dans son UI et appeler les routes publiques autorisées. **KOR n'a pas à héberger les dossiers scolaires, le classement privé ni les règles éditoriales.** Voir [integration-manifest.schema.json](../contracts/schemas/integration-manifest.schema.json) et l'exemple [kor.adapter.example.json](../examples/integrations/kor.adapter.example.json).

## Versionnage

- API et événements en `/v1`; `schema_version` entier pour les enveloppes, `contract_version` semver pour l'intégration.
- Schémas conservés comme source de vérité; changements incompatibles = nouvelle version majeure.
- Contrats testés de chaque côté de la frontière. Évolution via ADR, pas par modification silencieuse.
