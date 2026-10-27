# S2_2024 – Indicatori macroeconomici per capita (2021)

Enunț original: [enunt_S2_2024.pdf](enunt_S2_2024.pdf)

**Date:** `GlobalIndicatorsPerCapita_2021.csv` – `CountryID`, `Country`, `GNI`, `ChangesInv`, `Exports`, `Imports`, `FinalConsExp`, `GrossCF`, `HouseholdConsExp` și valoarea adăugată pe ramuri: `AgrHuntForFish`, `Construction`, `Manufacturing`, `MiningManUt`, `TradeT`, `TransportComm`, `Other` (USD per capita).
`CoduriTari.csv` – `CountryID`, `Country` (alte denumiri!), `Continent`.

## Cerințe

**A1.** Pentru fiecare țară, **ramura cu valoarea adăugată cea mai mare** → `Cerinta1.csv`. *(2p)*
```
CountryID,Country,Ramura Dominanta
4,Afghanistan,AgrHuntForFish
```

**A2.** Valorile medii ale indicatorilor (GNI ... Other) pe continent → `Cerinta2.csv`. *(2p)*
```
Continent,GNI,ChangesInv,Exports,...,Other
Africa,2417.27,59.98,1124.58,1221.01,2057.66,532.65,1568.04,266.27,123.15,267.32,584.3,335.28,196.5,818.07
```

**B.** Clusteri Ward: 1. matricea ierarhie la consolă *(1p)*; 2. partiția optimală (Elbow) + scorul Silhouette pe instanță → `popt.csv` (cod, țară, cluster, silhouette) *(2p)*; 3. histograma pentru partiția optimală și variabila GNI *(2p)*.

## Rezolvări
- [rezolvare_A.py](rezolvare_A.py) – `idxmax(axis=1)` pe ramuri; 4 țări fără continent se pierd la merge (corect)
- [rezolvare_B.py](rezolvare_B.py) – Ward + Silhouette (capitol încă nefăcut la seminar)
