# =====================================================================
# MODEL M5 - Consumul de energie electrica pe localitati, 2019-2023 (MWh)
# Tiparul S2_1091 (date pe ANI): medie pe rand, anul cu maximul,
# raport pe judet si an cu div(axis=0), judetul cu maximul pe regiune si an
# Date: data_in/Energie.csv, data_in/PopulatieLocalitati.csv, data_in/Coduri_Judete.csv
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_energie = pd.read_csv("data_in/Energie.csv", index_col=0)                # index = Siruta
ani = list(df_energie.columns.values[1:])          # ['2019', ..., '2023'] (sunt TEXTE, nu numere)
df_pop = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)
df_coduri = pd.read_csv("data_in/Coduri_Judete.csv", index_col=0)           # index = IndicativJudet

df_merge = df_energie.merge(df_pop[["Judet", "Populatie"]], left_index=True, right_index=True)


# =====================================================================
# CERINTA 1 - consumul mediu anual, doar pentru localitatile cu consum
# in TOTI anii, descrescator                                         (2p)
# (df[ani] > 0).all(axis=1) = True daca TOATE valorile din rand sunt > 0
# =====================================================================
df_complete = df_energie[(df_energie[ani] > 0).all(axis=1)]
df_output1 = df_complete[["Localitate"]].copy()
df_output1["ConsumMediu"] = df_complete[ani].mean(axis=1)
df_output1 = df_output1.sort_values(by="ConsumMediu", ascending=False)
df_output1.to_csv("data_out/Output1.csv")


# =====================================================================
# CERINTA 2 - pentru fiecare localitate, anul cu cel mai mare consum  (2p)
# idxmax(axis=1) -> numele COLOANEI cu maximul de pe fiecare rand
# =====================================================================
df_output2 = df_energie[["Localitate"]].copy()
df_output2["AnMaxim"] = df_energie[ani].idxmax(axis=1)
df_output2.to_csv("data_out/Output2.csv")


# =====================================================================
# CERINTA 3 - consumul pe locuitor (kWh / locuitor) pe judet, pentru
# fiecare an                                                         (2p)
# REGULA: sume pe judet, apoi impartire. 1 MWh = 1000 kWh
# df[ani].div(serie, axis=0): fiecare RAND (judet) impartit la populatia lui
# (df[ani] / serie ar alinia pe COLOANE -> tot NaN!)
# =====================================================================
df_judete = df_merge[ani + ["Judet", "Populatie"]].groupby("Judet").sum()
df_cons_loc = df_judete[ani].div(df_judete["Populatie"], axis=0) * 1000

df_output3 = df_cons_loc.copy()
df_output3.index = df_output3.index.str.upper()
df_output3.to_csv("data_out/Output3.csv")


# =====================================================================
# CERINTA 4 - pentru fiecare regiune si fiecare an, judetul cu cel mai
# mare consum pe locuitor                                            (3p)
# 1. lipesti Regiune pe tabelul pe judete (indexul = indicativul judetului)
# 2. groupby("Regiune")[ani].idxmax() -> pe fiecare an, INDEXUL (judetul) cu maximul
# CAPCANA: faci merge-ul pe indicativele cu litere MICI (ca in Coduri_Judete),
#          abia la final .str.upper()
# =====================================================================
df_cons_reg = df_cons_loc.merge(df_coduri[["Regiune"]], left_index=True, right_index=True)
df_output4 = df_cons_reg.groupby("Regiune")[ani].idxmax()
df_output4 = df_output4.apply(lambda col: col.str.upper())
df_output4.to_csv("data_out/Output4.csv")
