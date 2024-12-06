import numpy as np

class Algorithme:
    def generer_chemin_hamiltonien(self) -> None: ...
    def generer_chemin_zig_zag_vertical(self) -> np.ndarray: ...
    def generer_chemin_zig_zag_horizontal(self) -> np.ndarray: ...
    def mettre_a_jour_listes(self) -> None : ...
    def initialiser_chemin_aleatoire(self, liste_murs : list, debut : list, direction_initiale : list) -> np.ndarray: ...
    def voisins_petite_grille(self, pos : list) -> list: ...
    def creer_liste_murs(self, debut : list, pos_petite_grille_a_eviter : list) -> list: ...
    def tracer_murs(self, liste_aretes : list) -> None: ...
    def initialiser_dico_adjacence_oriente(self) -> dict: ...
    def mettre_a_jour_direction(self, nom_fonction : str) -> None: ...
    def generer_deux_facteur(self) -> dict: ...
    def generer_liste_aretes_depuis_dico_adjacence(self, dico_adjacence : dict) -> list: ...
    def souder_deux_facteur(self, dico_adjacence_deux_facteur :  dict) -> None: ...
    
    def raccourcis_croissants_v2(self) -> None: ...
    def raccourcis_croissants_v3(self) -> None: ...
    def raccourcis_croissants_v3(self) -> None: ...
    def a_etoile_projection_queue(self) -> None: ...
    def a_etoile_graphe_oriente(self) -> None: ...
    def a_etoile_graphe_oriente_cout(self) -> None: ...
    def a_etoile_graphe_oriente_hami(self): ...
    
    def pos_direction_compatibles(self, pos : list, direction : list) -> list: ...
    def liste_aretes_petite_grille(self, pos : list, pos_debut : list, direction_initiale : list,liste_pos_petite_grille_occupees : list, pos_petite_grille_traites : list) -> list: ...
    def contour_liste_aretes(self, liste_aretes : list, pos_debut : list, direction_initiale : list): ...
    def arbre_raccourcis_modifier_hami(self) -> None: ...
    def pos_suivante_selon_cycle_hami(self, pos : list, cycle_hami : np.ndarray) -> list: ...
    def peut_prendre_raccourci(self, pos : list, pos_suivante : list, cycle_hami : np.ndarray) -> bool: ...