import numpy as np

def  generer_dico_indices(nb_cases):
        dico_indices={}
        indice=0
        for  i  in  range(nb_cases):
            for  j  in  range(nb_cases):
                dico_indices[indice]=(j,i)
                indice+=1
        return  dico_indices

def dico_noms_canonique(nb_cases):
        dico_noms={}
        numero=0
        for i in range(nb_cases):
            for j in range(nb_cases):
                dico_noms[numero]=(j,i)
                numero+=1

        return dico_noms

def generer_matrice_adjacence(nb_cases,dico_indices):

    matrice=np.zeros((nb_cases**2,nb_cases**2))
    for i in range(nb_cases**2):
        for j in range(nb_cases**2):
            if [dico_indices[j][0],dico_indices[j][1]] in recuperer_liste_voisins(nb_cases,dico_indices[i]):
                matrice[i,j]=1
                matrice[j,i]=1

    return matrice

def recuperer_liste_voisins(nb_cases,pos):
    liste_voisins=[]
    for  j  in  range(-1,2):
        for  i  in  range(-1,2):
            if  i*j==0  and  pos[0]+j>=0  and  pos[0]+j<=nb_cases-1  and  pos[1]+i>=0  and  pos[1]+i<=nb_cases-1  and  (i,j)!=(0,0):
                #  print(i,j)
                liste_voisins.append([pos[0]+j,pos[1]+i])
    return liste_voisins

def generer_matrice(nb_cases,dico_indices,chemin):
    matrice=np.zeros((nb_cases**2,nb_cases**2))
    for  i  in  range(nb_cases**2):
        for  j  in  range(nb_cases**2):
            #  print(self.numero_depuis_pos(self.dico_indices[i]),self.numero_depuis_pos(self.dico_indices[j]))
            #  print(self.dico_indices[i],self.dico_indices[j])
            if  abs(int(numero_depuis_pos(chemin,dico_indices[i]))-int(numero_depuis_pos(chemin,dico_indices[j])))==1:
                matrice[j-1,i-1]=1
                #  matrice[i-1,j-1]=1
                    #  print(matrice)
    return  matrice

def  numero_depuis_pos(chemin,pos):
    #  print(self.chemin[pos[1]][pos[0]])
    return  int(chemin[pos[1],pos[0]])


def  composante_petite_grille(k):    #  renvoie  la  composante  (coordonnées)  de  la  petite  grille  à  partir  d'une  composante  de  la  grande  grille
    if  k%2==0:
        return(k//2)
    else:
        return((k-1)//2)

