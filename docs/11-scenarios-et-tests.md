# 11 — Scénarios d'acceptation et plan de validation

## Parcours nominal (20 élèves / 20 rôles)

```gherkin
Étant donné une capsule à 20 rôles unitaires et 20 participants actifs
Et des diagnostics comparables et des choix individuels autorisés
Quand l'enseignant clôture le diagnostic
Alors le quota de premiers choix est de 7
Et les 7 tours s'exécutent en ordre vérifiable sans afficher les rangs
Et les 13 autres élèves reçoivent une proposition sous contraintes
Et aucun rôle n'est publié sans validation enseignante
```

## Diagnostic incomparable

```gherkin
Étant donné deux diagnostics non comparables selon l'instrument utilisé
Quand KOMPOSE prépare la distribution par classement
Alors KOMPOSE ne classe pas ces participants comme s'ils avaient passé la même épreuve
Et la console propose une attribution guidée ou une alternative annoncée
```

## Contrainte de sécurité

```gherkin
Étant donné une incompatibilité directe confidentielle et motivée
Quand un rôle impose un dialogue direct entre les élèves concernés
Alors l'attribution est rejetée ou révisée
Et aucun élève ne reçoit une notification révélant la contrainte
```

## Garde et accès

```gherkin
Étant donné un Kristal publié, versionné et un gardien désigné
Quand le demandeur remplit les conditions de quête
Et le gardien accepte une demande (ou l'enseignant applique un secours)
Alors une autorisation temporaire est créée
Et le demandeur peut sélectionner une question existante
Et le lecteur restitue exactement la réponse éditée et ses sources
```

## Absence de gardien

```gherkin
Étant donné un gardien absent après le début de la capsule
Quand le délai de secours est atteint
Alors l'enseignant peut réattribuer la garde ou ouvrir une voie alternative
Et la mission demeure réalisable sans pénaliser le demandeur
```

## Réponse inexistante / non vérifiée

```gherkin
Étant donné une question non prévue ou un Kristal à l'état demo/draft
Quand une consultation de production est demandée
Alors aucune réponse inventée ou texte demo n'est servi
Et un code d'erreur contrôlé est retourné
```

## Scénarios de sécurité à exécuter en intégration

- Un élève modifie l'ID de participant dans une requête : accès refusé.
- Un autre élève tente de lire les contraintes enseignant : refus et aucune fuite dans les messages.
- Réutilisation d'un code expiré ou jeton révoqué : refus.
- Deux choix simultanés du dernier rôle : un seul est confirmé (`409` pour l'autre).
- Même événement rejoué : pas de second prompt.
- Un Kristal retiré ne se publie pas dans une nouvelle séance.
- Aucune requête du lecteur ne fait appel à un service IA ou à un réseau externe.

## Validation automatisée présente

`tests/test_reference.py` contrôle la cohérence de l'exemple, les références, les statuts, les réponses exactes, les déclencheurs déterministes et les cas de refus. **Ne prétend pas** valider une attribution réelle ni un examen psychométrique.
