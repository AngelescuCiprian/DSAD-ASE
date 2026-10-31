# =====================================================================
# PRACTICA P3 - Numarul de someri pe localitati, 2015-2023
# Date: data_in/Somaj.csv (date de TEST generate), data_in/PopulatieLocalitati.csv
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_somaj = pd.read_csv("data_in/Somaj.csv", index_col=0)                    # index = Siruta
ani = list(df_somaj.columns.values[1:])                                      # '2015' ... '2023'
df_pop = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)        # Siruta, Localitate, Judet, Populatie


# =====================================================================
# CERINTA 1 - numarul mediu de someri pe localitate, descrescator      (1p)
# =====================================================================
df_output1 = df_somaj[["Localitate"]].copy()
df_output1["Medie"] = df_somaj[ani].mean(axis=1)
df_output1 = df_output1.sort_values(by="Medie", ascending=False)
df_output1.to_csv("data_out/Output1.csv")


# =====================================================================
# CERINTA 2 - anul cu cei mai multi someri pe localitate, fara localitatile
# care nu au avut niciun somer in toata perioada                        (2p)
# CAPCANA: pe un rand numai cu 0, idxmax da primul an (2015) -> filtrezi INAINTE
# =====================================================================
df_cu_someri = df_somaj[df_somaj[ani].sum(axis=1) > 0]
df_output2 = df_cu_someri[["Localitate"]].copy()
df_output2["Anul"] = df_cu_someri[ani].idxmax(axis=1)
df_output2.to_csv("data_out/Output2.csv")


# =====================================================================
# CERINTA 3 - rata somajului in 2023 pe localitate (someri 2023 / populatie),
# descrescator                                                          (2p)
# -> merge dupa Siruta + raport + sortare
# =====================================================================
df_merge = df_somaj.merge(df_pop[["Judet", "Populatie"]], left_index=True, right_index=True)
print("Shape dupa merge:", df_merge.shape)

df_output3 = df_merge[["Localitate"]].copy()
df_output3["Rata2023"] = df_merge["2023"] / df_merge["Populatie"]
df_output3 = df_output3.sort_values(by="Rata2023", ascending=False)
df_output3.to_csv("data_out/Output3.csv")


# =====================================================================
# CERINTA 4 - rata somajului pe judet pentru fiecare an + rata medie,
# descrescator dupa rata medie                                          (2p)
# REGULA: aduni BRUTELE pe judet (someri pe fiecare an + populatia), apoi imparti
# div(..., axis=0): fiecare an impartit la populatia judetului de pe acelasi rand
# (exact tiparul din subiectul E_NSAL)
# =====================================================================
df_judete = df_merge[ani + ["Populatie", "Judet"]].groupby("Judet").sum()
df_rata = df_judete[ani].div(df_judete["Populatie"], axis=0)
df_rata["RataMedie"] = df_rata[ani].mean(axis=1)
df_output4 = df_rata.sort_values(by="RataMedie", ascending=False)
df_output4.to_csv("data_out/Output4.csv")


# =====================================================================
# CERINTA 5 - pe judet, anul cu cea mai MICA rata a somajului          (2p)
# -> idxmin(axis=1) pe tabelul de rate (doar coloanele ani, fara RataMedie!)
# =====================================================================
s_output5 = df_rata[ani].idxmin(axis=1)
s_output5.name = "AnulMinim"
s_output5.to_csv("data_out/Output5.csv")
