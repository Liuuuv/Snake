import numpy as np

class Algorithme:
    def generer_chemin_hamiltonien(self) -> None : ...
    def generer_chemin_zig_zag_vertical(self) -> np.ndarray : ...
    def generer_chemin_zig_zag_horizontal(self) -> np.ndarray : ...
    def mettre_a_jour_listes(self) -> None : ...