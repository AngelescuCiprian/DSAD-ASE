# Genereaza datele de TEST (NU reale) pentru cele 3 modele de practica.
# Ruleaza din folderul practica_1085:  python generare_date.py
import numpy as np
import pandas as pd

pop = pd.read_csv("M1_Agricultura/data_in/PopulatieLocalitati.csv", index_col=0)
P = pop["Populatie"].values.astype(float)
n = len(pop)
urban = pop["Localitate"].str.contains("Municipiul|Oras").values


def jud_factor(rng, lo, hi):
    j = pop["Judet"].unique()
    return pop["Judet"].map(dict(zip(j, rng.uniform(lo, hi, len(j))))).values


# ---------------- M1 Agricultura ----------------
rng = np.random.default_rng(1)
sup = np.round(P * np.where(urban, 0.05, 0.9) * jud_factor(rng, 0.4, 1.8) * rng.lognormal(0, 0.5, n), 1)
sup[(rng.random(n) < 0.05) | (pop["Judet"].values == "b")] = 0.0          # fara teren agricol
ferme = np.round(sup / rng.uniform(4, 25, n) + rng.integers(0, 4, n)).astype(int)
productie = np.round(sup * rng.uniform(2.5, 7.5, n), 1)
animale = np.round(sup * rng.uniform(0, 1.5, n) + P * 0.02 * rng.random(n)).astype(int)
subventii = np.round(sup * rng.uniform(150, 420, n))
# cateva localitati cu subventii/productie dar fara suprafata inregistrata (capcana: impartire la 0)
idx0 = rng.choice(np.where(sup == 0)[0], 15, replace=False)
productie[idx0] = np.round(rng.uniform(50, 400, 15), 1)
subventii[idx0] = np.round(rng.uniform(5000, 60000, 15))
pd.DataFrame({"Localitate": pop["Localitate"], "NrFerme": ferme, "SuprafataHa": sup,
              "ProductieTone": productie, "NrAnimale": animale, "Subventii": subventii},
             index=pop.index).to_csv("M1_Agricultura/data_in/Agricultura.csv")

# ---------------- M2 Sanatate ----------------
rng = np.random.default_rng(2)
paturi = np.round(P * np.where(urban, 9, 0.3) / 1000 * rng.lognormal(0, 0.5, n)).astype(int)
paturi[~urban & (rng.random(n) < 0.85)] = 0
paturi = np.where(paturi > 0, np.maximum(paturi, 12), 0)                     # spitale de cel putin 12 paturi
medici = np.round(P * np.where(urban, 3.2, 0.6) / 1000 * jud_factor(rng, 0.6, 1.6) * rng.lognormal(0, 0.4, n)).astype(int)
farmacii = np.round(P / np.where(urban, 3500, 6000) * rng.lognormal(0, 0.4, n)).astype(int)
internari = np.round(paturi * rng.uniform(15, 45, n) + rng.integers(0, 40, n) * (paturi > 0)).astype(int)
cheltuieli = np.round(medici * rng.uniform(150_000, 400_000, n) + paturi * rng.uniform(80_000, 200_000, n))
idx0 = rng.choice(np.where(paturi == 0)[0], 20, replace=False)                # internari de zi fara paturi
internari[idx0] = rng.integers(20, 300, 20)
pd.DataFrame({"Localitate": pop["Localitate"], "NrMedici": medici, "NrPaturi": paturi,
              "NrFarmacii": farmacii, "Internari": internari, "Cheltuieli": cheltuieli},
             index=pop.index).to_csv("M2_Sanatate/data_in/Sanatate.csv")

# ---------------- M3 Comert ----------------
rng = np.random.default_rng(3)
angajati = np.round(P * np.where(urban, 45, 9) / 1000 * jud_factor(rng, 0.6, 1.5) * rng.lognormal(0, 0.5, n)).astype(int)
angajati[~urban & (rng.random(n) < 0.06)] = 0
magazine = np.round(angajati / rng.uniform(3, 9, n) + rng.integers(0, 3, n)).astype(int)
vanzari = np.round(angajati * rng.lognormal(np.log(420_000), 0.45, n))
chirii = np.round(vanzari * rng.uniform(0.04, 0.12, n))
idx0 = rng.choice(np.where(angajati == 0)[0], 15, replace=False)              # PFA-uri fara angajati
vanzari[idx0] = np.round(rng.uniform(80_000, 900_000, 15))
pd.DataFrame({"Localitate": pop["Localitate"], "NrMagazine": magazine, "NrAngajati": angajati,
              "Vanzari": vanzari, "Chirii": chirii},
             index=pop.index).to_csv("M3_Comert/data_in/Comert.csv")
print("Date generate.")
