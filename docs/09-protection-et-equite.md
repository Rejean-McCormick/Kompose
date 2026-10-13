# 09 — Protection des mineurs, confidentialité, accessibilité et équité

> Cadre de **conception**, non avis juridique. Les obligations exactes doivent être confirmées pour les établissements et juridictions de déploiement (dont les règles québécoises/canadiennes pertinentes si déployé au Québec).

## Principes non négociables

- **Minimisation :** utiliser des pseudonymes de séance; ne pas exporter les noms, diagnostics bruts ou liens relationnels sans nécessité stricte.
- **Séparation des rôles :** aucune information confidentielle de la console n'arrive au frontend de l'élève, même cachée dans le HTML.
- **Contrôle humain :** enseignant habilité peut suspendre la session, corriger une affectation, supprimer une contrainte, invalider un accès.
- **Proportionnalité :** consigner une contrainte d'aversion uniquement si elle améliore la sécurité ou la dynamique d'une mission donnée, avec justification minimale, date d'expiration et visibilité restreinte.
- **Ne pas inférer de diagnostics cliniques :** aucune catégorie médicale, sociale ou psychologique déduite automatiquement d'un test ou d'une relation.
- **Équité :** évaluer les biais et l'effet des accommodements; proposer le mode sans classement.
- **Pas de chat libre imposé :** interactions structurées modérées et alternatives hors ligne ou médiées par l'enseignant.

## Matrice d'accès simplifiée

| Donnée | Élève concerné | Autre élève | Enseignant habilité | Éditeur |
|---|---:|---:|---:|---:|
| rôle et mission propres | oui | seulement éléments publics | oui | non |
| diagnostic détaillé | limité au retour pédagogique | non | oui, nécessité | non |
| contrainte entre élèves | non | non | oui, nécessité | non |
| question/réponse publiée | si autorisé | si autorisé | oui | oui |
| journaux de décisions | non | non | pertinents à la séance | non |
| identification réelle | selon politique SSO | non | selon responsabilité | non |

## Protection technique à prévoir

Authentification intégrée à l'école, autorisation côté serveur par séance, TLS, chiffrement au repos selon risque, rotation des codes, limitation de débit, prévention d'accès croisé, journaux minimisés et protégés, gestion des incidents, sauvegarde contrôlée, suppression/expiration, revue de sécurité, tests d'accessibilité et de menace.

## Cycle de conservation (proposition, à valider)

- Codes de jonction et jetons : courts et révocables.
- Relations et adaptations : durée de la séance, suppression par défaut à clôture + délai opérationnel défini par l'établissement; aucune conservation longitudinale non autorisée.
- Résultats diagnostics : se limiter à la durée nécessaire; décider avec l'école de ce qui est conservé pédagogiquement.
- Statistiques de produit : agrégées et non ré-identifiantes.
- Logs d'audit : durée liée aux obligations institutionnelles, accès réduit.

## Risques et protections

| Risque | Réponse |
|---|---|
| stigmatisation par classement | scores/rangs non publics, option sans classement, missions accessibles |
| favoritisme des rôles/du savoir | alternance de garde, suivi équitable, critères explicites |
| isolement d'un enfant | voie d'accès alternative à chaque Kristal |
| divulgation par code de capsule | code non suffisant comme authentification |
| divulgation d'aversion par une justification | messages aux élèves neutres, explications privées |
| contenu historique préjudiciable | revue éditoriale, consultation appropriée, retrait/versionnage |
