# Test grupa 1086 – Coeficienți de localizare în industria energetică

Enunțul: [enunt_1086.png](enunt_1086.png). Datele din `data_in/` sunt **originalele** (`EnergLoc.csv`, `RO_NUTS.csv`): toate exemplele din enunț ies exact.

| Cerința | Ce exersezi | Puncte |
|---|---|---|
| 1. județele cu media pe cele 8 activități > 1 | `mean(axis=1)` + filtrare | 2 |
| 2. județele unde activitatea dominantă e c3530 | `idxmax(axis=1) == "c3530"` + `[["c3530"]]` | 2 |
| 3. coeficienții de variație pe regiune | merge index–index + `groupby().std() / groupby().mean()` | 3 |
| 4. județul cu maximul pe regiune și activitate | `groupby("Regiune").idxmax()` | 2 |

## Capcane
- **`index_col=0` face din `Judet` index**, deci activitățile sunt **toate** coloanele: `list(df.columns.values)`, NU `[1:]`. Cu `[1:]` pierzi `c3511`, iar media lui `dj` nu mai iese 2.300375.
- **Cerința 2:** `df[...]["c3530"]` dă o Series. Cu `[["c3530"]]` păstrezi antetul `Judet,c3530`.
- **Cerința 3:** `.std()` din pandas are `ddof=1`, și asta dă exemplul (0.683). Cu `np.std` (implicit `ddof=0`) iese 0.483, adică greșit.
- **Cerința 3:** celulele goale sunt regiuni unde toate județele au 0 la activitatea respectivă: 0 / 0 = NaN. E corect să rămână așa.
- **Cerința 4:** unde toate valorile din regiune sunt 0, `idxmax` dă primul județ. Nu te stresa, așa iese la toată lumea.

Datele nu au populație și sunt deja pe județ, deci e un singur merge (index–index cu `RO_NUTS`).
