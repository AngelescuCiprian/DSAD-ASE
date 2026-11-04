# Model M5 – Consumul de energie electrică pe localități (2019–2023)

În fișierul **Energie.csv** se află consumul anual de energie electrică (**MWh**) la nivel de localitate: `Siruta`, `Localitate`, `2019`, `2020`, `2021`, `2022`, `2023`. Un consum de 0 înseamnă că lipsesc datele pentru anul respectiv.
În fișierul **PopulatieLocalitati.csv** se află codurile Siruta, indicativele de județ și populația. În fișierul **Coduri_Judete.csv** este specificată regiunea fiecărui județ.

> Tiparul **S2_1091 (PIB)**: date pe ani, câte o coloană pe an.

**1.** Să se salveze în **Output1.csv** consumul mediu anual pentru localitățile care au consum **în toți anii**, în ordine descrescătoare. Siruta, localitatea, consumul mediu. *(2 puncte)*
```
Siruta,Localitate,ConsumMediu
179132,Municipiul Bucuresti,4777479.615999999
69900,Municipiul Craiova,1341122.9300000002
```

**2.** Să se salveze în **Output2.csv**, pentru fiecare localitate, anul în care consumul a fost maxim. Siruta, localitatea, anul. *(2 puncte)*
```
Siruta,Localitate,AnMaxim
1017,Municipiul Alba Iulia,2023
1071,Ciugud,2021
```

**3.** Să se calculeze consumul pe locuitor, în **kWh**, la nivel de județ, pentru fiecare an, și să se salveze în **Output3.csv**. *(2 puncte)*
```
Judet,2019,2020,2021,2022,2023
AB,1851.17410181408,1777.714862861865,2247.687920563506,1960.083555229088,2296.252869341658
AG,1540.6081388334646,1640.6289267319382,1984.116854592981,1690.4974711150296,1863.9413948308663
```

**4.** Să se determine, pentru fiecare regiune și fiecare an, **județul** cu cel mai mare consum pe locuitor și să se salveze în **Output4.csv**. *(3 puncte)*
```
Regiune,2019,2020,2021,2022,2023
Bucuresti-Ilfov,IF,IF,B,B,B
Centru,SB,SB,MS,SB,MS
```

1 punct din oficiu.
