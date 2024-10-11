import collections


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