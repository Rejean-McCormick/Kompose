# KOMPOSE / TANDEM / ORGO / EKOLE / P1 — Installation locale

Correctif P1 ciblé, **sans déploiement, compte enfant ni appel Orgo**.

1. Extraire uniquement cette archive dans la racine `Kompose` existante.
2. Dans PowerShell 7, appeler les trois lanceurs :

```powershell
.\PREVIEW_KOMPOSE_TANDEM_P1.cmd
.\INSTALL_KOMPOSE_TANDEM_P1.cmd
.\VERIFY_KOMPOSE_TANDEM_P1.cmd
```

Le programme vérifie les empreintes **SHA-256 de l'ancien état et du nouveau payload**.
Refus si dérive locale; aucun fichier n'est écrasé sans sauvegarde.
L'installation teste une **copie temporaire** puis reteste après copie.
Sauvegardes en dehors du dépôt : `..\Tandem_Local\kompose_tandem_orgo_ekole_p1\backups`.
Retour arrière : `.\ROLLBACK_KOMPOSE_TANDEM_P1.cmd` (refuse les modifications ultérieures).

**Le processus n'utilise ni Docker, ni DB, ni API Orgo, ni données réelles d'enfants.**
Les UUID du pilote sont des valeurs de fixture, pas des identifiants d'un World réel.
Une vérification structurelle n'est **pas** une autorisation ou une admission Orgo.
