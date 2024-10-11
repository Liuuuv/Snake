import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

nb_cases=5

dimensions_grille=(nb_cases,nb_cases)


graphe=nx.Graph()

def changer_referentiel(pos):
    return (pos[0],nb_cases-pos[1]-1)

def distance(pos1,pos2):
    return abs(pos2[0]-pos1[0])+abs(pos2[1]-pos1[1])

liste_pos=[]
for j in range(nb_cases):
    for i in range(nb_cases):
        graphe.add_node(changer_referentiel((j,i)),pos=(j,i))
        liste_pos.append((j,i))

        if j<nb_cases-1:
            graphe.add_edge((j,i),(j+1,i))
        if i<nb_cases-1:
            graphe.add_edge((j,i),(j,i+1))


# Extraire les positions des nœuds dans un dictionnaire
positions_noeuds={node:pos for node,pos in nx.get_node_attributes(graphe,'pos').items()}

# plt.figure()
# nx.draw(graphe, pos=positions_noeuds, with_labels=True)




# graphe_adjoint=nx.line_graph(graphe)

# plt.figure()
# nx.draw(graphe_adjoint, with_labels=True)

# print(nx.adjacency_spectrum(graphe))


# graphe_antecedent=nx.inverse_line_graph(graphe)
# plt.figure()
# nx.draw(graphe_antecedent, with_labels=True)

plt.show()













