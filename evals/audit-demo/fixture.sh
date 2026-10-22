#!/bin/bash
# Recrée le faux organisme Bureautik Conseil (copie de exemple/organisme-demo) dans le dossier de travail de l'éval.
set -e
mkdir -p "dossier/equipe"
cat > "dossier/equipe/cv-formateur-julie-martin.md" <<'FIN_FICHIER'
# Julie Martin — formatrice bureautique
15 ans d'expérience, certifiée Microsoft Office Specialist Expert Excel (2022). Formatrice chez Bureautik Conseil depuis 2019.
FIN_FICHIER
mkdir -p "dossier/pedagogie"
cat > "dossier/pedagogie/quiz-positionnement-excel.md" <<'FIN_FICHIER'
# Quiz de positionnement Excel (10 questions) — modèle vierge
1. Qu'est-ce qu'une référence absolue ? ...
FIN_FICHIER
mkdir -p "dossier/qualite"
cat > "dossier/qualite/procedure-reclamation.md" <<'FIN_FICHIER'
# Procédure de réclamation (modèle)
1. Le client envoie sa réclamation par e-mail.
2. Réponse sous 8 jours.
3. Action corrective si besoin.
Registre des réclamations : [vide]
FIN_FICHIER
mkdir -p "dossier/qualite"
cat > "dossier/qualite/reglement-interieur.md" <<'FIN_FICHIER'
# Règlement intérieur — Bureautik Conseil
Version du 03/09/2025. Horaires 9h-17h. Règles d'hygiène et de sécurité, discipline, sanctions, représentation des stagiaires (formations > 500 h non concernées).
FIN_FICHIER
mkdir -p "dossier/qualite"
cat > "dossier/qualite/satisfaction-2025.csv" <<'FIN_FICHIER'
session,date,stagiaires,note_moyenne_sur_5,taux_satisfaits
Excel-perf,2025-03-12,6,4.7,100%
Excel-perf,2025-06-18,8,4.5,88%
Excel-perf,2025-10-02,7,4.8,100%
FIN_FICHIER
mkdir -p "dossier/site"
cat > "dossier/site/catalogue-2026.md" <<'FIN_FICHIER'
# Formation Excel perfectionnement — Bureautik Conseil (Lyon)
Mis à jour le 12/01/2026
- Public : salariés et demandeurs d'emploi utilisant déjà Excel
- Prérequis : savoir créer un tableau simple
- Objectifs : à l'issue de la formation, le stagiaire sera capable de construire un tableau croisé dynamique, d'utiliser RECHERCHEX et de créer un graphique combiné.
- Durée : 14 heures (2 jours)
- Tarif : 690 € HT par stagiaire en inter-entreprise
- Délai d'accès : 15 jours après la demande
- Modalités : présentiel, salle de 8 places, 1 PC par stagiaire
- Évaluation : quiz de positionnement, exercices pratiques, quiz final
- Contact : contact@bureautik-conseil.fr — 04 00 00 00 00
- Taux de satisfaction 2025 : 96 % (52 stagiaires)
FIN_FICHIER
