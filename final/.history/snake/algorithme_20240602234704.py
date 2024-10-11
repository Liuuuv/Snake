import collections
import numpy as np
import random as rd
import pygame as py
import copy
import time
import matplotlib.pyplot as plt
import networkx as nx


from couleurs import*
import outils as outils

inf=float('inf')


class  Algorithme:
    def  __init__(self,affichage,jeu):
        self.affichage=affichage
        self.jeu=jeu
        #  self.chemin=[[0  for  _  in  range(self.affichage.nb_cases)]  for  _  in  range(self.affichage.nb_cases)]
        #  self.compteur=0
        #  self.last=False

        self.lock=False
        self.aller_sur_pomme=False


        self.liste_scores=[]
        self.liste_pas=[]

        self.dico_indices={}
        self.matrice=[]

        self.plus_court_chemin=[]
        self.plus_court_chemin_=[]

        self.plus_court_chemin_hor=[]
        self.plus_court_chemin_ver=[]


        self.pos_boucle_1=[]
        self.pos_boucle_2=[]

        self.chemin_optimal=[]


        # pour parcours cellules
        self.liste_pos_traitees=[]
        self.dico_arbre={}

        


        self.liste_murs=[]
        self.liste_aretes_deux_facteur=[]


        self.voisins=lambda pos:outils.recuperer_liste_voisins(self.affichage.nb_cases,pos)





        # self.chemin=self.generer_chemin_zig_zag_vertical()


        #  self.type_chemin="zig  zag  vertical"
        #  self.chemin=self.generer_chemin_zig_zag_horizontal()
        #  self.type_chemin="zig  zag  horizontal"


        self.generer_chemin_hamiltonien()



        self.chemin_zig_zag_horizontal=self.generer_chemin_zig_zag_horizontal()
        self.chemin_zig_zag_vertical=self.generer_chemin_zig_zag_vertical()




        self.nouveau_chemin=np.copy(self.chemin)

        self.dico_indices=outils.generer_dico_indices(self.affichage.nb_cases)
        self.matrice=outils.generer_matrice(self.affichage.nb_cases,self.dico_indices,self.chemin)

        self.dico_adjacence_oriente=self.initialiser_dico_adjacence_oriente()

        


        # self.numero_depuis_pos=lambda pos:outils.numero_depuis_pos(self.chemin,pos)

        # print(self.dico_adjacence_oriente)



        # self.dico_noms=outils.dico_noms_canonique(self.affichage.nb_cases)
        # self.matrice_adjacence=self.generer_matrice_adjacence()



        #  self.chemin=[
        #  [0,1,4,5,8,9,12,13],
        #  [63,2,3,6,7,10,11,14],
        #  [62,51,50,39,38,27,26,15],
        #  [61,52,49,40,37,28,25,16],
        #  [60,53,48,41,36,29,24,17],
        #  [59,54,47,42,35,30,23,18],
        #  [58,55,46,43,34,31,22,19],
        #  [57,56,45,44,33,32,21,20],
        #  ]







    def  generer_chemin_hamiltonien(self):
        self.liste_murs=self.creer_liste_murs([0,0],[])

        ajouter=[]
        for  couple  in  self.liste_murs:
            ajouter.append([couple[1][:],couple[0][:]])

        self.liste_murs+=ajouter

        self.chemin=self.initialiser_chemin_aleatoire(self.liste_murs,[0,0],[1,0])

    def  generer_chemin_zig_zag_vertical(self):
        assert  self.affichage.nb_cases%2==0

        chemin=np.zeros((self.affichage.nb_cases,self.affichage.nb_cases),dtype=np.uint)

        pos=[0,0]
        compteur=0
        direction=[0,1]
        while  compteur<self.affichage.nb_cases**2:
            if  pos[1]==self.affichage.nb_cases-1:
                if  direction==[0,1]:
                    direction=[1,0]
                elif  direction==[1,0]:
                    direction=[0,-1]
            if  pos[1]==1:
                if  direction==[0,-1]:
                    direction=[1,0]
                elif  direction==[1,0]:
                    direction=[0,1]

            if  pos[0]==self.affichage.nb_cases-1:
                if  direction==[1,0]:
                    direction=[0,-1]
                elif  pos[1]==0:
                    direction=[-1,0]

            chemin[pos[1],pos[0]]=compteur
            compteur+=1
            pos[0]+=direction[0]
            pos[1]+=direction[1]

        return  chemin
        #  print(chemin)

    def  generer_chemin_zig_zag_horizontal(self):
        assert  self.affichage.nb_cases%2==0

        chemin=np.zeros((self.affichage.nb_cases,self.affichage.nb_cases),dtype=np.uint)

        pos=[0,0]
        compteur=0
        direction=[1,0]
        while  compteur<self.affichage.nb_cases**2:
            if  pos[0]==self.affichage.nb_cases-1:
                if  direction==[1,0]:
                    direction=[0,1]
                elif  direction==[0,1]:
                    direction=[-1,0]
            if  pos[0]==1:
                if  direction==[-1,0]:
                    direction=[0,1]
                elif  direction==[0,1]:
                    direction=[1,0]

            if  pos[1]==self.affichage.nb_cases-1:
                if  direction==[0,1]:
                    direction=[-1,0]
                elif  pos[0]==0:
                    direction=[0,-1]

            chemin[pos[1],pos[0]]=compteur
            compteur+=1
            pos[0]+=direction[0]
            pos[1]+=direction[1]

        return  chemin
        #  print(chemin)


    def  mettre_a_jour_listes(self):      #  pour  avoir  donnees
        self.liste_scores.append(self.jeu.score)
        if  self.jeu.score==0:
            self.liste_pas.append(self.jeu.distance_parcourue)
        else:
            self.liste_pas.append(self.jeu.distance_parcourue-sum(self.liste_pas))
            #  print(self.liste_pas,self.jeu.distance_parcourue)

    #  def  mettre_a_jour_matrice_adjacence(self):
    #      for  i  in  range(self.affichage.nb_cases):
    #          for  j  in  range(self.affichage.nb_cases):
    #              if
    #              self.matrice_adjacence[i,j]




    def  initialiser_chemin_aleatoire(self,liste_murs,debut,direction_initiale):
        # chemin=np.array([[0  for  _  in  range(self.affichage.nb_cases)]  for  _  in  range(self.affichage.nb_cases)])
        chemin=np.zeros((self.affichage.nb_cases,self.affichage.nb_cases))

        n=self.affichage.nb_cases//2

        pos=debut
        compteur=0
        direction=direction_initiale[:]
        # while  compteur<=4*n**2-2:
        while compteur<self.affichage.nb_cases**2-1:
            # print(compteur)

            pos_n=[outils.composante_petite_grille(pos[0]),outils.composante_petite_grille(pos[1])]
            if  direction==[1,0]:    #  j  pair
                if  pos[0]%2==0:
                    if  pos_n[1]-1>=0  and  [pos_n,[pos_n[0],pos_n[1]-1]]  in  liste_murs:
                        direction=[0,-1]
                elif  pos_n[0]+1>n-1  or  not  [pos_n,[pos_n[0]+1,pos_n[1]]]  in  liste_murs:
                    direction=[0,1]

            elif  direction==[-1,0]:      #  j  impair
                if    pos[0]%2==1:
                    if  [pos_n,[pos_n[0],pos_n[1]+1]]  in  liste_murs:
                        direction=[0,1]
                elif  pos_n[0]-1<0  or  not  [pos_n,[pos_n[0]-1,pos_n[1]]]  in  liste_murs:
                    direction=[0,-1]

            elif  direction==[0,1]:    #  i  impair
                if  pos[1]%2==0:
                    if  pos_n[0]+1<=n-1  and  [pos_n,[pos_n[0]+1,pos_n[1]]]  in  liste_murs:
                        direction=[1,0]
                elif  pos_n[1]+1>n-1  or  not  [pos_n,[pos_n[0],pos_n[1]+1]]  in  liste_murs:
                    direction=[-1,0]

            elif  direction==[0,-1]:    #  i  pair
                if  pos[1]%2==1:
                    if  [pos_n,[pos_n[0]-1,pos_n[1]]]  in  liste_murs:
                        direction=[-1,0]
                elif  pos_n[1]-1<0  or  not  [pos_n,[pos_n[0],pos_n[1]-1]]  in  liste_murs:
                    direction=[1,0]



            pos[0]+=direction[0]
            pos[1]+=direction[1]

            #  print(pos,  direction)
            compteur+=1
            chemin[pos[1]][pos[0]]=compteur

        return chemin

    def  voisins_petite_grille(self,pos):
        liste_voisins=[]
        for  j  in  range(-1,2):
            for  i  in  range(-1,2):
                if  i*j==0  and  pos[0]+j>=0  and  pos[0]+j<=self.affichage.nb_cases//2-1  and  pos[1]+i>=0  and  pos[1]+i<=self.affichage.nb_cases//2-1  and  (i,j)!=(0,0):
                    #  print(i,j)
                    liste_voisins.append([pos[0]+j,pos[1]+i])
        return liste_voisins


    def  creer_liste_murs(self,debut,pos_petite_grille_a_eviter):
        a_traiter=[debut[:]]    #  point  de  départ
        deja_traites=[]
        liste_murs=[]

        while  a_traiter!=[]:
            

            #  on  choisit  au  hasard  un  sommet
            pos=rd.choice(a_traiter)

            liste_voisins=self.voisins_petite_grille(pos)


            #  s'il  y  a  un  sommet  a  regarder  dans  la  liste  des  voisins,  on  ne  supprime  pas  le  sommet
            supprimer=True
            for  voisin  in  liste_voisins:
                if  not  voisin  in  a_traiter  and  not  voisin  in  deja_traites and not voisin in pos_petite_grille_a_eviter:
                    supprimer=False
            if  supprimer:
                a_traiter.remove(pos)

            #  cas  ou  on  ne  supprime  pas
            voisin=rd.choice(liste_voisins)
            if  not  voisin  in  a_traiter  and  not  voisin  in  deja_traites and not voisin in pos_petite_grille_a_eviter:
                liste_murs.append([pos[:],voisin[:]])
                a_traiter.append(voisin[:])


            deja_traites.append(pos[:])

        return  liste_murs


    

    #  def  tracer(self):
    #      for  i  in  range(len(self.liste_tracer)-1):
    #          py.draw.line(self.affichage.fenetre,noir,self.liste_tracer[i],self.liste_tracer[i+1])

    def  tracer_murs(self,liste_aretes):
        coef=self.affichage.taille_case*2
        offset=(self.affichage.taille_case,self.affichage.taille_case)
        for  couple  in  liste_aretes:
            py.draw.line(self.affichage.fenetre,noir,[offset[0]+couple[0][0]*coef,offset[1]+couple[0][1]*coef],[offset[0]+couple[1][0]*coef,offset[1]+couple[1][1]*coef],2)

    def initialiser_dico_adjacence_oriente(self):
        dico={}
        for j in range(self.affichage.nb_cases):
            for i in range(self.affichage.nb_cases):
                dico[(j,i)]=[]
                if j%2==0:
                    if i+1<=self.affichage.nb_cases-1:
                        dico[(j,i)].append([j,i+1])
                else:
                    if 0<=i-1:
                        dico[(j,i)].append([j,i-1])
                
                if i%2==0:
                    if 0<=j-1:
                        dico[(j,i)].append([j-1,i])
                else:
                    if j+1<=self.affichage.nb_cases-1:
                        dico[(j,i)].append([j+1,i])
        
        return dico


    def mettre_a_jour_direction(self,nom_fonction):
        fonction=getattr(Algorithme,nom_fonction)
        fonction(self)
    
    def generer_deux_facteur(self):     # des deux facteurs peuvent etre inclus dans le cors du serpent ou dans la boucle que forme le corps
        heure_debut=time.time()
        graphe_transforme=outils.graphe_transforme(self.affichage.nb_cases)
        print('graphe_transforme',time.time()-heure_debut)
        
        heure_debut=time.time()
        # on dit les aretes qui seront deja couplés dans le transforme, i.e. les aretes du deux facteurs qu'on ne veut pas avoir
        liste_sommets_a_enlever=[]
        aretes_a_rajouter=set()
        for i in range(len(self.jeu.serpent.pos_queue)):
            pos1=self.jeu.serpent.pos_queue[i]
            liste_voisins=self.voisins(pos1)

            for voisin in liste_voisins:
                if i<len(self.jeu.serpent.pos_queue)-1 and voisin==self.jeu.serpent.pos_queue[i+1]:
                    continue
                if i>0 and voisin==self.jeu.serpent.pos_queue[i-1]:
                    continue
                if voisin==self.jeu.serpent.pos and i==len(self.jeu.serpent.pos_queue)-1:
                    continue
                if i==0:
                    continue
                pos2=voisin[:]
                # liste_sommets_a_enlever.append(
                #     (str(pos1[0])+str(pos2[0])+str('\''),str(pos1[1])+str(pos2[1])+str('\''))
                #     )
                # liste_sommets_a_enlever.append(
                #     (str(pos2[0])+str(pos1[0])+str('\''),str(pos2[1])+str(pos1[1])+str('\''))
                # )
                liste_sommets_a_enlever.append(
                    (f"{pos1[0]},{pos2[0]}\'",f"{pos1[1]},{pos2[1]}\'")
                    )
                liste_sommets_a_enlever.append(
                    (f"{pos2[0]},{pos1[0]}\'",f"{pos2[1]},{pos1[1]}\'")
                )

                # aretes_a_rajouter.add((
                #     (str(pos1[0])+str(pos2[0])+str('\''),str(pos1[1])+str(pos2[1])+str('\'')),
                #     (str(pos2[0])+str(pos1[0])+str('\''),str(pos2[1])+str(pos1[1])+str('\''))
                # ))
                aretes_a_rajouter.add((
                    (f"{pos1[0]},{pos2[0]}\'",f"{pos1[1]},{pos2[1]}\'"),
                    (f"{pos2[0]},{pos1[0]}\'",f"{pos2[1]},{pos1[1]}\'")
                ))
        print('liste_sommets_a_enlever',time.time()-heure_debut)

        # pre_couplage=set(pre_couplage)
        # print('a enlever',liste_sommets_a_enlever)

        heure_debut=time.time()
        couplage_parfait=outils.avoir_couplage_parfait(graphe_transforme,liste_sommets_a_enlever=liste_sommets_a_enlever)
        print('couplage_parfait',time.time()-heure_debut)


        if not couplage_parfait:
            # print('couplage non parfait')
            return {}
        for arete in aretes_a_rajouter:
            couplage_parfait.add(arete)
        
        heure_debut=time.time()
        dico_adjacence=outils.deuxfacteur(self.affichage.nb_cases,couplage_parfait)
        print('dico_adjacence',time.time()-heure_debut)

        return dico_adjacence
    
    def generer_liste_aretes_depuis_dico_adjacence(self,dico_adjacence):
        heure_debut=time.time()
        liste_aretes=[]
        for pos in dico_adjacence.keys():
            for voisin in dico_adjacence[pos]:
                if not (voisin,pos) in liste_aretes:
                    liste_aretes.append((
                        ((pos[0]+0.5)*self.affichage.taille_case,(pos[1]+0.5)*self.affichage.taille_case),
                        ((voisin[0]+0.5)*self.affichage.taille_case,(voisin[1]+0.5)*self.affichage.taille_case)
                        ))
        print('aretes depuis dico_adjacence',time.time()-heure_debut)
        
        return liste_aretes

    def souder_deux_facteur(self,dico_adjacence_deux_facteur):
        ensemble_boucles=self.ensemble_boucles_depuis_dico_adjacence(dico_adjacence_deux_facteur)
        if not self.modifier_cycle(ensemble_boucles):
            # print('2-facteur non modifiable')
            self.affichage.liste_aretes_cycle

        # print('chemin',self.chemin)




    #  def  mettre_a_jour_direction(self):
    #      self.a_etoile(self.jeu.pomme.pos,[])
    #      if  self.chemin[self.jeu.serpent.pos[1]][self.jeu.serpent.pos[0]]<self.jeu.pomme.numero:
    #          if  self.raccourci_croissant():
    #              self.modifier_cycle()
    #              pass
    #          else:
    #              self.suivre_chemin()
    #      elif  self.chemin[self.jeu.serpent.pos[1]][self.jeu.serpent.pos[0]]>self.jeu.pomme.numero:
    #          if  self.reprendre_cycle():
    #              self.modifier_cycle()
    #              pass
    #          elif  self.aller_vers_0():
    #              self.modifier_cycle()
    #              pass
    #          else:
    #              self.suivre_chemin()
    #      else:
    #          self.suivre_chemin()





    """raccourci  croissant  avec  modif"""  #  ok  sauf  que  modifier_cycle  est  cassée
    # def  mettre_a_jour_direction(self):
    #     if  self.numero_depuis_pos(self.jeu.serpent.pos)<self.jeu.pomme.numero:
    #         if  self.raccourci_croissant():
    #             #  self.modifier_cycle()

    #             pass
    #         else:
    #             self.suivre_chemin()
    #     else:
    #         self.suivre_chemin()
    #     #  else:
    #     #      if  self.aller_vers_0():
    #     #          #  self.modifier_cycle()
    #     #          pass
    #     #      else:
    #     #          self.suivre_chemin()




    """raccourci  croissant  dans  tous  les  cas  (v2  de  raccourci  croissant  seulement)"""  #  ok
    def raccourcis_croissants_v2(self):


        # # pour optimiser
        # if  self.jeu.score>=9*(self.affichage.nb_cases**2)//20:
        #     self.suivre_chemin()
        #     return


        

        self.soustraire(self.numero_depuis_pos(self.jeu.serpent.pos))


        liste_voisins=[voisin  for  voisin  in  self.voisins(self.jeu.serpent.pos)  if  voisin  not  in  self.jeu.serpent.pos_queue]

        liste_pos_suivantes_potentielles=[]
        for  voisin  in  liste_voisins:


            numero_voisin=self.numero_depuis_pos(voisin)

            # si on avance en croissant vers la queue, en prennant raccourci: il y en aura un ou deux
            if  1<=numero_voisin<=self.jeu.pomme.numero:

                if self.jeu.pomme.numero-numero_voisin>=self.jeu.serpent.taille_queue-self.affichage.taux_risque:
                    liste_pos_suivantes_potentielles.append(voisin)
            
            # print(self.peut_prendre_raccourci(pos=self.jeu.serpent.pos,
            #                               pos_suivante=voisin,
            #                               cycle_hami=self.chemin))
        

        

        if  liste_pos_suivantes_potentielles==[]:
            self.suivre_chemin()
            # print('faux')
        else:
            # print('vrai')

            voisin_objectif=max(liste_pos_suivantes_potentielles,key=self.numero_depuis_pos)

            self.jeu.serpent.direction[0]=voisin_objectif[0]-self.jeu.serpent.pos[0]
            self.jeu.serpent.direction[1]=voisin_objectif[1]-self.jeu.serpent.pos[1]
        
        # print()
    

    """raccourci  croissant  dans  tous  les  cas, on considere la queue"""
    def raccourcis_croissants_v3(self): # faire qu'on peut inverser la numerotation


        # # pour optimiser
        # if  self.jeu.score>=9*(self.affichage.nb_cases**2)//20:
        #     self.suivre_chemin()
        #     return


        

        self.soustraire(self.numero_depuis_pos(self.jeu.serpent.pos))

        marge_a_prendre=self.jeu.serpent.taille_queue+1


        liste_voisins=[voisin  for  voisin  in  self.voisins(self.jeu.serpent.pos)  if  voisin  not  in  self.jeu.serpent.pos_queue]

        liste_pos_suivantes_potentielles=[]
        for  voisin  in  liste_voisins:

            ok=True


            numero_voisin=self.numero_depuis_pos(voisin)
            if numero_voisin==self.affichage.nb_cases**2-1:
                continue
                
            if marge_a_prendre+numero_voisin-1>self.jeu.pomme.numero:
                continue
            
            # si on n'a pas la place
            for pos_queue in self.jeu.serpent.pos_queue:
                if marge_a_prendre+numero_voisin-1>self.numero_depuis_pos(pos_queue):
                    ok=False
                    break
            
            if ok:
                liste_pos_suivantes_potentielles.append(voisin)
            
        

        

        if  liste_pos_suivantes_potentielles==[]:
            self.suivre_chemin()
            # print('faux')
        else:
            # print('vrai')

            voisin_objectif=max(liste_pos_suivantes_potentielles,key=self.numero_depuis_pos)

            self.jeu.serpent.direction[0]=voisin_objectif[0]-self.jeu.serpent.pos[0]
            self.jeu.serpent.direction[1]=voisin_objectif[1]-self.jeu.serpent.pos[1]
        
        # print()
    
    """raccourci  croissant  dans  tous  les  cas osef"""
    def raccourcis_croissants_v3(self): # faire qu'on peut inverser la numerotation


        # # pour optimiser
        # if  self.jeu.score>=9*(self.affichage.nb_cases**2)//20:
        #     self.suivre_chemin()
        #     return


        

        self.soustraire(self.numero_depuis_pos(self.jeu.serpent.pos))



        liste_voisins=[voisin  for  voisin  in  self.voisins(self.jeu.serpent.pos)  if  voisin  not  in  self.jeu.serpent.pos_queue]

        liste_pos_suivantes_potentielles=[]
        for  voisin  in  liste_voisins:




            numero_voisin=self.numero_depuis_pos(voisin)
            if numero_voisin==self.affichage.nb_cases**2-1:
                continue
                
            if numero_voisin>self.jeu.pomme.numero:
                continue
            
            if self.jeu.serpent.taille_queue!=0:
                if self.jeu.pomme_atteinte:
                    if numero_voisin<self.numero_depuis_pos(self.jeu.serpent.pos_queue[0]):
                        liste_pos_suivantes_potentielles.append(voisin)
                else:
                    if numero_voisin<=self.numero_depuis_pos(self.jeu.serpent.pos_queue[0]):
                        liste_pos_suivantes_potentielles.append(voisin)
            else:
                liste_pos_suivantes_potentielles.append(voisin)
            
        # print(self.jeu.pomme_atteinte,self.jeu.serpent.pos,liste_pos_suivantes_potentielles,self.jeu.serpent.pos_queue)
            
        

        

        if  liste_pos_suivantes_potentielles==[]:
            self.suivre_chemin()
            # print('faux')
        else:
            # print('vrai')

            voisin_objectif=max(liste_pos_suivantes_potentielles,key=self.numero_depuis_pos)

            self.jeu.serpent.direction[0]=voisin_objectif[0]-self.jeu.serpent.pos[0]
            self.jeu.serpent.direction[1]=voisin_objectif[1]-self.jeu.serpent.pos[1]
        
        # print()
        





    """A* avec projection sur queue"""
    def  a_etoile_projection_queue(self):    #  regarder  tout  les  plus  courts  chemins!!!!, ou faire que A* ne fait pas de trous

        if self.jeu.distance_parcourue>=1300:
            self.jeu.fin_jeu=True
            self.jeu.etat_partie=-1

        # si pas de queue
        if  self.jeu.serpent.taille_queue==0:
            # juste A* sur la pomme
            self.a_etoile(self.jeu.pomme.pos,[],True)
            return

        if self.jeu.pomme_atteinte:
            

            # on a une queue
            if  self.a_etoile(self.jeu.pomme.pos,[],True):

                

                liste_pos_apres_deplacement=self.liste_pos_apres_deplacement_chemin(list(self.jeu.serpent.pos_queue)+[self.jeu.serpent.pos],self.plus_court_chemin)
                # print(liste_pos_apres_deplacement)
                if  self.a_etoile_neutre(self.jeu.pomme.pos,liste_pos_apres_deplacement[0],liste_pos_apres_deplacement,True):
                    self.aller_sur_pomme=True
                    # print('la pomme est safe')
                    return
                else:
                    self.aller_sur_pomme=False
                    # print('on ne peut pas aller a la pomme, on suit queue')
                    self.a_etoile(self.jeu.serpent.pos_queue[0],[],True)
                    return

            else:
                self.aller_sur_pomme=False
                # print('on suit queue')
                self.a_etoile(self.jeu.serpent.pos_queue[0],[],True)
                return

        # si pomme pas atteinte
        else:
            if not self.aller_sur_pomme:

                # on a une queue
                if  self.a_etoile(self.jeu.pomme.pos,[],False):

                    liste_pos_apres_deplacement=self.liste_pos_apres_deplacement_chemin(list(self.jeu.serpent.pos_queue)+[self.jeu.serpent.pos],self.plus_court_chemin)
                    if  self.a_etoile_neutre(self.jeu.pomme.pos,liste_pos_apres_deplacement[0],liste_pos_apres_deplacement,True):
                        self.aller_sur_pomme=True
                        # print('on peut finalement aller a pomme')
                        return
                    else:
                        self.aller_sur_pomme=False
                        # print('on ne peut pas aller a la pomme, on suit queue')
                        self.a_etoile(self.jeu.serpent.pos_queue[0],[],True)
                        return


                else:
                    self.a_etoile(self.jeu.serpent.pos_queue[0],[],True)
                    # print('on continue aller sur queue')
                    return

            else:
                self.suivre_chemin_particulier(self.plus_court_chemin)
                # print('on continue aller sur pomme')
                return

        print("ABORT")
    

    """A* sur graphe oriente"""
    def a_etoile_graphe_oriente(self):

        if self.jeu.distance_parcourue==0:
            self.a_etoile_oriente(self.jeu.pomme.pos,[],True)
            return
        
        
        # print('pcc',self.plus_court_chemin)
        if self.jeu.pomme_atteinte:
            self.aller_sur_pomme=self.a_etoile_oriente(self.jeu.pomme.pos,[],True)

            if not self.aller_sur_pomme:
                self.a_etoile_oriente(self.jeu.serpent.pos_queue[0],[],True)
        
            
        

        
        # if self.aller_sur_pomme:
            

        #     grille_coupee=True


        #     liste_pos_corps=list(self.jeu.serpent.pos_queue)+[self.jeu.serpent.pos]
        #     liste_pos_corps_apres_deplacement=self.liste_pos_apres_deplacement_chemin(liste_pos_corps,self.plus_court_chemin)

        #     if len(self.plus_court_chemin)>=len(liste_pos_corps_apres_deplacement):
        #         grille_coupee,pos_probleme=self.coupe_grille(liste_pos_corps_apres_deplacement)
        #     else:
        #         grille_coupee,pos_probleme=self.coupe_grille(self.plus_court_chemin)
            
        #     if pos_probleme==self.plus_court_chemin[-1]:
        #         self.suivre_chemin_particulier(self.plus_court_chemin)
        #         self.mettre_a_jour_plus_court_chemin(self.plus_court_chemin)
        #         return

        #     liste_pos_petite_grille_a_combler=[]
        #     if grille_coupee:
        #         self.affichage.mode_manuel=True
                
        # #         print(pos_probleme)
        # #         print('pcc',self.plus_court_chemin)
        # #         return
                
        # #         print(liste_pos_corps_apres_deplacement)
        # #         print(self.plus_court_chemin)
                
                

        #         if len(self.plus_court_chemin)>=len(liste_pos_corps_apres_deplacement):
        #             i_probleme=liste_pos_corps_apres_deplacement.index(pos_probleme)
        #             direction_chemin=[liste_pos_corps_apres_deplacement[i_probleme+1][0]-liste_pos_corps_apres_deplacement[i_probleme][0],liste_pos_corps_apres_deplacement[i_probleme+1][1]-liste_pos_corps_apres_deplacement[i_probleme][1]]      
        #         else:
        #             i_probleme=self.plus_court_chemin.index(pos_probleme)
        #             direction_chemin=[self.plus_court_chemin[i_probleme+1][0]-self.plus_court_chemin[i_probleme][0],self.plus_court_chemin[i_probleme+1][1]-self.plus_court_chemin[i_probleme][1]]

                

        #         # regarder a droite
        #         if direction_chemin==[0,1]:
        #             direction_a_traiter=[-1,0]
        #         elif direction_chemin==[0,-1]:
        #             direction_a_traiter=[1,0]
        #         elif direction_chemin==[1,0]:
        #             direction_a_traiter=[0,1]
        #         elif direction_chemin==[-1,0]:
        #             direction_a_traiter=[0,-1]
                
                

        # #         pos_probleme_petite_grille=self.pos_petite_grille(pos_probleme)
        #         print('pos probleme',pos_probleme)
        # #         print('pos probleme petite grille',pos_probleme_petite_grille)
        #         debut=[pos_probleme[0]+direction_a_traiter[0],pos_probleme[1]+direction_a_traiter[1]]
        #         debut_petite_grille=self.pos_petite_grille(debut)

        #         # initialisation des pos petite grille occupees
        #         liste_pos_petite_grille_occupees=[]
        #         for pos in liste_pos_corps_apres_deplacement:
        #             pos_petite_grille=self.pos_petite_grille(pos[:])
        #             if not pos_petite_grille in liste_pos_petite_grille_occupees:
        #                 liste_pos_petite_grille_occupees.append(pos_petite_grille[:])


        #         # parcours en largeur de la ou on bloque
        #         a_traiter=collections.deque([debut_petite_grille])
        #         deja_traites=[]
        #         vide=collections.deque([])

        #         while a_traiter!=vide:
        #             pos=a_traiter.popleft()
        #             if not pos in deja_traites and not pos in a_traiter and not pos in [self.pos_petite_grille(pos) for pos in self.plus_court_chemin+liste_pos_corps]:
                        
        #                 liste_voisins=self.voisins_petite_grille(pos)
        #                 for voisin in liste_voisins:
        #                     if not voisin in liste_pos_corps:
        #                         a_traiter.append(voisin[:])

        #                 deja_traites.append(pos[:])
                
        #         liste_pos_petite_grille_a_combler=deja_traites[:]

        #         # rajout des cases manquantes
        #         pos_a_ajouter=[]
        #         for i in range(len(self.plus_court_chemin)-1):

        #             pos=self.plus_court_chemin[i]
        #             pos_suivante=self.plus_court_chemin[i+1]
        #             direction=[pos_suivante[0]-pos[0],pos_suivante[1]-pos[1]]

        #             direction_droite=self.direction_droite(direction)
        #             pos_petite_grille=self.pos_petite_grille(pos)

        #             if [pos_petite_grille[0]+direction_droite[0],pos_petite_grille[1]+direction_droite[1]] in liste_pos_petite_grille_a_combler:

        #                 print('pos transition',pos)
        #                 if not self.pos_direction_compatibles(pos,direction):
        #                     continue
                        

        #                 i_transition=i
                        
        #                 a=[pos[0]+direction_droite[0],pos[1]+direction_droite[1]]
        #                 b=[pos[0]+2*direction_droite[0],pos[1]+2*direction_droite[1]]
        #                 c=[pos[0]+2*direction_droite[0]+direction[0],pos[1]+2*direction_droite[1]+direction[1]]
        #                 d=[pos[0]+direction_droite[0]+direction[0],pos[1]+direction_droite[1]+direction[1]]
        #                 pos_a_ajouter=[a,b,c,d]

        #                 break

                
        #         print('dir',direction,direction_droite)
                
        #         if pos_a_ajouter!=[]:
        #             self.plus_court_chemin=self.plus_court_chemin[:(i_transition+1)]+pos_a_ajouter+self.plus_court_chemin[(i_transition+1):]
        #         print(self.plus_court_chemin,pos_a_ajouter)
        

        self.suivre_chemin_particulier(self.plus_court_chemin)
        # self.mettre_a_jour_plus_court_chemin(self.plus_court_chemin)
    
    def a_etoile_graphe_oriente_cout(self):
        self.a_etoile_oriente_sans_grille_coupee(self.jeu.pomme.pos,[],True)

    def pos_direction_compatibles(self,pos,direction):
        if direction==[1,0]:
            return pos[0]%2==0
        elif direction==[0,1]:
            return pos[1]%2==0
        elif direction==[-1,0]:
            return pos[0]%2==1
        elif direction==[0,-1]:
            return pos[1]%2==1

    # def a_etoile_graphe_oriente_v2(self):   # CHANGER QU'ON REGARDE TOUT LE TEMPS PLUS COURT CHEMIN DANS L AUTRE CODE?? (ancien)
    #     score_limite=4
    #     if self.jeu.distance_parcourue==0:
    #         self.a_etoile_oriente(self.jeu.pomme.pos,[],True)
    #         return
        

    #     # # tests ok
    #     # temp=self.contour_liste_aretes([[[0,0],[1,0]]],[0,0],[0,1])
    #     # temp.reverse()
    #     # print('ici',temp)
        
        
    #     self.aller_sur_pomme=self.a_etoile_oriente(self.jeu.pomme.pos,[],True)

    #     # if not self.aller_sur_pomme:
    #     #     self.a_etoile_oriente(self.jeu.serpent.pos_queue[0],[],True)
        
    #     if self.jeu.score>=score_limite and self.liste_murs==[]:
    #         pos_petite_grille_traites=[]  # position qu'on aura parcouru
    #         liste_pos_corps=list(self.jeu.serpent.pos_queue)+[self.jeu.serpent.pos]
    #         plus_court_chemin=[]
    #         print('execution')
    #         for i in range(1,len(self.plus_court_chemin)-1):
    #             if self.liste_murs!=[]:
    #                 break
                
    #             pos=self.plus_court_chemin[i]
    #             pos_suivante=self.plus_court_chemin[i+1]
    #             direction=[pos_suivante[0]-pos[0],pos_suivante[1]-pos[1]]

    #             pos_debut=None

    #             # droite relative
    #             direction_droite=self.direction_droite(direction)
    #             pos_regardee=[pos[0]+direction_droite[0],pos[1]+direction_droite[1]]

    #             if self.pos_petite_grille(pos_regardee) not in pos_petite_grille_traites and 0<=pos_regardee[0]<=self.affichage.nb_cases-1 and 0<=pos_regardee[1]<=self.affichage.nb_cases-1:     # licite
    #                 if self.pos_petite_grille(pos_regardee)!=self.pos_petite_grille(pos) and not pos_regardee in self.jeu.serpent.pos_queue and not pos_regardee in self.plus_court_chemin:
    #                     pos_debut=pos_regardee
    #                     direction_initiale=direction_droite


    #             # gauche relative
    #             direction_gauche=self.direction_gauche(direction)
    #             pos_regardee=[pos[0]+direction_gauche[0],pos[1]+direction_gauche[1]]

    #             if self.pos_petite_grille(pos_regardee) not in pos_petite_grille_traites and 0<=pos_regardee[0]<=self.affichage.nb_cases-1 and 0<=pos_regardee[1]<=self.affichage.nb_cases-1:     # licite
    #                 if self.pos_petite_grille(pos_regardee)!=self.pos_petite_grille(pos) and not pos_regardee in self.jeu.serpent.pos_queue and not pos_regardee in self.plus_court_chemin:
    #                     pos_debut=pos_regardee
    #                     direction_initiale=direction_gauche
                

    #             plus_court_chemin=[]
    #             # plus_court_chemin.append(pos)
    #             if pos_debut is None:
    #                 continue
    #             # plus_court_chemin.append(pos_debut)
                    
                
    #             # self.chemin=np.zeros((self.affichage.nb_cases,self.affichage.nb_cases))
    #             # if self.affichage.nb_cases**2-1 in self.chemin:
    #             #     break
                

    #             direction_initiale=[-direction_initiale[0],-direction_initiale[1]]


    #             debut_petite_grille=self.pos_petite_grille(pos_debut)


    #             liste_aretes=[]
    #             indice_pos=self.plus_court_chemin.index(pos)
    #             # initialisation des pos petite grille occupees et de liste_aretes
    #             liste_pos_petite_grille_occupees=[]
    #             for i in range(indice_pos-1,len(liste_pos_corps)):
    #                 pos_petite_grille=self.pos_petite_grille(liste_pos_corps[i])[:]
    #                 if not pos_petite_grille in liste_pos_petite_grille_occupees:
    #                     liste_pos_petite_grille_occupees.append(pos_petite_grille[:])
                    
    #                 if i<len(liste_pos_corps)-1:
    #                     liste_aretes.append([pos_petite_grille[:],self.pos_petite_grille(liste_pos_corps[i+1][:])])
                
                
    #             liste_aretes.append([self.pos_petite_grille(pos)[:],debut_petite_grille[:]])

                
    #             for i in range(indice_pos):
    #                 if self.pos_petite_grille(self.plus_court_chemin[i])!=self.pos_petite_grille(self.plus_court_chemin[i+1]):
    #                     if not [self.pos_petite_grille(self.plus_court_chemin[i])[:],self.pos_petite_grille(self.plus_court_chemin[i+1])[:]] in liste_aretes:
    #                         liste_aretes.append([self.pos_petite_grille(self.plus_court_chemin[i])[:],self.pos_petite_grille(self.plus_court_chemin[i+1])[:]])


    #             if self.pos_petite_grille(self.jeu.serpent.pos)!=self.pos_petite_grille(self.plus_court_chemin[0]):
    #                 if not [self.pos_petite_grille(self.jeu.serpent.pos)[:],self.pos_petite_grille(self.plus_court_chemin[0])[:]] in liste_aretes:
    #                     liste_aretes.append([self.pos_petite_grille(self.jeu.serpent.pos)[:],self.pos_petite_grille(self.plus_court_chemin[0])[:]])


    #             # liste_aretes=[]
    #             # # initialisation des pos petite grille occupees et de liste_aretes
    #             # liste_pos_petite_grille_occupees=[]
    #             # for pos_ in liste_pos_corps:
    #             #     pos_petite_grille=self.pos_petite_grille(pos_[:])
    #             #     if not pos_petite_grille in liste_pos_petite_grille_occupees:
    #             #         liste_pos_petite_grille_occupees.append(pos_petite_grille[:])
                
                

    #             # parcours en profondeur
    #             a_traiter=collections.deque([debut_petite_grille])
    #             # a_traiter=[]
    #             deja_traites=[]
    #             vide=collections.deque([])



    #             while a_traiter!=vide:
    #                 pos_=a_traiter.pop()
    #                 if not pos_ in deja_traites and not pos_ in a_traiter and not pos_ in liste_pos_petite_grille_occupees:
                        
    #                     liste_voisins=self.voisins_petite_grille(pos_)
    #                     for voisin in liste_voisins:
    #                         if not voisin in a_traiter and not voisin in deja_traites and not voisin in liste_pos_petite_grille_occupees:
    #                             a_traiter.append(voisin[:])


    #                             # on prepare la liste d'aretes (un arbre)
    #                             liste_aretes.append([pos_[:],voisin[:]])

    #                     deja_traites.append(pos_[:])
    #                     pos_petite_grille_traites.append(pos_[:])                    

                
    #             print('pos',pos)
    #             print('pos_debut',pos_debut)
    #             print('liste_pos_petite_grille_occupees',liste_pos_petite_grille_occupees)
    #             print('liste_aretes',liste_aretes)
                
    #             liste_pos_a_ajouter=self.contour_liste_aretes(liste_aretes,pos_debut,direction_initiale)
    #             liste_pos_a_ajouter.reverse()
    #             print('liste_pos_a_ajouter',liste_pos_a_ajouter)
    #             # liste_pos_a_ajouter=[]

    #             print('plus_court_chemin avant',plus_court_chemin)
    #             # for pos_ in liste_pos_a_ajouter:
    #             #     # if pos_ in plus_court_chemin:
    #             #     #     plus_court_chemin.remove(pos_)
    #             #     # plus_court_chemin.append(pos_)

    #             #     if not pos_ in plus_court_chemin:
    #             #         plus_court_chemin.append(pos_)
    #             plus_court_chemin=liste_pos_a_ajouter
    #             print('plus_court_chemin apres',plus_court_chemin)
                
    #             # self.chemin=np.zeros((self.affichage.nb_cases,self.affichage.nb_cases))
    #             for compteur,pos_ in enumerate(plus_court_chemin):
    #                 self.chemin[pos_[1],pos_[0]]=compteur
                    
                
    #             print('plus_court_chemin',plus_court_chemin)
                
    #             print(self.chemin)
        
    #             self.liste_murs=liste_aretes

    'a_etoile_graphe_oriente_hami'
    def a_etoile_graphe_oriente_hami(self):   # CHANGER QU'ON REGARDE TOUT LE TEMPS PLUS COURT CHEMIN DANS L AUTRE CODE??
        score_limite=40
        
        if self.jeu.distance_parcourue==0:
            self.a_etoile_oriente(self.jeu.pomme.pos,[],True)
            return
        
        
        
        

        # if not self.aller_sur_pomme:
        #     self.a_etoile_oriente(self.jeu.serpent.pos_queue[0],[],True)
        
        if self.jeu.score>=score_limite and self.liste_murs==[]:
            self.affichage.mode_manuel=True
            pos_petite_grille_traites=[]  # position qu'on aura parcouru
            # plus_court_chemin=[]
            liste_pos_corps_tete=list(self.jeu.serpent.pos_queue)+[self.jeu.serpent.pos]
            print('execution')


            # initialisation de liste_aretes_final
            liste_aretes_final=[]
            for i in range(len(liste_pos_corps_tete)-1):
                liste_aretes_final.append([self.pos_petite_grille(liste_pos_corps_tete[i])[:],self.pos_petite_grille(liste_pos_corps_tete[i+1][:])])

            # parcours
            for i in range(len(liste_pos_corps_tete)-1):
                print('i=',i)
                
                pos=liste_pos_corps_tete[i]
                pos_suivante=liste_pos_corps_tete[i+1]
                direction=[pos_suivante[0]-pos[0],pos_suivante[1]-pos[1]]


                # initialisation des pos petite grille occupees
                liste_pos_petite_grille_occupees=[]
                for i in range(len(liste_pos_corps_tete)):
                    pos_petite_grille=self.pos_petite_grille(liste_pos_corps_tete[i])[:]
                    if not pos_petite_grille in liste_pos_petite_grille_occupees:
                        liste_pos_petite_grille_occupees.append(pos_petite_grille[:])
                
            

                pos_debut=None
                liste_aretes=[]




                # droite relative
                direction_droite=self.direction_droite(direction)

                # 1 de profondeur
                pos_regardee=[pos[0]+direction_droite[0],pos[1]+direction_droite[1]]
                if self.pos_petite_grille(pos_regardee) not in pos_petite_grille_traites and 0<=pos_regardee[0]<=self.affichage.nb_cases-1 and 0<=pos_regardee[1]<=self.affichage.nb_cases-1:     # licite
                    if self.pos_petite_grille(pos_regardee)!=self.pos_petite_grille(pos) and not self.pos_petite_grille(pos_regardee) in liste_pos_petite_grille_occupees and not pos_regardee in liste_pos_corps_tete:
                        pos_debut=pos_regardee
                        # direction_initiale=direction_droite
                        liste_aretes+=self.liste_aretes_petite_grille(pos,pos_debut,direction_droite,liste_pos_petite_grille_occupees,pos_petite_grille_traites)

                # 2 de profondeur
                pos_regardee=[pos[0]+2*direction_droite[0],pos[1]+2*direction_droite[1]]
                if self.pos_petite_grille(pos_regardee) not in pos_petite_grille_traites and 0<=pos_regardee[0]<=self.affichage.nb_cases-1 and 0<=pos_regardee[1]<=self.affichage.nb_cases-1:     # licite
                    if self.pos_petite_grille(pos_regardee)!=self.pos_petite_grille(pos) and not self.pos_petite_grille(pos_regardee) in liste_pos_petite_grille_occupees and not pos_regardee in liste_pos_corps_tete:
                        pos_debut=pos_regardee
                        # direction_initiale=direction_droite
                        liste_aretes+=self.liste_aretes_petite_grille(pos,pos_debut,direction_droite,liste_pos_petite_grille_occupees,pos_petite_grille_traites)




                # gauche relative
                direction_gauche=self.direction_gauche(direction)

                # 1 de profondeur
                pos_regardee=[pos[0]+direction_gauche[0],pos[1]+direction_gauche[1]]
                if self.pos_petite_grille(pos_regardee) not in pos_petite_grille_traites and 0<=pos_regardee[0]<=self.affichage.nb_cases-1 and 0<=pos_regardee[1]<=self.affichage.nb_cases-1:     # licite
                    if self.pos_petite_grille(pos_regardee)!=self.pos_petite_grille(pos) and not self.pos_petite_grille(pos_regardee) in liste_pos_petite_grille_occupees and not pos_regardee in liste_pos_corps_tete:
                        pos_debut=pos_regardee
                        # direction_initiale=direction_gauche
                        liste_aretes+=self.liste_aretes_petite_grille(pos,pos_debut,direction_gauche,liste_pos_petite_grille_occupees,pos_petite_grille_traites)

                # 2 de profondeur
                pos_regardee=[pos[0]+2*direction_gauche[0],pos[1]+2*direction_gauche[1]]
                if self.pos_petite_grille(pos_regardee) not in pos_petite_grille_traites and 0<=pos_regardee[0]<=self.affichage.nb_cases-1 and 0<=pos_regardee[1]<=self.affichage.nb_cases-1:     # licite
                    if self.pos_petite_grille(pos_regardee)!=self.pos_petite_grille(pos) and not self.pos_petite_grille(pos_regardee) in liste_pos_petite_grille_occupees and not pos_regardee in liste_pos_corps_tete:
                        pos_debut=pos_regardee
                        # direction_initiale=direction_gauche
                        liste_aretes+=self.liste_aretes_petite_grille(pos,pos_debut,direction_gauche,liste_pos_petite_grille_occupees,pos_petite_grille_traites)


                # plus_court_chemin.append(pos)
                # if pos_debut is None:
                #     continue
                # plus_court_chemin.append(pos_debut)
                    
                
                # self.chemin=np.zeros((self.affichage.nb_cases,self.affichage.nb_cases))
                # if self.affichage.nb_cases**2-1 in self.chemin:
                #     break
                
                liste_aretes_final+=liste_aretes

                

            print('liste_aretes_final',liste_aretes_final)
            self.liste_murs=liste_aretes_final
                
            
            # apres le parcours de liste_pos_corps_tete
            if [[0,0],[0,1]] in liste_aretes_final:
                liste_pos_a_ajouter=self.contour_liste_aretes(liste_aretes_final,[0,0],[0,1])
            else:
                liste_pos_a_ajouter=self.contour_liste_aretes(liste_aretes_final,[0,0],[1,0])

            liste_pos_a_ajouter.reverse()




            for compteur,pos_ in enumerate(liste_pos_a_ajouter):
                self.chemin[pos_[1],pos_[0]]=compteur
            
            print(self.chemin)



        if self.jeu.score<score_limite:
            self.a_etoile_oriente(self.jeu.pomme.pos,[],True)
            self.suivre_chemin_particulier(self.plus_court_chemin)
            return
        elif self.liste_murs==[]:
            self.a_etoile_oriente(self.jeu.pomme.pos,[],True)
            self.suivre_chemin_particulier(self.plus_court_chemin)
            return
            
        else:
            self.suivre_chemin()
    
    def liste_aretes_petite_grille(self,pos,pos_debut,direction_initiale,liste_pos_petite_grille_occupees,pos_petite_grille_traites):
        liste_aretes=[]


        if pos_debut is None:
            return liste_aretes
        
        direction_initiale=[-direction_initiale[0],-direction_initiale[1]]


        debut_petite_grille=self.pos_petite_grille(pos_debut)



        liste_aretes.append([self.pos_petite_grille(pos)[:],debut_petite_grille[:]])
        

        

        # if self.pos_petite_grille(self.jeu.serpent.pos)!=self.pos_petite_grille(self.plus_court_chemin[0]):
        #     if not [self.pos_petite_grille(self.jeu.serpent.pos)[:],self.pos_petite_grille(self.plus_court_chemin[0])[:]] in liste_aretes:
        #         liste_aretes.append([self.pos_petite_grille(self.jeu.serpent.pos)[:],self.pos_petite_grille(self.plus_court_chemin[0])[:]])


        # liste_aretes=[]
        # # initialisation des pos petite grille occupees et de liste_aretes
        # liste_pos_petite_grille_occupees=[]
        # for pos_ in liste_pos_corps:
        #     pos_petite_grille=self.pos_petite_grille(pos_[:])
        #     if not pos_petite_grille in liste_pos_petite_grille_occupees:
        #         liste_pos_petite_grille_occupees.append(pos_petite_grille[:])
        
        

        # parcours en profondeur
        a_traiter=collections.deque([debut_petite_grille])
        # a_traiter=[]
        deja_traites=[]
        vide=collections.deque([])



        while a_traiter!=vide:
            pos_=a_traiter.pop()
            if not pos_ in deja_traites and not pos_ in a_traiter and not pos_ in liste_pos_petite_grille_occupees:
                
                liste_voisins=self.voisins_petite_grille(pos_)
                for voisin in liste_voisins:
                    if not voisin in a_traiter and not voisin in deja_traites and not voisin in liste_pos_petite_grille_occupees:
                        a_traiter.append(voisin[:])


                        # on prepare la liste d'aretes (un arbre)
                        liste_aretes.append([pos_[:],voisin[:]])

                deja_traites.append(pos_[:])
                pos_petite_grille_traites.append(pos_[:])                    

        print('intermediaire debut')
        print('pos',pos)
        print('pos_debut',pos_debut)
        print('liste_pos_petite_grille_occupees',liste_pos_petite_grille_occupees)
        print('liste_aretes',liste_aretes)
        print('intermediaire fin')
        
        
        # print('liste_pos_a_ajouter',liste_pos_a_ajouter)
        # liste_pos_a_ajouter=[]

        # print('plus_court_chemin avant',plus_court_chemin)
        # for pos_ in liste_pos_a_ajouter:
        #     # if pos_ in plus_court_chemin:
        #     #     plus_court_chemin.remove(pos_)
        #     # plus_court_chemin.append(pos_)

        #     if not pos_ in plus_court_chemin:
        #         plus_court_chemin.append(pos_)
        # plus_court_chemin=liste_pos_a_ajouter
        # print('plus_court_chemin apres',plus_court_chemin)
        
        # self.chemin=np.zeros((self.affichage.nb_cases,self.affichage.nb_cases))
        

        return liste_aretes
    
    def contour_liste_aretes(self,liste_aretes,pos_debut,direction_initiale):    # convention: rotation trigo
        n=self.affichage.nb_cases//2

        pos=pos_debut[:]
        direction=direction_initiale[:]

        chemin=[pos_debut[:]]


        # doublons pour deux sens
        ajouter=[]
        for  couple  in  liste_aretes:
            ajouter.append([couple[1][:],couple[0][:]])

        liste_aretes+=ajouter

        
        
        while pos!=pos_debut or len(chemin)==1:
            print('avant',pos,direction)

            pos_n=[outils.composante_petite_grille(pos[0]),outils.composante_petite_grille(pos[1])]
            if  direction==[1,0]:    #  j  pair
                if  pos[0]%2==0:
                    if  pos_n[1]-1>=0  and  [pos_n,[pos_n[0],pos_n[1]-1]]  in  liste_aretes:
                        direction=[0,-1]
                elif  pos_n[0]+1>n-1  or  not  [pos_n,[pos_n[0]+1,pos_n[1]]]  in  liste_aretes:
                    direction=[0,1]

            elif  direction==[-1,0]:      #  j  impair
                if    pos[0]%2==1:
                    if  [pos_n,[pos_n[0],pos_n[1]+1]]  in  liste_aretes:
                        direction=[0,1]
                elif  pos_n[0]-1<0  or  not  [pos_n,[pos_n[0]-1,pos_n[1]]]  in  liste_aretes:
                    direction=[0,-1]

            elif  direction==[0,1]:    #  i  impair
                if  pos[1]%2==0:
                    if  pos_n[0]+1<=n-1  and  [pos_n,[pos_n[0]+1,pos_n[1]]]  in  liste_aretes:
                        direction=[1,0]
                elif  pos_n[1]+1>n-1  or  not  [pos_n,[pos_n[0],pos_n[1]+1]]  in  liste_aretes:
                    direction=[-1,0]

            elif  direction==[0,-1]:    #  i  pair
                if  pos[1]%2==1:
                    if  [pos_n,[pos_n[0]-1,pos_n[1]]]  in  liste_aretes:
                        direction=[-1,0]
                elif  pos_n[1]-1<0  or  not  [pos_n,[pos_n[0],pos_n[1]-1]]  in  liste_aretes:
                    direction=[1,0]

            

            pos[0]+=direction[0]
            pos[1]+=direction[1]


            print('apres',pos,direction)
            print('param',liste_aretes,pos_debut,direction_initiale)

            chemin.append(pos[:])
        
        return chemin[:-1]

    
        
    'arbre_raccourcis_modifier_hami'
    def arbre_raccourcis_modifier_hami(self):

        if self.jeu.score==0:
            self.a_etoile_seul()
            return
        
        # on ne fait le parcours que s il y a besoin
        
        if not self.jeu.pomme_atteinte:
            self.suivre_chemin_particulier(self.chemin_optimal)
            
        else:
            # parcours en largeur
            pos=self.jeu.serpent.pos[:]
            liste_pos_queue=list(self.jeu.serpent.pos_queue)

            a_traiter=[(
                                          abs(self.jeu.pomme.pos[0]-pos[0])+abs(self.jeu.pomme.pos[1]-pos[1]),
                                          pos[:],
                                          liste_pos_queue,
                                          self.chemin.copy(),
                                          [pos[:]],
                                          0,
                                          0)]    # pos,liste_pos_queue,cycle_hami,chemin_emprunte,nb_raccourcis,nb_modifications
            a_regarder=[]

            profondeur=0
            profondeur_max=inf

            deque_vide=collections.deque([])

            pos_pomme=self.jeu.pomme.pos

            while a_traiter!=deque_vide:  #FAIRE QU'IL Y A UN DEPLACEMENT POS_QUEUE
                
                
                _,pos,liste_pos_queue,cycle_hami,chemin_emprunte,nb_raccourcis,nb_modifications=min(a_traiter,key=lambda couple:couple[0])
                a_traiter.remove((_,pos,liste_pos_queue,cycle_hami,chemin_emprunte,nb_raccourcis,nb_modifications))
                liste_voisins_pos=self.voisins(pos)
                



                # print(len(chemin_emprunte)-1)

                if len(chemin_emprunte)-1>profondeur_max:
                    break
                
                if pos==self.jeu.pomme.pos:
                    profondeur_max=len(chemin_emprunte)-1

                # heure_debut=time.time()
                for voisin in liste_voisins_pos:
                    if voisin in liste_pos_queue:
                        continue
                    # print('en cours',_,pos,liste_pos_queue,chemin_emprunte,nb_raccourcis,nb_modifications,voisin)
                    
                    
                    peut_prendre_raccourci=self.peut_prendre_raccourci(pos,voisin,cycle_hami)
                    
                    peut_modifier_cycle,nouveau_cycle_hami=self.peut_modifier_cycle(pos,voisin,liste_pos_queue,cycle_hami)
                    
                    

                    nb_raccourcis_a_ajouter=0
                    nb_modifications_a_ajouter=0
                    if peut_prendre_raccourci:
                        pos_suivante=voisin[:]
                        nb_raccourcis_a_ajouter=1
                        # print('raccourci')

                    # elif peut_modifier_cycle:
                    #     pos_suivante=voisin[:]
                    #     nb_modifications_a_ajouter=1
                    #     # print('modif')
                    else:
                        pos_suivante=self.pos_suivante_selon_cycle_hami(pos,cycle_hami)
                    
                    numero_pos=int(cycle_hami[pos[1],pos[0]])
                    score=(int(cycle_hami[pos_pomme[1],pos_pomme[0]])-numero_pos)%(self.affichage.nb_cases**2)-(int(cycle_hami[pos_suivante[1],pos_suivante[0]])-numero_pos)%(self.affichage.nb_cases**2)

                    if nb_modifications_a_ajouter==1:
                        couple_a_ajouter=(score,pos_suivante[:],liste_pos_queue[1:]+[pos_suivante[:]],nouveau_cycle_hami,chemin_emprunte+[pos_suivante[:]],nb_raccourcis+nb_raccourcis_a_ajouter,nb_modifications+nb_modifications_a_ajouter)
                    else:
                        couple_a_ajouter=(score,pos_suivante[:],liste_pos_queue[1:]+[pos_suivante[:]],cycle_hami,chemin_emprunte+[pos_suivante[:]],nb_raccourcis+nb_raccourcis_a_ajouter,nb_modifications+nb_modifications_a_ajouter)
                    
                    if not couple_a_ajouter in a_traiter:
                        a_traiter.append(couple_a_ajouter)

                # print(time.time()-heure_debut)
                if chemin_emprunte[-1]==pos_pomme:
                    a_regarder.append((pos,liste_pos_queue,cycle_hami,chemin_emprunte[:],nb_raccourcis,nb_modifications))
                    break


            if a_traiter==deque_vide:
                print('probleme',a_regarder)

            # couple_optimal=min(a_regarder,key=lambda couple:couple[4]+couple[5])
            # print(a_regarder)
            couple_optimal=a_regarder[0]
            # print(couple_optimal)
            chemin_optimal=couple_optimal[3]
            nouveau_cycle_hami=couple_optimal[2]

            self.chemin_optimal=chemin_optimal
            self.chemin=nouveau_cycle_hami
            self.affichage.liste_aretes_cycle=self.affichage.initialiser_liste_aretes_cycle()
            self.suivre_chemin_particulier(self.chemin_optimal)
            # print(self.chemin_optimal)


        # print('chemin_opti',self.chemin_optimal)
    
    def pos_suivante_selon_cycle_hami(self,pos,cycle_hami):
        numero_suivant=int(cycle_hami[pos[1],pos[0]])+1
        
        #  dir_0=[0,0]
        if  numero_suivant==self.affichage.nb_cases**2:
            numero_suivant=0
        
        for  j  in  range(-1,2):
            for  i  in  range(-1,2):
                if  i*j==0  and  pos[0]+j>=0  and  pos[0]+j<=self.affichage.nb_cases-1  and  pos[1]+i>=0  and  pos[1]+i<=self.affichage.nb_cases-1:
                    if  int(cycle_hami[pos[1]+i,pos[0]+j])==numero_suivant:
                        return [pos[0]+j,pos[1]+i]
    
    def peut_prendre_raccourci(self,pos,pos_suivante,cycle_hami):
        numero_pos=int(cycle_hami[pos[1],pos[0]])
        numero_pos_suivante=(int(cycle_hami[pos_suivante[1],pos_suivante[0]])-numero_pos)%(self.affichage.nb_cases**2)


        # raccourci croissant
        numero_pomme=(cycle_hami[self.jeu.pomme.pos[1],self.jeu.pomme.pos[0]]-numero_pos)%(self.affichage.nb_cases**2)
        if 1<=numero_pos_suivante<=numero_pomme:
            return numero_pomme-numero_pos_suivante>self.jeu.serpent.taille_queue
        
        return False

    def peut_modifier_cycle(self,pos,voisin,liste_pos_queue,cycle_hami):

        self.pos_boucle_1=[]
        self.pos_boucle_2=[]


        numero_actuel=int(cycle_hami[pos[1],pos[0]])
        numero_desire=int(cycle_hami[voisin[1],voisin[0]])

        difference_numero=abs(numero_desire-numero_actuel)

        
        if difference_numero in [-1,0,1,self.affichage.nb_cases**2-1]:
            return  False,[]



        #  etablissement  des  pos  des  deux  boucles
        
        pos_boucle_1=[]
        pos_boucle_2=[]

        boucle_actuelle=1

        # pour savoir comment on recolle, depend de si c'est un raccourci croissant ou non
        parite=None


        # direction=[voisin[0]-pos[0],voisin[1]-pos[1]]

        pos_suivante=voisin[:]


        if  len(self.jeu.serpent.pos_queue)==0:
            # on s'en fiche
            parite=1
        else:
            #  cas  ou  on  est  croissant
            if  int(cycle_hami[liste_pos_queue[-1][1],liste_pos_queue[-1][0]])<numero_actuel:
                # print('croissant')
                #  raccourci  croissant
                if  int(cycle_hami[pos_suivante[1],pos_suivante[0]])>numero_actuel:
                    parite=1
                else:
                    parite=2
            #  cas  ou  on  est  decroissant
            else:
                # print('décroissant')
                #  raccourci  croissant
                if  int(cycle_hami[pos_suivante[1],pos_suivante[0]])>numero_actuel:
                    parite=2
                else:
                    parite=1

        #  parite=1






        pos_=[0,0]      #  a  l'origine
        for  _  in  range(self.affichage.nb_cases**2):
            i,j=np.where(cycle_hami==int(cycle_hami[pos_[1],pos_[0]]+1))   # pour savoir ou on va apres

            pos_suivante=[j,i]
            # print('a pos_suivante',pos_suivante)


            #  print(boucle_actuelle,pos)
            numero_pos_=int(cycle_hami[pos_[1],pos_[0]])
            if  numero_pos_!=numero_actuel and numero_pos_!=numero_desire:
                if  boucle_actuelle==1:
                    pos_boucle_1.append(pos_[:])
                elif  boucle_actuelle==2:
                    pos_boucle_2.append(pos_[:])

            elif  numero_pos_==numero_actuel or numero_pos_==numero_desire:
                #  print('atteint')
                if  boucle_actuelle==1:
                    boucle_actuelle=2
                elif  boucle_actuelle==2:
                    boucle_actuelle=1
                if  parite==1:
                    pos_boucle_1.append(pos_[:])
                else:
                    pos_boucle_2.append(pos_[:])


            pos_[:]=pos_suivante[:]

        """s'en occuper"""
        def pos_depuis_numero(numero):
            for  i  in  range(self.affichage.nb_cases):
                for  j  in  range(self.affichage.nb_cases):
                    if  int(cycle_hami[i][j])==numero:
                        return([j,i])
            print('pos_depuis_numero local, pas trouvé la pos')
        #  si  les  deux  boucles  ne  sont  pas  faites  au  bon  endroit
        if  len(self.jeu.serpent.pos_queue)==0:


            if  abs(pos_boucle_2[0][0]-pos_boucle_2[-1][0])  not  in  [0,1]  or  abs(pos_boucle_2[0][1]-pos_boucle_2[-1][1])  not  in  [0,1]:
                #  print(difference(pos_boucle_2[-1][0],pos_boucle_2[-1][1]))
                pos_boucle_1.remove(pos_depuis_numero(numero_actuel))
                pos_boucle_1.remove(pos_depuis_numero(numero_desire))
                pos_boucle_2.insert(0,pos_depuis_numero(min(numero_actuel,numero_desire)))
                pos_boucle_2.append(pos_depuis_numero(max(numero_actuel,numero_desire)))

                # print('correction')


        #  si  on  veut  les  voir
        self.pos_boucle_1=pos_boucle_1
        self.pos_boucle_2=pos_boucle_2


        #  on  verifie  que  les  deux  boucles  sont  bien  des  boucles
        if  abs(pos_boucle_2[0][0]-pos_boucle_2[-1][0])  not  in  [0,1]  or  abs(pos_boucle_2[0][1]-pos_boucle_2[-1][1])  not  in  [0,1]:
            # print('boucle 2 pas boucle')
            return  False,[]

        if  abs(pos_boucle_1[0][0]-pos_boucle_1[-1][0])  not  in  [0,1]  or  abs(pos_boucle_1[0][1]-pos_boucle_1[-1][1])  not  in  [0,1]:
            # print('boucle 1 pas boucle')
            return  False,[]

        for  i  in  range(len(pos_boucle_1)-1):
            if  pos_boucle_1[i]  not  in  self.voisins(pos_boucle_1[i+1]):
                # print('boucle 1 pas boucle')
                return  False,[]

        for  i  in  range(len(pos_boucle_2)-1):
            if  pos_boucle_2[i]  not  in  self.voisins(pos_boucle_2[i+1]):
                # print('boucle 2 pas boucle')
                return  False,[]

        # return


        #  on  cherche  a  recoller  les  boucles
        pos_boucle=pos_boucle_1[:]

        depart_arrivee_1=[]
        depart_arrivee_2=[]

        for  i  in  range(len(pos_boucle)-1):

            liste_voisins=self.voisins(pos_boucle[i])
            liste_voisins_suivant=self.voisins(pos_boucle[i+1])

            

            #  on  regarde  les  voisinages
            for  voisin_  in  liste_voisins:

                #  si  on  a  trouvé
                if  depart_arrivee_1!=[]:
                    break

                for  voisin_suivant  in  liste_voisins_suivant:

                    #  pour  recoller  entre  les  deux  boucles
                    if  voisin_  not  in  pos_boucle  and  voisin_suivant  not  in  pos_boucle:

                        #  pour  ne  pas  recoller  la  ou  on  va  ou  est
                        if  int(cycle_hami[voisin_[1],voisin_[0]])  not  in  [numero_actuel,numero_desire]  and  int(cycle_hami[voisin_suivant[1],voisin_suivant[0]]) not  in  [numero_actuel,numero_desire]  and  int(cycle_hami[pos_boucle[i][1],pos_boucle[i][0]]) not  in  [numero_actuel,numero_desire]  and  int(cycle_hami[pos_boucle[i+1][1],pos_boucle[i+1][0]]) not  in  [numero_actuel,numero_desire]:

                            # pour ne pas recoller sur la queue
                            if  pos_boucle[i][:]  not  in  liste_pos_queue  and  pos_boucle[i+1][:]  not  in  liste_pos_queue  and  voisin_[:]  not  in  liste_pos_queue  and  voisin_suivant[:]  not  in  liste_pos_queue:
                                if  abs(int(cycle_hami[voisin_[1],voisin_[0]])-int(cycle_hami[voisin_suivant[1],voisin_suivant[0]]))==1:
                                    depart_arrivee_1=[pos_boucle[i][:],pos_boucle[i+1][:]]
                                    depart_arrivee_2=[voisin_[:],voisin_suivant[:]]
                                    break

                            if  depart_arrivee_1!=[]:
                                break
                        

        if  depart_arrivee_1==[]:
            # print('pas  boucle')
            return  False,[]

        #  on  reindice
        pos=[0,0]
        pos_suivante=None
        nouveau_cycle_hami=copy.deepcopy(cycle_hami)
        for  _  in  range(self.affichage.nb_cases**2):

            if  pos==depart_arrivee_1[0]:
                pos_suivante=depart_arrivee_2[0]
            elif  pos==depart_arrivee_2[1]:
                pos_suivante=depart_arrivee_1[1]
            else:
                if  pos_boucle==pos_boucle_1:
                    if  pos  in  pos_boucle_1:
                        pos_suivante=pos_boucle_1[(pos_boucle_1.index(pos)+1)%len(pos_boucle_1)]
                    else:
                        pos_suivante=pos_boucle_2[(pos_boucle_2.index(pos)+1)%len(pos_boucle_2)]

            nouveau_cycle_hami[pos[1],pos[0]]=_
            pos=pos_suivante[:]

        cycle_hami=nouveau_cycle_hami[:]

        # print(self.chemin)

        # self.affichage.liste_aretes_cycle=self.affichage.initialiser_liste_aretes_cycle()

        return  True,cycle_hami


            


        

         
    


    def pos_petite_grille(self,pos):
        return [outils.composante_petite_grille(pos[0]),outils.composante_petite_grille(pos[1])]

    def direction_gauche(self,direction):
        if direction==[0,1]:
            return [1,0]
        elif direction==[0,-1]:
            return [-1,0]
        elif direction==[1,0]:
            return [0,-1]
        elif direction==[-1,0]:
            return [0,1]

    def direction_droite(self,direction):
        if direction==[0,1]:
            return [-1,0]
        elif direction==[0,-1]:
            return [1,0]
        elif direction==[1,0]:
            return [0,1]
        elif direction==[-1,0]:
            return [0,-1]

    def direction_suivante_cellule(self,pos_cellule):
        if pos_cellule==[0,0]:
            return [0,1]
        elif pos_cellule==[0,1]:
            return [1,0]
        elif pos_cellule==[1,1]:
            return [0,-1]
        elif pos_cellule==[1,0]:
            return [-1,0]
    
    def distance(self,pos1,pos2):
        return abs(pos2[0]-pos1[0])+abs(pos2[1]-pos1[1])



    def parcours_cellules(self):
        
        """reste dans les cellules (2,2), sens de rotation: trigo, on voit  ça comme un arbre, on ne aller que là où on n'a pas exploré
        ou sur le parent"""

        pos_petite_grille=self.pos_petite_grille(self.jeu.serpent.pos)

        # pour ne pas boucler
        if self.jeu.pomme_atteinte:
            self.liste_pos_traitees=[]

            # gestion de l'arbre
            a_supprimer=[]
            liste_pos_queue_tete_serpent=[self.pos_petite_grille(pos) for pos in list(self.jeu.serpent.pos_queue)+[self.jeu.serpent.pos]]
            for parent in self.dico_arbre:
                if not [parent[0],parent[1]] in liste_pos_queue_tete_serpent:
                    a_supprimer.append(parent)
            for parent in a_supprimer:
                del self.dico_arbre[parent]
            

        self.liste_pos_traitees.append(self.jeu.serpent.pos[:])
        
        # cas ou on lance le jeu
        if self.jeu.distance_parcourue==0:
            self.jeu.serpent.direction=[0,1]

        

        pos_cellule=[self.jeu.serpent.pos[0]%2,self.jeu.serpent.pos[1]%2]
        direction_suivante_cellule=self.direction_suivante_cellule(pos_cellule)
        direction_optionnelle=self.direction_droite(direction_suivante_cellule)

        pos_suivante_optionnelle=[self.jeu.serpent.pos[0]+direction_optionnelle[0],self.jeu.serpent.pos[1]+direction_optionnelle[1]]
        pos_suivante_cellule=[self.jeu.serpent.pos[0]+direction_suivante_cellule[0],self.jeu.serpent.pos[1]+direction_suivante_cellule[1]]

        pos_suivante_optionnelle_petite_grille=self.pos_petite_grille(pos_suivante_optionnelle)
        pos_serpent_petite_grille=self.pos_petite_grille(self.jeu.serpent.pos)

        deplacement_fait=False
        

        # si on sort de la grille via l'optionnelle
        if not 0<=pos_suivante_optionnelle[0]<=self.affichage.nb_cases-1 or not 0<=pos_suivante_optionnelle[1]<=self.affichage.nb_cases-1:
            self.jeu.serpent.direction=direction_suivante_cellule
            print('bords')
            deplacement_fait=True

        # cas ou on doit prendre l'optionnelle, la suivante_cellule est inaccessible
        if pos_suivante_cellule in self.jeu.serpent.pos_queue:
            self.jeu.serpent.direction=direction_optionnelle
            print('suivante_cellule dans queue')
            deplacement_fait=True    

        # cas ou on ne peut pas prendre l'optionnelle
        if pos_suivante_optionnelle in self.jeu.serpent.pos_queue or pos_suivante_optionnelle in self.liste_pos_traitees:
            self.jeu.serpent.direction=direction_suivante_cellule
            print('optionnelle dans queue ou deja traite')
            deplacement_fait=True
        
        # if (pos_suivante_optionnelle_petite_grille[0],pos_suivante_optionnelle_petite_grille[1]) in self.dico_arbre:
        #     if pos_suivante_optionnelle_petite_grille!=self.parent(pos_serpent_petite_grille):
        #         self.jeu.serpent.direction=direction_suivante_cellule
        #         # self.affichage.mode_manuel=True
        #         print('arbre')
        #         deplacement_fait=True

        

        # cas ou on separe la grille en deux
        if self.coupe_grille(list(self.jeu.serpent.pos_queue)+[self.jeu.serpent.pos,pos_suivante_optionnelle])[0]:
            self.jeu.serpent.direction=direction_suivante_cellule
            deplacement_fait=True
        
        # cas ou on separe la grille en deux
        if self.coupe_grille(list(self.jeu.serpent.pos_queue)+[self.jeu.serpent.pos,pos_suivante_cellule])[0]:
            self.jeu.serpent.direction=direction_optionnelle
            deplacement_fait=True

        if not deplacement_fait:
            # si rien a signaler, on prend la distance la plus petite
            if self.distance(pos_suivante_cellule,self.jeu.pomme.pos)<self.distance(pos_suivante_optionnelle,self.jeu.pomme.pos):
                self.jeu.serpent.direction=direction_suivante_cellule
            else:
                self.jeu.serpent.direction=direction_optionnelle
        
        # if pos_suivante_parent is not None and pos_suivante_parent in self.jeu.serpent.pos_queue:
        #     if self.distance(pos_suivante_parent,self.jeu.pomme.pos)<min(self.distance(pos_suivante_cellule,self.jeu.pomme.pos),self.distance(pos_suivante_optionnelle,self.jeu.pomme.pos)):
        #         self.jeu.serpent.direction=direction_parent
        #         self.affichage.mode_manuel=True


        pos_suivante_serpent=[self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]]
        pos_suivante_serpent_petite_grille=self.pos_petite_grille(pos_suivante_serpent)
        if pos_suivante_serpent_petite_grille!=pos_serpent_petite_grille:
            self.dico_arbre[(pos_serpent_petite_grille[0],pos_serpent_petite_grille[1])]=pos_suivante_serpent_petite_grille[:]
        print(self.dico_arbre)
    

    def parent(self,enfant):
        for parent in self.dico_arbre:
            if self.dico_arbre[parent]==enfant:
                return [parent[0],parent[1]]
        
        print("probleme, pas de parent trouvé")
    
        
    



    """Monté Carlo tree search"""
    def monte_carlo_tree_search(self):
        nb_essais=1000
        profondeur_max=int(self.affichage.nb_cases)

        recompense_pomme=1
        malus_bloque=-1

        # dico_choix={(-1,0):[0,0],(0,-1):[0,0],(1,0):[0,0],(0,1):[0,0]}

        dico_choix={}
        for pos in [voisin for voisin in self.voisins(self.jeu.serpent.pos) if voisin not in self.jeu.serpent.pos_queue]:
            dico_choix[(pos[0]-self.jeu.serpent.pos[0],pos[1]-self.jeu.serpent.pos[1])]=[0,0]
        
        
        if dico_choix=={}:
            print('a')
            self.affichage.mode_manuel=True
            return
        
        for _ in range(nb_essais):
            
            pos=self.jeu.serpent.pos
            pos_queue=self.jeu.serpent.pos_queue.copy()
            pos_pomme=self.jeu.pomme.pos[:]


            liste_pos_suivantes_potentielles=[voisin for voisin in self.voisins(pos) if voisin not in pos_queue]
            if liste_pos_suivantes_potentielles==[]:
                print("NONONONON")
                break
            else:
                pos_suivante=rd.choice(liste_pos_suivantes_potentielles)
            
            direction_initiale=(pos_suivante[0]-self.jeu.serpent.pos[0],pos_suivante[1]-pos[1])
            dico_choix[direction_initiale][1]+=1

            pos=pos_suivante[:]
            profondeur=1

            pomme_atteinte=False

            
            while profondeur<profondeur_max:
                liste_pos_suivantes_potentielles=[voisin for voisin in self.voisins(pos) if voisin not in pos_queue]

                if liste_pos_suivantes_potentielles==[]:
                    # si bloqué
                    # (total,nb_essais)
                    dico_choix[direction_initiale][0]+=malus_bloque
                    break

                else:
                    pos_suivante=rd.choice(liste_pos_suivantes_potentielles)

                if pos==pos_pomme:
                    dico_choix[direction_initiale][0]+=recompense_pomme
                    pomme_atteinte=True
                else:
                    pomme_atteinte=False
                
                # on replace la pomme
                if pomme_atteinte:
                    liste_pos_pomme_potentielles=[]
                    for i in range(self.affichage.nb_cases):
                        for j in range(self.affichage.nb_cases):
                            if not [i,j] in list(pos_queue) and not [i,j]==pos:
                                liste_pos_pomme_potentielles.append([i,j])

                    if liste_pos_pomme_potentielles==[]:
                        pos_pomme=[-1,-1]
                        dico_choix[direction_initiale][0]-=malus_bloque    # le jeu est alors fini, on va perdre un point
                        break
                    else:
                        pos_pomme=rd.choice(liste_pos_pomme_potentielles)

                if not pomme_atteinte and len(pos_queue)!=0:
                    pos_queue.popleft()
                
                pos_queue.append(pos[:])

                pos=pos_suivante[:]

                profondeur+=1

            if _==nb_essais-1:
                dico_choix[direction_initiale][0]+=(self.affichage.nb_cases/2-self.distance(pos,pos_pomme))**3
        
        # print(dico_choix)
        direction_suivante=max(dico_choix,key=lambda cle: dico_choix[cle][0]/(dico_choix[cle][1]+.0000001))
        # print(direction_suivante)
        if dico_choix[direction_suivante][1]==0:
            print('b')
            self.affichage.mode_manuel=True

        self.jeu.serpent.direction=direction_suivante
                
            


    """A*  que  si  modification"""  #  modifier_cyle  à  reparer..
    def  a_etoile_seulement_si_modif(self):
        
        # pour boucles
        if self.jeu.distance_parcourue>=1300:
            self.jeu.fin_jeu=True
            self.jeu.etat_partie=-1
        
        #  if  self.jeu.pomme.numero<self.numero_depuis_pos(self.jeu.serpent.pos):
        #      self.inverser_grille()
        self.a_etoile(self.jeu.pomme.pos,[],True)

        # a=self.peut_modifier_cycle(pos=self.jeu.serpent.pos,
        #                                voisin=[self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]],
        #                                liste_pos_queue=self.jeu.serpent.pos_queue,
        #                                cycle_hami=self.chemin)
        # b=self.modifier_cycle()
        
        liste_boucles=self.recuperer_deux_boucles()
        if liste_boucles is False or not self.modifier_cycle(liste_boucles):
            self.suivre_chemin()
            if  self.jeu.serpent.pos_queue!=collections.deque([])  and  [self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]]==self.jeu.serpent.pos_queue[-1]:
                self.inverser_grille()
                self.suivre_chemin()
                print('grille inv')
        # print()
        


    """A*  sans  rien"""
    def a_etoile_seul(self):
        if self.plus_court_chemin==[]:
            self.a_etoile(self.jeu.pomme.pos,[],True)
        else:
            self.suivre_chemin_particulier(self.plus_court_chemin)
        


        """ POUR SOUDER 2 FACTEURS
        dico_adjacence_deux_facteur=self.generer_deux_facteur()
        self.liste_aretes_deux_facteur=self.generer_liste_aretes_depuis_dico_adjacence(dico_adjacence_deux_facteur)
        if dico_adjacence_deux_facteur!={}:
            self.souder_deux_facteur(dico_adjacence_deux_facteur)
        else:
            self.affichage.liste_aretes_cycle=[]
            # print('PAS DE DEUX FACTEUR')

        # self.affichage.liste_aretes_cycle
        """


    """rien"""
    # c'est juste self.suivre_chemin()


    """pomme-queue  naif  avec  modif  chemin"""    #  pas  ok
    #  def  mettre_a_jour_direction(self):
    #      if  self.jeu.pomme_atteinte:
    #          x_a_parcourir=abs(self.jeu.pomme.pos[0]-self.jeu.serpent.pos[0])
    #          y_a_parcourir=abs(self.jeu.pomme.pos[1]-self.jeu.serpent.pos[1])
    #
    #
    #          if  x_a_parcourir<y_a_parcourir:
    #              self.chemin=self.chemin_zig_zag_vertical
    #              self.type_chemin="zig  zag  vertical"
    #              pos_a_eviter=[self.pos_depuis_numero(numero)  for  numero  in  range(self.numero_depuis_pos([self.jeu.pomme.pos[0],self.jeu.serpent.pos[1]]),self.jeu.pomme.numero)]
    #          else:
    #              self.chemin=self.chemin_zig_zag_horizontal
    #              self.type_chemin="zig  zag  horizontal"
    #              pos_a_eviter=[self.pos_depuis_numero(numero)  for  numero  in  range(self.numero_depuis_pos([self.jeu.serpent.pos[0],self.jeu.pomme.pos[1]]),self.jeu.pomme.numero)]
    #
    #
    #      if  self.jeu.serpent.taille_queue==0:
    #          pos_a_eviter=[]
    #      marge=3
    #      if  self.type_chemin=="zig  zag  vertical":
    #
    #          bord_petit_y=marge    #  y  minimum  a  avoir
    #          bord_grand_y=self.affichage.nb_cases-marge-1    #  y  maximum  a  avoir
    #
    #          #  si  on  est  dans  la  bonne  tranche
    #          if  bord_petit_y<=self.jeu.serpent.pos[1]<=bord_grand_y:
    #              #  cas  ou  on  est  au  bon  x,  on  va  a  la  pomme
    #              if  self.jeu.serpent.pos[0]==self.jeu.pomme.pos[0]:
    #  chemin_existe=self.a_etoile(self.jeu.pomme.pos,[])
    #              #  cas  ou  on  n  est  pas  au  bon  x,  on  y  va
    #              else:
    #
    #  #  print(self.numero_depuis_pos([self.jeu.pomme.pos[0],self.jeu.serpent.pos[1]]),self.jeu.pomme.numero)
    #  #  print(pos_a_eviter)
    #  chemin_existe=self.a_etoile([self.jeu.pomme.pos[0],self.jeu.serpent.pos[1]],pos_a_eviter)
    #  self.modifier_cycle()
    #
    #          #  si  on  est  pas  dans  la  bonne  tranche  en  y,  on  y  va
    #          else:
    #              if  np.abs(self.jeu.serpent.pos[1]-bord_petit_y)<=np.abs(self.jeu.serpent.pos[1]-bord_grand_y):
    #
    #  objectif=[self.jeu.serpent.pos[0],bord_petit_y]
    #              else:
    #  objectif=[self.jeu.serpent.pos[0],bord_grand_y]
    #              chemin_existe=self.a_etoile(objectif,[])
    #
    #      elif  self.type_chemin=="zig  zag  horizontal":
    #          bord_petit_x=marge    #  x  minimum  a  avoir
    #          bord_grand_x=self.affichage.nb_cases-marge-1    #  x  maximum  a  avoir
    #
    #          #  si  on  est  dans  la  bonne  tranche
    #          if  bord_petit_x<=self.jeu.serpent.pos[0]<=bord_grand_x:
    #              #  cas  ou  on  est  au  bon  y,  on  va  a  la  pomme
    #              if  self.jeu.serpent.pos[1]==self.jeu.pomme.pos[1]:
    #  chemin_existe=self.a_etoile(self.jeu.pomme.pos,[])
    #              #  cas  ou  on  n  est  pas  au  bon  y,  on  y  va
    #              else:
    #
    #  chemin_existe=self.a_etoile([self.jeu.serpent.pos[0],self.jeu.pomme.pos[1]],pos_a_eviter)
    #  self.modifier_cycle()
    #
    #          #  si  on  est  pas  dans  la  bonne  tranche  en  x,  on  y  va
    #          else:
    #              if  np.abs(self.jeu.serpent.pos[0]-bord_petit_x)<=np.abs(self.jeu.serpent.pos[0]-bord_grand_x):
    #
    #  objectif=[bord_petit_x,self.jeu.serpent.pos[1]]
    #              else:
    #  objectif=[bord_grand_x,self.jeu.serpent.pos[1]]
    #              chemin_existe=self.a_etoile(objectif,[])
    #
    #      print(chemin_existe)
    #      print(self.jeu.serpent.direction)
    #      if  not  chemin_existe:
    #          self.suivre_chemin()
    #
    #
    #      #  try:
    #      #      x_a_parcourir+=1
    #      #      x_a_parcourir-=1
    #      #  except  UnboundLocalError:
    #      #      #  self.a_etoile(self.jeu.pomme.pos,[])
    #      #      return


    






    """pomme-taille (pas  encore  de  modif de cycle)"""  #  ok, faire qu'on change de cycle si possible
    def pomme_moins_queue(self):
        # self.changer_chemin_selon_distance()    #  change  de  chemin  selon  les  prédefinis


        # reset  les  plus  courts  chemins
        if  self.lock:
            # self.plus_court_chemin_ver=[]
            # self.plus_court_chemin_hor=[]
            self.plus_court_chemin=[]

        
    
        # si  on  est  arrive  a  pomme-queue,  on  suit  le  chemin
        numero_pos=self.numero_depuis_pos(self.jeu.serpent.pos)
        if  (self.jeu.pomme.numero-self.jeu.serpent.taille_queue-1)%self.affichage.nb_cases**2==numero_pos:
            self.lock=True
        
    
        if  self.lock:
            self.suivre_chemin()
            return
    
        # aller  a  pomme-queue
        else:
            
            

            # on doit prendre en compte qu'à l'image d'après on grandit
            if  self.jeu.pomme_atteinte:
                pos_pomme_moins_queue=self.pos_depuis_numero((self.jeu.pomme.numero-self.jeu.serpent.taille_queue-1)%self.affichage.nb_cases**2)
                numero_pos_futures=[(self.jeu.pomme.numero-self.jeu.serpent.taille_queue+i)%(self.affichage.nb_cases**2)  for  i  in  range(self.jeu.serpent.taille_queue+1)]
            else:
                pos_pomme_moins_queue=self.pos_depuis_numero((self.jeu.pomme.numero-self.jeu.serpent.taille_queue)%self.affichage.nb_cases**2)
                numero_pos_futures=[(self.jeu.pomme.numero-self.jeu.serpent.taille_queue+i+1)%(self.affichage.nb_cases**2)  for  i  in  range(self.jeu.serpent.taille_queue)]
            
            liste_pos_queue_futures=[self.pos_depuis_numero(numero)  for  numero  in  numero_pos_futures]

            if  not  self.a_etoile(pos_pomme_moins_queue,liste_pos_queue_futures+list(self.jeu.serpent.pos_queue),False):
                self.suivre_chemin()
    
    
        

        
        
    # pas utilisé
    def longer_liste_murs(self,debut,liste_murs,direction_a_traiter): # NE MARCHE PAS
        
        chemin=[]

        # direction_murs=[liste_murs[0][1][0]-liste_murs[0][0][0],liste_murs[0][1][1]-liste_murs[0][0][1]]


        debut_petite_grille=[outils.composante_petite_grille(debut[0]),outils.composante_petite_grille(debut[1])]
        debut_cellule=[debut[0]%2,debut[1]%2]


        if direction_a_traiter==[1,0]:

            # on sait debut_cellule[0]=0
            if debut_cellule==[0,0]:

                direction_initiale=[0,1]
            
            elif debut_cellule==[0,1]:

                if self.appartient([debut_petite_grille,[debut_petite_grille[0],debut_petite_grille[1]+1]],liste_murs):
                    direction_initiale=[0,1]
                
                else:
                    direction_initiale=[1,0]
        
        elif direction_a_traiter==[0,-1]:

            # on sait debut_cellule[1]=1
            if debut_cellule==[0,1]:

                direction_initiale=[1,0]
            
            elif debut_cellule==[0,1]:

                if self.appartient([debut_petite_grille,[debut_petite_grille[0]+1,debut_petite_grille[1]]],liste_murs):
                    direction_initiale=[1,0]
                
                else:
                    direction_initiale=[0,-1]
        
        elif direction_a_traiter==[-1,0]:

            # on sait debut_cellule[0]=1
            if debut_cellule==[1,1]:

                direction_initiale=[0,-1]
            
            elif debut_cellule==[1,0]:

                if self.appartient([debut_petite_grille,[debut_petite_grille[0],debut_petite_grille[1]-1]],liste_murs):
                    direction_initiale=[0,-1]
                
                else:
                    direction_initiale=[-1,0]
        
        elif direction_a_traiter==[0,1]:

            # on sait debut_cellule[1]=0
            if debut_cellule==[1,0]:

                direction_initiale=[-1,0]
            
            elif debut_cellule==[0,0]:

                if self.appartient([debut_petite_grille,[debut_petite_grille[0]-1,debut_petite_grille[1]]],liste_murs):
                    direction_initiale=[-1,0]
                
                else:
                    direction_initiale=[0,1]



        # # pour doublons
        # ajouter=[]
        # for  couple  in  liste_murs:
        #     ajouter.append([couple[1][:],couple[0][:]])

        # liste_murs+=ajouter
        


        liste_pos_occupees_petite_grille=[]
        for pos in chemin:
            pos_petite_grille=[outils.composante_petite_grille(pos[0]),outils.composante_petite_grille(pos[1])]
            if not pos_petite_grille in liste_pos_occupees_petite_grille:
                liste_pos_occupees_petite_grille.append(pos_petite_grille)
        
        # print(debut)
        
        # iteration_max=4*(len(liste_murs)+1)//2

           
        

        if direction_a_traiter==[0,1]:
            direction_gauche=[1,0]
        elif direction_a_traiter==[0,-1]:
            direction_gauche=[-1,0]
        elif direction_a_traiter==[1,0]:
            direction_gauche=[0,-1]
        elif direction_a_traiter==[-1,0]:
            direction_gauche=[0,1]
        

        fin=[debut[0]+direction_gauche[0],debut[1]+direction_gauche[1]]

        

        print('debut,fin',debut,fin)
        # print('direction',direction)
        

        chemin=self.temp(liste_murs,debut,fin,direction_initiale)    
        return chemin

        
        # n=self.affichage.nb_cases//2

        # pos=debut[:]
        # direction=direction_initiale[:]

        # chemin=[]
        # while pos!=fin:

        #     # print(pos)
            
        
        #     pos_petite_grille=[outils.composante_petite_grille(pos[0]),outils.composante_petite_grille(pos[1])]
            

        #     if direction==[1,0]:

        #         if pos[0]%2==0:

        #             # on veut aller en bas
        #             if pos_petite_grille[1]<=n-1 and self.appartient([pos_petite_grille,[pos_petite_grille[0],pos_petite_grille[1]+1]],liste_murs):
        #                 direction=[0,1]
                
        #         else:
                    
        #             # on veut aller en haut
        #             if pos_petite_grille[1]>=0 and self.appartient([[pos_petite_grille[0],pos_petite_grille[1]-1],pos_petite_grille],liste_murs):
        #                 direction=[0,-1]
                    
        #             if pos_petite_grille[0]==n-1:
        #                 direction=[0,-1]


        #     if direction==[0,1]:

        #         if pos[1]%2==0:

        #             # on veut aller a gauche
        #             if pos_petite_grille[0]>=0 and self.appartient([pos_petite_grille,[pos_petite_grille[0]-1,pos_petite_grille[1]]],liste_murs):
        #                 direction=[-1,0]
                
        #         else:
                    
        #             # on veut aller a droite
        #             if pos_petite_grille[1]<=n-1 and self.appartient([pos_petite_grille,[pos_petite_grille[0]+1,pos_petite_grille[1]]],liste_murs):
        #                 direction=[0,-1]
                    
        #             if pos_petite_grille[1]==n-1:
        #                 direction=[1,0]
            

        #     if direction==[0,-1]:

        #         if pos[0]%2==1:

        #             # on veut aller a droite
        #             if pos_petite_grille[0]<=n-1 and self.appartient([[pos_petite_grille[0]+1,pos_petite_grille[1]],pos_petite_grille],liste_murs):
        #                 direction=[1,0]
                
        #         else:
                    
        #             # on veut aller a gauche
        #             if pos_petite_grille[0]>=0 and self.appartient([pos_petite_grille,[pos_petite_grille[0]-1,pos_petite_grille[1]]],liste_murs):
        #                 direction=[0,-1]

        #             if pos_petite_grille[1]==0:
        #                 direction=[-1,0]
            

        #     if direction==[-1,0]:

        #         if pos[0]%2==1:

        #             # on veut aller en haut
        #             if pos_petite_grille[1]<=n-1 and self.appartient([pos_petite_grille,[pos_petite_grille[0],pos_petite_grille[1]-1]],liste_murs):
        #                 direction=[0,-1]
                
        #         else:
                    
        #             # on veut aller en bas
        #             if pos_petite_grille[1]>=0 and self.appartient([pos_petite_grille,[pos_petite_grille[0],pos_petite_grille[1]+1]],liste_murs):
        #                 direction=[0,1]
                    
        #             if pos_petite_grille[0]==0:
        #                 direction=[0,1]

        #     pos=[pos[0]+direction[0],pos[1]+direction[1]]
        #     chemin.append(pos[:])
        
        
        # return chemin
    

    def temp(self,liste_murs,debut,fin,direction_initiale):
        # chemin=np.array([[0  for  _  in  range(self.affichage.nb_cases)]  for  _  in  range(self.affichage.nb_cases)])
        # chemin=np.zeros((self.affichage.nb_cases,self.affichage.nb_cases))
        chemin=[]

        n=self.affichage.nb_cases//2

        pos=debut[:]
        compteur=0
        direction=direction_initiale[:]
        while  pos!=fin and compteur<64:

            print(pos[:])

            pos_n=[outils.composante_petite_grille(pos[0]),outils.composante_petite_grille(pos[1])]
            if  direction==[1,0]:    #  j  pair
                if  pos[0]%2==0:
                    if  pos_n[1]-1>=0  and  [pos_n,[pos_n[0],pos_n[1]-1]]  in  liste_murs:
                        direction=[0,-1]
                elif  pos_n[0]+1>n-1  or  not  [pos_n,[pos_n[0]+1,pos_n[1]]]  in  liste_murs:
                    if  [pos_n,[pos_n[0],pos_n[1]+1]]  in  liste_murs  or  True:
                        direction=[0,1]

            elif  direction==[-1,0]:      #  j  impair
                if    pos[0]%2==1:
                    if  [pos_n,[pos_n[0],pos_n[1]+1]]  in  liste_murs:
                        direction=[0,1]
                elif  pos_n[0]-1<0  or  not  [pos_n,[pos_n[0]-1,pos_n[1]]]  in  liste_murs:
                    if  [pos_n,[pos_n[0],pos_n[1]-1]]  in  liste_murs  or  True:
                        direction=[0,-1]

            elif  direction==[0,1]:    #  i  impair
                if  pos[1]%2==0:
                    if  pos_n[0]+1<=n-1  and  [pos_n,[pos_n[0]+1,pos_n[1]]]  in  liste_murs:
                        direction=[1,0]
                elif  pos_n[1]+1>n-1  or  not  [pos_n,[pos_n[0],pos_n[1]+1]]  in  liste_murs:
                    if  [pos_n,[pos_n[0]-1,pos_n[1]]]  in  liste_murs  or  True:
                        direction=[-1,0]

            elif  direction==[0,-1]:    #  i  pair
                if  pos[1]%2==1:
                    if  [pos_n,[pos_n[0]-1,pos_n[1]]]  in  liste_murs:
                        direction=[-1,0]
                elif  pos_n[1]-1<0  or  not  [pos_n,[pos_n[0],pos_n[1]-1]]  in  liste_murs:
                    if  [pos_n,[pos_n[0]+1,pos_n[1]]]  in  liste_murs  or  True:
                        direction=[1,0]



            pos[0]+=direction[0]
            pos[1]+=direction[1]

            #  print(pos,  direction)
            compteur+=1
            chemin.append(pos[:])

        return chemin


    def appartient(self,couple,liste_couples):
        return [couple[0],couple[1]] in liste_couples or [couple[1],couple[1]] in liste_couples
            

    
    def coupe_grille(self,liste_pos):
        
        # print('a',liste_pos_corps,chemin)
        
        
        # print('liste',liste_pos_corps_apres_deplacement)
        for i in range(len(liste_pos)):
            
            
            pos=liste_pos[i]

            if i<len(liste_pos)-1:
                pos_suivante=liste_pos[i+1]
                direction_pos=[pos_suivante[0]-pos[0],pos_suivante[1]-pos[1]]
            elif i==len(liste_pos)-1:
                if len(liste_pos)==1:
                    continue
                direction_pos=[pos[0]-liste_pos[-2][0],pos[1]-liste_pos[-2][1]]

            # print(len(liste_pos_corps_apres_deplacement))

            liste_pos_corps=list(self.jeu.serpent.pos_queue)+[self.jeu.serpent.pos]
            liste_pos_corps_apres_deplacement=self.liste_pos_apres_deplacement_chemin(liste_pos_corps,self.plus_court_chemin)
            # print(liste_pos_corps_apres_ deplacement)
            if direction_pos[0]==0:

                # il faut regarder à droite et gauche
                if pos[0]!=0 and pos[0]!=self.affichage.nb_cases-1:
                    if [pos[0]-1,pos[1]] not in liste_pos:
                        nb_cases_libres_gauche=self.parcours_largeur_compter([pos[0]-1,pos[1]],liste_pos_corps_apres_deplacement)
                    else:
                        # on s'en fiche si on longe un bord
                        continue

                    if [pos[0]+1,pos[1]] not in liste_pos:
                        nb_cases_libres_droite=self.parcours_largeur_compter([pos[0]+1,pos[1]],liste_pos_corps_apres_deplacement)
                    else:
                        # on s'en fiche si on longe un bord
                        continue
                    
                    print(nb_cases_libres_gauche,nb_cases_libres_droite)
                    if nb_cases_libres_gauche!=0 and nb_cases_libres_gauche!=self.affichage.nb_cases**2-len(liste_pos_corps_apres_deplacement):
                        print('a')
                        return (True,pos)
                    if nb_cases_libres_droite!=0 and nb_cases_libres_droite!=self.affichage.nb_cases**2-len(liste_pos_corps_apres_deplacement):
                        print('a')
                        return (True,pos)
                    
                    if nb_cases_libres_gauche!=0 and nb_cases_libres_droite!=0 and not self.a_etoile_neutre([pos[0]-1,pos[1]],[pos[0]+1,pos[1]],liste_pos_corps_apres_deplacement,False):
                        print('b')
                        return (True,pos)
            
            if direction_pos[1]==0:

                # il faut regarder en haut et bas
                if pos[1]!=0 and pos[1]!=self.affichage.nb_cases-1:
                    if [pos[0],pos[1]-1] not in liste_pos:
                        nb_cases_libres_haut=self.parcours_largeur_compter([pos[0],pos[1]-1],liste_pos_corps_apres_deplacement)
                    else:
                        # on s'en fiche si on longe un bord
                        continue
                    if [pos[0],pos[1]+1] not in liste_pos:
                        nb_cases_libres_bas=self.parcours_largeur_compter([pos[0],pos[1]+1],liste_pos_corps_apres_deplacement)
                    else:
                        # on s'en fiche si on longe un bord
                        continue
                    
                    print(nb_cases_libres_haut,nb_cases_libres_bas)
                    if nb_cases_libres_haut!=0 and nb_cases_libres_haut!=self.affichage.nb_cases**2-len(liste_pos_corps_apres_deplacement):
                        print('a')
                        return (True,pos)
                    if nb_cases_libres_bas!=0 and nb_cases_libres_bas!=self.affichage.nb_cases**2-len(liste_pos_corps_apres_deplacement):
                        print('a')
                        return (True,pos)

                    if nb_cases_libres_haut!=0 and nb_cases_libres_bas!=0 and not self.a_etoile_neutre([pos[0],pos[1]+1],[pos[0],pos[1]-1],liste_pos_corps_apres_deplacement,False):
                        print('b')
                        return (True,pos)
        
        
            
            

        return (False,None)
            




    def parcours_largeur_compter(self,debut,liste_pos_corps):
        if debut in liste_pos_corps:
            return 0
        a_traiter=collections.deque([debut])
        deja_traites=[]
        vide=collections.deque([])
        

        while a_traiter!=vide:
            pos=a_traiter.popleft()
            if not pos in deja_traites and not pos in a_traiter:
                
                liste_voisins=self.voisins(pos)
                for voisin in liste_voisins:
                    if not voisin in liste_pos_corps:
                        a_traiter.append(voisin[:])

                deja_traites.append(pos[:])
        
        # print(deja_traites)
        return len(deja_traites)







    def  changer_chemin_selon_distance(self): #pas utilisé
        # comparer  longueur  des  plus  court  chemin
        if  self.jeu.pomme_atteinte:    #  sur  pomme


            longueur_chemin_zigzag_vertical=0
            longueur_chemin_zigzag_horizontal=0

            #  vertical
            self.chemin=self.chemin_zig_zag_vertical

            liste_numeros_futures=[(self.numero_depuis_pos(self.jeu.pomme.pos)-self.jeu.serpent.taille_queue+i)%self.affichage.nb_cases**2  for  i  in  range(self.jeu.serpent.taille_queue+1)]
            liste_pos_queue_futures=[self.pos_depuis_numero(numero)  for  numero  in  liste_numeros_futures]

            for  pos  in  self.jeu.serpent.pos_queue:
                if  pos  in  liste_pos_queue_futures:
                    longueur_chemin_zigzag_vertical=inf
                    # print('inf')
                    break

            if  longueur_chemin_zigzag_vertical!=inf:
                self.a_etoile(self.pos_depuis_numero((self.numero_depuis_pos(self.jeu.pomme.pos)-self.jeu.serpent.taille_queue-1)%self.affichage.nb_cases**2),liste_pos_queue_futures)
                longueur_chemin_zigzag_vertical=len(self.plus_court_chemin)
                self.plus_court_chemin_ver=self.plus_court_chemin[:]
                # print(self.plus_court_chemin)


            # horizontal
            self.chemin=self.chemin_zig_zag_horizontal

            liste_numeros_futures=[(self.numero_depuis_pos(self.jeu.pomme.pos)-self.jeu.serpent.taille_queue+i)%self.affichage.nb_cases**2  for  i  in  range(self.jeu.serpent.taille_queue+1)]
            liste_pos_queue_futures=[self.pos_depuis_numero(numero)  for  numero  in  liste_numeros_futures]

            for  pos  in  self.jeu.serpent.pos_queue:
                if  pos  in  liste_pos_queue_futures:
                    longueur_chemin_zigzag_horizontal=inf
                    # print('inf')
                    break

            if  longueur_chemin_zigzag_horizontal!=inf:

                self.a_etoile(self.pos_depuis_numero((self.numero_depuis_pos(self.jeu.pomme.pos)-self.jeu.serpent.taille_queue-1)%self.affichage.nb_cases**2),liste_pos_queue_futures)
                longueur_chemin_zigzag_horizontal=len(self.plus_court_chemin)
                self.plus_court_chemin_hor=self.plus_court_chemin[:]
                # print(self.plus_court_chemin)


            # comparaison
            if  longueur_chemin_zigzag_vertical<longueur_chemin_zigzag_horizontal:
                self.chemin=self.chemin_zig_zag_vertical
                # print('verti')
            elif  longueur_chemin_zigzag_vertical>longueur_chemin_zigzag_horizontal:
                self.chemin=self.chemin_zig_zag_horizontal
                # print('hori')

            # print(longueur_chemin_zigzag_vertical,longueur_chemin_zigzag_horizontal)

        self.affichage.actualiser_pomme()

    def  aller_a_pomme_sur_cycle_croissant(self):    #  regarde  le  voisin  qui  rapproche  le  plus  de  la  pomme  selon  le  cycle, pas ok
        # pas ok

        liste_voisins=[voisin  for  voisin  in  self.voisins(self.jeu.serpent.pos)  if  voisin  not  in  self.jeu.serpent.pos_queue]

        voisin_objectif=min(liste_voisins,key=lambda  pos:self.numero_depuis_pos(self.jeu.pomme.pos)-self.numero_depuis_pos(pos))

        #  print(liste_voisins)
        #  print(voisin_objectif)

        self.jeu.serpent.direction[0]=voisin_objectif[0]-self.jeu.serpent.pos[0]
        self.jeu.serpent.direction[1]=voisin_objectif[1]-self.jeu.serpent.pos[1]



    #  def  mettre_a_jour_direction(self):
    #      if  self.chemin[self.jeu.serpent.pos[1]][self.jeu.serpent.pos[0]]<self.jeu.pomme.numero:
    #          if  self.raccourci_croissant():
    #              if  not  self.modifier_cycle():
    #  self.suivre_chemin()
    #          else:
    #              self.suivre_chemin()
    #      else:
    #          if  self.aller_vers_0():
    #              if  not  self.modifier_cycle():
    #  self.suivre_chemin()
    #          elif  self.reprendre_cycle():
    #              if  not  self.modifier_cycle():
    #  self.suivre_chemin()
    #          else:
    #              self.suivre_chemin()


    def  inverser_grille(self):
        for  i  in  range(self.affichage.nb_cases):
            for  j  in  range(self.affichage.nb_cases):
                self.chemin[i][j]=(self.affichage.nb_cases**2)-self.chemin[i][j]
        self.chemin[0][0]=0

    def  numero_max_corps(self):
        if  self.jeu.serpent.pos_queue==[]:
            return  0
        else:
            return  max([self.numero_depuis_pos(pos)  for  pos  in  self.jeu.serpent.pos_queue])



    def  raccourci(self):
        pos=self.jeu.serpent.pos
        pos_suivante=[pos[0]+self.jeu.serpent.direction[0],pos[1]+self.jeu.serpent.direction[1]]

        numero=self.numero_depuis_pos(pos)
        numero_suivant=self.numero_depuis_pos(pos_suivante)

        if  abs(self.jeu.pomme.numero-numero_suivant)>=self.jeu.serpent.taille_queue:
            return(True)
        else:
            return(False)

    def  soustraire(self,offset):
        #  print(self.jeu.serpent.pos)
        #  print(self.numero_depuis_pos(self.jeu.serpent.pos))
        for  i  in  range(self.affichage.nb_cases):
            for  j  in  range(self.affichage.nb_cases):
                #  print(self.chemin[i,j]-offset)
                self.chemin[i,j]=(self.chemin[i,j]-offset)%(self.affichage.nb_cases**2)
        self.jeu.pomme.numero=self.numero_depuis_pos(self.jeu.pomme.pos)



    def  raccourci_croissant(self):
        directions_possibles=[]
        for  j  in  range(-1,2):
            for  i  in  range(-1,2):
                if  i*j==0  and  self.jeu.serpent.pos[0]+j>=0  and  self.jeu.serpent.pos[0]+j<=self.affichage.nb_cases-1  and  self.jeu.serpent.pos[1]+i>=0  and  self.jeu.serpent.pos[1]+i<=self.affichage.nb_cases-1:    #  verif  que  les  directions  sont  ok


                    if  self.chemin[self.jeu.serpent.pos[1]][self.jeu.serpent.pos[0]]+1<self.chemin[self.jeu.serpent.pos[1]+i][self.jeu.serpent.pos[0]+j]<=self.jeu.pomme.numero:    #  croissance  du  numéro

                        a_parcourir=self.jeu.pomme.numero-self.chemin[self.jeu.serpent.pos[1]+i][self.jeu.serpent.pos[0]+j]
                        #  a_parcourir=inf      #  debut  de  la  modif  pour  enlever  la  marge
                        if  a_parcourir>=self.jeu.serpent.taille_queue:    #  assez  de  place

                            directions_possibles.append([j,i])
                        if  directions_possibles!=[]:
                            self.jeu.serpent.direction=max(directions_possibles,key=self.numero_depuis_pos)
                            #  print(directions_possibles)
                            #  print(self.jeu.serpent.direction)
                            return(True)
                        else:
                            return(False)

    def  aller_vers_0(self):    #  aller  vers  0
        directions_possibles={}
        for  j  in  range(-1,2):
            for  i  in  range(-1,2):
                if  i*j==0  and  self.jeu.serpent.pos[0]+j>=0  and  self.jeu.serpent.pos[0]+j<=self.affichage.nb_cases-1  and  self.jeu.serpent.pos[1]+i>=0  and  self.jeu.serpent.pos[1]+i<=self.affichage.nb_cases-1:    #  verif  que  les  directions  sont  ok


                    if  self.chemin[self.jeu.serpent.pos[1]][self.jeu.serpent.pos[0]]<self.chemin[self.jeu.serpent.pos[1]+i][self.jeu.serpent.pos[0]+j]:    #  croissance  du  numéro

                        #  a_parcourir=self.affichage.nb_cases**2-1-self.chemin[self.jeu.serpent.pos[1]+i][self.jeu.serpent.pos[0]+j]+self.jeu.pomme.pos[0]+self.jeu.pomme.pos[1]
                        a_parcourir=self.affichage.nb_cases**2-1-self.chemin[self.jeu.serpent.pos[1]+i][self.jeu.serpent.pos[0]+j]
                        if  a_parcourir>self.jeu.serpent.taille_queue:    #  assez  de  place
                            directions_possibles[j,i]=self.chemin[self.jeu.serpent.pos[1]+i][self.jeu.serpent.pos[0]+j]
                        if  directions_possibles!={}:
                            self.jeu.serpent.direction=max(directions_possibles)
                            return(True)
                        else:
                            return(False)

    def  reprendre_cycle(self):
        directions_possibles={}
        for  j  in  range(-1,2):
            for  i  in  range(-1,2):
                if  i*j==0  and  self.jeu.serpent.pos[0]+j>=0  and  self.jeu.serpent.pos[0]+j<=self.affichage.nb_cases-1  and  self.jeu.serpent.pos[1]+i>=0  and  self.jeu.serpent.pos[1]+i<=self.affichage.nb_cases-1:    #  verif  que  les  directions  sont  ok


                    if  self.chemin[self.jeu.serpent.pos[1]][self.jeu.serpent.pos[0]]>=self.jeu.pomme.numero>=self.chemin[self.jeu.serpent.pos[1]+i][self.jeu.serpent.pos[0]+j]:    #  croissance  du  numéro
                        #  print('veut')
                        a_parcourir=self.jeu.pomme.numero-self.chemin[self.jeu.serpent.pos[1]+i][self.jeu.serpent.pos[0]+j]
                        if  a_parcourir>self.jeu.serpent.taille_queue:    #  assez  de  place
                            directions_possibles[j,i]=self.chemin[self.jeu.serpent.pos[1]+i][self.jeu.serpent.pos[0]+j]
                        if  directions_possibles!={}:
                            self.jeu.serpent.direction=max(directions_possibles)
                            return(True)
                        else:
                            return(False)

    def recuperer_deux_boucles(self):
        self.pos_boucle_1=[]
        self.pos_boucle_2=[]


        numero_actuel=self.numero_depuis_pos(self.jeu.serpent.pos)
        numero_desire=self.numero_depuis_pos([self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]])

        # if  numero_desire>=numero_actuel:
        #     difference_numero=numero_desire-numero_actuel
        # else:
        #     difference_numero=numero_actuel-numero_desire

        difference_numero=abs(numero_desire-numero_actuel)
        
        # if difference_numero>10000:
        #     print('probleme difference numero')

        if  difference_numero  in  [-1,0,1,self.affichage.nb_cases**2-1]:
            return  False



        #  etablissement  des  pos  des  deux  boucles
        pos_boucle_1=[]
        pos_boucle_2=[]

        boucle_actuelle=1

        # pour savoir comment on recolle, depend de si c'est un raccourci croissant ou non
        parite=None

        direction=self.jeu.serpent.direction

        pos_suivante=[self.jeu.serpent.pos[0]+direction[0],self.jeu.serpent.pos[1]+direction[1]]


        if  len(self.jeu.serpent.pos_queue)==0:
            # print('len(queue)=1')
            # on s'en fiche
            parite=1
        else:
            #  cas  ou  on  est  croissant
            if  self.numero_depuis_pos(self.jeu.serpent.pos_queue[-1])<self.numero_depuis_pos(self.jeu.serpent.pos):
                # print('croissant')
                #  raccourci  croissant
                if  self.numero_depuis_pos(pos_suivante)>self.numero_depuis_pos(self.jeu.serpent.pos):
                    parite=1
                else:
                    parite=2
            #  cas  ou  on  est  decroissant
            else:
                # print('décroissant')
                #  raccourci  croissant
                if  self.numero_depuis_pos(pos_suivante)>self.numero_depuis_pos(self.jeu.serpent.pos):
                    parite=2
                else:
                    parite=1

        #  parite=1






        pos=[0,0]      #  a  l'origine
        for  _  in  range(self.affichage.nb_cases**2):
            
            direction=self.direction_suivante(pos[:])

            pos_suivante=[pos[0]+direction[0],pos[1]+direction[1]]
            # print('b pos_suivante',pos_suivante)

            #  print(boucle_actuelle,pos)

            if  self.numero_depuis_pos(pos[:])!=numero_actuel  and  self.numero_depuis_pos(pos[:])!=numero_desire:
                if  boucle_actuelle==1:
                    pos_boucle_1.append(pos[:])
                elif  boucle_actuelle==2:
                    pos_boucle_2.append(pos[:])

            elif  self.numero_depuis_pos(pos[:])==numero_actuel  or  self.numero_depuis_pos(pos[:])==numero_desire:
                #  print('atteint')
                if  boucle_actuelle==1:
                    boucle_actuelle=2
                elif  boucle_actuelle==2:
                    boucle_actuelle=1
                if  parite==1:
                    pos_boucle_1.append(pos[:])
                else:
                    pos_boucle_2.append(pos[:])


            pos[:]=pos_suivante[:]

        """s'en occuper"""
        #  si  les  deux  boucles  ne  sont  pas  faites  au  bon  endroit
        if  len(self.jeu.serpent.pos_queue)==0:


            if  abs(pos_boucle_2[0][0]-pos_boucle_2[-1][0])  not  in  [0,1]  or  abs(pos_boucle_2[0][1]-pos_boucle_2[-1][1])  not  in  [0,1]:
                #  print(difference(pos_boucle_2[-1][0],pos_boucle_2[-1][1]))
                pos_boucle_1.remove(self.pos_depuis_numero(numero_actuel))
                pos_boucle_1.remove(self.pos_depuis_numero(numero_desire))
                pos_boucle_2.insert(0,self.pos_depuis_numero(min(numero_actuel,numero_desire)))
                pos_boucle_2.append(self.pos_depuis_numero(max(numero_actuel,numero_desire)))

                # print('correction')


        #  si  on  veut  les  voir
        self.pos_boucle_1=pos_boucle_1
        self.pos_boucle_2=pos_boucle_2


        #  on  verifie  que  les  deux  boucles  sont  bien  des  boucles
        if  abs(pos_boucle_2[0][0]-pos_boucle_2[-1][0])  not  in  [0,1]  or  abs(pos_boucle_2[0][1]-pos_boucle_2[-1][1])  not  in  [0,1]:
            # print('boucle 2 pas boucle')
            return  False

        if  abs(pos_boucle_1[0][0]-pos_boucle_1[-1][0])  not  in  [0,1]  or  abs(pos_boucle_1[0][1]-pos_boucle_1[-1][1])  not  in  [0,1]:
            # print('boucle 1 pas boucle')
            return  False

        for  i  in  range(len(pos_boucle_1)-1):
            if  pos_boucle_1[i]  not  in  self.voisins(pos_boucle_1[i+1]):
                # print('boucle 1 pas boucle')
                return  False

        for  i  in  range(len(pos_boucle_2)-1):
            if  pos_boucle_2[i]  not  in  self.voisins(pos_boucle_2[i+1]):
                # print('boucle 2 pas boucle')
                return  False

        return [pos_boucle_1,pos_boucle_2]

    def souder_deux_boucles(self,pos_boucle_1,pos_boucle_2):
        

        numero_actuel=self.numero_depuis_pos(self.jeu.serpent.pos)
        numero_desire=self.numero_depuis_pos([self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]])

        # print(self.jeu.score)

        

        


        #  on  cherche  a  recoller  les  boucles
        pos_boucle=pos_boucle_1[:]

        depart_arrivee_1=[]
        depart_arrivee_2=[]

        for  i  in  range(len(pos_boucle)-1):

            liste_voisins=self.voisins(pos_boucle[i])
            liste_voisins_suivant=self.voisins(pos_boucle[i+1])

            

            #  on  regarde  les  voisinages
            for  voisin  in  liste_voisins:

                #  si  on  a  trouvé
                if  depart_arrivee_1!=[]:
                    break

                for  voisin_suivant  in  liste_voisins_suivant:

                    #  pour  recoller  entre  les  deux  boucles
                    if  voisin  not  in  pos_boucle  and  voisin_suivant  not  in  pos_boucle:

                        #  pour  ne  pas  recoller  la  ou  on  va  ou  est
                        # print(self.numero_depuis_pos(voisin),self.numero_depuis_pos(voisin_suivant),self.numero_depuis_pos(pos_boucle[i][:]),self.numero_depuis_pos(pos_boucle[i+1][:]))
                        if  self.numero_depuis_pos(voisin)  not  in  [numero_actuel,numero_desire]  and  self.numero_depuis_pos(voisin_suivant)  not  in  [numero_actuel,numero_desire]  and  self.numero_depuis_pos(pos_boucle[i][:])  not  in  [numero_actuel,numero_desire]  and  self.numero_depuis_pos(pos_boucle[i+1][:])  not  in  [numero_actuel,numero_desire]:

                            # pour ne pas recoller sur la queue
                            if  pos_boucle[i][:]  not  in  self.jeu.serpent.pos_queue  and  pos_boucle[i+1][:]  not  in  self.jeu.serpent.pos_queue  and  voisin[:]  not  in  self.jeu.serpent.pos_queue  and  voisin_suivant[:]  not  in  self.jeu.serpent.pos_queue:
                                if  abs(self.numero_depuis_pos(voisin)-self.numero_depuis_pos(voisin_suivant))==1:
                                    depart_arrivee_1=[pos_boucle[i][:],pos_boucle[i+1][:]]
                                    depart_arrivee_2=[voisin[:],voisin_suivant[:]]
                                    break

                            if  depart_arrivee_1!=[]:
                                break
        
        return depart_arrivee_1,depart_arrivee_2
                        

        

    def modifier_cycle(self,listes_boucles):
        if len(listes_boucles)==2:
            pos_boucle_1,pos_boucle_2=listes_boucles[0],listes_boucles[1]

            depart_arrivee_1,depart_arrivee_2=self.souder_deux_boucles(pos_boucle_1,pos_boucle_2)

            if  depart_arrivee_1==[]:
                # print('pas  boucle')
                return  False
                
            # print(depart_arrivee_1,depart_arrivee_2)

            self.reindicer_chemin(depart_arrivee_1,depart_arrivee_2,pos_boucle_1,pos_boucle_2)

            return True
        
        else:
            # if True:
            # print('liste boucles',listes_boucles)
            while len(listes_boucles)>1:
                # print('liste_boucles',listes_boucles)


                pos_boucle_1=listes_boucles[0]

                depart_arrivee_1,depart_arrivee_2=[],[]
                for i,pos in enumerate(pos_boucle_1):
                    
                    # si déjà trouvé
                    if depart_arrivee_1!=[]:
                        break
                    
                    # on ne regarde pas ce qui est dans serpent
                    if pos in self.jeu.serpent.pos_queue or pos==self.jeu.serpent.pos:
                        continue

                    liste_voisins=[pos_ for pos_ in self.voisins(pos) if pos_ not in pos_boucle_1 and pos_ not in self.jeu.serpent.pos_queue and pos_!=self.jeu.serpent.pos]

                    for boucle in listes_boucles:
                        
                        # si déjà trouvé
                        if depart_arrivee_1!=[]:
                            break
                        
                        # inutile de regarder la meme boucle
                        if boucle==pos_boucle_1:
                            continue
                        
                        # on regarde les voisins
                        for voisin in liste_voisins:
                            
                            # on ne regarde pas ce qui est dans serpent
                            if voisin in self.jeu.serpent.pos_queue or voisin==self.jeu.serpent.pos:
                                continue
                            
                            # si déjà trouvé
                            if depart_arrivee_1!=[]:
                                break

                            # voisin candidat pour etre depart
                            if voisin in boucle:

                                # on regarde la pos suivante
                                if i==len(pos_boucle_1)-1:
                                    pos_suivante=pos_boucle_1[0]
                                else:
                                    pos_suivante=pos_boucle_1[i+1]


                                liste_voisins_pos_suivante=[pos_ for pos_ in self.voisins(pos_suivante) if pos_ not in pos_boucle_1 and pos_ in boucle]

                                if liste_voisins_pos_suivante==[]:
                                    continue

                                # s'il y a un voisin (de pos_suivante) dans boucle
                                numero_voisin=self.numero_depuis_pos(voisin)
                                for voisin_pos_suivante in liste_voisins_pos_suivante:
                                    if voisin_pos_suivante in self.jeu.serpent.pos_queue or pos==self.jeu.serpent.pos:
                                        continue
                                    numero_voisin_pos_suivante=self.numero_depuis_pos(voisin_pos_suivante)

                                    # condition d'adjacence
                                    # if abs(numero_voisin_pos_suivante-numero_voisin)==1:
                                    # print('se_suivent',boucle,voisin_pos_suivante,voisin,self.se_suivent(boucle,voisin_pos_suivante,voisin))
                                    if self.se_suivent(boucle,voisin_pos_suivante,voisin):
                                        depart_arrivee_1=[pos[:],pos_suivante[:]]
                                        depart_arrivee_2=[voisin[:],voisin_pos_suivante[:]]
                                        pos_boucle_2=boucle
                                        # print('depart arrivée 1 et 2',depart_arrivee_1,depart_arrivee_2)
                                        break

                            


                if  depart_arrivee_1==[]:
                    # print('pas  boucle')
                    # print(pos_boucle_1)
                    return  False
                
                # print(depart_arrivee_1,depart_arrivee_2)


                # coller les boucles
                pos_boucle_3=[]

                indice_depart_1=pos_boucle_1.index(depart_arrivee_1[0])
                indice_depart_2=pos_boucle_2.index(depart_arrivee_2[0])

                pos_boucle_3+=pos_boucle_1[:(indice_depart_1+1)]

                pos_boucle_3+=pos_boucle_2[indice_depart_2:]
                pos_boucle_3+=pos_boucle_2[:indice_depart_2]

                pos_boucle_3+=pos_boucle_1[(indice_depart_1+1):]


                # for pos in pos_boucle_3:
                #     print(self.numero_depuis_pos(pos))
                
                listes_boucles.remove(pos_boucle_1)
                listes_boucles.remove(pos_boucle_2)
                
                listes_boucles.append(pos_boucle_3)


                # print(depart_arrivee_1,depart_arrivee_2)

            # self.reindicer_chemin(depart_arrivee_1,depart_arrivee_2,pos_boucle_1,pos_boucle_2)
            
            for compteur,pos in enumerate(listes_boucles[0]):
                # print(self.numero_depuis_pos(pos))
                self.chemin[pos[1],pos[0]]=compteur
            
            self.affichage.liste_aretes_cycle=self.affichage.initialiser_liste_aretes_cycle()

            return True
    
    def se_suivent(self,boucle,pos1,pos2):
        for i,pos in enumerate(boucle):
            if i==len(boucle)-1:
                if pos==pos1 and pos2==boucle[0]:
                    return True
            else:
                if pos==pos1 and pos2==boucle[i+1]:
                    return True
        return False
        

    def ensemble_boucles_depuis_dico_adjacence(self,dico_adjacence):   # pour deux facteur
        liste_boucles=[]
        sommets_depart_deja_traites=[]
        for x in range(self.affichage.nb_cases):
            for y in range(self.affichage.nb_cases):
                if not [x,y] in sommets_depart_deja_traites:
                    pos=[x,y]
                    deja_traites=[[pos[0],pos[1]]]
                    
                    pos=dico_adjacence[(pos[0],pos[1])][0]
                    a_traiter=collections.deque([[pos[0],pos[1]]])

                    vide=collections.deque([])
                    while a_traiter!=vide:
                        pos=a_traiter.popleft()
                        deja_traites.append([pos[0],pos[1]])
                        sommets_depart_deja_traites.append([pos[0],pos[1]])
                        for voisin in dico_adjacence[(pos[0],pos[1])]:
                            if not [voisin[0],voisin[1]] in deja_traites and not [voisin[0],voisin[1]] in a_traiter:
                                a_traiter.append([voisin[0],voisin[1]])
                                sommets_depart_deja_traites.append([voisin[0],voisin[1]])
                                

                    liste_boucles.append(deja_traites)
                    # print('AAAA LISTE BOUCLE',liste_boucles)
                    sommets_depart_deja_traites.append([pos[0],pos[1]])

        # print(liste_boucles)
        return liste_boucles








        
    def reindicer_chemin(self,depart_arrivee_1,depart_arrivee_2,pos_boucle_1,pos_boucle_2):
        

        pos_boucle=pos_boucle_1
        
        
        # print(depart_arrivee_1,depart_arrivee_2)

        #  on  reindice
        pos=[0,0]
        pos_suivante=None
        nouveau_cycle_hami=copy.deepcopy(self.chemin)
        for  _  in  range(self.affichage.nb_cases**2):

            if  pos==depart_arrivee_1[0]:
                pos_suivante=depart_arrivee_2[0]
            elif  pos==depart_arrivee_2[1]:
                pos_suivante=depart_arrivee_1[1]
            else:
                if  pos_boucle==pos_boucle_1:
                    if  pos  in  pos_boucle_1:
                        pos_suivante=pos_boucle_1[(pos_boucle_1.index(pos)+1)%len(pos_boucle_1)]
                    else:
                        pos_suivante=pos_boucle_2[(pos_boucle_2.index(pos)+1)%len(pos_boucle_2)]

            nouveau_cycle_hami[pos[1],pos[0]]=_
            pos=pos_suivante[:]

        self.chemin=nouveau_cycle_hami[:]

        # print(self.chemin)

        self.affichage.liste_aretes_cycle=self.affichage.initialiser_liste_aretes_cycle()

        return  True


        



    def a_etoile_oriente(self,fin,liste_pos_a_eviter,prise_en_compte_deplacement):

        debut=self.jeu.serpent.pos
        # fin=self.jeu.pomme.pos
        dico_couts={(debut[0],debut[1]):0}
        a_traiter=collections.deque([debut])

        dico_parents={}

        vide=collections.deque([])

        while  a_traiter!=vide:
            pos=min(a_traiter,key=lambda  p:dico_couts[(p[0],p[1])])
            a_traiter.remove(pos)

            # print(pos)


            #  si  c'est  fini
            if  pos==fin:

                chemin=[[pos[0],pos[1]]]
                while  (chemin[-1][0],chemin[-1][1])  in  dico_parents:
                    chemin.append(dico_parents[(chemin[-1][0],chemin[-1][1])])
                chemin.reverse()
                self.plus_court_chemin[:]=chemin[:]

                #  print('CHEMIN',chemin)

                if  len(chemin)>=2:
                    self.jeu.serpent.direction=[chemin[1][0]-debut[0],chemin[1][1]-debut[1]]
                else:
                    self.jeu.serpent.direction=[fin[0]-debut[0],fin[1]-debut[1]]
                
                

                if  self.jeu.serpent.direction==[0,0]:
                    return  False

                #  print(self.jeu.serpent.direction)

                return  True


            liste_voisins=self.dico_adjacence_oriente[(pos[0],pos[1])]
            # liste_voisins=self.voisins(pos)
            # print(pos,liste_voisins)

            pos_queue=list(self.jeu.serpent.pos_queue)
            if prise_en_compte_deplacement:
                profondeur=0
                pos_=[pos[0],pos[1]]
                while  (pos_[0],pos_[1])  in  dico_parents:
                    profondeur+=1
                    pos_=dico_parents[(pos_[0],pos_[1])]


                

                # si on est sur la pomme
                if  self.jeu.pomme_atteinte:
                    if  profondeur==0:
                        pos_queue_predits=pos_queue
                    else:
                        pos_queue_predits=pos_queue[(profondeur):]

                # si on n'est pas sur la pomme
                else:
                    pos_queue_predits=pos_queue[(profondeur+1):]
            else:
                pos_queue_predits=pos_queue
            # print(profondeur)

            # print(pos_queue_predits)

            # pos_queue_predits=pos_queue



            for  voisin  in  liste_voisins:
                if  not  voisin  in  pos_queue_predits and not voisin in liste_pos_a_eviter:
                    cout_g=abs(voisin[0]-debut[0])+abs(voisin[1]-debut[1])
                    cout_h=abs(voisin[0]-fin[0])+abs(voisin[1]-fin[1])
                    cout_f=cout_g+cout_h



    #  if  not  (voisin[0],voisin[1])  in  dico_profondeurs  or  dico_profondeurs[(pos[0],pos[1])]+1>dico_profondeurs[(voisin[0],voisin[1])]:
    #      dico_profondeurs[(voisin[0],voisin[1])]=dico_profondeurs[(pos[0],pos[1])]+1


                    if  not  (voisin[0],voisin[1])  in  dico_couts  or  cout_f<dico_couts[(voisin[0],voisin[1])]:
                        a_traiter.append(voisin)
                        dico_parents[(voisin[0],voisin[1])]=pos[:]
                        dico_couts[(voisin[0],voisin[1])]=cout_f

                        #  print(dico_parents)


        return  False


    def longueur_plus_court_chemin(self,debut,fin):     # inutile
        k=1



        indice_debut=self.numero_depuis_pos_matrice(debut)
        indice_fin=self.numero_depuis_pos_matrice(fin)

        # print(indice_debut,indice_fin)

        matrice_adjacence_=np.copy(self.matrice_adjacence)
        matrice_adjacence=np.copy(self.matrice_adjacence)
        while matrice_adjacence[indice_debut,indice_fin]==0.:
            matrice_adjacence=np.matmul(matrice_adjacence_,matrice_adjacence)
            k+=1
        return k


    def numero_depuis_pos_matrice(self,pos):
        for numero in self.dico_indices:
            if self.dico_indices[numero]==pos:
                return numero

        print("pas de numero depuis pos matrice trouvé")

    def  reindicage_chemin(self,debut_fin,entree_sortie,numero_actuel,numero_desire):
        liste_pos_boucle=None
        pos=self.pos_depuis_numero(0)

        for  compteur  in  range(self.affichage.nb_cases**2):
            numero_pos=self.numero_depuis_pos(pos)
            liste_voisins_pos=self.voisins(pos)



            #  etablissement  de  la  position  suivante
            pos_suivante=None


            #  cas  ou  numero_pos  est  la  numero_actuel:  il  faut  aller  au  numero  desire
            if  numero_pos==numero_actuel:
                #  print('1')
                for  voisin  in  liste_voisins_pos:
                    if  self.numero_depuis_pos(voisin)==numero_desire:
                        pos_suivante=voisin
                        break

            #  cas  ou  on  est  sur  debut_fin[0]  apres  la  reparation  du  cycle,  on  va  au  voisin  suivant  dans  la  boucle
            elif  pos==debut_fin[0]:
                #  print('2')
                for  voisin  in  liste_voisins_pos:
                    if  self.numero_depuis_pos(voisin)==entree_sortie[1]:
                        pos_suivante.append(voisin)
                        break

            #  cas  ou  on  est  a  entree_sortie[0]:  go  a  debut_fin[1]
            elif  numero_pos==entree_sortie[0]:
                #  print('3')
                for  voisin  in  liste_voisins_pos:
                    if  voisin==debut_fin[1]:
                        pos_suivante=voisin
                        break

            #  cas  ou  on  doit  avancer  de  un  (rien  de  particulier)
            else:
                #  print('4')
                for  voisin  in  liste_voisins_pos:
                    if  self.numero_depuis_pos(voisin)==numero_pos+1:
                        pos_suivante=voisin
                        break


            #  cas  ou  pas  de  voisin+1
            if  pos_suivante is None:
                #  print('5')
                pos_suivantes_possibles=[]
                for  voisin  in  liste_voisins_pos:
                    if  voisin  in  liste_pos_boucle  and  self.numero_depuis_pos(voisin)>numero_actuel:
                        pos_suivantes_possibles.append(voisin)
                pos_suivante=min(pos_suivantes_possibles,key=self.numero_depuis_pos)[:]

            self.nouveau_chemin[pos[1]][pos[0]]=compteur

    def mettre_a_jour_plus_court_chemin(self,plus_court_chemin):
        plus_court_chemin.remove(self.jeu.serpent.pos)



    def  a_etoile(self,fin,liste_pos_murs,prise_en_compte_deplacement):
        debut=self.jeu.serpent.pos
        dico_couts={(debut[0],debut[1]):0}
        a_traiter=collections.deque([debut])

        dico_parents={}
        dico_profondeurs={(debut[0],debut[1]):0}

        vide=collections.deque([])

        while  a_traiter!=vide:
            pos=min(a_traiter,key=lambda  p:dico_couts[(p[0],p[1])])
            a_traiter.remove(pos)

            #  si  c'est  fini
            if  pos==fin:
                chemin=[[pos[0],pos[1]]]
                while  (chemin[-1][0],chemin[-1][1])  in  dico_parents:
                    chemin.append(dico_parents[(chemin[-1][0],chemin[-1][1])])
                chemin.reverse()
                self.plus_court_chemin[:]=chemin[:]

                #  print('CHEMIN',chemin)

                if  len(chemin)>=2:
                    self.jeu.serpent.direction=[chemin[1][0]-debut[0],chemin[1][1]-debut[1]]
                else:
                    self.jeu.serpent.direction=[fin[0]-debut[0],fin[1]-debut[1]]

                if  self.jeu.serpent.direction==[0,0]:
                    return  False

                #  print(self.jeu.serpent.direction)

                return  True


            liste_voisins=self.voisins(pos)


            profondeur=0
            pos_=[pos[0],pos[1]]
            while  (pos_[0],pos_[1])  in  dico_parents:
                profondeur+=1
                pos_=dico_parents[(pos_[0],pos_[1])]


            pos_queue=list(self.jeu.serpent.pos_queue)

            if prise_en_compte_deplacement:
                # si on est sur la pomme
                if  self.jeu.pomme_atteinte:
                    if  profondeur==0:
                        pos_queue_predits=pos_queue
                    else:
                        pos_queue_predits=pos_queue[(profondeur):]

                # si on n'est pas sur la pomme
                else:
                    pos_queue_predits=pos_queue[(profondeur+1):]

                # print(pos_queue_predits)
            else:
                pos_queue_predits=pos_queue





            for  voisin  in  liste_voisins:
                if  not  voisin  in  pos_queue_predits  and  not  voisin  in  liste_pos_murs:
                    cout_g=abs(voisin[0]-debut[0])+abs(voisin[1]-debut[1])
                    cout_h=abs(voisin[0]-fin[0])+abs(voisin[1]-fin[1])
                    cout_f=cout_g+cout_h

                    # if voisin in self.chemin:
                    #     cout_f-=10
                    # else:
                    #     cout_f+=10



    #  if  not  (voisin[0],voisin[1])  in  dico_profondeurs  or  dico_profondeurs[(pos[0],pos[1])]+1>dico_profondeurs[(voisin[0],voisin[1])]:
    #      dico_profondeurs[(voisin[0],voisin[1])]=dico_profondeurs[(pos[0],pos[1])]+1


                    if  not  (voisin[0],voisin[1])  in  dico_couts  or  cout_f<dico_couts[(voisin[0],voisin[1])]:
                        a_traiter.append(voisin)
                        dico_parents[(voisin[0],voisin[1])]=pos[:]
                        dico_couts[(voisin[0],voisin[1])]=cout_f

                        #  print(dico_parents)


        return  False

    def calculer_taux_raccourcis(self):
        pos=[0,0]
        liste_taux_raccourcis=[]
        for _ in range(self.affichage.nb_cases**2):
            direction=self.direction_suivante(pos[:])
            pos_suivante=[pos[0]+direction[0],pos[1]+direction[1]]

            a_ajouter=0
            numero_pos=self.numero_depuis_pos(pos)
            self.soustraire(numero_pos)
            for voisin in self.voisins(pos):
                if self.affichage.nb_cases**2-1>self.numero_depuis_pos(voisin)>1:
                    a_ajouter+=self.numero_depuis_pos(voisin)
                
                # print(pos,voisin,a_ajouter)
            
            liste_taux_raccourcis.append(a_ajouter)

            pos=pos_suivante[:]
        
        # print(liste_taux_raccourcis)
        
        # self.soustraire(numero_pos)
        
        # print(sum(liste_taux_raccourcis),liste_taux_raccourcis)
        # plt.plot(list(range(self.affichage.nb_cases**2)),liste_taux_raccourcis)
        # plt.show()
        # print(liste_taux_raccourcis)
        
        return sum(liste_taux_raccourcis)


    def  a_etoile_neutre(self,debut,fin,liste_pos_eviter,prise_en_compte_deplacement):

        dico_couts={(debut[0],debut[1]):0}
        a_traiter=collections.deque([debut])

        dico_parents={}

        vide=collections.deque([])



        while  a_traiter!=vide:
            pos=min(a_traiter,key=lambda  p:dico_couts[(p[0],p[1])])
            a_traiter.remove(pos)



            #  si  c'est  fini
            if  pos==fin:
                chemin=[[pos[0],pos[1]]]
                while  (chemin[-1][0],chemin[-1][1])  in  dico_parents:
                    chemin.append(dico_parents[(chemin[-1][0],chemin[-1][1])])  #  inutile  d'append

                chemin.reverse()
                self.plus_court_chemin_[:]=chemin[:]

                # print('CHEMIN  neutre',chemin)

                if  len(chemin)>=2:
                    direction=[chemin[1][0]-debut[0],chemin[1][1]-debut[1]]
                else:
                    direction=[fin[0]-debut[0],fin[1]-debut[1]]

                if  direction==[0,0]:
                    return  False

                return  True


            liste_voisins=self.voisins(pos)



            if prise_en_compte_deplacement:

                profondeur=0
                pos_=[pos[0],pos[1]]
                while  (pos_[0],pos_[1])  in  dico_parents:
                    profondeur+=1
                    pos_=dico_parents[(pos_[0],pos_[1])]

                # si on est sur la pomme
                if  debut==self.jeu.pomme.pos:
                    if  profondeur==0:
                        liste_pos_eviter_predits=liste_pos_eviter
                    else:
                        liste_pos_eviter_predits=liste_pos_eviter[(profondeur):]

                # si on n'est pas sur la pomme
                else:
                    liste_pos_eviter_predits=liste_pos_eviter[(profondeur+1):]

            else:
                # print('eviter',liste_pos_eviter)
                liste_pos_eviter_predits=liste_pos_eviter[:]





            for  voisin  in  liste_voisins:
                if  not  voisin  in  liste_pos_eviter_predits:
                    cout_g=abs(voisin[0]-debut[0])+abs(voisin[1]-debut[1])
                    cout_h=abs(voisin[0]-fin[0])+abs(voisin[1]-fin[1])
                    cout_f=cout_g+cout_h


                    if  not  (voisin[0],voisin[1])  in  dico_couts  or  cout_f<dico_couts[(voisin[0],voisin[1])]:
                        a_traiter.append(voisin)
                        dico_parents[(voisin[0],voisin[1])]=pos[:]
                        dico_couts[(voisin[0],voisin[1])]=cout_f

        # print("A* pas de chemin")
        return  False



    


    def  liste_pos_apres_deplacement_chemin(self,liste_pos,chemin):
        taille_chemin=len(chemin)
        taille_liste_pos=len(liste_pos)
        #  print('LEN  POS',len(liste_pos))

        if self.jeu.pomme_atteinte:

            if  taille_liste_pos<taille_chemin:
                liste_pos_post=chemin[(taille_chemin-taille_liste_pos-1):]
            elif  taille_liste_pos>=taille_chemin:
                # print('b')
                #  print('true',liste_pos,chemin)
                difference_taille=taille_liste_pos-taille_chemin
                liste_pos_post=[liste_pos[0]]
                liste_pos_post+=liste_pos
                liste_pos_post+=chemin[1:]
                liste_pos_post=liste_pos_post[(taille_chemin-1):]

                # print("list",liste_pos_post)

        else:

            if  taille_liste_pos<=taille_chemin:
                liste_pos_post=chemin[(taille_chemin-taille_liste_pos):]
            elif  taille_liste_pos>taille_chemin:
                #  print('b')
                #  print('true',liste_pos,chemin)
                difference_taille=taille_liste_pos-taille_chemin
                liste_pos_post=liste_pos+chemin[1:]
                liste_pos_post=liste_pos_post[(taille_chemin-1):]

            #  print('LEN  POS  APRES',len(liste_pos_post))
        # print(liste_pos_post)
        return  liste_pos_post

    def suivre_chemin_particulier(self,chemin):
        for i in range(len(chemin)-1):
            if self.jeu.serpent.pos==chemin[i]:
                self.jeu.serpent.direction=[chemin[i+1][0]-self.jeu.serpent.pos[0],chemin[i+1][1]-self.jeu.serpent.pos[1]]
                return

        # print("fonction suivre_chemin_particulier, pas de direction trouvée")










    def  pos_depuis_numero(self,numero):
        for  i  in  range(self.affichage.nb_cases):
            for  j  in  range(self.affichage.nb_cases):
                if  self.chemin[i][j]==numero:
                    return([j,i])
                        #  print('pos_depuis_numero(),numero  pas  sur  la  grille')




#  [[0,  229,  228,  227,  226,  225,  224,  223,  222,  221,  220,  219,  218,  217,  216,  215],
#  [1,  4,  5,  34,  35,  64,  65,  94,  95,  124,  125,  154,  155,  184,  185,  214],
#  [2,  3,  6,33,  36,  63,  66,  93,  96,  123,  126,  153,  156,  183,  186,  213],
#  [3,  28,  7,  32,  37,  62,  67,  92,  97,  122,  127,  152,  157,  182,  187,  212],
#  [4,  27,  8,  31,  38,  61,  68,  91,  98,  121,  128,  151,  158,  181,  188,  211],
#  [5,  26,  9,  30,  39,  60,  69,  90,  99,  120,  129,  150,  159,  180,  189,  210],
#  [6,  25,  10,  29,  40,  59,  70,  89,  100,  119,  130,149,  160,  179,  190,  209],
#  [7,  24,  11,  28,  41,  58,  71,  88,  101,  118,  131,  148,  161,  178,  191,  208],
#  [8,  23,  12,  27,  42,  57,  72,  87,  102,  117,  132,  147,  162,  177,  192,  207],
#  [9,  22,  13,  26,  43,  56,  73,  86,  103,  116,  133,  146,  163,  176,  193,  206],
#  [10,  21,  14,  25,  44,  55,  74,  85,  104,  115,  134,  145,  164,  175,  194,  205],
#  [11,  20,  15,  24,  45,  54,  75,  84,  105,  114,  135,  144,  165,  174,  195,  204],
#  [12,  19,  16,  23,  46,  53,  76,  83,  106,  113,  136,  143,  166,  173,  196,  203],
#  [13,  18,  17,22,  47,  52,  77,  82,  107,  112,  137,  142,  167,  172,  197,  202],
#  [14,  17,  18,  21,  48,  51,  78,  81,  108,  111,  138,  141,  168,  171,  198,  201],
#  [15,  16,  19,  20,  49,  50,79,  80,  109,  110,  139,  140,  169,  170,  199,  200]]







    def  direction_suivante(self,pos):      #  pos  selon  coordonnees  du  serpent
        numero_suivant=self.numero_depuis_pos(pos)+1
        
        #  dir_0=[0,0]
        if  numero_suivant==self.affichage.nb_cases**2:
            numero_suivant=0
        
        for  j  in  range(-1,2):
            for  i  in  range(-1,2):
                if  i*j==0  and  pos[0]+j>=0  and  pos[0]+j<=self.affichage.nb_cases-1  and  pos[1]+i>=0  and  pos[1]+i<=self.affichage.nb_cases-1:
                    if  self.numero_depuis_pos((pos[0]+j,pos[1]+i))==numero_suivant:
                        return  [j,i]
                    #  if  self.chemin[pos[1]+i][pos[0]+j]==0:
                    #      dir_0=[j,i]
                        #  return(dir_0)
        print("pas  de  direction  suivante  trouvee")
        print(self.chemin)
        print(self.liste_murs)
    
    def  numero_depuis_pos(self,pos):
        #  print(self.chemin[pos[1]][pos[0]])
        return  int(self.chemin[pos[1],pos[0]])


    def  suivre_chemin(self):
        # print(self.pos_suivante_selon_cycle_hami(self.jeu.serpent.pos,self.chemin))
        self.jeu.serpent.direction=self.direction_suivante([self.jeu.serpent.pos[0],self.jeu.serpent.pos[1]])