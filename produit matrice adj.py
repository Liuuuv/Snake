import numpy as np

nb_cases=4

M=np.array([
[0,1,1,0],
[1,0,0,1],
[1,0,0,1],
[0,1,1,0]
])

M=np.array([
[0,1,0,1],
[1,0,1,0],
[0,1,0,1],
[1,0,1,0]
])

M=np.array([
[0,0,1,1],
[0,0,1,1],
[1,1,0,0],
[1,1,0,0]
])


# M^k
k=6
N=np.identity(4)
for _ in range(k):
   N=np.matmul(N,M)

# laplacien: creation
matrice_adjacence=M.copy()
laplacien=np.negative(np.copy(matrice_adjacence))
for i in range(nb_cases):
   compteur=0
   for j in range(nb_cases):
     if matrice_adjacence[i,j]==1:
        compteur+=1
   laplacien[i,i]=compteur



print(laplacien)
print(np.linalg.eigvals(laplacien))


print(np.linalg.eigvals(M))

"""[M^k]_ij donne le nombre de chemins de i à j de longueur k, on peut voir M+M^3+M^4+...+M^n pour avoir le nb de chemins de longueur inférieure à n"""