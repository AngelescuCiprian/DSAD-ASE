# Test S2 (1091) – PIB-ul țărilor europene 1995–2021

Enunț: [enunt_S2_1091.docx](enunt_S2_1091.docx) · Rezolvare: [rezolvare.py](rezolvare.py)

> ⚠️ **Lipsesc datele** (`gdp.csv`, `populatie.csv`). Rezolvarea e scrisă pe structura dedusă din exemplele din enunț și e testată pe date de probă. Când apar fișierele: pune-le în `data_in/`, rulează, iar dacă dă `KeyError`, ajustează cele 3 nume de coloane de la începutul scriptului (`COL_TARA`, `COL_POPULATIE`, `COL_REGIUNE`).

1. **Output1.csv**: PIB-ul mediu pe țară. *(1p)* → `mean(axis=1)`
2. **Output2.csv**: PIB pe locuitor pe fiecare an, în euro/locuitor. *(2p)* → PIB-ul e în **milioane** de euro → `* 1_000_000`, apoi `div(populatie, axis=0)`
3. **Output3.csv**: anul cu cel mai mic PIB. *(2p)* → `idxmin(axis=1)`
4. **Output4.csv**: PIB-ul pe an, pe regiune. *(2p)* → `groupby(regiune).sum()` (exemplul e sumă, nu medie)
5. **Output5.csv**: țara cu cel mai mare PIB/locuitor, pe regiune și an. *(2p)* → pe tabelul de la cerința 2: `groupby(regiune).idxmax()` (indexul e CODE, deci iese direct codul țării)

**Verificare când ai datele:** Belgium → PIB mediu 344422.97, PIB/loc 1995 = 20021.702, anul minim 1996; EasternE 1995 = 294850.2; EasternE → SI în toți anii.
