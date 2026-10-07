# Analyse des taux de change EUR/USD et EUR/GBP

Projet Python réalisé en groupe — BFA, Université Paris Dauphine, 2026-2027
Enseignante : Rahma Gargouri

## Auteurs

- Ellyn Ordonneau-Moliton
- Victor Vauthier
- Anna Toubert

## Description

Ce projet récupère les **taux de change de référence de la BCE** (Banque centrale européenne) grâce à l'API gratuite [Frankfurter](https://frankfurter.dev), puis les nettoie, les analyse et les représente en graphiques.

Nous étudions deux devises par rapport à l'euro, le **dollar américain (USD)** et la **livre sterling (GBP)**, sur la période du **1er janvier au 1er septembre 2026**.

Le projet a été construit en quatre séances, chacune ajoutant une étape :

| Séance | Thème | Ce qui a été fait |
|---|---|---|
| 1 | Bases de Python | Types, opérations, conditions, boucles ; premier appel à l'API, cache JSON et CSV |
| 2 | Fonctions et robustesse | Fonctions, gestion des erreurs (`try/except`), journalisation (`logging`), récursivité et complexité |
| 3 | pandas, jointures, numpy | Nettoyage (*forward-fill*), moyenne mobile, `resample`, jointure des deux devises, numpy et polars |
| 4 | Finalisation | Code idiomatique, classe `SerieTaux`, graphiques matplotlib, outil en ligne de commande |

## Installation

Il faut **Python 3.10 ou plus récent** (le projet a été développé avec Python 3.14).

1. Récupérer le dépôt :

   ```
   git clone <adresse-du-dépôt>
   cd "NOUVEAU REPOSITORY"
   ```

2. *(Conseillé)* Créer et activer un environnement virtuel :

   ```
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   source .venv/bin/activate       # macOS / Linux
   ```

3. Installer les librairies nécessaires (pandas, numpy, polars, matplotlib) :

   ```
   pip install -r requirements.txt
   ```

Une connexion internet est nécessaire pour télécharger les taux. Les réponses de l'API sont ensuite gardées dans les dossiers `cache/`, ce qui permet de relancer les analyses sans internet.

## Utilisation

### L'outil en ligne de commande (séance 4)

L'ensemble du projet se pilote avec une commande unique, `taux_cli.py`, qui propose trois sous-commandes :

```
cd "SEANCE 4"

python taux_cli.py extraire                       # télécharger les taux (cache/ et donnees/)
python taux_cli.py analyser                       # tableau des statistiques de chaque devise
python taux_cli.py graphiques                     # créer les graphiques PNG dans graphiques/
```

Chaque sous-commande accepte des options :

```
python taux_cli.py analyser --devises USD GBP JPY                   # choisir les devises
python taux_cli.py analyser --debut 2026-03-01 --fin 2026-06-30     # choisir la période
python taux_cli.py analyser --date 2026-05-01                       # taux à une date précise
python taux_cli.py analyser --export                                # résumé enregistré en CSV
python taux_cli.py -v extraire                                      # afficher le suivi détaillé
```

L'aide complète s'affiche avec :

```
python taux_cli.py --help
python taux_cli.py analyser --help
```

### Les scripts de chaque séance

Chaque script se lance depuis le dossier de sa séance, par exemple `python analyse.py` dans `SEANCE 3`. Les scripts retrouvent tout seuls les données produites aux séances précédentes.

| Séance | Script | Rôle |
|---|---|---|
| 1 | `hello_world.py` | Premier programme |
| 1 | `bases_python.py` | Types, opérations, conditions et boucles |
| 1 | `appel_api.py` | Taux du jour et série 2026 : cache JSON + CSV |
| 2 | `fonctions.py` | Lecture du CSV, moyenne, min/max, comparaison avec `statistics.mean` |
| 2 | `appel_api_protege.py` | Appel à l'API protégé par `try/except` et journalisé (`appel_api.log`) |
| 2 | `recursivite.py` | Factorielle, somme récursive, trois versions de Fibonacci chronométrées |
| 3 | `analyse.py` | pandas : inspection, filtres, *forward-fill*, variation, moyenne mobile, `resample` |
| 3 | `jointures.py` | Jointure USD + GBP, les quatre types de jointure, `merge` / `join` / `concat` |
| 3 | `numpy_polars.py` | Calculs vectorisés numpy, `dtype`, *broadcasting*, comparaison pandas / polars |
| 4 | `idiomatique.py` | Compréhensions, `enumerate`, `zip`, `sorted`, f-strings, `lambda`, `map` / `filter` |
| 4 | `serie_taux.py` | La classe `SerieTaux`, attributs de classe et d'instance, `dataclass` |
| 4 | `graphiques.py` | Les graphiques matplotlib, enregistrés en PNG |
| 4 | `taux_cli.py` | L'outil en ligne de commande (`argparse`) |

## Organisation du dépôt

```
NOUVEAU REPOSITORY/
├── README.md               ← ce fichier
├── requirements.txt        ← librairies à installer, versions figées
├── SEANCE 1/               ← bases de Python et premier appel à l'API
├── SEANCE 2/               ← fonctions, erreurs, logging, récursivité
├── SEANCE 3/               ← pandas, jointures, numpy et polars
└── SEANCE 4/               ← version finale du projet
    ├── taux_cli.py         ← point d'entrée : la ligne de commande
    ├── src/                ← package du projet
    │   ├── __init__.py
    │   ├── extraction.py   ← récupérer les taux (API, cache, CSV)
    │   └── statistiques.py ← calculer les indicateurs
    ├── serie_taux.py       ← la classe SerieTaux
    ├── graphiques.py       ← les graphiques matplotlib
    ├── idiomatique.py
    └── graphiques/         ← les images PNG produites
```

Chaque dossier de séance contient aussi :

- `cache/` : les réponses brutes de l'API, au format JSON ;
- `donnees/` : les taux au format CSV (une ligne par date) ;
- `docs/notes_seanceN.md` : nos réponses aux questions de la séance.

## Résultats

![Comparaison EUR/USD et EUR/GBP en base 100](SEANCE%204/graphiques/2_comparaison_devises.png)

- Sur la période, la BCE a publié des taux sur **171 jours ouvrés**. Les jours fériés sans publication (1er janvier, Vendredi saint, lundi de Pâques, 1er mai) sont comblés par *forward-fill*, en reprenant le dernier taux connu.
- Le taux EUR/USD moyen est de **1,1624** (moyenne identique avec nos fonctions de la séance 2, `statistics.mean`, pandas et polars).
- Pour Fibonacci, la version récursive naïve devient inutilisable très vite (plus d'1 seconde dès n = 30), alors que les versions mémoïsée et itérative restent instantanées.
- numpy est environ **30 fois plus rapide** qu'une boucle Python, et polars **3 à 7 fois plus rapide** que pandas sur 2 millions de lignes.

Le détail des analyses et nos réponses aux questions se trouvent dans les fichiers `docs/notes_seanceN.md` de chaque séance.

## Source des données

Taux de change de référence publiés par la **Banque centrale européenne**, récupérés via l'API [Frankfurter](https://frankfurter.dev) (gratuite, sans clé). Les taux sont exprimés en **base euro** : `1 EUR = x USD`. Ils ne sont publiés que les **jours ouvrés**, ni les week-ends ni les jours fériés.
