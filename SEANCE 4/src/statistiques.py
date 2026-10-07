# -*- coding: utf-8 -*-
"""
src/statistiques.py
Module de statistiques des séries de taux (objets SerieTaux).

    resumer(serie)            -> dictionnaire des indicateurs d'une série
    afficher_resume(series)   -> tableau comparatif dans le terminal
    exporter_resume(series, chemin) -> le même tableau en CSV
"""

import csv
import statistics


def resumer(serie):
    """Calcule les indicateurs principaux d'une série.

    Paramètre :
        serie (SerieTaux) : la série à résumer.
    Renvoie :
        dict : devise, nombre de jours, période, moyenne, min, max,
               variation sur la période et volatilité (écart-type des
               variations quotidiennes, en %).
    """
    date_min, taux_min = serie.minimum()
    date_max, taux_max = serie.maximum()
    return {
        "devise": serie.devise,
        "jours": len(serie),
        "debut": serie.dates[0],
        "fin": serie.dates[-1],
        "moyenne": serie.moyenne(),
        "min": taux_min,
        "date_min": date_min,
        "max": taux_max,
        "date_max": date_max,
        "variation_%": serie.variation(),
        "volatilite_%": statistics.stdev(serie.variations_quotidiennes()),
    }


def afficher_resume(series):
    """Affiche un tableau comparatif des séries dans le terminal.

    Paramètre :
        series (list de SerieTaux) : les séries à comparer.
    """
    resumes = [resumer(serie) for serie in series]
    print(f"\n{'Devise':<7}| {'Jours':>5} | {'Période':^25} | {'Moyenne':>8} | "
          f"{'Minimum':^20} | {'Maximum':^20} | {'Variation':>9} | {'Volatilité':>10}")
    print("-" * 125)
    for r in resumes:
        print(f"{r['devise']:<7}| {r['jours']:>5} | "
              f"{r['debut']:%d/%m/%Y} → {r['fin']:%d/%m/%Y}  | {r['moyenne']:>8.4f} | "
              f"{r['min']:.4f} le {r['date_min']:%d/%m/%Y} | "
              f"{r['max']:.4f} le {r['date_max']:%d/%m/%Y} | "
              f"{r['variation_%']:>+8.2f} % | {r['volatilite_%']:>8.3f} %")


def exporter_resume(series, chemin):
    """Enregistre le tableau comparatif dans un fichier CSV.

    Paramètres :
        series (list de SerieTaux) : les séries à comparer.
        chemin (Path)              : le fichier CSV à écrire.
    """
    resumes = [resumer(serie) for serie in series]
    chemin.parent.mkdir(exist_ok=True)
    with open(chemin, "w", newline="", encoding="utf-8") as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=list(resumes[0]))
        ecrivain.writeheader()
        ecrivain.writerows(resumes)
