# Modele de practică pe tiparul testului S1_1085

5 modele construite după subiectul dat de prof anul acesta ([S1_1085_Firme](../S1_1085_Firme)): **4 cerințe (2 + 2 + 2 + 3 puncte) + 1 din oficiu**, aceleași tipare, de fiecare dată cu altă „răsucire”.

| Tipar din test | M1 Agricultură | M2 Sănătate | M3 Comerț |
|---|---|---|---|
| 1. raport pe localitate, **doar unde numitorul > 0**, desc. | producție / hectar | internări / pat | vânzări / angajat |
| 2. rată **la 1000 de locuitori**, desc. | ferme, pe județ | medici, pe județ | angajați, pe **regiune** (2 merge-uri) |
| 3. maxim „pe locuitor” în grup → **nume** | subvenții pe **hectar** (filtru!) | cheltuieli/loc + **valoarea** | **județul** cu max pe regiune (2 niveluri) |
| 4. **medie ponderată** pe grup (3p) | ponderea = **suprafața**, nu populația | ponderea = populația (identic cu testul) | pe **regiune** |

**Ultimele 2 modele** acoperă ce n-ai exersat încă din seminarii (în caz că testul nu seamănă cu S1_1085):

| | [M4 Turism](M4_Turism) – tiparul **seminarului 3** | [M5 Energie](M5_Energie) – tiparul **S2_1091** (date pe ani) |
|---|---|---|
| 1 | total pe rând `sum(axis=1)` + filtru | medie pe rând, doar rândurile **fără niciun 0** (`.all(axis=1)`) |
| 2 | procente pe rând, **0 dacă totalul e 0** (`fillna(0)`) | anul cu maximul: `idxmax(axis=1)` |
| 3 | tipul dominant pe județ: sume, apoi `idxmax(axis=1)` | consum pe locuitor pe județ și an: `div(axis=0)` + conversie MWh → kWh |
| 4 (3p) | **indicele de localizare** (seminar 3, cerința 6) | județul cu maximul pe **regiune și an**: `groupby()[ani].idxmax()` |

**Ordinea recomandată:** M2 (cel mai apropiat de test) → M1 → M3 (cel mai greu) → M4 → M5.
Date de **test** generate ([generare_date.py](generare_date.py), [generare_date_m4_m5.py](generare_date_m4_m5.py)), populația și codurile de județ sunt reale. În fiecare set există câteva localități cu numărătorul > 0 și numitorul 0: dacă uiți filtrul la cerința 1, primul rând iese `inf`.
