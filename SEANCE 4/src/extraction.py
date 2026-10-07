# -*- coding: utf-8 -*-
"""
src/extraction.py
Module d'extraction : récupérer les taux sur l'API Frankfurter.

    extraire(devise, debut, fin)  -> appelle l'API, enregistre la réponse brute
                                     dans cache/ et une version CSV dans donnees/
    charger(devise, debut, fin)   -> relit les taux depuis le cache et renvoie
                                     un objet SerieTaux

Erreurs gérées avec try/except, suivi journalisé avec logging (séance 2).
"""

import csv
import json
import logging
import urllib.error
import urllib.request
from pathlib import Path

from serie_taux import SerieTaux, charger_serie

URL_API = "https://api.frankfurter.app"
DELAI_MAX = 10

# Les dossiers sont placés dans SEANCE 4, c'est-à-dire le dossier parent de src/
DOSSIER_RACINE = Path(__file__).resolve().parent.parent
DOSSIER_CACHE = DOSSIER_RACINE / "cache"
DOSSIER_DONNEES = DOSSIER_RACINE / "donnees"

logger = logging.getLogger(__name__)


def nom_fichier(devise, debut, fin):
    """Renvoie le nom commun des fichiers d'une série, sans extension.

    Paramètres :
        devise (str) : le code de la devise.
        debut, fin (date) : la période.
    Renvoie :
        str : par exemple "EUR_USD_2026-01-01_2026-09-01".
    """
    return f"EUR_{devise}_{debut:%Y-%m-%d}_{fin:%Y-%m-%d}"


def appeler_api(url):
    """Appelle l'API et renvoie la réponse JSON (dict), ou None en cas d'erreur.

    Paramètre :
        url (str) : l'adresse à appeler.
    """
    logger.info("Appel de l'API : %s", url)
    requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(requete, timeout=DELAI_MAX) as reponse:
            return json.loads(reponse.read().decode("utf-8"))
    except urllib.error.HTTPError as erreur:
        logger.error("Le serveur a refusé la requête (code HTTP %s).", erreur.code)
    except urllib.error.URLError as erreur:
        logger.error("Impossible de joindre l'API : %s", erreur.reason)
    except TimeoutError:
        logger.error("L'API n'a pas répondu en moins de %s secondes.", DELAI_MAX)
    except json.JSONDecodeError:
        logger.error("La réponse de l'API est illisible (JSON invalide).")
    return None


def extraire(devise, debut, fin):
    """Récupère les taux EUR -> devise sur la période, les enregistre et renvoie leur nombre.

    Paramètres :
        devise (str) : le code de la devise, par exemple "USD".
        debut, fin (date) : la période voulue.
    Renvoie :
        int : le nombre de jours récupérés (0 en cas d'échec).
    """
    url = f"{URL_API}/{debut:%Y-%m-%d}..{fin:%Y-%m-%d}?from=EUR&to={devise}"
    donnees = appeler_api(url)
    if donnees is None or not donnees.get("rates"):
        logger.warning("Aucun taux récupéré pour %s.", devise)
        return 0

    nom = nom_fichier(devise, debut, fin)
    DOSSIER_CACHE.mkdir(exist_ok=True)
    DOSSIER_DONNEES.mkdir(exist_ok=True)

    chemin_json = DOSSIER_CACHE / f"{nom}.json"
    with open(chemin_json, "w", encoding="utf-8") as fichier:
        json.dump(donnees, fichier, ensure_ascii=False, indent=2)
    logger.info("Réponse brute enregistrée : %s", chemin_json)

    chemin_csv = DOSSIER_DONNEES / f"{nom}.csv"
    with open(chemin_csv, "w", newline="", encoding="utf-8") as fichier:
        ecrivain = csv.writer(fichier)
        ecrivain.writerow(["date", "taux"])
        ecrivain.writerows((jour, valeurs[devise])
                           for jour, valeurs in sorted(donnees["rates"].items())
                           if devise in valeurs)
    logger.info("CSV enregistré : %s", chemin_csv)
    return len(donnees["rates"])


def charger(devise, debut, fin):
    """Charge la série d'une devise depuis le cache de la séance 4.

    Si la commande « extraire » n'a pas encore été lancée pour cette période,
    on cherche dans les fichiers des séances précédentes (mêmes dates par défaut).

    Paramètres :
        devise (str) : le code de la devise.
        debut, fin (date) : la période.
    Renvoie :
        SerieTaux, ou None si aucune donnée n'est trouvée.
    """
    chemin_json = DOSSIER_CACHE / f"{nom_fichier(devise, debut, fin)}.json"
    if chemin_json.exists():
        logger.info("%s : lu depuis %s", devise, chemin_json)
        return SerieTaux.depuis_json(chemin_json, devise)

    logger.warning("%s : pas de cache pour cette période dans SEANCE 4, "
                   "recherche dans les séances précédentes.", devise)
    serie = charger_serie(devise)
    if serie is None:
        return None

    # On ne garde que les dates de la période demandée
    couples = [(d, t) for d, t in zip(serie.dates, serie.taux) if debut <= d <= fin]
    if not couples:
        logger.error("%s : aucune donnée sur la période demandée. "
                     "Lancez d'abord la commande « extraire ».", devise)
        return None
    return SerieTaux(devise, couples)
