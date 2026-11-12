# Proposition de personnages et de rôles Ékole — 2026-11-11

Les 38 personnages-métiers viennent de `Kontexte/data/roles` et leurs identifiants visuels de Kolor. Kompose ne doit pas créer un deuxième catalogue. Les `role_code` de la mission sont des **perspectives narratives**, pas des autorisations de Work ou de World. Attribuer un personnage exige une identité autorisée, les besoins de l'enfant, l'accessibilité, un équilibre des rôles et **l'approbation d'un enseignant**.

`src/kompose/tandem_handoff.py` vérifie le schéma fermé de l'aperçu Ékole, les rôles, les dépendances déjà connues et l'état initial `ready` / `waiting`. Il ne produit aucun `TaskAssignment` réel. Le contrôleur de conformité croisé vérifie désormais les 6 nouvelles missions + la fête sans modifier ce contrat. Les profils, scores et aménagements ne doivent jamais être exposés à Kidaxion ni aux autres enfants.
