# Practică P1 – Structura votanților pe sex și vârstă

În fișierul **Vot_Categorii_Sex.csv** se află structura votanților pe categorii de sex și vârstă la nivel de localitate (procente din totalul votanților):
`Siruta` – codul Siruta; `Localitate` – denumirea; `Barbati_18-24`, `Barbati_25-34`, `Barbati_35-44`, `Barbati_45-64`, `Femei_18-24`, `Femei_25-34`, `Femei_35-44`, `Femei_45-64` – procentul votanților din categoria respectivă.
În fișierul **Coduri_Localitati.csv** se află județul fiecărei localități (`Siruta`, `Localitate_X`, `Judet`, `Localitate`). Legătura se face prin Siruta.

**1.** Să se salveze în **Output1.csv** procentul total de bărbați și procentul total de femei la nivel de localitate. Se salvează codul Siruta, localitatea, procentul bărbaților și al femeilor. *(1 punct)*
```
Siruta,Localitate,Barbati,Femei
1017,MUNICIPIUL ALBA IULIA,53.294,45.19499999999999
```

**2.** Să se salveze în **Output2.csv** localitățile în care procentul femeilor este mai mare decât cel al bărbaților, în ordinea descrescătoare a diferenței Femei − Barbati. Se salvează Siruta, localitatea, procentele și diferența. *(2 puncte)*
```
Siruta,Localitate,Barbati,Femei,Diferenta
159213,VARIAS,21.64,77.32600000000001,55.68600000000001
```

**3.** Să se salveze în **Output3.csv** categoria de votanți cu procentul cel mai mare, la nivel de localitate. *(2 puncte)*
```
Siruta,Localitate,Categorie
1017,MUNICIPIUL ALBA IULIA,Femei_18-24
```

**4.** Să se salveze în **Output4.csv** media procentelor pe fiecare categorie, la nivel de județ. *(2 puncte)*
```
Judet,Barbati_18-24,Barbati_25-34,...,Femei_45-64
ab,3.912576923076923,5.399333333333333,22.809410256410256,40.13152564102564,9.138602564102564,...
```

**5.** Să se salveze în **Output5.csv**, pentru fiecare județ, localitatea cu cel mai mare procent de votanți tineri (Barbati_18-24 + Femei_18-24) și valoarea acestuia. *(2 puncte)*
```
Judet,Localitate,Tineri
ab,RIMETEA,82.407
```

1 punct din oficiu.
