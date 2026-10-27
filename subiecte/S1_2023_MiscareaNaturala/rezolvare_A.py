# =====================================================================
# REZOLVARE - Subiect S1_2023 (MiscareaNaturala), partea A
# Deschide fisierul DOAR dupa ce ai incercat singur.
# Structura folderului:
#   main.py (sau acest fisier)
#   data_in/MiscareaNaturala.csv
#   data_in/CoduriTariExtins.csv
# =====================================================================

import os
import pandas as pd

os.makedirs("data_out", exist_ok=True)

# ---------------------------------------------------------------------
# Citire
# Prima coloana din MiscareaNaturala.csv e Country_Number -> index_col=0
# ---------------------------------------------------------------------
df_miscare = pd.read_csv("data_in/MiscareaNaturala.csv", index_col=0)

# Coloanele: Country_Name, Three_Letter_Country_Code, FR, IM, LE, LEF, LEM, MMR, RS
# Indicatorii numerici incep de la a 3-a coloana (pozitia 2) -> [2:]
indicatori = list(df_miscare.columns.values[2:])
# ['FR', 'IM', 'LE', 'LEF', 'LEM', 'MMR', 'RS']


# =====================================================================
# CERINTA 1
# Tarile cu rata sporului natural (RS) POZITIVA, in ordinea descrescatoare
# a lui RS. Se salveaza: codul de tara (3 litere), numele tarii, RS.
# ---------------------------------------------------------------------
# CALCUL DE MANA:
#   Oman     RS = 6.773  > 0  -> PASTRAT (si e primul, are cel mai mare RS)
#   Romania  RS = -0.541 < 0  -> ELIMINAT
#   Din 182 de tari, 21 au RS <= 0 -> raman 161.
#
# PASI:
#   1. masca: df["RS"] > 0                         (filtrare, ca la seminarul 3)
#   2. selectez coloanele cerute, IN ORDINEA din exemplu
#   3. sort_values dupa "RS", descrescator, CU ATRIBUIRE
#   4. to_csv cu index=False
#
# DE CE index=False?
#   Exemplul din subiect incepe cu Three_Letter_Country_Code, NU cu
#   Country_Number. Indexul nostru e Country_Number -> nu vrem sa apara.
# =====================================================================
df_cerinta1 = df_miscare[df_miscare["RS"] > 0][["Three_Letter_Country_Code", "Country_Name", "RS"]]
df_cerinta1 = df_cerinta1.sort_values(by="RS", ascending=False)

print("Cerinta 1:", df_cerinta1.shape)        # (161, 3)
print(df_cerinta1.head(3))                    # OMN 6.773, QAT 6.473, LBN 5.536
df_cerinta1.to_csv("data_out/cerinta1.csv", index=False)


# =====================================================================
# CERINTA 2
# Valorile medii ale indicatorilor la nivel de CONTINENT, doar pentru
# continentele unde media RS pe continent > media RS la nivel mondial.
# ---------------------------------------------------------------------
# CALCUL DE MANA:
#   Media mondiala RS = suma RS a celor 182 de tari / 182 = 1.428
#
#   Oceania (10 tari):
#     AUS 1.544, SLB 2.666, FJI 0.204, KIR 1.497, VUT 2.757,
#     NZL 1.089, FSM 1.130, PNG 2.070, TON -0.625, WSM 0.798
#     suma = 13.13  ->  media = 13.13 / 10 = 1.313
#     1.313 < 1.428  -> Oceania NU intra in rezultat
#
#   Africa: media RS = 2.359 > 1.428 -> INTRA
#   Asia:   media RS = 1.961 > 1.428 -> INTRA
#   Restul continentelor sunt sub 1.428 -> raman doar Africa si Asia
#   (exact ca in exemplul din subiect).
#
# CAPCANA - media mondiala:
#   "Media la nivel mondial" = media pe cele 182 de TARI: df["RS"].mean()
#   NU media celor 6 medii de continent. Aia ar da 1.296, iar Oceania
#   (1.313) ar intra GRESIT in rezultat.
#
# CAPCANA - merge:
#   In CoduriTariExtins.csv, Country_Number e a 4-a coloana (pozitia 3),
#   nu prima! Doua variante corecte:
#     a) index_col=3 la citire, apoi merge index-index      (folosita aici)
#     b) fara index_col, apoi merge cu right_on="Country_Number"
#
# CAPCANA - coloane duplicate:
#   Ambele fisiere au Country_Name si Three_Letter_Country_Code.
#   Daca faci merge pe tot tabelul de coduri, apar Country_Name_x/_y.
#   Solutie: iei din coduri DOAR coloana de care ai nevoie: [["Continent_Name"]]
#   (la fel a facut profu' la seminarul 2: df_coduri_jud[["IndicativJudet","Regiune"]])
#
# PASI:
#   1. citesc codurile cu index_col=3
#   2. merge index-index, doar cu coloana Continent_Name -> verific shape (182, 10)
#   3. groupby("Continent_Name") pe indicatori + mean()
#   4. calculez media mondiala RS pe tabelul INITIAL (de tari)
#   5. filtrez tabelul AGREGAT: df_cont[df_cont["RS"] > media_mondiala]
#   6. to_csv (aici indexul = Continent_Name, deci il PASTREZ)
# =====================================================================
df_coduri = pd.read_csv("data_in/CoduriTariExtins.csv", index_col=3)

df_merge = df_miscare.merge(df_coduri[["Continent_Name"]], left_index=True, right_index=True)
print("\nShape dupa merge:", df_merge.shape)   # (182, 10) -> nu am pierdut nicio tara

df_continent = df_merge[indicatori + ["Continent_Name"]].groupby("Continent_Name").mean()
print(df_continent["RS"])                       # Oceania 1.313, Africa 2.359, ...

media_mondiala_rs = df_miscare["RS"].mean()
print("Media mondiala RS:", media_mondiala_rs)  # 1.428

df_cerinta2 = df_continent[df_continent["RS"] > media_mondiala_rs]
print("Cerinta 2:\n", df_cerinta2)              # Africa, Asia
df_cerinta2.to_csv("data_out/cerinta2.csv")

# Verificare cu exemplul din subiect:
#   Africa,4.5636,52.51648076923077,60.83928846153846,...,2.358673076923077  OK
#   Asia,2.6341302325581397,21.960418604651164,...,1.960906976744186       OK
