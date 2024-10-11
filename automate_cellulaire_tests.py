import pygame as py
import math
import numpy as np

py.init()
py.display.set_caption("automate cellulaire")



blanc=(255,255,255)
noir=(0,0,0)


class Affichage:
    def __init__(self,facteur):
        self.dimensions=(int(1920*facteur),int(1080*facteur))
        self.fenetre=py.display.set_mode(self.dimensions)

        self.grille=np.array([
        [1,1,1,1,1],
        [1,-1,-1,-1,1],
        [1,-1,-1,-1,1],
        [1,-1,1,-1,1],
        [1,-1,1,-1,1] 
        ])

        self.nb_cases=len(self.grille)     # grille carré

        self.taille_grille=200
        self.taille_case=self.taille_grille/self.nb_cases

        self.dico_cases=self.initialiser_dico_cases()

    def initialiser_dico_cases(self):
        dico_cases={}
        for j in range(self.nb_cases):
            for i in range(self.nb_cases):
                UL=(j*self.taille_case,i*self.taille_case)
                UR=((j+1)*self.taille_case,i*self.taille_case)
                DR=((j+1)*self.taille_case,(i+1)*self.taille_case)
                DL=(j*self.taille_case,(i+1)*self.taille_case)
                # print([UL,UR,DR,DL])
                dico_cases[(j,i)]=[UL,UR,DR,DL]
                print(UL)
        return dico_cases

    def instant_suivant(self):
        grille_bis=self.grille[:]
        for i in range(self.nb_cases-1):
            for j in range(self.nb_cases-1):
                voisinage=np.array([
                [self.grille[i,j],self.grille[i,j+1]],
                [self.grille[i+1,j],self.grille[i+1,j+1]]
                ])

                if (voisinage[:,:]==[[-1,-1],[-1,-1]]).all() or (voisinage[:,:]==[[1,1],[1,1]]).all():
                    grille_bis[i:i+2,j:j+2]=1
        grille=grille_bis[:]
        # np.product(voisinage)==-1 or

    def dessiner_grille(self):
        for j in range(self.nb_cases):
            for i in range(self.nb_cases):
                UL,UR,DR,DL=self.dico_cases[(i,j)]
                print(UL)
                if self.grille[j,i]==1:
                    py.draw.polygon(self.fenetre,noir,[UL,UR,DR,DL])
                else:
                    py.draw.polygon(self.fenetre,(255,0,0),[UL,UR,DR,DL])

    def loop(self):
        horloge=py.time.Clock()


        # boucle de jeu
        continuer=True
        while continuer:
            for event in py.event.get():
                if event.type==py.QUIT:
                    continuer=False
                if event.type==py.KEYDOWN:
                    if event.key==py.K_ESCAPE:
                        continuer=False
            horloge.tick(2)
            py.display.set_caption(str(round(horloge.get_fps(),1)))
            print(self.grille)


            self.fenetre.fill(blanc)
            self.dessiner_grille()
            self.instant_suivant()
            # print(self.grille)




            # ici

            py.display.flip()

        py.quit()


facteur=0.5
affichage=Affichage(facteur)
affichage.loop()