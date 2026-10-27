# S1_2023 – Mișcarea naturală a populației

Enunț original: [enunt_S1_2023.pdf](enunt_S1_2023.pdf)

**Date:** `MiscareaNaturala.csv` – indicatori pe țări (2015, UN Statistics): `Country_Number`, `Country_Name`, `Three_Letter_Country_Code`, `FR` (fertilitate), `IM` (mortalitate), `LE` / `LEF` / `LEM` (speranța de viață: total / femei / bărbați), `MMR` (mortalitate maternală), `RS` (spor natural).
`CoduriTariExtins.csv` – codificări + continente (cheie: `Country_Number`, **a 4-a coloană**).

## Cerințe

**A1.** Salvarea în `cerinta1.csv` a țărilor cu rata sporului natural **pozitivă**, în ordinea descrescătoare a RS. Cod de țară, nume, RS. *(2p)*
```
Three_Letter_Country_Code,Country_Name,RS
OMN,"Oman, Sultanate of",6.773
QAT,"Qatar, State of",6.473
```

**A2.** Salvarea în `cerinta2.csv` a valorilor medii ale indicatorilor pe continent, pentru continentele unde media RS > media RS la nivel mondial. *(2p)*
```
Continent_Name,FR,IM,LE,LEF,LEM,MMR,RS
Africa,4.5636,52.51648076923077,...,2.358673076923077
Asia,2.6341302325581397,...,1.960906976744186
```

**B.** ACP standardizată: 1. varianțele componentelor la consolă *(1p)*; 2. scorurile → `scoruri.csv` *(2p)*; 3. graficul scorurilor în primele două axe *(2p)*.

## Rezolvări
- [rezolvare_A.py](rezolvare_A.py) – explicat, cu calcul de mână (Oceania 1.313 < 1.428)
- [rezolvare_B.py](rezolvare_B.py) – ACP cu funcțiile profului

**Observație B:** C7 are varianța ≈ 0, pentru că `LE` e practic media lui `LEF` și `LEM` (variabile aproape liniar dependente). E normal.
