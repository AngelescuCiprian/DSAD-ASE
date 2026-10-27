# Functii comune - pornite de la functii.py al profului (Seminarul 2 + Seminarul 4)
# si completate pentru analiza de clusteri (Ward).

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from scipy.cluster.hierarchy import fcluster


# ---------------------------------------------------------------------
# Inlocuire NaN (profu', seminarul 2)
# numeric -> media coloanei, text -> valoarea cea mai frecventa (moda)
# ---------------------------------------------------------------------
def nan_replace_df(df: pd.DataFrame):
    for col in df.columns:
        if df[col].isnull().any():
            if is_numeric_dtype(df[col]):
                df.fillna({col: df[col].mean()}, inplace=True)
            else:
                df.fillna({col: df[col].mode()[0]}, inplace=True)


# ---------------------------------------------------------------------
# ACP (profu', seminarul 4)
# x      -> matricea de date (n instante x m variabile)
# return -> x_ (date standardizate), r_v (matricea de corelatii),
#           alpha (valori proprii = variantele componentelor, descrescator),
#           a (vectori proprii pe COLOANE), c (componentele principale),
#           r (corelatii variabile - componente)
# ---------------------------------------------------------------------
def acp(x: np.ndarray, std=True, nlib=0):
    n, m = x.shape
    x_ = x - np.mean(x, axis=0)
    if std:
        x_ = x_ / np.std(x_, axis=0)
    r_v = (1 / (n - nlib)) * x_.T @ x_
    valp, vecp = np.linalg.eig(r_v)
    valp = np.real(valp)
    vecp = np.real(vecp)
    k = np.flip(np.argsort(valp))
    alpha = valp[k]
    a = vecp[:, k]
    c = x_ @ a
    if std:
        r = a * np.sqrt(alpha)
    else:
        r = np.corrcoef(x_, c, rowvar=False)[:m, m:]
    return x_, r_v, alpha, a, c, r


# ---------------------------------------------------------------------
# Tabelul variantei (profu', seminarul 4)
# ---------------------------------------------------------------------
def tabelare_varianta(alpha: np.ndarray):
    m = len(alpha)
    varianta_cumulata = np.cumsum(alpha)
    procent = alpha / varianta_cumulata[m - 1]
    df = pd.DataFrame(
        {
            "Varianta": alpha,
            "Varianta cumulata": varianta_cumulata,
            "Procent varianta": procent,
            "Procent cumulat": np.cumsum(procent),
        },
        index=["C" + str(i + 1) for i in range(m)],
    )
    return df


# ---------------------------------------------------------------------
# Standardizare simpla (folosita la Ward)
# ---------------------------------------------------------------------
def standardizare(x: np.ndarray):
    return (x - np.mean(x, axis=0)) / np.std(x, axis=0)


# ---------------------------------------------------------------------
# Matricea ierarhie (rezultatul lui scipy linkage) -> DataFrame lizibil
# Fiecare rand = o jonctiune: cei doi clusteri unificati, distanta dintre ei,
# numarul de instante din clusterul nou format.
# Clusterii 0..n-1 sunt instantele initiale; clusterul format la jonctiunea i
# primeste numarul n+i.
# ---------------------------------------------------------------------
def tabelare_ierarhie(h: np.ndarray):
    n = h.shape[0] + 1
    return pd.DataFrame(
        {
            "Cluster 1": h[:, 0].astype(int),
            "Cluster 2": h[:, 1].astype(int),
            "Distanta": h[:, 2],
            "Numar instante": h[:, 3].astype(int),
        },
        index=["Jonctiunea " + str(i + 1) for i in range(n - 1)],
    )


# ---------------------------------------------------------------------
# Partitia optimala - criteriul Elbow (cel mai mare salt intre distantele
# a doua jonctiuni consecutive).
#   d[j] = h[j+1, 2] - h[j, 2]   (cresterea distantei de la jonctiunea j la j+1)
#   j*   = argmax(d)             -> ne oprim DUPA jonctiunea j* (nu facem saltul mare)
#   dupa j*+1 jonctiuni raman n - (j*+1) clusteri
# Daca dai k, se calculeaza partitia cu k clusteri.
# Returneaza: k, pragul (pentru colorarea dendrogramei), etichetele "C1".."Ck"
# ---------------------------------------------------------------------
def partitie(h: np.ndarray, k=None):
    n = h.shape[0] + 1
    if k is None:
        d = h[1:, 2] - h[:n - 2, 2]
        j = int(np.argmax(d))
        k = n - (j + 1)
    else:
        j = n - k - 1
    prag = (h[j, 2] + h[j + 1, 2]) / 2
    coduri = fcluster(h, k, criterion="maxclust")
    etichete = np.array(["C" + str(c) for c in coduri])
    return k, prag, etichete
