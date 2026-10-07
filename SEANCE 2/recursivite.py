# -*- coding: utf-8 -*-
"""
recursivite.py
Séance 2 — Partie C : récursivité et complexité.

C.1 — Deux fonctions récursives simples : la factorielle n! et la somme
      des éléments d'une liste (cas de base + cas récursif).
C.2 — Fibonacci en trois versions :
        - récursive naïve           : temps O(2^n), mémoire O(n)
        - récursive + mémoïsation   : temps O(n),   mémoire O(n)
        - itérative (boucle for)    : temps O(n),   mémoire O(1)
      Mesure du temps avec time.perf_counter pour des n croissants,
      puis observation de la RecursionError pour une profondeur trop grande.
C.3 — Comparaison chiffrée des trois versions : temps, nombre d'appels,
      profondeur de récursion et mémoire (tracemalloc).

Uniquement la bibliothèque standard : functools, time, sys, tracemalloc.
"""

import sys
import time
import tracemalloc
from functools import lru_cache


# =====================================================================
# C.1 — FONCTIONS RÉCURSIVES SIMPLES
# =====================================================================

def factorielle(n):
    """Calcule n! = n × (n-1) × ... × 1 de façon récursive.

    Paramètre :
        n (int) : un entier positif ou nul.
    Renvoie :
        int : la factorielle de n.
    """
    if n == 0:                      # cas de base : 0! = 1, on s'arrête
        return 1
    return n * factorielle(n - 1)   # cas récursif : n! = n × (n-1)!


def somme_liste(liste):
    """Calcule la somme des éléments d'une liste de façon récursive.

    Paramètre :
        liste (list de nombres) : les éléments à additionner.
    Renvoie :
        nombre : la somme des éléments (0 pour une liste vide).
    """
    if len(liste) == 0:                     # cas de base : liste vide
        return 0
    return liste[0] + somme_liste(liste[1:])  # cas récursif : 1er + somme du reste


# =====================================================================
# C.2 — FIBONACCI EN TROIS VERSIONS
# fib(0) = 0, fib(1) = 1, fib(n) = fib(n-1) + fib(n-2)
# =====================================================================

# Compteurs pour mesurer le nombre d'appels et la profondeur atteinte
compteur = {"appels": 0, "profondeur": 0, "profondeur_max": 0}


def remettre_compteur_a_zero():
    """Remet les compteurs d'appels et de profondeur à zéro."""
    compteur["appels"] = 0
    compteur["profondeur"] = 0
    compteur["profondeur_max"] = 0


def fib_naif(n):
    """Fibonacci récursif naïf : recalcule plusieurs fois les mêmes valeurs.

    Paramètre :
        n (int) : le rang voulu (n >= 0).
    Renvoie :
        int : le n-ième nombre de Fibonacci.
    """
    compteur["appels"] += 1
    compteur["profondeur"] += 1
    compteur["profondeur_max"] = max(compteur["profondeur_max"], compteur["profondeur"])

    if n < 2:                                   # cas de base
        resultat = n
    else:                                       # cas récursif
        resultat = fib_naif(n - 1) + fib_naif(n - 2)

    compteur["profondeur"] -= 1
    return resultat


@lru_cache(maxsize=None)
def fib_memo(n):
    """Fibonacci récursif avec mémoïsation (functools.lru_cache).

    Chaque fib_memo(k) n'est calculé qu'une seule fois, puis gardé en mémoire.

    Paramètre :
        n (int) : le rang voulu (n >= 0).
    Renvoie :
        int : le n-ième nombre de Fibonacci.
    """
    compteur["appels"] += 1
    compteur["profondeur"] += 1
    compteur["profondeur_max"] = max(compteur["profondeur_max"], compteur["profondeur"])

    if n < 2:
        resultat = n
    else:
        resultat = fib_memo(n - 1) + fib_memo(n - 2)

    compteur["profondeur"] -= 1
    return resultat


def fib_iteratif(n):
    """Fibonacci itératif : une simple boucle, sans récursion.

    Paramètre :
        n (int) : le rang voulu (n >= 0).
    Renvoie :
        int : le n-ième nombre de Fibonacci.
    """
    a, b = 0, 1             # a = fib(0), b = fib(1)
    for _ in range(n):
        a, b = b, a + b     # on avance d'un rang
    return a


# =====================================================================
# OUTILS DE MESURE
# =====================================================================

def mesurer_temps(fonction, n):
    """Mesure le temps d'exécution de fonction(n) avec time.perf_counter.

    Paramètres :
        fonction (function) : la fonction à mesurer.
        n (int)             : l'argument à lui passer.
    Renvoie :
        tuple : (résultat, durée en secondes).
    """
    debut = time.perf_counter()
    resultat = fonction(n)
    duree = time.perf_counter() - debut
    return resultat, duree


def mesurer_memoire(fonction, n):
    """Mesure le pic de mémoire utilisé pendant fonction(n) avec tracemalloc.

    Paramètres :
        fonction (function) : la fonction à mesurer.
        n (int)             : l'argument à lui passer.
    Renvoie :
        int : le pic de mémoire alloué, en octets.
    """
    tracemalloc.start()
    fonction(n)
    _, pic = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pic


def formater_duree(secondes):
    """Affiche une durée de façon lisible (µs, ms ou s).

    Paramètre :
        secondes (float) : la durée en secondes.
    Renvoie :
        str : la durée formatée, par exemple "12.3 ms".
    """
    if secondes < 1e-3:
        return f"{secondes * 1e6:.1f} µs"
    if secondes < 1:
        return f"{secondes * 1e3:.1f} ms"
    return f"{secondes:.2f} s"


# =====================================================================
# PROGRAMME PRINCIPAL
# =====================================================================

def demo_c1():
    """Teste la factorielle et la somme récursive."""
    print("=" * 70)
    print("C.1 — FONCTIONS RÉCURSIVES SIMPLES")
    print("=" * 70)
    for n in [0, 1, 5, 10]:
        print(f"factorielle({n}) = {factorielle(n)}")
    liste = [1.02, 0.98, 1.05, 1.10, 0.95]
    print(f"somme_liste({liste}) = {somme_liste(liste):.2f}")
    print(f"Vérification avec sum()          = {sum(liste):.2f}")


def demo_c2_temps():
    """Mesure le temps des trois versions de Fibonacci pour des n croissants."""
    print()
    print("=" * 70)
    print("C.2 — TEMPS D'EXÉCUTION DE FIBONACCI POUR DES n CROISSANTS")
    print("=" * 70)
    print(f"{'n':>4} | {'fib(n)':>10} | {'naïf':>12} | {'appels naïf':>12} | "
          f"{'mémoïsé':>10} | {'itératif':>10}")
    print("-" * 70)

    lignes = []
    for n in [5, 10, 15, 20, 25, 30]:
        remettre_compteur_a_zero()
        resultat, t_naif = mesurer_temps(fib_naif, n)
        appels_naif = compteur["appels"]

        fib_memo.cache_clear()          # on vide le cache pour une mesure honnête
        _, t_memo = mesurer_temps(fib_memo, n)
        _, t_iter = mesurer_temps(fib_iteratif, n)

        print(f"{n:>4} | {resultat:>10} | {formater_duree(t_naif):>12} | "
              f"{appels_naif:>12,} | {formater_duree(t_memo):>10} | "
              f"{formater_duree(t_iter):>10}".replace(",", " "))
        lignes.append((n, resultat, t_naif, appels_naif, t_memo, t_iter))

    print("\n👉 Le temps du naïf est multiplié par environ 11 tous les 5 rangs :")
    print("   c'est la croissance exponentielle O(2^n). Les deux autres restent instantanés.")
    return lignes


def demo_c2_recursion_error():
    """Montre la RecursionError quand la profondeur de récursion est trop grande."""
    print()
    print("=" * 70)
    print("C.2 — PROFONDEUR TROP GRANDE : RecursionError")
    print("=" * 70)
    limite = sys.getrecursionlimit()
    print(f"Limite de récursion de Python : {limite} appels imbriqués")

    n = limite + 1000
    fib_memo.cache_clear()
    try:
        fib_memo(n)
    except RecursionError as erreur:
        print(f"fib_memo({n})     -> ❌ RecursionError : {erreur}")

    resultat = fib_iteratif(n)
    print(f"fib_iteratif({n}) -> ✅ OK, un nombre de {len(str(resultat))} chiffres")
    print("👉 La version itérative n'a pas de limite de profondeur : elle n'empile aucun appel.")


def demo_c3_comparaison():
    """Compare les trois versions pour un même n : temps, appels, profondeur, mémoire."""
    n = 25
    print()
    print("=" * 70)
    print(f"C.3 — COMPARAISON DES TROIS VERSIONS POUR n = {n}")
    print("=" * 70)

    resultats = []

    # Version naïve
    remettre_compteur_a_zero()
    _, t = mesurer_temps(fib_naif, n)
    appels, prof = compteur["appels"], compteur["profondeur_max"]
    memoire = mesurer_memoire(fib_naif, n)
    resultats.append(("Récursive naïve", "O(2^n)", "O(n)", t, appels, prof, memoire))

    # Version mémoïsée
    fib_memo.cache_clear()
    remettre_compteur_a_zero()
    _, t = mesurer_temps(fib_memo, n)
    appels, prof = compteur["appels"], compteur["profondeur_max"]
    fib_memo.cache_clear()
    memoire = mesurer_memoire(fib_memo, n)
    resultats.append(("Récursive + lru_cache", "O(n)", "O(n)", t, appels, prof, memoire))

    # Version itérative (pas d'appels récursifs : 1 appel, profondeur 1)
    _, t = mesurer_temps(fib_iteratif, n)
    memoire = mesurer_memoire(fib_iteratif, n)
    resultats.append(("Itérative (boucle)", "O(n)", "O(1)", t, 1, 1, memoire))

    print(f"{'Version':<22} | {'Temps':>9} | {'Appels':>8} | {'Profondeur':>10} | "
          f"{'Mémoire':>9} | {'Compl. temps':>12} | {'Compl. mémoire':>14}")
    print("-" * 102)
    for nom, c_temps, c_mem, t, appels, prof, memoire in resultats:
        print(f"{nom:<22} | {formater_duree(t):>9} | {appels:>8,} | {prof:>10} | "
              f"{memoire:>7,} o | {c_temps:>12} | {c_mem:>14}".replace(",", " "))

    # Tableau prêt à copier dans docs/notes_seance2.md
    print("\n📋 Tableau à copier dans docs/notes_seance2.md :\n")
    print("| Version | Temps (n = 25) | Nombre d'appels | Profondeur max | "
          "Pic mémoire | Complexité temps | Complexité mémoire |")
    print("|---|---|---|---|---|---|---|")
    for nom, c_temps, c_mem, t, appels, prof, memoire in resultats:
        print(f"| {nom} | {formater_duree(t)} | {appels:,} | {prof} | "
              f"{memoire:,} octets | {c_temps} | {c_mem} |".replace(",", " "))


def main():
    """Lance toutes les démonstrations de la partie C."""
    demo_c1()
    lignes = demo_c2_temps()
    demo_c2_recursion_error()
    demo_c3_comparaison()

    # Tableau des temps prêt à copier dans docs/notes_seance2.md
    print("\n📋 Tableau des temps à copier dans docs/notes_seance2.md :\n")
    print("| n | fib(n) | Naïf | Appels (naïf) | Mémoïsé | Itératif |")
    print("|---|---|---|---|---|---|")
    for n, resultat, t_naif, appels, t_memo, t_iter in lignes:
        print(f"| {n} | {resultat} | {formater_duree(t_naif)} | {appels:,} | "
              f"{formater_duree(t_memo)} | {formater_duree(t_iter)} |".replace(",", " "))


if __name__ == "__main__":
    main()
