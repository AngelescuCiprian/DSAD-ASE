# Exercițiu 04: ACP pe județele României (scris din memorie)

În `data_in/Teritorial_2022.csv` ai **42 de județe × 31 de indicatori** pe 2022: natalitate (`RN`), mortalitate (`RM`), salariul mediu (`Sal`), medici, PIB pe locuitor, producția agricolă, bugetele locale, rețeaua de apă și canalizare, export etc.
Primele 4 coloane sunt `Indicativ`, `Judet`, `Regiunea` și `Macroregiunea`.

**Regula de data asta:** scrii **fără să te uiți** în codul vechi sau în fișă. Ai 20 de minute. Te uiți abia când te blochezi de tot, apoi notezi unde te-ai blocat. Rezolvarea e în [rezolvare.py](rezolvare.py).

**1. Datele.** Indexul e `Indicativ`. Construiește `variabile` cu cei 31 de indicatori.
- ⚠️ `Macroregiunea` e număr, dar e un **cod** (1, 2, 3, 4), nu un indicator.
- ✅ `(42, 34) 31`. Primul indicator e `RN`, ultimul e `Export`.

**2. Valori lipsă.** Afișează câte NaN sunt înainte și după.
- ✅ Înainte sunt `4`, apoi `0`. De data asta chiar sunt NaN, deci dacă sari pasul ăsta, crapă PCA.

**3. Matricea și standardizarea.**
- ✅ `n, m` = `42 31`.

**4. Modelul și varianța.**
- ✅ `alpha[0]` ≈ `10.451`, iar `alpha.sum()` = `31`.

**5. `Varianta.csv`.**
- ✅ C1 = **33.714%**, iar procentul cumulat la C9 e 81.051.

**6. Criteriile.**
- ✅ `Kaiser: 9 | Procent > 80%: 9`

**7. `Scoruri.csv`.**
- ✅ `ab`: C1 = `-0.0743`, C2 = `1.0131`. Semnul inversat e ok.

**8. Primele 3 și ultimele 3 județe pe C1.**
- ✅ Sus: `b`, `cj`, `bv`. Jos: `tr`, `gr`, `cl`.

**9. `r.csv`.** Apoi afișează indicatorii cu |r| > 0.8 pe C1.
- ✅ `['Sal', 'Medici', 'PIB']`

**10. Graficul scorurilor (C1, C2),** cu indicativele pe puncte.
- ✅ București e singur, departe la dreapta. Ilfov e jos de tot.

---

🤔 **De gândit (fără cod):**
1. Ce reprezintă C1? Uită-te la pasul 9 și la județele de la pasul 8.
2. La GlobalIndicators, 14 variabile aveau nevoie de **3** componente ca să treacă de 80%. Aici 31 de variabile au nevoie de **9**. Ce spune asta despre cât de corelate sunt variabilele între ele?
3. Ce fel de județe au scor mic pe C1? Indiciu: în `r.csv`, care variabile au corelație **negativă** cu C1?
