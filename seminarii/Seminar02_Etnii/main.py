import os

import numpy as np
import pandas as pd

from functii import nan_replace_df

pd.set_option('display.max_columns', None)
df_etnii=pd.read_csv("data_in/Ethnicity.csv",index_col=0)
#print(df_etnii,type(df_etnii),sep="\n")

etnii=list(df_etnii.columns.values[1:])
#print(etnii)


nan_replace_df(df_etnii)


df_coduri_loc=pd.read_csv("data_in/Coduri_Localitati.csv",index_col=0)

#jonctiue
df_etnii_loc=df_etnii.merge(df_coduri_loc,left_index=True,right_index=True)
#print(df_etnii_loc)

df_etnii_jud=df_etnii_loc[etnii+["County"]].groupby("County").sum()
os.makedirs("data_out", exist_ok=True)
df_etnii_jud.to_csv("data_out/Ethnicity_Jud.csv")

df_coduri_jud=pd.read_csv("data_in/Coduri_Judete.csv",index_col=0)
df_etnii_jud_reg=df_etnii_jud[etnii].merge(df_coduri_jud[["IndicativJudet","Regiune"]],left_index=True,right_on="IndicativJudet")
df_etnii_reg=df_etnii_jud_reg[etnii+["Regiune"]].groupby(by="Regiune").sum()
df_etnii_reg.to_csv("data_out/Ethnicity_Reg.csv")

df_etnii_p=df_etnii[etnii].apply(func= lambda x : x*100/x.sum(),axis=1)
df_etnii_p.insert(0,"City",df_etnii["City"])
df_etnii_p.to_csv("data_out/Ethnicity_P.csv")

#De calculat acasa la nivel de judet si regiune

#3. Să se calculeze și să se salveze indicii de segregare etnică la nivelul județelor dupa indicii:


