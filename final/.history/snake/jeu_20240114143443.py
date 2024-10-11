class  Jeu:
    def  __init__(self,serpent):
        self.serpent=serpent
        self.score=0
        self.nb_images=0
        self.fin_jeu=False
        self.etat_partie=0  # 0: en cours, 1: gagnée, -1: perdu
        self.pomme=None
        self.emplacement_pomme=None
        self.distance_parcourue=0
        self.max_score=None

        self.pomme_atteinte=False