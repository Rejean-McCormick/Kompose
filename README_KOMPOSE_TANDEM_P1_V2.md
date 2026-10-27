# KOMPOSE / TANDEM / P1 — Correctif V2 du chemin du wiki sous Windows

Erreur V1 : `[ECHEC] Missing test source: wiki`. Ton wiki est un **dépôt voisin** :

- Code : `C:\mycode\Ekole\Kompose`
- Wiki : `C:\mycode\Ekole\Kompose.wiki`

**La V1 n'a rien installé** (PREVIEW READY, INSTALL refusé, VERIFY READY).
La V2 se pose sur le snapshot original avec son propre installateur. Les lanceurs V1 peuvent rester sur place mais ne doivent pas être relancés.

Extraire cette archive dans `C:\mycode\Ekole\Kompose` puis :

```powershell
.\PREVIEW_KOMPOSE_TANDEM_P1_V2.cmd
.\INSTALL_KOMPOSE_TANDEM_P1_V2.cmd
.\VERIFY_KOMPOSE_TANDEM_P1_V2.cmd
```

Retour arrière : `.\ROLLBACK_KOMPOSE_TANDEM_P1_V2.cmd`.

Le wiki reste **hors du dépôt, inchangé**, et seules ses pages Markdown sont recopiées dans le bac à sable temporaire pour la suite de tests. Si le wiki n'est pas trouvé, l'installateur refuse la pose. Aucune base, compte enfant, API Orgo, Docker ou VPS ne sont modifiés.

Les fichiers du dépôt sont verrouillés par les empreintes SHA-256 du snapshot original. La V2 corrige aussi les liens du README et de l'index documentaire, ainsi que `tests/test_wiki.py` pour détecter le dépôt voisin pendant les tests natifs. Sauvegardes sous `C:\mycode\Ekole\Tandem_Local\kompose_tandem_orgo_ekole_p1_v2\backups`.
