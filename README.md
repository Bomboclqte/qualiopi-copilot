# Qualiopi Copilot

**Préparez votre audit Qualiopi à partir de vos propres documents, avec Claude Code.**

Vous dirigez un organisme de formation, un centre de bilans de compétences, un accompagnement VAE ou un CFA ? Qualiopi Copilot lit votre dossier (programmes, site, questionnaires, CV, procédures…) et vous donne trois choses :

1. **Une matrice de preuves.** Pour chaque indicateur qui vous concerne : quels fichiers le prouvent, s'ils suffisent, et ce qui manque.
2. **Un audit blanc.** Un auditeur exigeant passe votre dossier au crible, indicateur par indicateur (conforme, non-conformité mineure ou majeure), puis vous donne le plan d'action et les questions qu'on posera à vos formateurs.
3. **Les documents manquants, à compléter.** Procédure de réclamation, questionnaire d'analyse du besoin, registre d'amélioration… Ils sont adaptés à vos vraies formations. Ce sont des outils à faire vivre, **jamais de fausses preuves**.

> ⚠️ **Réforme du 1er novembre 2026 incluse.** Le décret n° 2026-728 fait passer le référentiel à 33 indicateurs et modifie 11 d'entre eux. Qualiopi Copilot applique automatiquement la bonne version selon la date de votre prochain audit.

---

## Installation

Il vous faut [Claude Code](https://claude.com/claude-code) (version 2.1.275 ou plus récente) et Python 3.

Dans Claude Code, tapez :

```
/plugin install qualiopi-copilot --marketplace VOTRE_COMPTE/qualiopi-copilot
```

Redémarrez ensuite Claude Code.

## Utilisation

Ouvrez Claude Code **dans le dossier qui contient vos documents Qualiopi** (ou un dossier Google Drive synchronisé sur votre ordinateur), puis tapez :

```
/qualiopi-copilot:audit-blanc .
```

Claude vous demande ce qu'il ne peut pas deviner :
- vos catégories d'actions ;
- si vous préparez à une certification RNCP/RS ;
- si vous faites de l'alternance ou de la sous-traitance ;
- la date de votre prochain audit.

Il dépose ensuite trois fichiers dans votre dossier :

| Fichier | Contenu |
|---|---|
| `matrice-preuves.md` | Les indicateurs avec leur statut ✅ couvert, 🟠 partiel ou ❌ manquant |
| `rapport-audit-blanc.md` | Le verdict, les non-conformités, le plan d'action et les questions d'entretien |
| `cartographie.json` | Le détail des documents rattachés à chaque indicateur |

Vous pouvez aussi parler naturellement : *« Où en est-on pour Qualiopi ? »*, *« Prépare-moi une procédure de réclamation »*, *« Fais-moi un audit blanc »*.

### Essayer sans vos documents

Le dépôt contient un faux organisme, « Bureautik Conseil », avec des manques volontaires. Pour l'essayer :

```bash
git clone https://github.com/VOTRE_COMPTE/qualiopi-copilot
cd qualiopi-copilot/exemple/organisme-demo
claude --plugin-dir ../..
```

Puis : `/qualiopi-copilot:audit-blanc .`

Vous pouvez aussi voir le résultat sans rien installer, dans [`exemple/resultats-demo/`](exemple/resultats-demo/). Sur cet organisme, l'audit blanc conclut « non certifiable en l'état ». Il a même repéré que le catalogue annonce « 96 %, 52 stagiaires » alors que le fichier de satisfaction ne compte que 21 stagiaires.

## Ce qu'il y a dedans

| Élément | Type | Rôle |
|---|---|---|
| `qualiopi-cartographie` | Skill | Range chaque document sous les indicateurs et calcule la matrice |
| `qualiopi-modeles` | Skill | Prépare les documents manquants, à compléter |
| `auditeur-qualiopi` | Agent | Simule l'audit blanc. Il lit seulement vos documents et n'écrit que le rapport |
| `/qualiopi-copilot:audit-blanc` | Commande | Enchaîne tout |

Le référentiel est dans `skills/qualiopi-cartographie/referentiel.json`. L'applicabilité de chaque indicateur par catégorie suit le tableau officiel de France compétences : 28 indicateurs pour les actions de formation, 22 pour les bilans, 24 pour la VAE, 32 pour l'apprentissage, et 33 à partir du 1er novembre 2026.

## À lire avant de l'utiliser

- **C'est une simulation.** Seul un organisme certificateur accrédité délivre Qualiopi. Le guide de lecture officiel en vigueur fait foi pour les preuves recevables.
- **Réforme 2026 : textes encore attendus.** Les arrêtés qui fixent les seuils des indicateurs 19 et 20, et la nouvelle version du guide de lecture, n'étaient pas parus quand cette version a été écrite.
- **Vos données.** Vos documents sont lus par Claude, le modèle d'Anthropic, comme tout ce que vous ouvrez dans Claude Code. Si vos dossiers contiennent des données personnelles d'apprenants, pseudonymisez-les ou vérifiez que votre usage respecte le RGPD.
- **Aucune fausse preuve.** Le plugin refuse d'inventer des résultats, des signatures ou des comptes rendus. Une preuve, c'est ce que vous faites réellement.

## Pour les contributeurs

```bash
cd skills/qualiopi-cartographie/scripts && python3 -m unittest test_matrice   # tests du calcul
claude plugin validate .                                                        # manifeste
claude plugin eval .                                                            # évaluations (consomme des tokens)
```

Les signalements d'erreur dans le référentiel sont les contributions les plus précieuses. Citez le texte officiel.

## Licence

MIT. Voir [LICENSE](LICENSE).
