import pygame as py

class  Affichage:
    def  __init__(self,facteur,jeu):
        self.facteur=facteur
        self.dimensions=(int(facteur*1920),int(facteur*1080))
        self.jeu=jeu
        self.police=py.font.Font(None,40)
        self.police_petite=py.font.Font(None,20)
        self.fenetre=py.display.set_mode((self.dimensions[0],self.dimensions[1]))

        self.jeu_actif=False
        if  not  self.jeu_actif:
            self.jeu.serpent.pos=[-1,-1]

        self.clique_gauche_souris_en_cours=False
        self.clique_droit_souris_en_cours=False

        self.liste_cases_marquees=[]

        self.liste_pos_aretes_squelette=collections.deque([])




        self.mode_manuel=False

        self.liste_aretes_cycle=[]


        self.marge_cases=0
        self.nb_cases=4
        self.taille_case=(self.dimensions[1]-(self.nb_cases+1)*self.marge_cases)//self.nb_cases
        self.liste_emplacements_cases=self.initialiser_emplacements_cases()

        self.taille_plateau=self.taille_case*self.nb_cases

        self.algorithme=Algorithme(self,self.jeu)


        pos=[rd.randint(0,self.nb_cases-1),rd.randint(0,self.nb_cases-1)]
        #  pos=[1,4]
        self.jeu.pomme=Pomme(pos)

        self.initialiser_pomme()

        self.liste_aretes_cycle=self.initialiser_liste_aretes_cycle()

        self.dico_pos_ecran_aretes=self.initialiser_dico_aretes()



        self.jeu.max_score=self.nb_cases**2-1


    # pour avoir acces a tous les [UL,UR,DR,DL] des pixels
    def  initialiser_emplacements_cases(self):
        liste_emplacements_cases=[]
        for  i  in  range(self.nb_cases):
            for  j  in  range(self.nb_cases):
                UL=(j*(self.taille_case+self.marge_cases)+self.marge_cases,i*(self.taille_case+self.marge_cases)+self.marge_cases)
                DL=(j*(self.taille_case+self.marge_cases)+self.marge_cases,(i+1)*(self.taille_case+self.marge_cases))
                UR=(j*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,i*(self.taille_case+self.marge_cases)+self.marge_cases)
                DR=(j*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,(i+1)*(self.taille_case+self.marge_cases))
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
            print("Perdu")
        elif  self.jeu.score>=self.jeu.max_score:
            print("Partie  gagnée")
            self.jeu.fin_jeu=True

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
        self.jeu.pomme.UL=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases,pos[1]*(self.taille_case+self.marge_cases)+self.marge_cases)
        self.jeu.pomme.DL=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases,(pos[1]+1)*(self.taille_case+self.marge_cases))
        self.jeu.pomme.UR=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,pos[1]*(self.taille_case+self.marge_cases)+self.marge_cases)
        self.jeu.pomme.DR=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,(pos[1]+1)*(self.taille_case+self.marge_cases))
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
        py.draw.polygon(self.fenetre,rouge,[self.jeu.pomme.UL,self.jeu.pomme.UR,self.jeu.pomme.DR,self.jeu.pomme.DL])



    def  dessiner_serpent(self):
        self.dessiner_tete_serpent()
        self.dessiner_queue_serpent()

    def  dessiner_tete_serpent(self):    #  a  opti  avec  dico
        pos=self.jeu.serpent.pos
        UL=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases,pos[1]*(self.taille_case+self.marge_cases)+self.marge_cases)
        DL=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases,(pos[1]+1)*(self.taille_case+self.marge_cases))
        UR=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,pos[1]*(self.taille_case+self.marge_cases)+self.marge_cases)
        DR=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,(pos[1]+1)*(self.taille_case+self.marge_cases))
        py.draw.polygon(self.fenetre,bleu_clair,[UL,UR,DR,DL])

    def  dessiner_queue_serpent(self):      #  a  opti  avec  dico
        for  pos  in  self.jeu.serpent.pos_queue:
            UL=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases,pos[1]*(self.taille_case+self.marge_cases)+self.marge_cases)
            DL=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases,(pos[1]+1)*(self.taille_case+self.marge_cases))
            UR=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,pos[1]*(self.taille_case+self.marge_cases)+self.marge_cases)
            DR=(pos[0]*(self.taille_case+self.marge_cases)+self.marge_cases+self.taille_case,(pos[1]+1)*(self.taille_case+self.marge_cases))
            py.draw.polygon(self.fenetre,bleu,[UL,UR,DR,DL])

    def  initialiser_liste_aretes_cycle(self):
        #  print('init')
        liste_aretes_cycle=[]
        origine=[0,0]
        pos_avant=origine[:]
        pos=self.algorithme.direction_suivante([0,0])

        liste_aretes_cycle.append(([(pos_avant[0]+0.5)*self.taille_case,(pos_avant[1]+0.5)*self.taille_case],[(pos[0]+0.5)*self.taille_case,(pos[1]+0.5)*self.taille_case]))


        for  _  in  range(self.nb_cases**2-1):
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


    def  dessiner_cycle(self):
        epaisseur=3

        for  couple  in  self.liste_aretes_cycle:
            py.draw.line(self.fenetre,noir,*couple,epaisseur)




    def  dessiner_chiffres_chemin(self):      #  a  ameliorer
        liste_surfaces_texte=[]
        for  j  in  range(self.nb_cases):
            for  i  in  range(self.nb_cases):
                texte_surface=self.police_petite.render(str(self.algorithme.numero_depuis_pos([j,i])),True,noir)
                self.fenetre.blit(texte_surface,[(j+0.55)*self.taille_case,(i+0.55)*self.taille_case])

    def  dessiner_plus_court_chemin(self):      #  a  ameliorer
        for  i  in  range(len(self.algorithme.plus_court_chemin)-1):
            py.draw.line(self.fenetre,rouge_fonce,
            [(self.algorithme.plus_court_chemin[i][0]+0.5)*self.taille_case,(self.algorithme.plus_court_chemin[i][1]+0.5)*self.taille_case],
            [(self.algorithme.plus_court_chemin[i+1][0]+0.5)*self.taille_case,(self.algorithme.plus_court_chemin[i+1][1]+0.5)*self.taille_case],
            5)

    def  dessiner_chemin(self,liste_pos,couleur,tronquer_chemin):    #  a  ameliorer
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
                self.liste_cases_marquees.append((j,i))
        elif self.clique_droit_souris():
            souris_x,souris_y=py.mouse.get_pos()
            if  souris_y<=self.taille_plateau  and  souris_x<=self.taille_plateau:
                i=souris_y//self.taille_case
                j=souris_x//self.taille_case

                if (j,i) in self.liste_cases_marquees:
                    self.liste_cases_marquees.remove((j,i))





    def  simuler_modif_cycle(self):
        if  len(self.liste_cases_marquees)==2:
            #  print(2)

            debut=self.liste_cases_marquees[0]
            fin=self.liste_cases_marquees[1]

            self.liste_cases_marquees=[]

            self.jeu.serpent.pos=debut
            self.jeu.serpent.direction=[fin[0]-debut[0],fin[1]-debut[1]]
            if  not  self.algorithme.modifier_cycle():
                print('NON')



    def  loop(self):
        horloge=py.time.Clock()


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
                        self.afficher=not  self.afficher
                    if  event.key==py.K_m:
                        self.mode_manuel=not  self.mode_manuel


                    instant_suivant=False
                    if  self.mode_manuel:
                        if  event.key==py.K_SPACE:
                            instant_suivant=True



            if  not  self.mode_manuel:
                instant_suivant=True



            horloge.tick(self.fps)




            if  instant_suivant:
                instant_suivant=False

                self.jeu.nb_images=(self.jeu.nb_images+1)%60

                if  self.jeu_actif:


                    #  pour  algorithme  pomme-queue
                    if  self.jeu.serpent.pos==self.jeu.pomme.pos:
                        self.algorithme.lock=False




                    self.algorithme.mettre_a_jour_direction()
                    self.mettre_a_jour_direction()

                    self.mettre_a_jour_serpent()

                    self.mettre_a_jour_pomme()

                    self.verifier_fin_jeu()









                    self.jeu.distance_parcourue+=1






                if  self.jeu_actif:
                    self.fenetre.fill(blanc)
                    if  self.afficher:

                        #  print(self.jeu.serpent.pos,self.jeu.serpent.direction)

                        self.dessiner_cases()
                        self.dessiner_pomme()
                        self.dessiner_serpent()
                        self.dessiner_cycle()
                        self.dessiner_squelette_serpent()
                        # self.dessiner_plus_court_chemin()

                        self.dessiner_chemin(self.algorithme.plus_court_chemin_hor,(100,0,0),True)
                        self.dessiner_chemin(self.algorithme.plus_court_chemin_ver,(180,0,0),True)
                        self.dessiner_chemin(self.algorithme.plus_court_chemin,(150,0,0),True)
                        # print(self.algorithme.plus_court_chemin_,)
                        self.dessiner_chemin(self.algorithme.plus_court_chemin_,(10,200,100),False)
                        # self.dessiner_chiffres_chemin()






                #  si  jeu  inactif
                else:
                    self.fenetre.fill(blanc)

                    self.dessiner_cases()


                    self.marquer_case_souris()
                    # self.simuler_modif_cycle()    #  ne  marche  pas
                    self.dessiner_cases_marquees()
                    # self.dessiner_cases_boucles()


                    #  self.dessiner_cycle()
                    #  self.dessiner_chiffres_chemin()
                    # self.algorithme.tracer_murs()    #  labyrinthe


                    # self.algorithme.arbre_possibilites()  # inutile



                if  self.jeu.fin_jeu:
                    continuer=False
                    print(str("Jeu  terminé"))
                    print(str("score:")+str(self.jeu.score))
                    print(str("longueur  parcourue:")+str(self.jeu.distance_parcourue))
                    print("direction",self.jeu.serpent.direction)
                    break



                keys  =  py.key.get_pressed()
                if  keys[py.K_s]:
                    self.fps-=5
                if  keys[py.K_z]:
                    self.fps+=5
                self.fps=np.clip(self.fps,0.3,inf)



                marge_texte=20


                texte_surface1=self.police.render("fps:"+str(round(horloge.get_fps(),1)),True,noir)
                texte_surface2=self.police.render("score:"+str(self.jeu.score),True,noir)
                texte_surface3=self.police.render("distance  parcourue:"+str(self.jeu.distance_parcourue),True,noir)
                self.fenetre.blit(texte_surface1,(self.taille_plateau+marge_texte,0))
                self.fenetre.blit(texte_surface2,(self.taille_plateau+marge_texte,30))
                self.fenetre.blit(texte_surface3,(self.taille_plateau+marge_texte,60))



                py.display.flip()

            else:
                if  self.jeu.fin_jeu:
                    instant_suivant=True

        #  py.quit()

        plt.close()
        plt.plot(self.algorithme.liste_scores,self.algorithme.liste_pas,marker='+')
        # plt.show()