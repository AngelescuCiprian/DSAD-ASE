# Practică P3 – Șomajul pe localități 2015–2023

> Datele din `Somaj.csv` sunt **generate** ([generare_date.py](generare_date.py)), nu reale. `PopulatieLocalitati.csv` e real.

În fișierul **Somaj.csv** se află numărul de șomeri la nivel de localitate, în perioada 2015–2023: `Siruta`, `Localitate`, `2015` ... `2023`.
În fișierul **PopulatieLocalitati.csv** se află populația și indicativul de județ pentru fiecare localitate (`Siruta`, `Localitate`, `Judet`, `Populatie`). Legătura se face prin Siruta.

**1.** Să se salveze în **Output1.csv** numărul mediu de șomeri pe localitate, în ordine descrescătoare. *(1 punct)*
```
Siruta,Localitate,Medie
179132,Municipiul Bucuresti,29531.444444444445
```

**2.** Să se salveze în **Output2.csv** anul cu cei mai mulți șomeri, pentru fiecare localitate. Vor fi omise localitățile fără niciun șomer în toată perioada. *(2 puncte)*
```
Siruta,Localitate,Anul
1017,Municipiul Alba Iulia,2016
```

**3.** Să se salveze în **Output3.csv** rata șomajului în 2023 la nivel de localitate (șomeri 2023 / populație), în ordine descrescătoare. *(2 puncte)*
```
Siruta,Localitate,Rata2023
33382,Josenii Bargaului,0.11959761549925485
```

**4.** Să se salveze în **Output4.csv** rata șomajului la nivel de județ pentru fiecare an și rata medie (media ratelor anuale), în ordinea descrescătoare a ratei medii. Rata = numărul de șomeri / populația județului. *(2 puncte)*
```
Judet,2015,2016,...,2023,RataMedie
cj,0.058096334910400615,0.05450571536934657,...
```

**5.** Să se salveze în **Output5.csv**, pentru fiecare județ, anul cu cea mai mică rată a șomajului. *(2 puncte)*
```
Judet,AnulMinim
ab,2019
```

1 punct din oficiu.
