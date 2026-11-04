# Model M4 – Turism pe localități

În fișierul **Turism.csv** se află numărul de locuri de cazare pe tipuri de unități, la nivel de localitate: `Siruta`, `Localitate`, `Hotel`, `Pensiune`, `Vila`, `Camping`, `Hostel`.
În fișierul **PopulatieLocalitati.csv** se află codurile Siruta, indicativele de județ și populația fiecărei localități.

> Tiparul **seminarului 3** (IndustriaAlimentara): dacă te blochezi, deschide `Seminar3_1073/main.py`.

**1.** Să se salveze în **Output1.csv** capacitatea totală de cazare (suma pe toate tipurile) pentru localitățile **care au locuri de cazare**, în ordine descrescătoare. Siruta, localitatea, totalul. *(2 puncte)*
```
Siruta,Localitate,Total
179132,Municipiul Bucuresti,35764
95060,Municipiul Iasi,18087
```

**2.** Să se calculeze procentul fiecărui tip de cazare în capacitatea totală a localității și să se salveze în **Output2.csv**. **Dacă localitatea nu are locuri de cazare, procentele vor fi 0.** Siruta, localitatea, procentele. *(2 puncte)*
```
Siruta,Localitate,Hotel,Pensiune,Vila,Camping,Hostel
1017,Municipiul Alba Iulia,44.70956857073994,45.07110147023379,2.265606170161485,2.8922631959508314,5.061460592913955
...
2381,Arieseni,0.0,0.0,0.0,0.0,0.0
```

**3.** Să se salveze în **Output3.csv** tipul de cazare cu cele mai multe locuri la nivel de județ. Indicativul județului și tipul dominant. *(2 puncte)*
```
Judet,Tip
AB,Pensiune
AG,Vila
```

**4.** Să se calculeze **indicii de localizare** la nivel de județ pentru fiecare tip de cazare și să se salveze în **Output4.csv**. Indicele de localizare = ponderea județului în totalul național al tipului respectiv, împărțită la ponderea populației județului în populația țării. *(3 puncte)*

Exemplu: județul are 3.000 de locuri în pensiuni, țara 100.000; județul are 200.000 de locuitori, țara 20.000.000 → (3000 / 100000) / (200000 / 20000000) = **3**.
```
Judet,Hotel,Pensiune,Vila,Camping,Hostel
AB,1.4399087232899357,4.138076836079161,0.3686080009819729,1.536402558297493,1.1665183239226184
AG,1.3076527374872409,1.2517759242794826,9.017184274775715,2.2019858475679643,1.2495232668215688
```

1 punct din oficiu.
