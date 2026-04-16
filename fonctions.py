################################################################################
# File Name                      : fonctions.py
# UE                             : LU3IN025 - IA & Jeux - Projet 3
# Writers                        : BENNOUNA Kamil - 21204602
#                                : KHENNOUSSI Hanane - 21318242
# Creation date                  : 02/04/2026
# Last update date               : 16/04/2026 @ 09:30
# Description                    : Fonctions du projet
################################################################################

import random
import time
import gurobipy as gp
from gurobipy import GRB


# =========================
# Q1 : Lecture des fichiers
# =========================
def lire_pref_etu(fichier):
    """
    Lit les préférences étudiantes depuis un fichier texte (Q1, Q3).

    Args:
        fichier (str): Chemin du fichier des préférences étudiantes.

    Returns:
        list[list[int]]: Matrice CE où CE[i] est la liste ordonnée des
        parcours préférés de l'étudiant i.

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
        UnicodeDecodeError: Si le fichier n'est pas décodable en UTF-8.
        ValueError: Si une préférence ne peut pas être convertie en entier.
    """
    CE = []

    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    for ligne in lignes[1:]:
        morceaux = ligne.strip().split()
        prefs = list(map(int, morceaux[2:]))
        CE.append(prefs)

    return CE


def lire_pref_spe(fichier):
    """
    Lit les capacités et préférences des parcours depuis un fichier texte (Q1, Q3).

    Args:
        fichier (str): Chemin du fichier des préférences des parcours.

    Returns:
        tuple[list[int], list[list[int]]]: Un couple (capacites, CP) où
        capacites[j] est la capacité du parcours j et CP[j] sa
        liste ordonnée d'étudiants.

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
        UnicodeDecodeError: Si le fichier n'est pas décodable en UTF-8.
        ValueError: Si une capacité ou préférence n'est pas un entier valide.
        IndexError: Si le format du fichier est incomplet.
    """
    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    cap_line = lignes[1].strip().split()[1:]
    capacites = list(map(int, cap_line))

    CP = []
    for ligne in lignes[2:]:
        morceaux = ligne.strip().split()
        prefs = list(map(int, morceaux[2:]))
        CP.append(prefs)

    return capacites, CP


# ==============================
# Q3 : Gale-Shapley étudiants
# ==============================
def construire_rang_parcours(CP):
    """
    Construit un accès rapide au rang des étudiants pour chaque parcours (Q3).

    Args:
        CP (list[list[int]]): Préférences des parcours.

    Returns:
        list[dict[int, int]]: Pour chaque parcours j, un dictionnaire
        rang_parcours[j][etu] = position.
    """
    m = len(CP)
    rang_parcours = []

    for j in range(m):
        rang = {}
        for position, etudiant in enumerate(CP[j]):
            rang[etudiant] = position
        rang_parcours.append(rang)

    return rang_parcours


def pire_etudiant(parcours, affect_parcours, rang_parcours):
    """
    Retourne l'étudiant le moins bien classé dans un parcours donné (Q3).

    Args:
        parcours (int): Indice du parcours considéré.
        affect_parcours (list[list[int]]): Affectation courante par parcours.
        rang_parcours (list[dict[int, int]]): Rang des étudiants par parcours.

    Returns:
        int: Identifiant de l'étudiant le moins préféré parmi les affectés.

    Raises:
        IndexError: Si la liste des affectés du parcours est vide.
    """
    etudiants_affectes = affect_parcours[parcours]
    pire = etudiants_affectes[0]

    for e in etudiants_affectes:
        if rang_parcours[parcours][e] > rang_parcours[parcours][pire]:
            pire = e

    return pire


def gale_shapley_etudiants(CE, CP, capacites):
    """
    Exécute Gale-Shapley avec les étudiants comme proposeurs (Q3, Q5).

    Args:
        CE (list[list[int]]): Préférences des étudiants.
        CP (list[list[int]]): Préférences des parcours.
        capacites (list[int]): Capacités des parcours.

    Returns:
        tuple[list[int], list[list[int]]]: Un couple (affect_etu,
        affect_parcours) décrivant l'affectation stable obtenue.
    """
    n = len(CE)
    m = len(CP)

    rang_parcours = construire_rang_parcours(CP)

    libres = list(range(n))
    prochain_choix = [0] * n
    affect_etu = [-1] * n
    affect_parcours = [[] for _ in range(m)]

    while libres:
        etu = libres.pop()

        if prochain_choix[etu] >= len(CE[etu]):
            continue

        parcours = CE[etu][prochain_choix[etu]]
        prochain_choix[etu] += 1

        if len(affect_parcours[parcours]) < capacites[parcours]:
            affect_parcours[parcours].append(etu)
            affect_etu[etu] = parcours
        else:
            pire = pire_etudiant(parcours, affect_parcours, rang_parcours)

            if rang_parcours[parcours][etu] < rang_parcours[parcours][pire]:
                affect_parcours[parcours].remove(pire)
                affect_parcours[parcours].append(etu)

                affect_etu[etu] = parcours
                affect_etu[pire] = -1
                libres.append(pire)
            else:
                libres.append(etu)

    return affect_etu, affect_parcours


# ============================
# Q4 : Gale-Shapley parcours
# ============================
def construire_rang_etu(CE):
    """
    Construit un accès rapide au rang des parcours pour chaque étudiant (Q4).

    Args:
        CE (list[list[int]]): Préférences des étudiants.

    Returns:
        list[dict[int, int]]: Pour chaque étudiant i, un dictionnaire
        rang_etu[i][parcours] = position.
    """
    n = len(CE)
    rang_etu = []

    for i in range(n):
        rang = {}
        for position, parcours in enumerate(CE[i]):
            rang[parcours] = position
        rang_etu.append(rang)

    return rang_etu


def gale_shapley_parcours(CE, CP, capacites):
    """
    Exécute Gale-Shapley avec les parcours comme proposeurs (Q4, Q5).

    Args:
        CE (list[list[int]]): Préférences des étudiants.
        CP (list[list[int]]): Préférences des parcours.
        capacites (list[int]): Capacités des parcours.

    Returns:
        tuple[list[int], list[list[int]]]: Un couple (affect_etu,
        affect_parcours) décrivant l'affectation stable obtenue.
    """
    n = len(CE)
    m = len(CP)

    rang_etu = construire_rang_etu(CE)
    places_libres = capacites[:]
    prochain_choix_parcours = [0] * m
    affect_etu = [-1] * n
    affect_parcours = [[] for _ in range(m)]
    parcours_libres = [j for j in range(m) if places_libres[j] > 0]

    while parcours_libres:
        parcours = parcours_libres.pop()

        while places_libres[parcours] > 0 and prochain_choix_parcours[parcours] < n:
            etu = CP[parcours][prochain_choix_parcours[parcours]]
            prochain_choix_parcours[parcours] += 1

            if affect_etu[etu] == -1:
                affect_etu[etu] = parcours
                affect_parcours[parcours].append(etu)
                places_libres[parcours] -= 1
            else:
                ancien_parcours = affect_etu[etu]

                if rang_etu[etu][parcours] < rang_etu[etu][ancien_parcours]:
                    affect_parcours[ancien_parcours].remove(etu)
                    places_libres[ancien_parcours] += 1

                    affect_etu[etu] = parcours
                    affect_parcours[parcours].append(etu)
                    places_libres[parcours] -= 1

                    if prochain_choix_parcours[ancien_parcours] < n:
                        parcours_libres.append(ancien_parcours)

        if places_libres[parcours] > 0 and prochain_choix_parcours[parcours] < n:
            parcours_libres.append(parcours)

    return affect_etu, affect_parcours


# ==================
# Q6 : Stabilité
# ==================
def paires_instables(CE, CP, affect_etu, affect_parcours):
    """
    Détecte les paires bloquantes dans une affectation donnée (Q6).

    Args:
        CE (list[list[int]]): Préférences des étudiants.
        CP (list[list[int]]): Préférences des parcours.
        affect_etu (list[int]): Parcours affecté à chaque étudiant.
        affect_parcours (list[list[int]]): Étudiants affectés par parcours.

    Returns:
        list[tuple[int, int]]: Liste de paires (etu, parcours)
        potentiellement instables.
    """
    rang_parcours = construire_rang_parcours(CP)
    instables = []

    for etu in range(len(CE)):
        parcours_actuel = affect_etu[etu]

        for parcours in CE[etu]:
            if parcours == parcours_actuel:
                break

            for autre_etu in affect_parcours[parcours]:
                if rang_parcours[parcours][etu] < rang_parcours[parcours][autre_etu]:
                    instables.append((etu, parcours))
                    break

    return instables


# =============================
# Q7 : Génération aléatoire
# =============================
def generer_CE_aleatoire(n):
    """
    Génère une matrice CE aléatoire (Q7).

    Args:
        n (int): Nombre d'étudiants.

    Returns:
        list[list[int]]: Matrice CE de taille n x 9 contenant une
        permutation des 9 parcours pour chaque étudiant.
    """
    CE = []
    nb_parcours = 9

    for _ in range(n):
        prefs = list(range(nb_parcours))
        random.shuffle(prefs)
        CE.append(prefs)

    return CE


def generer_CP_aleatoire(n):
    """
    Génère une matrice CP aléatoire (Q7).

    Args:
        n (int): Nombre d'étudiants.

    Returns:
        list[list[int]]: Matrice CP de taille 9 x n contenant, pour chaque
        parcours, une permutation des étudiants.
    """
    CP = []
    nb_parcours = 9

    for _ in range(nb_parcours):
        prefs = list(range(n))
        random.shuffle(prefs)
        CP.append(prefs)

    return CP


# ======================================
# Q8 : Mesure de temps et visualisation
# ======================================
def generer_capacites(n):
    """
    Construit des capacités équilibrées dont la somme vaut n (Q8).

    Args:
        n (int): Nombre total d'étudiants à répartir.

    Returns:
        list[int]: Liste de 9 capacités, quasi-uniformes et sommant à n.
    """
    nb_parcours = 9
    capacites = [n // nb_parcours] * nb_parcours

    for i in range(n % nb_parcours):
        capacites[i] += 1

    return capacites


def moyenne(liste):
    """
    Calcule la moyenne arithmétique d'une liste numérique (Q8).

    Args:
        liste (list[float | int]): Valeurs à moyenner.

    Returns:
        float: Moyenne des éléments.

    Raises:
        ZeroDivisionError: Si la liste est vide.
        TypeError: Si les éléments ne sont pas numériques.
    """
    return sum(liste) / len(liste)


def tracer_courbe_svg(x, y1, y2, nom_fichier, titre, nom1, nom2):
    """
    Trace deux séries dans un fichier SVG simple (Q8).

    Args:
        x (list[float | int]): Valeurs en abscisse.
        y1 (list[float | int]): Première série.
        y2 (list[float | int]): Deuxième série.
        nom_fichier (str): Nom du fichier SVG à écrire.
        titre (str): Titre du graphique.
        nom1 (str): Légende de la première série.
        nom2 (str): Légende de la deuxième série.

    Returns:
        None: La fonction écrit le fichier sur disque.

    Raises:
        OSError: Si l'écriture du fichier échoue.
    """
    largeur = 800
    hauteur = 500
    marge = 60
    max_y = max(max(y1), max(y2))

    if max_y == 0:
        max_y = 1

    def point(i, y):
        """
        Convertit un point logique (indice, valeur) en coordonnées SVG (Q8).

        Args:
            i (int): Indice du point sur l'axe des x.
            y (float | int): Valeur associée sur l'axe des y.

        Returns:
            tuple[float, float]: Coordonnées (x, y) dans le repère SVG.
        """
        px = marge + i * (largeur - 2 * marge) / (len(x) - 1)
        py = hauteur - marge - y * (hauteur - 2 * marge) / max_y
        return px, py

    points1 = " ".join(f"{point(i, y)[0]},{point(i, y)[1]}" for i, y in enumerate(y1))
    points2 = " ".join(f"{point(i, y)[0]},{point(i, y)[1]}" for i, y in enumerate(y2))

    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500">\n')
        f.write('<rect width="800" height="500" fill="white"/>\n')
        f.write(f'<text x="400" y="30" text-anchor="middle" font-size="20">{titre}</text>\n')
        f.write('<line x1="60" y1="440" x2="740" y2="440" stroke="black"/>\n')
        f.write('<line x1="60" y1="60" x2="60" y2="440" stroke="black"/>\n')
        f.write(f'<polyline fill="none" stroke="blue" stroke-width="2" points="{points1}"/>\n')
        f.write(f'<polyline fill="none" stroke="red" stroke-width="2" points="{points2}"/>\n')
        f.write(f'<text x="600" y="80" fill="blue">{nom1}</text>\n')
        f.write(f'<text x="600" y="100" fill="red">{nom2}</text>\n')

        for i in range(len(x)):
            px, _ = point(i, 0)
            f.write(f'<text x="{px}" y="460" text-anchor="middle" font-size="12">{x[i]}</text>\n')

        f.write("</svg>\n")


def mesurer_temps_moyens(valeurs_n=None, repetitions=10):
    """
    Mesure les temps moyens des deux variantes de Gale-Shapley (Q8).

    Args:
        valeurs_n (list[int] | None): Valeurs de n à tester. Si None,
            utilise [200, 400, ..., 2000].
        repetitions (int): Nombre de tests par valeur de n.

    Returns:
        dict[str, list[float | int]]: Dictionnaire contenant les clés
        valeurs_n, temps_etu et temps_parcours.
    """
    if valeurs_n is None:
        valeurs_n = list(range(200, 2001, 200))

    temps_etu = []
    temps_parcours = []

    for n in valeurs_n:
        liste_temps_etu = []
        liste_temps_parcours = []

        for _ in range(repetitions):
            CE = generer_CE_aleatoire(n)
            CP = generer_CP_aleatoire(n)
            capacites = generer_capacites(n)

            debut = time.perf_counter()
            gale_shapley_etudiants_compte(CE, CP, capacites)
            fin = time.perf_counter()
            liste_temps_etu.append(fin - debut)

            debut = time.perf_counter()
            gale_shapley_parcours_compte(CE, CP, capacites)
            fin = time.perf_counter()
            liste_temps_parcours.append(fin - debut)

        temps_etu.append(moyenne(liste_temps_etu))
        temps_parcours.append(moyenne(liste_temps_parcours))

    return {
        "valeurs_n": valeurs_n,
        "temps_etu": temps_etu,
        "temps_parcours": temps_parcours,
    }


def afficher_temps_moyens(resultats):
    """
    Affiche les temps moyens et génère la courbe associée (Q8).

    Args:
        resultats (dict[str, list[float | int]]): Résultats renvoyés par
            mesurer_temps_moyens.

    Returns:
        None: La fonction affiche les valeurs et écrit courbe_temps.svg.
    """
    valeurs_n = resultats["valeurs_n"]
    temps_etu = resultats["temps_etu"]
    temps_parcours = resultats["temps_parcours"]

    print("\n--- Q8 : Temps moyens ---")
    for n, t_etu, t_parcours in zip(valeurs_n, temps_etu, temps_parcours):
        print(
            "n =",
            n,
            "| GS étudiants =",
            round(t_etu, 6),
            "s | GS parcours =",
            round(t_parcours, 6),
            "s",
        )

    tracer_courbe_svg(
        valeurs_n,
        temps_etu,
        temps_parcours,
        "courbe_temps.svg",
        "Temps moyens",
        "GS étudiants",
        "GS parcours",
    )
    print("Courbe des temps enregistrée dans : courbe_temps.svg")


# ==================================
# Q10 : Comptage des itérations
# ==================================
def gale_shapley_etudiants_compte(CE, CP, capacites):
    """
    Exécute Gale-Shapley côté étudiants et compte les propositions (Q10).

    Args:
        CE (list[list[int]]): Préférences des étudiants.
        CP (list[list[int]]): Préférences des parcours.
        capacites (list[int]): Capacités des parcours.

    Returns:
        tuple[list[int], list[list[int]], int]: Affectation étudiante,
        affectation par parcours et nombre d'itérations (propositions).
    """
    n = len(CE)
    m = len(CP)

    rang_parcours = construire_rang_parcours(CP)
    libres = list(range(n))
    prochain_choix = [0] * n
    affect_etu = [-1] * n
    affect_parcours = [[] for _ in range(m)]
    nb_iterations = 0

    while libres:
        etu = libres.pop()

        if prochain_choix[etu] >= len(CE[etu]):
            continue

        parcours = CE[etu][prochain_choix[etu]]
        prochain_choix[etu] += 1
        nb_iterations += 1

        if len(affect_parcours[parcours]) < capacites[parcours]:
            affect_parcours[parcours].append(etu)
            affect_etu[etu] = parcours
        else:
            pire = pire_etudiant(parcours, affect_parcours, rang_parcours)

            if rang_parcours[parcours][etu] < rang_parcours[parcours][pire]:
                affect_parcours[parcours].remove(pire)
                affect_parcours[parcours].append(etu)
                affect_etu[etu] = parcours
                affect_etu[pire] = -1
                libres.append(pire)
            else:
                libres.append(etu)

    return affect_etu, affect_parcours, nb_iterations


def gale_shapley_parcours_compte(CE, CP, capacites):
    """
    Exécute Gale-Shapley côté parcours et compte les propositions (Q10).

    Args:
        CE (list[list[int]]): Préférences des étudiants.
        CP (list[list[int]]): Préférences des parcours.
        capacites (list[int]): Capacités des parcours.

    Returns:
        tuple[list[int], list[list[int]], int]: Affectation étudiante,
        affectation par parcours et nombre d'itérations (propositions).
    """
    n = len(CE)
    m = len(CP)

    rang_etu = construire_rang_etu(CE)
    places_libres = capacites[:]
    prochain_choix_parcours = [0] * m
    affect_etu = [-1] * n
    affect_parcours = [[] for _ in range(m)]
    parcours_libres = [j for j in range(m) if places_libres[j] > 0]
    nb_iterations = 0

    while parcours_libres:
        parcours = parcours_libres.pop()

        while places_libres[parcours] > 0 and prochain_choix_parcours[parcours] < n:
            etu = CP[parcours][prochain_choix_parcours[parcours]]
            prochain_choix_parcours[parcours] += 1
            nb_iterations += 1

            if affect_etu[etu] == -1:
                affect_etu[etu] = parcours
                affect_parcours[parcours].append(etu)
                places_libres[parcours] -= 1
            else:
                ancien_parcours = affect_etu[etu]

                if rang_etu[etu][parcours] < rang_etu[etu][ancien_parcours]:
                    affect_parcours[ancien_parcours].remove(etu)
                    places_libres[ancien_parcours] += 1
                    affect_etu[etu] = parcours
                    affect_parcours[parcours].append(etu)
                    places_libres[parcours] -= 1

                    if prochain_choix_parcours[ancien_parcours] < n:
                        parcours_libres.append(ancien_parcours)

        if places_libres[parcours] > 0 and prochain_choix_parcours[parcours] < n:
            parcours_libres.append(parcours)

    return affect_etu, affect_parcours, nb_iterations

# ==========================================================
# Q11 : Équité (utilité minimale)
# ==========================================================
def construire_utilites_borda_etudiants(CE):
    """
    Construit les utilités de Borda des étudiants (Q11, Q12, Q13, Q15).

    Args:
        CE (list[list[int]]): Préférences des étudiants.

    Returns:
        list[list[int]]: Matrice Ue de taille n x m où Ue[i][j] est l'utilité
        de l'étudiant i s'il est affecté au parcours j.
    """
    n = len(CE)
    m = len(CE[0])
    rang_etu = construire_rang_etu(CE)

    utilites = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            utilites[i][j] = m - 1 - rang_etu[i][j]

    return utilites


def construire_utilites_borda_parcours(CP):
    """
    Construit les utilités de Borda des parcours (Q12, Q13, Q15).

    Args:
        CP (list[list[int]]): Préférences des parcours.

    Returns:
        list[list[int]]: Matrice Up de taille m x n où Up[j][i] est l'utilité
        du parcours j pour l'étudiant i.
    """
    m = len(CP)
    n = len(CP[0])
    rang_parcours = construire_rang_parcours(CP)

    utilites = [[0] * n for _ in range(m)]
    for j in range(m):
        for i in range(n):
            utilites[j][i] = n - 1 - rang_parcours[j][i]

    return utilites


def reconstruire_affectation_par_parcours(affect_etu, m):
    """
    Reconstruit l'affectation par parcours à partir de l'affectation étudiante (Q11, Q12, Q13, Q14, Q15).

    Args:
        affect_etu (list[int]): Parcours affecté à chaque étudiant.
        m (int): Nombre de parcours.

    Returns:
        list[list[int]]: Liste des étudiants affectés pour chaque parcours.
    """
    affect_parcours = [[] for _ in range(m)]
    for etu, parcours in enumerate(affect_etu):
        if parcours != -1:
            affect_parcours[parcours].append(etu)
    return affect_parcours


def extraire_affectation_variables(x, n, m):
    """
    Extrait une affectation étudiante depuis les variables binaires du modèle (Q11, Q12, Q13, Q14).

    Args:
        x (dict[tuple[int, int], gp.Var]): Variables d'affectation.
        n (int): Nombre d'étudiants.
        m (int): Nombre de parcours.

    Returns:
        list[int]: Affectation des étudiants.
    """
    affect_etu = [-1] * n
    for i in range(n):
        for j in range(m):
            if x[i, j].X > 0.5:
                affect_etu[i] = j
                break
    return affect_etu


def resoudre_modele_equite(CE, CP, capacites):
    """
    Résout le PLNE d'équité maximisant l'utilité minimale des étudiants (Q11).

    Args:
        CE (list[list[int]]): Préférences des étudiants.
        CP (list[list[int]]): Préférences des parcours.
        capacites (list[int]): Capacités des parcours.

    Returns:
        dict[str, int | float | list] | None: Résultat optimal avec affectation
        et métriques, sinon None si le modèle est infaisable.
    """
    n = len(CE)
    m = len(CP)
    utilites_etu = construire_utilites_borda_etudiants(CE)

    model = gp.Model("equite_utilite_min")
    model.Params.OutputFlag = 0

    x = model.addVars(n, m, vtype=GRB.BINARY, name="x")
    z = model.addVar(vtype=GRB.CONTINUOUS, name="z")

    for i in range(n):
        model.addConstr(gp.quicksum(x[i, j] for j in range(m)) == 1, name=f"assign_etu_{i}")

    for j in range(m):
        model.addConstr(gp.quicksum(x[i, j] for i in range(n)) <= capacites[j], name=f"cap_{j}")

    for i in range(n):
        utilite_i = gp.quicksum(utilites_etu[i][j] * x[i, j] for j in range(m))
        model.addConstr(z <= utilite_i, name=f"min_util_{i}")

    model.setObjective(z, GRB.MAXIMIZE)
    model.optimize()

    if model.Status != GRB.OPTIMAL:
        return None

    affect_etu = extraire_affectation_variables(x, n, m)
    affect_parcours = reconstruire_affectation_par_parcours(affect_etu, m)
    utilites_indiv = [utilites_etu[i][affect_etu[i]] for i in range(n)]

    return {
        "affect_etu": affect_etu,
        "affect_parcours": affect_parcours,
        "utilite_min_etu": min(utilites_indiv),
        "utilite_moy_etu": sum(utilites_indiv) / n,
        "objectif": model.ObjVal,
    }


# ==========================================================
# Q12 : Efficacité totale (utilité étu + parcours)
# ==========================================================
def resoudre_modele_utilite_totale(CE, CP, capacites):
    """
    Résout le PLNE maximisant la somme des utilités étudiants et parcours (Q12).

    Args:
        CE (list[list[int]]): Préférences des étudiants.
        CP (list[list[int]]): Préférences des parcours.
        capacites (list[int]): Capacités des parcours.

    Returns:
        dict[str, int | float | list] | None: Résultat optimal avec affectation
        et métriques, sinon None si le modèle est infaisable.
    """
    n = len(CE)
    m = len(CP)
    utilites_etu = construire_utilites_borda_etudiants(CE)
    utilites_parcours = construire_utilites_borda_parcours(CP)

    model = gp.Model("utilite_totale")
    model.Params.OutputFlag = 0

    x = model.addVars(n, m, vtype=GRB.BINARY, name="x")

    for i in range(n):
        model.addConstr(gp.quicksum(x[i, j] for j in range(m)) == 1, name=f"assign_etu_{i}")

    for j in range(m):
        model.addConstr(gp.quicksum(x[i, j] for i in range(n)) <= capacites[j], name=f"cap_{j}")

    objectif = gp.quicksum(
        (utilites_etu[i][j] + utilites_parcours[j][i]) * x[i, j]
        for i in range(n)
        for j in range(m)
    )
    model.setObjective(objectif, GRB.MAXIMIZE)
    model.optimize()

    if model.Status != GRB.OPTIMAL:
        return None

    affect_etu = extraire_affectation_variables(x, n, m)
    affect_parcours = reconstruire_affectation_par_parcours(affect_etu, m)
    utilites_indiv = [utilites_etu[i][affect_etu[i]] for i in range(n)]
    utilite_total_parcours = sum(utilites_parcours[affect_etu[i]][i] for i in range(n))

    return {
        "affect_etu": affect_etu,
        "affect_parcours": affect_parcours,
        "utilite_totale": model.ObjVal,
        "utilite_moy_etu": sum(utilites_indiv) / n,
        "utilite_min_etu": min(utilites_indiv),
        "utilite_totale_parcours": utilite_total_parcours,
    }


# ==========================================================
# Q13 : Efficacité totale avec contrainte top-k
# ==========================================================
def resoudre_modele_utilite_totale_top_k(CE, CP, capacites, k):
    """
    Résout le PLNE d'utilité totale avec contrainte top-k pour tous les étudiants (Q13).

    Args:
        CE (list[list[int]]): Préférences des étudiants.
        CP (list[list[int]]): Préférences des parcours.
        capacites (list[int]): Capacités des parcours.
        k (int): Nombre de premiers choix autorisés pour chaque étudiant.

    Returns:
        dict[str, int | float | list] | None: Résultat optimal si faisable,
        sinon None.
    """
    n = len(CE)
    m = len(CP)
    if not 1 <= k <= m:
        raise ValueError("k doit être compris entre 1 et le nombre de parcours.")

    utilites_etu = construire_utilites_borda_etudiants(CE)
    utilites_parcours = construire_utilites_borda_parcours(CP)
    seuil = m - k

    model = gp.Model("utilite_totale_top_k")
    model.Params.OutputFlag = 0

    x = model.addVars(n, m, vtype=GRB.BINARY, name="x")

    for i in range(n):
        model.addConstr(gp.quicksum(x[i, j] for j in range(m)) == 1, name=f"assign_etu_{i}")

    for j in range(m):
        model.addConstr(gp.quicksum(x[i, j] for i in range(n)) <= capacites[j], name=f"cap_{j}")

    for i in range(n):
        utilite_i = gp.quicksum(utilites_etu[i][j] * x[i, j] for j in range(m))
        model.addConstr(utilite_i >= seuil, name=f"topk_{i}")

    objectif = gp.quicksum(
        (utilites_etu[i][j] + utilites_parcours[j][i]) * x[i, j]
        for i in range(n)
        for j in range(m)
    )
    model.setObjective(objectif, GRB.MAXIMIZE)
    model.optimize()

    if model.Status != GRB.OPTIMAL:
        return None

    affect_etu = extraire_affectation_variables(x, n, m)
    affect_parcours = reconstruire_affectation_par_parcours(affect_etu, m)
    utilites_indiv = [utilites_etu[i][affect_etu[i]] for i in range(n)]

    return {
        "k": k,
        "affect_etu": affect_etu,
        "affect_parcours": affect_parcours,
        "utilite_totale": model.ObjVal,
        "utilite_moy_etu": sum(utilites_indiv) / n,
        "utilite_min_etu": min(utilites_indiv),
    }


# ==========================================================
# Q14 : Plus petit k faisable
# ==========================================================
def trouver_plus_petit_k_faisable(CE, CP, capacites):
    """
    Cherche le plus petit k pour lequel le modèle top-k admet une solution (Q14).

    Args:
        CE (list[list[int]]): Préférences des étudiants.
        CP (list[list[int]]): Préférences des parcours.
        capacites (list[int]): Capacités des parcours.

    Returns:
        dict[str, int | float | list] | None: Résultat de
        resoudre_modele_utilite_totale_top_k pour le plus petit k faisable.
    """
    m = len(CP)
    for k in range(1, m + 1):
        solution = resoudre_modele_utilite_totale_top_k(CE, CP, capacites, k)
        if solution is not None:
            return solution
    return None


# ==========================================================
# Q15 : Comparaison des solutions
# ==========================================================
def evaluer_solution(CE, CP, affect_etu, affect_parcours):
    """
    Évalue une affectation selon stabilité et utilités étudiantes (Q15).

    Args:
        CE (list[list[int]]): Préférences des étudiants.
        CP (list[list[int]]): Préférences des parcours.
        affect_etu (list[int]): Parcours attribué à chaque étudiant.
        affect_parcours (list[list[int]]): Étudiants affectés par parcours.

    Returns:
        dict[str, int | float | bool]: Indicateurs de qualité.
    """
    utilites_etu = construire_utilites_borda_etudiants(CE)
    utilites_indiv = [utilites_etu[i][affect_etu[i]] for i in range(len(CE))]
    instables = paires_instables(CE, CP, affect_etu, affect_parcours)

    return {
        "stable": len(instables) == 0,
        "nb_paires_instables": len(instables),
        "utilite_moy_etu": sum(utilites_indiv) / len(utilites_indiv),
        "utilite_min_etu": min(utilites_indiv),
    }


def comparer_solutions(CE, CP, solutions):
    """
    Compare plusieurs solutions selon les critères demandés (Q15).

    Args:
        CE (list[list[int]]): Préférences des étudiants.
        CP (list[list[int]]): Préférences des parcours.
        solutions (dict[str, tuple[list[int], list[list[int]]]]): Dictionnaire
            nom -> (affect_etu, affect_parcours).

    Returns:
        dict[str, dict[str, int | float | bool]]: Mesures par solution.
    """
    comparaison = {}
    for nom, (affect_etu, affect_parcours) in solutions.items():
        comparaison[nom] = evaluer_solution(CE, CP, affect_etu, affect_parcours)
    return comparaison
