# =====================================================================
# C. LDA cu 100 de instante, 10 predictori, valori proprii:
#    [0.9, 0.05, 0.8, 0.75, 0.5, 0.3, 0.2]
#    Numarul minim de variabile discriminante care acopera > 90% din
#    puterea de discriminare.
# ---------------------------------------------------------------------
# Puterea de discriminare a unei axe = valoarea ei proprie.
# Sortezi DESCRESCATOR (vectorul NU e sortat - capcana!), faci procentul
# cumulat si cauti prima pozitie > 90%.
#   sortat:     0.9  0.8  0.75  0.5  0.3  0.2  0.05     suma = 3.5
#   cumulat %: 25.7 48.6  70.0 84.3 92.9 98.6 100
#   prima > 90 e pozitia 4 -> 4 + 1 = 5 variabile discriminante
# =====================================================================
import numpy as np

alpha = np.array([0.9, 0.05, 0.8, 0.75, 0.5, 0.3, 0.2])
alpha = np.flip(np.sort(alpha))
procent_cumulat = np.cumsum(alpha) * 100 / np.sum(alpha)
k = np.where(procent_cumulat > 90)[0][0] + 1
print("Procent cumulat:", np.round(procent_cumulat, 2))
print("Numar minim de variabile discriminante:", k)     # 5
