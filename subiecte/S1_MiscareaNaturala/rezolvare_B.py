# =====================================================================
# REZOLVARE - Subiect S1 (MiscareaNaturala), partea B
# Analiza de clusteri prin metoda WARD pe cei 7 indicatori.
# (Capitol inca nefacut la seminar - aici ca referinta.)
# =====================================================================
# IDEEA IN 3 RANDURI:
#   - pornesti cu fiecare tara = un cluster (182 de clusteri)
#   - la fiecare pas unesti cei 2 clusteri "cei mai apropiati" (Ward = unirea care
#     creste cel mai putin varianta din interiorul clusterilor)
#   - dupa 181 de pasi ai un singur cluster; "partitia optimala" = unde te opresti
# =====================================================================

import os
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage

from functii import nan_replace_df, standardizare, tabelare_ierarhie, partitie
from grafice import plot_dendrograma, show

os.makedirs("data_out", exist_ok=True)

df = pd.read_csv("data_in/MiscareaNaturala.csv", index_col=0)
indicatori = list(df.columns.values[2:])
nan_replace_df(df)

# Standardizam: altfel MMR (sute) ar domina RS (unitati) in distante
x = standardizare(df[indicatori].values)


# ---------------------------------------------------------------------
# B1. Matricea ierarhie -> h.csv
#     linkage intoarce o matrice (n-1) x 4. Rand i = jonctiunea i:
#       [cluster 1, cluster 2, distanta, numar instante in clusterul nou]
# ---------------------------------------------------------------------
h = linkage(x, method="ward")
df_h = tabelare_ierarhie(h)
print(df_h.tail())
df_h.to_csv("data_out/h.csv")


# ---------------------------------------------------------------------
# B2. Dendrograma pentru partitia optimala
#     Partitia optimala = Elbow: cel mai mare salt intre distantele a doua
#     jonctiuni consecutive (vezi functia partitie din functii.py).
# ---------------------------------------------------------------------
k, prag, etichete = partitie(h)
print("Numar de clusteri in partitia optimala:", k)
plot_dendrograma(h, df["Three_Letter_Country_Code"].values, prag,
                 titlu="Dendrograma - partitia optimala (" + str(k) + " clusteri)")


# ---------------------------------------------------------------------
# B3. Componenta partitiei optimale -> popt.csv
#     Pentru fiecare tara: clusterul din care face parte.
# ---------------------------------------------------------------------
df_popt = pd.DataFrame({
    "Country": df["Country_Name"],
    "Code": df["Three_Letter_Country_Code"],
    "Cluster": etichete,
}, index=df.index)
df_popt.to_csv("data_out/popt.csv")
print(df_popt["Cluster"].value_counts())

show()
