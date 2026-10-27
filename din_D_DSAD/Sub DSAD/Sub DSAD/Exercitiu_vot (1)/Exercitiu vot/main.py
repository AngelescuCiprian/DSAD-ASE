import numpy as np
import pandas as pd

coduri_localitati = pd.read_csv('./DateIN/Coduri_Localitati.csv', index_col=0)
coduri_localitati = coduri_localitati[['Localitate', 'Judet']]

vot_categorii_sex = pd.read_csv('./DateIN/Vot_Categorii_Sex.csv', index_col=0)

categorii = vot_categorii_sex.columns[1:].values
#Cerinta 1

def vot_minim(linie, categorii):
    min_index = np.argmin(linie[categorii])
    categorie = linie[categorii].index[min_index]

    localitate = linie['Localitate']

    #data = [localitate, categorie]
    data = []
    data.append(localitate)
    data.append(categorie)

    return pd.Series(data=data, index=['Localitate', 'Categorie'])

df_cerinta_1 = vot_categorii_sex.apply(func=vot_minim, categorii=categorii, axis=1)

df_cerinta_1.to_csv('./DateOUT/cerinta1.csv')


#Cerinta 2


df_cerinta_2 = vot_categorii_sex.merge(coduri_localitati, right_index=True, left_index=True).groupby(['Judet']).mean(numeric_only=True)

df_cerinta_2.to_csv('./DateOUT/cerinta2.csv')









