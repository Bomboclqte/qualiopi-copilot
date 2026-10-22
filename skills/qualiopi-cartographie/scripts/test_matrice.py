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

    def test_force_insensible_a_la_casse(self):
        self.assertEqual(matrice.statut([{"fichier": "a", "force": "Forte "}]), "couvert")

    def test_entrees_invalides_refusees(self):
        import os, tempfile
        with tempfile.TemporaryDirectory() as d:
            ok = os.path.join(d, "ok.json")
            json.dump({"1": []}, open(ok, "w"))
            with self.assertRaises(SystemExit):
                matrice.main(["--cartographie", ok, "--categories", "AF", "--date-audit", "15/02/2027"])
            bad = os.path.join(d, "bad.json")
            json.dump({"ind-2": []}, open(bad, "w"))
            with self.assertRaises(SystemExit):
                matrice.main(["--cartographie", bad, "--categories", "AF", "--date-audit", "2027-02-15"])

    def test_cartographie_robuste(self):
        import os, tempfile
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "vrai|doc.pdf"), "w").close()
            chemin = os.path.join(d, "carto.json")
            with open(chemin, "w", encoding="utf-8-sig") as f:  # BOM du bloc-notes Windows
                json.dump({"1": [{"fichier": "vrai|doc.pdf", "force": "forte"}],
                           "2": [{"fichier": "invente.pdf", "force": "forte"}]}, f)
            carto = matrice.charger_cartographie(chemin, REF)
            texte, compte = matrice.construire(REF, carto, ["AF"], set(), "2026-06-01", False)
            self.assertEqual(compte["couvert"], 1)  # la preuve inventée ne compte pas
            self.assertIn("fichier introuvable", texte)
            self.assertIn("vrai\\|doc.pdf", texte)
            for mauvais in ({"1": "x.pdf"}, {"1": [None]}, {"1": [{"force": "forte"}]}, ["x"]):
                json.dump(mauvais, open(chemin, "w"))
                with self.assertRaises(SystemExit):
                    matrice.charger_cartographie(chemin, REF)

    def test_extraction_docx_xlsx(self):
        import os, tempfile, zipfile, extraire_texte
        with tempfile.TemporaryDirectory() as d:
            with zipfile.ZipFile(os.path.join(d, "proc.docx"), "w") as z:
                z.writestr("word/document.xml", "<w:p><w:r><w:t>Procédure &amp; registre</w:t></w:r></w:p><w:p><w:t>Ligne 2</w:t></w:p>")
            with zipfile.ZipFile(os.path.join(d, "satisf.xlsx"), "w") as z:
                z.writestr("xl/sharedStrings.xml", "<si><t>Taux</t></si>")
            open(os.path.join(d, "casse.docx"), "w").write("pas un zip")
            extraire_texte.main(d)
            ext = os.path.join(d, ".qualiopi", "extraits")
            self.assertEqual(open(os.path.join(ext, "proc.docx.txt"), encoding="utf-8").read(), "Procédure & registre\nLigne 2")
            self.assertIn("Taux", open(os.path.join(ext, "satisf.xlsx.txt"), encoding="utf-8").read())
            self.assertFalse(os.path.exists(os.path.join(ext, "casse.docx.txt")))

    def test_pas_de_note_reforme_avant_date(self):
        texte, _ = matrice.construire(REF, {}, ["AF"], set(), "2026-10-15", nouvel_entrant=False)
        self.assertNotIn("Réforme 2026", texte)


if __name__ == "__main__":
    unittest.main()
