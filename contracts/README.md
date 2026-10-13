# Contrats de KOMPOSE v0.2.0

Source de vérité de référence : `openapi.yaml` (API à construire), `events.md` (publication), `schemas/*.schema.json` (JSON Schema 2020-12) et `examples/integrations/kor.adapter.example.json` (adapter **facultatif** à une application distincte).

Les contrats ne représentent **aucun serveur en fonctionnement**. Les schémas décrivent des formes minimales, non une approbation de sécurité ou de conformité. Les validations Python du dossier `src/kompose` sont des contrôles sémantiques complémentaires.

**Invariants** : identité scolaire externe, token de séance limité, diagnostic et relations non exportés aux clients, approbation enseignante, accès Kristal versionné, idempotence, chiffrement et conservation appropriés en production. Toute migration doit disposer de tests de conformité avant retrait de l'ancien module.
