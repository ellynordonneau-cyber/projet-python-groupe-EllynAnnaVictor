# Question 1 :
Python est un langage de programmation créé en 1991. Il s'utilise dans de nombreux domaines comme l'analyse de données et statistiques, l'IA et le machine learning, le développement web, l'automatisation de tâches répétitives ou encore le calcul scientifique et la visualisation de données. Il s'agit d'un langage interprété. Contrairement au langage compilé, il n'a pas besoin d'être transformé en un programme exécutable avant de tourner. Il est exécuté directement par un programme appelé interpréteur. 

# Question 2 : 
Sur Windows et sur Mac, Python se télécharge sur internet où la dernière version stable est disponible. Sur Linux, Python est déjà installé. Pour vérifier que Python est bien installé, on peut ouvrir un terminal (invite de commandes dans Windows,terminal sur Mac/Linux) et enrer "python --version". Si un message s'affiche avec la version du Python qu'on a sur notre ordinateur, c'est que l'installation est bien configurée.

# Question 3 : 
On peut lancer du code Python via le terminal en tapant python script.py pour exécuter un programme complet, comme un script d'automatisation ou de traitement de fichiers. On peut lancer le code en tapant simplement python dans le terminal, si on veut tester rapidement une instruction ou une petite portion de code. On peut également utiliser un environnement de développement (IDE) comme VS Code pour développer un projet plus conséquent. Un notebook Jupyter peut aussi être utilisé pour l'analyse de données car les résultats peuvent être vus sous forme de tableaux et graphiques. Enfin, un environnement en ligne permet de tester du code sans rien installer sur son ordinateur.

# Question sur les types: 
Les types de base en Python sont "int" (nombres entiers), "float" (à virgule), "str" (chaine de caractères), "bool" (booléens),  "list" (listes ordonnées et modifiables), "tuple" (listes ordonnées mais non modifiables), "dict" (dictionnaires) et "set" (ensembles non ordonnés d'éléments uniques). Le typage dynamique signifie que le type est déterminé automatiquement à l'exécution, en fonction de la valeur assignée. On n'a donc pas besoin de déclarer le type d'une variable à l'avance. C'est l'inverse d'un typage statique où l'on doit déclarer le type dès le départ. "3" + 4 provoque une erreur car "3" est une chaine de caractères (type str) et 4 est un entier (type int). Python ne peut pas additionner deux types incompatibles. Il ne fait pas de conversion automatique entre types incompatibles.

# Question sur les opérateurs :
Les opérateurs de comparaison (booleéens) sont des opérateurs comme "==", "!=", "<" ou ">". Ils comparent deux valeurs et renvoient toujours un booléen (True or False). Les opérateurs logiques comme "and", "or" et "not" combinent ou modifient des expressions booléennes. Les opérateurs de comparaison produisent des booléens à partir de valeurs, alors que les opérateurs logiques combinent des expressions entre elles.

# Question sur les boucles :
On utilise la boucle For quand on connait à l'avance le nombre d'itérations, ou quand on veut parcourir une séquence (liste, chaine, plage de nombres...). On l'utilise par exemple pour parcourir une base de données ligne par ligne ou une somme sur une liste de valeurs. La boucle While est utilisée quand on ne connait pas à l'avance le nombre d'itérations et qu'on veut répéter tant qu'une certaine condition reste vraie. Par exemple, on l'utilise quand on demande une saisie à l'utilisateur jusqu'à ce qu'elle soit valide, ou tout processus qui s'arrête selon un critère plutôt qu'un nombre d'étapes fixé.

# Question 1 sur GitHub :
Git est un logiciel de contrôle de version qui sert à suivre l'historique des modifications d'un projet (d'un code, d'un document...). On peut voir qui a changé quoi, quand, et on peut aussi revenir en arrière et faire travailler plusieurs personnes en parallèle. GitHub est une plateforme en ligne qui héberge les projets Git dans le cloud. Elle permet de stocker ses dépôts (repositories) en ligne, de collaborer avec d'autres personnes, de partager son code publiquement et elle ajoute des fonctionnalités supplémentaires comme la gestion de tâches ou les demandes de fusion.

# Question 2 sur GitHub :
Git garde une trace de chaque modification, ce qui permet de comprendre l'évolution du projet. En cas d'erreur, on peut aussi facilement retrouver une version antérieure qui fonctionnait, sans risquer de tout perdre. Git permet aussi à chacun de travailler sur sa propre copie, puis de fusionner les contributions de façon organisée, en détectant et en aidant à résoudre les conflits. GitHub permet de faciliter ce travail collaboratif à distance : le projet est hébergé en ligne, accessible à toute équipe avec des outils pour discuter des changements, suivre les tâches et garder une trace centralisée de tout le travail.

# Question 1 sur les dictionnaires et autres :
Quand on affecte une valeur à une clé qui existe déjà, Python ne crée pas une nouvelle entrée : il remplace la valeur associée à cette clé (comme une mise à jour). Une dictionnaire ne peut jamais contenir deux fois la même clé. Les clés doivent être uniques. Si on essaie de créer une clé qui existe déjà, ce n'est pas interprété comme un ajout, mais comme une modification de l'entrée existante. cette contrainte permet d'enlever toute ambiguïté avec deux valeurs pour une même clé. Cette contrainte d'unicité s'applique aux clés, pas aux valeurs. 

# Question 2 sur les dictionnaires et autres :
Non, si on modifie une valeur de premier niveau dans la copie, l'original n'est pas affecté. En revanche, ".copy()" fait une copie superficielle (shallow copy). Cela veut dire qu'elle copie le dictionnaire "de surface", mais si une valeur est elle-même un objet mutable, cette valeur n'est pas dupliquée. Les deux dictionnaires poitent alors vers le même objet imbriqué en mémoire. Pour éviter ce problème et copier aussi les éléments imbriqués, il faut utiliser une copie profonde (deep copy), avec le module copy. 

# Question 3 sur les dictionnaires et autres :
Un objet est dit mutable s'il peut être modifié après sa création, sans que son identité ne change. A l'inverse, un objet immuable ne peut pas être modifié une fois crée. Toute modification crée en réalité un nouvel objet.
Une copie superficielle (shallow copy) crée un nouvel objet "conteneur", mais les éléments imbriqués (listes, dictionnaires à l'intérieur) restent partagés avec l'original. Une copie profonde (deep copy) crée un nouvel objet, et duplique aussi récursivement tous les objets imbriqués. L'original et la copie sont alors totalement indépendants, à tous les niveaux. Pour faire une copie profonde, on doit d'abord importer le module copy. Puis, on crée une nouvelle variable qui stockera le résultat de la copie. On lui attribue la valeur copy.deepcopy(original) où "original" est le dictionnaire ou la liste de départ. La fonction deepcopy() prend l'objet à copier en argument et renvoie une copie profonde. On doit donc écrire import copy, puis sur la ligne en-dessous, nouvelle variable = copy.deepcopy(original).

# Question 4 sur les dictionnaires et autres :
Les types mutables sont list, dict et set. Les types immuables sont int, float, str, tuple et bool.

Mutable : la liste est modifiée directement

l = [1, 2, 3]

l.append(4)

print(l)  # [1, 2, 3, 4] → même objet, juste modifié

Immuable : la chaîne n'est pas modifiée, on en crée une nouvelle

s = "bonjour"

s = s + "!"

print(s)  # "bonjour!" → en réalité, c'est un NOUVEL objet créé

# Question 1 sur les API :
Une API est une interface de programmation. C'est un intermédiaire qui permet à deux programmes de communiquer entre eux, sans que l'un ait besoin de connaitre le fonctionnement de l'autre. Pour obtenir des données via une API, on lui envoie une requête (souvent une requête HTTP), un peu comme si on tapait une adresse web dans un navigateur. Cette requête contient généralement une URL (l'adresse de l'API qu'on interroge) et parfois d'autres paramètres. L'API traite la demande et renvoie une réponse, le plus souvent au format JSON, contenant les données demandées. JSON (JavaScript Object Notation) est un format de données textuel, très utilisé pour échanger des informations entre systèmes (notamment via les API). Quand on récupère du JSON en Python, il est automatiquement converti en types Python équivalents : un objet devient un dict, un tableau devient un list, une chaîne devient un str, un nombre entier devient un int, un décimal devient un float, un true ou un false devient un bool et un null devient None. 

# Question 2 sur les API :
On enregistre la réponse de l'API dans un fichier, plutôt que de la redemander à chaque fois, pour gagner du temps : lire un fichier sur son ordinateur est beaucoup plus rapide qu'aller chercher les données sur internet. Ça évite aussi d'envoyer trop de requêtes à l'API, car beaucoup de services limitent le nombre de demandes qu'on peut faire (par exemple, pas plus de 100 par jour). Et si jamais l'API ne fonctionne pas ou qu'on n'a plus internet, on peut quand même utiliser les données déjà enregistrées dans le fichier.
