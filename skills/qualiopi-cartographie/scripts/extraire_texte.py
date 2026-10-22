"""Extrait le texte des fichiers Word, Excel et PowerPoint (DOCX, XLSX, PPTX), que l'outil Read ne lit pas.

Usage : python3 extraire_texte.py <dossier analysé>
Écrit un .txt par document dans <dossier>/.qualiopi/extraits/ (même arborescence) et liste ce qui a été extrait.
Bibliothèque standard uniquement.
"""
import os
import re
import sys
import zipfile

PARTIES = {".docx": r"word/(document|header\d*|footer\d*)\.xml",
           ".pptx": r"ppt/slides/slide\d+\.xml",
           ".xlsx": r"xl/(sharedStrings|worksheets/sheet\d+)\.xml"}
IGNORE = {".git", ".qualiopi", "node_modules", "modeles-a-completer"}


def texte_office(chemin):
    motif = re.compile(PARTIES[os.path.splitext(chemin)[1].lower()])
    morceaux = []
    with zipfile.ZipFile(chemin) as z:
        for nom in sorted(n for n in z.namelist() if motif.fullmatch(n)):
            xml = z.read(nom).decode("utf-8", "replace")
            xml = re.sub(r"</(w:p|a:p|row)>", "\n", xml)  # fins de paragraphe et de ligne
            xml = re.sub(r"</(w:tc|c)>", " | ", xml)      # fins de cellule
            morceaux.append(re.sub(r"<[^>]+>", "", xml))
    texte = "\n".join(morceaux)
    for ent, car in (("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&apos;", "'"), ("&amp;", "&")):
        texte = texte.replace(ent, car)
    return re.sub(r"\n\s*\n+", "\n", texte).strip()


def main(dossier):
    sortie = os.path.join(dossier, ".qualiopi", "extraits")
    faits = 0
    for racine, dirs, fichiers in os.walk(dossier):
        dirs[:] = [d for d in dirs if d not in IGNORE]
        for f in fichiers:
            if os.path.splitext(f)[1].lower() not in PARTIES or f.startswith("~$"):
                continue
            src = os.path.join(racine, f)
            rel = os.path.relpath(src, dossier)
            try:
                texte = texte_office(src)
            except (zipfile.BadZipFile, KeyError, OSError) as e:
                print(f"illisible : {rel} ({e})")
                continue
            dest = os.path.join(sortie, rel + ".txt")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8") as out:
                out.write(texte)
            faits += 1
            print(f"{rel} -> {os.path.relpath(dest, dossier)}")
    print(f"{faits} document(s) extrait(s)")


if __name__ == "__main__":
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        sys.exit("Usage : python3 extraire_texte.py <dossier>")
    main(sys.argv[1])
