# Modele de practică pentru test

3 modele în stilul testelor S1_1091 / S2_1091: **5 cerințe, 9 puncte + 1 din oficiu**, doar pandas (seminariile 1–3).
Fiecare are enunțul cu exemple (primul rând din fiecare output, ca să te verifici), datele în `data_in/` și rezolvarea explicată în `rezolvare.py`.

| Model | Date | Ce exersezi în plus |
|---|---|---|
| [P1_Vot](P1_Vot) | reale (vot pe localități) | sumă pe subset de coloane, filtrare după o coloană calculată, `groupby` + `idxmax` → nume |
| [P2_Alcool](P2_Alcool) | reale (consum de alcool pe țări) | NaN cu `nan_replace_df`, `index_col=2`, `groupby().idxmax()` + `map` |
| [P3_Somaj](P3_Somaj) | generate (șomeri pe localități) | rată pe județ și an cu `div(axis=0)`, `idxmin`, filtrare înainte de `idxmax` |

**Cum lucrezi:** citește `README.md` din folder (enunțul), scrie codul singur (~45 min), compară primele rânduri cu exemplele, abia apoi deschide `rezolvare.py`.
