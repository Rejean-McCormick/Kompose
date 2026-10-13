# Catalogue d'événements v1

## Enveloppe

```json
{
  "event_id": "evt-opaque",
  "schema_version": 1,
  "name": "kristal.acces_accorde",
  "aggregate_id": "KR-ARCHIVES",
  "session_id": "SESS-EXEMPLE",
  "occurred_at": "2026-10-12T12:00:00Z",
  "payload": {"kristal_id":"KR-ARCHIVES","grant_id":"ag-opaque","recipient_id":"P-003"}
}
```

Les notifications de l'UI affichent du **texte rédigé** via une `PromptDefinition`, jamais l'enveloppe brute ou des données privées d'événement.

| Événement | Émetteur | Charge utile minimale | Consommateurs |
|---|---|---|---|
| `session.ouverte` | orchestration | `capsule_id`, `session_id` | UI / diagnostic |
| `session.inscription_confirmee` | séance | `participant_id` | orchestration |
| `diagnostic.termine` | évaluation | `participant_id`, `result_ref`, `comparable` | attribution (canal privé) |
| `session.roles_publies` | attribution | `assignment_batch_id` | UI / missions |
| `role.attribue` | attribution | `participant_id`, `role_id` | missions |
| `kristal.garde_attribuee` | gameplay | `kristal_id`, `custodian_id` | UI gardien |
| `kristal.acces_demande` | gameplay | `kristal_id`, `request_id`, `custodian_id` | UI gardien / enseignant |
| `kristal.acces_accorde` | permissions | `kristal_id`, `recipient_id`, `grant_id` | lecteur / missions |
| `kristal.question_consultee` | lecteur | `kristal_id`, `question_id`, `participant_id` | missions / métriques minimales |
| `mission.validee` | mission | `mission_id`, `participant_id` | narrative |
| `session.terminee` | orchestration | `session_id` | rétention / archivage |

## Confidentialité et idempotence

- **Canal privé** distinct pour le diagnostic et les décisions enseignant; jamais de `TeacherConstraint` dans un événement consommé par l'élève.
- Les messages sont dédupliqués par `(event_id, prompt_id, recipient_id)` avec envoi « au plus une fois visible » même si le transport réessaie.
- Les projections appliquent des politiques de conservation séparées des archives de contenu.
- Les identifiants sont des références, non des noms ou descriptions sensibles.

## Extension KOMPOSE : coordination et continuité

| Événement | Origine | Cible et intérêt |
|---|---|---|
| `session.prete` | cycle de vie | session configurée, contenus vérifiés |
| `session.inscriptions_closes` | cycle de vie | fin d'entrée, début du diagnostic |
| `session.diagnostic_clos` | cycle de vie | résultats prêts pour casting privé |
| `session.attribution_proposee` | casting | prévisualisation privée prête |
| `session.attribution_revision` | casting | recalcul après intervention |
| `session.phase_changee` | coordination | projection d'un jalon partagé |
| `session.suspendue` | enseignant | arrêter la progression active |
| `session.reprise` | enseignant | reprendre l'ancien état |
| `session.annulee` | enseignant | fermeture anticipée |
| `kristal.transfert_propose` | garde | transfert à confirmer par enseignant |

En production, chaque événement porte `event_id`, `schema_version`, `session_id`, `aggregate_id`, `occurred_at`, `session_version` et une charge minimale. Les événements d'attribution sensibles passent **uniquement par le canal privé**. L'enveloppe structurée est validable par [event.schema.json](schemas/event.schema.json).

KOR (ou un autre client) souscrit seulement aux événements projetés pour son audience. Un manifeste d'adaptateur décrit les capacités demandées et indique explicitement qu'aucun export d'informations identifiantes, de diagnostic privé ou de contraintes enseignantes n'est permis par l'intégration de démonstration.
