# -*- coding: utf-8 -*-
"""
jointures.py
Séance 3 — Partie C : les jointures.

C.1 — Réunir deux séries : on récupère les taux des deux devises du groupe
      (un DataFrame par devise) et on les réunit en un seul DataFrame
      indexé par date avec pd.merge (jointure sur la date).
C.2 — Les quatre types de jointure : deux petites tables aux clés
      partiellement communes ({1, 2} à gauche, {2, 3} à droite), jointes
      avec how = "inner", "left", "right" et "outer".
      + l'effet de la duplication d'une clé.
C.3 — merge, join ou concat : trois façons d'assembler des tables.

Installation préalable (une seule fois) : pip install pandas
"""

import json
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------
# Paramètres : mettre ici les DEUX devises du groupe
# ---------------------------------------------------------------------
DEVISE_1 = "USD"
DEVISE_2 = "GBP"
DATE_DEBUT = "2026-01-01"
DATE_FIN = "2026-09-01"
URL_API = "https://api.frankfurter.app"

DOSSIER_SCRIPT = Path(__file__).resolve().parent
DOSSIER_CACHE = DOSSIER_SCRIPT / "cache"
DOSSIER_DONNEES = DOSSIER_SCRIPT / "donnees"

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


# =====================================================================
# RÉCUPÉRATION DES TAUX D'UNE DEVISE (API + cache)
# =====================================================================

def recuperer_taux(devise):
    """Récupère les taux EUR -> devise sur la période et renvoie un DataFrame.

    On appelle l'API Frankfurter ; la réponse brute est enregistrée dans cache/.
    Si l'API ne répond pas, on réutilise le cache s'il existe.

    Paramètre :
        devise (str) : le code de la devise, par exemple "USD".
    Renvoie :
        DataFrame : colonnes « date » et « taux_<devise> », ou None si échec.
    """
    url = f"{URL_API}/{DATE_DEBUT}..{DATE_FIN}?from=EUR&to={devise}"
    fichier_cache = DOSSIER_CACHE / f"EUR_{devise}_{DATE_DEBUT}_{DATE_FIN}.json"

    try:
        requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(requete, timeout=10) as reponse:
            donnees = json.loads(reponse.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as erreur:
        print(f"⚠️ API indisponible pour {devise} ({erreur}) : lecture du cache.")
        try:
            with open(fichier_cache, encoding="utf-8") as f:
                donnees = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"❌ Pas de cache utilisable pour {devise} : {fichier_cache}")
            return None
    else:
        DOSSIER_CACHE.mkdir(exist_ok=True)
        with open(fichier_cache, "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=2)
        print(f"✅ Taux {devise} reçus de l'API ({len(donnees['rates'])} jours), "
              f"réponse brute enregistrée dans cache/{fichier_cache.name}")

    # "rates" = {"2026-01-02": {"USD": 1.17}, ...}  ->  tableau date | taux_USD
    lignes = [(date, taux_du_jour[devise]) for date, taux_du_jour in donnees["rates"].items()]
    df = pd.DataFrame(lignes, columns=["date", f"taux_{devise}"])
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


# =====================================================================
# C.1 — RÉUNIR DEUX SÉRIES
# =====================================================================

def reunir_deux_devises(df_1, df_2):
    """Réunit les taux de deux devises en un seul DataFrame indexé par date.

    Paramètres :
        df_1 (DataFrame) : colonnes « date » et « taux_<devise 1> ».
        df_2 (DataFrame) : colonnes « date » et « taux_<devise 2> ».
    Renvoie :
        DataFrame : index « date », une colonne de taux par devise.
    """
    titre(f"C.1 — RÉUNIR LES TAUX {DEVISE_1} ET {DEVISE_2} (jointure sur la date)")

    print(f"Table {DEVISE_1} : {len(df_1)} lignes")
    print(df_1.head(3))
    print(f"\nTable {DEVISE_2} : {len(df_2)} lignes")
    print(df_2.head(3))

    # validate="one_to_one" : pandas vérifie qu'aucune date n'est en double
    df = pd.merge(df_1, df_2, on="date", how="inner", validate="one_to_one")
    df = df.set_index("date")

    print(f"\nRésultat de pd.merge(..., on='date', how='inner') : {len(df)} lignes")
    print(df.head())

    # Vérification du nombre de lignes après la jointure
    if len(df) == len(df_1) == len(df_2):
        print(f"\n✅ Jointure complète : les {len(df)} dates coïncident dans les deux tables, "
              "aucune ligne perdue.")
    else:
        print(f"\n⚠️ Jointure incomplète : {len(df_1)} et {len(df_2)} lignes au départ, "
              f"{len(df)} à l'arrivée.")

    # Un petit calcul rendu possible par la jointure : le taux croisé
    df[f"{DEVISE_2}_par_{DEVISE_1}"] = df[f"taux_{DEVISE_2}"] / df[f"taux_{DEVISE_1}"]
    print(f"\nTaux croisé (1 {DEVISE_1} = ? {DEVISE_2}), calculé grâce à la jointure :")
    print(df.tail(3))
    return df


# =====================================================================
# C.2 — LES QUATRE TYPES DE JOINTURE
# =====================================================================

def quatre_types_de_jointure():
    """Compare inner, left, right et outer sur deux petites tables.

    Table de gauche : clés {1, 2} ; table de droite : clés {2, 3}.
    """
    titre("C.2 — LES QUATRE TYPES DE JOINTURE")

    gauche = pd.DataFrame({"cle": [1, 2], "valeur_gauche": ["A", "B"]})
    droite = pd.DataFrame({"cle": [2, 3], "valeur_droite": ["X", "Y"]})
    print("Table de gauche (clés {1, 2}) :")
    print(gauche)
    print("\nTable de droite (clés {2, 3}) :")
    print(droite)

    explications = {
        "inner": "intersection : seulement les clés présentes des deux côtés",
        "left": "toutes les lignes de gauche ; NaN à droite si pas de correspondance",
        "right": "toutes les lignes de droite ; NaN à gauche si pas de correspondance",
        "outer": "union : toutes les clés ; NaN là où il manque une correspondance",
    }

    resume = []
    for how, explication in explications.items():
        resultat = pd.merge(gauche, droite, on="cle", how=how)
        cles = sorted(resultat["cle"].tolist())
        print(f"\n--- how='{how}' → clés conservées {set(cles)} ({explication})")
        print(resultat)
        resume.append({"how": how, "clés conservées": str(set(cles)),
                       "nb de lignes": len(resultat),
                       "nb de NaN": int(resultat.isna().sum().sum())})

    print("\nRésumé :")
    print(pd.DataFrame(resume).to_string(index=False))


def attention_duplication():
    """Montre qu'une clé présente plusieurs fois produit toutes les combinaisons."""
    titre("C.2 — ATTENTION À LA DUPLICATION")

    gauche = pd.DataFrame({"cle": [1, 1], "valeur_gauche": ["A1", "A2"]})
    droite = pd.DataFrame({"cle": [1, 1, 1], "valeur_droite": ["X1", "X2", "X3"]})
    resultat = pd.merge(gauche, droite, on="cle", how="inner")

    print("La clé 1 apparaît 2 fois à gauche et 3 fois à droite.")
    print(f"Résultat : {len(resultat)} lignes (2 × 3 = 6 combinaisons) :")
    print(resultat)
    print("👉 Toujours vérifier le nombre de lignes après un merge "
          "(ou utiliser validate='one_to_one').")


# =====================================================================
# C.3 — MERGE, JOIN OU CONCAT ?
# =====================================================================

def merge_join_concat():
    """Compare trois façons d'assembler des tables : merge, join et concat."""
    titre("C.3 — MERGE, JOIN OU CONCAT ?")

    janvier = pd.DataFrame({"date": ["2026-01-02", "2026-01-05"], "taux": [1.17, 1.16]})
    fevrier = pd.DataFrame({"date": ["2026-02-02", "2026-02-03"], "taux": [1.18, 1.19]})

    # concat : empile les tables (les unes sous les autres), sans apparier de clé
    empile = pd.concat([janvier, fevrier], ignore_index=True)
    print("pd.concat([janvier, fevrier]) → les lignes sont empilées :")
    print(empile)

    usd = pd.DataFrame({"date": ["2026-01-02", "2026-01-05"], "USD": [1.17, 1.16]})
    gbp = pd.DataFrame({"date": ["2026-01-02", "2026-01-05"], "GBP": [0.87, 0.86]})

    # merge : joint sur une COLONNE clé
    print("\npd.merge(usd, gbp, on='date') → appariement sur la colonne 'date' :")
    print(pd.merge(usd, gbp, on="date"))

    # join : joint sur l'INDEX
    print("\nusd.set_index('date').join(gbp.set_index('date')) → appariement sur l'index :")
    print(usd.set_index("date").join(gbp.set_index("date")))

    print("\n👉 merge = sur une colonne clé | join = sur l'index | "
          "concat = empile, sans clé.")


# =====================================================================
# PROGRAMME PRINCIPAL
# =====================================================================

def main():
    """Lance les trois parties C.1, C.2 et C.3."""
    titre(f"RÉCUPÉRATION DES TAUX {DEVISE_1} ET {DEVISE_2}")
    df_1 = recuperer_taux(DEVISE_1)
    df_2 = recuperer_taux(DEVISE_2)

    if df_1 is not None and df_2 is not None:
        df = reunir_deux_devises(df_1, df_2)
        DOSSIER_DONNEES.mkdir(exist_ok=True)
        fichier = DOSSIER_DONNEES / f"EUR_{DEVISE_1}_{DEVISE_2}_{DATE_DEBUT}_{DATE_FIN}.csv"
        df.to_csv(fichier)
        print(f"\nTable jointe enregistrée dans donnees/{fichier.name}")
    else:
        print("\n❌ Impossible de récupérer les deux devises : partie C.1 ignorée.")

    quatre_types_de_jointure()
    attention_duplication()
    merge_join_concat()


if __name__ == "__main__":
    main()
