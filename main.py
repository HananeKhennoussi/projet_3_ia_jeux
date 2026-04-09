################################################################################
# File Name                      : main.py
# UE                             : LU3IN025 - IA & Jeux - Projet 3
# Writers                        : BENNOUNA Kamil - 21204602
#                                : KHENNOUSSI Hanane - 21318242
# Creation date                  : 02/04/2026
# Last update date               : 09/04/2026 @ 20:00
################################################################################


#import exemple # Pour pouvoir utiliser les methodes de exemple.py

#print("bonjour")
#maListe=exemple.lectureFichier("test.txt") # Execution de la methode lectureFichier du fichier exemple.
#print(maListe)
#print(len(maListe)) #Longueur de la liste.
#exemple.createFichierLP(maListe[0][0],int(maListe[1][0])) #Methode int(): transforme la chaine de caracteres en entier
import random


def lire_pref_etu(fichier):
    CE = []

    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    # On commence a la ligne 2, car la premiere contient le nombre d'etudiants
    for ligne in lignes[1:]:
        morceaux = ligne.strip().split()

        # morceaux[0] = numero etudiant
        # morceaux[1] = nom etudiant
        # morceaux[2:] = preferences
        prefs = list(map(int, morceaux[2:]))

        CE.append(prefs)

    return CE


def lire_pref_spe(fichier):
    CP = []

    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    # On commence a la ligne 3 :
    # ligne 1 = nombre d'etudiants
    # ligne 2 = capacites
    # lignes suivantes = preferences des parcours
    for ligne in lignes[2:]:
        morceaux = ligne.strip().split()

        # morceaux[0] = numero parcours
        # morceaux[1] = nom parcours
        # morceaux[2:] = preferences
        prefs = list(map(int, morceaux[2:]))

        CP.append(prefs)

    return CP


# Test Q1
CE = lire_pref_etu("PrefEtu.txt")
CP = lire_pref_spe("PrefSpe.txt")

print("CE =", CE)
print("CP =", CP)

#question 3:

def lire_pref_etu(fichier):
    CE = []

    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    for ligne in lignes[1:]:
        morceaux = ligne.strip().split()
        prefs = list(map(int, morceaux[2:]))
        CE.append(prefs)

    return CE


def lire_pref_spe(fichier):
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


def construire_rang_parcours(CP):
    m = len(CP)
    rang_parcours = []

    for j in range(m):
        rang = {}
        for position, etudiant in enumerate(CP[j]):
            rang[etudiant] = position
        rang_parcours.append(rang)

    return rang_parcours


def pire_etudiant(parcours, affect_parcours, rang_parcours):
    etudiants_affectes = affect_parcours[parcours]
    pire = etudiants_affectes[0]

    for e in etudiants_affectes:
        if rang_parcours[parcours][e] > rang_parcours[parcours][pire]:
            pire = e

    return pire


def gale_shapley_etudiants(CE, CP, capacites):
    n = len(CE)
    m = len(CP)

    rang_parcours = construire_rang_parcours(CP)

    libres = list(range(n))
    prochain_choix = [0] * n
    affect_etu = [-1] * n
    affect_parcours = [[] for _ in range(m)]

    while libres:
        etu = libres.pop()

        # securite : si jamais l'etudiant a deja tout essaye
        if prochain_choix[etu] >= len(CE[etu]):
            continue

        parcours = CE[etu][prochain_choix[etu]]
        prochain_choix[etu] += 1

        # cas 1 : le parcours a encore une place
        if len(affect_parcours[parcours]) < capacites[parcours]:
            affect_parcours[parcours].append(etu)
            affect_etu[etu] = parcours

        # cas 2 : le parcours est plein
        else:
            pire = pire_etudiant(parcours, affect_parcours, rang_parcours)

            # le parcours prefere le nouvel etudiant au pire actuel
            if rang_parcours[parcours][etu] < rang_parcours[parcours][pire]:
                affect_parcours[parcours].remove(pire)
                affect_parcours[parcours].append(etu)

                affect_etu[etu] = parcours
                affect_etu[pire] = -1

                libres.append(pire)
            else:
                libres.append(etu)

    return affect_etu, affect_parcours


# ===== TEST Q3 =====
CE = lire_pref_etu("PrefEtu.txt")
capacites, CP = lire_pref_spe("PrefSpe.txt")

affect_etu, affect_parcours = gale_shapley_etudiants(CE, CP, capacites)

print("Affectation des etudiants :", affect_etu)
print("Affectation des parcours :", affect_parcours)

#question 4:

# ====== CONSTRUIRE LE RANG DES PARCOURS DANS LES PREFS DES ETUDIANTS ======
def construire_rang_etu(CE):
    n = len(CE)
    rang_etu = []

    for i in range(n):
        rang = {}
        for position, parcours in enumerate(CE[i]):
            rang[parcours] = position
        rang_etu.append(rang)

    return rang_etu


# ====== GALE-SHAPLEY COTE PARCOURS ======
def gale_shapley_parcours(CE, CP, capacites):
    n = len(CE)
    m = len(CP)

    rang_etu = construire_rang_etu(CE)

    # nombre de places encore libres dans chaque parcours
    places_libres = capacites[:]

    # prochain etudiant auquel chaque parcours doit proposer
    prochain_choix_parcours = [0] * m

    # affectation actuelle
    affect_etu = [-1] * n
    affect_parcours = [[] for _ in range(m)]

    # liste des parcours qui ont encore des places
    parcours_libres = [j for j in range(m) if places_libres[j] > 0]

    while parcours_libres:
        parcours = parcours_libres.pop()

        # tant que ce parcours a encore des places
        # et qu'il reste des etudiants a qui proposer
        while places_libres[parcours] > 0 and prochain_choix_parcours[parcours] < n:
            etu = CP[parcours][prochain_choix_parcours[parcours]]
            prochain_choix_parcours[parcours] += 1

            # cas 1 : l'etudiant est libre
            if affect_etu[etu] == -1:
                affect_etu[etu] = parcours
                affect_parcours[parcours].append(etu)
                places_libres[parcours] -= 1

            # cas 2 : l'etudiant a deja un parcours
            else:
                ancien_parcours = affect_etu[etu]

                # l'etudiant prefere le nouveau parcours
                if rang_etu[etu][parcours] < rang_etu[etu][ancien_parcours]:
                    affect_parcours[ancien_parcours].remove(etu)
                    places_libres[ancien_parcours] += 1

                    affect_etu[etu] = parcours
                    affect_parcours[parcours].append(etu)
                    places_libres[parcours] -= 1

                    # l'ancien parcours a maintenant une place libre,
                    # il devra continuer a proposer
                    if prochain_choix_parcours[ancien_parcours] < n:
                        parcours_libres.append(ancien_parcours)

                # sinon l'etudiant refuse, et le parcours continue
                else:
                    pass

        # si le parcours n'est pas plein mais peut encore proposer plus tard,
        # on le remet dans la liste
        if places_libres[parcours] > 0 and prochain_choix_parcours[parcours] < n:
            parcours_libres.append(parcours)

    return affect_etu, affect_parcours

# Test Question 3:

print("\n--- GS cote parcours ---")
affect_etu_p, affect_parcours_p = gale_shapley_parcours(CE, CP, capacites)
print("Affectation des etudiants :", affect_etu_p)
print("Affectation des parcours :", affect_parcours_p)


# Question 6:

def paires_instables(CE, CP, affect_etu, affect_parcours):
    rang_etu = construire_rang_etu(CE)
    rang_parcours = construire_rang_parcours(CP)

    instables = []

    # On regarde chaque etudiant
    for etu in range(len(CE)):
        parcours_actuel = affect_etu[etu]

        # On parcourt les preferences de l'etudiant
        for parcours in CE[etu]:

            # Des qu'on arrive a son parcours actuel, on s'arrete :
            # tous les suivants sont moins bien classes
            if parcours == parcours_actuel:
                break

            # Verifier si le parcours prefere cet etudiant
            # a au moins un etudiant deja affecte chez lui
            for autre_etu in affect_parcours[parcours]:
                if rang_parcours[parcours][etu] < rang_parcours[parcours][autre_etu]:
                    instables.append((etu, parcours))
                    break

    return instables


# ====== TEST Q6 ======

print("\n--- Verification stabilite GS cote etudiants ---")
instables_etu = paires_instables(CE, CP, affect_etu, affect_parcours)
print("Paires instables :", instables_etu)
print("Nombre de paires instables :", len(instables_etu))

print("\n--- Verification stabilite GS cote parcours ---")
instables_parcours = paires_instables(CE, CP, affect_etu_p, affect_parcours_p)
print("Paires instables :", instables_parcours)
print("Nombre de paires instables :", len(instables_parcours))

# Question 7:

def generer_CE_aleatoire(n):
    CE = []
    nb_parcours = 9

    for i in range(n):
        prefs = list(range(nb_parcours))   # [0,1,2,3,4,5,6,7,8]
        random.shuffle(prefs)              # melange aleatoire
        CE.append(prefs)

    return CE


def generer_CP_aleatoire(n):
    CP = []
    nb_parcours = 9

    for j in range(nb_parcours):
        prefs = list(range(n))             # [0,1,2,...,n-1]
        random.shuffle(prefs)              # melange aleatoire
        CP.append(prefs)

    return CP


# ====== TEST Q7 ======

n = 12

CE_test = generer_CE_aleatoire(n)
CP_test = generer_CP_aleatoire(n)

print("\n--- Q7 : test generation aleatoire ---")
print("CE aleatoire =", CE_test)
print("CP aleatoire =", CP_test)


# Question 8 a 10:

import time


def generer_capacites(n):
    nb_parcours = 9
    capacites = [n // nb_parcours] * nb_parcours

    for i in range(n % nb_parcours):
        capacites[i] += 1

    return capacites


def gale_shapley_etudiants_compte(CE, CP, capacites):
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


def tracer_courbe_svg(x, y1, y2, nom_fichier, titre, nom1, nom2):
    largeur = 800
    hauteur = 500
    marge = 60
    max_y = max(max(y1), max(y2))

    if max_y == 0:
        max_y = 1

    def point(i, y):
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


def moyenne(liste):
    return sum(liste) / len(liste)


def mesures_q8_q10():
    valeurs_n = list(range(200, 2001, 200))

    temps_etu = []
    temps_parcours = []
    iter_etu = []
    iter_parcours = []

    for n in valeurs_n:
        liste_temps_etu = []
        liste_temps_parcours = []
        liste_iter_etu = []
        liste_iter_parcours = []

        for _ in range(10):
            CE = generer_CE_aleatoire(n)
            CP = generer_CP_aleatoire(n)
            capacites = generer_capacites(n)

            debut = time.perf_counter()
            _, _, nb1 = gale_shapley_etudiants_compte(CE, CP, capacites)
            fin = time.perf_counter()
            liste_temps_etu.append(fin - debut)
            liste_iter_etu.append(nb1)

            debut = time.perf_counter()
            _, _, nb2 = gale_shapley_parcours_compte(CE, CP, capacites)
            fin = time.perf_counter()
            liste_temps_parcours.append(fin - debut)
            liste_iter_parcours.append(nb2)

        temps_etu.append(moyenne(liste_temps_etu))
        temps_parcours.append(moyenne(liste_temps_parcours))
        iter_etu.append(moyenne(liste_iter_etu))
        iter_parcours.append(moyenne(liste_iter_parcours))

    print("\n--- Q8 : temps moyens ---")
    for i in range(len(valeurs_n)):
        print(
            "n =",
            valeurs_n[i],
            "| GS etudiants =",
            round(temps_etu[i], 6),
            "s | GS parcours =",
            round(temps_parcours[i], 6),
            "s",
        )

    tracer_courbe_svg(
        valeurs_n,
        temps_etu,
        temps_parcours,
        "courbe_temps.svg",
        "Temps moyen",
        "GS etudiants",
        "GS parcours",
    )

    print("\n--- Q9 ---")
    print("Sur ces tests, le temps augmente globalement avec n.")
    print("On observe une croissance assez proche du lineaire.")
    print("C'est coherent pour GS cote parcours.")
    print("Pour GS cote etudiants, la borne theorique peut etre plus grande,")
    print("mais sur des preferences aleatoires le comportement reste ici modere.")

    print("\n--- Q10 : iterations moyennes ---")
    for i in range(len(valeurs_n)):
        print(
            "n =",
            valeurs_n[i],
            "| GS etudiants =",
            round(iter_etu[i], 2),
            "| GS parcours =",
            round(iter_parcours[i], 2),
        )

    tracer_courbe_svg(
        valeurs_n,
        iter_etu,
        iter_parcours,
        "courbe_iterations.svg",
        "Iterations moyennes",
        "GS etudiants",
        "GS parcours",
    )

    print("\nPour Q10, le nombre d'iterations augmente lui aussi globalement avec n.")
    print("Ici encore, on observe quelque chose de proche du lineaire.")


mesures_q8_q10()
