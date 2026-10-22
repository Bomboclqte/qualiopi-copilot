---
name: qualiopi-modeles
description: Prépare, pour un organisme de formation, les documents Qualiopi qui manquent (procédure de réclamation, questionnaire d'analyse du besoin, livret d'accueil, registre d'amélioration, tableau de veille, etc.), adaptés à son activité réelle et à compléter par lui. À utiliser après une matrice de preuves Qualiopi, ou quand l'utilisateur demande un modèle de document pour un indicateur Qualiopi.
---

# Modèles Qualiopi à compléter

Tu prépares les documents manquants **à partir de l'activité réelle** de l'organisme, jamais un kit générique : depuis la réforme du 1er novembre 2026, l'auditeur interroge formateurs et apprenants, et un document générique ne résiste pas à l'entretien.

## Règle absolue : un modèle n'est pas une preuve

- Tu crées des **outils à utiliser**, jamais des preuves déjà remplies.
- N'invente **aucun** résultat (taux de satisfaction, taux de réussite), aucune signature, aucun nom de bénéficiaire, aucune date passée, aucun compte rendu de réunion qui n'a pas eu lieu. Fabriquer une preuve pour un audit est une fraude.
- Chaque information que seul l'organisme connaît est un champ visible : `[À COMPLÉTER : ...]`.

## Étapes

1. **Partir des manques.** Lis `matrice-preuves.md` s'il existe (produite par le skill `qualiopi-cartographie`), sinon demande les indicateurs visés.
2. **Apprendre l'organisme.** Lis son catalogue, ses programmes, son site : thématiques, publics, durées, modalités (présentiel, distanciel), catégories (AF, BC, VAE, CFA). Reprends son vocabulaire et ses vraies formations dans les exemples.
3. **Rédiger** dans `<dossier>/modeles-a-completer/`, un fichier `.md` par document, nommé `ind-<num>-<objet>.md` (ex. `ind-31-procedure-reclamation.md`). Chaque fichier commence par :
   - l'indicateur couvert et ce que l'auditeur vérifie ;
   - **comment le faire vivre** : qui le remplit, quand, où le ranger. C'est ce qui le transforme en preuve forte ;
   - si l'audit tombe après le 1er novembre 2026 et que l'indicateur est modifié, les ajouts de la réforme (voir `evolution_2026` dans le `referentiel.json` du skill `qualiopi-cartographie`).
4. **Rester court.** Une procédure Qualiopi utile tient sur une page. Préfère un tableau à remplir à un long texte.
5. **Finir par une liste d'actions** : document par document, ce que l'organisme doit faire cette semaine pour qu'il devienne une preuve (première utilisation datée).

## Documents qui reviennent le plus

| Indicateur | Document |
|---|---|
| 2 | Tableau des indicateurs de résultats publiés, avec date de mise à jour |
| 4 | Questionnaire d'analyse du besoin (bénéficiaire et entreprise ou financeur) |
| 8 | Test ou grille de positionnement à l'entrée |
| 9 | Livret d'accueil et convocation type |
| 12 | Procédure de prévention des abandons ; depuis 2026, conduite à tenir en cas de violence, harcèlement ou discrimination |
| 23 à 25 | Tableau de veille : source, date, information, action décidée |
| 26 | Fiche référent handicap et annuaire des partenaires |
| 30 | Questionnaires à chaud et à froid, sans oublier les financeurs |
| 31 | Procédure et registre des réclamations |
| 32 | Registre d'amélioration : origine, action, responsable, date prévue, date réalisée ; depuis 2026, analyse des risques qualité |
| 33 (CFA, 2026) | Évaluation des enseignements par les apprentis, distincte de la satisfaction |
