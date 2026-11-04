# Modele de TEST (grupa 1091)

Testul acoperă **doar partea de pandas** (seminariile 1–3): 5 cerințe de tipul A1/A2 din examen, 9 puncte + 1 din oficiu.

| Test | Date | Status |
|---|---|---|
| [S1_1091_Industrie](S1_1091_Industrie) | ✅ `Industrie.csv`, `PopulatieLocalitati.csv` | rezolvat, toate 5 cerințele identice cu exemplele din enunț |
| [S1_1085_Firme](S1_1085_Firme) | ⚠️ `I2014.csv` generat, populația reală | **dat de prof anul acesta**; rezolvat, toate exemplele ies exact |
| [S1_1086_Energie](S1_1086_Energie) | ✅ `EnergLoc.csv`, `RO_NUTS.csv` (originale) | **dat la 1086 săptămâna asta**; rezolvat, toate exemplele ies exact |
| [S2_1091_PIB](S2_1091_PIB) | ⚠️ date de test generate (originalele lipsesc) | rezolvat, toate exemplele din enunț ies exact pe datele de test |

## Modele de practică

3 modele în același stil, cu date și rezolvări: [practica/](practica) (P1 Vot, P2 Alcool, P3 Șomaj).

5 modele pe tiparul testului dat anul acesta (S1_1085): [practica_1085/](practica_1085) (M1 Agricultură, M2 Sănătate, M3 Comerț, M4 Turism, M5 Energie).

## Ce concepte cer (toate din seminariile 1–3)

| Cerință | S1 (Industrie) | S2 (PIB) |
|---|---|---|
| 1 | total pe rând `sum(axis=1)` | medie pe rând `mean(axis=1)` |
| 2 | merge + raport (CA / locuitor) + sortare | merge + raport pe fiecare an (`div(axis=0)`) + conversie unități |
| 3 | `idxmax(axis=1)` după filtrare (total > 0) | `idxmin(axis=1)` |
| 4 | `groupby("Judet").sum()` | `groupby("REGION").sum()` |
| 5 | groupby sumă + raport + sortare | `groupby().idxmax()` (țara cu max pe regiune și an) |
