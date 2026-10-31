# =====================================================================
# PRACTICA P2 - Consumul de alcool pe tari (litri alcool pur / locuitor / an)
# Date: data_in/Alcool.csv, data_in/CoduriTariExtins.csv
# =====================================================================

import os
import pandas as pd
from pandas.api.types import is_numeric_dtype

os.makedirs("data_out", exist_ok=True)


def nan_replace_df(df: pd.DataFrame):           # functia profului (seminarul 2)
    for col in df.columns:
        if df[col].isnull().any():
            if is_numeric_dtype(df[col]):
                df.fillna({col: df[col].mean()}, inplace=True)
            else:
                df.fillna({col: df[col].mode()[0]}, inplace=True)


df_alcool = pd.read_csv("data_in/Alcool.csv", index_col=0)      # index = Code (AFG, ALB...)
ani = list(df_alcool.columns.values[1:])                         # '2000', '2005', '2010', '2015', '2018'


# =====================================================================
# CERINTA 1 - consumul mediu pe tara, descrescator               (1p)
# CAPCANA: o valoare lipseste (2010) -> NaN-ul se inlocuieste cu media anului
#          (functia profului). Fara asta, mean() l-ar ignora pur si simplu.
# =====================================================================
print("NaN inainte:", df_alcool[ani].isna().sum().sum())        # 1
nan_replace_df(df_alcool)

df_output1 = df_alcool[["Country"]].copy()
df_output1["Consum mediu"] = df_alcool[ani].mean(axis=1)
df_output1 = df_output1.sort_values(by="Consum mediu", ascending=False)
df_output1.to_csv("data_out/Output1.csv")


# =====================================================================
# CERINTA 2 - anul cu consumul maxim pe tara                     (2p)
# -> idxmax(axis=1)
# =====================================================================
df_output2 = df_alcool[["Country"]].copy()
df_output2["Anul"] = df_alcool[ani].idxmax(axis=1)
df_output2.to_csv("data_out/Output2.csv")


# =====================================================================
# CERINTA 3 - tarile in care consumul a SCAZUT intre 2000 si 2018,
# cu scaderea (2000 - 2018), descrescator dupa scadere            (2p)
# -> coloana calculata + filtrare + sortare
# =====================================================================
df_output3 = df_alcool[["Country"]].copy()
df_output3["Scadere"] = df_alcool["2000"] - df_alcool["2018"]
df_output3 = df_output3[df_output3["Scadere"] > 0].sort_values(by="Scadere", ascending=False)
df_output3.to_csv("data_out/Output3.csv")


# =====================================================================
# CERINTA 4 - consumul mediu pe continent, pentru fiecare an      (2p)
# CAPCANA merge: in CoduriTariExtins, codul de 3 litere e a 3-a coloana
#                (Three_Letter_Country_Code) -> index_col=2
# =====================================================================
df_coduri = pd.read_csv("data_in/CoduriTariExtins.csv", index_col=2)
df_merge = df_alcool.merge(df_coduri[["Continent_Name"]], left_index=True, right_index=True)
print("Shape dupa merge:", df_merge.shape)                       # (187, 7) - toate tarile s-au potrivit

df_output4 = df_merge[ani + ["Continent_Name"]].groupby("Continent_Name").mean()
df_output4.to_csv("data_out/Output4.csv")


# =====================================================================
# CERINTA 5 - pe continent, TARA (nume) cu consumul maxim in fiecare an  (2p)
# -> groupby().idxmax() da CODUL tarii (indexul), apoi .map() il traduce in nume
#    (acelasi tipar ca S1, cerinta 2)
# =====================================================================
df_cod_max = df_merge[ani + ["Continent_Name"]].groupby("Continent_Name").idxmax()
df_output5 = df_cod_max.apply(lambda coloana: coloana.map(df_alcool["Country"]))
df_output5.to_csv("data_out/Output5.csv")
