# -*- coding: utf-8 -*-
"""
idiomatique.py
Séance 4 — Partie A : Python plus idiomatique.

On reprend les taux de la séance 1 et des boucles écrites en séance 2,
puis on les réécrit de façon plus « pythonique » :

A.1 — Les compréhensions : de liste ([x*2 for x in liste]) et de dictionnaire.
A.2 — enumerate (indice + valeur), zip (associer deux listes),
      sorted(..., key=...) (trier selon un critère).
A.3 — f-strings (formater nombres et dates), lambda avec map et filter.

Pour chaque notion : la version « avant » (style séance 2) puis la version
« après » (idiomatique), et on vérifie que les deux donnent le même résultat.

Uniquement la bibliothèque standard : csv, datetime, pathlib.
"""

import csv
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------
# Paramètres
# ---------------------------------------------------------------------
DEVISE = "USD"
NOM_CSV = f"EUR_{DEVISE}_2026-01-01_2026-09-01.csv"

DOSSIER_SCRIPT = Path(__file__).resolve().parent
DOSSIER_PROJET = DOSSIER_SCRIPT.parent
EMPLACEMENTS_POSSIBLES = [
    DOSSIER_SCRIPT / "donnees" / NOM_CSV,
    DOSSIER_PROJET / "SEANCE 3" / "donnees" / NOM_CSV,
    DOSSIER_PROJET / "SEANCE 2" / "donnees" / NOM_CSV,
    DOSSIER_PROJET / "SEANCE 1" / "donnees" / NOM_CSV,
]


def titre(texte):
    """Affiche un titre de partie encadré."""
    print(f"\n{'=' * 70}\n{texte}\n{'=' * 70}")


def verifier(nom, avant, apres):
    """Affiche si les versions « avant » et « après » donnent le même résultat.

    Paramètres :
        nom (str) : ce qu'on compare.
        avant     : le résultat de la version classique.
        apres     : le résultat de la version idiomatique.
    """
    symbole = "✅" if avant == apres else "❌"
    print(f"   {symbole} {nom} : même résultat avant / après → {avant == apres}")


# =====================================================================
# LECTURE DES DONNÉES (déjà en version idiomatique)
# =====================================================================

def trouver_csv(emplacements):
    """Renvoie le premier chemin existant de la liste, ou None."""
    # next() + générateur : on s'arrête au premier chemin qui existe
    return next((chemin for chemin in emplacements if chemin.exists()), None)


def lire_csv(chemin):
    """Lit le CSV des taux et renvoie une liste de couples (date, taux).

    Version séance 2 : une boucle for + append.
    Version idiomatique : une compréhension de liste.

    Paramètre :
        chemin (Path) : le CSV avec les colonnes « date » et « taux ».
    Renvoie :
        list de tuples (date, float).
    """
    with open(chemin, newline="", encoding="utf-8") as fichier:
        return [(date.fromisoformat(ligne["date"]), float(ligne["taux"]))
                for ligne in csv.DictReader(fichier)]


# =====================================================================
# A.1 — LES COMPRÉHENSIONS
# =====================================================================

def partie_a1(dates, taux):
    """Compréhensions de liste et de dictionnaire (avant / après).

    Paramètres :
        dates (list de date)  : les dates.
        taux  (list de float) : les taux, dans le même ordre.
    Renvoie :
        list de float : les variations jour à jour en %.
    """
    titre("A.1 — LES COMPRÉHENSIONS")

    # --- Compréhension de liste : les variations jour à jour en % ---
    print("1) Liste des variations jour à jour (en %)")

    # AVANT (style séance 2) : une boucle for + append
    variations_avant = []
    for i in range(1, len(taux)):
        variation = (taux[i] / taux[i - 1] - 1) * 100
        variations_avant.append(variation)

    # APRÈS : une compréhension de liste, en une ligne
    variations = [(taux[i] / taux[i - 1] - 1) * 100 for i in range(1, len(taux))]

    print(f"   5 premières : {[round(v, 3) for v in variations[:5]]}")
    verifier("variations", variations_avant, variations)

    # --- Compréhension de liste avec condition : les jours de hausse ---
    print("\n2) Compréhension avec un filtre (if) : variations positives seulement")
    hausses = [v for v in variations if v > 0]
    print(f"   {len(hausses)} jours de hausse sur {len(variations)}")

    # --- Compréhension de dictionnaire : date → taux ---
    print("\n3) Compréhension de dictionnaire : {date: taux}")

    # AVANT : boucle + affectation clé par clé
    taux_par_date_avant = {}
    for i in range(len(dates)):
        taux_par_date_avant[dates[i].isoformat()] = taux[i]

    # APRÈS : compréhension de dictionnaire (avec zip, vu en A.2)
    taux_par_date = {d.isoformat(): t for d, t in zip(dates, taux)}

    print(f"   taux_par_date['{dates[1].isoformat()}'] = {taux_par_date[dates[1].isoformat()]}")
    verifier("dictionnaire", taux_par_date_avant, taux_par_date)

    # --- Compréhension de dictionnaire : moyenne par mois ---
    print("\n4) Compréhension de dictionnaire : moyenne des taux par mois")
    mois_presents = sorted({d.strftime("%Y-%m") for d in dates})   # compréhension d'ensemble
    moyenne_par_mois = {
        mois: sum(t for d, t in zip(dates, taux) if d.strftime("%Y-%m") == mois)
              / sum(1 for d in dates if d.strftime("%Y-%m") == mois)
        for mois in mois_presents
    }
    for mois, moyenne in moyenne_par_mois.items():
        print(f"   {mois} : {moyenne:.4f}")

    return variations


# =====================================================================
# A.2 — ENUMERATE, ZIP, SORTED
# =====================================================================

def partie_a2(dates, taux, variations):
    """enumerate, zip et sorted(..., key=...) (avant / après).

    Paramètres :
        dates (list de date)       : les dates.
        taux (list de float)       : les taux.
        variations (list de float) : les variations jour à jour en %.
    """
    titre("A.2 — ENUMERATE, ZIP, SORTED")

    # --- enumerate : indice + valeur ---
    print("1) enumerate : parcourir avec l'indice ET la valeur")
    print("   AVANT : for i in range(len(taux)): ... taux[i]")
    print("   APRÈS : for i, t in enumerate(taux, start=1): ...")
    for i, t in enumerate(taux[:3], start=1):
        print(f"   Jour n°{i} : {t}")

    # --- zip : associer deux listes élément par élément ---
    print("\n2) zip : associer les dates et les taux")

    # AVANT : on passe par les indices
    couples_avant = []
    for i in range(len(dates)):
        couples_avant.append((dates[i], taux[i]))

    # APRÈS : zip associe directement les deux listes
    couples = list(zip(dates, taux))

    for d, t in couples[:3]:
        print(f"   {d} → {t}")
    verifier("couples (date, taux)", couples_avant, couples)

    # zip permet aussi de « défaire » une liste de couples
    dates_2, taux_2 = zip(*couples)
    print(f"   zip(*couples) refait les deux listes : {list(taux_2) == taux}")

    # --- sorted avec key : trier selon un critère ---
    print("\n3) sorted(..., key=...) : trier selon un critère")

    les_5_plus_hauts = sorted(couples, key=lambda couple: couple[1], reverse=True)[:5]
    print("   Les 5 taux les plus hauts (tri sur le taux, décroissant) :")
    for rang, (d, t) in enumerate(les_5_plus_hauts, start=1):
        print(f"     {rang}. {d} : {t}")

    jours_variation = list(zip(dates[1:], variations))
    plus_fortes = sorted(jours_variation, key=lambda dv: abs(dv[1]), reverse=True)[:3]
    print("   Les 3 plus fortes variations (tri sur la valeur absolue) :")
    for d, v in plus_fortes:
        print(f"     {d} : {v:+.3f} %")

    # min / max acceptent aussi key=
    date_min, taux_min = min(couples, key=lambda couple: couple[1])
    date_max, taux_max = max(couples, key=lambda couple: couple[1])
    print(f"\n   min(..., key=...) : {taux_min} le {date_min}")
    print(f"   max(..., key=...) : {taux_max} le {date_max}")
    print("   👉 Remplace toute la fonction trouver_min_max de la séance 2 !")


# =====================================================================
# A.3 — F-STRINGS, LAMBDA, MAP / FILTER
# =====================================================================

def partie_a3(dates, taux):
    """f-strings, fonctions lambda, map et filter.

    Paramètres :
        dates (list de date)  : les dates.
        taux (list de float)  : les taux.
    """
    titre("A.3 — F-STRINGS, LAMBDA, MAP / FILTER")

    # --- f-strings : formater des nombres et des dates ---
    print("1) f-strings : formater des nombres")
    t = taux[0]
    moyenne = sum(taux) / len(taux)
    variation = (taux[-1] / taux[0] - 1) * 100
    print(f"   AVANT : 'Taux : ' + str(t) + ' ' + DEVISE  →  {'Taux : ' + str(t) + ' ' + DEVISE}")
    print(f"   APRÈS : f'Taux : {{t}} {{DEVISE}}'            →  Taux : {t} {DEVISE}")
    print(f"   {{moyenne:.2f}}    deux décimales      → {moyenne:.2f}")
    print(f"   {{moyenne:.4f}}    quatre décimales    → {moyenne:.4f}")
    print(f"   {{variation:+.2f}} avec le signe       → {variation:+.2f} %")
    print(f"   {{0.0136:.1%}}     en pourcentage      → {0.0136:.1%}")
    print(f"   {{1234567.8:,.2f}} séparateur milliers → {1234567.8:,.2f}")
    print(f"   {{t:>10.4f}}       aligné à droite     → [{t:>10.4f}]")

    print("\n2) f-strings : formater des dates")
    d = dates[1]
    print(f"   {{d}}                → {d}")
    print(f"   {{d:%d/%m/%Y}}       → {d:%d/%m/%Y}")
    print(f"   {{d:%A %d %B %Y}}    → {d:%A %d %B %Y}   (noms en anglais par défaut)")
    print(f"   {{d.year}}-T{{(d.month - 1) // 3 + 1}}    → {d.year}-T{(d.month - 1) // 3 + 1}  (trimestre)")

    # --- lambda : une petite fonction anonyme, en une ligne ---
    print("\n3) lambda : petite fonction anonyme")

    def en_pourcentage_def(x):
        return (x - 1) * 100

    en_pourcentage = lambda x: (x - 1) * 100   # même chose, en une ligne
    print(f"   def en_pourcentage(x): return (x - 1) * 100  → {en_pourcentage_def(1.17):.2f}")
    print(f"   lambda x: (x - 1) * 100                      → {en_pourcentage(1.17):.2f}")

    # --- map : appliquer une fonction à chaque élément ---
    print("\n4) map : appliquer une fonction à chaque élément")
    arrondis_avant = []
    for x in taux:
        arrondis_avant.append(round(x, 2))
    arrondis = list(map(lambda x: round(x, 2), taux))
    print(f"   list(map(lambda x: round(x, 2), taux))[:5] → {arrondis[:5]}")
    verifier("map", arrondis_avant, arrondis)
    inverses = list(map(lambda x: 1 / x, taux))
    print(f"   Taux inverses (1 {DEVISE} en EUR)[:3]        → {[f'{x:.4f}' for x in inverses[:3]]}")

    # --- filter : garder les éléments qui vérifient une condition ---
    print("\n5) filter : garder les éléments qui vérifient une condition")
    seuil = round(moyenne, 2)
    au_dessus_avant = []
    for x in taux:
        if x > seuil:
            au_dessus_avant.append(x)
    au_dessus = list(filter(lambda x: x > seuil, taux))
    print(f"   list(filter(lambda x: x > {seuil}, taux)) → {len(au_dessus)} taux au-dessus")
    verifier("filter", au_dessus_avant, au_dessus)

    # --- map/filter ou compréhension ? ---
    print("\n6) map / filter ou compréhension ?")
    print(f"   [round(x, 2) for x in taux]   == map  → {[round(x, 2) for x in taux] == arrondis}")
    print(f"   [x for x in taux if x > {seuil}] == filter → "
          f"{[x for x in taux if x > seuil] == au_dessus}")
    print("   👉 En Python, la compréhension est souvent préférée : plus lisible, sans lambda.")


# =====================================================================
# PROGRAMME PRINCIPAL
# =====================================================================

def main():
    """Charge les taux puis lance les parties A.1, A.2 et A.3."""
    chemin_csv = trouver_csv(EMPLACEMENTS_POSSIBLES)
    if chemin_csv is None:
        print("❌ Fichier CSV introuvable. Emplacements essayés :")
        print("\n".join(f"   - {chemin}" for chemin in EMPLACEMENTS_POSSIBLES))
        return

    couples = lire_csv(chemin_csv)
    dates, taux = [d for d, _ in couples], [t for _, t in couples]
    print(f"Fichier chargé : {chemin_csv.name} ({len(couples)} jours, "
          f"du {dates[0]:%d/%m/%Y} au {dates[-1]:%d/%m/%Y})")

    variations = partie_a1(dates, taux)
    partie_a2(dates, taux, variations)
    partie_a3(dates, taux)


if __name__ == "__main__":
    main()
