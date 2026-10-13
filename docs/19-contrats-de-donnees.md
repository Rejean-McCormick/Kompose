# 19 — Contrats, sécurité des données et événements

## Objets publics / privés

| Catégorie | Exemples | Autorisation |
|---|---|---|
| Public dans la session | rôle disponible, description, titre de mission, question du Kristal publiée | élève inscrit |
| Privé à l'élève | son rôle, sa progression, son accès Kristal | lui-même + enseignant autorisé |
| Privé enseignement | score brut, comparabilité, aménagement, affinité/aversion, contraintes de sécurité | enseignant avec besoin légitime / service spécialisé |
| Éditorial | sources, droits, révision, perspective, version | éditeur habilité |
| Événement minimal | références opaques, type, horodatage, version | services sur liste blanche |

## Étapes d'attribution

`diagnostic.termine` privé → `allocation.preview` privé → correction de conflits par l'enseignant → `session.roles_publies` public minimal. Le score ne doit jamais être présent dans le payload de publication.

## Transactions

`expected_session_version` requis pour publier les rôles, changer une phase ou transférer une garde. Pour éviter des effets en double, `Idempotency-Key` côté API et `event_id` dans l'outbox. Après relance, une commande rejouée doit rendre le même résultat ou un conflit clair, jamais une double attribution.

## Sources documentaires

La question est choisie parmi des clés définies, pas analysée par une IA libre. Un identifiant exact résout une réponse versionnée avec références et limites. Un thème nouveau exige une revue éditoriale; mode `demo` jamais rendu comme fait historique approuvé.

## Contrats consultables

- `contracts/openapi.yaml` : opérations HTTP de référence, **non hébergées**.
- `contracts/events.md` : événements et règles de diffusion.
- `contracts/schemas/` : schémas JSON 2020-12.
- `examples/integrations/kor.adapter.example.json` : adaptateur facultatif illustratif.
