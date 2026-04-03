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

    # On commence à la ligne 2, car la première contient le nombre d'étudiants
    for ligne in lignes[1:]:
        morceaux = ligne.strip().split()

        # morceaux[0] = numéro étudiant
        # morceaux[1] = nom étudiant
        # morceaux[2:] = préférences
        prefs = list(map(int, morceaux[2:]))

        CE.append(prefs)

    return CE


def lire_pref_spe(fichier):
    CP = []

    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    # On commence à la ligne 3 :
    # ligne 1 = nombre d'étudiants
    # ligne 2 = capacités
    # lignes suivantes = préférences des parcours
    for ligne in lignes[2:]:
        morceaux = ligne.strip().split()

        # morceaux[0] = numéro parcours
        # morceaux[1] = nom parcours
        # morceaux[2:] = préférences
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

        # sécurité : si jamais l'étudiant a déjà tout essayé
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

            # le parcours préfère le nouvel étudiant au pire actuel
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

print("Affectation des étudiants :", affect_etu)
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

    # prochain étudiant auquel chaque parcours doit proposer
    prochain_choix_parcours = [0] * m

    # affectation actuelle
    affect_etu = [-1] * n
    affect_parcours = [[] for _ in range(m)]

    # liste des parcours qui ont encore des places
    parcours_libres = [j for j in range(m) if places_libres[j] > 0]

    while parcours_libres:
        parcours = parcours_libres.pop()

        # tant que ce parcours a encore des places
        # et qu'il reste des étudiants à qui proposer
        while places_libres[parcours] > 0 and prochain_choix_parcours[parcours] < n:
            etu = CP[parcours][prochain_choix_parcours[parcours]]
            prochain_choix_parcours[parcours] += 1

            # cas 1 : l'étudiant est libre
            if affect_etu[etu] == -1:
                affect_etu[etu] = parcours
                affect_parcours[parcours].append(etu)
                places_libres[parcours] -= 1

            # cas 2 : l'étudiant a déjà un parcours
            else:
                ancien_parcours = affect_etu[etu]

                # l'étudiant préfère le nouveau parcours
                if rang_etu[etu][parcours] < rang_etu[etu][ancien_parcours]:
                    affect_parcours[ancien_parcours].remove(etu)
                    places_libres[ancien_parcours] += 1

                    affect_etu[etu] = parcours
                    affect_parcours[parcours].append(etu)
                    places_libres[parcours] -= 1

                    # l'ancien parcours a maintenant une place libre,
                    # il devra continuer à proposer
                    if prochain_choix_parcours[ancien_parcours] < n:
                        parcours_libres.append(ancien_parcours)

                # sinon l'étudiant refuse, et le parcours continue
                else:
                    pass

        # si le parcours n'est pas plein mais peut encore proposer plus tard,
        # on le remet dans la liste
        if places_libres[parcours] > 0 and prochain_choix_parcours[parcours] < n:
            parcours_libres.append(parcours)

    return affect_etu, affect_parcours

# Test Question 3:

print("\n--- GS côté parcours ---")
affect_etu_p, affect_parcours_p = gale_shapley_parcours(CE, CP, capacites)
print("Affectation des étudiants :", affect_etu_p)
print("Affectation des parcours :", affect_parcours_p)


# Question 6:

def paires_instables(CE, CP, affect_etu, affect_parcours):
    rang_etu = construire_rang_etu(CE)
    rang_parcours = construire_rang_parcours(CP)

    instables = []

    # On regarde chaque étudiant
    for etu in range(len(CE)):
        parcours_actuel = affect_etu[etu]

        # On parcourt les préférences de l'étudiant
        for parcours in CE[etu]:

            # Dès qu'on arrive à son parcours actuel, on s'arrête :
            # tous les suivants sont moins bien classés
            if parcours == parcours_actuel:
                break

            # Vérifier si le parcours préfère cet étudiant
            # à au moins un étudiant déjà affecté chez lui
            for autre_etu in affect_parcours[parcours]:
                if rang_parcours[parcours][etu] < rang_parcours[parcours][autre_etu]:
                    instables.append((etu, parcours))
                    break

    return instables


# ====== TEST Q6 ======

print("\n--- Vérification stabilité GS côté étudiants ---")
instables_etu = paires_instables(CE, CP, affect_etu, affect_parcours)
print("Paires instables :", instables_etu)
print("Nombre de paires instables :", len(instables_etu))

print("\n--- Vérification stabilité GS côté parcours ---")
instables_parcours = paires_instables(CE, CP, affect_etu_p, affect_parcours_p)
print("Paires instables :", instables_parcours)
print("Nombre de paires instables :", len(instables_parcours))

# Question 7:

def generer_CE_aleatoire(n):
    CE = []
    nb_parcours = 9

    for i in range(n):
        prefs = list(range(nb_parcours))   # [0,1,2,3,4,5,6,7,8]
        random.shuffle(prefs)              # mélange aléatoire
        CE.append(prefs)

    return CE


def generer_CP_aleatoire(n):
    CP = []
    nb_parcours = 9

    for j in range(nb_parcours):
        prefs = list(range(n))             # [0,1,2,...,n-1]
        random.shuffle(prefs)              # mélange aléatoire
        CP.append(prefs)

    return CP


# ====== TEST Q7 ======

n = 12

CE_test = generer_CE_aleatoire(n)
CP_test = generer_CP_aleatoire(n)

print("\n--- Q7 : test génération aléatoire ---")
print("CE aléatoire =", CE_test)
print("CP aléatoire =", CP_test)
