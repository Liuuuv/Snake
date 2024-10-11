import numpy as np
import matplotlib.pyplot as plt

nb_cases=3


def voisins(pos):  # pour avoir la liste des voisins
   liste_voisins=[]
   for i in range(-1,2):
      for j in range(-1,2):
         if i*j==0 and (i,j)!=(0,0) and 0<=pos[0]+i<=nb_cases-1 and 0<=pos[1]+j<=nb_cases-1:
            liste_voisins.append((pos[0]+i,pos[1]+j))

   return liste_voisins

# numerotation des aretes
dico_noms={}
numero=1
for j in range(nb_cases):
   for i in range(nb_cases):
     dico_noms[numero]=(j,i)
     numero+=1

matrice_adjacence=np.zeros((nb_cases**2,nb_cases**2))

for i in range(nb_cases**2):
   for j in range(nb_cases**2):
     # print(j+1)
     # print(dico_noms[j+1])
     # print()
     if dico_noms[j+1] in voisins(dico_noms[i+1]) or dico_noms[i+1] in voisins(dico_noms[j+1]):
        matrice_adjacence[i,j]=1

plt.close()

plt.figure()
plt.imshow(matrice_adjacence)
fig=plt.figure()

compteur=1
for i in range(nb_cases):
   for j in range(nb_cases):

     fig.add_subplot(nb_cases,nb_cases,compteur)
     plt.imshow(matrice_adjacence[nb_cases*i:nb_cases*(i+1),nb_cases*j:nb_cases*(j+1)])
     compteur+=1

# creation du laplacien
laplacien=np.negative(np.copy(matrice_adjacence))
for i in range(nb_cases**2):
   compteur=0
   for j in range(nb_cases**2):
     if matrice_adjacence[i,j]==1:
        compteur+=1
   laplacien[i,i]=compteur

print(np.linalg.det(laplacien[:-1,:-1]))
# print(laplacien)

plt.show()




