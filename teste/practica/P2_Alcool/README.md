# Practică P2 – Consumul de alcool pe țări

În fișierul **Alcool.csv** se află consumul de alcool (litri de alcool pur pe locuitor pe an) pe țări, în anii 2000, 2005, 2010, 2015 și 2018: `Code` – codul de țară din 3 litere, `Country` – numele țării, `2000` ... `2018`.
În fișierul **CoduriTariExtins.csv** se află codificările țărilor și împărțirea pe continente. Legătura se face prin codul de 3 litere (`Three_Letter_Country_Code`).

**1.** Să se salveze în **Output1.csv** consumul mediu pe țară, în ordine descrescătoare. Valorile lipsă se înlocuiesc cu media anului respectiv. *(1 punct)*
```
Code,Country,Consum mediu
LTU,Lithuania,14.662
```

**2.** Să se salveze în **Output2.csv** anul în care s-a înregistrat consumul maxim, pentru fiecare țară. *(2 puncte)*
```
Code,Country,Anul
AFG,Afghanistan,2005
```

**3.** Să se salveze în **Output3.csv** țările în care consumul a scăzut între 2000 și 2018, împreună cu scăderea (2000 − 2018), în ordinea descrescătoare a scăderii. *(2 puncte)*
```
Code,Country,Scadere
SOM,Somalia,6.091908455
```

**4.** Să se salveze în **Output4.csv** consumul mediu pe continent, pentru fiecare an. *(2 puncte)*
```
Continent_Name,2000,2005,2010,2015,2018
Africa,4.704260696415095,4.471921006207547,4.6621145976415095,4.718584905660378,4.684037735849056
```

**5.** Să se salveze în **Output5.csv**, pentru fiecare continent și fiecare an, numele țării cu cel mai mare consum. *(2 puncte)*
```
Continent_Name,2000,2005,2010,2015,2018
Africa,Rwanda,Rwanda,Uganda,Seychelles,Seychelles
```

1 punct din oficiu.
