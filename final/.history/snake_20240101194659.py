import  collections
import  pygame  as  py
import  numpy  as  np
import  math
import  random  as  rd
import  copy
import  matplotlib.pyplot  as  plt
import chemin_hamiltonien_rectangle as c

from serpent import Serpent







vert_clair=(150,250,150)
vert_fonce=(105,235,125)
bleu=(0,0,255)
bleu_clair=(100,100,255)
noir=(0,0,0)
blanc=(255,255,255)
rouge=(255,0,0)
rouge_fonce=(160,0,0)

inf=float('inf')

def  difference(x,y):
    if  x<=y:
        return  y-x
    else:
        return  x-y






class  Pomme:
    def  __init__(self,pos):
        self.pos=pos


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



        #  self.generer_chemin_hamiltonien()



        self.chemin=self.generer_chemin_zig_zag_vertical()
        #  self.type_chemin="zig  zag  vertical"
        #  self.chemin=self.generer_chemin_zig_zag_horizontal()
        #  self.type_chemin="zig  zag  horizontal"



        self.chemin_zig_zag_horizontal=self.generer_chemin_zig_zag_horizontal()
        self.chemin_zig_zag_vertical=self.generer_chemin_zig_zag_vertical()








        self.nouveau_chemin=np.copy(self.chemin)

        self.dico_indices=self.generer_dico_indices()
        self.matrice=self.generer_matrice()



        # self.dico_noms=self.dico_noms_canonique()
        self.matrice_adjacence=self.generer_matrice_adjacence()



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

    def  generer_dico_indices(self):
        dico_indices={}
        indice=0
        for  i  in  range(self.affichage.nb_cases):
            for  j  in  range(self.affichage.nb_cases):
                dico_indices[indice]=(j,i)
                indice+=1
        # print(dico_indices)
        return  dico_indices

    def dico_noms_canonique(self):
        dico_noms={}
        numero=0
        for i in range(self.affichage.nb_cases):
            for j in range(self.affichage.nb_cases):
                dico_noms[numero]=(j,i)
                numero+=1

        # print(dico_noms)
        return dico_noms


    def generer_matrice_adjacence(self):
        # print(self.dico_indices)

        matrice=np.zeros((self.affichage.nb_cases**2,self.affichage.nb_cases**2))
        for i in range(self.affichage.nb_cases**2):
            for j in range(self.affichage.nb_cases**2):
                if [self.dico_indices[j][0],self.dico_indices[j][1]] in self.voisins(self.dico_indices[i]):
                    matrice[i,j]=1
                    matrice[j,i]=1

        return matrice

    def  generer_matrice(self):
        matrice=np.zeros((self.affichage.nb_cases**2,self.affichage.nb_cases**2))
        for  i  in  range(self.affichage.nb_cases**2):
            for  j  in  range(self.affichage.nb_cases**2):
                #  print(self.numero_depuis_pos(self.dico_indices[i]),self.numero_depuis_pos(self.dico_indices[j]))
                #  print(self.dico_indices[i],self.dico_indices[j])
                if  abs(int(self.numero_depuis_pos(self.dico_indices[i]))-int(self.numero_depuis_pos(self.dico_indices[j])))==1:
                    matrice[j-1,i-1]=1
                    #  matrice[i-1,j-1]=1
                        #  print(matrice)
        return  matrice

    def  generer_chemin_hamiltonien(self):
        self.liste_murs=self.creer_liste_murs()

        ajouter=[]
        for  couple  in  self.liste_murs:
            ajouter.append([couple[1][:],couple[0][:]])

        self.liste_murs+=ajouter

        self.chemin=self.initialiser_chemin_aleatoire()

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


    def  composante_petite_grille(self,k):    #  renvoie  la  composante  (coordonnées)  de  la  petite  grille  à  partir  d'une  composante  de  la  grande  grille
        if  k%2==0:
            return(k//2)
        else:
            return((k-1)//2)

    def  initialiser_chemin_aleatoire(self):
        chemin=np.array([[0  for  _  in  range(self.affichage.nb_cases)]  for  _  in  range(self.affichage.nb_cases)])

        n=self.affichage.nb_cases//2

        pos=[0,0]
        compteur=0
        direction=[1,0]
        while  compteur<=4*n**2-2:

            pos_n=[self.composante_petite_grille(pos[0]),self.composante_petite_grille(pos[1])]
            if  direction==[1,0]:    #  j  pair
                if  pos[0]%2==0:
                    if  pos_n[1]-1>=0  and  [pos_n,[pos_n[0],pos_n[1]-1]]  in  self.liste_murs:
                        direction=[0,-1]
                elif  pos_n[0]+1>n-1  or  not  [pos_n,[pos_n[0]+1,pos_n[1]]]  in  self.liste_murs:
                    if  [pos_n,[pos_n[0],pos_n[1]+1]]  in  self.liste_murs  or  True:
                        direction=[0,1]

            elif  direction==[-1,0]:      #  j  impair
                if    pos[0]%2==1:
                    if  [pos_n,[pos_n[0],pos_n[1]+1]]  in  self.liste_murs:
                        direction=[0,1]
                elif  pos_n[0]-1<0  or  not  [pos_n,[pos_n[0]-1,pos_n[1]]]  in  self.liste_murs:
                    if  [pos_n,[pos_n[0],pos_n[1]-1]]  in  self.liste_murs  or  True:
                        direction=[0,-1]

            elif  direction==[0,1]:    #  i  impair
                if  pos[1]%2==0:
                    if  pos_n[0]+1<=n-1  and  [pos_n,[pos_n[0]+1,pos_n[1]]]  in  self.liste_murs:
                        direction=[1,0]
                elif  pos_n[1]+1>n-1  or  not  [pos_n,[pos_n[0],pos_n[1]+1]]  in  self.liste_murs:
                    if  [pos_n,[pos_n[0]-1,pos_n[1]]]  in  self.liste_murs  or  True:
                        direction=[-1,0]

            elif  direction==[0,-1]:    #  i  pair
                if  pos[1]%2==1:
                    if  [pos_n,[pos_n[0]-1,pos_n[1]]]  in  self.liste_murs:
                        direction=[-1,0]
                elif  pos_n[1]-1<0  or  not  [pos_n,[pos_n[0],pos_n[1]-1]]  in  self.liste_murs:
                    if  [pos_n,[pos_n[0]+1,pos_n[1]]]  in  self.liste_murs  or  True:
                        direction=[1,0]



            pos[0]+=direction[0]
            pos[1]+=direction[1]

            #  print(pos,  direction)
            compteur+=1
            chemin[pos[1]][pos[0]]=compteur

            #  print('AAAAAAAAAAAAAAAAAAAAAAAA')
            #  for  i  in  range(self.affichage.nb_cases):
            #      print(chemin[i])

        return(chemin)

    def  voisins_petite_grille(self,pos):
        liste_voisins=[]
        for  j  in  range(-1,2):
            for  i  in  range(-1,2):
                if  i*j==0  and  pos[0]+j>=0  and  pos[0]+j<=self.affichage.nb_cases//2-1  and  pos[1]+i>=0  and  pos[1]+i<=self.affichage.nb_cases//2-1  and  (i,j)!=(0,0):
                    #  print(i,j)
                    liste_voisins.append([pos[0]+j,pos[1]+i])
        return(liste_voisins)


    #  def  creer_liste_murs(self):
    #      a_traiter=collections.deque([[0,0]])    #  point  de  départ
    #      deja_traites=[]
    #      vide=collections.deque([])
    #      liste_murs=[]
    #
    #      while  a_traiter!=vide:
    #
    #
    #          liste_voisins=self.voisins_petite_grille(a_traiter[-1])
    #          if  liste_voisins!=[]:
    #              supprimer=True
    #              for  voisin  in  liste_voisins:
    #  if  not  voisin  in  a_traiter  and  not  voisin  in  deja_traites:
    #      supprimer=False
    #              if  supprimer:
    #  a_traiter.pop()
    #              else:
    #  voisin=rd.choice(liste_voisins)
    #  if  not  voisin  in  a_traiter  and  not  voisin  in  deja_traites:
    #      liste_murs.append([a_traiter[-1],voisin])
    #      a_traiter.append(voisin)
    #
    #          else:
    #              a_traiter.pop()
    #
    #          if  a_traiter!=vide:
    #              if  not  a_traiter[-1]  in  deja_traites:
    #  deja_traites.append(a_traiter[-1])
    #
    #
    #
    #      return  liste_murs

    def  creer_liste_murs(self):
        a_traiter=[[0,0]]    #  point  de  départ
        deja_traites=[]
        liste_murs=[]

        while  a_traiter!=[]:

            #  on  choisit  au  hasard  un  sommet
            pos=rd.choice(a_traiter)

            liste_voisins=self.voisins_petite_grille(pos)


            #  s'il  y  a  un  sommet  a  regarder  dans  la  liste  des  voisins,  on  ne  supprime  pas  le  sommet
            supprimer=True
            for  voisin  in  liste_voisins:
                if  not  voisin  in  a_traiter  and  not  voisin  in  deja_traites:
                    supprimer=False
            if  supprimer:
                a_traiter.remove(pos)

            #  cas  ou  on  ne  supprime  pas
            voisin=rd.choice(liste_voisins)
            if  not  voisin  in  a_traiter  and  not  voisin  in  deja_traites:
                liste_murs.append([pos,voisin])
                a_traiter.append(voisin)


            deja_traites.append(pos)

        return  liste_murs

    def  voisins(self,pos):
        liste_voisins=[]
        for  j  in  range(-1,2):
            for  i  in  range(-1,2):
                if  i*j==0  and  pos[0]+j>=0  and  pos[0]+j<=self.affichage.nb_cases-1  and  pos[1]+i>=0  and  pos[1]+i<=self.affichage.nb_cases-1  and  (i,j)!=(0,0):
                    #  print(i,j)
                    liste_voisins.append([pos[0]+j,pos[1]+i])
        return(liste_voisins)

    #  def  tracer(self):
    #      for  i  in  range(len(self.liste_tracer)-1):
    #          py.draw.line(self.affichage.fenetre,noir,self.liste_tracer[i],self.liste_tracer[i+1])

    def  tracer_murs(self):
        coef=self.affichage.taille_case*2
        offset=(self.affichage.taille_case,self.affichage.taille_case)
        for  couple  in  self.liste_murs:
            py.draw.line(self.affichage.fenetre,noir,[offset[0]+couple[0][0]*coef,offset[1]+couple[0][1]*coef],[offset[0]+couple[1][0]*coef,offset[1]+couple[1][1]*coef],2)


    def  scale(self,liste):
        L=[]
        coef=40
        for  i  in  range(len(liste)):
            #  print(liste[:2])
            #  print('i',i)
            #  print(liste[i][0][0])
            L.append([[liste[i][0][0]*coef,liste[i][0][1]*coef],[liste[i][1][0]*coef,liste[i][1][1]*coef]])
        return  L



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
    #  def  mettre_a_jour_direction(self):
    #      if  self.numero_depuis_pos(self.jeu.serpent.pos)<self.jeu.pomme.numero:
    #          if  self.raccourci_croissant():
    #              #  self.modifier_cycle()
    #
    #              pass
    #          else:
    #              self.suivre_chemin()
    #      else:
    #          self.suivre_chemin()
    #      #  else:
    #      #      if  self.aller_vers_0():
    #      #          #  self.modifier_cycle()
    #      #          pass
    #      #      else:
    #      #          self.suivre_chemin()




    """raccourci  croissant  dans  tous  les  cas  (v2  de  raccourci  croissant  seulement)"""  #  ok
    def  mettre_a_jour_direction(self):
        self.raccourci_croissant_sur_cycle()





    """A* avec projection sur queue"""
    # def  mettre_a_jour_direction(self):
    #     self.a_etoile_projection_queue(self.jeu.pomme.pos)



    """A*  que  si  modification"""  #  modifier_cyle  à  reparer..
    #  def  mettre_a_jour_direction(self):
    #      #  if  self.jeu.pomme.numero<self.numero_depuis_pos(self.jeu.serpent.pos):
    #      #      self.inverser_grille()
    #      self.a_etoile(self.jeu.pomme.pos,[])
    #      if  not  self.modifier_cycle():
    #          self.suivre_chemin()
    #          if  self.jeu.serpent.pos_queue!=collections.deque([])  and  [self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]]==self.jeu.serpent.pos_queue[-1]:
    #              self.inverser_grille()
    #              self.suivre_chemin()


    """A*  sans  rien"""
    # def  mettre_a_jour_direction(self):
    #     if self.plus_court_chemin==[]:
    #         self.a_etoile(self.jeu.pomme.pos,[])
    #     else:
    #         self.suivre_chemin_particulier(self.plus_court_chemin)

    # def mettre_a_jour_direction(self):
    #     self.a_etoile(self.jeu.pomme.pos,[])





    """rien"""
    #  def  mettre_a_jour_direction(self):
    #      self.suivre_chemin()


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







    """pomme-taille  avec  modif  (pas  encore  de  chemin)"""  #  ok
    # def  mettre_a_jour_direction(self):    #  a  opti      VOIR  PARITE  DE  VER  ET  HOR
    #
    #     #  reset  les  plus  courts  chemins
    #     if  self.lock:
    #         self.plus_court_chemin_ver=[]
    #         self.plus_court_chemin_hor=[]
    #         self.plus_court_chemin=[]
    #
    #
    #     #  self.changer_chemin_selon_distance()    #  change  de  chemin  selon  les  prédefinis
    #
    #     #  si  on  est  arrive  a  pomme-queue,  on  suit  le  chemin
    #     numero_pos=self.numero_depuis_pos(self.jeu.serpent.pos)
    #     if  numero_pos==(self.jeu.pomme.numero-self.jeu.serpent.taille_queue-1)%self.affichage.nb_cases**2:
    #         self.lock=True
    #
    #     if  self.lock:
    #         self.suivre_chemin()
    #         return
    #
    #     #  aller  a  pomme-queue
    #     self.aller_a_queue_pomme()
    #
    def raccourci_croissant_sur_cycle(self):
        #  avoir  une  belle  courbe  à  la  fin


        # pour optimiser
        if  self.jeu.score>=9*(self.affichage.nb_cases**2)//20:
            self.suivre_chemin()
            return

        self.soustraire(self.numero_depuis_pos(self.jeu.serpent.pos))


        liste_voisins=[voisin  for  voisin  in  self.voisins(self.jeu.serpent.pos)  if  voisin  not  in  self.jeu.serpent.pos_queue]

        liste_pos_suivantes_potentielles=[]
        for  voisin  in  liste_voisins:

            numero_voisin=self.numero_depuis_pos(voisin)

            if  numero_voisin>=0  and  numero_voisin<=self.jeu.pomme.numero:

                ok=True
                for  i  in  range(len(self.jeu.serpent.pos_queue)):
                    numero_pos_queue=self.numero_depuis_pos(self.jeu.serpent.pos_queue[i])

                    if  numero_pos_queue-numero_voisin<i+1:
                        ok=False
                        break
                if  ok:
                    liste_pos_suivantes_potentielles.append(voisin)

        if  liste_pos_suivantes_potentielles==[]:
            self.suivre_chemin()
        else:

            voisin_objectif=max(liste_pos_suivantes_potentielles,key=self.numero_depuis_pos)

            self.jeu.serpent.direction[0]=voisin_objectif[0]-self.jeu.serpent.pos[0]
            self.jeu.serpent.direction[1]=voisin_objectif[1]-self.jeu.serpent.pos[1]

    def  changer_chemin_selon_distance(self):
        #  comparer  longueur  des  plus  court  chemin
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
                    #  print('inf')
                    break

            if  longueur_chemin_zigzag_vertical!=inf:
                self.a_etoile(self.pos_depuis_numero((self.numero_depuis_pos(self.jeu.pomme.pos)-self.jeu.serpent.taille_queue-1)%self.affichage.nb_cases**2),liste_pos_queue_futures)
                longueur_chemin_zigzag_vertical=len(self.plus_court_chemin)
                self.plus_court_chemin_ver=self.plus_court_chemin[:]
                #  print(self.plus_court_chemin)


            #  horizontal
            self.chemin=self.chemin_zig_zag_horizontal

            liste_numeros_futures=[(self.numero_depuis_pos(self.jeu.pomme.pos)-self.jeu.serpent.taille_queue+i)%self.affichage.nb_cases**2  for  i  in  range(self.jeu.serpent.taille_queue+1)]
            liste_pos_queue_futures=[self.pos_depuis_numero(numero)  for  numero  in  liste_numeros_futures]

            for  pos  in  self.jeu.serpent.pos_queue:
                if  pos  in  liste_pos_queue_futures:
                    longueur_chemin_zigzag_horizontal=inf
                    #  print('inf')
                    break

            if  longueur_chemin_zigzag_horizontal!=inf:

                self.a_etoile(self.pos_depuis_numero((self.numero_depuis_pos(self.jeu.pomme.pos)-self.jeu.serpent.taille_queue-1)%self.affichage.nb_cases**2),liste_pos_queue_futures)
                longueur_chemin_zigzag_horizontal=len(self.plus_court_chemin)
                self.plus_court_chemin_hor=self.plus_court_chemin[:]
                #  print(self.plus_court_chemin)


            #  comparaison
            if  longueur_chemin_zigzag_vertical<longueur_chemin_zigzag_horizontal:
                self.chemin=self.chemin_zig_zag_vertical
                #  print('verti')
            elif  longueur_chemin_zigzag_vertical>longueur_chemin_zigzag_horizontal:
                self.chemin=self.chemin_zig_zag_horizontal
                #  print('hori')

            #  print(longueur_chemin_zigzag_vertical,longueur_chemin_zigzag_horizontal)

        self.affichage.actualiser_pomme()

    def  aller_a_pomme_sur_cycle_croissant(self):    #  regarde  le  voisin  qui  rapproche  le  plus  de  la  pomme  selon  le  cycle

        liste_voisins=[voisin  for  voisin  in  self.voisins(self.jeu.serpent.pos)  if  voisin  not  in  self.jeu.serpent.pos_queue]

        voisin_objectif=min(liste_voisins,key=lambda  pos:self.numero_depuis_pos(self.jeu.pomme.pos)-self.numero_depuis_pos(pos))

        #  print(liste_voisins)
        #  print(voisin_objectif)

        self.jeu.serpent.direction[0]=voisin_objectif[0]-self.jeu.serpent.pos[0]
        self.jeu.serpent.direction[1]=voisin_objectif[1]-self.jeu.serpent.pos[1]



    def  aller_a_queue_pomme(self):
        liste_pos_queue_futures=[self.pos_depuis_numero(numero)  for  numero  in  [(self.numero_depuis_pos(self.jeu.pomme.pos)-self.jeu.serpent.taille_queue+i)%(self.affichage.nb_cases**2)  for  i  in  range(self.jeu.serpent.taille_queue+1)]]

        if  self.jeu.pomme_atteinte:
            if  not  self.a_etoile(self.pos_depuis_numero((self.numero_depuis_pos(self.jeu.pomme.pos)-self.jeu.serpent.taille_queue-2)%self.affichage.nb_cases**2),liste_pos_queue_futures):
                self.suivre_chemin()
        else:
            if  not  self.a_etoile(self.pos_depuis_numero((self.numero_depuis_pos(self.jeu.pomme.pos)-self.jeu.serpent.taille_queue-1)%self.affichage.nb_cases**2),liste_pos_queue_futures):
                self.suivre_chemin()









    """raccourcis  croissant  avec  soustraction,  non  abouti"""
    #  def  mettre_a_jour_direction(self):
    #      #  if  self.chemin[self.jeu.serpent.pos[1]][self.jeu.serpent.pos[0]]>self.jeu.pomme.numero:
    #      #      self.inverser_grille()
    #      if  self.raccourci_croissant():
    #          #  print("croissant")
    #          #  print(self.jeu.serpent.pos)
    #          #  print(self.jeu.serpent.direction,'a')
    #          self.soustraire(self.numero_depuis_pos([self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]]))
    #          pass
    #      else:
    #          self.suivre_chemin()


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

    def  modifier_cycle(self):
        numero_desire=self.chemin[self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]][self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0]]
        numero_actuel=self.chemin[self.jeu.serpent.pos[1]][self.jeu.serpent.pos[0]]

        if  numero_actuel==self.affichage.nb_cases**2-1  and  numero_desire==0  or  numero_desire==self.affichage.nb_cases**2-1  and  numero_actuel==0:
            #  print(1)
            return(False)

        #  print()
        #  print(numero_desire)
        #  print(numero_actuel)
        #  print(numero_desire-numero_actuel)
        #  if  abs(numero_desire-numero_actuel)==1:
        #      print()
        #      return(False)



        #  si  ca  coupe  le  cycle  en  deux  boucles

        liste_pos_boucle=[]

        #  if  numero_desire<numero_actuel:
        #      for  i  in  range(self.affichage.nb_cases):
        #          for  j  in  range(self.affichage.nb_cases):
        #              self.chemin[i,j]=self.affichage.nb_cases**2-1-self.chemin[i,j]
        #      numero_desire=self.affichage.nb_cases**2-1-numero_desire
        #      numero_actuel=self.affichage.nb_cases**2-1-numero_actuel

        if  numero_desire>=numero_actuel:
            taille_boucle=numero_desire-numero_actuel-1
        else:
            print('non')
            taille_boucle=numero_desire-1+self.affichage.nb_cases**2-numero_actuel

        #  print(numero_actuel)
        #  print(numero_desire)
        #  print(taille_boucle)

        #  initialisation  de  liste_pos_boucle
        if  numero_desire>=numero_actuel:
            for  i  in  range(self.affichage.nb_cases):
                for  j  in  range(self.affichage.nb_cases):
                    #  if  self.chemin[i][j]>=numero_desire:
                    #      self.chemin[i][j]-=taille_boucle
                    if  numero_desire>self.chemin[i][j]>numero_actuel:
                        #  self.chemin[i][j]-=2
                        liste_pos_boucle.append([j,i])
        else:
            for  i  in  range(self.affichage.nb_cases):
                for  j  in  range(self.affichage.nb_cases):
                    if  self.chemin[i][j]>numero_actuel  or  numero_desire>self.chemin[i][j]:
                        liste_pos_boucle.append([j,i])


        if  len(liste_pos_boucle)==2:    #  a  inclure
            print(2)
            pass
            #  print(2)
            #  return(False)
        #  if  numero_desire<numero_actuel:
        #      if  len(liste_pos_boucle)==self.affichage.nb_cases**2-4:
        #          return(False)

        if  numero_actuel==255  and  numero_desire==2:
            print("PROBLEME  255:2")
            print(liste_pos_boucle)


        if  self.deux_boucles(liste_pos_boucle):

            #  print('cycle  modifié  en',numero_actuel,numero_desire)
            #  self.afficher(self.chemin)




            #  print('AAAAAAA',liste_numeros_petite_boucle)

            if  numero_desire>=numero_actuel:
                if  self.reparer_cycle_croissant(liste_pos_boucle,numero_actuel,numero_desire):
                    self.jeu.pomme.numero=self.chemin[self.jeu.pomme.pos[1]][self.jeu.pomme.pos[0]]
                    self.affichage.initialiser_liste_aretes_cycle()
                    #  print('oui')
                    return  True

                else:
                    #  print('non')
                    return  False
            else:
                if  self.reparer_cycle_decroissant(liste_pos_boucle,numero_actuel,numero_desire):
                    self.jeu.pomme.numero=self.chemin[self.jeu.pomme.pos[1]][self.jeu.pomme.pos[0]]
                    #  self.affichage.initialiser_liste_aretes_cycle()
                    return  True
                else:
                    return  False

        else:
            return  False


    def  deux_boucles(self,liste_pos_boucle):
        numero_desire=self.chemin[self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]][self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0]]
        numero_actuel=self.chemin[self.jeu.serpent.pos[1]][self.jeu.serpent.pos[0]]



        derniere_pos_boucle=self.pos_depuis_numero((numero_desire-1)%(self.affichage.nb_cases**2))
        premiere_pos_boucle=self.pos_depuis_numero((numero_actuel+1)%(self.affichage.nb_cases**2))
        return(derniere_pos_boucle  in  self.voisins(premiere_pos_boucle))





    def  reparer_cycle_croissant(self,liste_pos_boucle,numero_actuel,numero_desire):

        global  numero_desire_uwu
        numero_desire_uwu=numero_desire

        taille_boucle=numero_desire-numero_actuel-1

        pos=self.pos_depuis_numero(0)
        compteur=0
        cycle_ok=False
        deja_traites=[]

        liste_numeros_petite_boucle=[n  for  n  in  range(numero_actuel+1,numero_desire)]

        global  liste_numeros_petite_boucle_uwu
        liste_numeros_petite_boucle_uwu=liste_numeros_petite_boucle


        #  self.nouveau_chemin[:]=self.chemin[:]
        self.nouveau_chemin=copy.deepcopy(self.chemin)
        while  compteur<=self.affichage.nb_cases**2-1:

            if  not  cycle_ok  and  compteur==self.affichage.nb_cases**2-taille_boucle-1:
                break



            numero_pos=self.numero_depuis_pos(pos)
            liste_voisins_pos=self.voisins(pos)

            #  etablissement  de  la  position  suivante
            pos_suivante=None


            global  compteur_uwu
            compteur_uwu=compteur

            #  print(compteur)


            #  cas  ou  numero_pos  est  la  numero_actuel:  il  faut  aller  a  numero  desire
            if  numero_pos==numero_actuel:
                for  voisin  in  liste_voisins_pos:
                    if  not  voisin  in  liste_pos_boucle  and  self.numero_depuis_pos(voisin)==numero_desire:
                        pos_suivante=voisin[:]
                        break

            #  cas  ou  le  compteur  est  au  maximum  et  on  doit  quand  meme  attribuer  une  position  (la  boucle  while  s'arrete  après  cette  itération)
            elif  compteur==self.affichage.nb_cases**2-1:
                pos_suivante=[0,0]

            #  cas  ou  on  doit  avancer  de  un  (rien  de  particulier)
            else:
                for  voisin  in  liste_voisins_pos:
                    if  not  voisin  in  liste_pos_boucle  and  self.numero_depuis_pos(voisin)==numero_pos+1:
                        pos_suivante=voisin[:]
                        break

            #  print('aaaaaaaaaaa')
            #  print(pos)
            #  print(pos_suivante)



            if  not  cycle_ok:

                global  positions_uwu
                positions_uwu=[pos[:],pos_suivante[:],self.affichage.jeu.serpent.pos[:],self.jeu.serpent.pos[:],self.numero_depuis_pos(pos[:]),self.numero_depuis_pos(pos_suivante[:])]

                #  initialisation  du  voisinage  (en  pos  et  en  numero)  de  pos  et  pos_suivante
                liste_voisins_pos_suivante=self.voisins(pos_suivante[:])

                numeros_voisins_pos=[self.numero_depuis_pos(voisin[:])  for  voisin  in  liste_voisins_pos]
                numeros_voisins_pos_suivante=[self.numero_depuis_pos(voisin[:])  for  voisin  in  liste_voisins_pos_suivante]


                #  regarder  si  on  peut  recoller  les  deux  boucles
                debut_fin=[]
                for  numero  in  numeros_voisins_pos:
                    if  debut_fin!=[]:
                        break
                    for  numero_suivant  in  numeros_voisins_pos_suivante:


                        if  numero  in  liste_numeros_petite_boucle[:]  and  numero_suivant  in  liste_numeros_petite_boucle[:]:


                            global  temp3
                            temp3=liste_numeros_petite_boucle

                            #  il  ne  faut  pas  recoller  la  ou  il  y  a  la  queue
                            if  not  pos  in  self.jeu.serpent.pos_queue  and  not  pos_suivante  in  self.jeu.serpent.pos_queue  and  not  numero_pos  in  liste_numeros_petite_boucle[:]  and  not  self.numero_depuis_pos(pos_suivante)  in  liste_numeros_petite_boucle[:]  and  not  numero  in  [numero_actuel,numero_desire]  and  not  numero_suivant  in  [numero_actuel,numero_desire]:

                                global  temp2
                                temp2=liste_numeros_petite_boucle


                                global  temp1
                                temp1=liste_numeros_petite_boucle


                                #  #  ne  pas  recoller  ou  on  va  ou  ou  on  est

                                global  temp
                                temp=liste_numeros_petite_boucle

                                #  ne  pas  qu'on  soit  dans  la  boucle
                                if  numero==numero_suivant+1:





                                    global  numeros_uwu
                                    numeros_uwu=[numero,numero_suivant]



                                    debut_fin=[pos[:],pos_suivante[:]]
                                    #  print(numeros_voisins_pos)
                                    #  print(numeros_voisins_pos_suivante)
                                    #  print(numero)
                                    #  print(numero_suivant)
                                    break



                #  si  on  peut  recoller  les  deux  boucles
                if  debut_fin!=[]:

                    global  numeros_voisins_pos_suivante_uwu
                    numeros_voisins_pos_suivante_uwu=numeros_voisins_pos_suivante

                    global  debut_fin_uwu
                    debut_fin_uwu=debut_fin+[self.numero_depuis_pos(debut_fin[0][:]),self.numero_depuis_pos(debut_fin[1][:])]

                    global  chemin_uwu
                    chemin_uwu=self.chemin


                    #  print(debut_fin)
                    decalage=self.actualiser_boucle_croissant(debut_fin,compteur,numero_actuel,numero_desire,liste_pos_boucle)
                    compteur+=decalage
                    cycle_ok=True
                    #  print('TAILLE  BOUCLE',taille_boucle)

                else:      #  recollage  de  boucle  pas  encore  possible

                    #  on  met  a  jour  le  nouveau  chemin  et  le  compteur
                    self.nouveau_chemin[pos[1]][pos[0]]=compteur
                    compteur+=1

            else:      #  si  les  deux  boucles  sont  deja  recollees
                self.nouveau_chemin[pos[1]][pos[0]]=compteur
                compteur+=1

            #  apres  chaque  iteration  on  met  a  jour  la  liste  deja_traites  et  on  avance
            deja_traites.append(pos[:])
            pos[:]=pos_suivante[:]

        #  si  on  n'a  finalement  rien  trouve
        if  not  cycle_ok:
            #  print('return  False')
            return(False)

        #  self.chemin[:]=self.nouveau_chemin[:]
        self.chemin=copy.deepcopy(self.nouveau_chemin)
        return  True


    def  actualiser_boucle_croissant(self,debut_fin,compteur,numero_actuel,numero_desire,liste_pos_boucle):


        taille_boucle=numero_desire-numero_actuel-1
        self.nouveau_chemin[debut_fin[0][1]][debut_fin[0][0]]=compteur
        #  pos=debut_fin[0]
        #  print("COMPTEUR",compteur)
        #  print(taille_boucle)
        #  print('liste_pos_boucle',liste_pos_boucle)

        #  faire  que  la  pos  de  la  premiere  iteration  est  deja  dans  la  boucle  (car  la  derniere  l'est)
        liste_voisin_debut=self.voisins(debut_fin[0])
        pos_suivante_possibles=[]
        for  voisin  in  liste_voisin_debut:
            if  voisin  in  liste_pos_boucle:
                pos_suivante_possibles.append(voisin)

        pos=min(pos_suivante_possibles,key=self.numero_depuis_pos)[:]

        #  print(pos)


        for  indice_parcours  in  range(0,taille_boucle):

            liste_voisins_pos=self.voisins(pos)
            numero_pos=self.numero_depuis_pos(pos)


            #  etablissement  de  la  position  suivante
            pos_suivante=None

            #  cas  ou  on  est  là  ou  la  boucle  s'est  recollee  (a  numero_desire-1)
            if  numero_pos==numero_desire-1:
                for  voisin  in  liste_voisins_pos:
                    if  self.numero_depuis_pos(voisin)==numero_actuel+1  and  voisin  in  liste_pos_boucle:
                        pos_suivante=voisin
                        break

            #  si  on  est  a  la  toute  fin  de  l'actualisation  de  la  boucle  on  s'en  fiche  de  pos_suivante
            elif  indice_parcours==taille_boucle-1:
                pos_suivante=[-1,-1]

            #  cas  ou  rien  d'anormal,  on  suit  le  chemin  donne  par  la  boucle
            else:
                for  voisin  in  liste_voisins_pos:
                    if  self.numero_depuis_pos(voisin)==numero_pos+1:
                        pos_suivante=voisin
                        break


            #  print('ppppppp')
            #  print(debut_fin)
            #  print(indice_parcours)
            #  print(pos)
            #  print(pos_suivante)



            #  mettre  a  jour  nouveau  chemin  et  position
            self.nouveau_chemin[pos[1]][pos[0]]=compteur+indice_parcours+1
            pos[:]=pos_suivante[:]

        #  self.afficher(self.nouveau_chemin)
        return(indice_parcours+2)


    def  reparer_cycle_decroissant(self,liste_pos_boucle,numero_actuel,numero_desire):      #  2

        pos=self.pos_depuis_numero(numero_desire)
        compteur=0
        cycle_ok=False

        liste_numeros_petite_boucle=[n  for  n  in  range(0,numero_desire)]+[n  for  n  in  range(numero_actuel+1,self.affichage.nb_cases**2)]

        self.nouveau_chemin=copy.deepcopy(self.chemin)

        compteur_fantome=0
        while  compteur<=self.affichage.nb_cases**2-1:
            numero_pos=self.numero_depuis_pos(pos)
            liste_voisins_pos=self.voisins(pos)



            #  etablissement  de  la  position  suivante
            pos_suivante=None


            #  cas  ou  numero_pos  est  la  numero_actuel:  il  faut  aller  au  numero  desire
            if  numero_pos==numero_actuel:
                #  print('1')
                for  voisin  in  liste_voisins_pos:
                    if  not  voisin  in  liste_pos_boucle  and  self.numero_depuis_pos(voisin)==numero_desire:
                        pos_suivante=voisin
                        break

            #  cas  ou  on  est  sur  debut_fin[0]  apres  la  reparation  du  cycle,  on  va  au  voisin  suivant  dans  la  boucle
            elif  cycle_ok  and  pos==debut_fin[0]:
                #  print('2')
                pos_suivantes_possibles=[]
                for  voisin  in  liste_voisins_pos:
                    if  voisin  in  liste_pos_boucle:
                        pos_suivantes_possibles.append(voisin)

                pos_suivante=min(pos_suivantes_possibles,key=self.numero_depuis_pos)[:]


            #  cas  ou  on  est  dans  la  boucle  apres  la  reparation  du  cycle:  avancer  de  1  dans  la  boucle
            elif  pos  in  liste_pos_boucle:
                #  print('3')
                for  voisin  in  liste_voisins_pos:
                    if  voisin  in  liste_pos_boucle  and  self.numero_depuis_pos(voisin)==(numero_pos+1)%self.affichage.nb_cases**2:
                        pos_suivante=voisin
                        break

            #  cas  ou  on  doit  avancer  de  un  (rien  de  particulier)
            else:
                #  print('4')
                for  voisin  in  liste_voisins_pos:
                    if  not  voisin  in  liste_pos_boucle  and  self.numero_depuis_pos(voisin)==numero_pos+1:
                        pos_suivante=voisin
                        break


            #  cas  ou  on  est  dans  la  boucle  et  pas  de  voisin+1
            if  pos  in  liste_pos_boucle  and  pos_suivante==None:
                #  print('5')
                pos_suivantes_possibles=[]
                for  voisin  in  liste_voisins_pos:
                    if  voisin  in  liste_pos_boucle  and  self.numero_depuis_pos(voisin)>numero_actuel:
                        pos_suivantes_possibles.append(voisin)
                pos_suivante=min(pos_suivantes_possibles,key=self.numero_depuis_pos)[:]

            #  print('aaaaaaaaaaa')
            #  print(pos)
            #  print(pos_suivante)



            if  not  cycle_ok:

                #  initialisation  du  voisinage  (en  pos  et  en  numero)  de  pos  et  pos_suivante
                liste_voisins_pos_suivante=self.voisins(pos_suivante)

                numeros_voisins_pos=[self.numero_depuis_pos(voisin)  for  voisin  in  liste_voisins_pos]
                numeros_voisins_pos_suivante=[self.numero_depuis_pos(voisin)  for  voisin  in  liste_voisins_pos_suivante]

                #  regarder  si  on  peut  recoller  les  deux  boucles
                debut_fin=[]
                entree_sortie=[]
                if  numero_pos!=numero_desire  and  numero_pos!=numero_desire+1:
                    for  numero  in  numeros_voisins_pos:
                        if  debut_fin!=[]:
                            break
                        for  numero_suivant  in  numeros_voisins_pos_suivante:

                            #  il  faut  que  le  recollage  soit  avec  des  numeros  plus  faibles
                            if  max(numero,numero_suivant)>numero_pos+1:
                                continue

                            #  il  ne  faut  pas  recoller  la  ou  il  y  a  la  queue
                            if  pos  in  self.jeu.serpent.pos_queue  or  pos_suivante  in  self.jeu.serpent.pos_queue:
                                continue

                            if  numero  in  liste_numeros_petite_boucle  and  numero_suivant  in  liste_numeros_petite_boucle:
                                if  numero==numero_suivant+1:

                                    #  if  self.pos_depuis_numero(numero)  in  self.jeu.serpent.pos_queue  or  self.pos_depuis_numero(numero_suivant)  in  self.jeu.serpent.pos_queue:
                                    #      continue

                                    debut_fin=[pos[:],pos_suivante[:]]
                                    entree_sortie=[numero_suivant,numero]
                                    #  print(numeros_voisins_pos)
                                    #  print(numeros_voisins_pos_suivante)
                                    #  print(numero)
                                    #  print(numero_suivant)
                                    break

                #  si  on  peut  recoller  les  deux  boucles
                if  debut_fin!=[]:
                    self.reindicage_chemin(debut_fin,entree_sortie,numero_actuel,numero_desire)
                    break

            else:      #  si  les  deux  boucles  sont  deja  recollees
                compteur+=1

            #  apres  chaque  iteration  on  met  a  jour  la  liste  deja_traites  et  on  avance
            #  deja_traites.append(pos[:])
            pos[:]=pos_suivante[:]

            #  faire  que  si  ca  ne  trouve  rien,  la  boucle  while  s'arrete  quand  meme
            compteur_fantome+=1
            if  compteur_fantome>self.affichage.nb_cases**2-1:
                break

        #  si  on  n'a  finalement  rien  trouve
        if  not  cycle_ok:
            #  print('return  False')
            return(False)


        #  print('o')
        self.chemin=copy.deepcopy(self.nouveau_chemin)
        return  True



    def  modifier_cycle(self):
        self.pos_boucle_1=[]
        self.pos_boucle_2=[]


        numero_actuel=self.numero_depuis_pos(self.jeu.serpent.pos)
        numero_desire=self.numero_depuis_pos([self.jeu.serpent.pos[0]+self.jeu.serpent.direction[0],self.jeu.serpent.pos[1]+self.jeu.serpent.direction[1]])

        if  numero_desire>=numero_actuel:
            difference_numero=numero_desire-numero_actuel
        else:
            difference_numero=numero_actuel-numero_desire

        if  difference_numero  in  [-1,0,1,self.affichage.nb_cases**2-1]:
            return  False







        #  etablissement  des  pos  des  deux  boucles
        pos=[0,0]      #  a  l'origine

        pos_boucle_1=[]
        pos_boucle_2=[]

        boucle_actuelle=1

        parite=None


        direction=self.direction_suivante(pos[:])

        pos_suivante=[pos[0]+direction[0],pos[1]+direction[1]]


        if  len(self.jeu.serpent.pos_queue)==0:
            parite=1
        else:
            #  cas  ou  on  est  croissant
            if  self.numero_depuis_pos(self.jeu.serpent.pos_queue[-1])<self.numero_depuis_pos(self.jeu.serpent.pos):
                #  raccourci  croissant
                if  self.numero_depuis_pos(pos_suivante)>self.numero_depuis_pos(self.jeu.serpent.pos):
                    parite=1
                else:
                    parite=2
            #  cas  ou  on  est  decroissant
            else:
                print('décroissant')
                #  raccourci  croissant
                if  self.numero_depuis_pos(pos_suivante)>self.numero_depuis_pos(self.jeu.serpent.pos):
                    parite=2
                else:
                    parite=1

        #  parite=1


        print(parite)





        for  _  in  range(self.affichage.nb_cases**2):

            direction=self.direction_suivante(pos[:])

            pos_suivante=[pos[0]+direction[0],pos[1]+direction[1]]


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


        #  si  les  deux  boucles  ne  sont  pas  faites  au  bon  endroit
        if  len(self.jeu.serpent.pos_queue)==0:


            if  difference(pos_boucle_2[0][0],pos_boucle_2[-1][0])  not  in  [0,1]  or  difference(pos_boucle_2[0][1],pos_boucle_2[-1][1])  not  in  [0,1]:
                #  print(difference(pos_boucle_2[-1][0],pos_boucle_2[-1][1]))
                pos_boucle_1.remove(self.pos_depuis_numero(numero_actuel))
                pos_boucle_1.remove(self.pos_depuis_numero(numero_desire))
                pos_boucle_2.insert(0,self.pos_depuis_numero(min(numero_actuel,numero_desire)))
                pos_boucle_2.append(self.pos_depuis_numero(max(numero_actuel,numero_desire)))

                #  print('correction')


        #  si  on  veut  les  voir
        self.pos_boucle_1=pos_boucle_1
        self.pos_boucle_2=pos_boucle_2


        #  print(pos_boucle_1)
        #  print(pos_boucle_2)

        #  on  verifie  que  les  deux  boucles  sont  bien  des  boucles
        if  difference(pos_boucle_2[0][0],pos_boucle_2[-1][0])  not  in  [0,1]  or  difference(pos_boucle_2[0][1],pos_boucle_2[-1][1])  not  in  [0,1]:
            return  False

        for  i  in  range(len(pos_boucle_1)-1):
            if  pos_boucle_1[i]  not  in  self.voisins(pos_boucle_1[i+1]):
                #  print('boucle')
                return  False

        for  i  in  range(len(pos_boucle_2)-1):
            if  pos_boucle_2[i]  not  in  self.voisins(pos_boucle_2[i+1]):
                #  print('boucle')
                return  False



        #  on  cherche  a  recoller  les  boucles
        pos_boucle=pos_boucle_1[:]

        for  i  in  range(len(pos_boucle)-1):
            liste_voisins=self.voisins(pos_boucle[i])
            liste_voisins_suivant=self.voisins(pos_boucle[i+1])


            depart_arrivee_1=[]
            depart_arrivee_2=[]

            #  on  regarde  les  voisinages
            for  voisin  in  liste_voisins:
                #  si  on  a  trouvé
                if  depart_arrivee_1!=[]:
                    break
                for  voisin_suivant  in  liste_voisins_suivant:
                    #  pour  recoller  entre  les  deux  boucles
                    if  voisin  not  in  pos_boucle  and  voisin_suivant  not  in  pos_boucle:
                        #  pour  ne  pas  recoller  la  ou  on  va  ou  est
                        print(self.numero_depuis_pos(voisin),self.numero_depuis_pos(voisin_suivant),self.numero_depuis_pos(pos_boucle[i][:]),self.numero_depuis_pos(pos_boucle[i+1][:]))
                        if  self.numero_depuis_pos(voisin)  not  in  [numero_actuel,numero_desire]  and  self.numero_depuis_pos(voisin_suivant)  not  in  [numero_actuel,numero_desire]  and  self.numero_depuis_pos(pos_boucle[i][:])  not  in  [numero_actuel,numero_desire]  and  self.numero_depuis_pos(pos_boucle[i+1][:])  not  in  [numero_actuel,numero_desire]:
                            if  pos_boucle[i][:]  not  in  self.jeu.serpent.pos_queue  and  pos_boucle[i+1][:]  not  in  self.jeu.serpent.pos_queue  and  voisin[:]  not  in  self.jeu.serpent.pos_queue  and  voisin_suivant[:]  not  in  self.jeu.serpent.pos_queue:
                                if  difference(self.numero_depuis_pos(voisin),self.numero_depuis_pos(voisin_suivant))==1:
                                    depart_arrivee_1=[pos_boucle[i][:],pos_boucle[i+1][:]]
                                    depart_arrivee_2=[voisin[:],voisin_suivant[:]]
                                    break

                            if  depart_arrivee_1!=[]:
                                break
                        #  print(depart_arrivee_1,depart_arrivee_2)

        if  depart_arrivee_1==[]:
            #  print('pas  boucle')
            return  False



        #  on  reindice
        pos=[0,0]
        pos_suivante=None
        nouveau_chemin=copy.deepcopy(self.chemin)
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

            nouveau_chemin[pos[
1],pos[0]]=_
            pos=pos_suivante[:]

        self.chemin=nouveau_chemin[:]
        #  print(self.chemin)
        self.affichage.liste_aretes_cycle=self.affichage.initialiser_liste_aretes_cycle()

        return  True



    def arbre_possibilites(self):
        if len(self.affichage.liste_cases_marquees)==2:

            debut=self.affichage.liste_cases_marquees[0]
            fin=self.affichage.liste_cases_marquees[1]

            print(self.longueur_plus_court_chemin(debut,fin))

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
            if  pos_suivante==None:
                #  print('5')
                pos_suivantes_possibles=[]
                for  voisin  in  liste_voisins_pos:
                    if  voisin  in  liste_pos_boucle  and  self.numero_depuis_pos(voisin)>numero_actuel:
                        pos_suivantes_possibles.append(voisin)
                pos_suivante=min(pos_suivantes_possibles,key=self.numero_depuis_pos)[:]

            self.nouveau_chemin[pos[1]][pos[0]]=compteur

    def mettre_a_jour_plus_court_chemin(self,plus_court_chemin):
        plus_court_chemin.remove(self.jeu.serpent.pos)

    """
    def  actualiser_boucle_decroissant(self,debut_fin,compteur,numero_actuel,numero_desire,liste_pos_boucle):


        taille_boucle=self.affichage.nb_cases**2-numero_actuel+numero_desire-1
        #  self.nouveau_chemin[debut_fin[0][1]][debut_fin[0][0]]=compteur
        #  pos=debut_fin[0]
        #  print("COMPTEUR",compteur)
        #  print(taille_boucle)
        #  print('liste_pos_boucle',liste_pos_boucle)

        print([self.numero_depuis_pos(debut_fin[0]),self.numero_depuis_pos(debut_fin[1])])

        #  faire  que  la  pos  de  la  premiere  iteration  est  deja  dans  la  boucle  (car  la  derniere  l'est)
        liste_voisin_debut=self.voisins(debut_fin[0])
        pos_suivante_possibles=[]
        for  voisin  in  liste_voisin_debut:
            if  voisin  in  liste_pos_boucle:
pos_suivante_possibles.append(voisin)

        pos=min(pos_suivante_possibles,key=self.numero_depuis_pos)[:]

        #  print(pos)

        actualiser=False    #  on  n'actualise  qu'a  partir  du  debut  du  cycle  ([0,0]  ici)
        indice_parcours=0

        for  _  in  range(0,taille_boucle):

            liste_voisins_pos=self.voisins(pos)
            numero_pos=self.numero_depuis_pos(pos)


            #  etablissement  de  la  position  suivante
            pos_suivante=None

            #  cas  ou  on  est  là  ou  la  boucle  s'est  recollee  (a  numero_desire-1)
            if  numero_pos==numero_desire-1:
for  voisin  in  liste_voisins_pos:
    if  self.numero_depuis_pos(voisin)==numero_actuel+1  and  voisin  in  liste_pos_boucle:
        pos_suivante=voisin
        break



            #  si  on  est  a  la  toute  fin  de  l'actualisation  de  la  boucle  on  s'en  fiche  de  pos_suivante
            elif  _==taille_boucle-1:
pos_suivante=[-1,-1]

            #  cas  ou  rien  d'anormal,  on  suit  le  chemin  donne  par  la  boucle
            else:
for  voisin  in  liste_voisins_pos:
    if  self.numero_depuis_pos(voisin)==(numero_pos+1)%self.affichage.nb_cases**2:
        pos_suivante=voisin
        break

            #  si  pas  de  pos  suivante,  il  y  a  un  saut  a  faire
            if  pos_suivante==None:
pos_suivantes_possibles=[]
for  voisin  in  liste_voisins_pos:
    if  voisin  in  liste_pos_boucle  and  self.numero_depuis_pos(voisin)>numero_actuel:
        pos_suivantes_possibles.append(voisin)
        break

pos_suivante=min(pos_suivante_possibles,key=self.numero_depuis_pos)[:]



            if  numero_pos==0:
actualiser=True


            #  print('ppppppp')
            #  print(indice_parcours)
            #  print(pos)
            #  print(pos_suivante)



            #  mettre  a  jour  nouveau  chemin  et  position
            if  actualiser:
self.nouveau_chemin[pos[1]][pos[0]]=indice_parcours
indice_parcours+=1
            pos[:]=pos_suivante[:]

        self.afficher(self.nouveau_chemin)

        return(indice_parcours)
    """


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
                        pos_queue_predits=pos_queue[(profondeur-1):]

                # si on n'est pas sur la pomme
                else:
                    pos_queue_predits=pos_queue[(profondeur):]

                # print(pos_queue_predits)
            else:
                pos_queue_predits=pos_queue


            if fin in pos_queue_predits:
                pos_queue_predits.remove(fin)



            for  voisin  in  liste_voisins:
                if  not  voisin  in  pos_queue_predits  and  not  voisin  in  liste_pos_murs:
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
                if  self.jeu.pomme_atteinte:
                    if  profondeur==0:
                        liste_pos_eviter_predits=liste_pos_eviter
                    else:
                        liste_pos_eviter_predits=liste_pos_eviter[(profondeur-1):]

                # si on n'est pas sur la pomme
                else:
                    liste_pos_eviter_predits=liste_pos_eviter[(profondeur):]

            else:
                # print('eviter',liste_pos_eviter)
                liste_pos_eviter_predits=liste_pos_eviter[:]


            if fin in liste_pos_eviter_predits:
                liste_pos_eviter_predits.remove(fin)



            for  voisin  in  liste_voisins:
                if  not  voisin  in  liste_pos_eviter_predits:
                    cout_g=abs(voisin[0]-debut[0])+abs(voisin[1]-debut[1])
                    cout_h=abs(voisin[0]-fin[0])+abs(voisin[1]-fin[1])
                    cout_f=cout_g+cout_h


                    if  not  (voisin[0],voisin[1])  in  dico_couts  or  cout_f<dico_couts[(voisin[0],voisin[1])]:
                        a_traiter.append(voisin)
                        dico_parents[(voisin[0],voisin[1])]=pos[:]
                        dico_couts[(voisin[0],voisin[1])]=cout_f

        print("A* pas de chemin")
        return  False



    def  a_etoile_projection_queue(self,fin):    #  regarder  tout  les  plus  courts  chemins!!!!
        # si pas de queue
        if  self.jeu.serpent.taille_queue==0:
            # juste A* sur la pomme
            self.a_etoile(self.jeu.pomme.pos,[],False)
            return

        if self.jeu.pomme_atteinte:
            self.aller_sur_pomme=False

            # si on a une queue
            if  self.a_etoile(self.jeu.pomme.pos,[],False):

                liste_pos_apres_deplacement=self.liste_pos_apres_deplacement_chemin(list(self.jeu.serpent.pos_queue)+[self.jeu.serpent.pos],self.plus_court_chemin)
                if  self.a_etoile_neutre(self.jeu.pomme.pos,liste_pos_apres_deplacement[0],liste_pos_apres_deplacement,False):
                    self.aller_sur_pomme=True
                    print('aller sur pomme')
                    print(self.plus_court_chemin_)
                    return
                else:
                    self.aller_sur_pomme=False
                    print('revient queue')
                    self.a_etoile(self.jeu.serpent.pos_queue[0],[],False)
                    return

            else:
                self.a_etoile(self.jeu.serpent.pos_queue[0],[],False)
                print("PCC",self.plus_court_chemin,self.plus_court_chemin_)
                print('reste2')
                return

        # si pomme pas atteinte
        else:
            if not self.aller_sur_pomme:
                # si on a une queue
                if  self.a_etoile(self.jeu.pomme.pos,[],False):

                    liste_pos_apres_deplacement=self.liste_pos_apres_deplacement_chemin(list(self.jeu.serpent.pos_queue)+[self.jeu.serpent.pos],self.plus_court_chemin)
                    # print(liste_pos_apres_deplacement,self.plus_court_chemin)
                    if  self.a_etoile_neutre(self.jeu.pomme.pos,liste_pos_apres_deplacement[0],liste_pos_apres_deplacement,False):
                        self.aller_sur_pomme=True
                        print('go sur pomme,c est ok')
                        # print(self.plus_court_chemin_)
                        return

                # self.a_etoile_neutre(self.jeu.serpent.pos,self.jeu.serpent.pos_queue[0],list(self.jeu.serpent.pos_queue),False)
                # self.suivre_chemin_particulier(self.plus_court_chemin_)
                self.a_etoile(self.jeu.serpent.pos_queue[0],[],False)
                print('go sur queue')
                return

            else:
                print("go pomme, c est ok")
                self.suivre_chemin_particulier(self.plus_court_chemin)
                return

        print("ABORT")


    def  liste_pos_apres_deplacement_chemin(self,liste_pos,chemin):
        taille_chemin=len(chemin)
        taille_liste_pos=len(liste_pos)
        #  print('LEN  POS',len(liste_pos))

        if self.jeu.pomme_atteinte:

            if  taille_liste_pos<taille_chemin:
                liste_pos_post=chemin[(taille_chemin-taille_liste_pos-1):]
            elif  taille_liste_pos>=taille_chemin:
                #  print('b')
                #  print('true',liste_pos,chemin)
                difference_taille=taille_liste_pos-taille_chemin
                liste_pos_post=[liste_pos[0]]
                liste_pos_post+=liste_pos
                liste_pos_post+=chemin[1:]
                liste_pos_post=liste_pos_post[(taille_chemin-2):]

                print("list",liste_pos_post)

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
        return  liste_pos_post

    def suivre_chemin_particulier(self,chemin):
        for i in range(len(chemin)-1):
            if self.jeu.serpent.pos==chemin[i]:
                self.jeu.serpent.direction=[chemin[i+1][0]-self.jeu.serpent.pos[0],chemin[i+1][1]-self.jeu.serpent.pos[1]]
                return

        print("fonction suivre_chemin_particulier, pas de direction trouvée")



    def  numero_depuis_pos(self,pos):
        #  print(self.chemin[pos[1]][pos[0]])
        return  int(self.chemin[pos[1],pos[0]])






    def  pos_depuis_numero(self,numero):
        for  i  in  range(self.affichage.nb_cases):
            for  j  in  range(self.affichage.nb_cases):
                if  self.chemin[i][j]==numero:
                    return([j,i])
                        #  print('pos_depuis_numero(),numero  pas  sur  la  grille')

#
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
        numero_suivant=self.chemin[pos[1]][pos[0]]+1
        #  dir_0=[0,0]
        if  numero_suivant==self.affichage.nb_cases**2:
            numero_suivant=0
        for  j  in  range(-1,2):
            for  i  in  range(-1,2):
                if  i*j==0  and  pos[0]+j>=0  and  pos[0]+j<=self.affichage.nb_cases-1  and  pos[1]+i>=0  and  pos[1]+i<=self.affichage.nb_cases-1:
                    if  self.chemin[pos[1]+i][pos[0]+j]==numero_suivant:
                        return  [j,i]
                    #  if  self.chemin[pos[1]+i][pos[0]+j]==0:
                    #      dir_0=[j,i]
                        #  return(dir_0)
        print("pas  de  direction  suivante  trouvee")


    def  suivre_chemin(self):
        self.jeu.serpent.direction=self.direction_suivante([self.jeu.serpent.pos[0],self.jeu.serpent.pos[1]])





def  parcours(chemin):
    memoire=[]
    for  i  in  range(len(chemin)):
        for  j  in  range(len(chemin)):
            if  affichage.algorithme.numero_depuis_pos([j,i])  in  memoire:
                print([j,i])
            memoire.append(affichage.algorithme.numero_depuis_pos([j,i]))



liste_pas=[]
for  _  in  range(1):
    py.init()

    py.display.set_caption("le  serpent  qui  mange  des  pommes  et  grandit")

    jeu=Jeu(Serpent([0,0]))
    affichage=Affichage(0.5,jeu)
    affichage.afficher=True
    affichage.fps=10
    affichage.loop()
    liste_pas.append(jeu.distance_parcourue)
    #  print(_,np.mean(liste_pas))
    #  print()

    #  del  jeu
    #  del  affichage

#  print("FINAL",np.mean(liste_pas))


"""autre"""
#  peut  on  avoir  tous  les  cycles  hamiltoniens  via  la  methode  des  murs?  NON  VRAIMENT  PAS  DU  TOUT
#  position  de  securité=avoir  un  plus  court  chemin  jusqu'à  bout  de  la  queue?  NON CAR ON PEUT MOURIR SI ON SUIT LA QUEUE SI LA POMME APPARAIT TOUJOURS DEVANT NOUS (ET IL NE FAUT PAS SE LIMITER QU'A UN CHEMIN CAR ON PEUT BOUCLER)
#  il  faut  compter  le  nombre  de  cycles  hami  BIBLIO  OK

"""idées  randoms"""
#  faire  que  s'il  y  a  deux  plus  courts  chemins:  prend  le  meilleur
#  faire  qu'on  se  ramene  tjrs  avec  des  raccourcis  croissants  via  une  soustraction  de  tout  les  numeros  à  chaque  raccourcis
#  regarder  tout  les  chemins  possibles  et  y  mettre  un  score?
#  encodage:  mettre  un  poids  sur  chaque  element  de  la  queue  pour  designer  le  nombre  de  pas  necessaires  avant  que  la  place  soit  libre:  peut  servir  de  faire  un  "floodfill"  pour  avoir  une  carte  de  dans  combien  de  pas  telle  case  sera  disponible
#  pour  trouver  un  cycle  plus  long  chemin  (presque)  avec  condition  on  peut:  faire  plus  court  chemin  de  tete  jusqu'a  queue  sans  passer  par  queue  puis  etendre  le  chemin  un  maximum  depuis  la  tete  (via  deque  (file))
#  changer  matrice  adjacence  en  fonction  de  pos  du  serpent  (actualiser  a  chaque  pas)  comme  ça  on  s'en  fiche  des  conditions  pour  trouver  un  cycle  hami  qui  passe  sur  le  corps.  On  a  juste  a  retirer  des  aretes  du  graphe


"""truc  a  faire"""
#  ne  pas  dessiner  double  les  fps!!!
#  tracer  le  nombre  de  pas  parcouru  en  fonction  du  score  (moyennes)
#  optimiser  recherche  dans  listes  en  utilisant  des  np.array
#  tracer  une  matrice  d'adjacence??

""" ameliorer"""
# modif  cycles  pour  le  cas  taille_boucle=2  et  reessayer  A*  que  si  modif
#  faire  quand  on  repare  (pour  l'endroit)  qu'on  ne  doit  regarder  que  la  ou  le  serpent  SERA  et  pas  ou  il  EST
#  effet  des  modifications  de  cycle  sur  les  indices  de  pommes  par  rapport  aux  indices  de  tete  serpent  via  raccourci  croissant?  réindicer  pour  avoir  0  en  (0,0)??  NE  CHANGERA  RIEN  NON  CAR  NE  CHANGE  PAS  SI  POMME  AVANT  OU  APRES  LE  SERPENT
#  regarder  que  le  A*  a  un  nombre  maximal  d'itération:  s'il  n'y  a  pas  de  chemin  alors  on  stop  la  recherche  NECESSAIRE?
#  on  peut  avoir  un  "cycle  hamiltonien"  si  grille  de  coté  impair:  on  n'a  qu'à  en  considerer  deux  symétriques  (de  rotation  pi  de  centre  le  milieu)  et  alterner  entre  chaque.  chiant  et  inutile  (pas  interessant)  OK
#  il  faut  reussir  a  caracteriser  les  endroits  ou  on  ne  peut  pas  modifier  le  cycle  a  l'aide  des  deux  boucles.  et  regarder  quand  on  ne  peut  pas,  on  a  un  chemin  eulerien,  comme  le  transformer  en  cycle  hami?
#  il  faut  reussir  a  encoder  les  cycles  hamiltoniens  indépendamment  de  la  numerotation:  matrice  d'adjacence  à  isomorphisme  de  graphes  près?  et  que  dire  de  la  matrice  d'adjacence  pour  un  cycle?  REGARDER  INTERIEUR  DU  CYCLE??
#  faire  que  dans  la  fonction  modifier_cycle,  on  ne  regarde  pas  la  modif  de  cycle  si  on  ne  fait  que  suivre  le  chemin  (probleme  d'overflow...)
#  pour  A*  que  si  modif,  on  doit  IMPERATIVEMENT  regarder  plusieurs  (voire  tous)  les  plus  courts  chemin  et  ne  pas  passer  la  ou  il  y  a  impossibilité  de  modifier  cycle  (ca  sera  une  paire  de  sommet,  il  ne  faut  pas  qu'elle  soit  sur  le  cycle).  ou  si  on  doit  y  passer,  on  doit  pouvoir  faire  un  raccourci  sans  modif
#  penser  à  anticiper  là  ou  on  sera  dans  n  coups
# pour A* quand on regarde si on peut etre safe après le plus court chemin, on peut ne pas regarder que si on peut faire un plus court chemin vers le bout de la queue: on peut regarder plus long chemin vers queue, regarder si on a assez d'espace pour faire n coups où n est la taille de la queue


"""methodes"""
#  A*  idées:  faire  un  A*  naif  qui  ne  coupe  pas  le  plateau  en  deux,  si  la  pomme  est  trop  proche  le  serpent  l'evite
#  partir  d'un  chemin  zigzag  et  faire  du  A*  (à  modifier)  avec  modif,  une  fois  la  pomme  mangee  et  queue  pas  trop  la,  remettre  chemin  zigzag  (ou  le  passer  en  vertical  (resp.  horizontal)
#  raccourcis  croissants  n'ont  pas  tant  besoin  de  marge,  si  on  ne  fait  que  manger  des  pommes,  on  sera  collé  a  notre  queue  et  la  pomme  apparaitra  ailleurs NON DU COUP
#  faire  un  A*  et  a  chaque  instant  regarder  s'il  existe  un  cycle  hamiltonien  passant  par  la  queue  du  serpent
#  faire  un  A*  naif  tq  tjrs  avoir  une  sécurité,  si  on  va  la  briser  on  passe  sur  un  graphe  hamiltonien  qui  satisfasse  les  conditions  ON  POURRA  TOUJOURS??
#  on  peut  faire  un  A*  naif  et  verifier  pour  chaque  chemin  si  depuis  la  pomme  on  peut  parcourir  une  distance  de  la  taille  de  la  queue+1
#  au  lieu  de  prendre  la  marge  avant,  on  peut  eviter  la  ou  on  sera:  A*  sur  pomme  sans  modif  en  evitant  futures  positions  (mais  probleme  si  pomme  arrive  dans  suite  du  chemin,  on  peut  alors  regarder  chemin  vers  bout  queue?)
#  regarder  (plus  courts)  chemins  tels  que  on  est  croissant  sur  la  numerotation  du  cycle  (réindicer  si  besoin..)  OK  ENVIRON

#  regarder  "brutalement"  avec  des  arbres  les  possibilités  (heuristique,  encodage  efficient..)
# on regarde arbre de possibilités avec une profondeur max, pour augmenter la profondeur on peut faire un monte carlo
# on peut faire un reseau de neuronnes et au fil des parties, on repere les chemins qui marchent le mieux et le monte carlo devient de moins en moins probabiliste

#  on  fait  A*  de  tete  a  pomme,  si  ok  on  A*  de  pomme  a  bout  de  queue  (celui  qui  sera  lorsqu'on  mange  pomme),  si  ok  on  fait  une  recherche  en  largeur  depuis  pomme  pour  voir  si  toutes  les  cases  sont  atteignables.  si  oui,  on  fait  le  mouvement  vers  pomme.  si  non,  on  regarde  un  autre  plus  court  chemin.  il  en  existera  toujours  un  (mais  on  n'est  pas  sur  de  le  trouver  du  premier  coup)  (recurrence)




#  https://citeseerx.ist.psu.edu/document?repid=rep1  type=pdf  doi=bcc9203a455e521dc9f592805f36346ed336f3f0  ok

#  https://people.dmi.uns.ac.rs/~bodroza/Radovi/match43.pdf  encoder  cycle  ham  avec  alphabet  et  faire  transformation  par  colonne,  matrice  adjacence?

#  https://bpb-us-e2.wpmucdn.com/sites.uci.edu/dist/5/1894/files/2016/12/AutomatedSnakeGameSolvers.pdf  A*  avec  test  propagation  arriere

#  https://www.google.com/url?sa=t  rct=j  q=  esrc=s  source=web  cd=  cad=rja  uact=8  ved=2ahUKEwj-pPiqsIKCAxXAVqQEHfGiDpE4ChAWegQIAxAB  url=https%3A%2F%2Fwww.combinatorics.org%2Fojs%2Findex.php%2Feljc%2Farticle%2Fdownload%2Fv21i4p7%2Fpdf%2F  usg=AOvVaw0fbyrQPtCE-QYIt5I1pKxn  opi=89978449  nombre  de  cycles  ham

#  https://www.hindawi.com/journals/jam/2012/                                                                    475087/  acceptabilité  et  regarder  graphes  hamiltoniens  dans  graphe  grille  lettre

#  https://mathworld.wolfram.com/GridGraph.html  prémice  des  grid  graphs,  il  existe  une  relation  de  recurrence  linéaire  pour  le  nombre  de  cycles  hami  dans  graphe  grille  solide  (n,n)

#  https://github.com/neelgajjar/Snake-game-AI-Solver#readme  oui