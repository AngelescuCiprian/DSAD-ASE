# Modele de practică pe tiparul testului S1_1085

3 modele construite după subiectul dat de prof anul acesta ([S1_1085_Firme](../S1_1085_Firme)): **4 cerințe (2 + 2 + 2 + 3 puncte) + 1 din oficiu**, aceleași tipare, de fiecare dată cu altă „răsucire”.

| Tipar din test | M1 Agricultură | M2 Sănătate | M3 Comerț |
|---|---|---|---|
| 1. raport pe localitate, **doar unde numitorul > 0**, desc. | producție / hectar | internări / pat | vânzări / angajat |
| 2. rată **la 1000 de locuitori**, desc. | ferme, pe județ | medici, pe județ | angajați, pe **regiune** (2 merge-uri) |
| 3. maxim „pe locuitor” în grup → **nume** | subvenții pe **hectar** (filtru!) | cheltuieli/loc + **valoarea** | **județul** cu max pe regiune (2 niveluri) |
| 4. **medie ponderată** pe grup (3p) | ponderea = **suprafața**, nu populația | ponderea = populația (identic cu testul) | pe **regiune** |

**Ordinea recomandată:** M2 (cel mai apropiat de test) → M1 → M3 (cel mai greu).
Date de **test** generate ([generare_date.py](generare_date.py)), populația și codurile de județ sunt reale. În fiecare set există câteva localități cu numărătorul > 0 și numitorul 0: dacă uiți filtrul la cerința 1, primul rând iese `inf`.
