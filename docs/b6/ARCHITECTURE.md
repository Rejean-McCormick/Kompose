# B6 — KOMPOSE, Kontexte et Orgo : frontière de responsabilité

**Statut : proposition implémentée en simulateur uniquement. Pas de runtime scolaire ni d'intégration Orgo opérationnelle.**

## Ce qui est démontré par les dépôts fournis

1. KOMPOSE `0.2.0` contient des **règles pures** (`lifecycle`, `coordination`, `reader`, `allocation_policy`, `events`) et une capsule fictive « rivières ». Les transactions, authentifications, composants Web, attributions réelles et envois ne sont pas implémentés.
2. L'ADR-001 **adoptée dans Kontexte** (`docs/decisions/ADR-001-ORGO-CANONIQUE.md`) désigne **Orgo** comme propriétaire canonique des `Case`, `Task`, `Signal`, `WorkflowVersion` et transitions opérationnelles. Son document `docs/ekole-orgo/09_ADR_ORGO_GRAND_ORCHESTRATEUR.md` précise que le choix est une décision de conception **non implémentée**.
3. Kontexte contient déjà `src/kontexte/orgo.py` : `scenario_fixture` (1 Case + 1 Task de **préparation**, pas d'exécution d'élèves), `integration_manifest` et `synthetic_review_workflow_fixture`. **KOMPOSE ne doit pas dupliquer leurs opérations**.
4. La mission de boulangerie (`kontexte.mission/1`) contient 3 rôles, 3 étapes à dépendances, 2 fragments et 1 jointure. Toutes les étapes exigent une **revue humaine**. Son statut est `scenario_skeleton_requires_pedagogical_review`, et toutes les références `curriculum_ids` pointent vers `qc-pri-ma-006` ; **pas** vers `qc-pri-ma-008`.

## Frontière cible (proposée pour la consolidation)

| Donnée/fonction | Propriétaire | KOMPOSE B6 fournit |
|---|---|---|
| Rôles, situations, étapes et textes sources | **Kontexte** | Validation et projection en contrat d'aperçu |
| Contraintes curriculaires, critères, preuves scolaires | **Ekole + Kristals** | Références d'objectifs, **aucune note attribuée** |
| Case/Task/Signal/WorkflowVersion, idempotence, transaction, destinataires | **Orgo** | Intentions de review **sans opération distante** |
| Mise en page et activité élève | **Ekole / B4** | Aperçu d'un rôle, sans indices secrets |
| Dépendances, logique, tests locaux de capsule | **KOMPOSE** | Plan déterministe, contrôles et **mock-replay uniquement** |
| World/release | Orgo_Worlds | Aucune mutation |

```
Kontexte MissionFrame / RoleFrame   [source versionnée]
                  │
                  ▼
KOMPOSE B6 compile_preview         [vérification + projection, sans droits]
       ├── role_projection(role)   [aperçu sûr d'un rôle]
       ├── propose_absence_fallback [proposition, pas réaffectation]
       └── replay_receipts(...)    [événements synthétiques en mémoire]
                  │
                  ▼  CONTRAT À QUALIFIER / REVUE HUMAINE
Kontexte orgo.scenario_fixture       [préparation Orgo existante]
                  │
                  ▼  dans FUTUR ENVIRONNEMENT ORGO DE TEST
Orgo Work/Orchestration              [source des statuts réels]
                  │
           ┌──────┴──────┐
           ▼             ▼
     Projections      Références de constats
     autorisées       pédagogiques → Ekole
```

## Primitives existantes vs manquantes

- **Existantes dans le pilote** : validation des IDs, dépendances sans cycles, projections par rôle, imitation de pause/reprise, reçus fictifs ordonnés, idempotence d'un même `event_id`, validation humaine simulée, garde simulée de jointure A+B, proposition de repli.
- **Manquantes dans les archives fournies** : véritable identité scolaire, contrôle des accès signé, politique de transmission des fragments par Orgo, jointure A+B transactionnelle, worker Orgo et outbox, version de World épinglée, preuve scolaire signée, historique durable, reprise réseau et mode multiélève opérationnel.
- **À arbitrer** : lorsque kompose est présent en parallèle d'Orgo, son historique `lifecycle.apply_session_command` doit rester un **référentiel de règles** et **ne doit pas être appelé pour avancer des sessions réelles Orgo**. Un seul système peut posséder une transition d'exécution.

## Garanties et non-garanties B6

- Aucun appel HTTP Orgo, aucun token, aucune émission de message, aucun fichier d'élève, aucune création de vraie Task.
- Aucun contenu des deux fragments secrets dans le plan exporté; seules leurs références et règles apparaissent.
- Les reçus `orgo_mock_fixture` ne prouvent **jamais** qu'un enseignant réel ou Orgo a autorisé une action; ils servent aux tests d'hypothèses. Les flags `human_reviewed` et `teacher_authorized` sont **fictifs**, pas une authentification.
- Un `step_completed` simulé augmente uniquement le compteur de tâches de test, **pas** une maîtrise scolaire.
- Si Orgo est indisponible, ne pas exécuter un moteur parallèle en cachette; l'école doit continuer via ses activités normales (B4) ou accompagnement enseignant.

## Prochain raccordement après consolidation

1. B5 confirme/revoit la mission boulangerie, ses textes, sa qualité pédagogique et son mapping vers `qc-pri-ma-008` ou justifie la conservation de `qc-pri-ma-006`.
2. Une copie identifiée du dépôt Orgo doit être fournie pour qualifier ses routes, ses permissions, ses événements et `Scenario Injector`. Aucun appel `--apply` sans Orgo de test isolé et autorisation explicite.
3. Décider le propriétaire des transitions : Orgo (suivant ADR Kontexte), kompose devenant validateur/projection et moteur de tests de contrats; planifier la migration et l'éventuelle dépréciation de l'ancien cycle `lifecycle`.
4. B2/B4 précisent comment un objectif validé et un MiniLab émettent une preuve pédagogique **séparée** d'une Task Orgo accomplie.
5. B8 crée tests interopérabilité, anti-fuite, refus d'absence, rejeu multiéquipement, et teste le pilote avec adultes/enseignants avant un vrai groupe scolaire.
