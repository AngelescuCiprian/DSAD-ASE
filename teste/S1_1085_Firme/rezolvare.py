# =====================================================================
# TEST S1 (1085) - Activitatea firmelor in 2014, pe localitati
# Date: data_in/I2014.csv (date de TEST generate), data_in/PopulatieLocalitati.csv
# =====================================================================

import os
import numpy as np
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_firme = pd.read_csv("data_in/I2014.csv", index_col=0)                 # index = Siruta
indicatori = list(df_firme.columns.values[1:])
# ['NrFirme', 'NrSal', 'TotalCifraAfaceri', 'TotalProfit', 'TotalPierdere']

df_pop = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)    # Siruta, Localitate, Judet, Populatie
df_merge = df_firme.merge(df_pop[["Judet", "Populatie"]], left_index=True, right_index=True)
print("Shape dupa merge:", df_merge.shape)                               # (3181, 8)


# =====================================================================
# CERINTA 1 - raportul CA / NrSal pentru localitatile CU salariati,
# descrescator                                                     (2 puncte)
# CAPCANA: "unde exista salariati" -> filtrezi NrSal > 0 INAINTE de impartire.
#          Altfel: CA / 0 = inf (sau 0/0 = NaN) si inf iese primul la sortare!
# Independenta: 305595398 / 125 = 2444763.184
# =====================================================================
df_cu_sal = df_firme[df_firme["NrSal"] > 0]

df_output1 = df_cu_sal[["DenLocalitate"]].copy()
df_output1["Raport CA/NrSal"] = df_cu_sal["TotalCifraAfaceri"] / df_cu_sal["NrSal"]
df_output1 = df_output1.sort_values(by="Raport CA/NrSal", ascending=False)
df_output1.to_csv("data_out/Output1.csv")


# =====================================================================
# CERINTA 2 - rata ocuparii = salariati la 1000 de locuitori, pe judet,
# descrescator                                                     (2 puncte)
# REGULA: aduni BRUTELE pe judet (NrSal si Populatie), apoi imparti, apoi * 1000
# B: 1082794 salariati / 2107399 locuitori * 1000 = 513.806
# Judetul e cu litere MARI in exemplu -> .str.upper()
# =====================================================================
df_judete = df_merge[["Judet", "NrSal", "Populatie"]].groupby("Judet").sum()
s_output2 = df_judete["NrSal"] / df_judete["Populatie"] * 1000
s_output2 = s_output2.sort_values(ascending=False)
s_output2.index = s_output2.index.str.upper()
s_output2.name = "Rata Ocuparii"
s_output2.to_csv("data_out/Output2.csv")


# =====================================================================
# CERINTA 3 - pe judet, localitatea cu cel mai mare PROFIT PE LOCUITOR  (2 puncte)
# PASI (tiparul de la P1 Vot, cerinta 5):
#   1. coloana ProfitLoc = TotalProfit / Populatie (pe localitate)
#   2. groupby("Judet")["ProfitLoc"].idxmax() -> Siruta localitatii cu maximul
#   3. .map() traduce Siruta in denumire
# AB -> Galda De Jos
# =====================================================================
df_merge["ProfitLoc"] = df_merge["TotalProfit"] / df_merge["Populatie"]
s_siruta = df_merge.groupby("Judet")["ProfitLoc"].idxmax()          # Series: judet -> Siruta

df_output3 = s_siruta.map(df_merge["DenLocalitate"]).to_frame(name="Localitate")
df_output3.index = df_output3.index.str.upper()
df_output3.to_csv("data_out/Output3.csv")


# =====================================================================
# CERINTA 4 - mediile PONDERATE ale celor 5 indicatori pe judet,
# ponderea = populatia localitatilor                               (3 puncte)
# media ponderata = (x1*p1 + x2*p2 + ...) / (p1 + p2 + ...)
# -> groupby + apply cu o functie care primeste TOATE localitatile unui judet
#    (ca la seminarul 3, cerinta 5, si la subiectul S2 Emissions)
# AB: 946.407, 5690.334, 1336997181.357, 113378467.612, 31730528.39
# =====================================================================
def medii_ponderate(t: pd.DataFrame):
    return pd.Series(np.average(t[indicatori], axis=0, weights=t["Populatie"]), index=indicatori)


df_output4 = df_merge[indicatori + ["Populatie", "Judet"]].groupby("Judet").apply(
    func=medii_ponderate, include_groups=False)
df_output4.index = df_output4.index.str.upper()
df_output4.round(3).to_csv("data_out/Output4.csv")        # exemplul e cu 3 zecimale
