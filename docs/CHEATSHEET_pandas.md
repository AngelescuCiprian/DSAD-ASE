# Cheatsheet pandas – partea A

## Rețeta pentru orice cerință
1. **Nivel?** localitate / județ / regiune / continent → ce e pe rânduri în output
2. **Date?** în ce fișiere sunt → dacă sunt în mai multe: `merge`
3. **Operație?** filtrare / calcul pe rând / pe coloană / agregare pe grup
4. **Output?** copiezi formatul exemplului din enunț (coloane, ordine, index sau nu)

## Citire
```python
df = pd.read_csv("data_in/X.csv", index_col=0)    # prima coloană = cheia (Siruta, CountryID...)
coloane = list(df.columns.values[1:])             # coloanele numerice (sari peste nume)
df.shape   df.head()   df.columns   df.loc[cheie]  # verificări
```
- `index_col` = **poziția** coloanei-cheie (nu e mereu 0! ex. `CoduriTariExtins.csv` → 3)
- **DataFrame** = tabel 2D, **Series** = o coloană sau un rând (1D)
- pandas **aliniază după index**, nu după poziție

## axis
| | Rezultat | Exemplu |
|---|---|---|
| `axis=0` (implicit) | o valoare **per coloană** | media pe țară a fiecărui indicator, CV pe indicator |
| `axis=1` | o valoare **per rând** | totalul unei localități, ramura dominantă |

`axis` se pune pe **DataFrame** (`df.sum(axis=1)`, `df.apply(f, axis=1)`), nu pe Series-ul din lambda.

## Operații de bază
```python
df[coloane].sum(axis=1)                    # total pe rând
df[df["RS"] > 0]                           # filtrare cu mască
df[(df[ani] == 0).any(axis=1)]             # „cel puțin un an e 0”
df.sort_values(by="RS", ascending=False)   # sortare (ATRIBUIE rezultatul!)
df["Nou"] = df["A"] / df["B"]              # coloană nouă
df.apply(lambda x: ..., axis=1)            # logică pe fiecare rând (x = Series)
A if conditie else B                       # if într-un lambda
df.fillna(0)                               # NaN → 0 (ATRIBUIE!)
df.insert(0, "Nume", alt_df["Nume"])       # coloană pe poziția 0
df[coloane].idxmax(axis=1)                 # pe rând: NUMELE coloanei cu maximul
df[coloane].idxmax()                       # pe coloană: INDEXUL rândului cu maximul
serie.map(alta_serie)                      # traduce valori (cod → nume) după index
```

## max / argmax / idxmax
| Metodă | Returnează | Pe rândul Cluj: 1203, 12, ..., 3082 |
|---|---|---|
| `max()` | valoarea | 3082 |
| `argmax()` | poziția (0, 1, 2...) | 6 |
| `idxmax()` | eticheta | `"Panificatie"` |

## Merge
| Cheia în stânga | Cheia în dreapta | Scrii |
|---|---|---|
| index | index | `left_index=True, right_index=True` |
| coloană | index | `left_on="Judet", right_index=True` |
| index | coloană | `left_index=True, right_on="Col"` |
| coloană | coloană | `left_on="A", right_on="B"` |

- După merge: **verifică `shape`**. Rânduri pierdute = chei care nu s-au potrivit.
- Coloane cu același nume → `_x` / `_y`. Ia din tabelul de coduri doar ce-ți trebuie: `df_coduri[["Continent"]]`.

## Groupby
```python
df[["Judet", "Total", "Populatie"]].groupby("Judet").sum()
#   └ ce coloane iau ─────────────┘        └ după ce ┘  └ cum ┘
df[ind + ["Continent"]].groupby("Continent").mean()
df[ind + ["Continent"]].groupby("Continent").idxmax()      # indexul rândului cu max, pe grup și coloană
df[ind + ["Pop", "Regiune"]].groupby("Regiune").apply(func=f, include_groups=False)   # f primește un DataFrame
```
- Selectezi **doar** coloana de grupare + coloanele numerice (altfel textele se lipesc)
- Coloana de grupare **devine index** → `.loc["cj"]`

## Media ponderată
```python
def medii_ponderate(t):                    # t = toate rândurile unui grup
    return pd.Series(np.average(t[ind], axis=0, weights=t["Populatie"]), index=ind)
```
`(x1*p1 + x2*p2) / (p1 + p2)`. NU e media simplă.

## Salvare
```python
os.makedirs("data_out", exist_ok=True)
rezultat.to_csv("data_out/Cerinta1.csv")              # indexul = prima coloană
rezultat.to_csv("data_out/Cerinta1.csv", index=False) # când exemplul NU începe cu cheia
serie.name = "Ponderi"                                # numele coloanei pentru o Series
```

## Capcanele (în care am căzut deja)
1. Lipsă `index_col` → merge greșit **fără eroare**
2. `axis` pus în lambda în loc de `apply`
3. Lambda care returnează uneori un număr, alteori un rând → ambele ramuri trebuie să returneze același tip
4. Ponderi/procente calculate jos și adunate/mediate sus → **aduni brutele, apoi împarți**
5. `df.sort_values(...)` / `df.fillna(0)` fără atribuire → metodele returnează un obiect **nou**: `x = x.metoda()`
6. Rotunjirea ascunde valoarea reală (79.998% afișat ca 0.8)
