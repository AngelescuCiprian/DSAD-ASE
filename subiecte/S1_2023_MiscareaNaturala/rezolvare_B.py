# =====================================================================
# REZOLVARE - Subiect S1_2023 (MiscareaNaturala), partea B
# Analiza in componente principale STANDARDIZATA pe cei 7 indicatori.
# Foloseste functiile profului din functii.py (acp, nan_replace_df).
# =====================================================================

import os
import numpy as np
import pandas as pd

from functii import nan_replace_df, acp, tabelare_varianta
from grafice import plot_varianta, plot_scoruri, show

os.makedirs("data_out", exist_ok=True)
np.set_printoptions(precision=3, suppress=True)

df = pd.read_csv("data_in/MiscareaNaturala.csv", index_col=0)
indicatori = list(df.columns.values[2:])           # FR, IM, LE, LEF, LEM, MMR, RS
nan_replace_df(df)                                 # aici nu sunt NaN, dar e bine sa fie mereu
x = df[indicatori].values                          # 182 x 7

x_, r_v, alpha, a, c, r = acp(x)                   # std=True implicit -> ACP standardizata


# ---------------------------------------------------------------------
# B1. Variantele componentelor principale -> la consola
#     Varianta componentei k = valoarea proprie alpha[k]
#     (suma lor = 7 = numarul de variabile, pentru ca e standardizata)
# ---------------------------------------------------------------------
print("Variantele componentelor:", alpha)
print("Suma variantelor:", alpha.sum())            # 7.0
print(tabelare_varianta(alpha))                    # bonus: tabelul complet


# ---------------------------------------------------------------------
# B2. Scorurile asociate instantelor -> scoruri.csv
#     Scorurile = componentele principale standardizate: s = c / sqrt(alpha)
#     (fiecare coloana a lui c are varianta alpha_k; impartind la sqrt(alpha_k)
#      toate coloanele ajung la varianta 1 si se pot compara intre ele)
#     Daca profu' cere "componentele", salvezi c; pentru "scoruri", s.
# ---------------------------------------------------------------------
etichete_comp = ["C" + str(i + 1) for i in range(len(alpha))]
s = c / np.sqrt(alpha)
df_scoruri = pd.DataFrame(s, index=df["Three_Letter_Country_Code"], columns=etichete_comp)
df_scoruri.to_csv("data_out/scoruri.csv")
print(df_scoruri.head())


# ---------------------------------------------------------------------
# B3. Graficul scorurilor in primele doua axe (C1, C2)
#     Fiecare punct = o tara, etichetat cu codul ei.
# ---------------------------------------------------------------------
plot_varianta(alpha)
plot_scoruri(s, df["Three_Letter_Country_Code"].values, titlu="Plot scoruri (C1, C2)")
show()
