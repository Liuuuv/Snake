import sympy as sp
import random as rd
import numpy as np

# x=sp.symbols('x')
# y=sp.symbols('y')
# z=sp.symbols('z')

# M = sp.Matrix([
# [ 0.063*x**2,   0.0314*x*y, -0.0001*x*z],
# [ 0.0314*x*y, 96.1659*y**2, -0.0001*y*z],
# [-0.0001*x*z,  -0.0001*y*z, 0.0001*z**2]])
# print(M.det())

nb_cases=2

"""creation matrice_adj et laplacienne"""
def voisins(pos):  # pour avoir la liste des voisins
   liste_voisins=[]
   for i in range(-1,2):
      for j in range(-1,2):
         if i*j==0 and (i,j)!=(0,0) and 0<=pos[0]+i<=nb_cases-1 and 0<=pos[1]+j<=nb_cases-1:
            liste_voisins.append((pos[0]+i,pos[1]+j))

   return liste_voisins

# numerotation des aretes
liste_sommets=[]
for j in range(nb_cases):
   for i in range(nb_cases):
      liste_sommets.append((i,j))




def dico_noms_aleatoire():
   dico_noms={}
   numero=1
   while liste_sommets!=[]:
      pos=rd.choice(liste_sommets)
      dico_noms[numero]=pos
      liste_sommets.remove(pos)
      numero+=1

   return dico_noms


# print(dico_noms)

def dico_noms_canonique():
   dico_noms={}
   numero=1
   for i in range(nb_cases):
      for j in range(nb_cases):
         dico_noms[numero]=(j,i)
         numero+=1

   return dico_noms


# x = [sp.symbols('x%d' % i) for i in range(3)]
# x=sp.symbols('x:5(0:3)')
# x=sp.symbols('x:'+'(1:'+str(nb_cases**2)+')'+'(1:'+str(nb_cases**2)+')')
x=[sp.symbols('x{}{}'.format(i, j)) for i in range(1,nb_cases**2+1) for j in range(1,nb_cases**2+1)]
# print(x)

"""matrice adjacence"""
def matrice_adjacence_grille(dico_noms):
   # M=np.zeros((nb_cases**2,nb_cases**2))
   M=[]

   for i in range(nb_cases**2):
      ligne=[]
      for j in range(nb_cases**2):
         # print(j+1)
         # print(dico_noms[j+1])
         # print()
         if dico_noms[j+1] in voisins(dico_noms[i+1]) or dico_noms[i+1] in voisins(dico_noms[j+1]):
            ligne.append(x[i+j*nb_cases**2])
         else:
            ligne.append(0)
      M.append(ligne)
   # print(M)

   return sp.Matrix(M)

dico_noms=dico_noms_canonique()
M=matrice_adjacence_grille(dico_noms)


print(M.det())
# BEAUCOUP TROP LENT POUR N=4







