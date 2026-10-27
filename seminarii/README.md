# Seminarii

| Seminar | Temă | Ce se învață |
|---|---|---|
| [Seminar02_Etnii](Seminar02_Etnii) | Tema2_1 – populația pe etnii | `read_csv`, `nan_replace_df`, merge, groupby pe județ/regiune, procente cu `apply(axis=1)` |
| [Seminar03_IndustriaAlimentara](Seminar03_IndustriaAlimentara) | Tema2_4 – angajați în industria alimentară | filtrare, procente, merge + groupby, `idxmax`, medie ponderată |
| [Seminar04_ACP_ConsumAlimentar](Seminar04_ACP_ConsumAlimentar) | ACP pe consumul alimentar | `acp`, `tabelare_varianta`, Kaiser, procent de varianță |

## Observații despre codul profului
- **Seminar 3, cerința 2:** localitățile cu 0 angajați rămân cu NaN (celule goale în CSV), deși cerința zice „procentele vor fi 0”. Corect: `fillna(0)`, vezi [rezolvare_ciprian.py](Seminar03_IndustriaAlimentara/rezolvare_ciprian.py).
- **Seminar 3, cerința 3:** coloana se numește `Totaluri`, PDF-ul cere `Ponderi`.
- **Seminar 3:** importul `from numpy.ma.extras import average` merge, dar varianta normală e `np.average`.
- **Seminar 3, exemplul cerinței 5 din PDF** (Bucuresti-Ilfov Carne 2516.5) nu iese pe datele primite (iese 2256.56, inclusiv cu codul profului). Probabil e făcut pe altă versiune a datelor.
- **Seminar 4:** în `Varianta.csv`, C6 apare cu procent cumulat `0.8` din cauza `round(3)`. Valoarea reală e 0.79998, deci criteriul „> 80%” dă **7** componente, nu 6.
- **Seminar 4, `acp` cu `std=False`:** `np.corrcoef(x_, c)` fără `rowvar=False` corelează rândurile.
