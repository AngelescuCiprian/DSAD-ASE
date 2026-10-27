import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sb

mortalitate = pd.read_csv('./DateIN/Mortalitate.csv', index_col=0)
coduri_tari_extins = pd.read_csv('./DateIN/CoduriTariExtins.csv', index_col=0)

tari = mortalitate.index
variabile = mortalitate.columns


#Cerinta 1
df_cerinta_1 = mortalitate.loc[mortalitate['RS'] < 0, ['RS']]

df_cerinta_1.to_csv('./DateOUT/cerinta1.csv')

#Cerinta 2
df_merged = mortalitate.merge(coduri_tari_extins, right_index=True, left_index=True)
df_cerinta_2 = df_merged.groupby(['Continent']).mean(numeric_only=True)

df_cerinta_2.to_csv('./DateOUT/cerinta2.csv')


#Cerinta 3

x = mortalitate[variabile].values

def standardizare(x):
    return (x - np.mean(x, axis=0)) / np.std(x, axis=0)

Xstd = standardizare(x)


model_pca = PCA()
model_pca.fit(Xstd)

alpha = model_pca.explained_variance_
print("Variante: ", alpha)

#Cerinta 4

c = model_pca.transform(Xstd)

scoruri = c / np.sqrt(alpha)

etichete_componente = ["Componenta" + str(i+1) for i in range(len(alpha))]

df_scoruri = pd.DataFrame(data=scoruri, index=tari, columns=etichete_componente)
df_scoruri.to_csv('./DateOUT/scoruri.csv')



#Cerinta 5
def plot_componente(x, var_x, var_y):
    fig = plt.figure('Plot scoruri in cele doua axe principale', figsize=(9, 9))
    ax = fig.add_subplot(1, 1, 1)

    #labels
    ax.set_xlabel(var_x)
    ax.set_ylabel(var_y)
    ax.set_title('Plot scoruri in cele doua axe principale')

    ax.scatter(x[var_x], x[var_y], color='r')

    for i in range(len(x)):
        ax.text(x[var_x].iloc[i], x[var_y].iloc[i], x.index[i])

plot_componente(df_scoruri, "Componenta1", "Componenta2")
plt.show()


#Cerinta 6 - corelatii factoriale + corelograma(corelatii)

r_x_c = np.corrcoef(Xstd, c, rowvar=False)[:len(alpha), len(alpha):]

df_r_x_c = pd.DataFrame(data=r_x_c, index=variabile, columns=etichete_componente)

def corelograma(x, vmin=-1):
    fig = plt.figure('Corelograma', figsize=(9, 9))
    ax = fig.add_subplot(1, 1, 1)

    ax_ = sb.heatmap(data=x, vmin=vmin, vmax=1, cmap='bwr', annot=True, ax=ax)

    ax_.set_xticklabels(x.columns, rotation=30)

corelograma(df_r_x_c)
plt.show()




#Cerinta 7 - calculati si printati la consola cosinusurile

c_patrat = c * c
cosinusuri = np.transpose(c_patrat.T / np.sum(c_patrat, axis=1))
print(cosinusuri)

#Cerinta 8 - calculati si printati la consola contributiile
contributii = c_patrat / np.sum(c_patrat, axis=0)
print(contributii)


#Cerinta 9 - comunalitatile si corelograma(comunalitati)
comunalitati = np.cumsum(r_x_c * r_x_c, axis=1)
df_comunalitati = pd.DataFrame(data=comunalitati, index=variabile, columns=etichete_componente)
corelograma(df_comunalitati, vmin=0)
plt.show()



