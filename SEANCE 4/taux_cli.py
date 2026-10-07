# -*- coding: utf-8 -*-
"""
taux_cli.py
Séance 4 — Partie D.1 : l'outil en ligne de commande (argparse).

Une commande unique avec trois sous-commandes :

    python taux_cli.py extraire   --devises USD GBP --debut 2026-01-01 --fin 2026-09-01
    python taux_cli.py analyser   --devises USD GBP [--date 2026-05-01] [--export]
    python taux_cli.py graphiques --devises USD GBP

    python taux_cli.py --help              (aide générale)
    python taux_cli.py analyser --help     (aide d'une sous-commande)

Organisation du code en modules :
    src/extraction.py  -> récupérer les taux (API, cache, CSV)
    src/statistiques.py -> statistiques des séries
    serie_taux.py      -> la classe SerieTaux
    graphiques.py      -> les graphiques matplotlib
"""

import argparse
import logging
import sys
from datetime import date
from pathlib import Path

from src.statistiques import afficher_resume, exporter_resume
from src.extraction import charger, extraire

DOSSIER_SCRIPT = Path(__file__).resolve().parent
FICHIER_LOG = DOSSIER_SCRIPT / "taux.log"

DEVISES_PAR_DEFAUT = ["USD", "GBP"]
DEBUT_PAR_DEFAUT = "2026-01-01"
FIN_PAR_DEFAUT = "2026-09-01"


# =====================================================================
# LES SOUS-COMMANDES (une fonction par sous-commande)
# =====================================================================

def commande_extraire(args):
    """Sous-commande « extraire » : télécharge les taux de chaque devise.

    Paramètre :
        args (Namespace) : les arguments lus par argparse.
    Renvoie :
        int : 0 si tout s'est bien passé, 1 sinon (code de sortie).
    """
    print(f"Extraction de {', '.join(args.devises)} "
          f"du {args.debut:%d/%m/%Y} au {args.fin:%d/%m/%Y}…")
    echecs = 0
    for devise in args.devises:
        nb_jours = extraire(devise, args.debut, args.fin)
        if nb_jours:
            print(f"   ✅ {devise} : {nb_jours} jours enregistrés (cache/ et donnees/)")
        else:
            print(f"   ❌ {devise} : échec, voir {FICHIER_LOG.name}")
            echecs += 1
    return 1 if echecs else 0


def charger_series(args):
    """Charge une SerieTaux par devise demandée (sous-commandes analyser et graphiques).

    Paramètre :
        args (Namespace) : les arguments lus par argparse.
    Renvoie :
        list de SerieTaux : les séries trouvées (peut être vide).
    """
    series = [charger(devise, args.debut, args.fin) for devise in args.devises]
    return [serie for serie in series if serie is not None]


def commande_analyser(args):
    """Sous-commande « analyser » : affiche les statistiques de chaque devise.

    Paramètre :
        args (Namespace) : les arguments lus par argparse.
    Renvoie :
        int : code de sortie (0 = succès).
    """
    series = charger_series(args)
    if not series:
        print("❌ Aucune donnée. Lancez d'abord : python taux_cli.py extraire")
        return 1

    afficher_resume(series)

    if args.date:
        print(f"\nTaux au {args.date:%d/%m/%Y} :")
        for serie in series:
            taux = serie.taux_a(args.date)
            texte = f"{taux:.4f}" if taux is not None else "pas de donnée"
            print(f"   1 EUR = {texte} {serie.devise}")

    if args.export:
        chemin = DOSSIER_SCRIPT / "donnees" / "resume_analyse.csv"
        exporter_resume(series, chemin)
        print(f"\n✅ Résumé exporté dans donnees/{chemin.name}")
    return 0


def commande_graphiques(args):
    """Sous-commande « graphiques » : produit les graphiques PNG.

    Paramètre :
        args (Namespace) : les arguments lus par argparse.
    Renvoie :
        int : code de sortie (0 = succès).
    """
    # Import ici : matplotlib n'est chargé que si on demande des graphiques
    import graphiques

    series = charger_series(args)
    if not series:
        print("❌ Aucune donnée. Lancez d'abord : python taux_cli.py extraire")
        return 1

    print(f"Création des graphiques dans {graphiques.DOSSIER_GRAPHIQUES} :")
    graphiques.courbe_une_devise(series[0], graphiques.COULEURS[0])
    if len(series) >= 2:
        graphiques.comparer_deux_devises(series[:2])
    for i, serie in enumerate(series[:2]):
        graphiques.histogramme_variations(serie, graphiques.COULEURS[i])
    graphiques.tableau_de_bord(series[:2])
    return 0


# =====================================================================
# CONSTRUCTION DE LA LIGNE DE COMMANDE
# =====================================================================

def lire_date(texte):
    """Convertit un texte AAAA-MM-JJ en date, avec un message clair si c'est invalide.

    Paramètre :
        texte (str) : la date tapée par l'utilisateur.
    Renvoie :
        date.
    """
    try:
        return date.fromisoformat(texte)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"date invalide : '{texte}' (format attendu : AAAA-MM-JJ, ex. 2026-01-01)")


def creer_parser():
    """Construit l'analyseur de la ligne de commande et ses sous-commandes.

    Renvoie :
        ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        prog="taux_cli.py",
        description="Outil d'analyse des taux de change de la BCE (API Frankfurter).",
        epilog="Exemple : python taux_cli.py analyser --devises USD GBP --date 2026-05-01",
    )
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="afficher aussi les messages de suivi détaillés")

    # Options communes à toutes les sous-commandes (parser « parent »)
    communs = argparse.ArgumentParser(add_help=False)
    communs.add_argument("--devises", nargs="+", type=str.upper, default=DEVISES_PAR_DEFAUT,
                         metavar="DEVISE",
                         help=f"codes des devises (défaut : {' '.join(DEVISES_PAR_DEFAUT)})")
    communs.add_argument("--debut", type=lire_date, default=lire_date(DEBUT_PAR_DEFAUT),
                         help=f"date de début AAAA-MM-JJ (défaut : {DEBUT_PAR_DEFAUT})")
    communs.add_argument("--fin", type=lire_date, default=lire_date(FIN_PAR_DEFAUT),
                         help=f"date de fin AAAA-MM-JJ (défaut : {FIN_PAR_DEFAUT})")

    sous_commandes = parser.add_subparsers(dest="commande", metavar="COMMANDE",
                                           title="sous-commandes")

    p_extraire = sous_commandes.add_parser(
        "extraire", parents=[communs],
        help="télécharger les taux depuis l'API (cache/ et donnees/)")
    p_extraire.set_defaults(fonction=commande_extraire)

    p_analyser = sous_commandes.add_parser(
        "analyser", parents=[communs],
        help="afficher les statistiques de chaque devise")
    p_analyser.add_argument("--date", type=lire_date,
                            help="afficher aussi le taux à cette date (AAAA-MM-JJ)")
    p_analyser.add_argument("--export", action="store_true",
                            help="enregistrer le résumé dans donnees/resume_analyse.csv")
    p_analyser.set_defaults(fonction=commande_analyser)

    p_graphiques = sous_commandes.add_parser(
        "graphiques", parents=[communs],
        help="créer les graphiques PNG dans graphiques/")
    p_graphiques.set_defaults(fonction=commande_graphiques)

    return parser


def configurer_logging(verbose):
    """Écrit le suivi dans taux.log ; l'affiche aussi à l'écran avec --verbose.

    Paramètre :
        verbose (bool) : True pour afficher les messages INFO dans le terminal.
    """
    console = logging.StreamHandler()
    console.setLevel(logging.INFO if verbose else logging.ERROR)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[logging.FileHandler(FICHIER_LOG, encoding="utf-8"), console],
    )


def main(arguments=None):
    """Point d'entrée : lit la ligne de commande et lance la bonne sous-commande.

    Paramètre :
        arguments (list de str) : les arguments (None = ceux du terminal).
    Renvoie :
        int : le code de sortie du programme.
    """
    parser = creer_parser()
    args = parser.parse_args(arguments)

    if args.commande is None:          # aucune sous-commande : on affiche l'aide
        parser.print_help()
        return 0
    if args.debut > args.fin:
        parser.error("la date de début doit être avant la date de fin")

    configurer_logging(args.verbose)
    logging.getLogger(__name__).info("Commande : %s", " ".join(sys.argv[1:]))
    return args.fonction(args)


# Ce bloc ne s'exécute que si on lance « python taux_cli.py ... »,
# pas si un autre fichier fait « import taux_cli ».
if __name__ == "__main__":
    sys.exit(main())
