# 04 — Diagnostic, adaptation et attribution des rôles

## Deux résultats distincts, jamais confondus

1. **Profil pédagogique** : dimensions observées et aménagements pour adapter missions, supports et consignes. Aucune difficulté n'est déduite d'un unique score.
2. **Ordre de choix** (optionnel) : score comparable entre élèves **uniquement si** les instruments et aménagements ont une validité suffisante pour le classement. À défaut : renoncer au classement et choisir une règle alternative annoncée (rotation, tirage supervisé, choix guidé).

Le diagnostic adaptatif ajuste la difficulté **des items**, non la dignité ni le potentiel de l'élève. Les valeurs de calibrage, fiabilité, équité et interprétation doivent être établies séparément par des spécialistes; aucun algorithme psychométrique n'est livré dans ce dépôt.

## Politique de distribution de référence

- `mode = tiers_choix` (configurable), `quota = ceil(n_participants_eligibles / 3)` : 20 élèves donnent **7** tours de choix.
- Les élèves éligibles sont ordonnés sur une métrique *comparable* et autorisée. Les égalités se départagent par tirage déterministe auditable lié à la séance, jamais par nom, genre ou information sensible.
- Chaque tour sélectionne un rôle encore disponible et compatible avec des **contraintes dures**. Aucun classement individuel n'est rendu public.
- Après ces choix, le service résout un **problème d'affectation sous contraintes** pour les élèves restants et leurs rôles, puis donne un **aperçu enseignant**.
- L'enseignant confirme; les changements sont justifiés et journalisés, jamais masqués.

## Algorithme cible (normatif, pas exécuté par le code exemple)

```text
entrées : participants, rôles/capacités, résultats comparables, préférences,
          adaptations nécessaires, contraintes enseignant, interactions entre rôles
précontrôles : test comparable ? sinon mode guidé; ressources disponibles ?
1. réserver les aménagements, capacités, obligations de sécurité et rôles indispensables
2. ordonner les élèves du premier tiers avec départage non discriminant
3. permettre un choix transactionnel par tour (contrainte dure vérifiée)
4. construire le problème global d'affectation des élèves non servis :
   variables x[e,r] ∈ {0,1}, chaque élève reçoit un rôle, capacités respectées
   contraintes dures : accès, sécurité, incompatibilités explicitement justifiées,
                       aucune combinaison conflictuelle dans des interactions requises
   préférences souples : intérêts, diversité, défi adapté, coopération souhaitée
   maximiser l'utilité pédagogique, sans utiliser de données sensibles comme "score social"
5. résoudre avec optimisation de contraintes (type CP-SAT/MILP) avec politique de repli
6. présenter les attributions, raisons non stigmatisantes et conflits à résoudre
7. validation enseignante obligatoire avant publication
```

**Attention :** les affinités et aversions entre élèves induisent des contraintes **entre affectations**. Un simple appariement biparti ou un algorithme glouton ne garantit **pas** leur respect quand les rôles imposent des interactions. Le solveur de production doit intégrer le graphe des collaborations. Ce dépôt ne prétend pas fournir un tel solveur.

## Contraintes

| Catégorie | Force | Exemple de comportement |
|---|---|---|
| sécurité / protection | dure | ne pas imposer de contact direct à deux élèves si risque motivé |
| accessibilité et adaptations | dure | rôle accessible avec support requis |
| capacité du rôle | dure | un seul gardien si prévu |
| rôles requis par scénario | dure ou configuration explicite | garantir une couverture des fonctions essentielles |
| préférence déclarée par élève | souple | favoriser enquête si un élève le souhaite |
| affinité de coopération | souple | favoriser duo lorsque compatible avec objectifs |
| aversion sans enjeu de sécurité | souple et limitée dans le temps | diminuer probabilité d'une collaboration imposée |
| diversité de rôle d'une séance à l'autre | souple | éviter monopole permanent des rôles prestigieux |

## Cas limites

- **Moins de places que d'élèves** : rôle multi-capacité, équipe ou extension explicite; ne pas attribuer le néant silencieusement.
- **Plus de rôles que d'élèves** : définir les rôles essentiels et les rôles inactifs.
- **Ex æquo nombreux** : loterie traçable sans divulgation du score.
- **Absence de diagnostic** : adaptation par enseignant ou nouvelle tentative; jamais note nulle implicite.
- **Données insuffisantes ou non comparables** : pas de premier tiers par score; stratégie alternative approuvée.
- **Conflit sans solution** : lever les seules préférences souples; si contraintes dures insatisfaites, bloquer et demander décision humaine, avec options sûres.
- **Changement de groupe en cours d'aventure** : réévaluer attribution, gardiens, accès et messages non émis.

## Ce que la console explique

« Ce rôle correspond à l'intérêt déclaré pour la cartographie et dispose du support de lecture requis » est acceptable. « Cet élève a un mauvais score / est incompatible avec X » **ne doit jamais** être montré aux élèves.
