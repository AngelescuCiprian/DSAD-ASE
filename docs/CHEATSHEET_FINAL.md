# Cheatsheet final: testul de pandas

Ai câte un șablon pentru fiecare tip de cerință. Copiezi, schimbi numele coloanelor și compari cu exemplul. Unde găsești fiecare lucru în seminarii: [HARTA_SEMINARII](HARTA_SEMINARII.md).

## 0. Primele 3 minute
1. **Citește toate cerințele.** Notează pentru fiecare **nivelul** (localitate / județ / regiune) și **ce împarți la ce**.
2. **Deschide CSV-urile** și uită-te la primul rând. Ce coloană e cheia? E cu litere mici sau mari?
3. **Fă merge-ul o singură dată**, sus, și folosește-l la toate cerințele.

```python
import os
import numpy as np
import pandas as pd

os.makedirs("data_out", exist_ok=True)

df = pd.read_csv("data_in/Date.csv", index_col=0)                 # index = Siruta
ind = list(df.columns.values[1:])                                  # coloanele numerice
df_pop = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)
df_coduri = pd.read_csv("data_in/Coduri_Judete.csv", index_col=0)  # index = IndicativJudet (dacă e prima coloană!)

df_merge = df.merge(df_pop[["Judet", "Populatie"]], left_index=True, right_index=True)
df_merge = df_merge.merge(df_coduri[["Regiune"]], left_on="Judet", right_index=True)
print(df_merge.shape)                                               # câte rânduri au rămas?
```

## 1. Nivel LOCALITATE (fără merge)

**Raport, doar unde numitorul > 0, descrescător.** Filtrezi ÎNAINTE de împărțire, altfel îți iese `inf`.
```python
df_f = df[df["B"] > 0]
out = df_f[["Localitate"]].copy()                       # [[ ]] → DataFrame, ca să poți adăuga coloane
out["A/B"] = df_f["A"] / df_f["B"]
out = out.sort_values(by="A/B", ascending=False)        # ATRIBUI!
out.to_csv("data_out/Cerinta1.csv")
```

**Total pe rând + filtru** (S3, cerința 1):
```python
s_total = df[ind].sum(axis=1)                           # axis=1 = pe RÂND
out = df[s_total > 0]                                    # aceleași coloane ca fișierul
```

**Procente pe rând, cu 0 unde totalul e 0** (S3, cerința 2):
```python
out = df[ind].div(s_total, axis=0) * 100                 # fiecare RÂND împărțit la totalul lui
out = out.fillna(0)                                       # 0/0 = NaN → 0
out.insert(0, "Localitate", df["Localitate"])
```

**Media pe rând** / **doar rândurile fără niciun 0** / **cel puțin un 0**:
```python
df[ind].mean(axis=1)
df[(df[ind] > 0).all(axis=1)]
df[(df[ind] == 0).any(axis=1)]
```

**Coloana cu maximul pe fiecare rând** (anul sau activitatea):
```python
out = df[["Localitate"]].copy()
out["An"] = df[ind].idxmax(axis=1)                       # idxmin(axis=1) pentru minim
```

## 2. Nivel JUDEȚ / REGIUNE

**Regula de aur:** întâi **aduni brutele** pe grup, abia apoi împarți. Rapoartele nu se adună și nu se mediază.

**Rată la 1000 de locuitori, descrescător:**
```python
g = df_merge[["Judet", "A", "Populatie"]].groupby("Judet").sum()     # sau "Regiune"
s = (g["A"] / g["Populatie"] * 1000).sort_values(ascending=False)
s.index = s.index.str.upper()                                          # dacă exemplul are AB, nu ab
s.name = "Rata"                                                        # numele coloanei din exemplu
s.to_csv("data_out/Cerinta2.csv")
```

**Activitatea dominantă pe județ** (S3, cerința 4):
```python
g = df_merge[ind + ["Judet"]].groupby("Judet").sum()
s = g[ind].idxmax(axis=1)
s.name = "Activitate"
```

**Raport pe județ și pe fiecare an** (coloane = ani):
```python
g = df_merge[ani + ["Judet", "Populatie"]].groupby("Judet").sum()
out = g[ani].div(g["Populatie"], axis=0)           # NU g[ani] / g["Populatie"] → tot NaN!
```

**Procente pe județ** (S2, „de calculat acasă”):
```python
g = df_merge[ind + ["Judet"]].groupby("Judet").sum()
out = g[ind].div(g[ind].sum(axis=1), axis=0) * 100
```

## 3. „Pe grup, CINE are maximul?”

**Localitatea cu maximul X pe locuitor, pe județ.** `idxmax` îți dă Siruta, apoi o traduci în nume.
```python
df_merge["XLoc"] = df_merge["X"] / df_merge["Populatie"]
s_siruta = df_merge.groupby("Judet")["XLoc"].idxmax()            # județ → Siruta
out = s_siruta.map(df_merge["Localitate"]).to_frame(name="Localitate")
out["XLoc"] = s_siruta.map(df_merge["XLoc"])                     # dacă se cere și valoarea
# sau dintr-o mișcare: out = df_merge.loc[s_siruta, ["Judet", "Localitate", "XLoc"]].set_index("Judet")
```
Dacă împarți la ceva care poate fi 0, filtrezi întâi: `df_f = df_merge[df_merge["B"] > 0].copy()`.

**Județul cu maximul pe regiune** (două niveluri: sume pe județ, apoi max pe regiune):
```python
g = df_merge[["Judet", "Regiune", "X", "Populatie"]].groupby(["Judet", "Regiune"]).sum()
g = g.reset_index(level="Regiune")                                # Judet = index, Regiune = coloană
g["XLoc"] = g["X"] / g["Populatie"]
s = g.groupby("Regiune")["XLoc"].idxmax().str.upper()             # indexul ESTE județul
```

**Același lucru, pe fiecare an** (tabelul pe județe are deja coloanele-ani):
```python
t = out_judete.merge(df_coduri[["Regiune"]], left_index=True, right_index=True)   # pe litere MICI
r = t.groupby("Regiune")[ani].idxmax()
```

## 4. Medie ponderată (de obicei 3p)

Funcția primește TOATE localitățile unui grup. **Nu agrega nimic înainte!**
```python
def medii_ponderate(t):
    return pd.Series(np.average(t[ind], axis=0, weights=t["Populatie"]), index=ind)

out = df_merge[ind + ["Populatie", "Judet"]].groupby("Judet").apply(
    func=medii_ponderate, include_groups=False)
out.round(3).to_csv("data_out/Cerinta4.csv")                     # round dacă exemplul are 3 zecimale
```
- Dacă ponderea e altă coloană (de exemplu suprafața), schimbi `weights=`.
- Dacă un grup are suma ponderilor 0, filtrezi întâi `df_merge[df_merge["Suprafata"] > 0]`, altfel `ZeroDivisionError`.
- Varianta profului (S3:5–8) ia ponderea din **ultima coloană**, deci ordinea e `ind + ["Populatie", "Regiune"]`.

## 5. Indicele de localizare (S3, cerința 6, neterminată la prof)
`(județ / țară pe activitate) / (populație județ / populație țară)`
```python
g = df_merge[ind + ["Judet", "Populatie"]].groupby("Judet").sum()
pondere_act = g[ind] / g[ind].sum()                               # coloană / totalul coloanei
pondere_pop = g["Populatie"] / g["Populatie"].sum()
out = pondere_act.div(pondere_pop, axis=0)                        # verificat: ab Carne 3.188 ✓
```

## 6. Formatul output-ului
| Exemplul arată... | Scrii |
|---|---|
| `AB` în loc de `ab` | `x.index = x.index.str.upper()` |
| o coloană cu un anumit nume, de la o Series | `s.name = "Nume"` sau `s.to_frame(name="Nume")` |
| alt nume de coloană | `df = df.rename(columns={"vechi": "nou"})` (fără `inplace`!) |
| fără cheia în prima coloană | `to_csv(..., index=False)` |
| 3 zecimale | `.round(3)` |

## 7. `["X"]` sau `[["X"]]`?
- `df["X"]` dă o **Series**. O folosești la calcule, `weights=`, `.map()` și ca să atribui o coloană nouă.
- `df[["X"]]` dă un **DataFrame**. O folosești ca punct de pornire pentru un output la care adaugi coloane, sau pentru merge și groupby.

## 8. Când nu-ți iese
| Simptom | Cauză |
|---|---|
| primul rând e `inf` | n-ai filtrat numitorul > 0 |
| tot NaN după împărțire | `df / serie` aliniază pe coloane → `df.div(serie, axis=0)` |
| valori prea mari pe grup | ai adunat rapoarte în loc de brute, sau ai agregat înainte de media ponderată |
| `KeyError` | numele coloanei greșit, sau coloana e deja index după groupby |
| `TypeError` la `idxmax` / `sum` | ai lăsat o coloană text în groupby → selectează doar coloanele numerice + cheia |
| merge cu 0 rânduri | chei diferite (`ab` vs `AB`, index vs coloană) → `print(df.head())` la amândouă |
| `None` / `AttributeError: NoneType` | ai scris `x = x.metoda(..., inplace=True)` |
| tabelul de la cerința 3 are rânduri lipsă | ai suprascris `df` cu varianta filtrată la cerința 1 → pune filtrul într-o variabilă nouă |
