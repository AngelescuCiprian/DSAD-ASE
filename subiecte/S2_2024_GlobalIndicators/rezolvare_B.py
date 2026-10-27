# =====================================================================
# REZOLVARE - Subiect S2_2024 (GlobalIndicators), partea B
# Analiza de clusteri prin metoda WARD pe cei 14 indicatori macroeconomici.
# (Capitol inca nefacut la seminar - aici ca referinta.)
# =====================================================================

import os
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage
from sklearn.metrics import silhouette_samples

from functii import nan_replace_df, standardizare, tabelare_ierarhie, partitie
from grafice import plot_dendrograma, plot_histograme, show

os.makedirs("data_out", exist_ok=True)
pd.set_option("display.max_rows", 20)

df = pd.read_csv("data_in/GlobalIndicatorsPerCapita_2021.csv", index_col=0)
indicatori = list(df.columns.values[1:])
nan_replace_df(df)
x = standardizare(df[indicatori].values)


# ---------------------------------------------------------------------
# B1. Matricea ierarhie -> la CONSOLA (de data asta nu in fisier)
# ---------------------------------------------------------------------
h = linkage(x, method="ward")
print(tabelare_ierarhie(h))


# ---------------------------------------------------------------------
# B2. Partitia optimala dupa criteriul Elbow + scorul Silhouette al fiecarei
#     instante -> popt.csv, pe 4 coloane: cod, tara, cluster, silhouette
#
#     Silhouette (intre -1 si 1) pentru o instanta:
#       aproape de 1  -> e bine plasata in clusterul ei
#       aproape de 0  -> e la granita dintre doi clusteri
#       negativ       -> ar fi mai potrivita in alt cluster
# ---------------------------------------------------------------------
k, prag, etichete = partitie(h)
print("Numar de clusteri (Elbow):", k)

df_popt = pd.DataFrame({
    "Country": df["Country"],
    "Cluster": etichete,
    "Silhouette": silhouette_samples(x, etichete),
}, index=df.index)
df_popt.to_csv("data_out/popt.csv")
print(df_popt.head())
print(df_popt["Cluster"].value_counts())

plot_dendrograma(h, df["Country"].values, prag, titlu="Dendrograma - partitia optimala")


# ---------------------------------------------------------------------
# B3. Histograma pentru partitia optimala si variabila GNI
#     cate o histograma a lui GNI pentru fiecare cluster
# ---------------------------------------------------------------------
plot_histograme(df["GNI"].values, etichete, "GNI")
show()
