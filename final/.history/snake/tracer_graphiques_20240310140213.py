import matplotlib.pyplot as plt
import numpy as np

import main
import donnees

fichier=donnees.fichier


plt.close()


# couleurs='bgrcmykbgr'



nombre_figures=len(fichier.sheetnames)


# pour avoir des couleurs

# cmap = plt.get_cmap('jet')
cmap=plt.get_cmap('nipy_spectral')
couleurs=[cmap(i) for i in np.linspace(0,1,nombre_figures)]

# courbes individuelles
figure_secondaire,axes_secondaire=plt.subplots(2,nombre_figures)

# courbe commune
figure_primaire,axe_primaire=plt.subplots()

# courbe individuelles 2
figure_secondaire2,axes_secondaire2=plt.subplots(2,nombre_figures)

# courbe commune 2
figure_primaire2,axe_primaire2=plt.subplots()

# courbe commune: defaites
axe_defaites=axe_primaire.twinx()

# sur les courbes individuelles
axe_essais=np.array([axes_secondaire[0,i].twinx() for i in range(nombre_figures)])

# opacite de la courbe du nb d essais
alpha_essais=0.3


for numero_colonne,nom_feuille in enumerate(fichier.sheetnames,start=0):

    # creation des listes
    feuille=fichier[nom_feuille]

    liste_score=[]
    liste_pas_moyen=[]
    liste_essais=[]
    liste_ratio_defaite=[]
    liste_nb_pas_total=[]

    # recuperation des donnees en listes

    # pour tracer score en fonction nb_pas
    compteur_score=0
    
    for i in range(donnees.score_max):
        liste_score.append(feuille['A'+str(i+2)].value)
        liste_pas_moyen.append(feuille['B'+str(i+2)].value)
        liste_essais.append(feuille['C'+str(i+2)].value)
        liste_ratio_defaite.append(feuille['F'+str(i+2)].value)
        

        if liste_nb_pas_total==[]:
            liste_nb_pas_total.append(feuille['B'+str(i+2)].value)
        elif liste_nb_pas_total[-1]!=0:
            liste_nb_pas_total.append(liste_nb_pas_total[-1]+feuille['B'+str(i+2)].value)
    

    
    # nb pas moyen en fonction du score
    axes_secondaire[0,numero_colonne].plot(liste_score,liste_pas_moyen,color=couleurs[numero_colonne])
    axes_secondaire[0,numero_colonne].title.set_text(nom_feuille)

    # nb essais en fonction du score
    axe_essais[numero_colonne].plot(liste_score,liste_essais,color=couleurs[numero_colonne],alpha=alpha_essais)
    axe_essais[numero_colonne].set_ylim(ymin=0)

    # ratio parties perdues en fonctions score
    axes_secondaire[1,numero_colonne].plot(liste_score,liste_ratio_defaite,color=couleurs[numero_colonne],alpha=1) # on peut avoir .bar au lieu de .plot
    axes_secondaire[1,numero_colonne].set_ylim(ymin=0)
    axes_secondaire[1,numero_colonne].title.set_text('ratio de parties perdues')
    
    # plot du nb de pas en fonction du score
    axe_primaire.plot(liste_score,liste_pas_moyen,color=couleurs[numero_colonne],label=nom_feuille)

    # plot du ratio de defaites de chaque courbe
    axe_defaites.plot(liste_score,liste_ratio_defaite,color=couleurs[numero_colonne],alpha=0.6,linewidth=0.8,linestyle='-')
    axe_defaites.set_ylabel('ratio de parties perdues')

    # plot du score en fonction du nb total de pas
    axe_primaire2.plot(liste_nb_pas_total,liste_score,color=couleurs[numero_colonne],label=nom_feuille)
    

    # axe_essais[0].plot(liste_score,liste_essais,color=couleurs[numero_colonne],alpha=alpha_essais)





for i in range(nombre_figures):
    axes_secondaire[0,i].grid()
    axes_secondaire[1,i].grid()

axe_primaire.set_title('nombre de pas en fonction du score')
axe_primaire.set_xlabel('score')
axe_primaire.set_ylabel('nombre de pas')
axe_primaire.grid()
axe_primaire.legend()

axe_primaire2.set_title('score en fonction du nombre de pas total')
axe_primaire2.set_xlabel('nombre de pas total')
axe_primaire2.set_ylabel('score')
axe_primaire2.grid()
axe_primaire2.legend()

# axe_y_essais.tick_params(axis='y',labelcolor='black')
    
# mng = plt.get_current_fig_manager()
# mng.resize(1300,800)

plt.tight_layout()
plt.show()