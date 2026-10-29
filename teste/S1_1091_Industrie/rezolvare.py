# =====================================================================
# TEST S1 (1091) - Cifra de afaceri industriala pe localitati
# Date: data_in/Industrie.csv, data_in/PopulatieLocalitati.csv
# Toate cele 5 cerinte sunt verificate pe exemplele din enunt.
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_industrie = pd.read_csv("data_in/Industrie.csv", index_col=0)               # index = Siruta
activitati = list(df_industrie.columns.values[1:])
# ['Alimentara', 'Textila', 'Lemnului', 'ChimicaFarmaceutica', 'Metalurgica',
#  'ConstructiiMasini', 'CalculatoareElectronica', 'Mobila', 'Energetica']

df_populatie = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)     # Siruta, Localitate, Judet, Populatie


# =====================================================================
# CERINTA 1 - cifra de afaceri totala pe localitate          (1 punct)
# Cojocna (57350): suma celor 9 activitati = 1685412.0
# -> sum(axis=1), ca totalul de angajati de la seminarul 3
# =====================================================================
cifra_afaceri = df_industrie[activitati].sum(axis=1)

df_output1 = df_industrie[["Localitate"]].copy()
df_output1["Cifra de afaceri"] = cifra_afaceri
df_output1.to_csv("data_out/Output1.csv")
# Siruta,Localitate,Cifra de afaceri / 32768,Budesti,0.0 / 57350,Cojocna,1685412.0  OK


# =====================================================================
# CERINTA 2 - cifra de afaceri PE LOCUITOR, descrescator     (2 puncte)
# Populatia e in alt fisier -> MERGE (Siruta e index in ambele)
# Oras Mioveni (13301): cifra de afaceri totala / populatie = 586069.35
# =====================================================================
df_merge = df_industrie.merge(df_populatie[["Judet", "Populatie"]], left_index=True, right_index=True)
print("Shape dupa merge:", df_merge.shape)       # (3181, 12) - nicio localitate pierduta

df_output2 = df_industrie[["Localitate"]].copy()
df_output2["CF/Loc"] = cifra_afaceri / df_merge["Populatie"]      # se aliniaza dupa Siruta
df_output2 = df_output2.sort_values(by="CF/Loc", ascending=False)  # ATRIBUIRE!
df_output2.to_csv("data_out/Output2.csv")
# 13301,Oras Mioveni,586069.3455250441 / 40214,Oras Ghimbav,437357.66 / 40900,Cristian,360546.92  OK


# =====================================================================
# CERINTA 3 - activitatea cu cifra de afaceri maxima pe localitate,
#             FARA localitatile cu cifra de afaceri totala 0   (2 puncte)
# Cojocna -> Alimentara
# CAPCANA: pe un rand cu toate valorile 0, idxmax intoarce PRIMA coloana
#          (Alimentara) -> de-asta filtrezi INAINTE localitatile cu total 0.
#          Raman 2316 localitati.
# =====================================================================
df_cu_activitate = df_industrie[cifra_afaceri > 0]

df_output3 = df_cu_activitate[["Localitate"]].copy()
df_output3["Activitate"] = df_cu_activitate[activitati].idxmax(axis=1)
df_output3.to_csv("data_out/Output3.csv")
# 57350,Cojocna,Alimentara / 90119,Lunca Cernii De Jos,Lemnului / 73736,Poiana Mare,Alimentara  OK


# =====================================================================
# CERINTA 4 - cifra de afaceri pe fiecare activitate, pe judet  (2 puncte)
# -> groupby("Judet").sum() pe activitati
# In exemplu judetul e cu litere MARI (AB), in date e cu litere mici (ab)
# -> .str.upper() pe index
# =====================================================================
df_output4 = df_merge[activitati + ["Judet"]].groupby("Judet").sum()
df_output4.index = df_output4.index.str.upper()
df_output4.to_csv("data_out/Output4.csv")
# AB,1426022767.0,404955702.0,3749416915.0,...  OK


# =====================================================================
# CERINTA 5 - cifra de afaceri totala PE LOCUITOR, pe judet, descrescator (2 puncte)
# REGULA (seminarul 3): aduni BRUTELE pe judet (cifra de afaceri si populatia),
#                       abia apoi imparti. NU media cifrelor pe locuitor ale localitatilor!
# AG: cifra de afaceri totala AG / populatia AG = 42819.77
# =====================================================================
df_merge["Total"] = cifra_afaceri
df_judete = df_merge[["Judet", "Total", "Populatie"]].groupby("Judet").sum()

s_output5 = df_judete["Total"] / df_judete["Populatie"]
s_output5 = s_output5.sort_values(ascending=False)
s_output5.index = s_output5.index.str.upper()
s_output5.name = "CA/Loc"
s_output5.round(3).to_csv("data_out/Output5.csv")       # exemplul e cu 3 zecimale
# AG,42819.77 / B,27433.928 / TM,23958.813  OK
