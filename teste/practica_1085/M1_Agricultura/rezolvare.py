# =====================================================================
# MODEL M1 - Agricultura pe localitati (tiparul S1_1085)
# Date: data_in/Agricultura.csv, data_in/PopulatieLocalitati.csv
# =====================================================================

import os
import numpy as np
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_agri = pd.read_csv("data_in/Agricultura.csv", index_col=0)               # index = Siruta
df_pop = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)

df_merge = df_agri.merge(df_pop[["Judet", "Populatie"]], left_index=True, right_index=True)
print("Shape dupa merge:", df_merge.shape)                                   # (3181, 8)


# =====================================================================
# CERINTA 1 - randamentul (ProductieTone / SuprafataHa) pentru localitatile
# CU suprafata agricola, descrescator                                (2p)
# CAPCANA: exista localitati cu productie dar SuprafataHa = 0 -> fara filtru
#          iese inf primul la sortare.
# =====================================================================
df_cu_sup = df_agri[df_agri["SuprafataHa"] > 0]
df_output1 = df_cu_sup[["Localitate"]].copy()
df_output1["Randament"] = df_cu_sup["ProductieTone"] / df_cu_sup["SuprafataHa"]
df_output1 = df_output1.sort_values(by="Randament", ascending=False)
df_output1.to_csv("data_out/Output1.csv")


# =====================================================================
# CERINTA 2 - numarul de ferme la 1000 de locuitori, pe judet, desc.  (2p)
# REGULA: aduni NrFerme si Populatie pe judet (TOATE localitatile), apoi imparti
# =====================================================================
df_judete = df_merge[["Judet", "NrFerme", "Populatie"]].groupby("Judet").sum()
s_output2 = (df_judete["NrFerme"] / df_judete["Populatie"] * 1000).sort_values(ascending=False)
s_output2.index = s_output2.index.str.upper()
s_output2.name = "Ferme la 1000 loc"
s_output2.to_csv("data_out/Output2.csv")


# =====================================================================
# CERINTA 3 - pe judet, localitatea cu cele mai mari subventii pe HECTAR
# (doar localitatile cu suprafata agricola)                          (2p)
# CAPCANA: din nou impartire la suprafata -> filtrezi SuprafataHa > 0 INAINTE
# Judetul B nu are nicio localitate cu suprafata -> nu apare in output (corect)
# =====================================================================
df_m3 = df_merge[df_merge["SuprafataHa"] > 0].copy()
df_m3["SubvHa"] = df_m3["Subventii"] / df_m3["SuprafataHa"]
s_siruta = df_m3.groupby("Judet")["SubvHa"].idxmax()                         # judet -> Siruta

df_output3 = s_siruta.map(df_m3["Localitate"]).to_frame(name="Localitate")
df_output3.index = df_output3.index.str.upper()
df_output3.to_csv("data_out/Output3.csv")


# =====================================================================
# CERINTA 4 - mediile ponderate pe judet pentru NrFerme, ProductieTone,
# NrAnimale, Subventii, cu PONDEREA = SUPRAFATA AGRICOLA (nu populatia!).
# Judetele fara suprafata agricola se omit.                          (3p)
# CAPCANA: pentru B suma ponderilor e 0 -> np.average da ZeroDivisionError.
#          Daca pastrezi doar localitatile cu SuprafataHa > 0, B dispare singur.
# =====================================================================
indicatori4 = ["NrFerme", "ProductieTone", "NrAnimale", "Subventii"]


def medii_ponderate(t: pd.DataFrame):
    return pd.Series(np.average(t[indicatori4], axis=0, weights=t["SuprafataHa"]), index=indicatori4)


df_output4 = df_m3[indicatori4 + ["SuprafataHa", "Judet"]].groupby("Judet").apply(
    func=medii_ponderate, include_groups=False)
df_output4.index = df_output4.index.str.upper()
df_output4.round(3).to_csv("data_out/Output4.csv")

# Varianta fara functie:
#   produs = df_m3[indicatori4].mul(df_m3["SuprafataHa"], axis=0); produs["SuprafataHa"] = df_m3["SuprafataHa"]
#   produs["Judet"] = df_m3["Judet"]; sume = produs.groupby("Judet").sum()
#   sume[indicatori4].div(sume["SuprafataHa"], axis=0)
