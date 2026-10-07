## Sommaire

- [Partie A — Python plus idiomatique](#partie-a--python-plus-idiomatique)
- [Partie B — La programmation orientée objet](#partie-b--la-programmation-orientée-objet-les-classes)
- [Partie C — Visualiser avec matplotlib](#partie-c--visualiser-avec-matplotlib)
- [Partie D — Assembler et finaliser](#partie-d--assembler-et-finaliser)

---

## Partie A — Python plus idiomatique

*Fichier : `idiomatique.py`*

### 1. C'est quoi une compréhension de liste ? Quel avantage par rapport à une boucle `for` classique ?

Une **compréhension de liste** construit une nouvelle liste **en une seule ligne**, en décrivant ce qu'on veut obtenir pour chaque élément :

```python
# Boucle for classique (séance 2) : 3 lignes
variations = []
for i in range(1, len(taux)):
    variations.append((taux[i] / taux[i - 1] - 1) * 100)

# Compréhension de liste : 1 ligne
variations = [(taux[i] / taux[i - 1] - 1) * 100 for i in range(1, len(taux))]
```

On peut ajouter une condition pour filtrer : `[v for v in variations if v > 0]` ne garde que les hausses. Le même principe existe pour les dictionnaires : `{d: t for d, t in zip(dates, taux)}`.

**Avantages par rapport à une boucle `for` :**

- **Plus court et plus lisible :** on voit d'un coup d'œil qu'on fabrique une liste et à partir de quoi.
- **Pas de liste vide à créer ni d'`append`**, donc moins de risques d'erreur (oublier l'`append`, se tromper de liste).
- **Un peu plus rapide :** Python l'optimise en interne.

**La limite :** si la logique devient compliquée (plusieurs conditions, plusieurs étapes), une boucle `for` classique redevient plus lisible.

### 2. À quoi servent `enumerate` et `zip` ?

- **`enumerate`** donne, à chaque tour de boucle, **l'indice et la valeur** en même temps. On évite ainsi l'écriture lourde `for i in range(len(taux)): ... taux[i]`.

  ```python
  for i, t in enumerate(taux, start=1):   # start=1 : on commence à compter à 1
      print(f"Jour n°{i} : {t}")
  ```

- **`zip`** **associe plusieurs listes élément par élément** : le 1er avec le 1er, le 2e avec le 2e, etc. C'est idéal pour parcourir les dates et les taux ensemble.

  ```python
  for d, t in zip(dates, taux):
      print(f"{d} → {t}")
  ```

  `zip` s'arrête à la fin de la liste la plus courte. Et `zip(*couples)` fait l'inverse : il « défait » une liste de couples en deux listes.

### 3. Comment trier une liste selon un critère (`sorted` avec `key`) ?

`sorted(liste, key=fonction)` trie la liste selon la valeur que renvoie `fonction` pour chaque élément. Sans `key`, Python trie selon les éléments eux-mêmes. Avec `key`, on choisit **le critère du tri**.

```python
couples = list(zip(dates, taux))   # [(date, taux), ...]

# Trier selon le taux (2e élément du couple), du plus haut au plus bas
les_plus_hauts = sorted(couples, key=lambda couple: couple[1], reverse=True)[:5]

# Trier selon la taille de la variation, qu'elle soit positive ou négative
plus_fortes = sorted(jours_variation, key=lambda dv: abs(dv[1]), reverse=True)
```

- `reverse=True` trie dans l'ordre **décroissant**.
- `sorted` renvoie une **nouvelle liste** et ne modifie pas l'originale. À l'inverse, `liste.sort()` modifie la liste elle-même.
- `min` et `max` acceptent aussi `key=` : `min(couples, key=lambda c: c[1])` donne directement le couple du taux le plus bas, et remplace toute la fonction `trouver_min_max` de la séance 2.

### 4. C'est quoi une f-string ? Comment afficher un nombre à deux décimales ?

Une **f-string** est une chaîne de caractères précédée d'un **`f`**, dans laquelle on peut glisser des variables ou des calculs entre accolades `{}`. Python les remplace par leur valeur.

```python
# Avant : concaténation, avec str() partout
"Taux : " + str(t) + " " + devise

# Avec une f-string
f"Taux : {t} {devise}"
```

**Pour afficher un nombre à deux décimales**, on ajoute un format après deux-points : **`{taux:.2f}`** (`.2` pour deux chiffres après la virgule, `f` pour un nombre décimal).

| Format | Exemple | Résultat |
|---|---|---|
| `{x:.2f}` | deux décimales | `1.18` |
| `{x:+.2f}` | avec le signe + ou − | `+2.79` |
| `{x:.1%}` | en pourcentage | `1.4%` pour 0.0136 |
| `{x:,.2f}` | séparateur des milliers | `1,234,567.80` |
| `{d:%d/%m/%Y}` | une date | `02/01/2026` |

### 5. C'est quoi une fonction `lambda` ?

Une **`lambda`** est une **petite fonction anonyme** (sans nom), écrite **en une seule ligne**, qui renvoie directement le résultat d'une expression.

```python
# Fonction classique
def en_pourcentage(x):
    return (x - 1) * 100

# La même chose en lambda
lambda x: (x - 1) * 100
```

On l'utilise quand on a besoin d'une fonction **courte et utilisée une seule fois**, surtout comme argument d'une autre fonction :

- `sorted(couples, key=lambda c: c[1])` pour donner le critère de tri ;
- `map(lambda x: round(x, 2), taux)` pour appliquer un calcul à chaque élément ;
- `filter(lambda x: x > 1.18, taux)` pour garder les éléments qui vérifient une condition.

**Limites :** une lambda ne contient qu'**une seule expression** (pas de `if` sur plusieurs lignes, pas de boucle) et n'a pas de docstring. Dès que c'est plus compliqué, on écrit une vraie fonction avec `def`. Et en Python, une compréhension est souvent plus lisible que `map` ou `filter` avec une lambda : `[round(x, 2) for x in taux]`.

---

## Partie B — La programmation orientée objet (les classes)

*Fichier : `serie_taux.py`*

### 1. C'est quoi une classe ? Un objet ? Une instance ? À quoi sert `self` ?

- Une **classe** est un **modèle** (un « moule ») qui décrit un type de chose : quelles **données** elle contient (les **attributs**) et ce qu'elle sait faire (les **méthodes**). Notre classe `SerieTaux` décrit ce qu'est une série de taux : une devise, des dates, des taux, et des méthodes `moyenne()`, `variation()`, `taux_a(date)`…
- Un **objet** est une chose **concrète fabriquée à partir de ce modèle**, avec ses propres valeurs.
- **Instance** est un synonyme d'objet. On dit qu'un objet est une *instance de* sa classe. `usd = SerieTaux("USD", couples_usd)` et `gbp = SerieTaux("GBP", couples_gbp)` sont deux instances de la même classe `SerieTaux`.

**`self`** désigne **l'objet sur lequel on est en train de travailler**. C'est le premier paramètre de chaque méthode. Quand on écrit `usd.moyenne()`, Python appelle en fait `SerieTaux.moyenne(usd)` : `self` vaut alors `usd`. C'est grâce à `self` que la méthode sait **quels taux utiliser**, ceux de l'USD ou ceux du GBP.

```python
class SerieTaux:
    def moyenne(self):
        return sum(self.taux) / len(self.taux)   # les taux de CET objet
```

### 2. À quoi sert `__init__` ?

`__init__` est la méthode **appelée automatiquement à la création d'un objet**, quand on écrit `SerieTaux(...)`. Elle sert à **initialiser** l'objet, c'est-à-dire lui donner ses **attributs de départ**.

```python
class SerieTaux:
    def __init__(self, devise, couples):
        self.devise = devise                     # attributs d'instance
        self.dates = [d for d, _ in sorted(couples)]
        self.taux = [t for _, t in sorted(couples)]

usd = SerieTaux("USD", couples)   # __init__ est appelée ici, toute seule
```

On y fait aussi les vérifications de départ. Dans notre classe, `__init__` refuse une série vide avec `raise ValueError`, et trie les données par date une bonne fois pour toutes.

### 3. Différence entre un attribut de classe et un attribut d'instance ?

| | Attribut de **classe** | Attribut d'**instance** |
|---|---|---|
| **Où on le définit** | Directement dans la classe, hors de toute méthode | Dans `__init__` (ou une méthode), avec `self.` |
| **À qui il appartient** | **Partagé** par tous les objets de la classe | **Propre à chaque objet** |
| **Exemple dans `SerieTaux`** | `base = "EUR"`, `source = "BCE"`, le compteur `nb_series` | `self.devise`, `self.dates`, `self.taux` |

Modifier un attribut de classe (`SerieTaux.source = "BCE"`) change la valeur **pour tous les objets**. À l'inverse, chaque série a ses propres `taux`.

**⚠️ Le piège de la liste mutable :** si on déclare une **liste** en attribut de classe (`historique = []`), il n'existe **qu'une seule liste**, partagée par tous les objets. Ajouter une note à l'USD la fait donc aussi apparaître dans le GBP. C'est le même piège qu'en séance 1 : deux noms qui pointent vers le même objet. **La solution :** créer la liste dans `__init__` (`self.historique = []`), pour que chaque objet ait la sienne. `serie_taux.py` montre les deux versions.

### 4. Qu'apporte une `dataclass` par rapport à une classe écrite entièrement à la main ?

Le décorateur **`@dataclass`** fait écrire **automatiquement par Python** les méthodes répétitives, à partir de la simple liste des attributs :

```python
from dataclasses import dataclass, field

@dataclass
class SerieTauxDC:
    devise: str
    dates: list = field(default_factory=list)
    taux: list = field(default_factory=list)
    base: str = "EUR"
```

Ce qu'elle apporte :

- **`__init__` est généré tout seul :** plus besoin d'écrire `self.devise = devise` pour chaque attribut.
- **`__repr__` est généré :** `print(serie)` affiche lisiblement tous les attributs, au lieu de `<SerieTauxDC object at 0x...>`.
- **`__eq__` est généré :** deux objets avec les mêmes valeurs sont égaux (`==` renvoie `True`), alors qu'avec une classe normale, `==` compare seulement si c'est le même objet en mémoire.
- **Les attributs et leurs types sont lisibles d'un coup d'œil**, en haut de la classe.
- **`field(default_factory=list)` évite le piège de la liste mutable :** chaque objet reçoit une nouvelle liste vide.

👉 Une dataclass est idéale pour une classe qui sert surtout à **regrouper des données**. On peut toujours y ajouter ses propres méthodes (`moyenne()`, `variation()`…).

---

## Partie C — Visualiser avec matplotlib

*Fichier : `graphiques.py` — images dans `graphiques/`*

### 1. Différence entre la figure et les axes ? Pourquoi préférer `fig, ax = plt.subplots()` ?

- La **figure** (`fig`) est **l'image entière**, la « feuille » : sa taille, son titre général, le fichier qu'on enregistre.
- Les **axes** (`ax`) sont **un graphique** placé sur cette feuille : la zone où l'on trace, avec son axe x, son axe y, son titre, sa légende. Une figure peut contenir **plusieurs axes** : notre `4_tableau_de_bord.png` en contient 4.

```python
fig, ax = plt.subplots()             # une figure avec un graphique
fig, axes = plt.subplots(2, 2)       # une figure avec 4 graphiques (2 lignes × 2 colonnes)
```

**Pourquoi `fig, ax = plt.subplots()` plutôt que `plt.plot(...)` directement ?**

- **On sait exactement sur quoi on dessine.** `plt.plot()` dessine sur « le graphique actif », un état caché qui change selon ce qu'on a fait avant. Avec plusieurs graphiques, on risque de dessiner au mauvais endroit.
- **C'est indispensable pour plusieurs graphiques côte à côte :** `axes[0][1].plot(...)` vise précisément le graphique en haut à droite.
- **C'est plus clair dans des fonctions :** on peut passer `ax` en paramètre à une fonction, comme `mettre_en_forme_axe_dates(ax)` dans notre code.
- **On peut fermer la figure proprement** avec `plt.close(fig)` une fois enregistrée, ce qui libère la mémoire.

### 2. Quel type de graphique pour quel type de donnée ?

| Type de donnée | Graphique adapté | Pourquoi | Dans notre projet |
|---|---|---|---|
| **Série temporelle** (une valeur qui évolue dans le temps) | **Courbe** (`ax.plot`) | La ligne relie les dates dans l'ordre et montre la **tendance** | `1_courbe_USD.png` : évolution du taux |
| **Distribution** (comment se répartissent les valeurs) | **Histogramme** (`ax.hist`) | Il compte combien de valeurs tombent dans chaque intervalle et montre la **forme** de la répartition | `3_histogramme_*.png` : répartition des variations quotidiennes |
| **Comparaison** de plusieurs séries dans le temps | **Plusieurs courbes** sur un même graphique, ramenées à une **base commune** | On compare les évolutions | `2_comparaison_devises.png` : USD et GBP en base 100 |
| **Comparaison** entre catégories | **Diagramme en barres** (`ax.bar`) | On compare des quantités entre catégories | Par exemple, la moyenne de chaque mois |
| **Relation** entre deux variables | **Nuage de points** (`ax.scatter`) | On voit si les deux variables évoluent ensemble | Par exemple, le taux USD en fonction du taux GBP |

Pour comparer nos deux devises, on a utilisé la **base 100**. L'USD (environ 1,17) et le GBP (environ 0,86) n'ont pas le même niveau, donc on ramène les deux à 100 le premier jour pour comparer leurs **évolutions en %** sur la même échelle.

### 3. Comment sauvegarder une figure en PNG ?

Avec la méthode **`savefig`** de la figure, en donnant un nom de fichier qui finit par `.png` :

```python
fig, ax = plt.subplots()
ax.plot(dates, taux)
ax.set_title("Évolution du taux EUR/USD")
ax.set_xlabel("Date")
ax.set_ylabel("Taux")

fig.savefig("graphiques/courbe_USD.png", dpi=150, bbox_inches="tight")
plt.close(fig)
```

- `dpi=150` règle la **résolution** (le nombre de points par pouce) : plus il est grand, plus l'image est nette et lourde.
- `bbox_inches="tight"` **rogne les marges blanches** inutiles autour du graphique.
- `plt.close(fig)` ferme la figure une fois enregistrée, pour **libérer la mémoire**.
- Il faut appeler `savefig` **avant** `plt.show()`, car `show` peut vider la figure.
- Le format est déduit de l'extension : `.png`, `.pdf`, `.svg`…

---

## Partie D — Assembler et finaliser

*Fichiers : `taux_cli.py` et le package `src/` — `README.md` et `requirements.txt` à la racine*

### 1. À quoi sert `argparse` ? Pourquoi une ligne de commande plutôt que des `input()` ?

**`argparse`** est le module de la bibliothèque standard qui **lit les arguments tapés après le nom du script** dans le terminal :

```
python taux_cli.py analyser --devises USD GBP --date 2026-05-01
```

Il découpe cette ligne, vérifie que les valeurs sont correctes, convertit les types (ici le texte `2026-05-01` en vraie date), et **génère automatiquement l'aide** (`--help`) ainsi que des messages d'erreur clairs. Avec les **sous-commandes** (`extraire`, `analyser`, `graphiques`), on regroupe tous nos scripts derrière **une seule commande**.

**Pourquoi une ligne de commande plutôt que des `input()` ?**

- **On peut l'automatiser :** une commande peut être lancée par un autre programme ou un script, ou programmée tous les matins. Avec `input()`, il faut quelqu'un devant l'écran pour répondre.
- **C'est reproductible :** on peut noter la commande exacte dans le README et la relancer à l'identique. Avec `input()`, on doit retaper les réponses à chaque fois, avec un risque d'erreur.
- **C'est plus rapide :** on donne tout en une ligne, et on peut rappeler la commande précédente avec la flèche ↑.
- **L'aide et les vérifications sont gratuites :** `--help` décrit toutes les options, et une date invalide est refusée avec un message clair, sans code à écrire.
- **On a des valeurs par défaut :** `python taux_cli.py analyser` marche sans rien préciser.

### 2. Que fait exactement `if __name__ == "__main__":` ?

Chaque fichier Python possède une variable spéciale **`__name__`**, que Python remplit automatiquement :

- si on **lance le fichier directement** (`python taux_cli.py`), `__name__` vaut **`"__main__"` ;**
- si le fichier est **importé** par un autre (`import graphiques`), `__name__` vaut **le nom du module** (`"graphiques"`).

Donc `if __name__ == "__main__":` signifie : **« exécute ce bloc seulement si on a lancé ce fichier directement, pas si on l'importe »**.

```python
def main():
    ...

if __name__ == "__main__":
    main()
```

**Pourquoi c'est important :** `taux_cli.py` importe `graphiques.py` et `serie_taux.py` pour **réutiliser leurs fonctions**. Sans cette protection, le simple fait d'importer `graphiques` relancerait tout son programme principal et recréerait tous les graphiques. Grâce à elle, un même fichier peut servir **à la fois de script et de module réutilisable**.

### 3. C'est quoi un module ? Un package ?

- Un **module** est **un fichier `.py`** dont on peut importer le contenu (fonctions, classes, variables) dans un autre fichier. `serie_taux.py` est un module : `taux_cli.py` y récupère `SerieTaux` avec `from serie_taux import SerieTaux`. Les modules de la bibliothèque standard (`json`, `csv`, `argparse`…) sont aussi des modules.
- Un **package** est **un dossier qui regroupe plusieurs modules**, avec un fichier **`__init__.py`** qui indique à Python que ce dossier est un package. Notre dossier `src/` est un package :

  ```
  src/
  ├── __init__.py        ← fait de src/ un package
  ├── extraction.py      ← module : récupérer les taux
  └── statistiques.py    ← module : calculer les statistiques
  ```

  On importe alors avec le nom du package devant : `from src.statistiques import afficher_resume`. Ce préfixe évite aussi les conflits de noms : un fichier `statistiques.py` dans un autre dossier ne serait pas confondu avec celui de `src/`. pandas, numpy et matplotlib sont eux aussi des packages, juste beaucoup plus gros.

**L'intérêt :** chaque fichier a **un seul rôle**, le code est plus facile à lire, à tester et à réutiliser, et on sait où chercher quand il y a un problème.

### 4. Que doit contenir un bon `README` ? À quoi servent `requirements.txt` et `.gitignore` ?

**Un bon `README.md`** est la **page d'accueil du projet** : la première chose qu'on lit sur GitHub. Il doit permettre à quelqu'un qui ne connaît pas le projet de le comprendre et de le lancer sans aide. Il contient :

- le **titre** et une **description** en quelques lignes (ce que fait le projet, d'où viennent les données) ;
- les **auteurs**, c'est-à-dire les noms du groupe ;
- l'**installation** : la version de Python et `pip install -r requirements.txt` ;
- l'**utilisation**, avec des **exemples de commandes** prêtes à copier (`python taux_cli.py analyser --date 2026-05-01`) ;
- l'**organisation du dépôt** : quel dossier contient quoi ;
- éventuellement un aperçu des **résultats** (un graphique) et les limites connues.

**`requirements.txt`** liste les **librairies tierces** nécessaires au projet, **avec leurs versions** (`pandas==3.0.6`). Quelqu'un qui récupère le projet installe tout d'un coup avec `pip install -r requirements.txt`, **dans les mêmes versions** que nous. On évite ainsi le fameux « ça marche chez moi mais pas chez toi », dû à une version différente. On dit qu'on « fige » les versions.

**`.gitignore`** liste les **fichiers et dossiers que Git doit ignorer**, c'est-à-dire ne jamais mettre dans le dépôt :

- l'**environnement virtuel** (`.venv/`), très lourd et propre à chaque ordinateur : on le recrée avec `requirements.txt` ;
- les **fichiers générés automatiquement** par Python (`__pycache__/`, `*.pyc`) ;
- souvent les **fichiers de log** (`*.log`), qui changent à chaque exécution. Dans notre projet, on garde quand même `appel_api.log`, car c'est un livrable de la séance 2 ;
- les **fichiers personnels ou secrets** (mots de passe, clés d'API, réglages de l'éditeur).

Le dépôt reste ainsi **propre et léger**, et ne contient que ce qui est utile pour comprendre et relancer le projet.
