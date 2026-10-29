# =====================================================================
# TEST S2 (1091) - PIB-ul tarilor europene 1995-2021
# Date: data_in/gdp.csv, data_in/populatie.csv
#
# ATENTIE: fisierele de date NU au venit cu enuntul. Rezolvarea e scrisa pe
# structura dedusa din exemplele din enunt:
#   gdp.csv        -> CODE, Country, 1995, 1996, ..., 2021   (PIB in MILIOANE de euro)
#   populatie.csv  -> CODE, <nume tara>, <populatie>, <zona euro>, <regiune>
# Cand ai fisierele: print(df_pop.columns) si ajusteaza cele 3 nume de mai jos.
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_gdp = pd.read_csv("data_in/gdp.csv", index_col=0)          # index = CODE (BE, BG, CZ...)
ani = list(df_gdp.columns.values[1:])                         # '1995' ... '2021' (ca TEXT!)

df_pop = pd.read_csv("data_in/populatie.csv", index_col=0)    # index = CODE
print(df_pop.columns)                                         # <- verifica numele coloanelor!
COL_TARA = "COUNTRY"        # numele tarii (exemplele 2 si 3 au header-ul COUNTRY)
COL_POPULATIE = "POPULATION"
COL_REGIUNE = "REGION"


# =====================================================================
# CERINTA 1 - PIB-ul mediu pe tara, 1995-2021                  (1 punct)
# media pe RAND (pe ani) -> mean(axis=1)
# Belgium: (PIB 1995 + ... + PIB 2021) / 27 = 344422.97
# =====================================================================
df_output1 = df_gdp[["Country"]].copy()
df_output1["PIB Mediu"] = df_gdp[ani].mean(axis=1)
df_output1.to_csv("data_out/Output1.csv")


# =====================================================================
# CERINTA 2 - PIB pe locuitor, pe fiecare an, in EURO/locuitor  (2 puncte)
# CAPCANA - unitati: PIB-ul e in MILIOANE de euro -> * 1_000_000
#   Belgium 1995: PIB (mil. EUR) * 1e6 / populatie = 20021.702
# Populatia e in alt fisier -> merge dupa CODE (index in ambele).
# div(..., axis=0): impart FIECARE coloana (an) la populatia de pe acelasi RAND.
# =====================================================================
df_merge = df_gdp.merge(df_pop, left_index=True, right_index=True)
print("Shape dupa merge:", df_merge.shape)

df_pib_loc = df_merge[ani].mul(1_000_000).div(df_merge[COL_POPULATIE], axis=0)

df_output2 = df_pib_loc.copy()
df_output2.insert(0, "COUNTRY", df_merge[COL_TARA])
df_output2.round(3).to_csv("data_out/Output2.csv")        # exemplul e cu 3 zecimale

# Daca populatia ar fi PE ANI (coloane 1995..2021 si in populatie.csv), ar fi
#   df_merge[ani] / df_pop[ani]   (impartire element cu element, aliniata dupa CODE si an)


# =====================================================================
# CERINTA 3 - anul cu cel mai MIC PIB pentru fiecare tara        (2 puncte)
# -> idxmin(axis=1): pe fiecare rand, NUMELE coloanei (anul) cu minimul
# Belgium -> 1996
# =====================================================================
df_output3 = pd.DataFrame({
    "COUNTRY": df_merge[COL_TARA],
    "ANUL": df_merge[ani].idxmin(axis=1),
})
df_output3.to_csv("data_out/Output3.csv")


# =====================================================================
# CERINTA 4 - PIB-ul pe fiecare an, la nivel de regiune          (2 puncte)
# PIB-ul regiunii = SUMA PIB-urilor tarilor din regiune
# (exemplul: EasternE 1995 = 294850.2 -> e suma, nu media)
# =====================================================================
df_output4 = df_merge[ani + [COL_REGIUNE]].groupby(COL_REGIUNE).sum()
df_output4.index.name = "REGION"
df_output4.to_csv("data_out/Output4.csv")


# =====================================================================
# CERINTA 5 - tara cu cel mai mare PIB/locuitor, pe regiune si an (2 puncte)
# -> pe tabelul de la cerinta 2 (PIB/locuitor) adaug regiunea,
#    groupby(regiune).idxmax() -> pe fiecare regiune si an, INDEXUL randului
#    cu maximul = CODE-ul tarii (pentru ca indexul e CODE). Exact ce cere.
# EasternE -> SI (Slovenia) in toti anii
# =====================================================================
df_pib_loc[COL_REGIUNE] = df_merge[COL_REGIUNE]
df_output5 = df_pib_loc.groupby(COL_REGIUNE).idxmax()
df_output5.index.name = "REGION"
df_output5.to_csv("data_out/Output5.csv")
