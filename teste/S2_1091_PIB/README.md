# Test S2 (1091) – PIB-ul țărilor europene 1995–2021

Enunț: [enunt_S2_1091.docx](enunt_S2_1091.docx) · Rezolvare: [rezolvare.py](rezolvare.py)

> ⚠️ **Datele din `data_in/` sunt de TEST, nu originalele.** Sunt generate cu [generare_date_test.py](generare_date_test.py): 29 de țări europene, valori aproximativ realiste, construite astfel încât **toate exemplele din enunț să iasă exact** (Belgia, Bulgaria, Cehia, suma EasternE, Slovenia). Restul valorilor nu sunt reale.
> Dacă apar fișierele originale și dau `KeyError`, ajustează cele 3 nume de coloane de la începutul scriptului (`COL_TARA`, `COL_POPULATIE`, `COL_REGIUNE`).

**Structura datelor de test:**
- `gdp.csv`: `CODE, Country, 1995, ..., 2021` (PIB în **milioane** de euro)
- `populatie.csv`: `CODE, COUNTRY, POPULATION, EURO, REGION` (regiuni: EasternE, WesternE, NorthernE, SouthernE)

1. **Output1.csv**: PIB-ul mediu pe țară. *(1p)* → `mean(axis=1)`
2. **Output2.csv**: PIB pe locuitor pe fiecare an, în euro/locuitor. *(2p)* → PIB-ul e în **milioane** de euro → `* 1_000_000`, apoi `div(populatie, axis=0)`
3. **Output3.csv**: anul cu cel mai mic PIB. *(2p)* → `idxmin(axis=1)`
4. **Output4.csv**: PIB-ul pe an, pe regiune. *(2p)* → `groupby(regiune).sum()` (exemplul e sumă, nu medie)
5. **Output5.csv**: țara cu cel mai mare PIB/locuitor, pe regiune și an. *(2p)* → pe tabelul de la cerința 2: `groupby(regiune).idxmax()` (indexul e CODE, deci iese direct codul țării)

**Verificare (iese exact pe datele de test):** Belgium → PIB mediu 344422.97, PIB/loc 1995 = 20021.702, anul minim 1996; EasternE 1995 = 294850.2; EasternE → SI în toți anii.
