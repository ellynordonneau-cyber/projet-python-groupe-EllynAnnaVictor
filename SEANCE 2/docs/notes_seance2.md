## Sommaire

- [Partie A — Les fonctions](#partie-a--les-fonctions)
- [Partie B — Gérer les erreurs et journaliser](#partie-b--gérer-les-erreurs-tryexcept-et-journaliser-logging)
- [Partie C — Récursivité et complexité](#partie-c--récursivité-et-complexité)
- [Tableau des mesures — Fibonacci](#tableau-des-mesures--fibonacci)

---

## Partie A — Les fonctions

### 1. Pourquoi découper le code en fonctions ? Trois bénéfices concrets

| Bénéfice | Concrètement dans notre projet |
|---|---|
| **Réutilisation** | La fonction `calculer_moyenne(taux)` s'écrit une seule fois et sert pour l'USD, le GBP ou n'importe quelle période, sans copier-coller. |
| **Lisibilité** | Le programme principal se lit comme une phrase : `lire_csv()` → `calculer_moyenne()` → `min_max()`. On comprend ce que fait le code sans lire chaque ligne. |
| **Tests et corrections plus faciles** | Si la moyenne est fausse, on sait qu'il faut regarder **une seule** fonction. On peut aussi la tester à part avec une petite liste connue, par exemple `[1, 2, 3]` → `2`. |

### 2. Paramètre ou valeur de retour ? Que renvoie une fonction sans `return` ?

- Le **paramètre** est ce qui **entre** dans la fonction : la donnée qu'on lui fournit pour travailler.
- La **valeur de retour** (`return`) est ce qui **sort** de la fonction : le résultat qu'elle renvoie à celui qui l'a appelée.

```python
def calculer_moyenne(liste_taux):       # liste_taux = paramètre (entrée)
    return sum(liste_taux) / len(liste_taux)   # résultat renvoyé (sortie)

moyenne = calculer_moyenne([1.17, 1.16, 1.18])  # moyenne reçoit le résultat
```

Une fonction **sans `return`** renvoie automatiquement **`None`** (« rien »). Elle peut faire quelque chose, comme afficher avec `print`, mais on ne peut pas récupérer de résultat dans une variable.

### 3. Qu'est-ce qu'une docstring et où la place-t-on ?

Une **docstring** est un texte entre triples guillemets `"""..."""` qui **décrit ce que fait la fonction** : son rôle, ses paramètres et ce qu'elle renvoie.

On la place **juste en dessous de la ligne `def`**, en première ligne du corps de la fonction :

```python
def calculer_moyenne(liste_taux):
    """Calcule la moyenne d'une liste de taux.

    Paramètre : liste_taux (list de float)
    Renvoie   : la moyenne (float)
    """
    return sum(liste_taux) / len(liste_taux)
```

Contrairement à un simple commentaire `#`, Python la garde en mémoire : `help(calculer_moyenne)` l'affiche, et VS Code la montre quand on survole la fonction.

### 4. Variable locale ou variable globale ?

| | Variable **locale** | Variable **globale** |
|---|---|---|
| **Où est-elle créée ?** | À l'intérieur d'une fonction | En dehors de toute fonction (dans le corps du fichier) |
| **Où est-elle visible ?** | Uniquement dans cette fonction | Partout dans le fichier |
| **Durée de vie** | Disparaît à la fin de la fonction | Existe tant que le programme tourne |

```python
DEVISE = "USD"            # globale : visible partout

def afficher_total(liste):
    total = sum(liste)    # locale : n'existe que dans la fonction
    print(DEVISE, total)  # on peut lire la globale

afficher_total([1, 2])
print(total)              # ❌ NameError : total n'existe plus ici
```

👉 **Bonne pratique :** limiter les variables globales. Mieux vaut passer les données en **paramètre** et les récupérer avec **`return`**, pour que chaque fonction reste indépendante.

---

## Partie B — Gérer les erreurs (try/except) et journaliser (logging)

### 1. Pourquoi `try/except` ? Que se passe-t-il sans ? À quoi servent `else` et `finally` ?

**Sans gestion d'erreur**, une exception (pas de connexion, erreur `403`, fichier introuvable…) **arrête brutalement le programme**. Python affiche alors un long message rouge (le *traceback*) et rien de ce qui suit n'est exécuté.

**Avec `try/except`**, on **intercepte** l'erreur pour réagir proprement : afficher un message clair, réessayer ou utiliser le cache.

| Bloc | Quand est-il exécuté ? |
|---|---|
| `try` | On **essaie** le code qui risque d'échouer. |
| `except` | **Seulement si une erreur** se produit dans le `try`. |
| `else` | **Seulement s'il n'y a pas eu d'erreur** : la suite normale. |
| `finally` | **Toujours**, erreur ou pas : nettoyage, fermeture, message de fin. |

```python
try:
    donnees = appeler_api(url)
except urllib.error.HTTPError as e:
    print(f"Le serveur a refusé la requête (code {e.code}).")
except urllib.error.URLError:
    print("Impossible de se connecter : vérifiez votre connexion internet.")
else:
    print("Données reçues :", donnees["date"])
finally:
    print("Fin de l'appel à l'API.")
```

### 2. Pourquoi un `except:` nu est-il déconseillé ?

Un `except:` sans type d'erreur attrape **absolument tout**, y compris ce qu'on ne voulait pas attraper :

- **Il cache les vrais bugs.** Une faute de frappe dans un nom de variable (`NameError`) est avalée silencieusement, et on ne comprend plus pourquoi le programme ne marche pas.
- **Il attrape même le Ctrl+C** (`KeyboardInterrupt`), ce qui empêche d'arrêter le programme.
- **On ne sait pas quoi faire.** Une coupure réseau et une réponse illisible ne se traitent pas de la même façon, mais un `except:` nu les met dans le même sac.

👉 Il faut **nommer l'erreur attendue** : `except urllib.error.URLError:`, `except json.JSONDecodeError:`, `except FileNotFoundError:`…

### 3. C'est quoi `logging` ? Pourquoi le préférer à `print` ? Les niveaux de log

`logging` est le module de la bibliothèque standard qui sert à **tenir un journal** de ce que fait le programme : chaque message est horodaté, a un niveau d'importance et peut être écrit dans un fichier `.log`.

**Pourquoi le préférer à `print` dans un vrai programme ?**

- **Les messages sont gardés** dans un fichier `.log` : on peut relire ce qui s'est passé hier soir, même si personne ne regardait l'écran.
- **Chaque ligne a la date et l'heure** : on sait quand l'erreur a eu lieu.
- **On filtre par importance** : en temps normal on n'affiche que les erreurs, et quand on cherche un bug on affiche tout. Il suffit de changer une ligne, sans supprimer de `print`.
- Les messages de suivi restent **séparés** de ce qu'on affiche vraiment à l'utilisateur.

**Les niveaux de log**, du moins grave au plus grave :

| Niveau | Usage | Exemple dans notre projet |
|---|---|---|
| `DEBUG` | Détails techniques pour chercher un bug | `"URL appelée : https://api.frankfurter.app/…"` |
| `INFO` | Déroulement normal | `"171 taux récupérés et enregistrés dans donnees/"` |
| `WARNING` | Situation suspecte, mais le programme continue | `"Aucun taux pour le 2026-01-01 (jour férié)"` |
| `ERROR` | Une opération a échoué | `"Échec de l'appel à l'API : 403 Forbidden"` |
| `CRITICAL` | Erreur grave, le programme ne peut plus continuer | `"Ni API ni cache disponibles : arrêt du programme"` |

```python
import logging

logging.basicConfig(
    filename="appel_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("Début de l'appel à l'API")
logging.warning("Réponse vide pour cette date")
logging.error("Pas de connexion internet")
```

---

## Partie C — Récursivité et complexité

### 1. C'est quoi la récursivité ? Cas de base et cas récursif. Et sans cas de base ?

Une fonction est **récursive** quand elle **s'appelle elle-même** pour résoudre un problème plus petit du même type.

- **Cas de base :** la situation simple où l'on connaît directement la réponse. C'est lui qui **arrête** la récursion.
- **Cas récursif :** la fonction s'appelle elle-même avec un problème **plus petit**, qui se rapproche du cas de base.

```python
def factorielle(n):
    if n == 0:                        # cas de base : 0! = 1
        return 1
    return n * factorielle(n - 1)     # cas récursif : n! = n × (n-1)!

# factorielle(3) = 3 × factorielle(2) = 3 × 2 × factorielle(1) = 3 × 2 × 1 × 1 = 6
```

**Sans cas de base**, la fonction s'appelle à l'infini. Chaque appel prend de la mémoire, et Python finit par s'arrêter avec une **`RecursionError: maximum recursion depth exceeded`**.

### 2. Pourquoi utiliser la récursivité ? Est-ce toujours le meilleur choix ?

**Pourquoi l'utiliser ?** Certains problèmes sont **naturellement définis à partir d'eux-mêmes** : la factorielle, les arbres (dossiers et sous-dossiers), les structures imbriquées comme un JSON dans un JSON. Le code récursif est alors **court, élégant et proche de la définition mathématique**.

**Ce n'est pas toujours le meilleur choix.** Contre-exemple précis : **Fibonacci naïf**.

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

Pour calculer `fib(5)`, la fonction calcule `fib(3)` **deux fois**, `fib(2)` **trois fois**, etc. Le nombre d'appels **double presque à chaque fois que n augmente de 1** : c'est une complexité en **O(2ⁿ)**.

- `fib(30)` fait déjà environ **1,6 million d'appels**.
- `fib(40)` en fait plus de **300 millions** et prend plusieurs dizaines de secondes.

Une simple **boucle `for`** calcule `fib(40)` en 40 étapes, de façon quasi instantanée. De plus, en Python, une récursion trop profonde (environ 1000 appels) provoque une `RecursionError`, ce qui n'arrive jamais avec une boucle.

### 3. Complexité temporelle et spatiale. Que signifient O(n), O(n²), O(2ⁿ) ?

- **Complexité temporelle :** comment le **nombre d'opérations** (donc le temps) augmente quand la taille de l'entrée *n* grandit.
- **Complexité spatiale :** comment la **mémoire supplémentaire** utilisée augmente avec *n* (variables, listes créées, profondeur des appels récursifs, cache de mémoïsation…).

La notation **O(…)** (« grand O ») donne l'**ordre de grandeur** de cette croissance :

| Notation | Nom | Exemple | Si *n* est multiplié par 2… |
|---|---|---|---|
| **O(n)** | Linéaire | Une boucle simple : parcourir la liste des 171 taux pour faire la somme | … le temps **double** |
| **O(n²)** | Quadratique | Deux boucles imbriquées : comparer chaque taux à tous les autres | … le temps est **multiplié par 4** |
| **O(2ⁿ)** | Exponentielle | Fibonacci récursif naïf | … le temps **explose** : avec seulement *n* + 1, il double déjà |

👉 O(2ⁿ) devient inutilisable très vite, même sur un ordinateur puissant.

### 4. C'est quoi la mémoïsation ? Que fait `functools.lru_cache` ? Pourquoi Python limite-t-il la profondeur de récursion ?

**La mémoïsation** consiste à **mémoriser les résultats déjà calculés** pour ne pas les recalculer. Quand la fonction est rappelée avec les mêmes arguments, on renvoie directement le résultat gardé en mémoire.

**`functools.lru_cache`** est un *décorateur* de la bibliothèque standard qui ajoute la mémoïsation à une fonction **en une seule ligne** :

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

Chaque `fib(k)` n'est plus calculé qu'**une seule fois** : on passe de **O(2ⁿ)** à **O(n)** en temps. En échange, on utilise un peu de **mémoire** pour stocker les résultats : complexité spatiale en O(n). *LRU* signifie *Least Recently Used* : si on fixe une taille maximale, ce sont les résultats utilisés le moins récemment qui sont effacés en premier.

**Pourquoi Python limite-t-il la profondeur de récursion ?** Chaque appel de fonction en cours occupe une place dans la **pile d'appels** (*call stack*), une zone de mémoire limitée. Sans limite, une récursion infinie ou trop profonde remplirait cette mémoire et ferait **planter tout le programme** brutalement. Python préfère donc s'arrêter proprement, vers **1000 appels** par défaut, avec une **`RecursionError`** que l'on peut lire et corriger.

---

## Tableau des mesures — Fibonacci

Mesures obtenues en lançant `recursivite.py` : temps mesuré avec `time.perf_counter`, mémoire avec `tracemalloc`. Les chiffres varient légèrement d'une exécution à l'autre et d'un ordinateur à l'autre.

### Évolution du temps quand n augmente

| n | fib(n) | Naïf | Appels (naïf) | Mémoïsé | Itératif |
|---|---|---|---|---|---|
| 5 | 5 | 13.2 µs | 15 | 13.3 µs | 2.8 µs |
| 10 | 55 | 142.0 µs | 177 | 16.1 µs | 2.4 µs |
| 15 | 610 | 818.9 µs | 1 973 | 21.2 µs | 2.2 µs |
| 20 | 6765 | 9.4 ms | 21 891 | 29.9 µs | 2.1 µs |
| 25 | 75025 | 152.6 ms | 242 785 | 51.2 µs | 3.9 µs |
| 30 | 832040 | **1.09 s** | **2 692 537** | 254.7 µs | 4.9 µs |

**Ce qu'on observe :**

- **Version naïve :** quand n augmente de 5, le nombre d'appels est multiplié par environ **11**, et le temps aussi. Passer de n = 25 à n = 30 fait passer de 0,15 s à plus d'**1 seconde**. C'est la croissance **exponentielle O(2ⁿ)** : à ce rythme, n = 40 prendrait plus de 2 minutes.
- **Version mémoïsée :** le temps reste de l'ordre de quelques dizaines de microsecondes. Chaque valeur n'est calculée qu'une seule fois : **O(n)**.
- **Version itérative :** c'est la plus rapide (quelques microsecondes), et son temps ne bouge presque pas : **O(n)** avec très peu d'opérations par étape.

### Comparaison des trois versions pour n = 25

| Version | Temps | Nombre d'appels | Profondeur max | Pic mémoire | Complexité temps | Complexité mémoire |
|---|---|---|---|---|---|---|
| Récursive naïve | 135.9 ms | 242 785 | 25 | 0 octets | O(2ⁿ) | O(n) |
| Récursive + lru_cache | 33.9 µs | 26 | 25 | 1 672 octets | O(n) | O(n) |
| Itérative (boucle) | 3.4 µs | 1 | 1 | 0 octets | O(n) | O(1) |

**Ce qu'on observe :**

- **Temps :** pour le même résultat, la version naïve est environ **4 000 fois plus lente** que la version mémoïsée et **40 000 fois plus lente** que la boucle. Elle fait 242 785 appels là où la mémoïsation n'en fait que 26 (un par valeur de 0 à 25).
- **Mémoire de la mémoïsation :** les **1 672 octets** correspondent au cache de `lru_cache`, qui garde en mémoire les 26 résultats déjà calculés. C'est le prix à payer pour gagner du temps : on échange de la mémoire contre de la vitesse.
- **Pourquoi « 0 octets » pour le naïf et l'itératif ?** `tracemalloc` ne compte que les objets Python créés en mémoire (listes, dictionnaires, caches…). Il ne voit pas la **pile d'appels**. Pour les versions récursives, c'est donc la colonne **profondeur max** qui montre la vraie mémoire utilisée : 25 appels empilés en même temps, soit O(n). La boucle, elle, n'empile rien (profondeur 1) et n'utilise que deux variables `a` et `b` : O(1).
- **Limite de profondeur :** avec n = 2000, la version mémoïsée provoque une `RecursionError` (limite de Python : 1000 appels imbriqués), alors que la version itérative calcule le résultat sans problème. C'est un argument de plus en faveur de la boucle quand la profondeur peut devenir grande.

**Conclusion :** la récursion naïve est la plus proche de la définition mathématique, mais elle est inutilisable dès n ≈ 35. La mémoïsation la rend rapide en utilisant un peu de mémoire. La version itérative est à la fois la plus rapide, la plus économe en mémoire et sans limite de profondeur : c'est la meilleure pour Fibonacci.
