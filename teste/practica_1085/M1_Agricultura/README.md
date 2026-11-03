# Model M1 – Agricultura pe localități

În fișierul **Agricultura.csv** se află date privind agricultura la nivel de localitate: `Siruta`, `Localitate`, `NrFerme`, `SuprafataHa` (suprafața agricolă, hectare), `ProductieTone`, `NrAnimale`, `Subventii` (lei).
În fișierul **PopulatieLocalitati.csv** se află codurile Siruta, indicativele de județ și populația fiecărei localități.

**1.** Să se salveze în **Output1.csv** randamentul (producția / suprafața agricolă) pentru fiecare localitate **cu suprafață agricolă**, în ordine descrescătoare. Siruta, localitatea, randamentul. *(2 puncte)*
```
Siruta,Localitate,Randament
39959,Dimacheni,7.4976512655121645
73996,Sadova,7.497565425748234
```

**2.** Să se calculeze numărul de ferme **la 1000 de locuitori** pentru fiecare județ și să se salveze în **Output2.csv**, în ordine descrescătoare. *(2 puncte)*
```
Judet,Ferme la 1000 loc
GR,122.2691654930849
TR,97.86742628377857
```

**3.** Să se determine pentru fiecare județ localitatea cu cele mai mari **subvenții pe hectar** și să se salveze în **Output3.csv**. Se iau în calcul doar localitățile cu suprafață agricolă. *(2 puncte)*
```
Judet,Localitate
AB,Sancel
AG,Botesti
```

**4.** Să se calculeze mediile ponderate ale indicatorilor `NrFerme`, `ProductieTone`, `NrAnimale`, `Subventii` la nivel de județ, folosind ca pondere **suprafața agricolă** a localităților. Județele fără suprafață agricolă se omit. Rezultatul în **Output4.csv**. *(3 puncte)*
```
Judet,NrFerme,ProductieTone,NrAnimale,Subventii
AB,287.214,17746.937,2446.201,1219236.243
AG,289.198,13256.507,3205.441,1015735.037
```

1 punct din oficiu.
