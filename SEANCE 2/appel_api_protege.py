# -*- coding: utf-8 -*-
"""
appel_api_protege.py
Séance 2 — Partie B : gérer les erreurs (try/except) et journaliser (logging).

On reprend l'appel à l'API Frankfurter de la séance 1 :
  B.1 — l'appel est entouré de try/except pour gérer les erreurs réseau
        (pas de connexion, code HTTP d'erreur comme 403, réponse illisible)
        et afficher un message clair au lieu de planter ;
  B.2 — les print de suivi sont remplacés par du logging, écrit dans le
        fichier appel_api.log, avec les niveaux :
          info    -> déroulement normal
          warning -> cas suspect (le programme continue)
          error   -> une opération a échoué

Si l'API ne répond pas, on se rabat sur la réponse déjà enregistrée
dans cache/ (si elle existe).

Uniquement la bibliothèque standard : urllib, json, csv, logging, pathlib.
"""

import csv
import json
import logging
import urllib.error
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------
# Paramètres : remplacer "USD" par la devise de votre groupe
# ---------------------------------------------------------------------
DEVISE_BASE = "EUR"
DEVISE = "USD"
DATE_DEBUT = "2026-01-01"
DATE_FIN = "2026-09-01"
URL_API = "https://api.frankfurter.app"
DELAI_MAX = 10  # secondes d'attente maximum pour la réponse du serveur

# Dossiers et fichiers, placés à côté de ce script
DOSSIER_SCRIPT = Path(__file__).resolve().parent
DOSSIER_CACHE = DOSSIER_SCRIPT / "cache"
DOSSIER_DONNEES = DOSSIER_SCRIPT / "donnees"
FICHIER_LOG = DOSSIER_SCRIPT / "appel_api.log"
NOM_FICHIERS = f"{DEVISE_BASE}_{DEVISE}_{DATE_DEBUT}_{DATE_FIN}"

# ---------------------------------------------------------------------
# Configuration du logging : les messages vont à la fois
#   - dans le fichier appel_api.log (pour garder une trace) ;
#   - dans le terminal (pour les voir pendant l'exécution).
# ---------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(FICHIER_LOG, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# =====================================================================
# FONCTIONS
# =====================================================================

def appeler_api(url):
    """Appelle l'API et renvoie la réponse JSON sous forme de dictionnaire.

    Les erreurs possibles sont gérées une par une, avec un message clair.

    Paramètre :
        url (str) : l'adresse à appeler.
    Renvoie :
        dict : la réponse de l'API, ou None si l'appel a échoué.
    """
    logger.info("Appel de l'API : %s", url)
    requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    try:
        with urllib.request.urlopen(requete, timeout=DELAI_MAX) as reponse:
            texte = reponse.read().decode("utf-8")
        donnees = json.loads(texte)

    except urllib.error.HTTPError as erreur:
        # Le serveur a répondu, mais avec un code d'erreur (403, 404, 500...)
        # HTTPError doit être placé AVANT URLError, car c'en est un cas particulier.
        logger.error("Le serveur a refusé la requête (code HTTP %s : %s).",
                     erreur.code, erreur.reason)
        return None

    except urllib.error.URLError as erreur:
        # Pas de réponse du serveur : pas d'internet, adresse fausse, proxy...
        logger.error("Impossible de joindre l'API : %s. "
                     "Vérifiez votre connexion internet.", erreur.reason)
        return None

    except TimeoutError:
        logger.error("L'API n'a pas répondu en moins de %s secondes.", DELAI_MAX)
        return None

    except json.JSONDecodeError:
        # Le serveur a répondu, mais pas avec du JSON lisible
        logger.error("La réponse de l'API est illisible (ce n'est pas du JSON valide).")
        return None

    else:
        # Exécuté seulement s'il n'y a eu aucune erreur
        logger.info("Réponse reçue et lue correctement.")
        return donnees


def lire_cache(chemin):
    """Relit une réponse de l'API enregistrée précédemment dans le cache.

    Paramètre :
        chemin (Path) : le fichier JSON du cache.
    Renvoie :
        dict : la réponse enregistrée, ou None si le fichier est absent ou abîmé.
    """
    try:
        with open(chemin, encoding="utf-8") as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        logger.error("Aucun cache trouvé : %s", chemin)
        return None
    except json.JSONDecodeError:
        logger.error("Le fichier de cache est abîmé : %s", chemin)
        return None


def enregistrer_cache(donnees, chemin):
    """Enregistre la réponse brute de l'API dans le cache (fichier JSON).

    Paramètres :
        donnees (dict) : la réponse de l'API.
        chemin (Path)  : le fichier JSON à écrire.
    """
    try:
        chemin.parent.mkdir(exist_ok=True)
        with open(chemin, "w", encoding="utf-8") as fichier:
            json.dump(donnees, fichier, ensure_ascii=False, indent=2)
    except OSError as erreur:
        logger.error("Impossible d'écrire le cache %s : %s", chemin, erreur)
    else:
        logger.info("Réponse brute enregistrée dans %s", chemin)


def ecrire_csv(taux_par_date, devise, chemin):
    """Écrit les taux dans un CSV simple : une ligne par date.

    Paramètres :
        taux_par_date (dict) : la partie « rates » de la réponse,
                               par exemple {"2026-01-02": {"USD": 1.17}, ...}.
        devise (str)         : la devise à extraire, par exemple "USD".
        chemin (Path)        : le fichier CSV à écrire.
    Renvoie :
        int : le nombre de lignes écrites.
    """
    nb_lignes = 0
    try:
        chemin.parent.mkdir(exist_ok=True)
        with open(chemin, "w", newline="", encoding="utf-8") as fichier:
            ecrivain = csv.writer(fichier)
            ecrivain.writerow(["date", "taux"])
            for date in sorted(taux_par_date):
                taux_du_jour = taux_par_date[date]
                if devise not in taux_du_jour:
                    # Cas suspect : on saute la date, mais on continue
                    logger.warning("Pas de taux %s pour le %s : date ignorée.", devise, date)
                    continue
                ecrivain.writerow([date, taux_du_jour[devise]])
                nb_lignes += 1
    except OSError as erreur:
        logger.error("Impossible d'écrire le CSV %s : %s", chemin, erreur)
    else:
        logger.info("CSV enregistré dans %s (%s lignes)", chemin, nb_lignes)
    return nb_lignes


# =====================================================================
# PROGRAMME PRINCIPAL
# =====================================================================

def main():
    """Enchaîne : taux du jour, puis série sur la période avec cache et CSV."""
    logger.info("===== Début du programme =====")

    try:
        # --- 1. Taux du jour ---
        url_jour = f"{URL_API}/latest?from={DEVISE_BASE}&to={DEVISE}"
        donnees_jour = appeler_api(url_jour)

        if donnees_jour is None:
            logger.warning("Taux du jour indisponible : on passe à la suite.")
        elif DEVISE not in donnees_jour.get("rates", {}):
            logger.warning("La réponse ne contient pas de taux %s.", DEVISE)
        else:
            print(f"\n👉 Le {donnees_jour['date']}, 1 {DEVISE_BASE} = "
                  f"{donnees_jour['rates'][DEVISE]} {DEVISE}\n")

        # --- 2. Série sur la période ---
        url_serie = f"{URL_API}/{DATE_DEBUT}..{DATE_FIN}?from={DEVISE_BASE}&to={DEVISE}"
        fichier_cache = DOSSIER_CACHE / f"{NOM_FICHIERS}.json"
        donnees_serie = appeler_api(url_serie)

        if donnees_serie is not None:
            enregistrer_cache(donnees_serie, fichier_cache)
        else:
            # Plan B : on réutilise la dernière réponse enregistrée
            logger.warning("L'API ne répond pas : utilisation du cache %s", fichier_cache)
            donnees_serie = lire_cache(fichier_cache)

        if donnees_serie is None:
            logger.error("Ni l'API ni le cache ne sont disponibles : arrêt.")
            print("\n❌ Impossible de récupérer les taux. "
                  f"Consultez le fichier {FICHIER_LOG.name} pour le détail.")
            return

        taux_par_date = donnees_serie.get("rates", {})
        if len(taux_par_date) == 0:
            logger.warning("La réponse ne contient aucun taux pour cette période.")
            return

        fichier_csv = DOSSIER_DONNEES / f"{NOM_FICHIERS}.csv"
        nb_lignes = ecrire_csv(taux_par_date, DEVISE, fichier_csv)
        print(f"\n✅ {nb_lignes} taux enregistrés dans donnees/{fichier_csv.name}")

    finally:
        # Exécuté dans tous les cas, erreur ou pas
        logger.info("===== Fin du programme =====")


if __name__ == "__main__":
    main()
