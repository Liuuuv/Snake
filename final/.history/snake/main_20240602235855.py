import  collections
import  pygame  as  py
import  numpy  as  np
import  math
import  random  as  rd
import  copy
import  matplotlib.pyplot  as  plt
import time

from serpent import Serpent
from jeu import Jeu
from pomme import Pomme
from affichage import Affichage
from donnees import Donnees

inf=float('inf')


liste_methodes=['suivre_chemin','raccourcis_croissants_v2','a_etoile_seul','pomme_moins_queue','a_etoile_seulement_si_modif',
                'a_etoile_graphe_oriente','a_etoile_projection_queue','parcours_cellules A COMPLETER',
                'monte_carlo_tree_search NE MARCHE PAS','a_etoile_graphe_oriente_cout','a_etoile_graphe_oriente_hami',
                'arbre_raccourcis_modifier_hami EXPONENTIEL','raccourcis_croissants_v3']

# probleme avec les ratios parties perdues

nb_iterations=1
methode='pomme_moins_queue'
ajouter_donnees=False

nom_fichier='donnees'
liste_noms_fichiers=['donnees','donnees_raccourcis_risque']

execution_rapide=False

fps=30
afficher=True
jeu_actif=True
nb_cases=8

execution_instantanee=False
mode_manuel=True

facteur_resolution=0.5
depart_serpent=[0,0]
titre_fenetre='le serpent qui mange des pommes et grandit'

taux_risque='0'

# donnees.recreer_fichier(liste_methodes)

if nb_cases!=8 and ajouter_donnees:
    print("NB CASES!!!")
    nb_iterations=0

if execution_rapide:
    fps=3000
    afficher=False
    facteur_resolution=0.01
    jeu_actif=True

if execution_instantanee:
    facteur_resolution=0.01

def main():

    heure_debut=time.time()
    liste_pas=[]
    dico_taux_raccourcis={}

    donnees=Donnees()
    donnees.nom_fichier=nom_fichier
    donnees.initialiser()



    for  _  in  range(nb_iterations):
        py.init()

        py.display.set_caption(titre_fenetre)

        jeu=Jeu(Serpent(depart_serpent))

        affichage=Affichage(facteur_resolution,jeu,nb_cases)

        affichage.afficher=afficher
        affichage.jeu_actif=jeu_actif
        affichage.mode_manuel=mode_manuel
        affichage.fps=fps
        affichage.nom_methode=methode
        affichage.numero_essai=_+1
        
        affichage.taux_risque=int(taux_risque)


        if execution_instantanee:
            taux_raccourcis=affichage.algorithme.calculer_taux_raccourcis()
            if taux_raccourcis in dico_taux_raccourcis.keys():
                dico_taux_raccourcis[taux_raccourcis]+=1
            else:
                dico_taux_raccourcis[taux_raccourcis]=1

        else:
            affichage.loop()

            # print(affichage.algorithme.liste_pas)
            
            if nom_fichier=='donnees':
                # plot classique
                if ajouter_donnees and affichage.jeu.etat_partie!=0:    # 0: en cours, 1: gagnée, -1: perdu
                    donnees.ajouter_liste_score(methode,affichage.algorithme.liste_pas,affichage.jeu.etat_partie)
            
            if nom_fichier=='donnees_raccourcis_risque':
                # pour plot en fonction du risque
                if ajouter_donnees:
                    if not donnees.existence_feuille(taux_risque):
                        donnees.creer_feuille(taux_risque)
                        donnees.initialiser_feuille(taux_risque)
                if ajouter_donnees and affichage.jeu.etat_partie!=0:    # 0: en cours, 1: gagnée, -1: perdu
                    donnees.ajouter_liste_score(taux_risque,affichage.algorithme.liste_pas,affichage.jeu.etat_partie)
        

        py.quit()


        del  jeu
        del  affichage
    
    donnees.fichier.close()
    
    if execution_instantanee:
        # print(dico_taux_raccourcis)
        
        liste_x=dico_taux_raccourcis.keys()
        liste_y=dico_taux_raccourcis.values()

        print(list(liste_x))
        print(list(liste_y))

        plt.scatter(liste_x,liste_y,color='black',marker='+')
        plt.show()
    
    heure_fin=time.time()
    print('temps d\'execution:',heure_fin-heure_debut)
    
    # liste_score=np.arange(len(min(liste_pas,key=len)))
    # liste_pas_moyen=[np.mean(sub_list) for sub_list in zip(*liste_pas)]


    # plt.plot(liste_score,liste_pas_moyen,color='black')
    # plt.show()



if __name__=='__main__':
    main()
    print()



#  print("FINAL",np.mean(liste_pas))


"""autre"""
#  peut  on  avoir  tous  les  cycles  hamiltoniens  via  la  methode  des  murs?  NON  VRAIMENT  PAS  DU  TOUT
#  position  de  securité=avoir  un  plus  court  chemin  jusqu'à  bout  de  la  queue?  NON CAR ON PEUT MOURIR SI ON SUIT LA QUEUE SI LA POMME APPARAIT TOUJOURS DEVANT NOUS (ET IL NE FAUT PAS SE LIMITER QU'A UN CHEMIN CAR ON PEUT BOUCLER)
#  il  faut  compter  le  nombre  de  cycles  hami  BIBLIO  OK

"""idées  randoms"""
#  faire  que  s'il  y  a  deux  plus  courts  chemins:  prend  le  meilleur
#  regarder  tout  les  chemins  possibles  et  y  mettre  un  score?
#  encodage:  mettre  un  poids  sur  chaque  element  de  la  queue  pour  designer  le  nombre  de  pas  necessaires  avant  que  la  place  soit  libre:  peut  servir  de  faire  un  "floodfill"  pour  avoir  une  carte  de  dans  combien  de  pas  telle  case  sera  disponible
#  pour  trouver  un  cycle  plus  long  chemin  (presque)  avec  condition  on  peut:  faire  plus  court  chemin  de  tete  jusqu'a  queue  sans  passer  par  queue  puis  etendre  le  chemin  un  maximum  depuis  la  tete  (via  deque  (file))
#  changer  matrice  adjacence  en  fonction  de  pos  du  serpent  (actualiser  a  chaque  pas)  comme  ça  on  s'en  fiche  des  conditions  pour  trouver  un  cycle  hami  qui  passe  sur  le  corps.  On  a  juste  a  retirer  des  aretes  du  graphe



""" ameliorer"""
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
# faire de la reconfiguration de cycles hamis pour canoniser un max le cycle hami dans A* seulement si modif, traiter les cas impossibles?
# modifier le A* de A* seulement si modif
# faire que les courbes affichent les ecarts types


"""methodes"""
#  A*  idées:  faire  un  A*  naif  qui  ne  coupe  pas  le  plateau  en  deux,  si  la  pomme  est  trop  proche  le  serpent  l'evite
#  partir  d'un  chemin  zigzag  et  faire  du  A*  (à  modifier)  avec  modif,  une  fois  la  pomme  mangee  et  queue  pas  trop  la,  remettre  chemin  zigzag  (ou  le  passer  en  vertical  (resp.  horizontal)
#  raccourcis  croissants  n'ont  pas  tant  besoin  de  marge,  si  on  ne  fait  que  manger  des  pommes,  on  sera  collé  a  notre  queue  et  la  pomme  apparaitra  ailleurs NON DU COUP
#  faire  un  A*  et  a  chaque  instant  regarder  s'il  existe  un  cycle  hamiltonien  passant  par  la  queue  du  serpent COUTEUX MAIS FAISABLE PAR BELLMAN KASP JE SUPPOSE?
#  faire  un  A*  naif  tq  tjrs  avoir  une  sécurité,  si  on  va  la  briser  on  passe  sur  un  graphe  hamiltonien  qui  satisfasse  les  conditions  ON  POURRA  TOUJOURS??
#  on  peut  faire  un  A*  naif  et  verifier  pour  chaque  chemin  si  depuis  la  pomme  on  peut  parcourir  une  distance  de  la  taille  de  la  queue+1 INUTILE, AVOIR CHEMIN JUSQU'A QUEUE EN PRENANT EN COMPTE DEPLACEMENT SUFFIT NON??
#  au  lieu  de  prendre  la  marge  avant,  on  peut  eviter  la  ou  on  sera:  A*  sur  pomme  sans  modif  en  evitant  futures  positions  (mais  probleme  si  pomme  arrive  dans  suite  du  chemin,  on  peut  alors  regarder  chemin  vers  bout  queue?)
# faire qu'on regarde tous les plus courts chemins et on en prend un qui nous permet d'avoir une sécurité
# faire qu'on prend des raccourcis en prenant de moins en moins de marge

# mélange de modifier le cycle en temps réel et prendre des raccourcis:
# on fait un arbre de toutes les possibilités pour atteindre la pomme selon les plus courts chemins (voires quasi-plus courts chemins), seules sont autorisées celles qui prennent un raccourci sur le cycle ou celle qui changent de cycle
# il faut alors changer les fonctions faisant les méthodes, et les faire prendre en argument une configuration d'une partie



# on peut faire un reseau de neuronnes et au fil des parties, on repere les chemins qui marchent le mieux et le monte carlo devient de moins en moins probabiliste

#  on  fait  A*  de  tete  a  pomme,  si  ok  on  A*  de  pomme  a  bout  de  queue  (celui  qui  sera  lorsqu'on  mange  pomme),  si  ok  on  fait  une  recherche  en  largeur  depuis  pomme  pour  voir  si  toutes  les  cases  sont  atteignables.  si  oui,  on  fait  le  mouvement  vers  pomme.  si  non,  on  regarde  un  autre  plus  court  chemin.  il  en  existera  toujours  un  (mais  on  n'est  pas  sur  de  le  trouver  du  premier  coup)  (recurrence)

# amélioration de A* avec projection queue : faire que le A* retour soit un plus long chemin (sous optimal)



#  https://citeseerx.ist.psu.edu/document?repid=rep1  type=pdf  doi=bcc9203a455e521dc9f592805f36346ed336f3f0  ok

#  https://people.dmi.uns.ac.rs/~bodroza/Radovi/match43.pdf  encoder  cycle  ham  avec  alphabet  et  faire  transformation  par  colonne,  matrice  adjacence?

#  https://bpb-us-e2.wpmucdn.com/sites.uci.edu/dist/5/1894/files/2016/12/AutomatedSnakeGameSolvers.pdf  A*  avec  test  propagation  arriere

#  https://www.google.com/url?sa=t  rct=j  q=  esrc=s  source=web  cd=  cad=rja  uact=8  ved=2ahUKEwj-pPiqsIKCAxXAVqQEHfGiDpE4ChAWegQIAxAB  url=https%3A%2F%2Fwww.combinatorics.org%2Fojs%2Findex.php%2Feljc%2Farticle%2Fdownload%2Fv21i4p7%2Fpdf%2F  usg=AOvVaw0fbyrQPtCE-QYIt5I1pKxn  opi=89978449  nombre  de  cycles  ham

#  https://www.hindawi.com/journals/jam/2012/                                                                    475087/  acceptabilité  et  regarder  graphes  hamiltoniens  dans  graphe  grille  lettre

#  https://mathworld.wolfram.com/GridGraph.html  prémice  des  grid  graphs,  il  existe  une  relation  de  recurrence  linéaire  pour  le  nombre  de  cycles  hami  dans  graphe  grille  solide  (n,n)

#  https://github.com/neelgajjar/Snake-game-AI-Solver#readme  oui