import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import collections
import time

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

def graphe_transforme(nb_cases):
    graphe=nx.Graph()

    deja_traites=[]

    for x in range(nb_cases):
        for y in range(nb_cases):
            graphe.add_node((str(x),str(y)))
            liste_voisins=recuperer_liste_voisins(nb_cases,(x,y))

            for voisin in liste_voisins:
                if not ((str(voisin[0]),str(voisin[1])),(str(x),str(y))) in deja_traites:    # inutile
                    graphe.add_node((str(x)+str(voisin[0])+str('\''),str(y)+str(voisin[1])+str('\'')))  # x'
                    graphe.add_node((str(voisin[0])+str(x)+str('\''),str(voisin[1])+str(y)+str('\'')))  # y'
                
                    graphe.add_edge(
                        (str(x),str(y)),
                        (str(x)+str(voisin[0])+str('\''),str(y)+str(voisin[1])+str('\''))
                        )
                    graphe.add_edge(
                        (str(voisin[0]),str(voisin[1])),
                        (str(voisin[0])+str(x)+str('\''),str(voisin[1])+str(y)+str('\''))
                        )
                    
                    graphe.add_edge(
                        (str(x)+str(voisin[0])+str('\''),str(y)+str(voisin[1])+str('\'')),
                        (str(voisin[0])+str(x)+str('\''),str(voisin[1])+str(y)+str('\''))
                        )
            deja_traites.append(((str(x),str(y)),(str(voisin[0]),str(voisin[1]))))
                    
    for x in range(nb_cases):
        for y in range(nb_cases):
            graphe.add_node((str(x)+str('\'\''),str(y)+str('\'\'')))    # x''

            aretes_a_ajouter=[]
            for voisin in nx.neighbors(graphe,(str(x),str(y))):
                # print((str(x),str(y)),(str(voisin[0]),str(voisin[1])))
                aretes_a_ajouter.append((
                    (str(x)+str('\'\''),str(y)+str('\'\'')),
                    (str(voisin[0]),str(voisin[1]))
                    ))
            for arete in aretes_a_ajouter:
                e1,e2=arete
                graphe.add_edge(e1,e2)

            
    
    return graphe


# nx.draw(graphe,node_size=20,with_labels=True)
def avoir_couplage_parfait(graphe_,liste_sommets_a_enlever=None):
    if liste_sommets_a_enlever is not None:
        # graphe=graphe_.copy()
        graphe=graphe_
        graphe.remove_nodes_from(liste_sommets_a_enlever)

    # couplage=nx.maximal_matching(graphe)
    couplage=[list(graphe.edges)[0]]

    # print(nx.is_perfect_matching(graphe,couplage))
    # liste_sommets_departs_traites=[]
    
    while not nx.is_perfect_matching(graphe,couplage):

        # print(couplage)

        # init de liste sommets du couplage
        liste_sommets_couplage=[]
        for couple in couplage:
        #     print(couple)
            v1,v2=couple
            
            if not v1 in liste_sommets_couplage:
                liste_sommets_couplage.append(v1)
            if not v2 in liste_sommets_couplage:
                liste_sommets_couplage.append(v2)

        # print(longueur_couplage)
        # print(couplage)
        
        # print(liste_sommets_couplage)
        
        # on cherche sommet libre
        sommet_depart=None
        for sommet in graphe.nodes():
            # if not sommet in liste_sommets_couplage and not sommet in liste_sommets_departs_traites:
            if not sommet in liste_sommets_couplage:
                sommet_depart=sommet
                break
        if sommet_depart is None:
            return False
        # print(sommet_depart,liste_sommets_departs_traites,sommet_depart in liste_sommets_departs_traites)

        # parcours largeur
        a_traiter=collections.deque([sommet_depart])
        deja_traites=[]
        vide=collections.deque([])

        heure_debut=time.time()
        dico_parents={}
        sommet_final=None
        while a_traiter!=vide:
            sommet=a_traiter.popleft()

            # condition d'arret
            if sommet not in liste_sommets_couplage and sommet!=sommet_depart:
                sommet_final=sommet
                break

            # on continue
            else:
                deja_traites.append(sommet)
                for sommet_voisin in graphe.neighbors(sommet):

                    # pas au debut du parcours
                    if sommet!=sommet_depart:
                        if sommet_voisin not in deja_traites and sommet_voisin not in a_traiter:

                            if (dico_parents[sommet],sommet) in couplage or (sommet,dico_parents[sommet]) in couplage:
                                if (sommet,sommet_voisin) not in couplage and (sommet_voisin,sommet) not in couplage:
                                    a_traiter.append(sommet_voisin)
                                    dico_parents[sommet_voisin]=sommet
                            
                            else:
                                if (sommet,sommet_voisin) in couplage or (sommet_voisin,sommet) in couplage:
                                    a_traiter.append(sommet_voisin)
                                    dico_parents[sommet_voisin]=sommet
                    
                    # au debut du parcours
                    else:
                        a_traiter.append(sommet_voisin)
                        dico_parents[sommet_voisin]=sommet
        print('couplage >>> parcours',time.time()-heure_debut)

        if sommet_final is None:
            # print('pas de sommet final')
            continue

        # heure_debut=time.time()
        # chemin
        chemin=[]
        sommet=sommet_final
        while sommet in dico_parents.keys():
            chemin.append(sommet)
            sommet=dico_parents[sommet]
        chemin.append(sommet_depart)

        chemin.reverse()


        # print(chemin)

        nouveau_couplage=[]

        for i in range(len(chemin)-1):
            if i%2==0:
                nouveau_couplage.append((chemin[i],chemin[i+1]))
        
        for couple in couplage:
            v1,v2=couple
            if not v1 in chemin and not v2 in chemin:
                nouveau_couplage.append(couple)


        nouveau_couplage=set(nouveau_couplage)

        # print('couplage >>> nouveau_couplage',time.time()-heure_debut)
        couplage=nouveau_couplage
        

        # print(nouveau_couplage)
    
    


    # dico_aretes={arete:'XXXXX' for arete in couplage}

    # pos = nx.spring_layout(graphe, iterations=50)

    # nx.draw(graphe,pos,node_size=20,with_labels=True)
    # nx.draw_networkx_edge_labels(graphe,pos,edge_labels=dico_aretes,font_color='red')
    



    # nx.draw_networkx_edges(graphe, pos,)
    # nx.draw_networkx_nodes(graphe, pos, node_size=10, node_color='r')
    # nx.draw_networkx_labels(graphe,pos)



    

    # plt.show()

    return couplage

def deuxfacteur(nb_cases,couplage):
    aretes_interdites=[]
    for couple in couplage:
        sommet1,sommet2=couple   # sommet est un tuple
        n11,n12=sommet1
        n21,n22=sommet2
        n11=n11.replace('\'','')
        n12=n12.replace('\'','')
        n21=n21.replace('\'','')
        n22=n22.replace('\'','')
        if len(n11)==2 and len(n12)==2 and len(n21)==2 and len(n22)==2:
            # print(n11,n12,n21,n22)
            aretes_interdites.append(((int(n11[0]),int(n12[0])),(int(n21[0]),int(n22[0]))))
    
    # print(aretes_interdites)

    dico_adjacence={}
    for x in range(nb_cases):
        for y in range(nb_cases):

            liste_voisins_grille=recuperer_liste_voisins(nb_cases,(x,y))
            
            for voisin in liste_voisins_grille:
                tuple_voisin=(voisin[0],voisin[1])
                tuple_pos=(x,y)
                if not (tuple_pos,tuple_voisin) in aretes_interdites and not (tuple_voisin,tuple_pos) in aretes_interdites:
                    if not (x,y) in dico_adjacence.keys():
                        dico_adjacence[(x,y)]=[]
                    dico_adjacence[(x,y)].append(tuple_voisin)

    

    

    return dico_adjacence




# nb_cases=10
# graphe=graphe_transforme(nb_cases)
# couplage_parfait=avoir_couplage_parfait(graphe)

# if not couplage_parfait:
#     print('no')

# dico_adjacence=deuxfacteur(nb_cases,couplage_parfait)
# graphe_=nx.from_dict_of_lists(dico_adjacence)


# nx.draw(graphe_,node_size=10,with_labels=True)
# plt.show()