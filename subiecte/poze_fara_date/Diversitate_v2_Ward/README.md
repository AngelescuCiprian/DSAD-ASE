# Diversitate economică – varianta 2 (Ward)

![enunt](enunt.jpg)

**Date (lipsesc):** `Diversitate.csv` – indicii de diversitate economică pe localități și ani: `Siruta`, `Localitate`, `2008`, `2009`, ..., `2021`.
`Coduri_Localitati.csv` – `Siruta`, `Localitate`, `Judet`. Cheia de legătură: `Siruta`.

## Cerințe (transcrise din poză)

**A1.** Valoarea medie a indicelui de diversitate (media pe ani) pe localitate, **în ordine descrescătoare** → `Cerinta1.csv`: Siruta, localitate, diversitate. *(1p)*
```
Siruta,Localitate,Diversitate
179132,Municipiul Bucuresti,0.7748850000000002
95060,Municipiul Iasi,0.7460085714285715
54975,Municipiul Cluj-Napoca,0.7419014285714285
```

**A2.** Pentru fiecare județ și fiecare an, **numărul de localități cu diversitatea 0** → `Cerinta2.csv`. *(2p)*
```
Judet,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021
ab,3,5,3,4,2,2,1,2,1,1,2,3,1,2
```

**B.** Clusteri Ward: 1. matricea ierarhie la consolă *(1p)*; 2. dendrograma pentru partiția optimală *(2p)*; 3. componența partiției optimale → `popt.csv` *(2p)*.

**C.** Model de analiză factorială cu 5 variabile standardizate și 2 factori comuni; coeficienții factoriali L (factor loadings) în `g20.csv`. Afișați **factorul specific cu cea mai mare varianță** (număr 1–5). *(1p)*

> Idee C: varianța specifică = `1 - (L[:,0]**2 + L[:,1]**2)`; răspunsul = `argmax + 1`.

## Idei de rezolvare A
- A1: `df[ani].mean(axis=1)` + `sort_values(ascending=False)`
- A2: `(df[ani] == 0)` dă True/False; merge cu județul; `groupby("Judet").sum()` numără True-urile
