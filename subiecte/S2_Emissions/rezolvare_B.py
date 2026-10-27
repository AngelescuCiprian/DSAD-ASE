# =====================================================================
# REZOLVARE - Subiect S2 (Emissions), partea B
# Analiza in componente principale STANDARDIZATA pe cele 8 tipuri de emisii.
# (Fiind standardizata, nu conteaza ca GreenGE/GreenGIE sunt in mii de tone.)
# =====================================================================

import os
import numpy as np
import pandas as pd

from functii import nan_replace_df, acp, tabelare_varianta
from grafice import plot_varianta, plot_scoruri, show

os.makedirs("data_out", exist_ok=True)
np.set_printoptions(precision=3, suppress=True)

df = pd.read_csv("data_in/Emissions.csv", index_col=0)    # index = CountryCode
variabile = list(df.columns.values[1:])
nan_replace_df(df)
x = df[variabile].values                                   # 32 x 8

x_, r_v, alpha, a, c, r = acp(x)


# ---------------------------------------------------------------------
# B1. Tabelul variantei -> Varianta.csv
#     varianta, procent, varianta cumulata, procent cumulat (functia profului)
# ---------------------------------------------------------------------
df_varianta = tabelare_varianta(alpha)
print(df_varianta)
df_varianta.to_csv("data_out/Varianta.csv")


# ---------------------------------------------------------------------
# B2. Scorurile -> Scoruri.csv   (s = c / sqrt(alpha))
# ---------------------------------------------------------------------
etichete_comp = ["C" + str(i + 1) for i in range(len(alpha))]
s = c / np.sqrt(alpha)
df_scoruri = pd.DataFrame(s, index=df.index, columns=etichete_comp)
df_scoruri.to_csv("data_out/Scoruri.csv")


# ---------------------------------------------------------------------
# B3. Graficul scorurilor in C1, C2
# ---------------------------------------------------------------------
plot_varianta(alpha)
plot_scoruri(s, df.index.values, titlu="Plot scoruri (C1, C2)")
show()
