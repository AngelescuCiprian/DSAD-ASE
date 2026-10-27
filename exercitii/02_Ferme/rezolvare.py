# =====================================================================
# REZOLVARI - Exercitii ferme agricole
# Deschide fisierul DOAR dupa ce ai incercat singur fiecare cerinta.
# Ruleaza-l din acelasi folder in care ai data_in/ si compara cu outputul tau.
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

# ---------------------------------------------------------------------
# Citire (MEREU index_col=0 cand prima coloana e un cod)
# ---------------------------------------------------------------------
df_productie = pd.read_csv("data_in/Productie.csv", index_col=0)
culturi = list(df_productie.columns.values[1:])    # ['Grau', 'Porumb', 'Floarea', 'Rapita']


# =====================================================================
# CERINTA 1
# Pentru fermele cu productie totala > 0: productia totala si cultura
# principala (cultura cu cea mai mare productie).
# Output: CodFerma, Ferma, Total, CulturaPrincipala
# ---------------------------------------------------------------------
# CALCUL DE MANA - Agro Lugoj (734):
#   Grau 600, Porumb 900, Floarea 200, Rapita 100
#   Total = 600 + 900 + 200 + 100 = 1800
#   Maximul e 900 -> pe coloana Porumb -> CulturaPrincipala = Porumb
#
# Holde Pecica (481) are 0 peste tot -> total 0 -> NU apare in output.
#
# IDEI FOLOSITE:
#   - sum(axis=1)     -> un total pe fiecare RAND (ferma)
#   - df[masca]       -> filtrare
#   - idxmax(axis=1)  -> ETICHETA (numele coloanei) cu maximul, pe fiecare rand
# =====================================================================
totaluri = df_productie[culturi].sum(axis=1)

df_cerinta1 = df_productie[totaluri > 0][["Ferma"]].copy()    # [[...]] -> DataFrame, nu Series
df_cerinta1["Total"] = totaluri[totaluri > 0]
df_cerinta1["CulturaPrincipala"] = df_productie.loc[totaluri > 0, culturi].idxmax(axis=1)

print("Cerinta 1:\n", df_cerinta1, "\n")
df_cerinta1.to_csv("data_out/Cerinta1.csv")

# NOTA: de ce .copy()? Fara el, pandas poate da un warning
# (SettingWithCopyWarning) cand adaugi coloane pe o "felie" din alt tabel.
# Varianta alternativa, fara copy: construiesti direct cu insert sau cu
# pd.DataFrame({...}). Important e rezultatul.
#
# NOTA 2: de ce idxmax doar pe culturi? Daca il aplici pe tot randul,
# intra si coloana "Ferma" (text) si da eroare/rezultat aiurea.


# =====================================================================
# CERINTA 2
# Randamentul (tone / hectar) la nivel de judet, sortat descrescator.
# Output: Judet, Randament
# ---------------------------------------------------------------------
# CALCUL DE MANA - Timis (tm), 3 ferme:
#   Agro Lugoj (734)        total 1800 t,  450 ha
#   Ferma Sannicolau (215)  total 2500 t,  500 ha
#   Campia Banatului (908)  total 1700 t,  350 ha
#   ----------------------------------------------
#   tm                      6000 t      1300 ha
#   Randament tm = 6000 / 1300 = 4.615 t/ha
#
# CAPCANA: NU calculezi randamentul pe ferma si apoi faci media.
#   Aduni intai tonele si hectarele pe judet, ABIA APOI imparti.
#
# IDEI FOLOSITE:
#   - merge index-index (CodFerma e index in ambele)
#   - verificare shape dupa merge -> trebuie 14 randuri
#   - groupby("Judet") pe [Judet, Total, Hectare] + sum()
#   - impartire coloana / coloana
#   - sort_values CU atribuire
#   - .name pentru numele coloanei din CSV
# =====================================================================
df_ferme = pd.read_csv("data_in/Ferme.csv", index_col=0)

df_productie["Total"] = totaluri
df_merge = df_productie.merge(df_ferme, left_index=True, right_index=True)
print("Shape dupa merge:", df_merge.shape)            # (14, 9)
# Coloana "Ferma" apare in ambele fisiere -> devine Ferma_x si Ferma_y. E normal.

df_jud = df_merge[["Judet", "Total", "Hectare"]].groupby("Judet").sum()
print(df_jud.loc["tm"])                                # Total 6000, Hectare 1300

s_cerinta2 = df_jud["Total"] / df_jud["Hectare"]
s_cerinta2 = s_cerinta2.sort_values(ascending=False)   # ATRIBUIRE!
s_cerinta2.name = "Randament"

print("Cerinta 2:\n", s_cerinta2, "\n")
s_cerinta2.to_csv("data_out/Cerinta2.csv")
# Rezultat: tm 4.615 primul, ar 2.667 ultimul.
# ar e ultimul pentru ca Holde Pecica are 150 ha si 0 productie -> trage
# randamentul judetului in jos (1200 t / 450 ha).


# =====================================================================
# CERINTA 3
# Structura productiei pe regiuni: procentul fiecarei culturi din
# productia totala a regiunii.
# Output: Regiune, Grau, Porumb, Floarea, Rapita (procente)
# ---------------------------------------------------------------------
# CALCUL DE MANA - Vest (tm + ar, 5 ferme):
#   Grau   = 600 + 1200 + 400 + 500 + 0 = 2700
#   Porumb = 900 +  800 + 1100 + 300 + 0 = 3100
#   Floarea= 200 +  300 + 150 + 400 + 0 = 1050
#   Rapita = 100 +  200 +  50 +   0 + 0 =  350
#   Total Vest = 2700 + 3100 + 1050 + 350 = 7200
#
#   Grau   = 2700 * 100 / 7200 = 37.50 %
#   Porumb = 3100 * 100 / 7200 = 43.06 %
#   Floarea= 1050 * 100 / 7200 = 14.58 %
#   Rapita =  350 * 100 / 7200 =  4.86 %
#   Suma = 100 %  ✓
#
# CAPCANA (aceeasi ca la cerinta 2, alta forma):
#   Daca iei procentele de la nivel de ferma (ca la Cerinta 2 de la
#   seminar) si faci media pe regiune, la Vest-Grau iti iese 29.31 %,
#   nu 37.50 %. GRESIT. Procentele nu se mediaza - aduni tonele brute
#   pe regiune, apoi calculezi procentul.
#
# IDEI FOLOSITE:
#   - merge cu cheia in COLOANA in stanga si in INDEX in dreapta:
#       left_on="Judet", right_index=True
#   - groupby("Regiune") pe culturi + sum()
#   - apply(lambda x: x*100/x.sum(), axis=1) pe tabelul agregat
#     (aceeasi formula ca la Cerinta 2 de la seminar, doar ca pe regiuni)
# =====================================================================
df_judete = pd.read_csv("data_in/Judete.csv", index_col=0)

# In stanga, judetul e COLOANA "Judet"; in dreapta e INDEXUL (IndicativJudet)
df_merge_reg = df_merge.merge(df_judete, left_on="Judet", right_index=True)
print("Shape dupa merge cu regiuni:", df_merge_reg.shape)   # (14, 11)
print(df_merge_reg.loc[734, ["Judet", "Regiune"]])           # tm, Vest

df_reg = df_merge_reg[culturi + ["Regiune"]].groupby("Regiune").sum()
print(df_reg)                                                 # Vest: 2700 3100 1050 350

df_cerinta3 = df_reg.apply(lambda x: x * 100 / x.sum(), axis=1)
# Aici nu e nevoie de fillna: nicio regiune nu are total 0.
# (Daca ar putea avea, adaugi df_cerinta3 = df_cerinta3.fillna(0).)

print("Cerinta 3:\n", df_cerinta3.round(2), "\n")
df_cerinta3.to_csv("data_out/Cerinta3.csv")
# Rezultat:
#   Sud       Grau 39.58  Porumb 27.08  Floarea 20.83  Rapita 12.50
#   Sud-Vest  Grau 27.88  Porumb 45.19  Floarea 22.12  Rapita  4.81
#   Vest      Grau 37.50  Porumb 43.06  Floarea 14.58  Rapita  4.86
