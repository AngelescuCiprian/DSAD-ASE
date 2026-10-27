# Subiecte – tiparul și cerințele ordonate

9 subiecte distincte: 4 din PDF-uri (cu date) + 5 din poze (fără date).

| Folder | Date | A1 | A2 | B | C |
|---|---|---|---|---|---|
| [S1_2023_MiscareaNaturala](S1_2023_MiscareaNaturala) | ✅ | filtrare RS > 0 | medii pe continent + filtru | ACP | – |
| [S1_MiscareaNaturala](S1_MiscareaNaturala) | ✅ | filtrare RS < media | țara cu max pe continent | Ward | – |
| [S2_Emissions](S2_Emissions) | ✅ | total pe rând (+ conversie) | medie **ponderată** pe regiune | ACP | – |
| [S2_2024_GlobalIndicators](S2_2024_GlobalIndicators) | ✅ | ramura dominantă (`idxmax`) | medii pe continent | Ward + Silhouette | – |
| [Diversitate_v1](poze_fara_date/Diversitate_v1_AnalizaFactoriala) | ❌ | localități cu 0 în cel puțin un an | localitatea cu media max pe județ | Analiză factorială | comunalități ACP |
| [Diversitate_v2](poze_fara_date/Diversitate_v2_Ward) | ❌ | media pe rând, sortată | nr. localități cu 0, pe județ și an | Ward | factori specifici |
| [CalitateaAerului_v1](poze_fara_date/CalitateaAerului_v1_ACP) | ❌ | CV pe indicator (`axis=0`) | indicatorul cu CV max pe continent | ACP | LDA (✅ rezolvat) |
| [CalitateaAerului_v2](poze_fara_date/CalitateaAerului_v2_Ward) | ❌ | țara cu max pe indicator | țara cu max pe continent | Ward | KMO |
| [E_NSAL](poze_fara_date/E_NSAL_Discriminanta) | ❌ | anul cu max angajați | rata ocupării pe județ și an | LDA | Kaiser |

**Partea B:** Ward 4×, ACP 3×, analiză factorială 1×, LDA 1×.

---

## Toate cerințele A, pe tipare (de la ușor la greu)

### A1 – un singur fișier

| Tipar | Subiect | Cerința | Concept |
|---|---|---|---|
| Filtrare + sortare | S1_2023 | țări cu RS > 0, desc. | `df[masca]`, `sort_values` |
| | S1 | țări cu RS < media globală, desc. | masca față de `.mean()` |
| | Diversitate v1 | localități cu 0 în cel puțin un an | `(df[ani] == 0).any(axis=1)` |
| Calcul pe rând | Diversitate v2 | media pe ani, desc. | `mean(axis=1)` |
| | S2 | emisii totale în tone | `sum(axis=1)` + ×1000 la 2 coloane |
| Maxim pe rând | S2_2024 | ramura dominantă | `idxmax(axis=1)` |
| | E_NSAL | anul cu cei mai mulți angajați | `idxmax(axis=1)` |
| Calcul pe coloană | CalitAer v1 | coeficientul de variație pe indicator | `std / mean`, **axis=0** |
| | CalitAer v2 | țara cu max pe fiecare indicator | `idxmax(axis=0)` |

### A2 – merge + groupby

| Tipar | Subiect | Cerința | Concept |
|---|---|---|---|
| Medie pe grup | S2_2024 | media indicatorilor pe continent | `groupby().mean()` |
| | S1_2023 | idem, doar continentele peste media mondială | filtru pe tabelul agregat |
| Numărare pe grup | Diversitate v2 | câte localități cu 0, pe județ și an | `(df[ani]==0)` + `groupby().sum()` |
| Sumă + raport | E_NSAL | angajați / populație pe județ și an + media | `groupby().sum()`, `div(axis=0)` |
| Medie ponderată | S2 | medii pe regiune, ponderi = populația | `groupby().apply(np.average)` |
| Maxim în grup | S1 | codul țării cu max, pe continent | `groupby().idxmax()` + `map` |
| | Diversitate v1 | localitatea cu media max pe județ | `groupby` + `idxmax` |
| | CalitAer v1 | indicatorul cu CV max pe continent | `groupby().apply(cv)` + `idxmax` |
| | CalitAer v2 | țara cu max pe continent, pe indicator | ca la S1 |

**Ordinea de exersat:** S1_2023 → S2_2024 → S1 → S2 → subiectele din poze.

## Capcane care apar în subiecte

1. **Cheia de legătură nu e mereu prima coloană** (ex. `CoduriTariExtins.csv`: `Country_Number` e a 4-a → `index_col=3`).
2. **Coloane duplicate la merge** (`Country`, `Country_Name`) → iei din coduri doar ce-ți trebuie: `df_coduri[["Continent"]]`.
3. **„Media mondială” = media pe țări**, nu media mediilor de continent.
4. **Unități de măsură** (S2: GreenGE/GreenGIE în mii de tone).
5. **Media ponderată ≠ media simplă** (S2).
6. **Index în output:** dacă exemplul nu începe cu cheia, `to_csv(..., index=False)`.
7. **Merge-ul inner pierde rânduri** fără pereche (S2_2024: 4 țări fără continent). Verifică mereu `shape`.
