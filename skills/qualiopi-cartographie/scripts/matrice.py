"""Construit la matrice de preuves Qualiopi à partir de la cartographie produite par Claude.

Usage :
  python matrice.py --cartographie cartographie.json --categories AF,CFA \
      --date-audit 2027-03-15 [--certification] [--alternance] [--sous-traitance] [--nouvel-entrant]

cartographie.json : {"<num indicateur>": [{"fichier": "...", "pourquoi": "...", "force": "forte|faible"}]}
Écrit la matrice en Markdown sur la sortie standard.
"""
import argparse
import json
import os
import sys

REFERENTIEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "referentiel.json")
STATUT = {"couvert": "✅ couvert", "partiel": "🟠 partiel", "manquant": "❌ manquant"}


def indicateurs_applicables(ref, categories, conditions, date_audit):
    out = []
    for ind in ref["indicateurs"]:
        if not set(ind["categories"]) & set(categories):
            continue
        if ind.get("condition") and ind["condition"] not in conditions:
            continue
        if ind.get("depuis") and date_audit < ind["depuis"]:  # dates ISO : comparaison de chaînes valide
            continue
        out.append(ind)
    return out


def statut(preuves):
    if any(p.get("force") == "forte" for p in preuves):
        return "couvert"
    return "partiel" if preuves else "manquant"


def construire(ref, carto, categories, conditions, date_audit, nouvel_entrant):
    apres_reforme = date_audit >= ref["date_reforme"]
    lignes, compte = [], {"couvert": 0, "partiel": 0, "manquant": 0}
    for ind in indicateurs_applicables(ref, categories, conditions, date_audit):
        preuves = carto.get(str(ind["num"]), [])
        s = statut(preuves)
        compte[s] += 1
        notes = []
        if nouvel_entrant and ind.get("nouvel_entrant"):
            notes.append("Nouvel entrant : formalisation du processus suffit à l'audit initial.")
        if apres_reforme and ind.get("evolution_2026"):
            notes.append("⚠️ Réforme 2026 : " + ind["evolution_2026"])
        if s != "couvert":
            notes.append("Preuves attendues : " + ", ".join(ind["preuves"]))
        fichiers = "<br>".join(f"`{p['fichier']}` ({p.get('force', '?')})" for p in preuves) or "—"
        lignes.append(f"| {ind['num']} | {ind['critere']} | {ind['libelle']} | {STATUT[s]} | {fichiers} | {' '.join(notes)} |")

    total = sum(compte.values())
    entete = [
        "# Matrice de preuves Qualiopi",
        "",
        f"Catégories : {', '.join(categories)} · Conditions : {', '.join(sorted(conditions)) or 'aucune'} · "
        f"Audit prévu le {date_audit} · Référentiel {'2026 (33 indicateurs)' if apres_reforme else '2019 (32 indicateurs)'}",
        "",
        f"**{total} indicateurs applicables : {compte['couvert']} couverts, {compte['partiel']} partiels, {compte['manquant']} manquants.**",
        "",
        "| # | Critère | Indicateur | Statut | Preuves trouvées | Notes |",
        "|---|---|---|---|---|---|",
    ]
    pied = ["", "_Source du référentiel : " + ref["_source"] + "_"]
    return "\n".join(entete + lignes + pied), compte


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--cartographie", required=True)
    p.add_argument("--categories", required=True, help="AF,BC,VAE,CFA séparées par des virgules")
    p.add_argument("--date-audit", required=True, help="AAAA-MM-JJ")
    p.add_argument("--certification", action="store_true")
    p.add_argument("--alternance", action="store_true")
    p.add_argument("--sous-traitance", action="store_true")
    p.add_argument("--nouvel-entrant", action="store_true")
    a = p.parse_args(argv)

    ref = json.load(open(REFERENTIEL, encoding="utf-8"))
    categories = [c.strip().upper() for c in a.categories.split(",") if c.strip()]
    inconnues = set(categories) - set(ref["categories"])
    if inconnues:
        sys.exit(f"Catégories inconnues : {', '.join(sorted(inconnues))} (attendu : AF, BC, VAE, CFA)")
    conditions = {c for c, on in [("certification", a.certification), ("alternance", a.alternance),
                                  ("sous-traitance", a.sous_traitance)] if on}
    carto = json.load(open(a.cartographie, encoding="utf-8"))
    texte, _ = construire(ref, carto, categories, conditions, a.date_audit, a.nouvel_entrant)
    print(texte)


if __name__ == "__main__":
    main()
