################################################################################
# File Name                      : main.py
# UE                             : LU3IN025 - IA & Jeux - Projet 3
# Writers                        : BENNOUNA Kamil - 21204602
#                                : KHENNOUSSI Hanane - 21318242
# Creation date                  : 02/04/2026
# Last update date               : 16/04/2026 @ 09:30
# Description                    : Tests des fonctions implémentées
################################################################################

from fonctions import *


if __name__ == "__main__":
    # =========================
    # Q1 : Lecture des fichiers
    # =========================
    print("\n===== Q1 : Lecture des préférences =====")
    fichier_etu = "PrefEtu.txt"
    fichier_spe = "PrefSpe.txt"

    CE = lire_pref_etu(fichier_etu)
    capacites, CP = lire_pref_spe(fichier_spe)

    print("CE =", CE)
    print("CP =", CP)
    print("Capacités =", capacites)

    # =================================
    # Q3 : Gale-Shapley côté étudiants
    # =================================
    print("\n===== Q3 : Gale-Shapley côté étudiants =====")
    affect_etu_q3, affect_parcours_q3 = gale_shapley_etudiants(CE, CP, capacites)
    print("Affectation des étudiants :", affect_etu_q3)
    print("Affectation des parcours :", affect_parcours_q3)

    # ================================
    # Q4 : Gale-Shapley côté parcours
    # ================================
    print("\n===== Q4 : Gale-Shapley côté parcours =====")
    affect_etu_q4, affect_parcours_q4 = gale_shapley_parcours(CE, CP, capacites)
    print("Affectation des étudiants :", affect_etu_q4)
    print("Affectation des parcours :", affect_parcours_q4)

    # ===========================================
    # Q5 : Application des deux algorithmes tests
    # ===========================================
    print("\n===== Q5 : Affectations obtenues sur les fichiers tests =====")
    print("GS côté étudiants ->", affect_etu_q3)
    print("GS côté parcours  ->", affect_etu_q4)

    # =================================
    # Q6 : Vérification de la stabilité
    # =================================
    print("\n===== Q6 : Paires instables =====")
    instables_q3 = paires_instables(CE, CP, affect_etu_q3, affect_parcours_q3)
    instables_q4 = paires_instables(CE, CP, affect_etu_q4, affect_parcours_q4)

    print("GS côté étudiants - paires instables :", instables_q3)
    print("GS côté étudiants - nombre :", len(instables_q3))
    print("GS côté parcours  - paires instables :", instables_q4)
    print("GS côté parcours  - nombre :", len(instables_q4))

    # =================================
    # Q7 : Génération aléatoire CE / CP
    # =================================
    print("\n===== Q7 : Génération aléatoire =====")
    n = 12
    CE_test = generer_CE_aleatoire(n)
    CP_test = generer_CP_aleatoire(n)
    print("CE aléatoire =", CE_test)
    print("CP aléatoire =", CP_test)

    # ======================================
    # Q8 : Mesure du temps de calcul (moyen)
    # ======================================
    print("\n===== Q8 : Évolution du temps de calcul =====")
    resultats_temps = mesurer_temps_moyens()
    afficher_temps_moyens(resultats_temps)

    # ==================================
    # Q9 : Évolution du temps de calcul
    # ==================================
    # Complexité observée : croissance globalement proche du linéaire en n
    # dans nos tests (9 parcours fixes), ce qui est cohérent empiriquement
    # avec le comportement attendu sur des préférences aléatoires.

    # ===================================
    # Q10 : Évolution du nombre d'itérations
    # ===================================
    # Le nombre d'itérations augmente lui aussi globalement avec n.
    # Sur ce cadre (nombre de parcours fixé), l'évolution observée reste
    # cohérente avec l'analyse théorique.

    # ==========================================================
    # Q11 : PLNE d'équité
    # ==========================================================
    print("\n===== Q11 : Équité (utilité minimale) =====")
    # Réponse (formulation PLNE) :
    # Variables :
    # x_{i,j} ∈ {0,1} : 1 si l'étudiant i est affecté au parcours j.
    # z ∈ R : utilité minimale garantie aux étudiants.
    #
    # Paramètres :
    # u^E_{i,j} : utilité de Borda de l'étudiant i pour le parcours j.
    # c_j : capacité du parcours j.
    #
    # Objectif :
    # max z
    #
    # Contraintes :
    # 1) Pour tout i : Σ_j x_{i,j} = 1
    # 2) Pour tout j : Σ_i x_{i,j} ≤ c_j
    # 3) Pour tout i : z ≤ Σ_j u^E_{i,j} x_{i,j}
    # 4) x_{i,j} ∈ {0,1}
    sol_q11 = resoudre_modele_equite(CE, CP, capacites)
    print("Affectation Q11 :", sol_q11["affect_etu"])
    print("Utilité minimale étudiants (Q11) :", sol_q11["utilite_min_etu"])
    print("Utilité moyenne étudiants (Q11) :", round(sol_q11["utilite_moy_etu"], 3))

    # ==========================================================
    # Q12 : PLNE d'efficacité totale
    # ==========================================================
    print("\n===== Q12 : Utilité totale (étudiants + parcours) =====")
    # Réponse (formulation PLNE) :
    # Variables :
    # x_{i,j} ∈ {0,1}
    #
    # Paramètres :
    # u^E_{i,j} : utilité de Borda étudiante
    # u^P_{j,i} : utilité de Borda parcours
    # c_j : capacité du parcours j
    #
    # Objectif :
    # max Σ_i Σ_j (u^E_{i,j} + u^P_{j,i}) x_{i,j}
    #
    # Contraintes :
    # 1) Pour tout i : Σ_j x_{i,j} = 1
    # 2) Pour tout j : Σ_i x_{i,j} ≤ c_j
    # 3) x_{i,j} ∈ {0,1}
    sol_q12 = resoudre_modele_utilite_totale(CE, CP, capacites)
    print("Affectation Q12 :", sol_q12["affect_etu"])
    print("Utilité moyenne étudiants (Q12) :", round(sol_q12["utilite_moy_etu"], 3))
    print("Utilité minimale étudiants (Q12) :", sol_q12["utilite_min_etu"])

    # ==========================================================
    # Q13 : PLNE efficacité totale sous contrainte top-k
    # ==========================================================
    print("\n===== Q13 : Utilité totale avec contrainte top-k =====")
    # Réponse (formulation PLNE) :
    # Même modèle que Q12, avec la contrainte supplémentaire :
    # pour tout i, Σ_j u^E_{i,j} x_{i,j} ≥ m - k
    # (équivalent à : l'étudiant i est affecté à l'un de ses k premiers choix).
    k_test = 3
    sol_q13 = resoudre_modele_utilite_totale_top_k(CE, CP, capacites, k_test)
    if sol_q13 is None:
        print(f"Aucune solution faisable pour k = {k_test}.")
    else:
        print(f"Solution faisable pour k = {k_test}.")
        print("Affectation Q13 :", sol_q13["affect_etu"])
        print("Utilité minimale étudiants (Q13) :", sol_q13["utilite_min_etu"])

    # ==========================================================
    # Q14 : Recherche du plus petit k faisable
    # ==========================================================
    print("\n===== Q14 : Plus petit k pour un mariage parfait =====")
    sol_q14 = trouver_plus_petit_k_faisable(CE, CP, capacites)
    if sol_q14 is None:
        print("Aucun k faisable trouvé.")
    else:
        print("Plus petit k faisable :", sol_q14["k"])
        print("Affectation obtenue (Q14) :", sol_q14["affect_etu"])

    # ==========================================================
    # Q15 : Comparaison des solutions
    # ==========================================================
    print("\n===== Q15 : Comparaison des solutions =====")
    solutions = {
        "GS côté étudiants": (affect_etu_q3, affect_parcours_q3),
        "GS côté parcours": (affect_etu_q4, affect_parcours_q4),
        "Q11 équité": (sol_q11["affect_etu"], sol_q11["affect_parcours"]),
        "Q12 utilité totale": (sol_q12["affect_etu"], sol_q12["affect_parcours"]),
        "Q14 top-k minimum": (sol_q14["affect_etu"], sol_q14["affect_parcours"]),
    }
    comparaison = comparer_solutions(CE, CP, solutions)
    for nom, stats in comparaison.items():
        print(
            f"{nom} | stable={stats['stable']} | "
            f"paires_instables={stats['nb_paires_instables']} | "
            f"utilité_moyenne={round(stats['utilite_moy_etu'], 3)} | "
            f"utilité_minimale={stats['utilite_min_etu']}"
        )
