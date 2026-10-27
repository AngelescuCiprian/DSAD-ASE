import sys

import numpy as np
import pandas as pd

from grafice import plot_varianta

np.set_printoptions(precision=3,threshold=sys.maxsize,suppress=True)
from functii import nan_replace_df, acp, tabelare_varianta

df=pd.read_csv('data_in/ConsumAlimentar/ConsumAlimentar.csv',index_col=1)
variabile_observate=list(df.columns.values[1:])
nan_replace_df(df)
x=df[variabile_observate].values
#print(x)
x_,r_v,alpha,a,c,r=acp(x)

#Tabelare varianta
df_varianta=tabelare_varianta(alpha)
df_varianta.round(3).to_csv('data_out/Varianta.csv')
plot_varianta(alpha)