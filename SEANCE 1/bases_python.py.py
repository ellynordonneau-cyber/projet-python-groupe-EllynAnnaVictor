# -*- coding: utf-8 -*-
"""
bases_python.py
Exercices sur les bases de Python :
  1. Les types
  2. Les opérations
  3. Les conditions
  4. Les boucles
"""

# =====================================================================
# 1. LES TYPES
# =====================================================================
print("=" * 60)
print("1. LES TYPES")
print("=" * 60)

entier = 42
decimal = 3.14
chaine = "Bonjour"
booleen = True
liste = [1, 2, 3]
dictionnaire = {"nom": "Alice", "age": 30}

print(entier, "->", type(entier))
print(decimal, "->", type(decimal))
print(chaine, "->", type(chaine))
print(booleen, "->", type(booleen))
print(liste, "->", type(liste))
print(dictionnaire, "->", type(dictionnaire))


# =====================================================================
# 2. LES OPÉRATIONS
# =====================================================================
print()
print("=" * 60)
print("2. LES OPÉRATIONS")
print("=" * 60)

# --- Arithmétique sur les nombres ---
print("\n--- Arithmétique ---")
a = 17
b = 5
print(f"a = {a}, b = {b}")
print(f"a + b  = {a + b}")    # addition
print(f"a - b  = {a - b}")    # soustraction
print(f"a * b  = {a * b}")    # multiplication
print(f"a / b  = {a / b}")    # division (résultat décimal)
print(f"a // b = {a // b}")   # division entière
print(f"a % b  = {a % b}")    # reste de la division (modulo)
print(f"a ** b = {a ** b}")   # puissance

# --- Chaînes de caractères ---
print("\n--- Chaînes de caractères ---")
s1 = "Bonjour"
s2 = "le monde"
phrase = s1 + " " + s2          # concaténation
print(f"Concaténation : '{phrase}'")
print(f".upper()      : '{phrase.upper()}'")
print(f".lower()      : '{phrase.lower()}'")
print(f".split()      : {phrase.split()}")
print(f".replace()    : '{phrase.replace('monde', 'Python')}'")
print(f".strip()      : '{'   espaces   '.strip()}'")
print(f".count('o')   : {phrase.count('o')}")
print(f"len(phrase)   : {len(phrase)}")

# --- Listes ---
print("\n--- Listes ---")
nombres = [10, 20, 30]
print(f"Liste de départ   : {nombres}")
nombres.append(40)              # ajout d'un élément
print(f"Après append(40)  : {nombres}")
print(f"Longueur          : {len(nombres)}")
print(f"Premier élément   : {nombres[0]}")
print(f"Troisième élément : {nombres[2]}")
print(f"Dernier élément   : {nombres[-1]}")

# --- Dictionnaires ---
print("\n--- Dictionnaires ---")
personne = {"nom": "Alice", "age": 30}
print(f"Dictionnaire de départ : {personne}")
print(f"Accès à 'nom'          : {personne['nom']}")
print(f"Accès à 'age'          : {personne['age']}")
personne["ville"] = "Paris"     # ajout d'une clé
print(f"Après ajout de 'ville' : {personne}")

# --- Comparaisons ---
print("\n--- Comparaisons ---")
x = 7
y = 3
print(f"x = {x}, y = {y}")
print(f"x == y : {x == y}")
print(f"x != y : {x != y}")
print(f"x < y  : {x < y}")
print(f"x > y  : {x > y}")
print(f"x <= y : {x <= y}")
print(f"x >= y : {x >= y}")

# --- Opérateurs booléens ---
print("\n--- Opérateurs booléens ---")
p = True
q = False
print(f"p = {p}, q = {q}")
print(f"p and q : {p and q}")
print(f"p or q  : {p or q}")
print(f"not p   : {not p}")
print(f"not q   : {not q}")


# =====================================================================
# 3. LES CONDITIONS
# =====================================================================
print()
print("=" * 60)
print("3. LES CONDITIONS")
print("=" * 60)

taux = 1.08
if taux > 1:
    print(f"taux = {taux} : au-dessus de 1")
elif taux == 1:
    print(f"taux = {taux} : égal à 1")
else:
    print(f"taux = {taux} : en-dessous de 1")

# Test avec plusieurs valeurs de taux
print("\nTest avec plusieurs valeurs :")
for taux in [1.08, 1, 0.95, 1.0, 2.5, 0]:
    if taux > 1:
        print(f"taux = {taux} : au-dessus de 1")
    elif taux == 1:
        print(f"taux = {taux} : égal à 1")
    else:
        print(f"taux = {taux} : en-dessous de 1")


# =====================================================================
# 4. LES BOUCLES
# =====================================================================
print()
print("=" * 60)
print("4. LES BOUCLES")
print("=" * 60)

taux_liste = [1.02, 0.98, 1.05, 1.10, 0.95]

# --- Boucle for : parcourir la liste et afficher chaque valeur ---
print("\n--- Boucle for ---")
somme_for = 0
for t in taux_liste:
    print(f"Taux : {t}")
    somme_for += t
print(f"Somme des taux (for) : {somme_for:.2f}")

# --- Boucle while : même chose avec un indice ---
print("\n--- Boucle while ---")
somme_while = 0
i = 0
while i < len(taux_liste):
    print(f"Indice {i} -> taux : {taux_liste[i]}")
    somme_while += taux_liste[i]
    i += 1
print(f"Somme des taux (while) : {somme_while:.2f}")

# Vérification avec la fonction intégrée sum()
print(f"\nVérification avec sum() : {sum(taux_liste):.2f}")
