## Sommaire

- [Comparatif avec la séance 2](#comparatif-avec-la-séance-2)
- [Partie A — Découvrir pandas](#partie-a--découvrir-pandas)
- [Partie B — Nettoyer, consolider et analyser](#partie-b--nettoyer-consolider-et-analyser)
- [Partie C — Les jointures](#partie-c--les-jointures)
- [Partie D — numpy et polars](#partie-d--numpy-et-polars)

---

## Comparatif avec la séance 2

En séance 2, tout était écrit « à la main » avec la bibliothèque standard (`csv`, boucles `for`). En séance 3, `pandas` fait la même chose en beaucoup moins de lignes.

| Tâche | Séance 2 — Python de base | Séance 3 — pandas |
|---|---|---|
| Lire le CSV | Fonction `lire_csv` : `open`, `csv.DictReader`, boucle, conversion `float()` à la main (≈ 8 lignes) | `pd.read_csv(chemin, parse_dates=["date"])` : 1 ligne, types reconnus automatiquement |
| Moyenne | Fonction `calculer_moyenne` avec une boucle | `df["taux"].mean()` |
| Minimum / maximum | Fonction `trouver_min_max` avec une boucle et deux comparaisons | `df["taux"].min()`, `.max()`, et `.idxmin()` / `.idxmax()` pour la date |
| Filtrer des lignes | Boucle `for` + `if` + `append` | `df[df["taux"] > 1.17]` |
| Combler les jours fériés | Très long à écrire (calendrier, boucle, mémoriser la dernière valeur) | `df.reindex(pd.bdate_range(...)).ffill()` |
| Moyenne mobile, moyenne par mois | Plusieurs boucles imbriquées | `.rolling(20).mean()` et `.resample("ME").mean()` |

**Résultats identiques :** sur nos 171 jours de taux EUR/USD, `analyse.py` retrouve exactement la même moyenne (1,162368), le même minimum et le même maximum que les fonctions de la séance 2. pandas ne change pas le résultat : il rend le code **plus court, plus lisible et plus rapide**.

Ce qu'on garde de la séance 2 : comprendre ce que fait une boucle permet de comprendre ce que pandas fait « derrière », et de vérifier ses résultats.

---

## Partie A — Découvrir pandas

### 1. Qu'est-ce qu'un `DataFrame` ? Une `Series` ?

- Un **`DataFrame`** est un **tableau à deux dimensions**, comme une feuille Excel : des lignes, des colonnes nommées, et un **index** qui identifie chaque ligne (chez nous, la date). Chaque colonne peut avoir son propre type.
- Une **`Series`** est **une seule colonne** : une suite de valeurs du même type, avec son index.

Un DataFrame est donc un ensemble de Series qui partagent le même index.

```python
df = pd.read_csv("taux.csv", parse_dates=["date"]).set_index("date")
type(df)           # DataFrame : tout le tableau
type(df["taux"])   # Series : une seule colonne
```

### 2. Pourquoi pandas plutôt que des boucles et le module `csv` ? Que signifie « vectorisation » ?

**Pourquoi pandas :**

- **Moins de code :** une ligne au lieu d'une fonction entière (voir le comparatif plus haut).
- **Moins d'erreurs :** pas de conversion de types à la main, pas d'indice qui déborde, et les valeurs manquantes sont gérées.
- **Beaucoup plus rapide** sur de gros volumes.
- **Des outils tout prêts** pour les dates, les regroupements, les jointures, les moyennes mobiles…

**La vectorisation**, c'est appliquer une opération à **toute une colonne d'un coup**, au lieu d'écrire une boucle qui traite les valeurs une par une. Par exemple, `df["taux"] * 100` multiplie les 171 taux en une seule instruction. La boucle existe toujours, mais elle est exécutée **en langage C** à l'intérieur de pandas et numpy, ce qui est bien plus rapide qu'une boucle Python.

### 3. Pourquoi déconseille-t-on `iterrows()` ?

`iterrows()` parcourt le DataFrame **ligne par ligne avec une boucle Python**. On perd donc tout l'intérêt de pandas :

- **C'est très lent :** chaque ligne est transformée en une nouvelle `Series` à chaque tour, ce qui coûte cher. Sur un gros tableau, c'est des dizaines voire des centaines de fois plus lent qu'une opération vectorisée.
- **Les types peuvent changer :** comme chaque ligne devient une Series, des colonnes de types différents sont converties vers un type commun. Un entier peut ainsi devenir un décimal.
- **Modifier la ligne ne modifie pas le DataFrame**, ce qui crée des bugs discrets.

👉 Il faut presque toujours préférer une opération vectorisée : `df[df["taux"] > 1.17]` plutôt qu'une boucle avec `if`.

### 4. Comment pandas représente-t-il les valeurs manquantes (`NaN`) ? Conséquences sur les moyennes ?

pandas représente une valeur manquante par **`NaN`** (*Not a Number*). Pour les dates, c'est `NaT` (*Not a Time*). Par exemple, quand on réindexe nos taux sur le calendrier des jours ouvrés, les jours fériés sans taux deviennent `NaN`. On les repère avec `df.isna()`.

**Conséquences sur les moyennes :**

- Par défaut, `.mean()`, `.sum()`, `.min()`… **ignorent les `NaN`** (`skipna=True`). La moyenne est donc calculée **seulement sur les valeurs présentes**, et le diviseur est le nombre de valeurs non manquantes, pas le nombre total de lignes.
- Ce n'est pas forcément neutre : si les valeurs manquantes ne sont pas réparties au hasard (par exemple toujours les mêmes jours), la moyenne peut être **biaisée**.
- **numpy, lui, ne les ignore pas :** `np.mean` d'un tableau qui contient un `NaN` renvoie `NaN`. Il faut alors utiliser `np.nanmean`.
- Remplir les `NaN` (avec `ffill()`) ou les supprimer (avec `dropna()`) **change le résultat**. Remplir ajoute des valeurs recopiées qui comptent dans la moyenne. Il faut donc toujours choisir consciemment et le justifier.

---

## Partie B — Nettoyer, consolider et analyser

### 1. C'est quoi le *forward-fill* ? Quelle hypothèse fait-on en l'utilisant ?

Le **forward-fill** (`ffill()`, « propager vers l'avant ») remplace chaque valeur manquante par la **dernière valeur connue avant elle**.

Dans notre cas, la BCE ne publie pas de taux les jours fériés. Entre le 31/12/2025 et le 01/09/2026, il manque 4 jours ouvrés : le 1er janvier, le Vendredi saint (3 avril), le lundi de Pâques (6 avril) et le 1er mai. Après réindexation sur `pd.bdate_range`, ces 4 jours valent `NaN`, et `ffill()` leur donne le taux du jour ouvré précédent.

**L'hypothèse :** on suppose que **le taux n'a pas changé** pendant le jour manquant, autrement dit que la dernière valeur publiée reste la meilleure estimation.

**Pourquoi ce choix est justifié ici :**

- Les jours fériés, la BCE ne fixe **pas de nouveau taux de référence**. Le dernier taux publié reste donc bien la référence officielle en vigueur.
- On n'utilise **que le passé**. Une interpolation (moyenne entre la veille et le lendemain) utiliserait une valeur du futur, qu'on ne connaissait pas encore ce jour-là.
- Il n'y a que 4 trous, d'un jour isolé ou de deux jours : l'hypothèse « le taux n'a pas bougé » reste raisonnable.

**La limite :** si les trous étaient longs (plusieurs semaines), répéter la même valeur fausserait les calculs (variations nulles, moyenne mobile aplatie).

### 2. À quoi sert `resample` ? Que signifie une moyenne mobile ?

**`resample`** sert à **changer la fréquence** d'une série temporelle. Ici, on passe de données **quotidiennes** à des données **mensuelles** : `df["taux"].resample("ME").mean()` regroupe tous les jours d'un même mois et en calcule la moyenne. Il faut toujours dire **comment** on résume chaque période : avec la moyenne, le dernier taux du mois (`.last()`), le minimum, le maximum… C'est l'équivalent d'un `groupby`, mais par période de temps.

**Une moyenne mobile** est une moyenne calculée sur une **fenêtre glissante** des derniers jours, recalculée chaque jour. Par exemple, `df["taux"].rolling(20).mean()` donne, pour chaque date, la moyenne des 20 derniers jours ouvrés (environ un mois). Le lendemain, la fenêtre avance d'un jour : le jour le plus ancien sort et le nouveau entre.

Elle sert à **lisser les variations quotidiennes** pour faire apparaître la **tendance**. Les 19 premières valeurs sont `NaN`, car il n'y a pas encore 20 jours disponibles.

---

## Partie C — Les jointures

### 1. Rappelez les quatre types de jointure : que garde chacune ?

Avec une table de gauche aux clés {1, 2} et une table de droite aux clés {2, 3} :

| `how` | Ce qui est gardé | Clés conservées |
|---|---|---|
| `inner` | Seulement les clés présentes **dans les deux tables** (l'intersection) | {2} |
| `left` | **Toutes les lignes de gauche**, `NaN` à droite quand il n'y a pas de correspondance | {1, 2} |
| `right` | **Toutes les lignes de droite**, `NaN` à gauche quand il n'y a pas de correspondance | {2, 3} |
| `outer` | **Toutes les clés des deux tables** (l'union), `NaN` là où il manque une correspondance | {1, 2, 3} |

### 2. Sur quelle colonne (clé) joint-on ? Que devient une ligne sans correspondance ?

On joint sur une **colonne commune aux deux tables**, la **clé**, qui identifie la même « chose » des deux côtés. Pour nos deux devises, c'est la colonne **`date`** : on met côte à côte le taux USD et le taux de l'autre devise **du même jour**. On l'indique avec `on="date"`.

Ce que devient une ligne **sans correspondance** dépend du type de jointure :

- avec `inner`, elle est **supprimée** du résultat ;
- avec `left`, `right` ou `outer`, elle est **gardée** si elle appartient au côté conservé, et les colonnes de l'autre table sont remplies avec **`NaN`**.

### 3. Pour réunir deux séries de taux sur la même période, quelle jointure choisir et pourquoi ?

On choisit une jointure **`inner` sur la date**.

- Les deux séries viennent de la même source (la BCE) et sur la même période, donc **les dates coïncident** : la jointure est complète et on ne perd aucune ligne. `jointures.py` le vérifie en comparant le nombre de lignes avant et après.
- `inner` garantit qu'il n'y a **aucun `NaN`** dans le résultat. Chaque ligne a bien les deux taux, ce qui permet de calculer directement un taux croisé.
- Si un jour une date manquait d'un côté, `inner` l'écarterait proprement, au lieu de créer une ligne à moitié vide. Avec `outer`, on la garderait avec un `NaN`, ce qui peut être utile pour **repérer** les trous.

On ajoute aussi `validate="one_to_one"` pour vérifier qu'aucune date n'est en double, ce qui évite le piège de la duplication (2 lignes × 3 lignes donnent 6 lignes).

### 4. Quelle différence entre `merge` et `concat` ? Dans quel cas utiliser l'un ou l'autre ?

| | `merge` | `concat` |
|---|---|---|
| **Ce qu'il fait** | **Apparie** les lignes des deux tables grâce à une **clé** commune | **Empile** les tables, sans chercher de correspondance |
| **Sens** | Ajoute des **colonnes** (côte à côte) | Ajoute des **lignes** (les unes sous les autres), ou colle côte à côte selon l'index avec `axis=1` |
| **Exemple** | Réunir le taux USD et le taux GBP **du même jour** | Mettre bout à bout les taux de **janvier** puis ceux de **février** |

👉 On utilise **`merge`** quand on veut **relier** des informations différentes sur les mêmes éléments (même date, même client…). On utilise **`concat`** quand on a **plusieurs morceaux d'un même tableau** (mêmes colonnes) à rassembler. Le troisième outil, `join`, fait comme `merge` mais sur l'**index** au lieu d'une colonne.

---

## Partie D — numpy et polars

### 1. Liste Python ou tableau numpy (`ndarray`) ? C'est quoi un `dtype` ? Le broadcasting ?

| | Liste Python | Tableau numpy (`ndarray`) |
|---|---|---|
| **Types des éléments** | N'importe quel mélange (`[1, "a", True]`) | **Un seul type** pour tous les éléments |
| **Stockage en mémoire** | Chaque élément est un objet Python séparé, rangé n'importe où | Les nombres sont **collés les uns aux autres** dans un bloc continu |
| **Taille** | Peut grandir (`append`) | Taille fixe |
| **Calculs** | Il faut une boucle | Opérations directement sur tout le tableau |
| **`* 2`** | `[1.17, 1.16] * 2` → `[1.17, 1.16, 1.17, 1.16]` (répète la liste) | `np.array([1.17, 1.16]) * 2` → `[2.34, 2.32]` (multiplie chaque élément) |

**Le `dtype`** (*data type*) est le **type commun à tous les éléments** du tableau : `float64` pour nos taux, `int64` pour des entiers, `bool` pour le résultat d'une comparaison comme `taux > 1.17`… Si on mélange des types à la création, numpy convertit tout vers un type commun : `np.array([1, 2.5])` devient `float64`.

**Le broadcasting** (« diffusion ») permet de faire une opération entre un tableau et un **nombre**, ou un tableau de forme compatible, sans boucle. Le nombre est automatiquement « diffusé » à chaque élément : `taux * 100` multiplie chaque taux par 100, et `taux - taux.mean()` soustrait la moyenne à chaque taux.

### 2. Pourquoi numpy est-il plus rapide que des boucles Python ?

- **Le calcul se fait en langage C** (compilé), pas en Python (interprété). Une boucle Python, à chaque tour, doit vérifier le type de chaque valeur, chercher l'opération à faire et créer un nouvel objet pour le résultat. numpy fait tout le calcul d'un coup en C.
- **Un seul type (`dtype`) :** numpy sait à l'avance que tous les éléments sont des `float64`, donc il n'a **rien à vérifier** à chaque élément.
- **Les données sont contiguës en mémoire :** les nombres sont rangés les uns à côté des autres. Le processeur les lit très vite et peut même traiter **plusieurs nombres en une seule instruction** (instructions SIMD).

Mesuré avec `numpy_polars.py` : sur 2 millions de nombres, `np.mean` est **environ 30 fois plus rapide** qu'une boucle `for` qui fait la même moyenne.

### 3. Différences entre pandas et polars ? Quand choisir l'un ou l'autre ?

| | pandas | polars |
|---|---|---|
| **Langage d'implémentation** | Python, avec numpy (C) en dessous | **Rust** (langage compilé, rapide et sûr pour la mémoire) |
| **Usage des cœurs du processeur** | Principalement **un seul cœur** | Utilise **tous les cœurs en parallèle** automatiquement |
| **Évaluation** | **Immédiate** (*eager*) : chaque ligne de code est exécutée tout de suite | Immédiate **ou paresseuse** (*lazy*) : avec `scan_csv(...)...collect()`, polars construit d'abord tout le plan de calcul, l'**optimise** (ne lit que les colonnes et lignes utiles, regroupe les étapes), puis l'exécute d'un coup |
| **Syntaxe** | `df["taux"].mean()`, `df.groupby("mois")["taux"].mean()` | Par expressions : `df.select(pl.col("taux").mean())`, `df.group_by("mois").agg(pl.col("taux").mean())` |
| **Index** | Oui (dates en index, `resample`…) | **Pas d'index** : tout est en colonnes |
| **Écosystème** | Très ancien, énormément de documentation et de librairies compatibles | Plus récent, en croissance |

**Nos mesures** (`numpy_polars.py`) — les résultats sont identiques (moyenne 1,162368, variation −1,362 %, mêmes moyennes mensuelles), mais pas les temps :

| Calcul (2 000 000 lignes) | pandas | polars | pandas / polars |
|---|---|---|---|
| Moyenne | 7.0 ms | 1.1 ms | 6.2x |
| Variation jour à jour | 18.5 ms | 6.6 ms | 2.8x |
| Moyenne par groupe | 53.8 ms | 7.2 ms | 7.4x |

polars est **3 à 7 fois plus rapide**. L'écart est le plus grand sur le regroupement, qui profite du calcul en parallèle sur plusieurs cœurs. Sur nos 171 lignes, en revanche, la différence est invisible.

**Quand choisir l'un ou l'autre ?**

- **pandas** pour des données de taille petite ou moyenne (comme nos 171 taux), pour les **séries temporelles** (index de dates, `resample`, `rolling`), et quand on a besoin d'autres librairies qui attendent un DataFrame pandas (graphiques, statistiques, machine learning). C'est aussi le plus documenté pour apprendre.
- **polars** pour de **gros volumes** (millions de lignes, fichiers de plusieurs Go), quand la **vitesse** compte, ou pour des chaînes de traitement lourdes où l'évaluation paresseuse optimise tout le calcul.
