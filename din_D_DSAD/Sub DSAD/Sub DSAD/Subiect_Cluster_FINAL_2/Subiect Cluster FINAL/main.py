import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as hclust
import seaborn as sb
from sklearn.decomposition import PCA

alcohol = pd.read_csv('./DateIN/alcohol.csv', index_col=0)
coduri_tari_extins = pd.read_csv('./DateIN/CoduriTariExtins.csv', index_col=0)

tari = alcohol.index
variabile = alcohol.columns[1:]


# Cerinta 1


def calcul_medie(linie):
    cod = linie['Code']

    valori = linie[1:]

    medie = np.mean(valori)

    data = [cod, medie]

    return pd.Series(data=data, index=['Cod', 'Medie'])


df_cerinta_1 = alcohol.apply(func=calcul_medie, axis=1)

df_cerinta_1.to_csv('./DateOUT/cerinta1.csv', index=False)

# Cerinta 2

df_merged = alcohol.merge(coduri_tari_extins, right_index=True, left_index=True)
df_grouped_continent_medie = df_merged.groupby(['Continent']).mean(numeric_only=True)


def calcul_min_medie(linie):
    index_min = np.argmin(linie)

    return pd.Series(data=linie.index[index_min], index=['Anul'])


df_cerinta_2 = df_grouped_continent_medie.apply(func=calcul_min_medie, axis=1)

df_cerinta_2.to_csv('./DateOUT/cerinta2.csv')

# Cerinta 3


x = alcohol[variabile].values
print(x)


def change_nan(x):
    is_nan = np.isnan(x)
    k_nan = np.where(is_nan)

    x[k_nan] = np.nanmean(x[:, k_nan[1]], axis=0)


change_nan(x)

metoda = 'ward'
h = hclust.linkage(x, metoda)

print(h)

# nr de jonctiuni
p = len(tari) - 1

# distanta maxima intre 2 clusteri
k_diff_max = np.argmax(h[1:, 2] - h[:(p - 1), 2])

# nr clusteri
nr_clusteri = p - k_diff_max


# Cerinta 4


def dendograma(h, prag, tari):
    fig = plt.figure('Dendograma partitie optimala', figsize=(9, 9))
    ax = fig.add_subplot(1, 1, 1)

    hclust.dendrogram(h, color_threshold=prag, labels=tari, ax=ax)


def partitie(h, nr_clusteri, p, tari):
    k_diff_max = p - nr_clusteri
    prag = (h[k_diff_max, 2] + h[k_diff_max + 1, 2]) / 2

    dendograma(h, prag, tari)

    n = p + 1
    c = np.arange(n)

    for i in range(n - nr_clusteri):
        k1 = h[i, 0]
        k2 = h[i, 1]

        c[c == k1] = n + i
        c[c == k2] = n + i

    coduri = pd.Categorical(c).codes
    return np.array(["c" + str(cod + 1) for cod in coduri])


partitie_optimala = partitie(h, nr_clusteri, p, tari)
plt.show()

# Cerinta 5

df_cerinta_5 = pd.DataFrame(data={"Tari": tari,
                                  "Cluster": partitie_optimala})

df_cerinta_5.to_csv('./DateOUT/popt.csv', index=False)


# Cerinta 6 - plot partitie in axe principale

def plot_partitie(z, paritie_optimala):
    fig = plt.figure('Plot partitie optimala in axele principale', figsize=(9, 9))
    ax = fig.add_subplot(1, 1, 1)

    sb.scatterplot(x=z[:, 0], y=z[:, 1], hue=paritie_optimala, hue_order=np.unique(partitie_optimala), ax=ax)


model_pca = PCA(2)
z = model_pca.fit_transform(x)

plot_partitie(z, partitie_optimala)
plt.show()


