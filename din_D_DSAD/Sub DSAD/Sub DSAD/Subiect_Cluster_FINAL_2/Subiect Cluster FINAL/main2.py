import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as hclust

tabel_alcohol = pd.read_csv('./DateIN/alcohol.csv', index_col=0)
tabel_tari = pd.read_csv('./DateIN/CoduriTariExtins.csv', index_col=0)

tari = tabel_alcohol.index
variabile = tabel_alcohol.columns[1:]

# Cerinta1
def alcohol_medie(t):
    linie = t.values[1:]
    medie = np.mean(linie)
    return pd.Series(data=[t['Code'], medie], index=['Code', 'Media'])
cerinta1 = tabel_alcohol.apply(func=alcohol_medie, axis=1)
cerinta1.to_csv('./dataOUT2/cerinta1.csv', index=False)

# Cerinta2

tabel_merge = tabel_alcohol.merge(right=tabel_tari, right_index=True, left_index=True)

t = tabel_merge.groupby('Continent').mean(numeric_only=True)
def maxAvg(t):
    linie = t.values
    max_pe_linie = np.argmax(linie)
    return pd.Series(data=[t.index[max_pe_linie]], index=['Anul'])
cerinta2 = t.apply(func=maxAvg, axis=1)
cerinta2.to_csv('./dataOUT2/cerinta2.csv')

# Cerinta3 - afis console matrice ierarhie cu informatii privind jonctiunile facute
# pt fiec jonctiune - clusterii, distanta dintre cei doi clusteri, nr de instante in clusterul nou
x = tabel_alcohol[variabile].values
print(x)

# matrice ierarhie
h = hclust.linkage(x, 'ward')
print(h)

# nr de jonctiuni
p = len(tari) - 1
print("Numar de jonctiuni: ", p)

# dist maxima dintre clusteri
k_diff_max = np.argmax(h[1:, 2] - h[:(p - 1), 2])
print("Distanta maxima dintre doi clusteri: ", k_diff_max)

# nr clusteri
n = p - k_diff_max
print("Numar de clusteri: ", n)
