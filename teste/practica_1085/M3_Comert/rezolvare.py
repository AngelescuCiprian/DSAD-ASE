# =====================================================================
# MODEL M3 - Comert pe localitati, agregat pe REGIUNI (tiparul S1_1085 + un nivel in plus)
# Date: data_in/Comert.csv, data_in/PopulatieLocalitati.csv, data_in/Coduri_Judete.csv
# =====================================================================

import os
import numpy as np
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_com = pd.read_csv("data_in/Comert.csv", index_col=0)                     # index = Siruta
indicatori = list(df_com.columns.values[1:])        # ['NrMagazine', 'NrAngajati', 'Vanzari', 'Chirii']
df_pop = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)       # Siruta, Localitate, Judet, Populatie
df_coduri = pd.read_csv("data_in/Coduri_Judete.csv", index_col=0)          # IndicativJudet, NumeJudet, Regiune

# DOUA merge-uri: localitate -> judet (dupa Siruta), apoi judet -> regiune
# al doilea: cheia e COLOANA "Judet" in stanga si INDEXUL in dreapta -> left_on + right_index
df_merge = df_com.merge(df_pop[["Judet", "Populatie"]], left_index=True, right_index=True)
df_merge = df_merge.merge(df_coduri[["Regiune"]], left_on="Judet", right_index=True)
print("Shape dupa merge:", df_merge.shape)                                   # (3181, 8)


# =====================================================================
# CERINTA 1 - vanzarile pe angajat, pentru localitatile CU angajati,
# descrescator                                                       (2p)
# =====================================================================
df_cu_ang = df_com[df_com["NrAngajati"] > 0]
df_output1 = df_cu_ang[["Localitate"]].copy()
df_output1["Vanzari/Angajat"] = df_cu_ang["Vanzari"] / df_cu_ang["NrAngajati"]
df_output1 = df_output1.sort_values(by="Vanzari/Angajat", ascending=False)
df_output1.to_csv("data_out/Output1.csv")


# =====================================================================
# CERINTA 2 - angajati in comert la 1000 de locuitori, pe REGIUNE, desc.  (2p)
# =====================================================================
df_regiuni = df_merge[["Regiune", "NrAngajati", "Populatie"]].groupby("Regiune").sum()
s_output2 = (df_regiuni["NrAngajati"] / df_regiuni["Populatie"] * 1000).sort_values(ascending=False)
s_output2.name = "Angajati la 1000 loc"
s_output2.to_csv("data_out/Output2.csv")


# =====================================================================
# CERINTA 3 - pe regiune, JUDETUL cu cele mai mari vanzari pe locuitor   (2p)
# DOUA niveluri:
#   1. vanzarile si populatia pe JUDET (sume), apoi vanzari / locuitor pe judet
#   2. pe REGIUNE, judetul cu maximul -> idxmax da direct indicativul (e indexul)
# =====================================================================
df_jud = df_merge[["Judet", "Regiune", "Vanzari", "Populatie"]].groupby(["Judet", "Regiune"]).sum()
df_jud = df_jud.reset_index(level="Regiune")                     # Judet ramane index, Regiune coloana
df_jud["VanzariLoc"] = df_jud["Vanzari"] / df_jud["Populatie"]

s_output3 = df_jud.groupby("Regiune")["VanzariLoc"].idxmax().str.upper()
s_output3.name = "Judet"
s_output3.to_csv("data_out/Output3.csv")


# =====================================================================
# CERINTA 4 - mediile ponderate (pondere = populatia LOCALITATILOR) ale celor
# 4 indicatori, pe regiune                                           (3p)
# =====================================================================
def medii_ponderate(t: pd.DataFrame):
    return pd.Series(np.average(t[indicatori], axis=0, weights=t["Populatie"]), index=indicatori)


df_output4 = df_merge[indicatori + ["Populatie", "Regiune"]].groupby("Regiune").apply(
    func=medii_ponderate, include_groups=False)
df_output4.round(3).to_csv("data_out/Output4.csv")
