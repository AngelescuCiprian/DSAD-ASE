# Genereaza I2014.csv - date de TEST (NU reale) pentru subiectul S1_1085.
# Valorile sunt construite astfel incat TOATE exemplele din enunt sa iasa exact.
import itertools
import numpy as np
import pandas as pd

rng = np.random.default_rng(1085)
pop = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)
P = pop["Populatie"]
n = len(pop)

# --- generare de baza ---
judete = pop["Judet"].unique()
rata_judet = dict(zip(judete, rng.uniform(70, 200, len(judete))))          # salariati la 1000 loc.
urban = pop["Localitate"].str.contains("Municipiul|Oras").values
rata = pop["Judet"].map(rata_judet).values * np.where(urban, 1.6, 0.45) * rng.lognormal(0, 0.4, n)
nr_sal = np.round(P.values * rata / 1000).astype(np.int64)
fara = rng.random(n) < 0.08                                                 # localitati fara salariati
nr_sal[fara & ~urban] = 0
nr_firme = np.round(nr_sal / rng.uniform(5, 12, n) + (P.values / 400) * rng.random(n)).astype(np.int64)
productivitate = np.clip(rng.lognormal(np.log(250_000), 0.55, n), 40_000, 1_500_000)
ca = np.round(nr_sal * productivitate).astype(np.int64)
profit = np.round(ca * rng.uniform(0.03, 0.12, n)).astype(np.int64)
pierdere = np.round(ca * rng.uniform(0.01, 0.04, n)).astype(np.int64)

df = pd.DataFrame({"DenLocalitate": pop["Localitate"], "NrFirme": nr_firme, "NrSal": nr_sal,
                   "TotalCifraAfaceri": ca, "TotalProfit": profit, "TotalPierdere": pierdere},
                  index=pop.index)
ind = ["NrFirme", "NrSal", "TotalCifraAfaceri", "TotalProfit", "TotalPierdere"]

# --- cerinta 2: rata ocuparii B, IF, TM (exacte) + celelalte judete sub 249 ---
def fixeaza_total(judet, total):
    idx = pop.index[pop["Judet"] == judet]
    mare = P[idx].idxmax()
    df.loc[mare, "NrSal"] += total - df.loc[idx, "NrSal"].sum()
fixeaza_total("b", 1082794)
fixeaza_total("if", 146332)
fixeaza_total("tm", 185383)
for j in judete:
    if j in ("b", "if", "tm"):
        continue
    idx = pop.index[pop["Judet"] == j]
    r = df.loc[idx, "NrSal"].sum() / P[idx].sum() * 1000
    if r > 230:
        df.loc[idx, "NrSal"] = np.round(df.loc[idx, "NrSal"] * 220 / r).astype(np.int64)

# --- cerinta 1: Independenta si Navodari au cel mai mare raport CA/NrSal ---
df.loc[93771, ["NrSal", "TotalCifraAfaceri"]] = [125, 305595398]           # 2444763.184
df.loc[60507, ["NrSal", "TotalCifraAfaceri"]] = [5000, 12220756780]        # 2444151.356
for s in (93771, 60507):
    df.loc[s, "TotalProfit"] = round(df.loc[s, "TotalCifraAfaceri"] * 0.06)
    df.loc[s, "TotalPierdere"] = round(df.loc[s, "TotalCifraAfaceri"] * 0.02)

# --- cerinta 3: in AB, Galda De Jos are cel mai mare profit pe locuitor ---
ab = pop.index[pop["Judet"] == "ab"]
df.loc[4366, "TotalProfit"] = 180_000_000

# --- cerinta 4: mediile ponderate din AB (exacte, la 3 zecimale) ---
tinta = {"NrFirme": 946.407, "NrSal": 5690.334, "TotalCifraAfaceri": 1336997181.357,
         "TotalProfit": 113378467.612, "TotalPierdere": 31730528.39}
Pab = P[ab].astype(object)                 # intregi Python -> aritmetica exacta
S = sum(Pab)
alba = 1017
fin = [s for s in P[ab].sort_values().index if 1500 <= P[s] <= 6000 and s != 4366][:2]
for col, t in tinta.items():
    def media():
        return np.average(df.loc[ab, col].astype(float), weights=P[ab])
    # 1) grosier: Alba Iulia
    rest = round(t * S) - sum(int(df.loc[s, col]) * Pab[s] for s in ab if s != alba)
    df.loc[alba, col] = rest // Pab[alba]
    # 2) fin: doua localitati mijlocii, cautare pe o grila de valori intregi
    r = round(t * S) - sum(int(df.loc[s, col]) * Pab[s] for s in ab)
    p1, p2 = int(P[fin[0]]), int(P[fin[1]])
    cand = sorted(itertools.product(range(-80, 81), repeat=2), key=lambda bc: abs(r - bc[0] * p1 - bc[1] * p2))
    baza = df.loc[fin, col].copy()
    for b, c in cand[:200]:
        df.loc[fin[0], col] = baza.iloc[0] + b
        df.loc[fin[1], col] = baza.iloc[1] + c
        if round(media(), 3) == t:
            break
    assert round(media(), 3) == t, col

df.to_csv("data_in/I2014.csv")
print("I2014.csv generat:", df.shape)
