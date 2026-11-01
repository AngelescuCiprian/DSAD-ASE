# Test S1 (1085) – Activitatea firmelor în 2014 · dat de prof anul acesta

Enunț: [enunt_S1_1085.png](enunt_S1_1085.png) · Rezolvare: [rezolvare.py](rezolvare.py)

> ⚠️ `I2014.csv` e **generat** ([generare_date.py](generare_date.py)), nu e fișierul original. E construit astfel încât **toate exemplele din enunț să iasă exact**. `PopulatieLocalitati.csv` e real și e același fișier pe care l-a folosit profu' (ratele B / IF / TM din exemplu ies exact pe el).

**Date:** `I2014.csv`: `Siruta, DenLocalitate, NrFirme, NrSal, TotalCifraAfaceri, TotalProfit, TotalPierdere`. `PopulatieLocalitati.csv`: `Siruta, Localitate, Judet, Populatie`.

**1. Output1.csv:** raportul cifra de afaceri / număr de salariați pentru localitățile **cu salariați**, descrescător. *(2p)*
```
Siruta,DenLocalitate,Raport CA/NrSal
93771,Independenta,2444763.184
60507,Oras Navodari,2444151.356
```

**2. Output2.csv:** rata ocupării = salariați **la 1000 de locuitori**, pe județ, descrescător. *(2p)*
```
Judet,Rata Ocuparii
B,513.8058810884887
IF,374.32818563436416
TM,249.36274846084416
```

**3. Output3.csv:** pe județ, localitatea cu cel mai mare **profit pe locuitor**. *(2p)*
```
Judet,Localitate
AB,Galda De Jos
```

**4. Output4.csv:** mediile **ponderate** (pondere = populația localităților) ale celor 5 indicatori, pe județ. *(3p)*
```
Judet,NrFirme,NrSal,TotalCifraAfaceri,TotalProfit,TotalPierdere
AB,946.407,5690.334,1336997181.357,113378467.612,31730528.39
```

1 punct din oficiu.

## Capcane
1. **Cerința 1:** filtrezi `NrSal > 0` **înainte** de împărțire. Altfel `CA / 0 = inf` iese primul la sortare.
2. **Cerința 2:** aduni salariații și populația pe județ, **apoi** împarți și înmulțești cu 1000.
3. **Cerința 3:** `groupby(...)["ProfitLoc"].idxmax()` dă **Siruta**, iar numele îl iei cu `.map()`.
4. **Cerința 4:** media ponderată, nu `.mean()`. Funcția cu `np.average(..., weights=...)` + `groupby().apply()`.
5. Județele sunt cu litere **mari** în exemple → `.index.str.upper()`.
