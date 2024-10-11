import matplotlib.pyplot as plt
import numpy as np
import scipy


def test1():
    nb_cases=12

    liste_x=list(range(2,nb_cases,2))
    liste_y=[]

    def f(x):
        return ((2**0.25)*scipy.special.gamma(1/2)*np.exp((4*0.9*x**2)/np.pi))/((np.pi**0.75)*np.sqrt(x)*(2.414)**(2*x))

    for x in liste_x:
        produit=1
        for k in range(0,x//2):
            for l in range(0,x//2):
                if (k,l)!=(0,0):
                    produit*=(4-2*np.cos(k*np.pi/(x//2))-2*np.cos(l*np.pi/(x//2)))
        
        liste_y.append(produit/((x//2)**2))
        print(liste_y[-1])
        

    # liste_hami=[1,6,1072,4638576,467260456608,1076226888605605706,56126499620491437281263608,65882516522625836326159786165530572,1733926377888966183927790794055670829347983946,1020460427390768793543026965678152831571073052662428097106]
    liste_y_tests=[f(x) for x in liste_x]

    plt.plot(liste_x,liste_y,color='blue')
    # plt.plot(liste_x[:len(liste_hami)],liste_hami,color='red')
    # plt.plot(liste_x,liste_y_tests,color='black')
    plt.yscale('log')
    plt.show()

def test2():
    liste_x=list(range(4,20,2))
    liste_y=[40,192,528,1120,2040,3360,5152,7488]

    # print(np.polyfit(liste_x,liste_y,4))

    def f(x):
        return 1.5*x**3-4*x**2+2*x
    liste_y_test=[f(x) for x in liste_x]

    plt.plot(liste_x,liste_y,color='blue')
    plt.plot(liste_x,liste_y_test,color='red')
    plt.show()


test1()

