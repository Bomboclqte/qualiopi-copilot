---
description: Audit blanc Qualiopi complet d'un dossier d'organisme de formation (cartographie des preuves puis simulation d'audit)
argument-hint: "[dossier de l'organisme]"
---

Fais un audit blanc Qualiopi du dossier : $ARGUMENTS (si vide, demande le dossier).

1. Utilise le skill `qualiopi-cartographie` pour produire `cartographie.json` et `matrice-preuves.md` (dans le dossier de sortie, par défaut le dossier analysé).
2. Lance ensuite le subagent `auditeur-qualiopi`. Transmets-lui : le dossier analysé, le dossier de sortie, les chemins de la matrice, de la cartographie et du `referentiel.json` du skill, les catégories, la date d'audit et le statut de nouvel entrant.
3. Résume à l'utilisateur en français simple : le verdict, puis les non-conformités majeures avec leur action corrective. Propose ensuite le skill `qualiopi-modeles` pour préparer les documents manquants.
