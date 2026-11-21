# Fișa ACP (sklearn): structura pe de rost

## Structura: 5 blocuri, mereu în aceeași ordine
```
DATE  →  MODEL  →  VARIANȚĂ  →  SCORURI  →  GRAFIC   (+ R la interpretare)
x        x_, fit    alpha        c, s         scatter
```
Fiecare bloc folosește ce a ieșit din blocul dinainte: `x` → `x_` → `model` → `alpha` → `s`.

## Trucul 1: din model scoți 3 lucruri
| Ce vrei | Din model | Cum ții minte |
|---|---|---|
| `alpha` | `model.explained_variance_ * (n-1)/n` | **variance** → varianța. Corecția: sklearn împarte la n−1, profu la n |
| `c` | `model.transform(x_)` | **transform** → transformă țările în coordonate noi |
| `a` | `model.components_.T` | **components** → rețeta. `.T`, pentru că sklearn o dă pe rânduri |

## Trucul 2: celelalte le calculezi tu cu √alpha
```
s = c / √alpha      ← „s” de la „supra”: SCORURILE împart
r = a * √alpha      ← „r” de la „ori”: CORELAȚIILE înmulțesc
```

## Trucul 3: orice output e un DataFrame. Te întrebi doar „ce e pe rânduri?”
| Output | Matricea | Pe rânduri (`index=`) | Pe coloane |
|---|---|---|---|
| Varianta.csv | dicționarul cu 4 coloane | componentele: `etichete` | Varianta, Varianta cumulata, Procent varianta, Procent cumulat |
| Scoruri.csv | `s` | **țările**: `df.index` | `etichete` |
| r.csv | `r` | **variabilele**: `variabile` | `etichete` |

Scorurile sunt despre **țări**. Corelațiile sunt despre **variabile**. Pe coloane ai mereu componentele C1…Cm.

## Trucul 4: tabelul varianței = 2 numere + `cumsum` pe ele
```python
procent = alpha * 100 / alpha.sum()
# Varianta = alpha              Varianta cumulata = np.cumsum(alpha)
# Procent varianta = procent    Procent cumulat   = np.cumsum(procent)
```

## Trucul 5: criteriile
```python
nr_kaiser = (alpha > 1).sum()                              # NUMERI câte sunt > 1
nr_80 = np.where(np.cumsum(procent) > 80)[0][0] + 1       # PRIMA poziție > 80, +1 (pozițiile încep de la 0)
```

## Trucul 6: graficul = 4 linii de fond, restul e decor
```python
fig, ax = plt.subplots(figsize=(10, 7))
ax.scatter(s[:, 0], s[:, 1])                    # x = C1, y = C2
for i in range(n):
    ax.text(s[i, 0], s[i, 1], df.index[i])      # eticheta fiecărui punct
plt.show()                                       # ULTIMA linie din script
# decor: set_title, set_xlabel/ylabel, axhline(0)/axvline(0), c="r", fontsize
```

## Extra: comunalitățile (au apărut la partea C)
```python
comunalitati = df_r["C1"]**2 + df_r["C2"]**2          # pe primele 2
# pe toate, cumulat: np.cumsum(r * r, axis=1)
```

## Greșelile tale de până acum
- [ ] `import os` + `os.makedirs("data_out", exist_ok=True)`
- [ ] antetele scrise corect („Procent cumulat”, nu „Procent cumulata”)
- [ ] `print` la ce cere „afișați”
- [ ] `plt.show()` la final, altfel restul codului așteaptă să închizi fereastra
- [ ] `components_` **cu** `.T`

## Test de 2 minute: completează golurile din memorie
```python
x_ = ________().fit_transform(x)
model = ____().fit(x_)
alpha = model.__________________ * (___) / ___
c = model._________(x_)
s = c ___ np.sqrt(alpha)
a = model.___________.__
r = a ___ np.sqrt(alpha)
df_scoruri = pd.DataFrame(s, index=_________, columns=________)
df_r = pd.DataFrame(r, index=_________, columns=________)
```
