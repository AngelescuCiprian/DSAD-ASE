# Test S1 (1091) – Cifra de afaceri industrială

Enunț: [enunt_S1_1091.docx](enunt_S1_1091.docx) · Rezolvare: [rezolvare.py](rezolvare.py) · Output: [data_out/](data_out)

**Date:** `Industrie.csv` (cifra de afaceri pe 9 activități industriale, pe localitate) și `PopulatieLocalitati.csv` (Siruta, Localitate, Judet, Populatie). Sunt aceleași fișiere ca în `din_D_DSAD/.../Canonica/dataIn`.

1. **Output1.csv**: cifra de afaceri totală pe localitate. *(1p)* → `sum(axis=1)`
2. **Output2.csv**: cifra de afaceri pe locuitor, descrescător. *(2p)* → merge + împărțire + `sort_values`
3. **Output3.csv**: activitatea cu cifra de afaceri maximă, fără localitățile cu total 0. *(2p)* → filtrare **înainte**, apoi `idxmax(axis=1)` (pe un rând numai cu 0, `idxmax` ar întoarce `Alimentara`)
4. **Output4.csv**: cifra de afaceri pe activitate, pe județ. *(2p)* → `groupby("Judet").sum()`; exemplul are județele cu litere mari → `.str.upper()`
5. **Output5.csv**: cifra de afaceri pe locuitor, pe județ, descrescător. *(2p)* → **aduni brutele pe județ, apoi împarți**

Verificat: primele rânduri din fiecare output coincid cu exemplele din enunț (Cojocna 1685412.0, Oras Mioveni 586069.35, AB 1426022767.0, AG 42819.77...).
