import numpy as np
import random as rd
import collections
from functools import lru_cache
import time


dimensions=(3,3)
# trop long pour plus de 3

class Arbre:
   def __init__(self,noeud,aretes,deja_traites,enfants):
     self.noeud=noeud
     self.aretes=aretes
     self.deja_traites=deja_traites
     self.enfants=enfants



     if self.enfants!=[]:
        self.longueur=1+self.enfants[0].longueur
        self.affichage=[self.noeud,[enfant.affichage for enfant in self.enfants]]
     else:
        self.longueur=1
        self.affichage=[self.noeud,[]]

   def ajouter(self,arbre):
     self.enfants+=arbre

   def afficher(self):
     # print([self.noeud,[arbre.afficher() for arbre in arbre.enfants]])
     print(self.affichage)

def recuperer_liste_voisins(pos):
   liste_voisins=[]
   for i in range(-1,2):
      for j in range(-1,2):
         if i*j==0 and i!=j and 0<=pos[0]+i<=dimensions[0]-1 and 0<=pos[1]+j<=dimensions[1]-1:
            liste_voisins.append((pos[0]+i,pos[1]+j))
   return liste_voisins



# print(arbre.enfants[0].enfants[0].enfants[1].noeud)

arbre=Arbre((0,0),set(((0,0),(0,0))),[(0,0)],[])

@lru_cache(maxsize = 1000)
def generer_murs(arbre):
   # liste_voisins=[]
   # for voisin in [recuperer_liste_voisins(pos) for pos in arbre.deja_traites]:
   #   if not voisin in liste_voisins and not voisin in arbre.deja_traites+[arbre.noeud]:
   #      liste_voisins.append(voisin)

   # nouvelle_arete=(arbre.noeud,voisin)   # VOISIN

   # if len(arbre.deja_traites)==dimensions[0]*dimensions[1]+1:
   #   return arbre

   liste_aretes=[]
   for pos in arbre.deja_traites:
      for voisin in recuperer_liste_voisins(pos):
         if not voisin in arbre.deja_traites:
            liste_aretes.append((pos,voisin))

   # print(arbre.noeud,liste_aretes,arbre.deja_traites)

   if liste_aretes==[]:
     return arbre

   return Arbre(arbre.noeud,arbre.aretes,arbre.deja_traites,[generer_murs(Arbre(couple[1],set(couple),arbre.deja_traites+[couple[1]],[])) for couple in liste_aretes])

debut=time.time()
arbre=generer_murs(arbre)
fin=time.time()
print("generer: "+str(fin-debut))

print("arbre généré")

def egale(liste1,liste2):
   if len(liste1)!=len(liste2):
     print("pas meme taille")
     return False

   for elem in liste1:
     if not elem in liste2:
        return False

   return True

liste_configurations=[]
def afficher(arbre,liste_murs):
   # liste_murs.append(arbre.aretes)

   if arbre.enfants==[]:
     # print(liste_murs+[arbre.aretes])
     if not liste_murs in liste_configurations:
        liste_configurations.append(liste_murs+[arbre.aretes])
     return
   for enfant in arbre.enfants:
     afficher(enfant,liste_murs+[arbre.aretes])

debut=time.time()
afficher(arbre,[])
fin=time.time()
print("afficher: "+str(fin-debut))
# print(liste_configurations)

# liste_configurations=[[1],[2],[2],[3]]
debut=time.time()
liste_config=[]
for config in liste_configurations:
   ajouter=True
   for config_deja in liste_config:
     if egale(config,config_deja):
        ajouter=False

   if ajouter:
     liste_config.append(config)
fin=time.time()
print("finir: "+str(fin-debut))
# print(liste_config)
print(len(liste_config))






