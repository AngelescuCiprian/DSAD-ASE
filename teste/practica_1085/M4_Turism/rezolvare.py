# =====================================================================
# MODEL M4 - Turism: locuri de cazare pe tipuri, pe localitati
# Tiparul SEMINARULUI 3 (IndustriaAlimentara): total pe rand, procente cu 0,
# tip dominant pe judet, indice de localizare
# Date: data_in/Turism.csv, data_in/PopulatieLocalitati.csv
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_turism = pd.read_csv("data_in/Turism.csv", index_col=0)                  # index = Siruta
tipuri = list(df_turism.columns.values[1:])        # ['Hotel', 'Pensiune', 'Vila', 'Camping', 'Hostel']
df_pop = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)

df_merge = df_turism.merge(df_pop[["Judet", "Populatie"]], left_index=True, right_index=True)


# =====================================================================
# CERINTA 1 - capacitatea totala de cazare, doar localitatile care AU
# locuri de cazare, descrescator                                     (2p)
# Seminar 3, cerinta 1: sum(axis=1) = total pe RAND
# =====================================================================
s_total = df_turism[tipuri].sum(axis=1)
df_output1 = df_turism[["Localitate"]].copy()
df_output1["Total"] = s_total
df_output1 = df_output1[df_output1["Total"] > 0].sort_values(by="Total", ascending=False)
df_output1.to_csv("data_out/Output1.csv")


# =====================================================================
# CERINTA 2 - procentul fiecarui tip de cazare in capacitatea localitatii.
# Daca localitatea nu are locuri de cazare, procentele sunt 0.        (2p)
# Seminar 3, cerinta 2. CAPCANA: 0/0 = NaN -> fillna(0)
# df.div(serie, axis=0) = imparte fiecare RAND la valoarea lui din serie
# =====================================================================
df_output2 = df_turism[tipuri].div(s_total, axis=0) * 100
df_output2 = df_output2.fillna(0)
df_output2.insert(0, "Localitate", df_turism["Localitate"])
df_output2.to_csv("data_out/Output2.csv")
# varianta profului: apply(lambda x: x[tipuri]*100/x["Total"], axis=1) + fillna(0)


# =====================================================================
# CERINTA 3 - pe judet, tipul de cazare cu cele mai multe locuri      (2p)
# Seminar 3, cerinta 4: intai SUME pe judet, apoi idxmax(axis=1) = numele COLOANEI
# =====================================================================
df_judete = df_merge[tipuri + ["Judet", "Populatie"]].groupby("Judet").sum()
s_output3 = df_judete[tipuri].idxmax(axis=1)
s_output3.index = s_output3.index.str.upper()
s_output3.name = "Tip"
s_output3.to_csv("data_out/Output3.csv")


# =====================================================================
# CERINTA 4 - indicele de localizare pe judet, pentru fiecare tip     (3p)
#   IL = (locuri judet / locuri tara) / (populatie judet / populatie tara)
# Seminar 3, cerinta 6 (la prof e neterminata!)
#   - numaratorul: fiecare COLOANA impartita la totalul ei -> df / serie (aliniere pe coloane)
#   - numitorul: o serie pe judete -> .div(..., axis=0) (aliniere pe randuri)
# =====================================================================
s_nat = df_judete[tipuri].sum()                                   # totalul national pe fiecare tip
pondere_tip = df_judete[tipuri] / s_nat                           # judet / tara, pe fiecare coloana
pondere_pop = df_judete["Populatie"] / df_judete["Populatie"].sum()
df_output4 = pondere_tip.div(pondere_pop, axis=0)
df_output4.index = df_output4.index.str.upper()
df_output4.to_csv("data_out/Output4.csv")
