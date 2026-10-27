# Kompose Tandem P1 V3 — Interop + Sécurité

**Pourquoi V3?** Les V1/V2 ont échoué au test de documentation wiki; la V2 a été refusée avant installation. Ce lot ne dépend plus de `Kompose.wiki`. Aucun changement du wiki et aucune condition requise à son existence.

## Installation

Extraire ce ZIP dans `C:\mycode\Ekole\Kompose`.

1. `PREVIEW_KOMPOSE_TANDEM_INTEROP_P1_V3.cmd`
2. `INSTALL_KOMPOSE_TANDEM_INTEROP_P1_V3.cmd`
3. `VERIFY_KOMPOSE_TANDEM_INTEROP_P1_V3.cmd`

Pour restaurer : `ROLLBACK_KOMPOSE_TANDEM_INTEROP_P1_V3.cmd`. Sauvegardes : `C:\mycode\Ekole\Tandem_Local\kompose_tandem_interop_p1_v3\backups`. Contrôle SHA256 avant modification, pas de DB/VPS/réseau.

## Couverture réelle

Le pré-contrôle exécute la compilation, les tests Python **hors les 5 tests de wiki et un test des liens documentaires** (signalés comme différés), la validation du JSON Ekole et la validation de capsule. Il ne lance ni Orgo, ni authentification scolaire, ni élèves réels. Les chaînes JSON sont limitées, les doublons rejetés, les données privées inattendues refusées. L’accès enseignant appartient à Ekole; l’affectation et le workflow réel appartiennent à Orgo.

**Aucun nouveau fichier n'est copié par simple extraction** (sauf scripts, manifeste, payload). Le correctif ne modifie pas `Kompose.wiki`.
