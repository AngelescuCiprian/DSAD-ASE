# Exercițiu 03: ACP ghidată pe GlobalIndicatorsPerCapita_2021

În `data_in/GlobalIndicatorsPerCapita_2021.csv` ai **212 țări × 14 indicatori economici pe locuitor** (USD, 2021): venitul național brut (`GNI`), exporturi, importuri, consum, investiții, apoi valoarea adăugată pe ramuri (agricultură, construcții, industrie, comerț, transport...). Prima coloană e `CountryID`, a doua e `Country`.

Faci o **ACP standardizată** cu sklearn. Scrie codul singur, pas cu pas, și verifică-te după fiecare pas. Rezolvarea e în [rezolvare.py](rezolvare.py); deschide-o doar la final.

---

**1. Citire.** Citește fișierul cu indexul = **numele țării**. Construiește lista `variabile` cu cei 14 indicatori.
- 💡 `Country` e a doua coloană, deci `index_col=?`. `CountryID` e număr, dar e un **cod**, nu un indicator, așa că nu intră în analiză.
- ✅ `df.shape` = `(212, 15)`, `len(variabile)` = `14`, iar primul element din `variabile` e `GNI`.

**2. Valori lipsă.** Afișează câte NaN sunt, apoi înlocuiește-le cu media.
- ✅ `0`. Pasul se scrie oricum, ca reflex: la examen datele pot avea NaN.

**3. Matricea și standardizarea.** Treci în numpy, ia `n` și `m`, standardizează.
- ✅ `n, m` = `212 14`. Coloanele lui `x_` au media 0 și abaterea standard 1.

**4. Modelul + varianța.** Antrenează PCA și calculează `alpha` (nu uita corecția!).
- ✅ `alpha[0]` ≈ `9.269`, iar `alpha.sum()` = `14`.

**5. Tabelul varianței → `Varianta.csv`.** Coloanele sunt: Varianta, Varianta cumulata, Procent varianta, Procent cumulat. Indexul e C1…C14.
- ✅ C1 = **66.204%**, iar procentul cumulat la C3 e 85.596.

**6. Câte componente păstrezi.** Afișează numărul după Kaiser și după criteriul de 80%.
- ✅ `Kaiser: 3 | Procent > 80%: 3`
- 🤔 La seminar ieșiseră 4 și 7. De ce aici ies mult mai puține? Uită-te la cât duce C1.

**7. Scorurile → `Scoruri.csv`.** Indexul e țara, coloanele sunt C1…C14.
- ✅ Afghanistan: C1 = `-0.6317`, C2 = `-0.0263`.
- Dacă îți iese cu semn inversat, e ok (vezi lecția despre semn).

**8. Topul pe C1.** Afișează primele 3 și ultimele 3 țări după scorul pe C1.
- 💡 `df_scoruri["C1"].sort_values(...)`, adică exact sortarea de la partea A.
- ✅ Sus: Monaco, Liechtenstein, Luxembourg. Jos: Burundi, Yemen, South Sudan.

**9. Corelațiile factoriale → `r.csv`.** Apoi afișează variabilele cu |r| > 0.7 pe C1.
- 💡 Filtrare cu mască pe `df_r["C1"].abs()`, la fel ca la partea A.
- ✅ 11 variabile, printre care `GNI` = 0.981.
- 🤔 Ce înseamnă C1, dacă aproape toți indicatorii au corelație mare și pozitivă cu ea?

**10. Comunalitățile pe primele 2 componente.** Pentru fiecare variabilă calculezi r²(C1) + r²(C2). Care variabilă e **cel mai slab** explicată de C1 și C2?
- 💡 Rezultatul e o Series indexată după variabile, deci `idxmin()`.
- ✅ `AgrHuntForFish`, cu 0.094.

**11. Graficul scorurilor (C1, C2),** cu numele țărilor pe puncte.
- ✅ Aproape toate țările sunt strânse în stânga, câteva state mici și bogate stau departe la dreapta, iar Liechtenstein e jos de tot, la C2 ≈ −10.
- 🤔 De ce stă Liechtenstein atât de jos pe C2? Indiciu: în `r`, C2 e corelată negativ cu `Manufacturing` și `MiningManUt`.
