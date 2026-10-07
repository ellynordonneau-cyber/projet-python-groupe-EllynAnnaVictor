# -*- coding: utf-8 -*-
"""
appel_api.py
Partie C.2 — Appeler l'API Frankfurter pour de vrai.

Uniquement la bibliothèque standard : urllib, json, csv, pathlib.

1. Taux du jour  : on affiche le taux et la date.
2. Série 2026    : on enregistre la réponse brute dans cache/
                   puis une version simple en CSV dans donnees/.
"""

import csv
import json
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

# Dossiers de sortie (créés s'ils n'existent pas), placés à côté de ce script
DOSSIER_SCRIPT = Path(__file__).resolve().parent
DOSSIER_CACHE = DOSSIER_SCRIPT / "cache"
DOSSIER_DONNEES = DOSSIER_SCRIPT / "donnees"
DOSSIER_CACHE.mkdir(exist_ok=True)
DOSSIER_DONNEES.mkdir(exist_ok=True)


def appeler_api(url):
    """Appelle une URL et renvoie la réponse JSON sous forme de dictionnaire."""
    # Un User-Agent évite que certains serveurs refusent la requête
    requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(requete) as reponse:
        texte = reponse.read().decode("utf-8")
    return json.loads(texte)


# =====================================================================
# 1. TAUX DU JOUR
# =====================================================================
print("=" * 60)
print("1. TAUX DU JOUR")
print("=" * 60)

url_jour = f"{URL_API}/latest?from={DEVISE_BASE}&to={DEVISE}"
print("URL appelée :", url_jour)

donnees_jour = appeler_api(url_jour)
print("Réponse complète :", donnees_jour)

taux_jour = donnees_jour["rates"][DEVISE]
date_jour = donnees_jour["date"]
print(f"Le {date_jour}, 1 {DEVISE_BASE} = {taux_jour} {DEVISE}")


# =====================================================================
# 2. SÉRIE SUR UNE PÉRIODE
# =====================================================================
print()
print("=" * 60)
print("2. SÉRIE SUR UNE PÉRIODE")
print("=" * 60)

url_serie = f"{URL_API}/{DATE_DEBUT}..{DATE_FIN}?from={DEVISE_BASE}&to={DEVISE}"
print("URL appelée :", url_serie)

donnees_serie = appeler_api(url_serie)

# --- a) Enregistrer la réponse brute dans cache/ ---
fichier_cache = DOSSIER_CACHE / f"{DEVISE_BASE}_{DEVISE}_{DATE_DEBUT}_{DATE_FIN}.json"
with open(fichier_cache, "w", encoding="utf-8") as f:
    json.dump(donnees_serie, f, ensure_ascii=False, indent=2)
print("Réponse brute enregistrée dans :", fichier_cache)

# --- b) Écrire une version simple en CSV dans donnees/ ---
# "rates" ressemble à : {"2026-01-02": {"USD": 1.03}, "2026-01-05": {...}, ...}
taux_par_date = donnees_serie["rates"]

fichier_csv = DOSSIER_DONNEES / f"{DEVISE_BASE}_{DEVISE}_{DATE_DEBUT}_{DATE_FIN}.csv"
with open(fichier_csv, "w", newline="", encoding="utf-8") as f:
    ecrivain = csv.writer(f)
    ecrivain.writerow(["date", "taux"])          # ligne d'en-tête
    for date in sorted(taux_par_date):           # une ligne par date
        ecrivain.writerow([date, taux_par_date[date][DEVISE]])

print("CSV enregistré dans :", fichier_csv)
print(f"Nombre de jours ouvrés : {len(taux_par_date)}")

# Petit aperçu des premières lignes
print("\nAperçu :")
for date in sorted(taux_par_date)[:5]:
    print(f"  {date} : {taux_par_date[date][DEVISE]}")