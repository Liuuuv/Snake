import matplotlib.pyplot as plt
import numpy as np

import main
from donnees import Donnees

nom_fichier='donnees'
liste_noms_fichiers=['donnees','donnees_raccourcis_risque']

donnees=Donnees()
donnees.nom_fichier=nom_fichier
donnees.initialiser()
fichier=donnees.fichier



liste_plots_possibles=['methodes_individuelles','nb_pas','nb_pas_total',
                       '3d_risque']

plot_a_faire='nb_pas'



plt.close()


# couleurs='bgrcmykbgr'

nombre_figures=len(fichier.sheetnames)


# pour avoir des couleurs

# cmap = plt.get_cmap('jet')
cmap=plt.get_cmap('nipy_spectral')
couleurs=[cmap(i) for i in np.linspace(0,1,nombre_figures)]

if 'methodes_individuelles'==plot_a_faire:

    # courbes individuelles
    figure_secondaire,axes_secondaire=plt.subplots(2,nombre_figures)

    # sur les courbes individuelles
    axe_essais=np.array([axes_secondaire[0,i].twinx() for i in range(nombre_figures)])


if 'nb_pas'==plot_a_faire:

    # courbe commune
    figure_primaire,axe_primaire=plt.subplots()

    # courbe commune: defaites
    axe_defaites=axe_primaire.twinx()


if 'nb_pas_total' == plot_a_faire:
    # courbe commune 2
    figure_primaire2,axe_primaire2=plt.subplots()

    # courbe commune: defaites2
    axe_defaites2=axe_primaire2.twinx()

if '3d_risque'==plot_a_faire:
    # courbe 3d
    figure_risque,axe_risque=plt.subplots()


# opacite de la courbe du nb d essais
alpha_essais=0.3


# f=lambda t:-0.25*t**2+0.5*t+32*t

# a_plot_x=np.arange(65)
# a_plot_y=(lambda t:f(t+1))(a_plot_x)

# axe_primaire2.plot(a_plot_y,a_plot_x,linestyle=':')

a_sauter=['a_etoile_graphe_oriente_hami','a_etoile_projection_queue']

if plot_a_faire in ['methodes_individuelles','nb_pas','nb_pas_total']:
    for numero_colonne,nom_feuille in enumerate(fichier.sheetnames,start=0):

        if nom_feuille in a_sauter:
            continue

        if nom_feuille!='raccourcis_croissants_v3':
            continue

        # creation des listes
        feuille=fichier[nom_feuille]

        liste_score=[]
        liste_pas_moyen=[]
        liste_essais=[]
        liste_ratio_defaite=[]
        liste_nb_pas_total=[]
        liste_score_tronquee=[]
        liste_ratio_defaite_tronquee=[]

        # recuperation des donnees en listes
        
        for i in range(donnees.score_max):
            pas_moyen=feuille['B'+str(i+2)].value
            score=feuille['A'+str(i+2)].value
            nb_parties=feuille['C'+str(i+2)].value
            ratio=feuille['F'+str(i+2)].value

            liste_score.append(score)
            liste_pas_moyen.append(pas_moyen)
            liste_essais.append(nb_parties)
            liste_ratio_defaite.append(ratio)
            

            if liste_nb_pas_total==[]:
                liste_nb_pas_total.append(pas_moyen)
                liste_score_tronquee.append(score)
                liste_ratio_defaite_tronquee.append(ratio)
            elif pas_moyen!=0:
                liste_nb_pas_total.append(liste_nb_pas_total[-1]+pas_moyen)
                liste_score_tronquee.append(score)
                liste_ratio_defaite_tronquee.append(ratio)
        

        
        if 'methodes_individuelles' == plot_a_faire:
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
        
        if 'nb_pas' == plot_a_faire:
            # plot du nb de pas en fonction du score
            axe_primaire.plot(liste_score,liste_pas_moyen,color=couleurs[numero_colonne],label=nom_feuille)

            # plot du ratio de defaites de chaque courbe
            axe_defaites.plot(liste_score,liste_ratio_defaite,color=couleurs[numero_colonne],alpha=0.6,linewidth=0.8,linestyle='-')
            axe_defaites.set_ylabel('ratio de parties perdues')

        if 'nb_pas_total' == plot_a_faire:
            # plot du score en fonction du nb de pas total
            axe_primaire2.plot(liste_nb_pas_total,liste_score_tronquee,color=couleurs[numero_colonne],label=nom_feuille)

            # plot du ratio de defaites en fonction du nb de pas total
            axe_defaites2.plot(liste_nb_pas_total,liste_ratio_defaite_tronquee,color=couleurs[numero_colonne],alpha=0.6,linewidth=0.8,linestyle='-')
            axe_defaites2.set_ylabel('ratio de parties perdues')
        

        # axe_essais[0].plot(liste_score,liste_essais,color=couleurs[numero_colonne],alpha=alpha_essais)


        # if nom_feuille=='suivre_chemin':
        #     liste_coef=np.polyfit(liste_nb_pas_total,liste_score_tronquee,2)
        #     print(liste_coef)

        #     liste_y=(lambda t:sum([liste_coef[len(liste_coef)-1-i]*t**i for i in range(len(liste_coef))]))(np.array(liste_nb_pas_total))

        #     axe_primaire2.plot(liste_nb_pas_total,liste_y,color=couleurs[numero_colonne],linestyle=':')
        



    if 'methodes_individuelles' == plot_a_faire:
        for i in range(nombre_figures):
            axes_secondaire[0,i].grid()
            axes_secondaire[1,i].grid()

    if 'nb_pas' == plot_a_faire:
        axe_primaire.set_title('nombre de pas en fonction du score')
        axe_primaire.set_xlabel('score')
        axe_primaire.set_ylabel('nombre de pas')
        axe_primaire.grid()
        axe_primaire.legend()

    if 'nb_pas_total' == plot_a_faire:
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