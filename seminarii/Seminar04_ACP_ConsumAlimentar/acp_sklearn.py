# =====================================================================
# ACP CU BIBLIOTECA (sklearn) - sablonul de retinut pentru examen
# Varianta profului din seminar + tot ce cere partea B la ACP:
#   varianta (consola / Varianta.csv), scoruri (Scoruri.csv), graficul scorurilor
# + extra: corelatii factoriale, cercul corelatiilor, comunalitati
# =====================================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from functii import nan_replace_df

os.makedirs("data_out", exist_ok=True)

# ---------------------------------------------------------------------
# 0. DATELE -> matricea x (numpy). La fel ca la partea A.
# ---------------------------------------------------------------------
df = pd.read_csv("data_in/ConsumAlimentar/ConsumAlimentar.csv", index_col=0)  # index = Country
variabile = list(df.columns.values[1:])         # sari peste Code (text)
nan_replace_df(df)                               # NaN -> media
x = df[variabile].values                         # 170 x 11
n, m = x.shape

# ---------------------------------------------------------------------
# 1. MODELUL: standardizare + PCA  (2 linii care fac toata matematica)
# ---------------------------------------------------------------------
x_ = StandardScaler().fit_transform(x)           # medie 0, varianta 1 pe fiecare coloana
model = PCA()                                     # fara n_components -> toate cele m componente
model.fit(x_)

# ---------------------------------------------------------------------
# 2. CE SCOTI DIN MODEL (de stiut pe de rost)
# ---------------------------------------------------------------------
alpha = model.explained_variance_ * (n - 1) / n  # valorile proprii (sklearn imparte la n-1, profu la n)
a = model.components_.T                          # vectorii proprii PE COLOANE (sklearn ii da pe randuri)
c = model.transform(x_)                          # componentele (n x m) = x_ @ a
s = c / np.sqrt(alpha)                           # SCORURILE = componente standardizate
r = a * np.sqrt(alpha)                           # corelatiile variabile - componente
etichete = ["C" + str(i + 1) for i in range(m)]

# ---------------------------------------------------------------------
# B1. VARIANTA COMPONENTELOR (+ criteriile de selectie)
# ---------------------------------------------------------------------
procent = alpha * 100 / alpha.sum()              # = model.explained_variance_ratio_ * 100
df_varianta = pd.DataFrame({
    "Varianta": alpha,
    "Varianta cumulata": np.cumsum(alpha),
    "Procent varianta": procent,
    "Procent cumulat": np.cumsum(procent),
}, index=etichete)
print(df_varianta)
df_varianta.to_csv("data_out/Varianta.csv")

nr_kaiser = (alpha > 1).sum()                                  # criteriul Kaiser
nr_procent = np.where(np.cumsum(procent) > 80)[0][0] + 1      # prima pozitie > 80%, +1 (pozitia incepe de la 0)
print("Kaiser:", nr_kaiser, "componente | Procent > 80%:", nr_procent, "componente")

# ---------------------------------------------------------------------
# B2. SCORURILE -> Scoruri.csv
# ---------------------------------------------------------------------
df_scoruri = pd.DataFrame(s, index=df.index, columns=etichete)
df_scoruri.to_csv("data_out/Scoruri.csv")

# ---------------------------------------------------------------------
# B3. GRAFICUL SCORURILOR in primele doua axe
# ---------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_title("Plot scoruri (C1, C2)")
ax.set_xlabel("C1")
ax.set_ylabel("C2")
ax.scatter(s[:, 0], s[:, 1], c="r", alpha=0.5)
ax.axhline(0, c="g")
ax.axvline(0, c="g")
for i, eticheta in enumerate(df.index):
    ax.text(s[i, 0], s[i, 1], eticheta, fontsize=7)

# ---------------------------------------------------------------------
# EXTRA (apar la unele subiecte / la partea C)
# ---------------------------------------------------------------------
# Corelatiile factoriale -> r.csv (cu ele interpretezi componentele)
df_r = pd.DataFrame(r, index=variabile, columns=etichete)
df_r.to_csv("data_out/r.csv")

# Comunalitatile: cat din varianta fiecarei variabile explica primele k componente
df_comunalitati = pd.DataFrame(np.cumsum(r * r, axis=1), index=variabile, columns=etichete)
df_comunalitati.to_csv("data_out/Comunalitati.csv")

# Cercul corelatiilor (C1, C2): fiecare variabila e un punct (r pe C1, r pe C2)
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_title("Cercul corelatiilor (C1, C2)")
ax.add_patch(plt.Circle((0, 0), 1, fill=False, color="b"))
ax.scatter(r[:, 0], r[:, 1], c="r")
for i, v in enumerate(variabile):
    ax.text(r[i, 0], r[i, 1], v, fontsize=8)
ax.axhline(0, c="g")
ax.axvline(0, c="g")
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect(1)

plt.show()
