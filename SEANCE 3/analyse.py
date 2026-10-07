# -*- coding: utf-8 -*-
"""
analyse.py
Séance 3 — Parties A et B : découvrir pandas, nettoyer et analyser les taux.

A.1 — Charger le CSV des taux (séance 1) dans un DataFrame avec read_csv,
      puis l'inspecter : head(), describe(), dtypes.
A.2 — Sélectionner une colonne (Series), filtrer des lignes, recalculer
      moyenne / minimum / maximum avec pandas et comparer avec les
      fonctions de la séance 2.
B.1 — Combler les trous : réindexer sur un calendrier de jours ouvrés
      continu et propager la dernière valeur connue (forward-fill).
B.2 — Analyser : variation en % sur la période, moyenne mobile,
      rééchantillonnage en données mensuelles (resample).

Installation préalable (une seule fois, dans le terminal) :
    pip install pandas
"""

import sys
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------
# Paramètres
# ---------------------------------------------------------------------
DEVISE = "USD"
NOM_CSV = f"EUR_{DEVISE}_2026-01-01_2026-09-01.csv"
SEUIL_FILTRE = 1.17          # A.2 : on filtre les jours où le taux dépasse ce seuil
FENETRE_MOBILE = 20          # B.2 : 20 jours ouvrés ≈ 1 mois

DOSSIER_SCRIPT = Path(__file__).resolve().parent
DOSSIER_PROJET = DOSSIER_SCRIPT.parent

# On cherche le CSV dans donnees/ à côté du script, puis dans les séances précédentes
EMPLACEMENTS_POSSIBLES = [
    DOSSIER_SCRIPT / "donnees" / NOM_CSV,
    DOSSIER_PROJET / "SEANCE 2" / "donnees" / NOM_CSV,
    DOSSIER_PROJET / "SEANCE 1" / "donnees" / NOM_CSV,
]

# Les résultats nettoyés sont enregistrés dans donnees/ à côté de ce script
DOSSIER_SORTIE = DOSSIER_SCRIPT / "donnees"

# Affichage plus lisible des tableaux dans le terminal
pd.set_option("display.width", 120)
pd.set_option("display.precision", 4)


def titre(texte):
    """Affiche un titre de partie encadré.

    Paramètre :
        texte (str) : le titre à afficher.
    """
    print()
    print("=" * 70)
    print(texte)
    print("=" * 70)


def trouver_csv(emplacements):
    """Renvoie le premier chemin de la liste qui existe, ou None.

    Paramètre :
        emplacements (list de Path) : chemins possibles du fichier CSV.
    Renvoie :
        Path ou None.
    """
    for chemin in emplacements:
        if chemin.exists():
            return chemin
    return None


# =====================================================================
# A.1 — INSTALLER ET CHARGER
# =====================================================================

def charger(chemin):
    """Charge le CSV des taux dans un DataFrame indexé par date.

    Paramètre :
        chemin (Path) : le fichier CSV (colonnes « date » et « taux »).
    Renvoie :
        DataFrame : une colonne « taux », index de type date (DatetimeIndex).
    """
    df = pd.read_csv(chemin, parse_dates=["date"])   # « date » lue comme une vraie date
    df = df.set_index("date").sort_index()
    return df


def inspecter(df):
    """Affiche les premières lignes, les statistiques et le type des colonnes.

    Paramètre :
        df (DataFrame) : le tableau à inspecter.
    """
    titre("A.1 — INSPECTION DU DATAFRAME")
    print("Les 5 premières lignes — head() :")
    print(df.head())
    print("\nStatistiques descriptives — describe() :")
    print(df.describe())
    print("\nType de chaque colonne — dtypes :")
    print(df.dtypes)
    print(f"\nType de l'index : {df.index.dtype}")
    print(f"Nombre de lignes : {len(df)}")
    print(f"Valeurs manquantes (NaN) : {df['taux'].isna().sum()}")


# =====================================================================
# A.2 — SÉLECTIONNER ET FILTRER
# =====================================================================

def selectionner_et_filtrer(df, seuil):
    """Sélectionne la colonne des taux et filtre les jours au-dessus d'un seuil.

    Paramètres :
        df (DataFrame) : le tableau des taux.
        seuil (float)  : la valeur à dépasser.
    Renvoie :
        DataFrame : uniquement les lignes où le taux est strictement supérieur au seuil.
    """
    titre("A.2 — SÉLECTIONNER ET FILTRER")

    serie = df["taux"]          # une colonne = une Series
    print(f"df['taux'] est de type : {type(serie).__name__}")
    print(f"df est de type        : {type(df).__name__}")

    filtre = df[df["taux"] > seuil]   # masque booléen, sans boucle
    print(f"\nJours où le taux dépasse {seuil} : {len(filtre)} sur {len(df)}")
    print(filtre.head())
    return filtre


def statistiques_pandas(df):
    """Calcule moyenne, minimum et maximum avec pandas.

    Paramètre :
        df (DataFrame) : le tableau des taux.
    Renvoie :
        dict : {"moyenne", "min", "date_min", "max", "date_max"}.
    """
    serie = df["taux"]
    return {
        "moyenne": serie.mean(),
        "min": serie.min(),
        "date_min": serie.idxmin().date(),   # date du minimum
        "max": serie.max(),
        "date_max": serie.idxmax().date(),   # date du maximum
    }


def comparer_avec_seance2(chemin_csv, stats):
    """Compare les statistiques pandas avec les fonctions de la séance 2.

    On importe fonctions.py depuis le dossier SEANCE 2, s'il est trouvé.

    Paramètres :
        chemin_csv (Path) : le CSV des taux.
        stats (dict)      : les statistiques calculées avec pandas.
    """
    print("\nStatistiques avec pandas :")
    print(f"  Moyenne : {stats['moyenne']:.6f}")
    print(f"  Minimum : {stats['min']} (le {stats['date_min']})")
    print(f"  Maximum : {stats['max']} (le {stats['date_max']})")

    dossier_seance2 = DOSSIER_PROJET / "SEANCE 2"
    sys.path.insert(0, str(dossier_seance2))
    try:
        import fonctions   # le fichier fonctions.py de la séance 2
    except ImportError:
        print(f"\n(fonctions.py de la séance 2 introuvable dans {dossier_seance2} : "
              "comparaison ignorée.)")
        return

    couples = fonctions.lire_csv(chemin_csv)
    moyenne_s2 = fonctions.calculer_moyenne(fonctions.extraire_taux(couples))
    (date_min, taux_min), (date_max, taux_max) = fonctions.trouver_min_max(couples)

    print("\nStatistiques avec les fonctions de la séance 2 :")
    print(f"  Moyenne : {moyenne_s2:.6f}")
    print(f"  Minimum : {taux_min} (le {date_min})")
    print(f"  Maximum : {taux_max} (le {date_max})")

    identiques = (abs(moyenne_s2 - stats["moyenne"]) < 1e-9
                  and taux_min == stats["min"] and taux_max == stats["max"])
    if identiques:
        print("\n✅ Mêmes résultats : pandas fait en une ligne ce qui prenait une fonction entière.")
    else:
        print("\n⚠️ Résultats différents : à vérifier.")


# =====================================================================
# B.1 — COMBLER LES TROUS (FORWARD-FILL)
# =====================================================================

def combler_les_trous(df):
    """Réindexe sur un calendrier de jours ouvrés continu et applique un forward-fill.

    La BCE ne publie pas de taux les jours fériés (1er janvier, Vendredi saint,
    lundi de Pâques, 1er mai, 25-26 décembre). On crée tous les jours ouvrés
    (lundi au vendredi) entre la première et la dernière date, puis on remplit
    chaque trou avec la dernière valeur connue.

    Paramètre :
        df (DataFrame) : les taux bruts, indexés par date.
    Renvoie :
        DataFrame : colonnes « taux » (complétée) et « rempli » (True si la
                    valeur a été recopiée par forward-fill).
    """
    titre("B.1 — COMBLER LES TROUS (FORWARD-FILL)")

    calendrier = pd.bdate_range(df.index.min(), df.index.max(), name="date")
    df_complet = df.reindex(calendrier)   # les jours sans taux deviennent NaN

    trous = df_complet["taux"].isna()
    print(f"Jours ouvrés dans le calendrier : {len(calendrier)}")
    print(f"Jours avec un taux publié       : {len(df)}")
    print(f"Jours manquants (NaN) à combler : {trous.sum()}")
    if trous.sum() > 0:
        print("Dates manquantes :", ", ".join(str(d.date()) for d in df_complet.index[trous]))

    df_complet["rempli"] = trous
    df_complet["taux"] = df_complet["taux"].ffill()   # forward-fill
    print(f"Valeurs manquantes après ffill() : {df_complet['taux'].isna().sum()}")
    return df_complet


# =====================================================================
# B.2 — ANALYSER : VARIATION, MOYENNE MOBILE, RESAMPLE
# =====================================================================

def analyser(df, fenetre):
    """Calcule la variation sur la période, la variation quotidienne et la moyenne mobile.

    Paramètres :
        df (DataFrame) : les taux complétés (après forward-fill).
        fenetre (int)  : le nombre de jours de la moyenne mobile.
    Renvoie :
        DataFrame : df avec deux colonnes en plus, « variation_jour_% »
                    et « moyenne_mobile ».
    """
    titre("B.2 — ANALYSER")

    # Variation en % sur toute la période
    premier = df["taux"].iloc[0]
    dernier = df["taux"].iloc[-1]
    variation = (dernier / premier - 1) * 100
    print(f"Variation sur la période : {premier} ({df.index[0].date()}) → "
          f"{dernier} ({df.index[-1].date()}) = {variation:+.2f} %")

    # Variation jour à jour, en %
    df["variation_jour_%"] = df["taux"].pct_change() * 100
    jour_max = df["variation_jour_%"].abs().idxmax()
    print(f"Plus forte variation sur un jour : "
          f"{df.loc[jour_max, 'variation_jour_%']:+.2f} % le {jour_max.date()}")

    # Moyenne mobile : moyenne des « fenetre » derniers jours, recalculée chaque jour
    df["moyenne_mobile"] = df["taux"].rolling(window=fenetre).mean()
    print(f"\nMoyenne mobile sur {fenetre} jours ouvrés (dernières lignes) :")
    print(df[["taux", "moyenne_mobile"]].tail())
    return df


def reechantillonner(df):
    """Passe des données quotidiennes à des données mensuelles avec resample.

    Paramètre :
        df (DataFrame) : les taux quotidiens complétés.
    Renvoie :
        DataFrame : une ligne par mois (moyenne, min, max, dernier taux du mois).
    """
    print("\nRééchantillonnage mensuel — resample('ME') :")
    mensuel = df["taux"].resample("ME").agg(["mean", "min", "max", "last"])
    mensuel.columns = ["moyenne", "min", "max", "fin_de_mois"]
    mensuel.index = mensuel.index.strftime("%Y-%m")
    mensuel.index.name = "mois"
    print(mensuel)
    return mensuel


# =====================================================================
# PROGRAMME PRINCIPAL
# =====================================================================

def main():
    """Enchaîne chargement, inspection, filtrage, nettoyage et analyse."""
    chemin_csv = trouver_csv(EMPLACEMENTS_POSSIBLES)
    if chemin_csv is None:
        print("❌ Fichier CSV introuvable. Emplacements essayés :")
        for chemin in EMPLACEMENTS_POSSIBLES:
            print("   -", chemin)
        return
    print("Fichier chargé :", chemin_csv)

    # Partie A
    df = charger(chemin_csv)
    inspecter(df)
    selectionner_et_filtrer(df, SEUIL_FILTRE)
    comparer_avec_seance2(chemin_csv, statistiques_pandas(df))

    # Partie B
    df_complet = combler_les_trous(df)
    df_complet = analyser(df_complet, FENETRE_MOBILE)
    mensuel = reechantillonner(df_complet)

    # Enregistrement des résultats
    DOSSIER_SORTIE.mkdir(exist_ok=True)
    fichier_quotidien = DOSSIER_SORTIE / f"EUR_{DEVISE}_quotidien_nettoye.csv"
    fichier_mensuel = DOSSIER_SORTIE / f"EUR_{DEVISE}_mensuel.csv"
    df_complet.to_csv(fichier_quotidien)
    mensuel.to_csv(fichier_mensuel)
    titre("RÉSULTATS ENREGISTRÉS")
    print("Données quotidiennes nettoyées :", fichier_quotidien)
    print("Données mensuelles             :", fichier_mensuel)


if __name__ == "__main__":
    main()
