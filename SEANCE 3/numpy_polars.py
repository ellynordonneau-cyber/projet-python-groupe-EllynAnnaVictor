# -*- coding: utf-8 -*-
"""
numpy_polars.py
Séance 3 — Partie D : un peu de numpy (et aperçu de polars).

D.1 — Du DataFrame au tableau numpy : convertir la colonne des taux avec
      to_numpy(), puis calculer SANS BOUCLE (vectorisé) la moyenne,
      l'écart-type et les variations jour à jour.
D.2 — Comprendre numpy : la notion de dtype (type des éléments du tableau)
      et le broadcasting (opération entre un tableau et un nombre, ex. taux * 100).
D.3 — Aperçu de polars : refaire trois calculs (moyenne, variation,
      regroupement par mois) en polars et comparer syntaxe et temps avec pandas.

Installation préalable (une seule fois, dans le terminal) :
    pip install pandas polars
(numpy est installé automatiquement avec pandas.)
"""

import time
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# Paramètres
# ---------------------------------------------------------------------
DEVISE = "USD"
NOM_CSV = f"EUR_{DEVISE}_2026-01-01_2026-09-01.csv"
TAILLE_GRANDE = 2_000_000    # nombre de lignes du jeu de test pour les chronos

DOSSIER_SCRIPT = Path(__file__).resolve().parent
DOSSIER_PROJET = DOSSIER_SCRIPT.parent
EMPLACEMENTS_POSSIBLES = [
    DOSSIER_SCRIPT / "donnees" / NOM_CSV,
    DOSSIER_PROJET / "SEANCE 2" / "donnees" / NOM_CSV,
    DOSSIER_PROJET / "SEANCE 1" / "donnees" / NOM_CSV,
]


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


def chronometrer(fonction, repetitions=5):
    """Mesure le meilleur temps d'exécution de fonction() sur plusieurs essais.

    Paramètres :
        fonction (function) : une fonction sans argument à chronométrer.
        repetitions (int)   : nombre d'essais (on garde le plus rapide).
    Renvoie :
        float : le meilleur temps, en secondes.
    """
    meilleur = float("inf")
    for _ in range(repetitions):
        debut = time.perf_counter()
        fonction()
        meilleur = min(meilleur, time.perf_counter() - debut)
    return meilleur


def formater_duree(secondes):
    """Affiche une durée de façon lisible (µs, ms ou s).

    Paramètre :
        secondes (float) : la durée en secondes.
    Renvoie :
        str : la durée formatée.
    """
    if secondes < 1e-3:
        return f"{secondes * 1e6:.1f} µs"
    if secondes < 1:
        return f"{secondes * 1e3:.1f} ms"
    return f"{secondes:.2f} s"


# =====================================================================
# D.1 — DU DATAFRAME AU TABLEAU NUMPY
# =====================================================================

def calculs_numpy(df):
    """Convertit la colonne des taux en tableau numpy et fait des calculs vectorisés.

    Paramètre :
        df (DataFrame) : colonnes « date » et « taux ».
    Renvoie :
        ndarray : le tableau numpy des taux.
    """
    titre("D.1 — DU DATAFRAME AU TABLEAU NUMPY")

    taux = df["taux"].to_numpy()
    print(f"df['taux'].to_numpy() → type : {type(taux).__name__}, "
          f"forme : {taux.shape}, dtype : {taux.dtype}")
    print("Les 5 premiers éléments :", taux[:5])

    # Calculs vectorisés : une seule instruction, aucune boucle for
    moyenne = taux.mean()
    ecart_type = taux.std(ddof=1)            # ddof=1 : écart-type d'échantillon, comme pandas
    variations = (taux[1:] / taux[:-1] - 1) * 100   # variation jour à jour en %

    print(f"\nMoyenne     : {moyenne:.6f}")
    print(f"Écart-type  : {ecart_type:.6f}")
    print(f"Variations jour à jour (%) — {len(variations)} valeurs, les 5 premières :")
    print(np.round(variations[:5], 4))
    print(f"Plus forte hausse : {variations.max():+.3f} %  |  "
          f"plus forte baisse : {variations.min():+.3f} %")
    print(f"Nombre de jours en hausse : {(variations > 0).sum()} sur {len(variations)}")

    # Vérification avec pandas
    print(f"\nVérification pandas : moyenne {df['taux'].mean():.6f}, "
          f"écart-type {df['taux'].std():.6f} ✅")
    return taux


def comparer_boucle_et_numpy():
    """Compare une boucle Python et numpy sur un grand tableau (somme et moyenne)."""
    print(f"\nBoucle Python ou numpy ? Moyenne de {TAILLE_GRANDE:,} nombres :".replace(",", " "))
    grand = np.random.default_rng(0).normal(1.17, 0.01, TAILLE_GRANDE)
    grande_liste = grand.tolist()

    def moyenne_boucle():
        somme = 0
        for x in grande_liste:
            somme += x
        return somme / len(grande_liste)

    t_boucle = chronometrer(moyenne_boucle, repetitions=3)
    t_numpy = chronometrer(grand.mean)
    print(f"  Boucle for  : {formater_duree(t_boucle)}")
    print(f"  numpy.mean  : {formater_duree(t_numpy)}")
    print(f"  👉 numpy est environ {t_boucle / t_numpy:.0f} fois plus rapide.")


# =====================================================================
# D.2 — COMPRENDRE NUMPY : DTYPE ET BROADCASTING
# =====================================================================

def dtype_et_broadcasting(taux):
    """Illustre la notion de dtype et le broadcasting.

    Paramètre :
        taux (ndarray) : le tableau numpy des taux.
    """
    titre("D.2 — COMPRENDRE NUMPY : DTYPE ET BROADCASTING")

    # --- dtype : tous les éléments d'un tableau ont le même type ---
    print("Le dtype = le type (unique) de tous les éléments du tableau :")
    exemples = {
        "np.array([1, 2, 3])": np.array([1, 2, 3]),
        "np.array([1.17, 1.16])": np.array([1.17, 1.16]),
        "np.array([1, 2.5])  (mélange)": np.array([1, 2.5]),
        "taux > 1.17  (comparaison)": taux[:3] > 1.17,
        "np.array([1, 'a'])  (mélange)": np.array([1, "a"]),
    }
    for nom, tableau in exemples.items():
        print(f"  {nom:<34} → dtype {str(tableau.dtype):<8} {tableau}")
    print("  👉 Un mélange est converti vers un type commun (ici l'entier devient décimal,")
    print("     ou tout devient texte). Une liste Python, elle, accepte n'importe quel mélange.")

    # --- broadcasting : opération entre un tableau et un nombre ---
    print("\nBroadcasting = le nombre est « diffusé » à chaque élément du tableau :")
    extrait = taux[:4]
    print(f"  taux              = {extrait}")
    print(f"  taux * 100        = {extrait * 100}")
    print(f"  taux - moyenne    = {np.round(extrait - taux.mean(), 4)}")
    print(f"  1 / taux          = {np.round(1 / extrait, 4)}   (taux inverse : 1 {DEVISE} en EUR)")

    # Comparaison avec une liste Python : * n'a pas du tout le même sens
    liste = [1.17, 1.16]
    print("\nAttention, avec une liste Python ce n'est pas pareil :")
    print(f"  [1.17, 1.16] * 2            = {liste * 2}   (la liste est répétée)")
    print(f"  np.array([1.17, 1.16]) * 2  = {np.array(liste) * 2}   (chaque élément est multiplié)")


# =====================================================================
# D.3 — APERÇU DE POLARS
# =====================================================================

def apercu_polars(chemin_csv, df_pandas):
    """Refait trois calculs en polars et compare syntaxe et temps avec pandas.

    Paramètres :
        chemin_csv (Path)        : le CSV des taux.
        df_pandas (DataFrame)    : les mêmes données chargées avec pandas.
    """
    titre("D.3 — APERÇU DE POLARS")
    try:
        import polars as pl
    except ImportError:
        print("❌ polars n'est pas installé. Dans le terminal, tapez :  pip install polars")
        print("   puis relancez ce script.")
        return

    df_polars = pl.read_csv(chemin_csv, try_parse_dates=True)
    print("Chargement : pl.read_csv(chemin, try_parse_dates=True)")
    print(df_polars.head(3))

    # --- Calcul 1 : moyenne ---
    print("\n1) Moyenne")
    print(f"   pandas : df['taux'].mean()                 → {df_pandas['taux'].mean():.6f}")
    moyenne_pl = df_polars.select(pl.col("taux").mean()).item()
    print(f"   polars : df.select(pl.col('taux').mean())  → {moyenne_pl:.6f}")

    # --- Calcul 2 : variation sur la période ---
    print("\n2) Variation sur la période (%)")
    var_pd = (df_pandas["taux"].iloc[-1] / df_pandas["taux"].iloc[0] - 1) * 100
    var_pl = df_polars.select(
        ((pl.col("taux").last() / pl.col("taux").first() - 1) * 100)
    ).item()
    print(f"   pandas : (s.iloc[-1] / s.iloc[0] - 1) * 100                       → {var_pd:+.3f} %")
    print(f"   polars : ((pl.col('taux').last() / pl.col('taux').first()) - 1) * 100 → {var_pl:+.3f} %")

    # --- Calcul 3 : regroupement par mois ---
    print("\n3) Moyenne par mois (regroupement)")
    mensuel_pd = (df_pandas.assign(mois=df_pandas["date"].dt.strftime("%Y-%m"))
                  .groupby("mois")["taux"].mean())
    mensuel_pl = (df_polars
                  .with_columns(pl.col("date").dt.strftime("%Y-%m").alias("mois"))
                  .group_by("mois")
                  .agg(pl.col("taux").mean().alias("moyenne"))
                  .sort("mois"))
    print("   pandas : df.groupby('mois')['taux'].mean()")
    print("   polars : df.group_by('mois').agg(pl.col('taux').mean())")
    print(mensuel_pl)
    identiques = np.allclose(mensuel_pd.to_numpy(), mensuel_pl["moyenne"].to_numpy())
    print(f"   Mêmes résultats que pandas : {'✅ oui' if identiques else '⚠️ non'}")

    # --- Évaluation paresseuse (lazy) ---
    print("\nÉvaluation paresseuse (lazy) : polars prépare tout le plan, puis exécute d'un coup")
    resultat_lazy = (pl.scan_csv(chemin_csv, try_parse_dates=True)   # rien n'est lu ici
                     .filter(pl.col("taux") > moyenne_pl)
                     .select(pl.len().alias("jours_au_dessus_de_la_moyenne"))
                     .collect())                                     # exécution ici
    print(resultat_lazy)

    # --- Comparaison des temps sur un grand jeu de données ---
    print(f"\nComparaison des temps sur {TAILLE_GRANDE:,} lignes "
          "(171 lignes, c'est trop peu pour voir une différence) :".replace(",", " "))
    rng = np.random.default_rng(0)
    valeurs = rng.normal(1.17, 0.01, TAILLE_GRANDE)
    groupes = rng.integers(0, 100, TAILLE_GRANDE)
    grand_pd = pd.DataFrame({"groupe": groupes, "taux": valeurs})
    grand_pl = pl.DataFrame({"groupe": groupes, "taux": valeurs})

    mesures = [
        ("Moyenne",
         lambda: grand_pd["taux"].mean(),
         lambda: grand_pl.select(pl.col("taux").mean())),
        ("Variation jour à jour",
         lambda: grand_pd["taux"].pct_change(),
         lambda: grand_pl.select(pl.col("taux").pct_change())),
        ("Moyenne par groupe",
         lambda: grand_pd.groupby("groupe")["taux"].mean(),
         lambda: grand_pl.group_by("groupe").agg(pl.col("taux").mean())),
    ]

    print(f"\n   {'Calcul':<24} | {'pandas':>10} | {'polars':>10} | {'rapport':>8}")
    print("   " + "-" * 61)
    lignes_tableau = []
    for nom, calcul_pd, calcul_pl in mesures:
        t_pd = chronometrer(calcul_pd)
        t_pl = chronometrer(calcul_pl)
        rapport = t_pd / t_pl
        print(f"   {nom:<24} | {formater_duree(t_pd):>10} | {formater_duree(t_pl):>10} | "
              f"{rapport:>7.1f}x")
        lignes_tableau.append((nom, t_pd, t_pl, rapport))
    print("   (rapport > 1 : polars est plus rapide ; < 1 : pandas est plus rapide)")

    print("\n📋 Tableau à copier dans docs/notes_seance3.md :\n")
    print(f"| Calcul ({TAILLE_GRANDE:,} lignes) | pandas | polars | pandas / polars |"
          .replace(",", " "))
    print("|---|---|---|---|")
    for nom, t_pd, t_pl, rapport in lignes_tableau:
        print(f"| {nom} | {formater_duree(t_pd)} | {formater_duree(t_pl)} | {rapport:.1f}x |")


# =====================================================================
# PROGRAMME PRINCIPAL
# =====================================================================

def main():
    """Lance les parties D.1, D.2 et D.3."""
    chemin_csv = trouver_csv(EMPLACEMENTS_POSSIBLES)
    if chemin_csv is None:
        print("❌ Fichier CSV introuvable. Emplacements essayés :")
        for chemin in EMPLACEMENTS_POSSIBLES:
            print("   -", chemin)
        return
    print("Fichier chargé :", chemin_csv)

    df = pd.read_csv(chemin_csv, parse_dates=["date"]).sort_values("date")

    taux = calculs_numpy(df)
    comparer_boucle_et_numpy()
    dtype_et_broadcasting(taux)
    apercu_polars(chemin_csv, df)


if __name__ == "__main__":
    main()
