# -*- coding: utf-8 -*-
"""
serie_taux.py
Séance 4 — Partie B : la programmation orientée objet (les classes).

B.1 — Une première classe, SerieTaux, qui regroupe des DONNÉES (les taux
      d'une devise) et des MÉTHODES (moyenne, variation, taux à une date).
      On y voit __init__, les attributs, les méthodes et le paramètre self.
B.2 — Plusieurs objets : une instance par devise. Différence entre un
      attribut de CLASSE (partagé) et un attribut d'INSTANCE (propre à
      chaque objet). Le piège de la liste mutable en attribut de classe.
B.3 — Les dataclasses : la même classe sans écrire __init__ soi-même.

Les taux sont relus depuis les fichiers cache/ (JSON) des séances
précédentes, ou à défaut depuis le CSV de la séance 1.

Uniquement la bibliothèque standard : json, csv, datetime, dataclasses, pathlib.
"""

import csv
import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------
# Paramètres : les deux devises du groupe
# ---------------------------------------------------------------------
DEVISES = ["USD", "GBP"]
PERIODE = "2026-01-01_2026-09-01"

DOSSIER_SCRIPT = Path(__file__).resolve().parent
DOSSIER_PROJET = DOSSIER_SCRIPT.parent
SEANCES = ["SEANCE 4", "SEANCE 3", "SEANCE 2", "SEANCE 1"]


def titre(texte):
    """Affiche un titre de partie encadré."""
    print(f"\n{'=' * 70}\n{texte}\n{'=' * 70}")


# =====================================================================
# B.1 — VOTRE PREMIÈRE CLASSE
# =====================================================================

class SerieTaux:
    """Une série de taux de change EUR -> devise, avec ses calculs.

    Attributs de classe (partagés par toutes les séries) :
        base (str)   : la devise de base, toujours "EUR".
        source (str) : l'origine des données.
        nb_series (int) : compteur du nombre de séries créées.

    Attributs d'instance (propres à chaque série) :
        devise (str)         : le code de la devise, par exemple "USD".
        dates (list de date) : les dates, triées.
        taux (list de float) : les taux, dans le même ordre que les dates.
    """

    # --- Attributs de CLASSE : définis ici, partagés par tous les objets ---
    base = "EUR"
    source = "BCE (via l'API Frankfurter)"
    nb_series = 0

    def __init__(self, devise, couples):
        """Crée une série à partir d'une devise et d'une liste de couples (date, taux).

        __init__ est appelée automatiquement quand on écrit SerieTaux(...).
        self désigne l'objet en train d'être créé.

        Paramètres :
            devise (str)               : le code de la devise.
            couples (list de tuples)   : des couples (date, taux), dans n'importe quel ordre.
        """
        if not couples:
            raise ValueError(f"La série {devise} ne contient aucun taux.")

        # --- Attributs d'INSTANCE : self.xxx, propres à CET objet ---
        couples_tries = sorted(couples)
        self.devise = devise
        self.dates = [d for d, _ in couples_tries]
        self.taux = [t for _, t in couples_tries]

        # On modifie l'attribut de classe : visible depuis toutes les séries
        SerieTaux.nb_series += 1

    # --- Façons de créer une série depuis un fichier (méthodes de classe) ---

    @classmethod
    def depuis_json(cls, chemin, devise):
        """Crée une série à partir d'une réponse brute de l'API (fichier du cache/).

        Paramètres :
            chemin (Path) : le fichier JSON, au format {"rates": {"2026-01-02": {"USD": 1.17}}}.
            devise (str)  : la devise à extraire.
        Renvoie :
            SerieTaux.
        """
        with open(chemin, encoding="utf-8") as fichier:
            donnees = json.load(fichier)
        couples = [(date.fromisoformat(jour), valeurs[devise])
                   for jour, valeurs in donnees["rates"].items() if devise in valeurs]
        return cls(devise, couples)

    @classmethod
    def depuis_csv(cls, chemin, devise):
        """Crée une série à partir d'un CSV « date,taux ».

        Paramètres :
            chemin (Path) : le fichier CSV.
            devise (str)  : la devise correspondante.
        Renvoie :
            SerieTaux.
        """
        with open(chemin, newline="", encoding="utf-8") as fichier:
            couples = [(date.fromisoformat(ligne["date"]), float(ligne["taux"]))
                       for ligne in csv.DictReader(fichier)]
        return cls(devise, couples)

    # --- Méthodes : des fonctions qui travaillent sur les données de self ---

    def moyenne(self):
        """Renvoie la moyenne des taux de la série."""
        return sum(self.taux) / len(self.taux)

    def minimum(self):
        """Renvoie le couple (date, taux) du taux le plus bas."""
        return min(zip(self.dates, self.taux), key=lambda couple: couple[1])

    def maximum(self):
        """Renvoie le couple (date, taux) du taux le plus haut."""
        return max(zip(self.dates, self.taux), key=lambda couple: couple[1])

    def variation(self):
        """Renvoie la variation en % entre le premier et le dernier taux."""
        return (self.taux[-1] / self.taux[0] - 1) * 100

    def variations_quotidiennes(self):
        """Renvoie la liste des variations jour à jour, en %."""
        return [(apres / avant - 1) * 100 for avant, apres in zip(self.taux, self.taux[1:])]

    def taux_a(self, jour):
        """Renvoie le taux à une date donnée.

        Si la date n'a pas de taux (week-end, jour férié), on renvoie le dernier
        taux connu avant elle (même logique que le forward-fill de la séance 3).

        Paramètre :
            jour (date ou str) : la date voulue, par exemple "2026-05-01".
        Renvoie :
            float, ou None si la date est avant le début de la série.
        """
        if isinstance(jour, str):
            jour = date.fromisoformat(jour)
        connus = [t for d, t in zip(self.dates, self.taux) if d <= jour]
        return connus[-1] if connus else None

    # --- Méthodes spéciales : comment l'objet s'affiche et se mesure ---

    def __len__(self):
        """Permet d'écrire len(serie) : le nombre de jours de la série."""
        return len(self.taux)

    def __repr__(self):
        """Ce qui s'affiche quand on fait print(serie)."""
        return (f"SerieTaux({self.base}/{self.devise}, {len(self)} jours, "
                f"du {self.dates[0]} au {self.dates[-1]})")


# =====================================================================
# B.2 — LE PIÈGE DE LA LISTE MUTABLE EN ATTRIBUT DE CLASSE
# =====================================================================

class SerieAvecPiege:
    """MAUVAIS EXEMPLE : une liste déclarée comme attribut de classe."""

    historique = []          # ❌ une seule liste, partagée par TOUS les objets

    def __init__(self, devise):
        """Crée une série vide pour une devise."""
        self.devise = devise

    def noter(self, message):
        """Ajoute un message à l'historique."""
        self.historique.append(f"{self.devise} : {message}")


class SerieCorrigee:
    """BON EXEMPLE : la liste est créée dans __init__, une par objet."""

    def __init__(self, devise):
        """Crée une série vide pour une devise, avec son propre historique."""
        self.devise = devise
        self.historique = []     # ✅ une nouvelle liste pour CHAQUE objet

    def noter(self, message):
        """Ajoute un message à l'historique."""
        self.historique.append(f"{self.devise} : {message}")


# =====================================================================
# B.3 — LES DATACLASSES
# =====================================================================

@dataclass
class SerieTauxDC:
    """La même série, en dataclass : __init__, __repr__ et __eq__ sont écrits
    automatiquement par Python à partir des attributs déclarés ci-dessous."""

    devise: str
    dates: list = field(default_factory=list)   # default_factory : une liste neuve par objet
    taux: list = field(default_factory=list)
    base: str = "EUR"

    def moyenne(self):
        """Renvoie la moyenne des taux."""
        return sum(self.taux) / len(self.taux)

    def variation(self):
        """Renvoie la variation en % entre le premier et le dernier taux."""
        return (self.taux[-1] / self.taux[0] - 1) * 100


# =====================================================================
# CHARGEMENT DES SÉRIES
# =====================================================================

def charger_serie(devise):
    """Cherche les taux d'une devise dans les dossiers cache/ ou donnees/ des séances.

    Paramètre :
        devise (str) : le code de la devise.
    Renvoie :
        SerieTaux, ou None si aucun fichier n'est trouvé.
    """
    nom = f"EUR_{devise}_{PERIODE}"
    for seance in SEANCES:
        dossier = DOSSIER_SCRIPT if seance == DOSSIER_SCRIPT.name else DOSSIER_PROJET / seance
        chemin_json = dossier / "cache" / f"{nom}.json"
        chemin_csv = dossier / "donnees" / f"{nom}.csv"
        if chemin_json.exists():
            print(f"   {devise} : lu depuis {seance}/cache/{chemin_json.name}")
            return SerieTaux.depuis_json(chemin_json, devise)
        if chemin_csv.exists():
            print(f"   {devise} : lu depuis {seance}/donnees/{chemin_csv.name}")
            return SerieTaux.depuis_csv(chemin_csv, devise)
    print(f"   ❌ {devise} : aucun fichier trouvé (lancez jointures.py de la séance 3).")
    return None


# =====================================================================
# PROGRAMME PRINCIPAL
# =====================================================================

def demo_b1(serie):
    """Utilise les méthodes d'une série (B.1)."""
    titre(f"B.1 — UNE PREMIÈRE CLASSE : SerieTaux ({serie.devise})")
    print(f"print(serie)              → {serie}")
    print(f"type(serie)               → {type(serie).__name__}")
    print(f"serie.devise              → {serie.devise}   (attribut d'instance)")
    print(f"len(serie)                → {len(serie)}")
    print(f"serie.moyenne()           → {serie.moyenne():.4f}")
    date_min, taux_min = serie.minimum()
    date_max, taux_max = serie.maximum()
    print(f"serie.minimum()           → {taux_min} le {date_min:%d/%m/%Y}")
    print(f"serie.maximum()           → {taux_max} le {date_max:%d/%m/%Y}")
    print(f"serie.variation()         → {serie.variation():+.2f} %")
    print(f"serie.taux_a('2026-03-02')→ {serie.taux_a('2026-03-02')}")
    print(f"serie.taux_a('2026-05-01')→ {serie.taux_a('2026-05-01')}   "
          "(1er mai férié : dernier taux connu)")
    print("\n👉 serie.moyenne() est équivalent à SerieTaux.moyenne(serie) :")
    print(f"   SerieTaux.moyenne(serie) → {SerieTaux.moyenne(serie):.4f}   "
          "(self = l'objet sur lequel on appelle la méthode)")


def demo_b2(series):
    """Compare plusieurs instances, attributs de classe et d'instance (B.2)."""
    titre("B.2 — PLUSIEURS OBJETS")
    print(f"{'Devise':<8} | {'Jours':>5} | {'Moyenne':>8} | {'Variation':>10} | "
          f"{'Base':>4} | Source")
    print("-" * 70)
    for serie in series:
        print(f"{serie.devise:<8} | {len(serie):>5} | {serie.moyenne():>8.4f} | "
              f"{serie.variation():>+9.2f} % | {serie.base:>4} | {serie.source}")

    print(f"\nAttribut de CLASSE   SerieTaux.nb_series = {SerieTaux.nb_series} "
          "(compte toutes les séries créées)")
    print("Attributs d'INSTANCE : chaque objet a ses propres valeurs")
    for serie in series:
        print(f"   {serie.devise} → serie.taux[0] = {serie.taux[0]}")

    s1 = series[0]
    print(f"\nModifier un attribut de classe touche tous les objets :")
    SerieTaux.source = "BCE"
    print(f"   SerieTaux.source = 'BCE'  →  "
          + ", ".join(f"{s.devise}.source = '{s.source}'" for s in series))
    print("Affecter self.xxx crée un attribut d'instance qui « cache » celui de la classe :")
    s1.source = "fichier local"
    print(f"   {s1.devise}.source = 'fichier local'  →  "
          + ", ".join(f"{s.devise}.source = '{s.source}'" for s in series))

    print("\n⚠️ Le piège de la liste mutable en attribut de classe :")
    a, b = SerieAvecPiege("USD"), SerieAvecPiege("GBP")
    a.noter("chargée")
    print(f"   MAUVAIS : on note seulement sur USD, mais GBP.historique = {b.historique}")
    print(f"             a.historique is b.historique → {a.historique is b.historique} "
          "(c'est la MÊME liste)")
    a, b = SerieCorrigee("USD"), SerieCorrigee("GBP")
    a.noter("chargée")
    print(f"   CORRIGÉ : on note seulement sur USD,       GBP.historique = {b.historique}")
    print(f"             a.historique is b.historique → {a.historique is b.historique}")
    print("   👉 Même piège qu'en séance 1 : deux noms qui pointent vers la même liste.")


def demo_b3(serie):
    """Compare la classe écrite à la main avec une dataclass (B.3)."""
    titre("B.3 — LES DATACLASSES")
    dc = SerieTauxDC(serie.devise, serie.dates, serie.taux)
    print("@dataclass écrit automatiquement __init__, __repr__ et __eq__ :")
    print(f"   SerieTauxDC('{dc.devise}', dates, taux).moyenne()   → {dc.moyenne():.4f}")
    print(f"   Même résultat que SerieTaux.moyenne()            → "
          f"{abs(dc.moyenne() - serie.moyenne()) < 1e-12}")

    petite = SerieTauxDC("USD", [date(2026, 1, 2), date(2026, 1, 5)], [1.17, 1.16])
    print(f"   print(petite) → {petite}")
    copie = SerieTauxDC("USD", [date(2026, 1, 2), date(2026, 1, 5)], [1.17, 1.16])
    print(f"   petite == copie → {petite == copie}   "
          "(__eq__ compare les attributs ; avec une classe normale ce serait False)")
    vide_1, vide_2 = SerieTauxDC("USD"), SerieTauxDC("GBP")
    vide_1.taux.append(1.17)
    print(f"   field(default_factory=list) évite le piège : GBP.taux = {vide_2.taux}")


def main():
    """Charge une série par devise puis lance les démonstrations B.1, B.2 et B.3."""
    print("Chargement des séries :")
    series = [serie for serie in map(charger_serie, DEVISES) if serie is not None]
    if not series:
        print("❌ Aucune série chargée : impossible de continuer.")
        return

    demo_b1(series[0])
    demo_b2(series)
    demo_b3(series[0])


if __name__ == "__main__":
    main()
