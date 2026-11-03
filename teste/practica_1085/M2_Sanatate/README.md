# Model M2 – Sănătate pe localități

În fișierul **Sanatate.csv** se află date privind sistemul de sănătate la nivel de localitate: `Siruta`, `Localitate`, `NrMedici`, `NrPaturi` (paturi de spital), `NrFarmacii`, `Internari`, `Cheltuieli` (lei).
În fișierul **PopulatieLocalitati.csv** se află codurile Siruta, indicativele de județ și populația fiecărei localități.

**1.** Să se salveze în **Output1.csv** numărul de internări pe pat de spital pentru localitățile **care au paturi**, în ordine descrescătoare. Siruta, localitatea, raportul. *(2 puncte)*
```
Siruta,Localitate,Internari/Pat
81754,Sacelu,47.916666666666664
77561,Radesti,47.666666666666664
```

**2.** Să se calculeze numărul de medici **la 1000 de locuitori** pe județ și să se salveze în **Output2.csv**, în ordine descrescătoare. *(2 puncte)*
```
Judet,Medici la 1000 loc
BR,6.711936696784331
SB,4.058013446340576
```

**3.** Să se determine pentru fiecare județ localitatea cu cele mai mari **cheltuieli pe locuitor** și să se salveze în **Output3.csv**: județul, localitatea și valoarea cheltuielilor pe locuitor. *(2 puncte)*
```
Judet,Localitate,Cheltuieli/Loc
AB,Municipiul Blaj,3677.4836619986663
AG,Oras Costesti,3438.1874647622626
```

**4.** Să se calculeze mediile ponderate ale celor 5 indicatori la nivel de județ, folosind ca pondere **populația** localităților. Rezultatul în **Output4.csv**. *(3 puncte)*
```
Judet,NrMedici,NrPaturi,NrFarmacii,Internari,Cheltuieli
AB,63.071,232.308,7.264,7772.607,53991510.165
AG,259.952,557.659,17.806,12757.571,138458855.06
```

1 punct din oficiu.
