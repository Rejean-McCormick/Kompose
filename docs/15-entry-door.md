# 15 — Entry Door : entrée dans une capsule

## Découpage d'accès

1. Un enseignant autorisé choisit une capsule et configure la session (version de contenu épinglée, rôles, places, politique de diagnostic et date de fin).
2. Un fournisseur IAM scolaire valide l'identité; le code temporaire de capsule **ne vaut pas preuve d'identité**.
3. L'élève saisit le code sur Chromebook/tablette dans une page HTML sans installation et reçoit uniquement son identifiant pseudonyme de session.
4. Le serveur vérifie la durée de vie du code, l'autorisation de rejoindre le groupe, la capacité et l'état `inscriptions`.
5. L'élève voit les fiches de rôles **publiques** puis commence ou reprend son diagnostic adapté.
6. Un élève déjà inscrit retrouve le même identifiant de session, sans réservation doublonnée.

## Stratégie de sécurité

- Générer des codes aléatoires à expiration rapide, sans données personnelles dans le code ou l'URL. Limiter les tentatives et régénérer au besoin.
- Utiliser un IAM fourni par l'école et des scopes par session, enseignant / élève / éditeur; séparer stockage IAM et session.
- Appliquer toutes les décisions côté serveur; une interface ne fait qu'afficher les choix autorisés.
- Ne jamais fournir le code serveur en clair au navigateur ni accepter `authenticated=true` envoyé par celui-ci.
- Limiter les métadonnées exposées lors d'un échec; journal d'accès limité et pseudonymisé.
- Prévoir déconnexion, poste partagé, réinscription, accessibilité clavier / lecteur d'écran et scénario hors ligne avec médiation enseignante.

## Démonstration incluse

`kompose.entry.may_join` teste une combinaison de préconditions. Il ne crée pas de code et **ne remplace pas** une authentification. Ses booléens `authenticated` et `enrolled` doivent provenir de composants de confiance. La simulation `demo-flow` injecte volontairement des valeurs fictives.

## Cas d'acceptation

- Code expiré ou erroné : refus.
- Code valide mais identité ou classe non autorisée : refus.
- Session complète : refus ou file d'attente définie par enseignant, jamais ajout silencieux.
- Reconnexion du même élève autorisé : récupérer l'état antérieur, pas créer un nouveau participant.
- Rôle public : aucun score, contrainte relationnelle ou raison personnelle n'est rendu.
