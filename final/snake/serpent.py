import collections

import numpy as np

class  Serpent:
    def  __init__(self,pos):
        self.pos=pos
        self.pos_queue=collections.deque([])
        self.direction=[0,0]      #  vecteur  (x,y)  ;  [0,1]  est  vers  le  bas
        self.taille_queue=len(self.pos_queue)
        self.en_attente=None    # pour faire grandir le serpent