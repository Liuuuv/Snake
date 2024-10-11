nb_cases=4
import random as rd

def voisins_petite_grille(pos):
   liste_voisins=[]
   for j in range(-1,2):
     for i in range(-1,2):
        if i*j==0 and pos[0]+j>=0 and pos[0]+j<=nb_cases//2-1 and pos[1]+i>=0 and pos[1]+i<=nb_cases//2-1 and (i,j)!=(0,0):
liste_voisins.append((pos[0]+j,pos[1]+i))
   return(liste_voisins)

def creer_liste_murs():
   a_traiter=[(0,0)]   # point de départ
   deja_traites=[]
   liste_murs=[]

   while a_traiter!=[]:

     # on choisit au hasard un sommet
     pos=rd.choice(a_traiter)

     liste_voisins=voisins_petite_grille(pos)


     # s'il y a un sommet a regarder dans la liste des voisins, on ne supprime pas le sommet
     supprimer=True
     for voisin in liste_voisins:
        if not voisin in a_traiter and not voisin in deja_traites:
supprimer=False
     if supprimer:
        a_traiter.remove(pos)

     # cas ou on ne supprime pas
     voisin=rd.choice(liste_voisins)
     if not voisin in a_traiter and not voisin in deja_traites:
        liste_murs.append(set((pos,voisin)))
        a_traiter.append(voisin)


     deja_traites.append(pos)

   return liste_murs

L=[]
for _ in range(6):

   liste=creer_liste_murs()
   print(liste)
   if not liste in L:
     L.append(liste)






print(L)
print(len(L))