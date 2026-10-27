# =====================================================================
# REZOLVARE - Subiect S2 (Emissions), partea A
# Date: data_in/Emissions.csv, data_in/PopulatieEuropa.csv
# =====================================================================

import os
import numpy as np
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_emisii = pd.read_csv("data_in/Emissions.csv", index_col=0)     # index = CountryCode (AUT, BEL...)
emisii = list(df_emisii.columns.values[1:])
# ['AirEmiss', 'Sulphur', 'Nitrogen', 'Ammonia', 'NonMeth', 'Partic', 'GreenGE', 'GreenGIE']


# =====================================================================
# CERINTA 1
# Emisiile TOTALE pe tara, exprimate in TONE.
# ---------------------------------------------------------------------
# CAPCANA - unitatile de masura:
#   Toate coloanele sunt in tone, MAI PUTIN GreenGE si GreenGIE, care sunt in
#   MII de tone -> le inmultesti cu 1000 inainte sa aduni.
#
# CALCUL DE MANA - Austria:
#   AirEmiss 272674.87 + Sulphur 418.6 + Nitrogen 1440.98 + Ammonia 27.48
#   + NonMeth 149.98 + Partic 161.58                         = 274873.49 t
#   GreenGE  1802.84 mii t * 1000                            = 1802840 t
#   GreenGIE  375.93 mii t * 1000                            =  375930 t
#   TOTAL                                                    = 2453643.49 t  (ca in exemplu)
#   Daca uitai *1000 ti-ar fi iesit 277052.26 -> GRESIT.
# =====================================================================
df_tone = df_emisii[emisii].copy()                 # copie, ca sa nu stric tabelul original
df_tone["GreenGE"] = df_tone["GreenGE"] * 1000
df_tone["GreenGIE"] = df_tone["GreenGIE"] * 1000

df_cerinta1 = df_emisii[["Country"]].copy()
df_cerinta1["Emisii_total_tone"] = df_tone.sum(axis=1)
print("Cerinta 1:\n", df_cerinta1.head(3))
df_cerinta1.to_csv("data_out/Cerinta1.csv")       # index = CountryCode -> prima coloana, ca in exemplu


# =====================================================================
# CERINTA 2
# Media PONDERATA a fiecarui tip de emisie, pe REGIUNE, cu ponderea =
# populatia tarilor. Coloanele GreenGE/GreenGIE se salveaza tot in tone
# (GreenGE_tone, GreenGIE_tone).
# ---------------------------------------------------------------------
# CE E MEDIA PONDERATA:
#   media simpla:     (x1 + x2) / 2
#   media ponderata:  (x1*p1 + x2*p2) / (p1 + p2)
#   -> tarile mari (populatie mare) "trag" mai tare de medie.
#
# CALCUL DE MANA - regiunea British (2 tari in Emissions):
#   GBR: AirEmiss 835646.72, populatia 67736802
#   IRL: AirEmiss 923406.87, populatia  5056935
#   media ponderata = (835646.72*67736802 + 923406.87*5056935) / (67736802 + 5056935)
#                   = 841743.36    (ca in exemplu)
#   media SIMPLA ar fi fost (835646.72 + 923406.87)/2 = 879526.80 -> GRESIT
#
# IDEEA IN COD (ca la seminarul 3, cerinta 5 a profului):
#   - merge emisii (in tone) cu Region + Population, dupa codul de tara
#   - groupby("Region").apply(functie) unde functia primeste TOATE tarile
#     unei regiuni (un DataFrame!) si returneaza mediile ponderate
#   - np.average(..., weights=...) face exact formula de mai sus
# =====================================================================
df_populatie = pd.read_csv("data_in/PopulatieEuropa.csv", index_col=0)   # index = Code (AUT...)

df_merge = df_tone.merge(df_populatie[["Region", "Population"]], left_index=True, right_index=True)
print("Shape dupa merge:", df_merge.shape)        # (32, 10) - toate cele 32 de tari s-au potrivit


def medii_ponderate(t: pd.DataFrame):
    # t = toate tarile dintr-o regiune (fara coloana Region, datorita include_groups=False)
    medii = np.average(t[emisii], axis=0, weights=t["Population"])
    return pd.Series(medii, index=emisii)


df_cerinta2 = df_merge[emisii + ["Population", "Region"]].groupby("Region").apply(
    func=medii_ponderate, include_groups=False)
df_cerinta2 = df_cerinta2.rename(columns={"GreenGE": "GreenGE_tone", "GreenGIE": "GreenGIE_tone"})

print("Cerinta 2:\n", df_cerinta2.round(3))
df_cerinta2.round(3).to_csv("data_out/Cerinta2.csv")      # exemplul e cu 3 zecimale
# Verificare: British,841743.362,1773.152,2652.611,8.613,899.088,138.32,2530203.541,987810.377  OK
