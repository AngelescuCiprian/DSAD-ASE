# Model M3 – Comerțul pe localități, agregat pe regiuni

În fișierul **Comert.csv** se află date privind comerțul cu amănuntul la nivel de localitate: `Siruta`, `Localitate`, `NrMagazine`, `NrAngajati`, `Vanzari`, `Chirii` (lei).
În fișierul **PopulatieLocalitati.csv** se află codurile Siruta, indicativele de județ și populația fiecărei localități.
În fișierul **Coduri_Judete.csv** se află regiunea fiecărui județ (`IndicativJudet`, `NumeJudet`, `Regiune`).

**1.** Să se salveze în **Output1.csv** vânzările pe angajat pentru localitățile **care au angajați**, în ordine descrescătoare. *(2 puncte)*
```
Siruta,Localitate,Vanzari/Angajat
10532,Craiva,2034502.3214285714
15064,Caldararu,1845546.6666666667
```

**2.** Să se calculeze numărul de angajați în comerț **la 1000 de locuitori** pe **regiune** și să se salveze în **Output2.csv**, în ordine descrescătoare. *(2 puncte)*
```
Regiune,Angajati la 1000 loc
Bucuresti-Ilfov,77.1671180370153
Sud-Vest,38.768649922687345
```

**3.** Să se determine pentru fiecare regiune **județul** cu cele mai mari vânzări pe locuitor și să se salveze în **Output3.csv**: regiunea și indicativul județului. *(2 puncte)*
```
Regiune,Judet
Bucuresti-Ilfov,B
Centru,BV
```

**4.** Să se calculeze mediile ponderate ale celor 4 indicatori la nivel de **regiune**, folosind ca pondere **populația localităților**. Rezultatul în **Output4.csv**. *(3 puncte)*
```
Regiune,NrMagazine,NrAngajati,Vanzari,Chirii
Bucuresti-Ilfov,47354.421,148485.889,56661895369.21,4609052328.876
Centru,682.598,3412.299,1791989466.718,134032432.355
```

1 punct din oficiu.
