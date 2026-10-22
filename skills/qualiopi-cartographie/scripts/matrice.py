"""Construit la matrice de preuves Qualiopi à partir de la cartographie produite par Claude.

Usage :
  python matrice.py --cartographie cartographie.json --categories AF,CFA \
      --date-audit 2027-03-15 [--certification] [--alternance] [--sous-traitance] [--nouvel-entrant] \
      [--sortie matrice-preuves.md]

cartographie.json : {"<num indicateur>": [{"fichier": "...", "pourquoi": "...", "force": "forte|faible"}]}
Écrit la matrice en Markdown dans --sortie (ou sur la sortie standard).
"""
import argparse
import json
import os
import sys
from datetime import date

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
    preuves = [p for p in preuves if not p.get("introuvable")]
    if any(str(p.get("force", "")).strip().lower() == "forte" for p in preuves):
        return "couvert"
    return "partiel" if preuves else "manquant"


def charger_cartographie(chemin, ref):
    """Lit et valide la cartographie ; marque les fichiers cités qui n'existent pas."""
    try:
        carto = json.load(open(chemin, encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"Cartographie illisible ({chemin}) : {e}")
    if not isinstance(carto, dict):
        sys.exit("Cartographie invalide : attendu un objet {\"1\": [ {\"fichier\": ...} ], ...}")
    inconnues = sorted(set(carto) - {str(i["num"]) for i in ref["indicateurs"]})
    if inconnues:
        sys.exit(f"Clés inconnues dans la cartographie : {', '.join(inconnues)} (attendu : numéros d'indicateur, ex. \"1\" à \"33\")")
    base = os.path.dirname(os.path.abspath(chemin))
    for num, preuves in carto.items():
        if not isinstance(preuves, list) or not all(isinstance(p, dict) and p.get("fichier") for p in preuves):
            sys.exit(f"Indicateur {num} : attendu une liste de {{\"fichier\": ..., \"pourquoi\": ..., \"force\": ...}}")
        for p in preuves:
            p["introuvable"] = not os.path.exists(os.path.join(base, p["fichier"]))
    return carto


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
        fichiers = "<br>".join(
            f"`{p['fichier']}` ({'⚠️ fichier introuvable' if p.get('introuvable') else p.get('force', '?')})"
            for p in preuves).replace("|", "\\|") or "—"
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
    p.add_argument("--sortie", help="fichier Markdown à écrire (sinon sortie standard)")
    a = p.parse_args(argv)

    ref = json.load(open(REFERENTIEL, encoding="utf-8"))
    categories = [c.strip().upper() for c in a.categories.split(",") if c.strip()]
    inconnues = set(categories) - set(ref["categories"])
    if inconnues or not categories:
        sys.exit(f"Catégories inconnues ou absentes : {', '.join(sorted(inconnues))} (attendu : AF, BC, VAE, CFA)")
    conditions = {c for c, on in [("certification", a.certification), ("alternance", a.alternance),
                                  ("sous-traitance", a.sous_traitance)] if on}
    try:
        a.date_audit = date.fromisoformat(a.date_audit).isoformat()
    except ValueError:
        sys.exit(f"Date d'audit invalide : {a.date_audit} (format attendu AAAA-MM-JJ, ex. 2027-02-15)")
    carto = charger_cartographie(a.cartographie, ref)
    texte, compte = construire(ref, carto, categories, conditions, a.date_audit, a.nouvel_entrant)
    if a.sortie:
        with open(a.sortie, "w", encoding="utf-8") as f:
            f.write(texte + "\n")
        print(f"Matrice écrite : {a.sortie} ({sum(compte.values())} indicateurs applicables : "
              f"{compte['couvert']} couverts, {compte['partiel']} partiels, {compte['manquant']} manquants)")
    else:
        sys.stdout.reconfigure(encoding="utf-8")  # sinon les emojis plantent sur une console Windows
        print(texte)


if __name__ == "__main__":
    main()
