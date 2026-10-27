import numpy as np
import pandas as pd
import factor_analyzer as fact

tabel_vot = pd.read_csv('./DateIN/VotBUN.csv', index_col=0)
tabel_localitati_jud = pd.read_csv('./DateIN/Coduri_Localitati.csv', index_col=0)

variabile = tabel_vot.columns[1:]
coduri_siruta = tabel_vot.index

# Cerinta1
def votMin(t):
    linie = t.values
    min_pe_linie = np.argmin(linie)
    localitate = tabel_vot.at[t.name, 'Localitate']
    return pd.Series(data=[localitate, t.index[min_pe_linie]], index=['Localitate', 'Categorie'])
cerinta1 = tabel_vot[variabile].apply(func=votMin, axis=1)
print(cerinta1)
cerinta1.to_csv('./dataOUT2/cerinta1.csv')

# Cerinta2
tabel_merge = tabel_vot.merge(right=tabel_localitati_jud, left_index=True, right_index=True)
print(tabel_merge)

cerinta2 =  tabel_merge.groupby('Judet').mean(numeric_only=True)
print(cerinta2)
cerinta2.to_csv('./dataOUT2/cerinta2.csv')

# Cerinta3 -- aplicare Test Bartlett + afisare p-value
x = tabel_vot[variabile].values

bartlett = fact.calculate_bartlett_sphericity(x)
print("P-value: ", bartlett[1])
# index_kmo = fact.calculate_kmo(x)
# print(index_kmo)

# Cerinta4 -- scoruri factoriale
model_af = fact.FactorAnalyzer(len(variabile), rotation=None)
model_af.fit(x)

scoruri = model_af.transform(x)
coloane = ["F" + str(i+1) for i in range(len(variabile))]
scoruri_df = pd.DataFrame(data=scoruri, index=coduri_siruta, columns=coloane)
print(scoruri_df)
