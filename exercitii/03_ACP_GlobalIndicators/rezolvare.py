# =====================================================================
# EXERCITIU 03 - ACP standardizata pe GlobalIndicatorsPerCapita_2021.csv
# 212 tari x 14 indicatori economici pe locuitor (USD)
# Deschide-l DOAR dupa ce ai scris codul tau!
# =====================================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

os.makedirs("data_out", exist_ok=True)

# ---- 1. Citire: index = Country (a 2-a coloana), CountryID NU intra in analiza
df = pd.read_csv("data_in/GlobalIndicatorsPerCapita_2021.csv", index_col=1)
variabile = list(df.columns.values[1:])            # sari peste CountryID (e un cod, nu un indicator)
print(df.shape, len(variabile))                     # (212, 15) 14

# ---- 2. Valori lipsa
print("NaN:", df[variabile].isna().sum().sum())    # 0 -> pasul e de siguranta
df[variabile] = df[variabile].fillna(df[variabile].mean())

# ---- 3. Matricea + standardizare + model
x = df[variabile].values
n, m = x.shape
x_ = StandardScaler().fit_transform(x)
model = PCA()
model.fit(x_)

# ---- 4. Varianta componentelor -> Varianta.csv
alpha = model.explained_variance_ * (n - 1) / n
etichete = ["C" + str(i + 1) for i in range(m)]
procent = alpha * 100 / alpha.sum()
df_varianta = pd.DataFrame({
    "Varianta": alpha,
    "Varianta cumulata": np.cumsum(alpha),
    "Procent varianta": procent,
    "Procent cumulat": np.cumsum(procent),
}, index=etichete)
print(df_varianta.round(3))
df_varianta.to_csv("data_out/Varianta.csv")

# ---- 5. Cate componente
nr_kaiser = (alpha > 1).sum()
nr_80 = np.where(np.cumsum(procent) > 80)[0][0] + 1
print("Kaiser:", nr_kaiser, "| Procent > 80%:", nr_80)  # 3 | 3

# ---- 6. Scorurile -> Scoruri.csv
c = model.transform(x_)
s = c / np.sqrt(alpha)
df_scoruri = pd.DataFrame(s, index=df.index, columns=etichete)
df_scoruri.to_csv("data_out/Scoruri.csv")
print(df_scoruri.iloc[:2, :3].round(4))

# ---- 7. Top 3 / ultimele 3 tari pe C1
print(df_scoruri["C1"].sort_values(ascending=False).head(3))
print(df_scoruri["C1"].sort_values().head(3))

# ---- 8. Corelatiile factoriale -> r.csv + variabilele "puternice" pe C1
a = model.components_.T
r = a * np.sqrt(alpha)
df_r = pd.DataFrame(r, index=variabile, columns=etichete)
df_r.to_csv("data_out/r.csv")
print(df_r[["C1", "C2"]].round(3))
print("|r| > 0.7 pe C1:", list(df_r.index[df_r["C1"].abs() > 0.7]))

# ---- 9. Comunalitatile pe primele 2 componente
comunalitati = df_r["C1"] ** 2 + df_r["C2"] ** 2
print(comunalitati.sort_values().round(3))
print("Cel mai slab explicata:", comunalitati.idxmin())

# ---- 10. Graficul scorurilor (C1, C2)
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_title("Plot scoruri (C1, C2)")
ax.set_xlabel("C1")
ax.set_ylabel("C2")
ax.scatter(s[:, 0], s[:, 1], c="r", alpha=0.5)
ax.axhline(0, c="g")
ax.axvline(0, c="g")
for i in range(n):
    ax.text(s[i, 0], s[i, 1], df.index[i], fontsize=7)
plt.show()
