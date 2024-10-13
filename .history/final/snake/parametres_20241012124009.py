## liste des méthodes disponibles
liste_methodes=['suivre_chemin','raccourcis_croissants_v2','a_etoile_seul','pomme_moins_queue','a_etoile_seulement_si_modif',
                'a_etoile_graphe_oriente','a_etoile_projection_queue','parcours_cellules A COMPLETER',
                'monte_carlo_tree_search NE MARCHE PAS','a_etoile_graphe_oriente_cout','a_etoile_graphe_oriente_hami',
                'arbre_raccourcis_modifier_hami EXPONENTIEL','raccourcis_croissants_v3']

## paramètre partie
nb_cases=8  # nombre de cases sur le côté de la grille carré
depart_serpent=[0,0]
nb_iterations=1
methode='suivre_chemin'

## gestion des données
ajouter_donnees=False
liste_noms_fichiers=['donnees','donnees_raccourcis_risque']
nom_fichier='donnees'

## affichage
execution_rapide=False
fps=30
afficher=True
afficher_taux_raccourcis=True
facteur_resolution=0.5  # relativement à la résolution 1920x1080
titre_fenetre='le serpent qui mange des pommes et grandit'

## debug
jeu_actif=True  # le serpent est sur la carte si True
mode_manuel=True    # le joueur doit manuellement faire avancer le temps si True


execution_instantanee=True


taux_risque='0'