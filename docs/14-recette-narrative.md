# 14 — Recette narrative d'une capsule à Kristals

Cette recette met les modules en relation. Elle n'imite aucun événement historique réel et n'utilise aucune voix autochtone fictive.

## Mise en scène

**Question motrice :** « Que faut-il savoir pour reconstituer l'histoire d'un territoire sans confondre sources, points de vue et preuves ? »

20 élèves / 20 rôles, dont cartographe, archiviste, enquêtrice, messager, diplomate, médiatrice et conservateur. Deux Kristals **de démonstration** sont accessibles seulement via le mode démo : archives administratives (fictives) et méthode d'analyse de perspectives situées (fictive). Dans une capsule réelle, chaque source devrait être identifiée et approuvée, avec permissions pertinentes.

## Séquence à embranchements

| Étape | Intervention narrative | Action / preuve | Événement |
|---|---|---|---|
| 0 | « La capsule est ouverte » | élève rejoint avec code + identité scolaire | `session.inscription_confirmee` |
| 1 | « Découvre les métiers de l'enquête » | rôles consultés puis diagnostic accessible | `diagnostic.termine` |
| 2 | « Chacun a une responsabilité » | enseignant publie les attributions | `session.roles_publies` |
| 3 | « Le premier Kristal a été confié » | gardien reçoit un indice et une consigne de médiation | `kristal.garde_attribuee` |
| 4a | « Retrouve le gardien » | demandeur sollicite l'accès | `kristal.acces_demande` |
| 4b | « Une piste cartographique apparaît » | autre équipe gagne un accès par découverte | `kristal.acces_accorde` |
| 5 | « Pose une question précise » | thème + question; lecture texte/sources/limites | `kristal.question_consultee` |
| 6 | « Les documents ne disent pas tous la même chose » | comparer les provenances, preuves, inconnues | `mission.validee` |
| 7 | « Transmettre la compréhension » | exposé d'équipe avec citations et limites | `mission.validee` |

## Exemple d'acquisition par un élève

- La mission indique qu'un Kristal existe; son gardien est identifié uniquement si cette révélation est permise par la capsule.
- L'élève demande une rencontre ou utilise le bouton **Demander l'accès**. Un échange structuré permet d'obtenir un jeton temporaire; un autre accès est possible via l'enseignant.
- L'élève choisit **Territoire → Quelles informations manquent pour identifier les occupants ?**
- KOMPOSE affiche exactement la réponse préécrite, les références et « ce qu'on ignore ».
- La mission demande de comparer avec un autre Kristal; les réponses ne sont pas converties en vérité unique par un calcul automatique.

## Éviter une économie inégalitaire du savoir

La garde n'est pas un rang. Une bonne performance peut déclencher une attribution dans certaines capsules, mais d'autres gardes doivent récompenser enquête, transmission, persévérance et rotation. Les élèves ne paient jamais et ne doivent jamais divulguer d'information personnelle pour accéder à un Kristal. Chaque Kristal essentiel dispose d'un chemin de secours.

## Simulation de prévisualisation

Voir `examples/capsule-rivieres/allocation.preview.example.json` : 20 affectations fictives, dont 7 rôles sélectionnés dans l'exemple, et 13 propositions. Ce fichier n'est **pas** le résultat d'un véritable solveur ni d'un examen.
