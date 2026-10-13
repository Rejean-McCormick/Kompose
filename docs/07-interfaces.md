# 07 — Interfaces utilisateur et console enseignante

## Interfaces élève

| Vue | Données nécessaires | Action principale | Données interdites |
|---|---|---|---|
| Entrée | code capsule, consentement/conditions | rejoindre la séance | participants et contraintes |
| Catalogue rôles | titre, description, aptitudes, places | consulter les rôles | scores ou classement |
| Diagnostic | item accessible, progrès, outils | répondre / pause | évaluations d'autrui |
| Choix de rôle | rôles disponibles, son tour | choisir, confirmer | scores des autres |
| Tableau d'aventure | rôle personnel, missions, notifications | explorer | contraintes interpersonnelles |
| Inventaire | Kristals disponibles, détenus, demandés | ouvrir/solliciter | gardien sans autorisation explicite |
| Lecteur | thème, question, réponse, sources | sélectionner et lire | contenus non publiés |
| Comparaison | deux ensembles de sources, questions guidées | établir preuves et limites | faux équilibre factuel |

### Maquette textuelle — élève

```text
KOMPOSE / Capsule : La rivière des témoignages
─────────────────────────────────────────
TON RÔLE : CARTOGRAPHE         MISSION 03/06
« Trouve qui détient une archive liée au territoire. »
[Mes missions]   [Kristals]   [Demander un accès]

KRISTAL DISPONIBLE : ARCHIVES DU TERRITOIRE
[Choisir thème]   Territoire | Échanges | Relations
[Choisir question]  Qui a rédigé cette source ?
[Consulter]      [Voir la source]   [Ce qu'on ignore]
```

## Console enseignant

Modules : création de séance; aperçu public des rôles; suivi d'inscription et diagnostic **sans projection de scores**; adaptation; contraintes privées; vue explicable des affectations; interventions; garde et accès; suivi d'apprentissages; historique des décisions; clôture / suppression.

### Maquette textuelle — enseignant

```text
CAPSULE / SESSION S-001         ÉTAT : VALIDATION
Inscrits 20 | Diagnostics valides 18 | Résultats incomparables 2
[Passer en attribution guidée]  [Réviser aménagements]

CONTRAINTES PRIVÉES            JUSTIFICATION OBLIGATOIRE
- Sécurité / séparation en interaction requise
- Collaboration souhaitable (souple)
- Support visuel / lecture (aménagement)

PROPOSITIONS (non publiées)
Participant P-005 → Cartographe | intérêts + support disponibles
Participant P-006 → Archiviste  | compétences ciblées
[Examiner les incompatibilités] [Modifier] [Valider et publier]
```

## Accessibilité

Navigation clavier, lecteur d'écran, contraste, police redimensionnable, sous-titres pour audio/vidéo, fonctionnement lent réseau, supports multimodaux, reprise de diagnostic, temps flexible et alternative non chronométrée. Les messages narratifs ne doivent jamais divulguer un besoin d'adaptation.

## Lisibilité et discrétion

- Au projecteur : seulement code de capsule temporaire et consignes génériques.
- Sur tablette/Chromebook : informations de rôle et mission limitées à l'élève concerné.
- Les badges de type « meilleur élève » sont déconseillés; préférer les fonctions narratives et la rotation des gardes.
- L'enseignant doit pouvoir expliquer et corriger chaque attribution, y compris une proposition automatiques.
