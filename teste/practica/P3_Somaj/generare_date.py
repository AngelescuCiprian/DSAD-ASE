# Genereaza Somaj.csv (date de test, NU reale): numarul de someri pe localitate, 2015-2023.
import numpy as np, pandas as pd
rng = np.random.default_rng(2026)
pop = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)
ani = [str(a) for a in range(2015, 2024)]
trend = np.array([0.95, 0.98, 0.90, 0.85, 0.80, 1.00, 0.97, 0.88, 0.84])     # scade, salt in 2020
judete = pop["Judet"].unique()
rata_judet = dict(zip(judete, rng.uniform(0.02, 0.09, len(judete))))
rata_loc = pop["Judet"].map(rata_judet).values * rng.lognormal(0, 0.35, len(pop))
activi = pop["Populatie"].values * 0.6
val = np.outer(activi * rata_loc, trend) * rng.normal(1, 0.10, (len(pop), len(ani)))
val = np.round(np.clip(val, 0, None)).astype(int)
fara = rng.choice(len(pop), 25, replace=False)          # cateva localitati fara someri in toata perioada
val[fara, :] = 0
df = pd.DataFrame(val, index=pop.index, columns=ani)
df.insert(0, "Localitate", pop["Localitate"])
df.to_csv("data_in/Somaj.csv")
