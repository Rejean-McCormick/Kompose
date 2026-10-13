# KOMPOSE — guide pour futurs contributeurs et agents

La priorité est de garder ce dépôt comme **référence testable et indépendante**. KOR est une application externe facultative, jamais une dépendance imposée.

## Invariants obligatoires

- Ne pas ajouter de données réelles de mineurs aux exemples, aux logs ou aux tests.
- L'Entry Door vérifie un code temporaire **et** une autorisation d'identité externe, avec une session ouverte.
- Ne jamais publier scores, classements, aménagements, affinités ou aversions dans les événements destinés aux élèves ou aux clients narratifs.
- Les décisions de distribution respectent contraintes fortes, accessibilité et validation enseignante. Aucun calcul de comparabilité psychométrique n'est prétendu par le prototype.
- Un Kristal est une ressource documentaire éditée; un gardien n'en est pas la source ni l'auteur. Les réponses restent déterministes, liées à une version et à des sources validées.
- Les exemples historiques sont fictifs et interdits comme contenu « vérifié » en production.
- La couche de coordination porte uniquement états, références et événements; IAM, stockage, messages et présentation sont des ports externes.
- Conserver l'idempotence, les versions de session, les tests et les ADR lors de tout changement de contrat.

## Checklist PR

1. Mettre à jour les docs, schémas et ADR appropriés.
2. Vérifier qu'aucun événement ou réponse publique ne contient de données sensibles.
3. Ajouter les tests positifs, négatifs, erreur et reprise.
4. Lancer `make check` (ou les commandes équivalentes du README).
5. Décrire explicitement ce qui reste **non opérationnel en production**.
