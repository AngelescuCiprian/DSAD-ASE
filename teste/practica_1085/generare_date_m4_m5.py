# Genereaza datele de TEST (NU reale) pentru modelele M4 si M5.
# Ruleaza din folderul practica_1085:  python generare_date_m4_m5.py
import numpy as np
import pandas as pd

pop = pd.read_csv("M4_Turism/data_in/PopulatieLocalitati.csv", index_col=0)
P = pop["Populatie"].values.astype(float)
n = len(pop)
urban = pop["Localitate"].str.contains("Municipiul|Oras").values
judete = pop["Judet"].unique()


def jud_factor(rng, lo, hi):
    return pop["Judet"].map(dict(zip(judete, rng.uniform(lo, hi, len(judete))))).values


# ---------------- M4 Turism: locuri de cazare pe tipuri ----------------
rng = np.random.default_rng(4)
tipuri = ["Hotel", "Pensiune", "Vila", "Camping", "Hostel"]
turistic = jud_factor(rng, 0.3, 2.5) * rng.lognormal(0, 0.9, n)          # cat de turistica e localitatea
are_cazare = urban | (rng.random(n) < 0.35 * np.minimum(turistic, 2))
# fiecare judet are propriul "profil" de cazare (ca sa difere tipul dominant)
profil = {j: rng.dirichlet([3, 3, 1.2, 0.8, 0.7]) for j in judete}
w = np.array([profil[j] for j in pop["Judet"]])
w[urban] = w[urban] * [3, 0.6, 0.8, 0.3, 1.5]                             # la oras mai multe hoteluri
w = w / w.sum(axis=1, keepdims=True)
cap_tot = P * np.where(urban, 0.012, 0.02) * turistic
locuri = np.zeros((n, 5))
for i in np.where(are_cazare)[0]:
    locuri[i] = rng.multinomial(int(max(cap_tot[i], 8)), w[i])
locuri[:, 4][~urban] = 0                                                  # hosteluri doar la oras
df4 = pd.DataFrame(locuri.astype(int), columns=tipuri, index=pop.index)
df4.insert(0, "Localitate", pop["Localitate"])
df4.to_csv("M4_Turism/data_in/Turism.csv")

# ---------------- M5 Energie: consum anual (MWh) 2019-2023 ----------------
rng = np.random.default_rng(5)
ani = ["2019", "2020", "2021", "2022", "2023"]
baza = P * np.where(urban, 2.4, 1.1) * jud_factor(rng, 0.7, 1.4) * rng.lognormal(0, 0.3, n)
trend = np.array([1.0, 0.94, 1.03, 0.97, 1.01])
jud_an = {j: rng.uniform(0.85, 1.15, 5) for j in judete}                  # socuri pe judet si an
ja = np.array([jud_an[j] for j in pop["Judet"]])
consum = baza[:, None] * trend * ja * rng.uniform(0.9, 1.1, (n, 5))
consum = np.round(consum, 2)
# capcana: localitati fara date intr-un an (consum 0) -> nu intra la cerinta 1
lipsa = np.where(~urban & (rng.random(n) < 0.05))[0]
consum[lipsa, rng.integers(0, 5, len(lipsa))] = 0.0
df5 = pd.DataFrame(consum, columns=ani, index=pop.index)
df5.insert(0, "Localitate", pop["Localitate"])
df5.to_csv("M5_Energie/data_in/Energie.csv")
print("Date generate.")
