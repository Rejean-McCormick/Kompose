# Pilotage B6 : boulangerie fictive en 3e année

Ces JSON sont **des copies non modifiées** de `znapshot_Kontexte_10152150.zip`, pour permettre des tests totalement autonomes. Aucune donnée d'élève.

La mission **source** est un squelette à relire, et vise `qc-pri-ma-006`. La cible expérimentale Ekole `qc-pri-ma-008` ne doit pas être ajoutée sans revue de B1/B5/B2.

## Démonstration (Python 3.10+ ; aucune dépendance supplémentaire)

Depuis la racine de `kompose` :

```powershell
$env:PYTHONPATH="src"
python -m kompose.cli preview-kontexte examples/kontexte-boulangerie/data/missions/boulangerie.json examples/kontexte-boulangerie/data/roles --target-course qc-pri-ma-008 --replay examples/kontexte-boulangerie/mock-orgo-receipts.json --out resultat-boulangerie.json
```

Variante élève, qui ne reçoit **ni réponses cachées ni contenu de fragment** :

```powershell
python -m kompose.cli preview-kontexte examples/kontexte-boulangerie/data/missions/boulangerie.json examples/kontexte-boulangerie/data/roles --role boulanger
```

Mode enseignant lorsqu'un partenaire est absent :

```powershell
python -m kompose.cli preview-kontexte examples/kontexte-boulangerie/data/missions/boulangerie.json examples/kontexte-boulangerie/data/roles --absent-role fermier
```

**Attention :** `mock-orgo-receipts.json` rejoue des faits *supposés* (révisions 1 à 7). Les fragments d'information ne sont pas libérés réellement. La jointure `indice-un` + `indice-deux` n'est **pas installée dans Orgo**. Le test montre qu'une future implémentation devra refuser la `phase-3` tant que les deux validations d'accès n'ont pas été confirmées.

Pour une fixture Orgo de **préparation uniquement**, Kontexte possède déjà `python -m kontexte.cli orgo-fixture boulangerie --out ...` (vérifier la CLI exacte de la version fournie), à faire valider avec le Scenario Injector d'un **Orgo de test autorisé**. Ne pas utiliser l'outil de replay de KOMPOSE comme si c'était un client Orgo.
