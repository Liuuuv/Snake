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