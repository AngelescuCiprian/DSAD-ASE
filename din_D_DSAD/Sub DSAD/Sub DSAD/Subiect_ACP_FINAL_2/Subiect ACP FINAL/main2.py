import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

tabel_mort = pd.read_csv('./DateIN/Mortalitate.csv', index_col=0)
tabel_tari = pd.read_csv('./DateIN/CoduriTariExtins.csv', index_col=0)

tari = tabel_mort.index
variabile = tabel_mort.columns

# Cerinta 1
cerinta1 = tabel_mort.loc[tabel_mort['RS'] < 0, ['RS']]
cerinta1.to_csv('./dateOUT2/cerinta1.csv')

# Cerinta2 - valorile medii pt fiec indicator, la nivel de continent
tabel_merge = tabel_mort.merge(right=tabel_tari, left_index=True, right_index=True)

cerinta2 = tabel_merge.groupby(['Continent']).mean(numeric_only=True)
cerinta2.to_csv('./dateOUT2/cerinta2.csv')

# Cerinta3 -- variantele componentelor principale standardizate
x = tabel_mort[variabile].values
def standardizare(x):
    return (x - np.mean(x, axis=0)) / np.std(x, axis=0)
Xstd = standardizare(x)

model_acp = PCA()
model_acp.fit(Xstd)

alpha = model_acp.explained_variance_
print("Variante: ", alpha)

# Cerinta4 -- scorurile asociate instantelor
c = model_acp.transform(Xstd)

scoruri = c / np.sqrt(alpha)
etichete_componente = ["Componenta" + str(i+1) for i in range (len(alpha))]
scoruri_df = pd.DataFrame(data=scoruri, index=tari, columns=etichete_componente)
scoruri_df.to_csv('./dateOUT2/scoruri.csv')
