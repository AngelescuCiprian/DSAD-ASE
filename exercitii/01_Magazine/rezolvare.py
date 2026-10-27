# =====================================================================
# REZOLVARE - Exercitiul 01 (Magazine)
# Date: data_in/Vanzari.csv, data_in/Magazine.csv, data_in/Judete.csv
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_vanzari = pd.read_csv("data_in/Vanzari.csv", index_col=0)         # index = CodMagazin
categorii = list(df_vanzari.columns.values[1:])                       # Paine ... Dulciuri

# ---------------------------------------------------------------------
# Cerinta 1 - magazinele cu vanzari totale > 0                (15 magazine)
# ---------------------------------------------------------------------
totaluri = df_vanzari[categorii].sum(axis=1)
df_vanzari[totaluri > 0].to_csv("data_out/Cerinta1.csv")

# ---------------------------------------------------------------------
# Cerinta 2 - procentul fiecarei categorii in vanzarile magazinului
# Mega Unirii (512): 120+80+150+200+50 = 600 -> Paine 120*100/600 = 20%
# ---------------------------------------------------------------------
df_cerinta2 = df_vanzari[categorii].apply(lambda x: x * 100 / x.sum(), axis=1)
df_cerinta2 = df_cerinta2.fillna(0)
df_cerinta2.insert(0, "Magazin", df_vanzari["Magazin"])
df_cerinta2.to_csv("data_out/Cerinta2.csv")

# ---------------------------------------------------------------------
# Cerinta 3 - vanzari pe m2 pe judet, descrescator
# b: (600 + 300 + 0) / (600 + 800 + 300) = 900 / 1700 = 0.529
# ---------------------------------------------------------------------
df_vanzari["Total"] = totaluri
df_magazine = pd.read_csv("data_in/Magazine.csv", index_col=0)
df_merge = df_vanzari.merge(df_magazine, left_index=True, right_index=True)
print(df_merge.shape)                                                 # (17, 10)

df_jud = df_merge[["Judet", "Total", "Suprafata"]].groupby("Judet").sum()
s_cerinta3 = (df_jud["Total"] / df_jud["Suprafata"]).sort_values(ascending=False)
s_cerinta3.name = "VanzariMp"
s_cerinta3.to_csv("data_out/Cerinta3.csv")

# ---------------------------------------------------------------------
# Cerinta 4 - categoria cu cele mai mari vanzari pe judet
# toate Bauturi, mai putin cj -> Carne (250 vs 240)
# ---------------------------------------------------------------------
s_cerinta4 = df_merge[categorii + ["Judet"]].groupby("Judet").sum().idxmax(axis=1)
s_cerinta4.name = "Categorie"
s_cerinta4.to_csv("data_out/Cerinta4.csv")

# ---------------------------------------------------------------------
# Cerinta 5 - vanzarile totale pe regiune (merge cu cheia in COLOANA la stanga)
# Bucuresti-Ilfov 2100, Nord-Vest 2250, Vest 2050
# ---------------------------------------------------------------------
df_judete = pd.read_csv("data_in/Judete.csv", index_col=0)
df_merge_reg = df_merge.merge(df_judete, left_on="Judet", right_index=True)
s_cerinta5 = df_merge_reg[["Regiune", "Total"]].groupby("Regiune").sum()["Total"]
s_cerinta5.to_csv("data_out/Cerinta5.csv")
