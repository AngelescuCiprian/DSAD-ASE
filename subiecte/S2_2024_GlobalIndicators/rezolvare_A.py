# =====================================================================
# REZOLVARE - Subiect S2_2024 (GlobalIndicatorsPerCapita_2021), partea A
# Date: data_in/GlobalIndicatorsPerCapita_2021.csv, data_in/CoduriTari.csv
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_ind = pd.read_csv("data_in/GlobalIndicatorsPerCapita_2021.csv", index_col=0)   # index = CountryID
indicatori = list(df_ind.columns.values[1:])        # GNI ... Other (14 indicatori)

# Ramurile (valoarea adaugata) = ultimele 7 coloane: de la AgrHuntForFish la Other
ramuri = indicatori[7:]
# ['AgrHuntForFish', 'Construction', 'Manufacturing', 'MiningManUt', 'TradeT', 'TransportComm', 'Other']


# =====================================================================
# CERINTA 1
# Pentru fiecare tara, ramura cu valoarea adaugata cea mai mare.
# Output: CountryID, Country, Ramura Dominanta
# ---------------------------------------------------------------------
# CALCUL DE MANA - Afghanistan (CountryID 4):
#   AgrHuntForFish 124.746, Construction 7.484, Manufacturing 33.756,
#   MiningManUt 50.593, TradeT 38.961, TransportComm 36.689, Other 97.604
#   maximul = 124.746 -> pe coloana AgrHuntForFish  (ca in exemplu)
#
# IDEEA: idxmax(axis=1) -> pe fiecare RAND, ETICHETA coloanei cu maximul.
#        Identic cu cerinta 4 de la seminarul 3 (activitatea dominanta).
# CAPCANA: idxmax DOAR pe cele 7 ramuri. Daca il pui pe toti indicatorii,
#          castiga GNI aproape peste tot.
# =====================================================================
df_cerinta1 = df_ind[["Country"]].copy()
df_cerinta1["Ramura Dominanta"] = df_ind[ramuri].idxmax(axis=1)
print("Cerinta 1:\n", df_cerinta1.head(3))
df_cerinta1.to_csv("data_out/Cerinta1.csv")


# =====================================================================
# CERINTA 2
# Mediile indicatorilor (GNI ... Other) la nivel de continent.
# ---------------------------------------------------------------------
# IDEEA: merge cu CoduriTari (cheia CountryID e index in ambele) + groupby mean.
#
# OBSERVATIE: 4 tari din GlobalIndicators NU exista in CoduriTari
#   (412 Kosovo, 729 Sudan, 835 Tanzania Mainland, 836 Zanzibar).
#   merge-ul (inner, implicit) le elimina -> 208 randuri in loc de 212.
#   E corect: fara continent nu pot intra la niciun continent. Rezultatul
#   coincide cu exemplul din subiect (Africa,2417.27,...).
#
# CAPCANA: ambele fisiere au coloana "Country" -> ia din coduri doar [["Continent"]].
# =====================================================================
df_coduri = pd.read_csv("data_in/CoduriTari.csv", index_col=0)
df_merge = df_ind.merge(df_coduri[["Continent"]], left_index=True, right_index=True)
print("Shape dupa merge:", df_merge.shape)        # (208, 16)

df_cerinta2 = df_merge[indicatori + ["Continent"]].groupby("Continent").mean()
print("Cerinta 2:\n", df_cerinta2.round(2))
df_cerinta2.round(2).to_csv("data_out/Cerinta2.csv")    # exemplul e rotunjit la 2 zecimale
