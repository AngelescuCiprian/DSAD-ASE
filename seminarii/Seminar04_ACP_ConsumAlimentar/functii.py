import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

def nan_replace_df(df: pd.DataFrame):
    for col in df.columns:
        if df[col].isnull().any():
            if is_numeric_dtype(df[col]):
                df.fillna({col: df[col].mean()}, inplace=True)
            else:
                df.fillna({col: df[col].mode()[0]}, inplace=True)

def acp(x:np.ndarray,std=True,nlib=0):
    n,m=x.shape
    x_=x-np.mean(x,axis=0)
    if std:
        x_=x_/np.std(x_,axis=0)
    r_v=(1/(n-nlib))*x_.T@x_
    valp,vecp=np.linalg.eig(r_v)
    valp=np.real(valp)
    vecp=np.real(vecp)
    #print(valp,vecp,sep='\n')
    k=np.flip(np.argsort(valp))
    #print(k)
    alpha=valp[k]
    a=vecp[:,k]
    c=x_@a
    if std:
        r=a*np.sqrt(alpha)
    else:
        r=np.corrcoef(x_,c)[:m,m:]
    return x_,r_v,alpha,a,c,r

    #Tabelare varianta

def tabelare_varianta(alpha:np.ndarray):
    m=len(alpha)
    varianta_cumulata=np.cumsum(alpha)
    procent=alpha/varianta_cumulata[m-1]
    df=pd.DataFrame(
        {
            "Varianta":alpha,
            "Varianta cumulata":varianta_cumulata,
            "Procent varianta":procent,
            "Procet cumulat":np.cumsum(procent)
        },
        index=["C"+str(i+1) for i in range(m)],
    )
    return df
