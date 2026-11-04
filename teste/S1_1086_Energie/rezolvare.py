# =====================================================================
# TEST grupa 1086 - Coeficienti de localizare in industria energetica, pe judete
# Date: data_in/EnergLoc.csv (Judet + 8 coduri CAEN), data_in/RO_NUTS.csv
# Datele sunt deja la nivel de JUDET -> un singur merge, fara populatie
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_energ = pd.read_csv("data_in/EnergLoc.csv", index_col=0)          # index = Judet (dj, ms, ...)
activitati = list(df_energ.columns.values)       # TOATE coloanele sunt numerice (Judet e deja index)
# ['c3511', 'c3512', 'c3513', 'c3514', 'c3521', 'c3522', 'c3523', 'c3530']
df_nuts = pd.read_csv("data_in/RO_NUTS.csv", index_col=0)            # index = IndicativJudet


# =====================================================================
# CERINTA 1 - judetele cu coeficientul MEDIU (pe cele 8 activitati) > 1  (2p)
# media pe RAND -> mean(axis=1), apoi filtrare. Ordinea din fisier (fara sortare).
# dj: (7.7+0+4.138+1.795+0+0+0+4.77)/8 = 2.300375
# =====================================================================
s_medie = df_energ[activitati].mean(axis=1)
s_output1 = s_medie[s_medie > 1]
s_output1.name = "Coeficient mediu"
s_output1.to_csv("data_out/Output1.csv")


# =====================================================================
# CERINTA 2 - judetele in care activitatea cu coeficientul MAXIM e c3530;
# se salveaza coeficientul pentru c3530                              (2p)
# idxmax(axis=1) -> pe fiecare rand, NUMELE coloanei cu maximul
# [["c3530"]] cu paranteze duble -> DataFrame, ca sa ramana antetul "c3530"
# =====================================================================
s_dominanta = df_energ[activitati].idxmax(axis=1)
df_output2 = df_energ[s_dominanta == "c3530"][["c3530"]]
df_output2.to_csv("data_out/Output2.csv")


# =====================================================================
# CERINTA 3 - coeficientii de VARIATIE pe activitate, la nivel de regiune  (3p)
#   CV = abaterea standard / media, calculate pe judetele din regiune
# pandas .std() are implicit ddof=1 (abaterea standard de selectie) -> asta da exemplul
#   B-Ilfov, c3511: b=1.277, if=0.445 -> media 0.861, std 0.588 -> CV 0.683
# =====================================================================
df_merge = df_energ.merge(df_nuts[["Regiune"]], left_index=True, right_index=True)   # index-index

g = df_merge[activitati + ["Regiune"]].groupby("Regiune")
df_output3 = g.std() / g.mean()
# varianta cu functie: groupby("Regiune").apply(lambda t: t.std() / t.mean(), include_groups=False)
df_output3.round(3).to_csv("data_out/Output3.csv")


# =====================================================================
# CERINTA 4 - pentru fiecare regiune, judetul cu coeficientul maxim
# pe fiecare activitate                                              (2p)
# groupby(...).idxmax() -> pe fiecare coloana, INDEXUL (judetul) cu maximul
# =====================================================================
df_output4 = df_merge[activitati + ["Regiune"]].groupby("Regiune").idxmax()
df_output4.to_csv("data_out/Output4.csv")
