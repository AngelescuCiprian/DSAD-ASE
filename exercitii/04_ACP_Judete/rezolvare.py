# =====================================================================
# EXERCITIU 04 - ACP standardizata pe judetele Romaniei (Teritorial_2022.csv)
# 42 de judete x 31 de indicatori (demografie, salarii, sanatate, cultura,
# agricultura, buget, utilitati, export). Deschide-l DOAR dupa ce ai scris codul tau!
# =====================================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

os.makedirs("data_out", exist_ok=True)

# ---- 1. DATE: index = Indicativ; Judet, Regiunea, Macroregiunea NU sunt indicatori
df = pd.read_csv("data_in/Teritorial_2022.csv", index_col=0)
variabile = list(df.columns.values[3:])          # Macroregiunea e numar, dar e un COD -> afara
print(df.shape, len(variabile), variabile[0], variabile[-1])   # (42, 34) 31 RN Export

# ---- 2. VALORI LIPSA
print("NaN inainte:", df[variabile].isna().sum().sum())        # 4
df[variabile] = df[variabile].fillna(df[variabile].mean())
print("NaN dupa:", df[variabile].isna().sum().sum())           # 0

# ---- 3. MATRICEA + STANDARDIZARE
x = df[variabile].values
n, m = x.shape
x_ = StandardScaler().fit_transform(x)

# ---- 4. MODEL + VARIANTA
model = PCA().fit(x_)
alpha = model.explained_variance_ * (n - 1) / n
print(round(alpha[0], 3), round(alpha.sum(), 3))              # 10.451 31.0

# ---- 5. TABELUL VARIANTEI -> Varianta.csv
etichete = ["C" + str(i + 1) for i in range(m)]
procent = alpha * 100 / alpha.sum()
df_varianta = pd.DataFrame({
    "Varianta": alpha,
    "Varianta cumulata": np.cumsum(alpha),
    "Procent varianta": procent,
    "Procent cumulat": np.cumsum(procent),
}, index=etichete)
print(df_varianta.round(3).head(10))
df_varianta.to_csv("data_out/Varianta.csv")

# ---- 6. CRITERII
nr_kaiser = (alpha > 1).sum()
nr_80 = np.where(np.cumsum(procent) > 80)[0][0] + 1
print("Kaiser:", nr_kaiser, "| Procent > 80%:", nr_80)       # 9 | 9

# ---- 7. SCORURI -> Scoruri.csv
c = model.transform(x_)
s = c / np.sqrt(alpha)
df_scoruri = pd.DataFrame(s, index=df.index, columns=etichete)
df_scoruri.to_csv("data_out/Scoruri.csv")
print(df_scoruri.iloc[:2, :2].round(4))

# ---- 8. TOP / COADA pe C1
print(df_scoruri["C1"].sort_values(ascending=False).head(3))  # b, cj, bv
print(df_scoruri["C1"].sort_values().head(3))                  # tr, gr, cl

# ---- 9. CORELATII -> r.csv + variabilele cu |r| > 0.8 pe C1
a = model.components_.T
r = a * np.sqrt(alpha)
df_r = pd.DataFrame(r, index=variabile, columns=etichete)
df_r.to_csv("data_out/r.csv")
print("|r| > 0.8 pe C1:", list(df_r.index[df_r["C1"].abs() > 0.8]))   # Sal, Medici, PIB

# ---- 10. GRAFICUL SCORURILOR (C1, C2)
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_title("Plot scoruri (C1, C2)")
ax.set_xlabel("C1")
ax.set_ylabel("C2")
ax.scatter(s[:, 0], s[:, 1], c="r")
ax.axhline(0, c="g")
ax.axvline(0, c="g")
for i in range(n):
    ax.text(s[i, 0], s[i, 1], df.index[i])
plt.show()
