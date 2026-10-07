# -*- coding: utf-8 -*-
"""
graphiques.py
Séance 4 — Partie C : visualiser avec matplotlib.

C.1 — Une première courbe : l'évolution d'une devise sur la période
      (date -> taux), avec un titre, des axes légendés, sauvegardée en PNG.
C.2 — Plusieurs graphiques :
        - les deux devises du groupe comparées sur un même graphique ;
        - un histogramme des variations quotidiennes ;
        - plusieurs graphiques côte à côte (subplots).

Toutes les figures sont créées avec  fig, ax = plt.subplots()  et
enregistrées dans le dossier graphiques/ à côté de ce script.

Les données sont chargées avec la classe SerieTaux (serie_taux.py).

Installation préalable (une seule fois) : pip install matplotlib
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")      # on enregistre les images sans ouvrir de fenêtre
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from serie_taux import DEVISES, charger_serie

DOSSIER_SCRIPT = Path(__file__).resolve().parent
DOSSIER_GRAPHIQUES = DOSSIER_SCRIPT / "graphiques"

COULEURS = {0: "#1f6fb4", 1: "#d9822b"}      # une couleur fixe par devise
MOIS_FR = ["janv.", "févr.", "mars", "avr.", "mai", "juin",
           "juil.", "août", "sept.", "oct.", "nov.", "déc."]


# =====================================================================
# OUTILS
# =====================================================================

def mettre_en_forme_axe_dates(ax):
    """Affiche un repère par mois sur l'axe des dates, avec les mois en français.

    Paramètre :
        ax (Axes) : le graphique à mettre en forme.
    """
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: MOIS_FR[mdates.num2date(x).month - 1]))
    ax.grid(True, alpha=0.3)


def enregistrer(fig, nom_fichier):
    """Enregistre une figure en PNG dans graphiques/ puis la ferme.

    Paramètres :
        fig (Figure)      : la figure à enregistrer.
        nom_fichier (str) : le nom du fichier, par exemple "courbe_USD.png".
    Renvoie :
        Path : le chemin du fichier créé.
    """
    DOSSIER_GRAPHIQUES.mkdir(exist_ok=True)
    chemin = DOSSIER_GRAPHIQUES / nom_fichier
    fig.savefig(chemin, dpi=150, bbox_inches="tight")   # dpi = résolution
    plt.close(fig)                                     # libère la mémoire
    print(f"   ✅ {chemin.name}")
    return chemin


# =====================================================================
# C.1 — UNE PREMIÈRE COURBE
# =====================================================================

def courbe_une_devise(serie, couleur):
    """Trace l'évolution d'une devise sur la période (courbe date -> taux).

    Paramètres :
        serie (SerieTaux) : la série à tracer.
        couleur (str)     : la couleur de la courbe.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(serie.dates, serie.taux, color=couleur, linewidth=1.8,
            label=f"1 {serie.base} en {serie.devise}")
    ax.axhline(serie.moyenne(), color="grey", linestyle="--", linewidth=1,
               label=f"Moyenne : {serie.moyenne():.4f}")

    # Repérer le minimum et le maximum
    for (jour, taux), texte in [(serie.minimum(), "min"), (serie.maximum(), "max")]:
        ax.scatter([jour], [taux], color=couleur, zorder=3)
        ax.annotate(f"{texte} {taux:.4f}\n{jour:%d/%m}", (jour, taux),
                    textcoords="offset points", xytext=(0, 10 if texte == "max" else -28),
                    ha="center", fontsize=9)

    ax.margins(y=0.15)      # de la place en haut et en bas pour les annotations
    ax.set_title(f"Évolution du taux {serie.base}/{serie.devise} "
                 f"du {serie.dates[0]:%d/%m/%Y} au {serie.dates[-1]:%d/%m/%Y} "
                 f"({serie.variation():+.2f} %)")
    ax.set_xlabel("Date")
    ax.set_ylabel(f"Taux ({serie.devise} pour 1 {serie.base})")
    ax.legend()
    mettre_en_forme_axe_dates(ax)
    enregistrer(fig, f"1_courbe_{serie.devise}.png")


# =====================================================================
# C.2 — PLUSIEURS GRAPHIQUES
# =====================================================================

def comparer_deux_devises(series):
    """Compare les deux devises sur un même graphique, en base 100.

    Les deux taux n'ont pas le même niveau (environ 1,17 pour l'USD, 0,86 pour
    le GBP) : on les ramène tous les deux à 100 au premier jour pour comparer
    leurs évolutions en %.

    Paramètre :
        series (list de SerieTaux) : les séries à comparer.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, serie in enumerate(series):
        base_100 = [t / serie.taux[0] * 100 for t in serie.taux]
        ax.plot(serie.dates, base_100, color=COULEURS[i], linewidth=1.8,
                label=f"{serie.base}/{serie.devise} ({serie.variation():+.2f} %)")
    ax.axhline(100, color="grey", linewidth=1)

    ax.set_title("Comparaison des devises du groupe (base 100 au premier jour)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Indice (100 = premier jour)")
    ax.legend()
    mettre_en_forme_axe_dates(ax)
    enregistrer(fig, "2_comparaison_devises.png")


def histogramme_variations(serie, couleur):
    """Trace l'histogramme des variations quotidiennes d'une devise.

    Paramètres :
        serie (SerieTaux) : la série à analyser.
        couleur (str)     : la couleur des barres.
    """
    variations = serie.variations_quotidiennes()
    moyenne = sum(variations) / len(variations)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(variations, bins=25, color=couleur, edgecolor="white")
    ax.axvline(0, color="black", linewidth=1)
    ax.axvline(moyenne, color="grey", linestyle="--", linewidth=1,
               label=f"Moyenne : {moyenne:+.3f} %")

    ax.set_title(f"Répartition des variations quotidiennes {serie.base}/{serie.devise} "
                 f"({len(variations)} jours)")
    ax.set_xlabel("Variation d'un jour à l'autre (%)")
    ax.set_ylabel("Nombre de jours")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    enregistrer(fig, f"3_histogramme_{serie.devise}.png")


def tableau_de_bord(series):
    """Plusieurs graphiques côte à côte (subplots) : courbes en haut, histogrammes en bas.

    Paramètre :
        series (list de SerieTaux) : les séries à afficher.
    """
    n = len(series)
    fig, axes = plt.subplots(2, n, figsize=(6 * n, 8), squeeze=False)

    for i, serie in enumerate(series):
        # Ligne du haut : courbe date -> taux
        ax_haut = axes[0][i]
        ax_haut.plot(serie.dates, serie.taux, color=COULEURS[i], linewidth=1.5)
        ax_haut.set_title(f"{serie.base}/{serie.devise} : évolution")
        ax_haut.set_xlabel("Date")
        ax_haut.set_ylabel(f"Taux ({serie.devise})")
        mettre_en_forme_axe_dates(ax_haut)

        # Ligne du bas : histogramme des variations
        ax_bas = axes[1][i]
        ax_bas.hist(serie.variations_quotidiennes(), bins=25, color=COULEURS[i],
                    edgecolor="white")
        ax_bas.axvline(0, color="black", linewidth=1)
        ax_bas.set_title(f"{serie.base}/{serie.devise} : variations quotidiennes")
        ax_bas.set_xlabel("Variation (%)")
        ax_bas.set_ylabel("Nombre de jours")
        ax_bas.grid(True, axis="y", alpha=0.3)

    fig.suptitle("Tableau de bord des taux de change (2026)", fontsize=14)
    fig.tight_layout()
    enregistrer(fig, "4_tableau_de_bord.png")


# =====================================================================
# PROGRAMME PRINCIPAL
# =====================================================================

def main():
    """Charge les séries et produit tous les graphiques PNG."""
    print("Chargement des séries :")
    series = [serie for serie in map(charger_serie, DEVISES) if serie is not None]
    if not series:
        print("❌ Aucune série chargée : impossible de tracer les graphiques.")
        return

    print(f"\nCréation des graphiques dans {DOSSIER_GRAPHIQUES} :")
    courbe_une_devise(series[0], COULEURS[0])                   # C.1
    if len(series) >= 2:
        comparer_deux_devises(series)                           # C.2
    for i, serie in enumerate(series):
        histogramme_variations(serie, COULEURS[i])              # C.2
    tableau_de_bord(series)                                     # C.2 (subplots)


if __name__ == "__main__":
    main()
