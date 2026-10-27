import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import factor_analyzer as fact

vot = pd.read_csv('./DateIN/VotBUN.csv', index_col=0)
coduri_localitati = pd.read_csv('./DateIN/Coduri_Localitati.csv', index_col=0)


variabile = vot.columns[1:]
sirute = vot.index

#Cerinta 1

def vot_minim(linie):
    localitate = linie['Localitate']

    valori = linie[1:]

    index_min = np.argmin(valori)

    data = [localitate, valori.index[index_min]]

    return pd.Series(data=data, index=['Localitate', 'Categorie'])

df_cerinta_1 = vot.apply(func=vot_minim, axis=1)

df_cerinta_1.to_csv('./DateOUT/cerinta1.csv')

#Cerinta 2
df_merged = vot.merge(coduri_localitati, left_index=True, right_index=True)

df_grouped_judet = df_merged.groupby(['Judet']).mean(numeric_only=True)

df_grouped_judet.to_csv('./DateOUT/cerinta2.csv')


#Cerinta 3

x = vot[variabile].values

barlett = fact.calculate_bartlett_sphericity(x)
print("P-value:", barlett[1])

#Cerinta 4


model_af = fact.FactorAnalyzer(len(variabile), rotation=None)
model_af.fit(x)

scoruri = model_af.transform(x)

etichete_factori = ["F" + str(i + 1) for i in range(len(variabile))]

df_scoruri = pd.DataFrame(data=scoruri, index=sirute, columns=etichete_factori)
df_scoruri.to_csv('./DateOUT/f.csv')


#Cerinta 5

def plot_componente(x, var_x, var_y, sirute):
    fig = plt.figure('Graficul scorurilor factoriale pentru primii 2 factori', figsize=(9, 9))
    ax = fig.add_subplot(1, 1, 1)

    #labels
    ax.set_xlabel(var_x)
    ax.set_ylabel(var_y)

    ax.scatter(x[var_x], x[var_y], color='r')

    for i in range(len(x)):
        ax.text(x[var_x].iloc[i], x[var_y].iloc[i], sirute[i])

plot_componente(df_scoruri, 'F1', 'F2', sirute)
plt.show()