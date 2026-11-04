# Harta seminariilor: ce găsești și unde

Liniile sunt din fișierele profului, cum le-ai primit în arhive (`Seminar1_1075`, `Seminar2_1073`, `Seminar3_1073`). Copiile sunt în [seminarii/originale_prof](../seminarii/originale_prof).

## Caută după ce cere subiectul

| Dacă cerința zice... | Deschide | Linii |
|---|---|---|
| „pentru localitățile în care **totalul** > 0” | S3 `main.py` | 16–19 |
| „**procentul** pe fiecare activitate/etnie la nivel de localitate” | S3 `main.py` · S2 `main.py` | 22–28 · 27–28 |
| „dacă totalul e 0, **procentele vor fi 0**” | ⚠️ S3 n-o face! Adaugi `.fillna(0)` | vezi [CHEATSHEET_FINAL](CHEATSHEET_FINAL.md) |
| „**pe județ**” (lipești județul pe localități) | S3 `main.py` · S2 `main.py` | 31–35 · 14–17 |
| „**pondere / raport** pe județ” (ex. angajați / populație) | S3 `main.py` | 36–38 |
| „activitatea / tipul **dominant** pe județ” | S3 `main.py` | 41–46 |
| „**pe regiune**” (județ → regiune) | S3 `main.py` (pornești de la localități) · S2 `main.py` (pornești de la județe) | 49–54 · 20–24 |
| „**medie ponderată** … pondere populația” | S3 `main.py` (funcția + apelul) | 5–8 + 56–59 |
| „**indicele de localizare**” | ⚠️ S3 e neterminată (64–65). Rezolvarea completă e în [CHEATSHEET_FINAL](CHEATSHEET_FINAL.md) | |
| „**macroregiune**” | S2 `Coduri_Regiuni.csv` (Regiune → MacroRegiune). Nu e în cod, e același tipar ca județ → regiune | |
| **valori lipsă** (NaN) într-un DataFrame | S2 `functii.py` → `nan_replace_df` (copiezi funcția) | 5–11 |
| valori lipsă / standardizare / corelații în **numpy** | S1 `functii.py` | 6–17 |
| matrice numpy → CSV cu nume de rânduri/coloane | S1 `functii.py` → `tabelare_salvare_matrice` | 19–31 |
| corelații / covarianțe **pe grupe** | S1 `main.py` + `functii.py` | 32–35 · 33–43 |

## Seminar 1: `Seminar1_1075` (Teritorial_2022, grupa 1075), numpy

| Ce | Unde |
|---|---|
| lista de coloane după primele 3: `list(df)[3:]` | `main.py:12` |
| din DataFrame în numpy: `df[variabile].values` | `main.py:13` |
| NaN → media coloanei (numpy): `nan_replace` | `functii.py:6–10` |
| standardizare / centrare (`scal=False`) | `functii.py:13–17`, apel `main.py:19–20` |
| salvare matrice cu index și coloane | `functii.py:19–31` |
| covarianță / corelație: `np.cov(x, rowvar=False)`, `np.corrcoef(x, rowvar=False)` | `main.py:28–31` |
| aceleași pe grupe (regiuni): mască `y == clasa` | `functii.py:33–43`, `main.py:32–35` |

Pentru testul cu pandas contează doar `list(df)[k:]` și `.values`. Restul e pentru ACP.

## Seminar 2: `Seminar2_1073` (Etnii), pandas, agregări pe niveluri

| Ce | Unde |
|---|---|
| `nan_replace_df`: NaN → media (numeric) / modul (text) | `functii.py:5–11`, apel `main.py:12` |
| merge **index–index** (etnii + coduri localități după Siruta) | `main.py:14–15` |
| `groupby("County").sum()` cu selecție de coloane `etnii + ["County"]` | `main.py:17–18` |
| merge **index → coloană**: `left_index=True, right_on="IndicativJudet"` | `main.py:20–23` |
| `groupby("Regiune").sum()` | `main.py:24–25` |
| procente pe rând: `apply(lambda x: x*100/x.sum(), axis=1)` | `main.py:27` |
| `insert(0, "Localitate", ...)`: pui numele înapoi pe poziția 0 | `main.py:28` |
| indicele de disimilaritate (segregare) | `functii.py:13–21` |

⚠️ **Coduri_Judete.csv diferă între seminarii:**
- **S2:** prima coloană e `NrCrt`. Cu `index_col=0`, `IndicativJudet` rămâne coloană, deci folosești `right_on="IndicativJudet"`.
- **S3:** prima coloană e `IndicativJudet`. Cu `index_col=0`, devine index, deci folosești `right_index=True`.

La test, **uită-te la primul rând din fișier** și abia apoi alegi.

## Seminar 3: `Seminar3_1073` (IndustriaAlimentara), cel mai apropiat de test

| Cerința | Ce face | Linii |
|---|---|---|
| funcția de **medie ponderată** | `average(x[:,:-1], weights=x[:,-1])`. ⚠️ Ponderea trebuie să fie **ultima coloană**: `activitati + ["Populatie", "Regiune"]` | 5–8 |
| 1. filtrare după total | `s_totaluri = df[activitati].sum(axis=1)`, apoi `df[s_totaluri > 0]` | 16–19 |
| 2. procente pe localitate | `df["Totaluri"] = s_totaluri`, apoi `apply(lambda x: x[activitati]*100/x["Totaluri"], axis=1)` + `insert` | 22–28 |
| 3. pondere pe județ, sortată | merge cu populația → `groupby("Judet").sum()` → `Totaluri / Populatie` → `.name` → `sort_values` | 31–38 |
| 4. activitatea dominantă pe județ | `apply(lambda x: x.index[x.argmax()], axis=1)`, la fel ca `idxmax(axis=1)` | 41–46 |
| 5. medie ponderată pe regiune | merge `left_on="Judet", right_index=True` → `groupby("Regiune").apply(calcul_medii, include_groups=False)` | 49–61 |
| 6. indice de localizare | doar început (totalurile naționale) | 64–65 |

⚠️ Bug-uri de știut:
- C2 lasă NaN acolo unde totalul e 0. Cerința zice 0, deci adaugi `fillna(0)`.
- C3 salvează coloana cu numele `Totaluri`, iar PDF-ul cere `Ponderi`.

## Seminar 4: ACP (nu intră la testul de mâine)

| Ce | Unde |
|---|---|
| `index_col=1` (cheia e a doua coloană) | `main.py:11` |
| `acp(x)` → `x_, r_v, alpha, a, c, r` | `functii.py:13`, apel `main.py:16` |
| tabelul de varianță (Kaiser, procent cumulat) | `functii.py:36`, apel `main.py:19–20` |
| graficul de varianță | `grafice.py:4` |

## Unde găsești rezolvări complete în repo
- Tiparul testului dat (4 cerințe): [teste/S1_1085_Firme](../teste/S1_1085_Firme/rezolvare.py) + [practica_1085](../teste/practica_1085) M1–M5
- Teste cu 5 cerințe: [S1_1091](../teste/S1_1091_Industrie), [S2_1091](../teste/S2_1091_PIB), [practica](../teste/practica) P1–P3
