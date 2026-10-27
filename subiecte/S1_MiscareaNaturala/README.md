# S1 – Mișcarea naturală a populației (varianta 2)

Enunț original: [enunt_S1.pdf](enunt_S1.pdf) · Aceleași date ca la [S1_2023](../S1_2023_MiscareaNaturala).

## Cerințe

**A1.** Salvarea în `Cerinta1.csv` a țărilor cu RS **mai mic decât media globală** a RS, în ordinea descrescătoare a RS. Cod, nume, RS. *(2p)*
```
Three_Letter_Country_Code,Country_Name,RS
MYS,Malaysia,1.412
```

**A2.** Pentru fiecare continent, **codurile țărilor cu valorile maxime** pentru fiecare indicator → `Cerinta2.csv`. *(2p)*
```
Continent_Name,FR,IM,LE,LEF,LEM,MMR,RS
Africa,NER,SLE,DZA,MUS,DZA,SLE,GNQ
```

**B.** Analiza de clusteri Ward: 1. matricea ierarhie → `h.csv` *(1p)*; 2. dendrograma pentru partiția optimală *(2p)*; 3. componența partiției optimale → `popt.csv` *(2p)*.

## Rezolvări
- [rezolvare_A.py](rezolvare_A.py) – `groupby().idxmax()` + `map` pentru coduri
- [rezolvare_B.py](rezolvare_B.py) – Ward, partiția optimală după Elbow (capitol încă nefăcut la seminar)
