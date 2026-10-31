# =====================================================================
# PRACTICA P1 - Structura votantilor pe sex si varsta
# Date: data_in/Vot_Categorii_Sex.csv, data_in/Coduri_Localitati.csv
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_vot = pd.read_csv("data_in/Vot_Categorii_Sex.csv", index_col=0)          # index = Siruta
categorii = list(df_vot.columns.values[1:])
barbati = [c for c in categorii if c.startswith("Barbati")]                # cele 4 categorii de barbati
femei = [c for c in categorii if c.startswith("Femei")]

df_coduri = pd.read_csv("data_in/Coduri_Localitati.csv", index_col=0)      # Siruta, Localitate_X, Judet, Localitate


# =====================================================================
# CERINTA 1 - procentul total de barbati si de femei pe localitate   (1p)
# Alba Iulia: Barbati = 1.216+4.003+20.099+27.976 = 53.294
#             Femei   = 28.941+4.172+1.413+10.669 = 45.195
# -> sum(axis=1) pe un SUBSET de coloane
# =====================================================================
df_output1 = df_vot[["Localitate"]].copy()
df_output1["Barbati"] = df_vot[barbati].sum(axis=1)
df_output1["Femei"] = df_vot[femei].sum(axis=1)
df_output1.to_csv("data_out/Output1.csv")


# =====================================================================
# CERINTA 2 - localitatile unde procentul femeilor e mai mare decat al
# barbatilor, descrescator dupa diferenta Femei - Barbati            (2p)
# -> coloana noua + filtrare + sortare (cu ATRIBUIRE)
# =====================================================================
df_output2 = df_output1.copy()
df_output2["Diferenta"] = df_output2["Femei"] - df_output2["Barbati"]
df_output2 = df_output2[df_output2["Diferenta"] > 0]
df_output2 = df_output2.sort_values(by="Diferenta", ascending=False)
df_output2.to_csv("data_out/Output2.csv")


# =====================================================================
# CERINTA 3 - categoria cu cel mai mare procent pe localitate        (2p)
# Alba Iulia -> Femei_18-24 (28.941)
# -> idxmax(axis=1): NUMELE coloanei cu maximul, pe fiecare rand
# =====================================================================
df_output3 = df_vot[["Localitate"]].copy()
df_output3["Categorie"] = df_vot[categorii].idxmax(axis=1)
df_output3.to_csv("data_out/Output3.csv")


# =====================================================================
# CERINTA 4 - media procentelor pe judet, pentru fiecare categorie   (2p)
# -> merge (doar coloana Judet!) + groupby mean
# CAPCANA: Coduri_Localitati are si ea o coloana "Localitate" -> iei doar [["Judet"]]
# OBSERVATIE: o localitate din Vot nu exista in Coduri -> dupa merge raman 3180 din 3181
# =====================================================================
df_merge = df_vot.merge(df_coduri[["Judet"]], left_index=True, right_index=True)
print("Shape dupa merge:", df_merge.shape)                       # (3180, 10)

df_output4 = df_merge[categorii + ["Judet"]].groupby("Judet").mean()
df_output4.to_csv("data_out/Output4.csv")


# =====================================================================
# CERINTA 5 - pe judet, localitatea cu cel mai mare procent de TINERI
# (Barbati_18-24 + Femei_18-24) si valoarea acestuia                 (2p)
# PASI:
#   1. coloana "Tineri" pe localitate (suma a 2 coloane)
#   2. groupby("Judet")["Tineri"].idxmax() -> Siruta localitatii cu maximul
#   3. din Siruta iei numele si valoarea cu .loc
# =====================================================================
df_merge["Tineri"] = df_merge["Barbati_18-24"] + df_merge["Femei_18-24"]
siruta_max = df_merge.groupby("Judet")["Tineri"].idxmax()        # Series: judet -> Siruta

df_output5 = pd.DataFrame({
    "Localitate": df_merge.loc[siruta_max.values, "Localitate"].values,
    "Tineri": df_merge.loc[siruta_max.values, "Tineri"].values,
}, index=siruta_max.index)
df_output5.to_csv("data_out/Output5.csv")
