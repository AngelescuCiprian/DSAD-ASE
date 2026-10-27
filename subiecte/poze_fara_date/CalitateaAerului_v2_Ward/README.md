# Calitatea aerului – varianta 2 (Ward)

![enunt](enunt.jpg)

**Date (lipsesc):** `CalitateaAeruluiTari.csv` – `CountryId`, `Country` și indicatorii `Air_quality_Carbon_Monoxide`, `Air_quality_Ozone`, `Air_quality_Nitrogen_dioxide`, `Air_quality_Sulphur_dioxide`, `Air_quality_PM2.5`, `Air_quality_PM10`.
`CoduriTari.csv` – codificări + continente. Cheia: `CountryId`.

## Cerințe (transcrise din poză – e neclară, verifică pe original)

**A1.** Țara în care se înregistrează **cea mai mare valoare pentru fiecare indicator** → `Cerinta1.csv`: indicator, țară. *(1p)*
```
Indicator,Country
Air_quality_Carbon_Monoxide,Indonesia
```

**A2.** Țările cu cele mai mari valori la nivel de continent, pentru fiecare indicator → `Cerinta2.csv`: continent + câte o țară pe indicator. *(2p)*
```
Continent,Air_quality_Carbon_Monoxide,Air_quality_Ozone,...
Africa,Ethiopia,Morocco,Algeria,South Africa,Burkina Faso,Mauritania
```

**B.** Clusteri Ward: 1. matricea ierarhie la consolă *(1p)*; 2. dendrograma pentru partiția optimală *(2p)*; 3. componența partiției optimale → `popt.csv` *(2p)*.

**C.** Analiză factorială cu 5 variabile X1..X5: coeficienții de corelație în `g21_1.csv`, coeficienții de corelație parțială în `g21_2.csv`. Calculați și afișați **indexul KMO global**. *(1p)*

> Idee C: KMO = Σ r²ᵢⱼ / (Σ r²ᵢⱼ + Σ p²ᵢⱼ), sumele doar pe elementele din afara diagonalei.

## Idei de rezolvare A
- A1: `df[ind].idxmax()` (axis=0 → pe fiecare coloană indexul rândului cu max) + `map` pe numele țării.
- A2: identic cu [S1 A2](../../S1_MiscareaNaturala/rezolvare_A.py).
