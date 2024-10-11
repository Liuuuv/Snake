import numpy as np
import matplotlib.pyplot as plt
import random as rd


nb_cases=4

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

"""matrice adjacence"""
def matrice_adjacence_grille(dico_noms):
   M=np.zeros((nb_cases**2,nb_cases**2))

   for i in range(nb_cases**2):
      for j in range(nb_cases**2):
         # print(j+1)
         # print(dico_noms[j+1])
         # print()
         if dico_noms[j+1] in voisins(dico_noms[i+1]) or dico_noms[i+1] in voisins(dico_noms[j+1]):
            M[i,j]=1

   return M



def matrice_adjacence_chemin():
   M=np.zeros((nb_cases**2,nb_cases**2))
   for i in range(nb_cases**2-1):
      M[i,i+1],M[i+1,i]=1,1

   return M



# creation du laplacien
def laplacienne(M):
   L=np.negative(np.copy(M))
   for i in range(nb_cases**2):
      compteur=0
      for j in range(nb_cases**2):
         if M[i,j]==1:
            compteur+=1
      L[i,i]=compteur

   return L

def matrice_adjacence_cycle(cycle,dico_noms):
   nombre=1
   C=np.zeros((nb_cases**2,nb_cases**2))
   for i in range(nb_cases**2):
      for j in range(nb_cases**2):
         if dico_noms[i+1] in cycle and dico_noms[j+1] in cycle:
            # print(abs(cycle.index(dico_noms[i+1])-cycle.index(dico_noms[j+1])),(i,j))
            if cycle[0]==dico_noms[i+1] and cycle[-1]==dico_noms[j+1]:
               C[i,j]=nombre
            elif cycle[0]==dico_noms[j+1] and cycle[-1]==dico_noms[i+1]:
               C[i,j]=nombre
            elif abs(cycle.index(dico_noms[i+1])-cycle.index(dico_noms[j+1]))==1:
               C[i,j]=nombre

   return C

# dico_noms1={1: (1, 2), 2: (0, 2), 3: (2, 1), 4: (0, 1), 5: (2, 2), 6: (1, 0), 7: (0, 0), 8: (1, 1), 9: (2, 0)}
# dico_noms2={1: (1, 0), 2: (0, 1), 3: (0, 2), 4: (2, 2), 5: (1, 1), 6: (2, 1), 7: (0, 0), 8: (1, 2), 9: (2, 0)}
# M=matrice_adjacence_grille(dico_noms1)

# dico_noms=dico_noms_aleatoire()
dico_noms=dico_noms_canonique()
# dico_noms={1: (2, 3), 2: (3, 0), 3: (3, 2), 4: (1, 2), 5: (2, 1), 6: (1, 1), 7: (3, 3), 8: (0, 1), 9: (2, 2), 10: (0, 2), 11: (0, 3), 12: (1, 3), 13: (3, 1), 14: (1, 0), 15: (0, 0), 16: (2, 0)}

M=matrice_adjacence_grille(dico_noms)

# k=nb_cases**2
# N=np.identity(nb_cases**2)
# for _ in range(k):
#    N=np.matmul(N,M)
# M=N
# print(M)

# M_chemin=matrice_adjacence_chemin()

# (2,2)
cycle=[(0,0),(1,0),(1,1),(0,1)]

# (3,3)
cycle=[(0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,1)]


# C=matrice_adjacence_cycle(cycle,dico_noms)

# print(C)

# M=np.ones((nb_cases**2,nb_cases**2))
# for i in range(nb_cases**2):
#   M[i,i]=0

# print(M)

# L=laplacienne(M)



"""calcul du signal"""
spectre=np.real(np.linalg.eigvals(M))
# print(np.round(spectre,2))
liste_temps=np.linspace(0,10,600)

def f(t):
   return sum([np.cos(lam*t) for lam in spectre if lam>=0])
liste_y=[f(t) for t in liste_temps]

"""plot"""
plt.close()

def plot_signal():
   plt.figure()
   plt.plot(liste_temps,liste_y)

def plot_matrice(M):
   plt.figure()
   plt.imshow(M)


def plot_decomposition_matrice(M):
   compteur=1
   fig=plt.figure()
   for i in range(nb_cases):
      for j in range(nb_cases):

         fig.add_subplot(nb_cases,nb_cases,compteur)
         plt.imshow(M[nb_cases*i:nb_cases*(i+1),nb_cases*j:nb_cases*(j+1)])
         compteur+=1


# plt.clf()

# plot_signal()
# plot_matrice(M)





def puissance(M,k):
   N=np.identity(len(M))
   for _ in range(k):
      N=np.matmul(N,M)
   return N

def elements_propres(M):
   liste_val_propres,matrice_vec_propres=np.linalg.eig(M)

   liste_val_propres=liste_val_propres.tolist()
   liste_vec_propres=[matrice_vec_propres[:,i].tolist() for i in range(len(liste_val_propres))]


   nb_decimales=3
   liste_val_propres=arrondir_liste(liste_val_propres,nb_decimales)
   liste_vec_propres=[arrondir_liste(vec,nb_decimales) for vec in liste_vec_propres]

   # print(len(liste_val_propres))
   # print(len(liste_vec_propres))

   return liste_val_propres,liste_vec_propres




def arrondir_liste(liste,nb_decimales):
   return [arrondir(elem,round(elem.real,nb_decimales)+j*round(elem.imag,nb_decimales),10**(-nb_decimales)) for elem in liste]


def arrondir(nombre,reference,tolerance):
   # print(nombre,reference)
   if nombre.imag==0:
      if abs(nombre-reference)<tolerance:
         return reference
      else: return round(nombre,5)
   else:
      if abs(nombre.real-reference.real)<tolerance and abs(nombre.imag-reference.imag)<tolerance:
         return reference
      else: return round(nombre.real,5)+j*round(nombre.imag,5)



def avoir_poly_cara(M: np.ndarray):
   return np.polynomial.Polynomial.fromroots(np.linalg.eigvals(M))

def avoir_poly_minimal(M):
   return np.polynomial.Polynomial.fromroots(list(set(arrondir_liste(np.linalg.eigvals(M),5))))


def arrondir_coef_polyome(polynome,nb_decimales):
   liste_coefs=polynome.coef
   return np.polynomial.Polynomial(arrondir_liste(liste_coefs,nb_decimales))




liste_val_propres,liste_vec_propres=elements_propres(M)
# liste_val_propres.sort()

print("valeurs propres de M:",liste_val_propres)
print([2*np.cos(k*np.pi/(nb_cases+1))+2*np.cos(l*np.pi/(nb_cases+1)) for k in range(1,nb_cases+1) for l in range(1,nb_cases+1)])
# # print("vecteurs propres de M:",liste_vec_propres)
# print()

# liste_val_propres,liste_vec_propres=elements_propres(M_chemin)
# liste_val_propres.sort()

# print("valeurs propres de M_chemin:",liste_val_propres)
# # print("vecteurs propres de M_chemin:",liste_vec_propres)
# print()


# poly_cara_M=avoir_poly_cara(M)
# poly_cara_M=arrondir_coef_polyome(poly_cara_M,3)

# print("poly cara de M:",poly_cara_M)
# print()

# poly_cara_M_chemin=avoir_poly_cara(M_chemin)
# poly_cara_M_chemin=arrondir_coef_polyome(poly_cara_M_chemin,3)


# print("poly cara de M_chemin:",poly_cara_M_chemin)
# print()

# # print(avoir_poly_cara(C))

# poly_minimal_M=avoir_poly_minimal(M)
# poly_minimal_M=arrondir_coef_polyome(poly_minimal_M,3)
# print("poly minimal de M:",poly_minimal_M)
# print()

# liste_coefs_M=[coef for coef in liste_coefs_M]
# liste_coefs_M=arrondir_liste(liste_coefs_M,3)
# liste_coefs_M=[coef%(nb_cases**2) for coef in liste_coefs_M]
#
# poly_cara_modulo=np.polynomial.Polynomial(liste_coefs_M)
# print()

# print("poly cara modulo",nb_cases**2,":",poly_cara_modulo)

# plot_matrice(C)
# plot_matrice(M)
# plot_decomposition_matrice(M)


plt.show()


""" les valeurs propres des matrices d'adjacences et laplaciennes sont invariantes par réindicage du graphe"""
"""la matrice d'adjacence d'un graphe grille carré sans trou G (n^2,n^2) est le produit cartésien de deux graphes chemins, ça se voit dans la tete de la matrice d'adjacence de G dans indicage canonique: quand on regroupe par blocs de n^2 matrices de taille (n,n): on voit des blocs B et des I_n, les B sont des mat d'adj de chemins et la disposition des I_n fait penser à la mat d'adj de graphe chemin"""

# regarder poly cara dans Z/mZ, m dans N
# regarder correspondance chemin x chemin = grille
# regarder graphes de matrices adj mineurs principaux car ils determinent entierement les coef du poly cara
