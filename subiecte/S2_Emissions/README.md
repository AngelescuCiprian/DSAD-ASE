# S2 – Emisii de particule în Europa

Enunț original: [enunt_S2.pdf](enunt_S2.pdf)

**Date:** `Emissions.csv` – `CountryCode`, `Country`, `AirEmiss`, `Sulphur`, `Nitrogen`, `Ammonia`, `NonMeth`, `Partic`, `GreenGE`, `GreenGIE`. Toate în **tone**, mai puțin `GreenGE` și `GreenGIE`, care sunt în **mii de tone**.
`PopulatieEuropa.csv` – `Code`, `NAME`, `Region` (EasternE, WesternE, ...), `Population`.

## Cerințe

**A1.** Salvarea în `Cerinta1.csv` a emisiilor totale pe țară, **în tone**. *(2p)*
```
CountryCode,Country,Emisii_total_tone
AUT,Austria,2453643.49
BEL,Belgium,2419287.04
```

**A2.** Salvarea în `Cerinta2.csv` a valorilor medii pe tip de particule, pe regiune – **media ponderată cu populația**. *(2p)*
```
Region,AirEmiss,Sulphur,Nitrogen,Ammonia,NonMeth,Partic,GreenGE_tone,GreenGIE_tone
British,841743.362,1773.152,2652.611,8.613,899.088,138.32,2530203.541,987810.377
```

**B.** ACP standardizată: 1. tabelul varianței → `Varianta.csv` *(1p)*; 2. scorurile → `Scoruri.csv` *(2p)*; 3. graficul scorurilor în primele două axe *(2p)*.

## Rezolvări
- [rezolvare_A.py](rezolvare_A.py) – conversia în tone + media ponderată, cu calculul de mână pe British
- [rezolvare_B.py](rezolvare_B.py)
