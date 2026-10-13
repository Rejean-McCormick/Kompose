# Contribuer à KOMPOSE

1. Décrire le besoin et **la responsabilité visée** (Entry Door, diagnostic, casting, coordination, Kristals, interaction, adaptation, supervision ou clôture).
2. Préciser l'interface partenaire concernée : KOMPOSE ne doit pas supposer que KOR ou un IAM particulier est toujours présent.
3. Documenter les implications en droits des mineurs, accessibilité, connaissance documentaire et confidentialité; aucun profil réel d'élève dans les fixtures ou PR.
4. Pour une décision qui change l'architecture ou une politique sensible, ajouter un **ADR** dans `docs/adr/`.
5. Modifier les JSON Schema/OpenAPI et tests de contrat de façon synchrone; changement incompatible = nouvelle version majeure.
6. Exécuter `PYTHONPATH=src python3 -m unittest discover -s tests -v` et `PYTHONPATH=src python3 -m kompose.cli validate examples/capsule-rivieres`.
7. Distinguer clairement **specification**, **simulation**, et **production** dans tout commit ou pull request.

La décision de licence reste ouverte : consulter [LICENSE-TO-DECIDE.md](LICENSE-TO-DECIDE.md).
