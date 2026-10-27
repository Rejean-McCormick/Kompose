# Tandem P1 — KOMPOSE validateur, pas orchestrateur opérationnel

Le code `src/kompose/lifecycle.py` et `coordination.py` sont conservés comme **modèles
purs de simulation**, indépendants de KOR. En production scolaire, ils ne peuvent
pas remplacer les transitions Orgo. Voir [ADR 0008](adr/0008-tandem-orgo-operational-authority.md).

Validation du JSON synthétique exporté depuis Kontexte :

```powershell
$env:PYTHONPATH='src'
python -m kompose.cli verify-ekole-preview examples/integrations/ekole-fete-sorciere.synthetic.json
```

Le vérificateur rejette tout champ supplémentaire (identité d'enfant, note, photo,
texte secret, token ou attribution directe). L'exemple inclus reprend les 11 étapes
du pilote Kontexte, **pas** des tâches Orgo réellement créées. Les UUID sont des
valeurs de démonstration; leur existence et leurs droits ne sont pas validés.

Pour Ekole P1, l'aperçu n'est accessible que via son outil enseignant local.
Son résultat n'est pas une preuve de qualification, un reçu Orgo, une autorisation
scolaire ni un engagement de compétence acquise.

## Sécurité du transfert P1

- Le fichier de prévisualisation reste **local, synthétique, sans authentification**; sa conformité structurelle ne prouve ni les permissions ni une WorldRelease.
- Le lecteur de l’outil Kompose interdit les clés JSON dupliquées, liens symboliques, entrées supérieures à 128 KiB et tout champ supplémentaire.
- Les tenant, World et release utilisent des UUID canonisés pour **éviter la confusion de périmètre**; leur existence et leur correspondance ne sont **pas prouvées**.
- Le passage au runtime exigera une opération distincte, authentifiée et autorisée par Orgo, sous supervision enseignante. Aucun élève réel dans ce lot.
- Wiki facultatif : aucune donnée d’interopérabilité ni de sécurité n’est lue depuis les pages de wiki.
