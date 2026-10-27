# DSAD – Dispozitive Software pentru Analiza Datelor (ASE, CSIE)

Materiale de studiu pentru DSAD: seminariile cu profesorul, subiecte din anii trecuți (enunțuri, date, rezolvări explicate), exerciții de antrenament și fițuici.

> Rezolvările sunt scrise în stilul de la seminar (pandas + numpy, `index_col`, `merge`, `groupby`, funcțiile `acp` / `tabelare_varianta` ale profului) și sunt **verificate**: output-ul coincide cu exemplele din enunțuri.

## Structura

```
DSAD-ASE/
├── docs/
│   ├── CHEATSHEET_pandas.md      ← tot ce trebuie pentru partea A (merge, groupby, axis, capcane)
│   └── ACP_explicat.md           ← Analiza în Componente Principale, de la zero
├── seminarii/
│   ├── Seminar02_Etnii/          ← merge, groupby, procente (Tema2_1)
│   ├── Seminar03_IndustriaAlimentara/   ← Tema2_4 + rezolvarea mea (rezolvare_ciprian.py)
│   └── Seminar04_ACP_ConsumAlimentar/   ← primul seminar de ACP
├── subiecte/
│   ├── README.md                 ← TIPARUL subiectelor + toate cerințele A ordonate pe tipuri
│   ├── S1_2023_MiscareaNaturala/ ← enunț + date + rezolvare A + B (ACP)
│   ├── S1_MiscareaNaturala/      ← enunț + date + rezolvare A + B (Ward)
│   ├── S2_Emissions/             ← enunț + date + rezolvare A + B (ACP)
│   ├── S2_2024_GlobalIndicators/ ← enunț + date + rezolvare A + B (Ward)
│   ├── poze_fara_date/           ← subiecte doar din poze (cerințe transcrise, fără date)
│   └── poze_originale/           ← pozele exact cum le-am făcut
├── exercitii/
│   ├── 01_Magazine/              ← antrenament partea A (filtrare, procente, merge, groupby)
│   └── 02_Ferme/                 ← antrenament partea A, cu rezolvare explicată
└── din_D_DSAD/                   ← conținutul folderului D:\DSAD (subiecte rezolvate pe toate metodele, fițuici)
```

## Cum rulezi o rezolvare

Fiecare folder de subiect e un proiect de sine stătător (are `data_in/`, `functii.py`, `grafice.py`):

```bash
cd subiecte/S1_2023_MiscareaNaturala
python rezolvare_A.py     # scrie în data_out/
python rezolvare_B.py     # scrie în data_out/ + deschide graficele (le salvează și ca PNG)
```

Pachete: `pandas`, `numpy`, `matplotlib`, `scipy`, `scikit-learn`.

## Tiparul subiectului (pe scurt)

| Parte | Puncte | Ce e |
|---|---|---|
| A1 | 1–2 | un fișier, fără merge: filtrare / calcul pe rând / pe coloană |
| A2 | 2 | **merge** cu fișierul de coduri + **groupby** pe nivel superior |
| B | 5 | ACP / analiză de clusteri (Ward) / analiză factorială / LDA |
| C | 1 | mini-problemă de teorie (valori proprii, comunalități, KMO) |
| oficiu | 1 | |

A + oficiu = 5 puncte. Detalii și toate cerințele ordonate pe tipuri: [subiecte/README.md](subiecte/README.md).

