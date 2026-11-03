# =====================================================================
# MODEL M2 - Sanatate pe localitati (tiparul S1_1085, cel mai apropiat de test)
# Date: data_in/Sanatate.csv, data_in/PopulatieLocalitati.csv
# =====================================================================

import os
import numpy as np
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_san = pd.read_csv("data_in/Sanatate.csv", index_col=0)                   # index = Siruta
indicatori = list(df_san.columns.values[1:])
# ['NrMedici', 'NrPaturi', 'NrFarmacii', 'Internari', 'Cheltuieli']
df_pop = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)

df_merge = df_san.merge(df_pop[["Judet", "Populatie"]], left_index=True, right_index=True)


# =====================================================================
# CERINTA 1 - internari pe pat de spital, pentru localitatile CU paturi,
# descrescator                                                       (2p)
# CAPCANA: localitati cu internari de zi dar 0 paturi -> inf fara filtru
# =====================================================================
df_cu_paturi = df_san[df_san["NrPaturi"] > 0]
df_output1 = df_cu_paturi[["Localitate"]].copy()
df_output1["Internari/Pat"] = df_cu_paturi["Internari"] / df_cu_paturi["NrPaturi"]
df_output1 = df_output1.sort_values(by="Internari/Pat", ascending=False)
df_output1.to_csv("data_out/Output1.csv")


# =====================================================================
# CERINTA 2 - medici la 1000 de locuitori, pe judet, descrescator     (2p)
# REGULA: sume pe judet pe TOT tabelul (nu pe cel filtrat la cerinta 1!)
# =====================================================================
df_judete = df_merge[["Judet", "NrMedici", "Populatie"]].groupby("Judet").sum()
s_output2 = (df_judete["NrMedici"] / df_judete["Populatie"] * 1000).sort_values(ascending=False)
s_output2.index = s_output2.index.str.upper()
s_output2.name = "Medici la 1000 loc"
s_output2.to_csv("data_out/Output2.csv")


# =====================================================================
# CERINTA 3 - pe judet, localitatea cu cele mai mari cheltuieli pe locuitor
# SI valoarea acestora                                               (2p)
# Diferenta fata de test: se cere si VALOAREA -> al doilea map
# =====================================================================
df_merge["ChLoc"] = df_merge["Cheltuieli"] / df_merge["Populatie"]
s_siruta = df_merge.groupby("Judet")["ChLoc"].idxmax()

df_output3 = s_siruta.map(df_merge["Localitate"]).to_frame(name="Localitate")
df_output3["Cheltuieli/Loc"] = s_siruta.map(df_merge["ChLoc"])
df_output3.index = df_output3.index.str.upper()
df_output3.to_csv("data_out/Output3.csv")


# =====================================================================
# CERINTA 4 - mediile ponderate (pondere = populatia) ale celor 5 indicatori,
# pe judet                                                           (3p)
# =====================================================================
def medii_ponderate(t: pd.DataFrame):
    return pd.Series(np.average(t[indicatori], axis=0, weights=t["Populatie"]), index=indicatori)


df_output4 = df_merge[indicatori + ["Populatie", "Judet"]].groupby("Judet").apply(
    func=medii_ponderate, include_groups=False)
df_output4.index = df_output4.index.str.upper()
df_output4.round(3).to_csv("data_out/Output4.csv")
