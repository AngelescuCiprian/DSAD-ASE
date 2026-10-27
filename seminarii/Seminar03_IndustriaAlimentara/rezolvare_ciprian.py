# =====================================================================
# Tema2_4 - Cerintele 1-4, rezolvate de mine (Ciprian), cu corecturile
# discutate. Comparatie cu main.py al profului:
#   - Cerinta 2: la profu' localitatile cu 0 angajati raman cu NaN (celule
#     goale in CSV), desi cerinta zice "procentele vor fi 0" -> aici fillna(0).
#   - Cerinta 3: coloana se numeste "Ponderi" (cum cere PDF-ul), nu "Totaluri".
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out_ciprian", exist_ok=True)

df_industrie = pd.read_csv("data_in/IndustriaAlimentara.csv", index_col=0)    # index = Siruta
activitati = list(df_industrie.columns.values[1:])                             # fara "Localitate"

# ---------------------------------------------------------------------
# Cerinta 1 - localitatile cu numar total de angajati > 0     (1372 randuri)
# ---------------------------------------------------------------------
totaluri = df_industrie[activitati].sum(axis=1)          # total pe RAND (localitate)
df_cerinta1 = df_industrie[totaluri > 0]                 # filtrare cu masca
df_cerinta1.to_csv("data_out_ciprian/Cerinta1.csv")

# ---------------------------------------------------------------------
# Cerinta 2 - procentul pe activitate, la nivel de localitate
# Gilau (57902): Carne 80 / total 90 * 100 = 88.89%
# ---------------------------------------------------------------------
df_cerinta2 = df_industrie[activitati].apply(func=lambda x: x * 100 / x.sum(), axis=1)
df_cerinta2 = df_cerinta2.fillna(0)                      # 0/0 = NaN -> 0 (ATRIBUIRE!)
df_cerinta2.insert(0, "Localitate", df_industrie["Localitate"])
df_cerinta2.to_csv("data_out_ciprian/Cerinta2.csv")

# ---------------------------------------------------------------------
# Cerinta 3 - judetele sortate desc. dupa ponderea angajatilor in populatie
# Cluj: 5632 angajati / 722438 locuitori = 0.0078
# REGULA: aduni BRUTELE pe judet, abia apoi imparti (nu media ponderilor!)
# ---------------------------------------------------------------------
df_industrie["Total"] = totaluri
df_populatie = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)    # index_col=0 OBLIGATORIU
df_merge = df_industrie.merge(df_populatie, left_index=True, right_index=True)
print(df_merge.shape)                                     # (3181, 12)

df_judete = df_merge[["Judet", "Total", "Populatie"]].groupby("Judet").sum()
s_cerinta3 = df_judete["Total"] / df_judete["Populatie"]
s_cerinta3 = s_cerinta3.sort_values(ascending=False)     # ATRIBUIRE!
s_cerinta3.name = "Ponderi"
s_cerinta3.to_csv("data_out_ciprian/Cerinta3.csv")               # if,0.017788851398883143 primul

# ---------------------------------------------------------------------
# Cerinta 4 - activitatea cu cei mai multi angajati, pe judet
# ab -> Carne, cj -> Panificatie
# ---------------------------------------------------------------------
df_judete_act = df_merge[activitati + ["Judet"]].groupby("Judet").sum()
s_cerinta4 = df_judete_act.idxmax(axis=1)                # ETICHETA coloanei cu maximul, pe rand
s_cerinta4.name = "Activitate"
s_cerinta4.to_csv("data_out_ciprian/Cerinta4.csv")
