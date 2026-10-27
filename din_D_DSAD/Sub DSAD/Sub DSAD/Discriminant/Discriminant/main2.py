import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split

tabel_invatare_testare = pd.read_csv('./dataIn/hernia.csv', index_col=0)

def nan_replace_t(t):
    assert isinstance(t, pd.DataFrame)
    for v in t.columns:
        if any(t[v].isna()):
            if is_numeric_dtype(t[v]):
                t[v].fillna(t[v].mean(), inplace=True)
            else:
                t[v].fillna(t[v].mode()[0], inplace=True)
nan_replace_t(tabel_invatare_testare)

variabile = tabel_invatare_testare.columns
predictori = variabile[:-1]
tinta = variabile[-1]

# Divizare in set de invatare si set de testare
x_train, x_test, y_train, y_test = train_test_split(tabel_invatare_testare[predictori], tabel_invatare_testare[tinta], test_size=0.4)

# Construire model liniar pentru ALD
model_ald = LinearDiscriminantAnalysis()
model_ald.fit(x_train, y_train)
clase = model_ald.classes_
q = len(clase)
n = len(x_train)
m = len(predictori)
nr_discriminatori = min(q - 1, m)
# Preluare scoruri discriminante pentru setul de testare
z = model_ald.transform(x_test)
tz = pd.DataFrame(data=z, index=x_test.index, columns=["Z" + str(i+1) for i in range(nr_discriminatori)])
tz.to_csv('./dataOut/z.csv')
