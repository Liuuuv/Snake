# 2 lignes, 3 colonnes, 3>=2
taille_grille=[7,3]

"""blanc: pair, noir: impair"""


debut=[2,0]
fin=[3,2]

assert 0<=debut[0]<=taille_grille[0]
assert 0<=debut[1]<=taille_grille[1]

# longueur=max(taille_grille[0],taille_grille[1])
# largeur=min(taille_grille[0],taille_grille[1])

# plus_petit_cote=min(longueur,largeur)


def pos_grille(pos,UL_grille,DR_grille):
    assert UL_grille[0]<=pos[0]<=DR_grille[0]
    assert UL_grille[1]<=pos[1]<=DR_grille[1]

    return [pos[0]-UL_grille[0],pos[1]-UL_grille[1]]


def  voisins(pos,UL_grille,DR_grille):
    liste_voisins=[]
    for  j  in  range(-1,2):
        for  i  in  range(-1,2):
            if  i*j==0 and UL_grille[0]<=pos[0]+j<=DR_grille[0]  and  UL_grille[1]<=pos[1]+i<=DR_grille[1] and (i,j)!=(0,0):
                #  print(i,j)
                liste_voisins.append([pos[0]+j,pos[1]+i])
    return liste_voisins

def nombre_parite(pos,UL_grille,DR_grille):
    x=pos[0]-UL_grille[0]
    y=pos[1]-UL_grille[1]
    return (x+y)%2


def conditions_realisees(UL_grille,DR_grille,debut,fin):

    taille_grille=(DR_grille[0]-UL_grille[0],DR_grille[1]-UL_grille[1])
    plus_petit_cote=min(taille_grille[0],taille_grille[1])

    # print(taille_grille)

    if taille_grille[0]>0 and taille_grille[1]>0:
        # color compatible
        if (taille_grille[0]+1)*(taille_grille[1]+1)%2==0:
            # taille paire, doivent etre de couleurs differentes
            if nombre_parite(debut,UL_grille,DR_grille)==nombre_parite(fin,UL_grille,DR_grille):
                return False
        else:
            # taille impaire, doivent etre blancs
            if nombre_parite(debut,UL_grille,DR_grille)==1 or nombre_parite(fin,UL_grille,DR_grille):
                return False

    # F1
    if plus_petit_cote==0:
        if debut[0]!=0 or fin[0]!=DR_grille[0]:
            return False

    # F2
    elif plus_petit_cote==1:

        # si debut, fin forment une arete
        if abs(fin[0]-debut[0])+abs(fin[1]-debut[1])==1:

            if debut[0]==fin[0]:
                if debut[0]!=UL_grille[0] and debut[0]!=DR_grille[0]:
                    return False

            if debut[1]==fin[1]:
                if debut[1]!=UL_grille[1] and debut[1]!=DR_grille[1]:
                    return False

    # F3
    elif plus_petit_cote==2:    # faux non? on doit regarder l'autre coté, par taille_grille[0]
        if (taille_grille[0]+1)%2==0 and (debut[0]+debut[1])%2==1 and (fin[0]+fin[1])%2==0:
            if debut[1]==1:
                if debut[0]<fin[0]:
                    return False
            else:
                if debut[0]<fin[0]-1:
                    return False

    return True



def strip(UL_grille,DR_grille,debut,fin): # faire qu'on essaie tous les cas

    taille_grille=(DR_grille[0]-UL_grille[0],DR_grille[1]-UL_grille[1])

    S=[]
    max_x=max(debut[0],fin[0])
    max_y=max(debut[1],fin[1])
    min_x=min(debut[0],fin[0])
    min_y=min(debut[1],fin[1])

    indice_separation=[0,0]
    direction_cycle=None
    cote_a_conserver=None

    # strip horizontale en bas
    if max_y<=DR_grille[1]-2:
        if (taille_grille[1]-max_y)*(taille_grille[0]+1)%2==0:
            print("i_strip=",max_y)
            i_strip=max_y
        elif max_y<=taille_grille[1]-3:
            if (taille_grille[1]-max_y-1)*(taille_grille[0]+1)%2==0:
                print("i_strip=",max_y-1)
                i_strip=max_y-1


        if (taille_grille[1]-i_strip)%2==0:     # parite ok verticalement
            direction_cycle="gauche" # ou droite
            S=cycle_hamiltonien(UL_grille,DR_grille,[0,i_strip+1],DR_grille,direction_cycle)
            indice_separation[1]=i_strip

        elif (taille_grille[0]+1)%2==0:     # parite ok horizontalement
            direction_cycle="bas"
            S=cycle_hamiltonien(UL_grille,DR_grille,[0,i_strip+1],DR_grille,direction_cycle)
            indice_separation[1]=i_strip

        if S!=[]:
            cote_a_conserver="haut"


    # strip verticale à droite
    elif max_x<=taille_grille[0]-2:
        if (taille_grille[0]-max_x)*(taille_grille[1]+1)%2==0:
            print("j_strip=",max_x)
            j_strip=max_x
        elif max_x<=taille_grille[0]-3:
            if (taille_grille[0]-max_x+1)*(taille_grille[1]+1)%2==0:
                print("j_strip=",max_x+1)
                j_strip=max_x+1


        if (taille_grille[0]-j_strip)%2==0:     # parite ok horizontalement
            direction_cycle="haut"
            S=cycle_hamiltonien(UL_grille,DR_grille,[j_strip+1,0],DR_grille,direction_cycle)
            indice_separation[0]=j_strip

        if (taille_grille[1]+1)%2==0:     # parite ok verticalement
            direction_cycle="droite" # ou bas
            S=cycle_hamiltonien(UL_grille,DR_grille,[j_strip+1,0],DR_grille,direction_cycle)
            indice_separation[0]=j_strip

        if S!=[]:
            cote_a_conserver="gauche"


    # strip verticale à gauche
    elif UL_grille[0]+2<=min_x:
        if (min_x)*(taille_grille[1]+1)%2==0:
            print("j_strip=",min_x)
            j_strip=min_x
        elif 3<=min_x:
            if (min_x-1)*(taille_grille[1]+1)%2==0:
                print("j_strip=",min_x-1)
                j_strip=min_x-1

        if j_strip%2==0:  # parite ok horizontalement
            direction_cycle="haut" # ou bas
            S=cycle_hamiltonien(UL_grille,DR_grille,UL_grille,[j_strip-1,DR_grille[1]],direction_cycle)
            indice_separation[0]=j_strip

        if (taille_grille[1]+1)%2==0:   # parite ok verticalement
            direction_cycle="haut"
            S=cycle_hamiltonien(UL_grille,DR_grille,UL_grille,[j_strip-1,DR_grille[1]],direction_cycle)
            indice_separation[0]=j_strip

        if S!=[]:
            cote_a_conserver="droite"



    # strip horizontale en haut
    elif UL_grille[1]+2<=min_y:
        if (min_y)*(taille_grille[0]+1)%2==0:
            print("i_strip=",min_y)
            i_strip=min_y
        elif 3<=min_y:
            if (min_y-1)*(taille_grille[0]+1)%2==0:
                print("i_strip=",min_y-1)
                i_strip=min_y-1

        if i_strip%2==0:    # parite ok verticalement
            direction_cycle="gauche" # ou droite
            S=cycle_hamiltonien(UL_grille,DR_grille,UL_grille,[DR_grille[0],i_strip-1],direction_cycle)
            indice_separation[1]=i_strip

        if (taille_grille[0]+1)%2==0:   # parite ok horizontalement
            direction_cycle="haut"
            S=cycle_hamiltonien(UL_grille,DR_grille,UL_grille,[DR_grille[0],i_strip-1],direction_cycle)
            indice_separation[1]=i_strip

        if S!=[]:
            cote_a_conserver="bas"

    return S,indice_separation,direction_cycle,cote_a_conserver

def cycle_hamiltonien(UL_grille,DR_grille,UL,DR,direction_cycle): # UL_grille,DR_grille inutiles

    cycle=[]

    pos=UL[:]
    # print('ICI',UL)


    taille_sous_grille=[DR[0]-UL[0],DR[1]-UL[1]]




    if taille_sous_grille[0]==1 or taille_sous_grille[1]==1:
        direction=[0,1]
        for _ in range((taille_sous_grille[0]+1)*(taille_sous_grille[1]+1)):
            if direction==[0,1]:
                if pos[1]==DR[1]:
                    direction=[1,0]
            elif direction==[1,0]:
                if pos[0]==DR[0]:
                    direction=[0,-1]
            elif direction==[0,-1]:
                if pos[1]==UL[1]:
                    direction=[-1,0]

            cycle.append(pos[:])

            pos[0]+=direction[0]
            pos[1]+=direction[1]


    if direction_cycle=="bas" and cycle==[]:
        direction=[0,1]
        for _ in range((taille_sous_grille[0]+1)*(taille_sous_grille[1]+1)):
            if direction==[0,1]:
                if pos[1]==DR[1]:
                    direction=[1,0]
            elif direction==[1,0]:
                if pos[1]==DR[1]:
                    direction=[0,-1]
                elif pos[1]==UL[1]+1:
                    direction=[0,1]
            elif direction==[0,-1]:
                if pos[0]==DR[0] and pos[1]==UL[1]:
                    direction=[-1,0]
                elif pos[0]!=DR[0] and pos[1]==UL[1]+1:
                    direction=[1,0]

            cycle.append(pos[:])

            pos[0]+=direction[0]
            pos[1]+=direction[1]


    elif direction_cycle=="haut" and cycle==[]:
        print("ICI",UL,DR,direction_cycle)

        pos=DR[:]
        direction=[0,-1]
        for _ in range((taille_sous_grille[0]+1)*(taille_sous_grille[1]+1)):

            if direction==[0,-1]:
                if pos[1]==UL[1]:
                    direction=[-1,0]

            elif direction==[-1,0]:
                if pos[1]==UL[1]:
                    direction=[0,1]
                elif pos[1]==DR[1]-1:
                    direction=[0,-1]

            elif direction==[0,1]:
                if pos[1]==DR[1]-1 and pos[0]!=UL[0]:
                    direction=[-1,0]
                elif pos[1]==DR[1]:
                    direction=[1,0]


            cycle.append(pos[:])

            pos[0]+=direction[0]
            pos[1]+=direction[1]

    elif direction_cycle=="droite" and cycle==[]:
        pos=UL[:]
        direction=[0,1]
        for _ in range((taille_sous_grille[0]+1)*(taille_sous_grille[1]+1)):

            if direction==[0,1]:
                if pos[1]==DR[1]:
                    direction=[1,0]

            elif direction==[1,0]:
                if pos[0]==DR[0]:
                    direction=[0,-1]

            elif direction==[0,-1]:
                if pos[0]==DR[0]:
                    direction=[-1,0]
                elif pos[0]==UL[0]+1:
                    direction=[1,0]

            elif direction==[-1,0]:
                if pos[0]==UL[0]+1 and pos[1]!=UL[1]:
                    direction=[0,-1]



            cycle.append(pos[:])

            pos[0]+=direction[0]
            pos[1]+=direction[1]

    elif direction_cycle=="gauche" and cycle==[]:
        pos=DR[:]
        direction=[0,-1]
        for _ in range((taille_sous_grille[0]+1)*(taille_sous_grille[1]+1)):

            if direction==[0,-1]:
                if pos[1]==UL[1]:
                    direction=[-1,0]

            elif direction==[-1,0]:
                if pos[0]==UL[0]:
                    direction=[0,1]

            elif direction==[0,1]:
                if pos[0]==UL[0]:
                    direction=[1,0]
                elif pos[0]==DR[0]-1:
                    direction=[-1,0]

            elif direction==[1,0]:
                if pos[0]==DR[0]-1:
                    direction=[0,1]



            cycle.append(pos[:])

            pos[0]+=direction[0]
            pos[1]+=direction[1]

    return cycle

def souder_strip_chemin(UL_grille,DR_grille,S,separation,cote_a_conserver,P,debut,fin):

    print('souder P:',P)
    print('souder S',S)
    # print('separation',separation)


    """avoir pos de transition de P"""
    # cas separation horizontale
    if separation[0]!=0:
        for i in range(len(P)-1):
            if P[i][0]==separation[0] and P[i+1][0]==separation[0]:
                i_transition_P=i
                break

    # cas separation verticale
    elif separation[1]!=0:
        for i in range(len(P)-1):
            if P[i][1]==separation[1] and P[i+1][1]==separation[1]:
                i_transition_P=i
                break

    elif separation==[0,0]:
        if cote_a_conserver in ["droite","gauche"]:
            for i in range(len(P)-1):
                print(i)
                if P[i][0]==separation[0] and P[i+1][0]==separation[0]:
                    i_transition_P=i
                    break
        elif cote_a_conserver in ["haut","bas"]:
            for i in range(len(P)-1):
                if P[i][1]==separation[1] and P[i+1][1]==separation[1]:
                    i_transition_P=i
                    break



    chemin=P[:(i_transition_P+1)]

    # avoir voisin de pos de transition de P
    liste_voisin_transition_S=voisins(P[i_transition_P],UL_grille,DR_grille)
    # print(P[i_transition_P],UL_grille,DR_grille)
    # print('voisins transition',liste_voisin_transition_S)

    for i in range(len(S)):
        if S[i] in liste_voisin_transition_S:   # unique
            i_debut=i
            break

    if not P[i_transition_P+1] in voisins(S[i_debut-1],UL_grille,DR_grille):
        S.reverse()

        for i in range(len(S)):
            if S[i] in liste_voisin_transition_S:   # unique
                i_debut=i
                break

    for i in range(len(S)):
        chemin.append(S[(i_debut+i)%len(S)])

    chemin+=P[(i_transition_P+1):]

    return chemin

def chemin_premier(UL_grille,DR_grille,debut,fin): # on passe dans referentiel [0,0] avant d'en sortir

    # print("debut",debut)

    debut_0=[debut[0]-UL_grille[0],debut[1]-UL_grille[1]]
    fin_0=[fin[0]-UL_grille[0],fin[1]-UL_grille[1]]

    print(debut_0,fin_0)

    taille_grille=(DR_grille[0]-UL_grille[0],DR_grille[1]-UL_grille[1])
    chemin=[]

    # cas ou la grille est en (3,3)
    if taille_grille==(2,2):

        # distance gauche-droite 2
        if abs(fin[0]-debut[0])==2:

            # opposés diamétrales, CAS 2

            if abs(fin[1]-debut[1])==2:
                chemin=cas_2(UL_grille,DR_grille,debut_0,fin_0)


            # distance haut-bas 0, CAS 1, on va a droite ou gauche
            elif abs(fin[1]-debut[1])==0:
                chemin=cas_1_hor(UL_grille,DR_grille,debut_0,fin_0)


        elif abs(fin[0]-debut[0])==0:

            # distance haut-bas 0, CAS 1, on va en haut ou bas
            if abs(fin[1]-debut[1])==2:
                chemin=cas_1_ver(UL_grille,DR_grille,debut_0,fin_0)

        # cas 3
        elif abs(fin[0]-debut[0])==1 and abs(fin[1]-debut[1])==1:

            chemin=cas_3(UL_grille,DR_grille,debut_0,fin_0)

    elif taille_grille==(2,1):

        # cas 4
        if debut[0]==fin[0]:

            chemin=cas_4_2_1(UL_grille,DR_grille,debut_0,fin_0)

        # cas 5
        elif abs(debut[0]-fin[0])+abs(debut[1]+fin[1])==1:

            chemin=cas_5_2_1(UL_grille,DR_grille,debut_0,fin_0)

        # cas 6
        else:
            chemin=cas_6_2_1(UL_grille,DR_grille,debut_0,fin_0)

    elif taille_grille==(1,2):

        # cas 4
        if debut[1]==fin[1]:

            chemin=cas_4_1_2(UL_grille,DR_grille,debut_0,fin_0)

        # cas 5
        elif abs(debut[0]-fin[0])+abs(debut[1]+fin[1])==1:

            chemin=cas_5_1_2(UL_grille,DR_grille,debut_0,fin_0)

        # cas 6
        else:
            chemin=cas_6_1_2(UL_grille,DR_grille,debut_0,fin_0)

    print('CHEMIN',chemin)

    for i in range(len(chemin)):
        chemin[i][0]+=UL_grille[0]
        chemin[i][1]+=UL_grille[1]

    if taille_grille==(1,1):

        if debut_0==[0,0]:

            if fin_0==[0,1]:
                chemin=[debut,[debut[0]+1,debut[1]],[debut[0]+1,debut[1]+1],fin]

            elif fin_0==[1,0]:
                chemin=[debut,[debut[0],debut[1]+1],[debut[0]+1,debut[1]+1],fin]

        elif debut_0==[1,1]:

            if fin_0==[0,1]:
                chemin=[debut,[debut[0],debut[1]-1],[debut[0]-1,debut[1]-1],fin]

            elif fin_0==[1,0]:
                chemin=[debut,[debut[0]-1,debut[1]],[debut[0]-1,debut[1]-1],fin]


    if taille_grille[0]==0:
        chemin=[[debut[0],debut[1]+i] for i in range(taille_grille[1])]+[fin]

    if taille_grille[1]==0:
        chemin=[[debut[0]+i,debut[1]] for i in range(taille_grille[0])]+[fin]


    if chemin==[]:
        chemin=chemin_premier(UL_grille,DR_grille,fin,debut)
        print("reverse")
        chemin.reverse()

    return chemin


def split(UL_grille,DR_grille,debut,fin):     # A FINIR

    p,q=[],[]
    separation=[]



    # ON REGARDE TOUT MEME SI ON A DEJA TROUVÉ, corriger ça


    # parcours
    for j in range(UL_grille[0],DR_grille[0]+1):
        for i in range(UL_grille[1],DR_grille[1]+1):



            # eviter d'etre sur debut/fin
            if [j,i] in [debut,fin]:
                continue

            # verifier separation verticale
            if min(debut[0],fin[0])<=j<max(debut[0],fin[0]):


                if debut[0]<fin[0]:

                    if conditions_realisees(UL_grille,[j,DR_grille[1]],debut,[j,i]) and conditions_realisees([j+1,UL_grille[1]],DR_grille,[j+1,i],fin):
                        print("separation ver",j,(j,i))

                        p=[j,i]
                        q=[j+1,i]
                        separation=[j,0]

                elif debut[0]>fin[0]:

                    if conditions_realisees(UL_grille,[j,DR_grille[1]],fin,[j,i]) and conditions_realisees([j+1,UL_grille[1]],DR_grille,[j+1,i],debut):
                        print("separation ver",j,(j,i))

                        p=[j,i]
                        q=[j+1,i]
                        separation=[j,0]


            # verifier separation horizontale
            if min(debut[1],fin[1])<=i<max(debut[1],fin[1]):



                if debut[1]<fin[1]:
                    print('i',(j,i),UL_grille,[DR_grille[0],i],debut,[j,i])
                    print('i',(j,i),[UL_grille[0],j+1],DR_grille,[j,i+1],fin)

                    if conditions_realisees(UL_grille,[DR_grille[0],i],debut,[j,i]) and conditions_realisees([UL_grille[0],i+1],DR_grille,[j,i+1],fin):
                        print("separation hor",i,(j,i))

                        p=[j,i]
                        q=[j,i+1]
                        separation=[0,i]

                elif debut[1]>fin[1]:

                    if conditions_realisees(UL_grille,[DR_grille[0],i],fin,[j,i]) and conditions_realisees([UL_grille[0],j+1],DR_grille,[j,i+1],debut):
                        print("separation hor",i,(j,i))

                        p=[j,i]
                        q=[j,i+1]
                        separation=[0,i]

    return p,q,separation


def cas_2(UL_grille,DR_grille,debut,fin):
    chemin=[]

    if debut==[0,0]:
        chemin=[[0,0],[0,1],[0,2],[1,2],[1,1],[1,0],[2,0],[2,1],[2,2]]

    elif debut==[2,0]:
        chemin=[[2,0],[2,1],[2,2],[1,2],[1,1],[1,0],[0,0],[0,1],[0,2]]

    return chemin

def cas_1_hor(UL_grille,DR_grille,debut,fin):
    print("cas_1_hor")
    chemin=[]


    if debut==[0,0]:
        chemin=[[0,0],[0,1],[0,2],[1,2],[2,2],[2,1],[1,1],[1,0],[2,0]]

    if debut==[0,2]:
        chemin=[[0,2],[0,1],[0,0],[1,0],[2,0],[2,1],[1,1],[1,2],[2,2]]

    return chemin

def cas_1_ver(UL_grille,DR_grille,debut,fin):
    print("cas_1_ver")
    chemin=[]

    if debut==[0,0]:
        chemin=[[0,0],[0,1],[1,1],[1,0],[2,0],[2,1],[2,2],[1,2],[0,2]]


    if debut==[2,0]:
        chemin=[[2,0],[2,1],[1,1],[1,0],[0,0],[0,1],[0,2],[1,2],[2,2]]

    return chemin

def cas_3(UL_grille,DR_grille,debut,fin):
    print("cas_3")
    chemin=[]


    if debut==[0,0]:
        chemin=[[0,0],[1,0],[2,0],[2,1],[2,2],[1,2],[0,2],[0,1],[1,1]]

    if debut==[0,2]:
        chemin=[[0,2],[0,1],[0,0],[1,0],[2,0],[2,1],[2,2],[1,2],[1,1]]

    if debut==[2,0]:
        chemin=[[2,0],[2,1],[2,2],[1,2],[0,2],[0,1],[0,0],[1,0],[1,1]]

    if debut==[2,2]:
        chemin=[[2,2],[1,2],[0,2],[0,1],[0,0],[1,0],[2,0],[2,1],[1,1]]

    return chemin

def cas_4_2_1(UL_grille,DR_grille,debut,fin):
    print("cas_4_2_1")
    chemin=[]


    if debut==[0,0]:
        chemin=[[0,0],[0,1],[0,2],[1,2],[1,1],[0,1]]

    if debut==[2,0]:
        chemin=[[2,0],[1,0],[0,0],[0,1],[1,1],[2,1]]

    return chemin

def cas_5_2_1(UL_grille,DR_grille,debut,fin):
    print("cas_5_2_1")
    chemin=[]


    if debut==[0,0]:
        chemin=[[0,0],[0,1],[1,1],[2,1],[2,0],[1,0]]

    if debut==[0,1]:
        chemin==[[0,1],[0,0],[1,0],[2,0],[2,1],[1,1]]

    if debut==[2,0]:
        chemin=[[2,0],[2,1],[1,1],[0,1],[0,0],[1,0]]

    if debut==[2,1]:
        chemin=[[2,1],[2,0],[1,0],[0,0],[0,1],[1,1]]

    return chemin

def cas_6_2_1(UL_grille,DR_grille,debut,fin):
    print("cas_6_2_1")
    chemin=[]

    # if debut==[0,0]:
    #     chemin=[debut,[debut[0],debut[1]+1],[debut[0]+1,debut[1]+1],[debut[0]+1,debut[1]],[debut[0]+2,debut[1]],fin]
    #
    # elif debut==[0,1]:
    #     chemin=[debut,[debut[0],debut[1]-1],[debut[0]+1,debut[1]-1],[debut[0]+1,debut[1]],[debut[0]+2,debut[1]],fin]

    if debut==[0,0]:
        chemin=[[0,0],[0,1],[1,1],[1,0],[2,0],[2,1]]

    if debut==[0,1]:
        chemin=[[0,1],[0,0],[1,0],[1,1],[2,1],[2,0]]

    if debut==[2,0]:
        chemin=[[2,0],[2,1],[1,1],[1,0],[0,0],[0,1]]

    if debut==[2,1]:
        chemin=[[2,1],[2,0],[1,0],[1,1],[0,1],[0,0]]

    return chemin


def cas_4_1_2(UL_grille,DR_grille,debut,fin):
    print("cas_4_1_2")
    chemin=[]


    if debut==[0,0]:
        chemin=[[0,0],[0,1],[0,2],[1,2],[1,1],[1,0]]

    if debut==[0,2]:
        chemin=[[0,2],[0,1],[0,0],[1,0],[1,1],[1,2]]

    return chemin

def cas_5_1_2(UL_grille,DR_grille,debut,fin):
    print("cas_5_1_2")
    chemin=[]


    if debut==[0,0]:
        chemin=[[0,0],[1,0],[1,1],[1,2],[0,2],[0,1]]

    if debut==[1,0]:
        chemin=[[1,0],[0,0],[0,1],[0,2],[1,2],[1,1]]

    if debut==[0,2]:
        chemin=[[0,2],[1,2],[1,1],[1,0],[0,0],[0,1]]

    if debut==[1,2]:
        chemin=[[1,2],[0,2],[0,1],[0,0],[1,0],[1,1]]

    return chemin

def cas_6_1_2(UL_grille,DR_grille,debut,fin):
    print("cas_6_1_2")
    chemin=[]


    if debut==[0,0]:
        chemin=[[0,0],[1,0],[1,1],[0,1],[0,2],[1,2]]

    if debut==[1,0]:
        chemin=[[1,0],[0,0],[0,1],[1,1],[1,2],[0,2]]

    if debut==[0,2]:
        chemin=[[2,0],[2,1],[1,1],[1,0],[0,0],[0,1]]

    if debut==[1,2]:
        chemin=[[2,1],[2,0],[1,0],[1,1],[0,1],[0,0]]

    return chemin

def plus_long_chemin(UL_grille,DR_grille,debut,fin):



    print("plus long chemin",UL_grille,DR_grille,debut,fin)

    taille_grille=(DR_grille[0]-UL_grille[0],DR_grille[1]-UL_grille[1])
    plus_petit_cote=min(taille_grille[0],taille_grille[1])

    if not conditions_realisees(UL_grille,DR_grille,debut,fin):

        print("pas de chemin Hamiltonien")
        return "pas de chemin Hamiltonien"


    # si c'est un 1 ou 2 rectangle
    if taille_grille in [(2,2),(2,1),(1,2),(1,1)]:
        print("chemin premier, (2,2),(1,2),(1,1)",UL_grille,DR_grille,debut,fin)
        return chemin_premier(UL_grille,DR_grille,debut,fin)

    else:
        # if peut_etre_stripped():
        S,separation,direction_cycle,cote_a_conserver=strip(UL_grille,DR_grille,debut,fin)

        if S!=[]:
            print(S)
            print(cote_a_conserver)

            if separation[0]!=0:
                if cote_a_conserver=="droite":
                    P=plus_long_chemin([separation[0],UL_grille[1]],DR_grille,debut,fin)

                elif cote_a_conserver=="gauche":
                    P=plus_long_chemin(UL_grille,[separation[0],DR_grille[1]],debut,fin)

            elif separation[1]!=0:
                if cote_a_conserver=="haut":
                    P=plus_long_chemin(UL_grille,[DR_grille[0],separation[1]],debut,fin)
                elif cote_a_conserver=="bas":
                    P=plus_long_chemin([UL_grille[0],separation[1]],DR_grille,debut,fin)

            elif separation==[0,0]:
                if cote_a_conserver=="droite":
                    P=plus_long_chemin([separation[0],UL_grille[1]],DR_grille,debut,fin)

                elif cote_a_conserver=="gauche":
                    P=plus_long_chemin(UL_grille,[separation[0],DR_grille[1]],debut,fin)

                elif cote_a_conserver=="haut":
                    P=plus_long_chemin(UL_grille,[DR_grille[0],separation[1]],debut,fin)

                elif cote_a_conserver=="bas":
                    P=plus_long_chemin([UL_grille[0],separation[1]],DR_grille,debut,fin)

            print("P:",P)
            # print("OUTPUT",S,separation,cote_a_conserver,P,debut,fin)
            return souder_strip_chemin(UL_grille,DR_grille,S,separation,cote_a_conserver,P,debut,fin)

        else:
            p,q,separation=split(UL_grille,DR_grille,debut,fin)

            if separation!=[]:
                print('peut etre split')

                # separation verticale
                if separation[0]!=0:

                    if debut[0]<fin[0]:
                        P1=plus_long_chemin(UL_grille,[separation[0],DR_grille[1]],debut,p)
                        P2=plus_long_chemin([separation[0]+1,UL_grille[1]],DR_grille,q,fin)

                        return P1+P2

                    elif debut[0]>fin[0]:
                        P1=plus_long_chemin([separation[0]+1,UL_grille[0]],DR_grille,debut,q)
                        P2=plus_long_chemin(UL_grille,[separation[0],DR_grille[1]],p,fin)


                        return P1+P2

                    elif debut[0]==fin[0]:
                        print("PROBLEME,debut[0]==fin[0]")

                # separation horizontale
                if separation[1]!=0:

                    if debut[1]<fin[1]:
                        P1=plus_long_chemin(UL_grille,[DR_grille[0],separation[1]],debut,p)
                        P2=plus_long_chemin([UL_grille[0],separation[1]+1],DR_grille,q,fin)

                        return P1+P2

                    elif debut[1]>fin[1]:
                        P1=plus_long_chemin([UL_grille[0],separation[1]+1],DR_grille,debut,p)
                        P1=plus_long_chemin(UL_grille,[DR_grille[0],separation[1]],q,fin)


                        return P1+P2

                    elif debut[1]==fin[1]:
                        print("PROBLEME,debut[1]==fin[1]")

            else:
                # problème premier
                print("problème premier")
                return chemin_premier(UL_grille,DR_grille,debut,fin)

#print(plus_long_chemin([0,0],taille_grille,debut,fin))
# print(cycle_hamiltonien(0,0,[0,0],[5,3],"gauche"))
# print(conditions_realisees([2, 2], [3, 3], [2, 2], [3, 3]))