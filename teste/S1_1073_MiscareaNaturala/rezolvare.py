# =====================================================================
# TEST S1 (1073) - Miscarea naturala a populatiei pe localitati
# Date: data_in/MiscareaNatLoc.csv, data_in/PopulatieLocalitati.csv
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_mn = pd.read_csv("data_in/MiscareaNatLoc.csv", index_col=0)               # index = Siruta
indicatori = list(df_mn.columns.values[1:])
# ['Casatorii', 'Decedati', 'DecedatiSub1An', 'Divorturi', 'NascutiMorti', 'NascutiVii']
df_pop = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)

df_merge = df_mn.merge(df_pop[["Judet", "Populatie"]], left_index=True, right_index=True)


# =====================================================================
# CERINTA 1 - localitatile cu TotalDecedati (Decedati + DecedatiSub1An)
# > NascutiVii                                                       (2p)
# Ordinea din fisier (fara sortare). Ciugud: 42 + 0 = 42 > 25
# =====================================================================
df_cerinta1 = df_mn[["Localitate"]].copy()
df_cerinta1["TotalDecedati"] = df_mn["Decedati"] + df_mn["DecedatiSub1An"]
df_cerinta1["NascutiVii"] = df_mn["NascutiVii"]
df_cerinta1 = df_cerinta1[df_cerinta1["TotalDecedati"] > df_cerinta1["NascutiVii"]]
df_cerinta1.to_csv("data_out/Cerinta1.csv")


# =====================================================================
# CERINTA 2 - rata mortalitatii infantile = DecedatiSub1An * 1000 / NascutiVii,
# descrescator                                                       (2p)
# In datele astea NU exista localitati cu 0 nascuti vii, deci merge si fara filtru.
# Filtrul e reflexul bun: daca ar exista, x/0 = inf ar iesi PRIMUL la sortare.
# =====================================================================
df_cu_nasteri = df_mn[df_mn["NascutiVii"] > 0]
df_cerinta2 = df_cu_nasteri[["Localitate"]].copy()
df_cerinta2["RMI"] = df_cu_nasteri["DecedatiSub1An"] * 1000 / df_cu_nasteri["NascutiVii"]
df_cerinta2 = df_cerinta2.sort_values(by="RMI", ascending=False)
df_cerinta2.to_csv("data_out/Cerinta2.csv")


# =====================================================================
# CERINTA 3 - rata sporului natural pe judet, CRESCATOR              (2p)
#   RSN = NascutiVii la 1000 loc - Decedati la 1000 loc
# REGULA: sume pe judet, apoi impartire
# =====================================================================
df_judete = df_merge[["Judet", "NascutiVii", "Decedati", "Populatie"]].groupby("Judet").sum()
s_cerinta3 = (df_judete["NascutiVii"] - df_judete["Decedati"]) * 1000 / df_judete["Populatie"]
s_cerinta3 = s_cerinta3.sort_values(ascending=True)
s_cerinta3.name = "RSN"
s_cerinta3.to_csv("data_out/Cerinta3.csv")


# =====================================================================
# CERINTA 4 - pe judet, localitatea cu rata maxima (la 1000 loc) pentru
# FIECARE indicator                                                  (3p)
# 1. ratele pe localitate: fiecare RAND impartit la populatia lui -> div(axis=0)
# 2. groupby("Judet").idxmax() -> in fiecare celula, Siruta localitatii cu maximul
# 3. traduci Siruta -> nume, coloana cu coloana: apply(lambda col: col.map(...))
# =====================================================================
df_rate = df_merge[indicatori].div(df_merge["Populatie"], axis=0) * 1000
df_rate["Judet"] = df_merge["Judet"]

df_siruta = df_rate.groupby("Judet").idxmax()                      # judet x indicator -> Siruta
df_cerinta4 = df_siruta.apply(lambda col: col.map(df_mn["Localitate"]))
df_cerinta4.to_csv("data_out/Cerinta4.csv")
