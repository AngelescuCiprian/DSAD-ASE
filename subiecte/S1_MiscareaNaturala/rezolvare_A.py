# =====================================================================
# REZOLVARE - Subiect S1 (MiscareaNaturala), partea A
# Date: data_in/MiscareaNaturala.csv, data_in/CoduriTariExtins.csv
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_miscare = pd.read_csv("data_in/MiscareaNaturala.csv", index_col=0)   # index = Country_Number
indicatori = list(df_miscare.columns.values[2:])                        # FR, IM, LE, LEF, LEM, MMR, RS


# =====================================================================
# CERINTA 1
# Tarile cu RS MAI MIC decat media globala a RS, in ordinea descrescatoare
# a lui RS. Se salveaza codul de tara, numele, RS.
# ---------------------------------------------------------------------
# CALCUL DE MANA:
#   media globala RS = suma RS a celor 182 de tari / 182 = 1.428
#   Malaysia  RS = 1.412 < 1.428 -> PASTRAT, si e PRIMUL (cel mai mare dintre cei sub medie)
#   Oman      RS = 6.773 > 1.428 -> ELIMINAT
#   Raman 100 de tari.
#
# DIFERENTA FATA DE S1_2023: pragul nu mai e 0, ci o valoare calculata (.mean()).
# =====================================================================
media_rs = df_miscare["RS"].mean()
print("Media globala RS:", media_rs)

df_cerinta1 = df_miscare[df_miscare["RS"] < media_rs][["Three_Letter_Country_Code", "Country_Name", "RS"]]
df_cerinta1 = df_cerinta1.sort_values(by="RS", ascending=False)
print("Cerinta 1:", df_cerinta1.shape)        # (100, 3), primul MYS 1.412
df_cerinta1.to_csv("data_out/Cerinta1.csv", index=False)


# =====================================================================
# CERINTA 2
# Pentru fiecare continent, CODUL (3 litere) al tarii cu valoarea maxima,
# pentru FIECARE indicator.
# Output: Continent_Name, FR, IM, LE, LEF, LEM, MMR, RS  (in celule: coduri de tara)
# ---------------------------------------------------------------------
# CALCUL DE MANA - Africa, indicatorul FR (fertilitatea):
#   dintre cele 52 de tari africane, maximul FR = 7.35 la Niger (Country_Number 562)
#   codul lui 562 = NER  -> in tabel, la Africa/FR scrie NER
#   (exemplul din subiect: Africa,NER,SLE,DZA,MUS,DZA,SLE,GNQ)
#
# IDEEA:
#   groupby(...).idxmax() da, pe fiecare grup si fiecare coloana, ETICHETA
#   (indexul = Country_Number) randului cu maximul. Exact ce faceam cu
#   idxmax la seminarul 3, doar ca acum pe grupuri.
#   Apoi traduci Country_Number -> cod de 3 litere cu .map().
#
# CAPCANA: daca folosesti argmax in loc de idxmax primesti POZITIA in grup
#   (0, 1, 2...), nu Country_Number -> traducerea iese gresita.
# =====================================================================
df_coduri = pd.read_csv("data_in/CoduriTariExtins.csv", index_col=3)    # Country_Number e a 4-a coloana
df_merge = df_miscare.merge(df_coduri[["Continent_Name"]], left_index=True, right_index=True)
print("Shape dupa merge:", df_merge.shape)    # (182, 10)

# 1. pe fiecare continent si indicator: Country_Number-ul tarii cu maximul
df_idmax = df_merge[indicatori + ["Continent_Name"]].groupby("Continent_Name").idxmax()

# 2. traduc fiecare Country_Number in codul de 3 litere
#    df_miscare["Three_Letter_Country_Code"] e o Series cu index = Country_Number -> perfecta pentru map
coduri_tari = df_miscare["Three_Letter_Country_Code"]
df_cerinta2 = df_idmax.apply(lambda coloana: coloana.map(coduri_tari))

print("Cerinta 2:\n", df_cerinta2)
df_cerinta2.to_csv("data_out/Cerinta2.csv")

# VARIANTA ALTERNATIVA (stilul profului, cu o functie aplicata pe fiecare grup):
#
# def tara_max(t: pd.DataFrame):
#     # t = toate tarile unui continent
#     return pd.Series({ind: t.loc[t[ind].idxmax(), "Three_Letter_Country_Code"] for ind in indicatori})
#
# df_cerinta2 = df_merge[indicatori + ["Three_Letter_Country_Code", "Continent_Name"]] \
#     .groupby("Continent_Name").apply(func=tara_max, include_groups=False)
