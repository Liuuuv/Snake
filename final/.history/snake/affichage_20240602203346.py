import pygame as py
import collections
import random as rd
import numpy as np
import matplotlib.pyplot as plt
import time

from pomme import Pomme
from algorithme import Algorithme
from couleurs import*

inf=float('inf')

class  Affichage:
    def  __init__(self,facteur,jeu,nb_cases):
        self.facteur=facteur
        self.dimensions=(int(facteur*1920),int(facteur*1080))
        self.jeu=jeu
        self.police=py.font.Font(None,40)
        self.police_petite=py.font.Font(None,20)
        self.fenetre=py.display.set_mode((self.dimensions[0],self.dimensions[1]))

        self.jeu_actif=True
        # if  not  self.jeu_actif:
        #     self.jeu.serpent.pos=[-1,-1]

        self.clique_gauche_souris_en_cours=False
        self.clique_droit_souris_en_cours=False

        self.liste_cases_marquees=[]

        self.liste_pos_aretes_squelette=collections.deque([])


        self.numero_essai=0

        self.nom_methode=None

        # pour raccourcis_croissants_v2, represente le manque de marge permis (en cases)
        self.taux_risque=0


        self.mode_manuel=False

        self.liste_aretes_cycle=[]


        self.marge_cases=0
        self.nb_cases=nb_cases
        self.taille_case=(self.dimensions[1]-(self.nb_cases+1)*self.marge_cases)//self.nb_cases
        self.liste_emplacements_cases=self.initialiser_emplacements_cases()

        self.taille_plateau=self.taille_case*self.nb_cases

        self.algorithme=Algorithme(self,self.jeu)

        pos=[rd.randint(0,self.nb_cases-1),rd.randint(0,self.nb_cases-1)]
        if pos==[0,0]:
            pos=rd.choice([[0,1],[1,0]])
        #  pos=[1,4]
        self.jeu.pomme=Pomme(pos)

        self.initialiser_pomme()

        self.liste_aretes_cycle=self.initialiser_liste_aretes_cycle()

        self.dico_pos_ecran_aretes=self.initialiser_dico_aretes()



        self.jeu.max_score=self.nb_cases**2


    # pour avoir acces a tous les [UL,UR,DR,DL] des pixels
    def  initialiser_emplacements_cases(self):
        liste_emplacements_cases=[]
        for  i  in  range(self.nb_cases):
            for  j  in  range(self.nb_cases):
                UL=(j*self.taille_case,i*self.taille_case)
                DL=(j*self.taille_case,(i+1)*(self.taille_case))
                UR=((j+1)*self.taille_case,i*self.taille_case)
                DR=((j+1)*self.taille_case,(i+1)*(self.taille_case))
                liste_emplacements_cases.append([UL,UR,DR,DL])
        return(liste_emplacements_cases)

    # pour dessiner les cases
    def  dessiner_cases(self):
        n=len(self.liste_emplacements_cases)
        alt=0
        for  i  in  range(0,n,2):
            if  i%self.nb_cases==0:
                alt+=1
            if  alt%2==0:
                py.draw.polygon(self.fenetre,vert_clair,self.liste_emplacements_cases[i])
                py.draw.polygon(self.fenetre,vert_fonce,self.liste_emplacements_cases[i+1])
            else:
                py.draw.polygon(self.fenetre,vert_clair,self.liste_emplacements_cases[i+1])
                py.draw.polygon(self.fenetre,vert_fonce,self.liste_emplacements_cases[i])

        """methode pour dessiner avec la meme couleur"""
        #  for  quadruplet  in  self.liste_emplacements_cases:
        #      py.draw.polygon(self.fenetre,vert_clair,quadruplet)

    # s'il y a des cases a mettre d'une autre couleur
    def  dessiner_cases_marquees(self):
        for  pos  in  self.liste_cases_marquees:
            py.draw.polygon(self.fenetre,bleu,self.liste_emplacements_cases[pos[0]+pos[1]*self.nb_cases])

    # pour dessiner differemment les cases selon les deux boucles
    def  dessiner_cases_boucles(self):
        for  pos  in  self.algorithme.pos_boucle_1:
            py.draw.polygon(self.fenetre,(150,0,0),self.liste_emplacements_cases[pos[0]+pos[1]*self.nb_cases])
        for  pos  in  self.algorithme.pos_boucle_2:
            py.draw.polygon(self.fenetre,(100,0,0),self.liste_emplacements_cases[pos[0]+pos[1]*self.nb_cases])

    # pour savoir ou est la queue du serpent
    def  dessiner_squelette_serpent(self):
        self.dessiner_liste_aretes(self.liste_pos_aretes_squelette,blanc)

    # pour dessiner des aretes
    def  dessiner_liste_aretes(self,liste_couple_pos,couleur):
        for  couple  in  liste_couple_pos:
            couple_ecran=self.dico_pos_ecran_aretes[((couple[0][0],couple[0][1]),(couple[1][0],couple[1][1]))]
            #  print(couple_ecran[0],couple_ecran[1])
            py.draw.line(self.fenetre,(200,200,200),couple_ecran[0],couple_ecran[1])

    # mise a jour du serpent a chaque iteration
    def  mettre_a_jour_serpent(self):
        """on ne grandit pas au meme moment qu'on mange"""
        # si on n'a pas de queue
        if  self.jeu.serpent.taille_queue!=0:

            if  self.jeu.serpent.en_attente==None:
                self.jeu.serpent.pos_queue.popleft()
                self.liste_pos_aretes_squelette.popleft()
            else:
                self.jeu.serpent.en_attente=None

            self.jeu.serpent.pos_queue.append(self.jeu.serpent.pos[:])
            self.liste_pos_aretes_squelette.append([self.jeu.serpent.pos,[self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]]])

        # si on a une queue
        else:
            if  self.jeu.serpent.en_attente!=None:

                self.jeu.serpent.pos_queue.append(self.jeu.serpent.pos[:])
                self.liste_pos_aretes_squelette.append([self.jeu.serpent.pos,[self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]]])

                self.jeu.serpent.en_attente=None


        """on grandit au meme moment qu'on mange"""
        # if  self.jeu.serpent.taille_queue==0:
        #     if [self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]]==self.jeu.pomme.pos:
        #         self.jeu.serpent.pos_queue.append(self.jeu.serpent.pos[:])
        #         self.liste_pos_aretes_squelette.append([self.jeu.serpent.pos,[self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]]])
        #
        # else:
        #     if [self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]]!=self.jeu.pomme.pos:
        #         self.jeu.serpent.pos_queue.popleft()
        #         self.liste_pos_aretes_squelette.popleft()
        #
        #     self.jeu.serpent.pos_queue.append(self.jeu.serpent.pos[:])
        #     self.liste_pos_aretes_squelette.append([self.jeu.serpent.pos,[self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]]])



        self.jeu.serpent.taille_queue=len(self.jeu.serpent.pos_queue)

        # deplacement
        self.jeu.serpent.pos=[
        self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],
        self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]
        ]



    def  verifier_fin_jeu(self):
        pos=self.jeu.serpent.pos
        if  pos[0]<=-1  or  pos[1]<=-1  or  pos[0]>=self.nb_cases  or  pos[1]>=self.nb_cases  or  pos  in  self.jeu.serpent.pos_queue:
            self.jeu.fin_jeu=True
            self.jeu.etat_partie=-1
            # self.mode_manuel=True
            print("Perdu")
            print("Numéro essai:",self.numero_essai)
        elif  self.jeu.score==self.jeu.max_score:
            self.jeu.fin_jeu=True
            self.jeu.etat_partie=1
            print("Partie  gagnée")
            print("Numéro essai:",self.numero_essai)
        

    # mise a jour de pomme
    def  mettre_a_jour_pomme(self):

        # si le serpent mange la pomme
        if  self.jeu.serpent.pos==self.jeu.pomme.pos:
            self.jeu.pomme_atteinte=True
            self.algorithme.plus_court_chemin=[]

            self.algorithme.mettre_a_jour_listes()

            self.jeu.score+=1


            liste_pos_pomme_potentielles=[]
            for i in range(self.nb_cases):
                for j in range(self.nb_cases):
                    if not [i,j] in list(self.jeu.serpent.pos_queue)+[self.jeu.serpent.pos]:
                        liste_pos_pomme_potentielles.append([i,j])

            if liste_pos_pomme_potentielles==[]:
                pos=[-1,-1]
            else:
                pos=rd.choice(liste_pos_pomme_potentielles)

            # pos=[rd.randint(0,self.nb_cases-1),rd.randint(0,self.nb_cases-1)]
            # #  pos=[3,5]
            # while  pos==self.jeu.serpent.pos  or  pos  in  self.jeu.serpent.pos_queue:
            #     pos=[rd.randint(0,self.nb_cases-1),rd.randint(0,self.nb_cases-1)]



            self.jeu.pomme.pos=pos
            self.initialiser_pomme()
            self.jeu.serpent.en_attente=self.jeu.serpent.pos[:]

        else:
            self.jeu.pomme_atteinte=False

    def  actualiser_pomme(self):
        self.jeu.pomme.numero=self.algorithme.numero_depuis_pos(self.jeu.pomme.pos)

    def  initialiser_pomme(self):
        pos=self.jeu.pomme.pos
        # self.jeu.pomme.UL=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases,pos[1]*(self.taille_case+self.marge_cases)+self.marge_cases)
        # self.jeu.pomme.DL=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases,(pos[1]+1)*(self.taille_case+self.marge_cases))
        # self.jeu.pomme.UR=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,pos[1]*(self.taille_case+self.marge_cases)+self.marge_cases)
        # self.jeu.pomme.DR=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,(pos[1]+1)*(self.taille_case+self.marge_cases))
        self.jeu.pomme.numero=self.algorithme.chemin[pos[1]][pos[0]]

    def  mettre_a_jour_direction(self):
        keys  =  py.key.get_pressed()
        if  keys[py.K_LEFT]:
            self.jeu.serpent.direction=[-1,0]
        if  keys[py.K_RIGHT]:
            self.jeu.serpent.direction=[1,0]
        if  keys[py.K_UP]:
            self.jeu.serpent.direction=[0,-1]
        if  keys[py.K_DOWN]:
            self.jeu.serpent.direction=[0,1]


    def  dessiner_pomme(self):
        # py.draw.polygon(self.fenetre,rouge,[self.jeu.pomme.UL,self.jeu.pomme.UR,self.jeu.pomme.DR,self.jeu.pomme.DL])
        py.draw.polygon(self.fenetre,rouge,self.liste_emplacements_cases[self.jeu.pomme.pos[0]+self.jeu.pomme.pos[1]*self.nb_cases])



    def  dessiner_serpent(self):
        self.dessiner_tete_serpent()
        self.dessiner_queue_serpent()

    def  dessiner_tete_serpent(self):    #  a  opti  avec  dico
        pos=self.jeu.serpent.pos
        # UL=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases,pos[1]*(self.taille_case+self.marge_cases)+self.marge_cases)
        # DL=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases,(pos[1]+1)*(self.taille_case+self.marge_cases))
        # UR=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,pos[1]*(self.taille_case+self.marge_cases)+self.marge_cases)
        # DR=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,(pos[1]+1)*(self.taille_case+self.marge_cases))
        try:
            py.draw.polygon(self.fenetre,bleu_clair,self.liste_emplacements_cases[pos[0]+pos[1]*self.nb_cases])
        except IndexError:
            print('erreur dessiner tete serpent,',pos)

    def  dessiner_queue_serpent(self):      #  a  opti  avec  dico
        for  pos  in  self.jeu.serpent.pos_queue:
            # UL=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases,pos[1]*(self.taille_case+self.marge_cases)+self.marge_cases)
            # DL=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases,(pos[1]+1)*(self.taille_case+self.marge_cases))
            # UR=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,pos[1]*(self.taille_case+self.marge_cases)+self.marge_cases)
            # DR=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,(pos[1]+1)*(self.taille_case+self.marge_cases))
            py.draw.polygon(self.fenetre,bleu,self.liste_emplacements_cases[pos[0]+pos[1]*self.nb_cases])

    def initialiser_liste_aretes_cycle(self):
        #  print('init')
        liste_aretes_cycle=[]
        origine=[0,0]
        pos_avant=origine[:]
        pos=origine

        liste_aretes_cycle.append(([(pos_avant[0]+0.5)*self.taille_case,(pos_avant[1]+0.5)*self.taille_case],[(pos[0]+0.5)*self.taille_case,(pos[1]+0.5)*self.taille_case]))


        for  _  in  range(self.nb_cases**2):
            direction=self.algorithme.direction_suivante(pos)

            pos_avant[:]=pos[:]


            pos=[pos[0]+direction[0],pos[1]+direction[1]]
            liste_aretes_cycle.append(([(pos_avant[0]+0.5)*self.taille_case,(pos_avant[1]+0.5)*self.taille_case],[(pos[0]+0.5)*self.taille_case,(pos[1]+0.5)*self.taille_case]))

        return  liste_aretes_cycle


    def  initialiser_dico_aretes(self):    #  il  y  a  des  aretes  en  trop  sur  les  bords
        dico_aretes={}
        for  i  in  range(self.nb_cases):
            for  j  in  range(self.nb_cases):
                for  i_  in  range(-1,2):
                    for  j_  in  range(-1,2):
                        dico_aretes[((i,j),(i+i_,j+j_))]=[self.pos_ecran_depuis_pos((i,j)),self.pos_ecran_depuis_pos((i+i_,j+j_))]

        return  dico_aretes

    def  pos_ecran_depuis_pos(self,pos):
        return  [int((pos[0]+0.5)*self.taille_case),int((pos[1]+0.5)*self.taille_case)]


    def  dessiner_cycle(self,liste_aretes=None):
        if liste_aretes is None:
            liste_aretes=self.liste_aretes_cycle

        epaisseur=3

        for  couple  in  liste_aretes:
            py.draw.line(self.fenetre,noir,*couple,epaisseur)




    def  dessiner_chiffres_chemin(self):      #  a  ameliorer
        liste_surfaces_texte=[]
        for  j  in  range(self.nb_cases):
            for  i  in  range(self.nb_cases):
                texte_surface=self.police_petite.render(str(self.algorithme.numero_depuis_pos([j,i])),True,noir)
                self.fenetre.blit(texte_surface,[(j+0.55)*self.taille_case,(i+0.55)*self.taille_case])
    
    def dessiner_pos_chemin(self):
        for  j  in  range(self.nb_cases):
            for  i  in  range(self.nb_cases):
                texte_surface=self.police_petite.render(str((j,i)).replace(' ',''),True,noir)
                self.fenetre.blit(texte_surface,[(j+0.55)*self.taille_case,(i+0.3)*self.taille_case])

    def  dessiner_plus_court_chemin(self):      #  a  ameliorer
        for  i  in  range(len(self.algorithme.plus_court_chemin)-1):
            py.draw.line(self.fenetre,rouge_fonce,
            [(self.algorithme.plus_court_chemin[i][0]+0.5)*self.taille_case,(self.algorithme.plus_court_chemin[i][1]+0.5)*self.taille_case],
            [(self.algorithme.plus_court_chemin[i+1][0]+0.5)*self.taille_case,(self.algorithme.plus_court_chemin[i+1][1]+0.5)*self.taille_case],
            5)

    def  dessiner_chemin(self,liste_pos,couleur,tronquer_chemin):    #  a  ameliorer
        # print(liste_pos)
        if tronquer_chemin:
            if liste_pos!=[]:
                i_min=liste_pos.index(self.jeu.serpent.pos)
            for  i  in  range(len(liste_pos)-1):
                if i<i_min:
                    continue
                py.draw.line(self.fenetre,couleur,
                [(liste_pos[i][0]+0.5)*self.taille_case,(liste_pos[i][1]+0.5)*self.taille_case],
                [(liste_pos[i+1][0]+0.5)*self.taille_case,(liste_pos[i+1][1]+0.5)*self.taille_case],
                5)
        else:
            for  i  in  range(len(liste_pos)-1):
                py.draw.line(self.fenetre,couleur,
                [(liste_pos[i][0]+0.5)*self.taille_case,(liste_pos[i][1]+0.5)*self.taille_case],
                [(liste_pos[i+1][0]+0.5)*self.taille_case,(liste_pos[i+1][1]+0.5)*self.taille_case],
                5)
    def  clique_gauche_souris(self):


        if  py.mouse.get_pressed()[0]:
            if  not  self.clique_gauche_souris_en_cours:
                self.clique_gauche_souris_en_cours=True
                return  True
        else:
            self.clique_gauche_souris_en_cours=False
            return  False

    def  clique_droit_souris(self):

        # print(py.mouse.get_pressed())

        if  py.mouse.get_pressed()[2]:
            if  not  self.clique_droit_souris_en_cours:
                self.clique_droit_souris_en_cours=True
                return  True
        else:
            self.clique_droit_souris_en_cours=False
            return  False


    def  marquer_case_souris(self):
        if  self.clique_gauche_souris():
            souris_x,souris_y=py.mouse.get_pos()
            if  souris_y<=self.taille_plateau  and  souris_x<=self.taille_plateau:
                i=souris_y//self.taille_case
                j=souris_x//self.taille_case

                #  print((j,i))
                self.liste_cases_marquees.append([j,i])
        elif self.clique_droit_souris():
            souris_x,souris_y=py.mouse.get_pos()
            if  souris_y<=self.taille_plateau  and  souris_x<=self.taille_plateau:
                i=souris_y//self.taille_case
                j=souris_x//self.taille_case

                if (j,i) in self.liste_cases_marquees:
                    self.liste_cases_marquees.remove([j,i])





    def  simuler_modif_cycle(self):
        if  len(self.liste_cases_marquees)==3:

            corps=self.liste_cases_marquees[0]
            debut=self.liste_cases_marquees[1]
            fin=self.liste_cases_marquees[2]

            self.liste_cases_marquees=[]

            self.jeu.serpent.pos=debut
            self.jeu.serpent.direction=[fin[0]-debut[0],fin[1]-debut[1]]
            self.jeu.serpent.pos_queue.append(corps)


            liste_boucles=self.algorithme.recuperer_deux_boucles()
            if  liste_boucles is not False:
                if self.algorithme.modifier_cycle(listes_boucles=liste_boucles):
                    print('OUI')
                else:
                    print('NON')
            else:
                print('NON')
                # print(self.algorithme.chemin)
            print()
            



    def  loop(self):
        horloge=py.time.Clock()

        blit=self.fenetre.blit

        instant_suivant=True

        taux_raccourci=self.algorithme.calculer_taux_raccourcis()

        # car on commence par mettre a jour le serpent
        self.algorithme.mettre_a_jour_direction(self.nom_methode)
        self.mettre_a_jour_direction()


        #  boucle  de  jeu
        continuer=True
        while  continuer:
            

            for  event  in  py.event.get():
                if  event.type==py.QUIT:
                    continuer=False
                if  event.type==py.KEYDOWN:
                    if  event.key==py.K_ESCAPE:
                        self.jeu.fin_jeu=True
                    if  event.key==py.K_a:
                        self.afficher=not self.afficher
                    if  event.key==py.K_m:
                        self.mode_manuel=not self.mode_manuel


                    instant_suivant=False
                    if  self.mode_manuel:
                        if  event.key==py.K_SPACE:
                            instant_suivant=True

            

            if  not  self.mode_manuel:
                instant_suivant=True



            horloge.tick(self.fps)
            

            



            if  instant_suivant:
                instant_suivant=False


                if  self.jeu.fin_jeu:
                    continuer=False
                    print(str("Jeu  terminé"))
                    print(str("score:")+str(self.jeu.score))
                    print(str("longueur  parcourue:")+str(self.jeu.distance_parcourue))
                    break

                # heure_depart=time.time()

                # on met a jour tout
                self.fenetre.fill(blanc)
                if  self.jeu_actif:

                    # print(self.algorithme.lock)

                    self.mettre_a_jour_serpent()
                    

                    #  pour  algorithme  pomme-queue, a modif si possible......
                    if  self.jeu.serpent.pos==self.jeu.pomme.pos:
                        self.algorithme.lock=False
                    
                    self.mettre_a_jour_pomme()

                    

                    
                    self.verifier_fin_jeu()
                    

                    if not self.jeu.fin_jeu:
                        self.algorithme.mettre_a_jour_direction(self.nom_methode)
                        self.mettre_a_jour_direction()

                    
                    


                    self.jeu.distance_parcourue+=1

                if  self.afficher:
                    

                    if  self.jeu_actif:


                        self.dessiner_cases()
                        self.dessiner_pomme()
                        self.dessiner_serpent()
                        
                        self.dessiner_squelette_serpent()
                        # self.dessiner_plus_court_chemin()

                        self.dessiner_chemin(self.algorithme.plus_court_chemin_hor,(100,0,0),True)
                        self.dessiner_chemin(self.algorithme.plus_court_chemin_ver,(180,0,0),True)
                        self.dessiner_chemin(self.algorithme.plus_court_chemin,(150,0,0),False)
                        self.dessiner_chemin(self.algorithme.chemin_optimal,(150,0,0),False)

                        # print(self.algorithme.plus_court_chemin_,)
                        # self.dessiner_chemin(self.algorithme.plus_court_chemin_,(10,200,100),False)

                        
                        self.dessiner_chiffres_chemin()
                        self.dessiner_cycle()

                        self.dessiner_pos_chemin()

                        # self.algorithme.tracer_murs(self.algorithme.liste_murs)

                        # self.dessiner_cycle(self.algorithme.liste_aretes_deux_facteur)

                        

                        


                        # heure_fin=time.time()
                        # print('temps execution',(heure_fin-heure_depart)*1000)
                        
                    #  si  jeu  inactif
                    else:
                    

                        self.dessiner_cases()


                        self.marquer_case_souris()
                        self.simuler_modif_cycle()
                        
                        self.dessiner_cases_boucles()
                        self.dessiner_cases_marquees()
                        self.dessiner_pos_chemin()


                        self.dessiner_cycle()
                        self.dessiner_chiffres_chemin()
                        
                        # self.algorithme.tracer_murs(self.algorithme.liste_murs)    #  labyrinthe

                        # self.dessiner_cycle(self.algorithme.liste_aretes_deux_facteur)

                        


                        # self.algorithme.arbre_possibilites()  # inutile



                



                keys  =  py.key.get_pressed()
                if  keys[py.K_s]:
                    self.fps-=5
                elif  keys[py.K_z]:
                    self.fps+=5
                self.fps=np.clip(self.fps,0.5,inf)



                marge_texte=20


                texte_surface1=self.police.render("fps:"+str(round(horloge.get_fps(),1)),True,noir)
                texte_surface2=self.police.render("score:"+str(self.jeu.score),True,noir)
                texte_surface3=self.police.render("distance  parcourue:"+str(self.jeu.distance_parcourue),True,noir)
                texte_surface4=self.police.render("numero de l'essai:"+str(self.numero_essai),True,noir)
                texte_surface5=self.police.render("taux de raccourci:"+str(taux_raccourci),True,noir)
                blit(texte_surface1,(self.taille_plateau+marge_texte,0))
                blit(texte_surface2,(self.taille_plateau+marge_texte,30))
                blit(texte_surface3,(self.taille_plateau+marge_texte,60))
                blit(texte_surface4,(self.taille_plateau+marge_texte,90))
                blit(texte_surface5,(self.taille_plateau+marge_texte,120))
                
                



                py.display.flip()
            
            

            else:
                if  self.jeu.fin_jeu and not self.mode_manuel:
                    instant_suivant=True
            
            

        # py.quit()

        # plt.close()
        # plt.plot(self.algorithme.liste_scores,self.algorithme.liste_pas,marker='+')
        # plt.show()