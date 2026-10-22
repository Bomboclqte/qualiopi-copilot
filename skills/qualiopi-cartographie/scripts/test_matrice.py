"""Tests : python -m unittest test_matrice (depuis ce dossier)"""
import json
import unittest

import matrice

REF = json.load(open(matrice.REFERENTIEL, encoding="utf-8"))


def nums(categories, conditions=(), date="2026-06-01"):
    return [i["num"] for i in matrice.indicateurs_applicables(REF, categories, set(conditions), date)]


class TestMatrice(unittest.TestCase):
    def test_referentiel_complet(self):
        self.assertEqual([i["num"] for i in REF["indicateurs"]], list(range(1, 34)))

    def test_of_simple_sans_certification(self):
        n = nums(["AF"])
        for absent in (3, 7, 13, 14, 15, 16, 20, 27, 28, 29, 33):
            self.assertNotIn(absent, n)
        self.assertEqual(len(n), 22)

    def test_conditions(self):
        n = nums(["AF"], ["certification", "alternance", "sous-traitance"])
        for present in (3, 7, 13, 16, 27, 28):
            self.assertIn(present, n)

    def test_indicateur_33_seulement_cfa_apres_reforme(self):
        self.assertNotIn(33, nums(["CFA"], date="2026-10-31"))
        self.assertIn(33, nums(["CFA"], date="2026-11-01"))
        self.assertNotIn(33, nums(["AF"], date="2027-01-01"))

    def test_totaux_officiels_france_competences(self):
        tout = ["certification", "alternance", "sous-traitance"]
        for cat, total in {"AF": 28, "BC": 22, "VAE": 24, "CFA": 32}.items():
            self.assertEqual(len(nums([cat], tout)), total, cat)
        self.assertEqual(len(nums(["CFA"], tout, date="2026-11-01")), 33)

    def test_statuts_et_compte(self):
        carto = {"1": [{"fichier": "site.pdf", "force": "forte"}], "2": [{"fichier": "x.xlsx", "force": "faible"}]}
        texte, compte = matrice.construire(REF, carto, ["AF"], set(), "2027-01-10", nouvel_entrant=True)
        self.assertEqual(compte, {"couvert": 1, "partiel": 1, "manquant": 20})
        self.assertIn("Réforme 2026", texte)
        self.assertIn("Nouvel entrant", texte)
        self.assertIn("2026 (33 indicateurs)", texte)

    def test_pas_de_note_reforme_avant_date(self):
        texte, _ = matrice.construire(REF, {}, ["AF"], set(), "2026-10-15", nouvel_entrant=False)
        self.assertNotIn("Réforme 2026", texte)


if __name__ == "__main__":
    unittest.main()
