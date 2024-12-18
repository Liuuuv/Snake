import  collections
import  pygame  as  py
import  numpy  as  np
import  math
import  random  as  rd
import  copy
import  matplotlib.pyplot  as  plt
import chemin_hamiltonien_rectangle as c

from serpent import Serpent
from jeu import Jeu
from pomme import Pomme







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