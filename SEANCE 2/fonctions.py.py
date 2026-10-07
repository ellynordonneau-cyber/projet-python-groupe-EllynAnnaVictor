# -*- coding: utf-8 -*-
"""
fonctions.py
Séance 2 — Partie A : les fonctions.

A.1 — On reprend le CSV des taux de la séance 1 et on découpe le traitement
      en fonctions :
        - lire_csv       : lit le CSV et renvoie une liste de couples (date, taux)
        - calculer_moyenne : calcule la moyenne d'une liste de taux
        - trouver_min_max  : renvoie le taux minimum et le taux maximum
A.2 — On recalcule la moyenne avec statistics.mean et on compare.

Uniquement la bibliothèque standard : csv, statistics, pathlib.
"""

import csv
import statistics
from pathlib import Path

# ---------------------------------------------------------------------
# Emplacement du CSV produit en séance 1
# ---------------------------------------------------------------------
NOM_CSV = "EUR_USD_2026-01-01_2026-09-01.csv"
DOSSIER_SCRIPT = Path(__file__).resolve().parent

# On cherche le CSV à deux endroits :
#   1. dans le dossier donnees/ à côté de ce script ;
#   2. dans le dossier donnees/ de la séance 1.
EMPLACEMENTS_POSSIBLES = [
    DOSSIER_SCRIPT / "donnees" / NOM_CSV,
    DOSSIER_SCRIPT.parent / "SEANCE 1" / "donnees" / NOM_CSV,
]


# =====================================================================
# A.1 — LES FONCTIONS
# =====================================================================

def lire_csv(chemin):
    """Lit le fichier CSV des taux et renvoie une liste de couples (date, taux).

    Paramètre :
        chemin (Path ou str) : chemin du fichier CSV, avec les colonnes
                               « date » et « taux ».
    Renvoie :
        list de tuples (str, float) : par exemple [("2026-01-02", 1.1721), ...]
    """
    couples = []
    with open(chemin, newline="", encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)
        for ligne in lecteur:
            date = ligne["date"]
            taux = float(ligne["taux"])   # le CSV contient du texte : on convertit
            couples.append((date, taux))
    return couples


def extraire_taux(couples):
    """Renvoie uniquement les taux d'une liste de couples (date, taux).

    Paramètre :
        couples (list de tuples) : liste de couples (date, taux).
    Renvoie :
        list de float : la liste des taux, dans le même ordre.
    """
    liste_taux = []
    for date, taux in couples:
        liste_taux.append(taux)
    return liste_taux


def calculer_moyenne(liste_taux):
    """Calcule la moyenne d'une liste de taux.

    Paramètre :
        liste_taux (list de float) : les taux à moyenner (liste non vide).
    Renvoie :
        float : la moyenne des taux.
    """
    if len(liste_taux) == 0:
        raise ValueError("Impossible de calculer la moyenne d'une liste vide.")

    somme = 0
    for taux in liste_taux:
        somme += taux
    return somme / len(liste_taux)


def trouver_min_max(couples):
    """Renvoie le taux minimum et le taux maximum, avec leur date.

    Paramètre :
        couples (list de tuples) : liste de couples (date, taux), non vide.
    Renvoie :
        tuple : (couple_minimum, couple_maximum),
                par exemple (("2026-03-10", 1.08), ("2026-07-01", 1.19)).
    """
    if len(couples) == 0:
        raise ValueError("Impossible de chercher le min et le max d'une liste vide.")

    couple_min = couples[0]
    couple_max = couples[0]
    for couple in couples:
        taux = couple[1]
        if taux < couple_min[1]:
            couple_min = couple
        if taux > couple_max[1]:
            couple_max = couple
    return couple_min, couple_max


def trouver_csv(emplacements):
    """Renvoie le premier chemin de la liste qui existe vraiment.

    Paramètre :
        emplacements (list de Path) : chemins possibles du fichier CSV.
    Renvoie :
        Path : le premier chemin existant, ou None si aucun n'existe.
    """
    for chemin in emplacements:
        if chemin.exists():
            return chemin
    return None


# =====================================================================
# PROGRAMME PRINCIPAL
# =====================================================================

def main():
    """Enchaîne les fonctions : lecture, moyenne, min/max, comparaison."""
    chemin_csv = trouver_csv(EMPLACEMENTS_POSSIBLES)
    if chemin_csv is None:
        print("❌ Fichier CSV introuvable. Emplacements essayés :")
        for chemin in EMPLACEMENTS_POSSIBLES:
            print("   -", chemin)
        print("Copiez le dossier donnees/ de la séance 1 à côté de ce script.")
        return

    # --- Lecture du CSV ---
    print("=" * 60)
    print("A.1 — LECTURE DU CSV")
    print("=" * 60)
    couples = lire_csv(chemin_csv)
    print("Fichier lu :", chemin_csv.name)
    print("Nombre de jours ouvrés :", len(couples))
    print("Trois premiers couples :", couples[:3])

    # --- Moyenne ---
    liste_taux = extraire_taux(couples)
    moyenne = calculer_moyenne(liste_taux)
    print(f"\nMoyenne (notre fonction) : {moyenne:.6f}")

    # --- Minimum et maximum ---
    (date_min, taux_min), (date_max, taux_max) = trouver_min_max(couples)
    print(f"Taux minimum : {taux_min} (le {date_min})")
    print(f"Taux maximum : {taux_max} (le {date_max})")

    # --- A.2 : comparaison avec statistics.mean ---
    print()
    print("=" * 60)
    print("A.2 — COMPARAISON AVEC statistics.mean")
    print("=" * 60)
    moyenne_statistics = statistics.mean(liste_taux)
    print(f"Moyenne (notre fonction)    : {moyenne:.10f}")
    print(f"Moyenne (statistics.mean)   : {moyenne_statistics:.10f}")
    ecart = abs(moyenne - moyenne_statistics)
    print(f"Écart entre les deux        : {ecart:.2e}")

    if ecart < 1e-9:
        print("✅ Les deux moyennes sont identiques (aux arrondis près).")
    else:
        print("⚠️ Les deux moyennes sont différentes : vérifier calculer_moyenne.")


# Ce bloc ne s'exécute que si on lance ce fichier directement
# (et pas si on l'importe depuis un autre fichier avec « import fonctions »).
if __name__ == "__main__":
    main()
