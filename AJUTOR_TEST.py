"""

 Ruleaza:   python AJUTOR_TEST.py            -> toate sectiunile
            python AJUTOR_TEST.py 6 13       -> doar sectiunile 6 si 13
 Fiecare sectiune ruleaza pe un MINI-tabel (7 localitati, 4 judete) ca sa
 VEZI ce iese din fiecare operatie. Copiezi sablonul, schimbi numele coloanelor.

 CUPRINS (cauta "# [nr]" in fisier)
   LOCALITATE  [1] raport cu filtru (numitor > 0)    [2] total pe rand + filtru
               [3] procente pe rand, 0 unde total=0  [4] medie pe rand / all / any
               [5] coloana cu maximul pe rand (+ filtru "dominanta == X")
   GRUP        [6] rata la 1000 loc (judet/regiune)  [7] tipul dominant pe judet
               [8] pe judet SI pe ani (div axis=0)   [9] procente pe judet
   CINE E MAX  [10] localitatea cu max pe judet      [11] judetul cu max pe regiune
               [12] groupby().idxmax() pe fiecare coloana / an
   AVANSAT     [13] medie ponderata                  [14] coeficient de variatie
               [15] indice de localizare             [16] rand / coloana de total
   FINAL       [17] formatarea output-ului           [18] valori lipsa (NaN)
               [19] diagnostic: arata(x), verifica_exemplu(...)

 CAND NU-TI IESE  (simptom -> cauza -> fix)
   primul rand e inf         -> n-ai filtrat numitorul > 0     -> df[df["B"] > 0] INAINTE de impartire
   tot NaN dupa impartire    -> df / serie aliniaza pe COLOANE -> df.div(serie, axis=0)
   tot NaN la df.div(df2)    -> ai [["X"]] (DataFrame)         -> foloseste ["X"] (Series)
   valori prea mari pe grup  -> ai adunat RAPOARTE             -> aduni brutele, apoi imparti
   media ponderata = sume    -> ai agregat inainte de apply    -> dai LOCALITATILE la groupby().apply
   KeyError: 'Judet'         -> coloana a devenit index        -> df.index / reset_index()
   TypeError la sum/idxmax   -> ai o coloana TEXT in groupby   -> selecteaza doar numerice + cheia
   merge cu 0 randuri        -> chei diferite (ab vs AB, index vs coloana) -> print(df.head()) la ambele
   lipseste o coloana (c3511)-> [1:] desi cheia e deja index   -> list(df.columns.values) fara [1:]
   NoneType has no attribute -> x = x.metoda(..., inplace=True)-> fara inplace SAU fara atribuire
   ZeroDivisionError average -> grup cu suma ponderilor 0      -> filtreaza ponderea > 0 inainte
   ImportError: rezolvare    -> PyCharm a pus singur un import -> sterge linia "from ... import"

 SCHELET (copiaza-l la inceputul testului)
   import os
   import numpy as np
   import pandas as pd
   os.makedirs("data_out", exist_ok=True)
   df = pd.read_csv("data_in/Date.csv", index_col=0)                 # PRIMA coloana = cheia
   ind = list(df.columns.values[1:])                                  # sari peste nume (Localitate)
   df_pop = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)
   df_coduri = pd.read_csv("data_in/Coduri_Judete.csv", index_col=0)  # uita-te la PRIMUL rand!
   df_merge = df.merge(df_pop[["Judet", "Populatie"]], left_index=True, right_index=True)
   df_merge = df_merge.merge(df_coduri[["Regiune"]], left_on="Judet", right_index=True)
   print(df_merge.shape)

 MERGE: cheia stanga / dreapta
   index   / index    -> left_index=True, right_index=True
   coloana / index    -> left_on="Judet", right_index=True
   index   / coloana  -> left_index=True, right_on="IndicativJudet"   (Coduri_Judete din S2 are NrCrt primul)
   coloana / coloana  -> left_on="A", right_on="B"
=====================================================================
"""
import sys

import numpy as np
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


# =====================================================================
# MINI-DATE (in loc de CSV) - aceleasi forme ca la test
# =====================================================================
def date_demo():
    # Date.csv: index = Siruta, prima coloana = Localitate, apoi indicatorii
    df = pd.DataFrame({
        "Siruta": [101, 102, 103, 201, 202, 301, 401],
        "Localitate": ["Oras1", "Sat1", "Sat2", "Oras2", "Sat3", "Oras3", "Oras4"],
        "A": [50, 0, 30, 80, 5, 100, 20],
        "B": [10, 0, 0, 40, 5, 20, 30],      # Sat1 si Sat2 au B = 0 -> capcana la impartire
        "C": [40, 0, 10, 0, 10, 60, 5],      # Sat1 are TOTUL 0 -> capcana la procente
    }).set_index("Siruta")
    df_pop = pd.DataFrame({
        "Siruta": [101, 102, 103, 201, 202, 301, 401],
        "Judet": ["ab", "ab", "ab", "cj", "cj", "b", "bv"],
        "Populatie": [60000, 2000, 3000, 300000, 4000, 1800000, 250000],
    }).set_index("Siruta")
    df_coduri = pd.DataFrame({
        "IndicativJudet": ["ab", "bv", "cj", "b"],
        "Regiune": ["Centru", "Centru", "Nord-Vest", "Bucuresti-Ilfov"],
    }).set_index("IndicativJudet")
    # date pe ANI (ca la S2_1091 / M5): coloanele sunt texte "2021", "2022", ...
    df_ani = pd.DataFrame({
        "Siruta": [101, 102, 103, 201, 202, 301, 401],
        "Localitate": ["Oras1", "Sat1", "Sat2", "Oras2", "Sat3", "Oras3", "Oras4"],
        "2021": [100.0, 5.0, 8.0, 400.0, 6.0, 2000.0, 300.0],
        "2022": [120.0, 0.0, 9.0, 380.0, 7.0, 2100.0, 310.0],   # Sat1 fara date in 2022
        "2023": [110.0, 6.0, 7.0, 420.0, 5.0, 1900.0, 330.0],
    }).set_index("Siruta")
    return df, df_pop, df_coduri, df_ani


df, df_pop, df_coduri, df_ani = date_demo()
ind = list(df.columns.values[1:])                  # ['A', 'B', 'C']
ani = list(df_ani.columns.values[1:])              # ['2021', '2022', '2023']
df_merge = df.merge(df_pop[["Judet", "Populatie"]], left_index=True, right_index=True)
df_merge = df_merge.merge(df_coduri[["Regiune"]], left_on="Judet", right_index=True)


def titlu(t):
    print("\n" + "=" * 70 + "\n" + t + "\n" + "=" * 70)


# =====================================================================
# [1] RAPORT PE LOCALITATE, DOAR UNDE NUMITORUL > 0, DESCRESCATOR
#     "pentru localitatile care AU salariati/paturi/angajati"
# =====================================================================
def s1():
    titlu("[1] Raport A/B doar unde B > 0, descrescator")
    df_f = df[df["B"] > 0]                              # FILTRU INAINTE (altfel A/0 = inf)
    out = df_f[["Localitate"]].copy()                   # [[ ]] -> DataFrame, poti adauga coloane
    out["A/B"] = df_f["A"] / df_f["B"]
    out = out.sort_values(by="A/B", ascending=False)    # ATRIBUIE!
    print(out)
    print("\nFara filtru -> Sat2 are inf si iese PRIMUL:")
    print((df["A"] / df["B"]).sort_values(ascending=False).head(2))
    # out.to_csv("data_out/Cerinta1.csv")


# =====================================================================
# [2] TOTAL PE RAND + FILTRU "total > 0"   (Seminar 3, cerinta 1)
# =====================================================================
def s2():
    titlu("[2] Total pe rand + doar localitatile cu total > 0")
    s_total = df[ind].sum(axis=1)                       # axis=1 = pe RAND
    print(df[s_total > 0])                               # aceleasi coloane ca fisierul
    print("\nCu coloana Total, sortat:")
    out = df[["Localitate"]].copy()
    out["Total"] = s_total
    print(out[out["Total"] > 0].sort_values(by="Total", ascending=False))


# =====================================================================
# [3] PROCENTE PE RAND, 0 UNDE TOTALUL E 0   (Seminar 3, cerinta 2)
# =====================================================================
def s3():
    titlu("[3] Procente pe rand (Sat1 are total 0 -> procente 0)")
    s_total = df[ind].sum(axis=1)
    out = df[ind].div(s_total, axis=0) * 100            # fiecare RAND la totalul lui
    out = out.fillna(0)                                  # 0/0 = NaN -> 0
    out.insert(0, "Localitate", df["Localitate"])        # numele pe pozitia 0
    print(out)
    # varianta profului (S3:22-28): df.apply(lambda x: x[ind]*100/x["Total"], axis=1) + fillna(0)


# =====================================================================
# [4] MEDIE PE RAND / "in TOTI anii" / "in CEL PUTIN un an"
# =====================================================================
def s4():
    titlu("[4] Medie pe rand, all(axis=1), any(axis=1)")
    complete = df_ani[(df_ani[ani] > 0).all(axis=1)]     # toate valorile > 0
    out = complete[["Localitate"]].copy()
    out["Medie"] = complete[ani].mean(axis=1)
    print(out.sort_values(by="Medie", ascending=False))
    print("\nCel putin un an cu 0:")
    print(df_ani[(df_ani[ani] == 0).any(axis=1)])
    print("\nMedia pe rand > 30 (tiparul 1086 C1, acolo era > 1):")
    s_m = df[ind].mean(axis=1)
    print(s_m[s_m > 30])


# =====================================================================
# [5] COLOANA CU MAXIMUL PE FIECARE RAND (anul / activitatea dominanta)
# =====================================================================
def s5():
    titlu("[5] idxmax(axis=1) = NUMELE coloanei cu maximul, pe rand")
    out = df_ani[["Localitate"]].copy()
    out["AnMaxim"] = df_ani[ani].idxmax(axis=1)          # idxmin(axis=1) pentru minim
    print(out)
    print("\nRandurile unde activitatea dominanta e 'C' + valoarea lui C (1086 C2):")
    s_dom = df[ind].idxmax(axis=1)
    print(df[s_dom == "C"][["C"]])                       # [["C"]] ca sa ramana antetul
    # ATENTIE: pe randuri cu TOTUL 0, idxmax da prima coloana -> filtreaza total > 0 daca cerinta zice


# =====================================================================
# [6] RATA LA 1000 DE LOCUITORI PE JUDET / REGIUNE
#     REGULA: SUME pe grup, abia apoi impartire
# =====================================================================
def s6():
    titlu("[6] A la 1000 loc, pe judet si pe regiune")
    g = df_merge[["Judet", "A", "Populatie"]].groupby("Judet").sum()
    s = (g["A"] / g["Populatie"] * 1000).sort_values(ascending=False)
    s.index = s.index.str.upper()
    s.name = "A la 1000 loc"
    print(s)
    g = df_merge[["Regiune", "A", "Populatie"]].groupby("Regiune").sum()
    print((g["A"] / g["Populatie"] * 1000).sort_values(ascending=False))
    # GRESIT: rata pe localitate si apoi .sum() / .mean() pe grup


# =====================================================================
# [7] TIPUL / ACTIVITATEA DOMINANTA PE JUDET   (Seminar 3, cerinta 4)
# =====================================================================
def s7():
    titlu("[7] Activitatea dominanta pe judet")
    g = df_merge[ind + ["Judet"]].groupby("Judet").sum()
    s = g[ind].idxmax(axis=1)
    s.name = "Activitate"
    print(s)
    # prof: g[ind].apply(lambda x: x.index[x.argmax()], axis=1)  -> acelasi rezultat


# =====================================================================
# [8] PE JUDET SI PE FIECARE AN: raport cu div(axis=0) + conversie
# =====================================================================
def s8():
    titlu("[8] Valoare pe locuitor, pe judet si an (MWh -> kWh: * 1000)")
    m = df_ani.merge(df_pop[["Judet", "Populatie"]], left_index=True, right_index=True)
    g = m[ani + ["Judet", "Populatie"]].groupby("Judet").sum()
    out = g[ani].div(g["Populatie"], axis=0) * 1000      # fiecare RAND la populatia lui
    print(out)
    print("\nGRESIT g[ani] / g['Populatie'] -> aliniaza pe coloane -> tot NaN:")
    print((g[ani] / g["Populatie"]).iloc[:2, :4])


# =====================================================================
# [9] PROCENTE PE JUDET   (Seminar 2, "de calculat acasa")
# =====================================================================
def s9():
    titlu("[9] Procente pe judet (sume, apoi procente pe rand)")
    g = df_merge[ind + ["Judet"]].groupby("Judet").sum()
    print(g[ind].div(g[ind].sum(axis=1), axis=0) * 100)


# =====================================================================
# [10] PE JUDET, LOCALITATEA CU MAXIMUL (pe locuitor) -> NUME (+ valoare)
# =====================================================================
def s10():
    titlu("[10] Localitatea cu max A/locuitor pe judet")
    m = df_merge.copy()
    m["ALoc"] = m["A"] / m["Populatie"]
    s_siruta = m.groupby("Judet")["ALoc"].idxmax()       # judet -> Siruta (NU nume!)
    print("idxmax da Siruta:\n", s_siruta, sep="")
    out = s_siruta.map(m["Localitate"]).to_frame(name="Localitate")   # Siruta -> nume
    out["ALoc"] = s_siruta.map(m["ALoc"])                             # Siruta -> valoare
    out.index = out.index.str.upper()
    print(out)
    print("\nAcelasi lucru cu .loc:")
    print(m.loc[s_siruta, ["Judet", "Localitate", "ALoc"]].set_index("Judet"))
    # daca imparti la ceva ce poate fi 0: m = df_merge[df_merge["B"] > 0].copy() INAINTE


# =====================================================================
# [11] PE REGIUNE, JUDETUL CU MAXIMUL (2 niveluri)
# =====================================================================
def s11():
    titlu("[11] Judetul cu max A/locuitor pe regiune")
    g = df_merge[["Judet", "Regiune", "A", "Populatie"]].groupby(["Judet", "Regiune"]).sum()
    g = g.reset_index(level="Regiune")                   # Judet = index, Regiune = coloana
    g["ALoc"] = g["A"] / g["Populatie"]
    s = g.groupby("Regiune")["ALoc"].idxmax().str.upper()   # indexul ESTE judetul
    s.name = "Judet"
    print(s)


# =====================================================================
# [12] groupby().idxmax() PE FIECARE COLOANA (activitate / an)
#      date deja pe judet (ca 1086 C4) sau tabel pe judete si ani
# =====================================================================
def s12():
    titlu("[12] Pe regiune, judetul cu maximul pe FIECARE coloana")
    g = df_merge[ind + ["Judet"]].groupby("Judet").sum()            # tabel pe judete
    t = g.merge(df_coduri[["Regiune"]], left_index=True, right_index=True)   # litere MICI!
    out = t[ind + ["Regiune"]].groupby("Regiune").idxmax()
    out = out.apply(lambda col: col.str.upper())         # optional, daca exemplul are AB
    print(out)
    print("\nPe regiune, maximul (valoarea) / localitatea (Siruta) cu max pe coloana:")
    print(df_merge[ind + ["Regiune"]].groupby("Regiune").max())
    print(df_merge[ind + ["Regiune"]].groupby("Regiune").idxmax())


# =====================================================================
# [13] MEDIE PONDERATA (de obicei 3p)   (Seminar 3, cerinta 5)
#      functia primeste TOATE localitatile unui grup -> NU agrega inainte!
# =====================================================================
def medii_ponderate(t):
    return pd.Series(np.average(t[ind], axis=0, weights=t["Populatie"]), index=ind)


def s13():
    titlu("[13] Medie ponderata cu populatia, pe judet")
    out = df_merge[ind + ["Populatie", "Judet"]].groupby("Judet").apply(
        func=medii_ponderate, include_groups=False)
    print(out.round(3))
    print("\nFara functie: (x*p).sum() / p.sum()  -> trebuie sa iasa la fel")
    produs = df_merge[ind].mul(df_merge["Populatie"], axis=0)
    produs["Populatie"] = df_merge["Populatie"]
    produs["Judet"] = df_merge["Judet"]
    sume = produs.groupby("Judet").sum()
    print(sume[ind].div(sume["Populatie"], axis=0).round(3))
    # alta pondere (ex. suprafata): weights=t["Suprafata"]; grupuri cu suma 0 -> filtreaza > 0 inainte
    # varianta profului (S3:5-8) ia ponderea din ULTIMA coloana -> ind + ["Populatie", "Regiune"]


# =====================================================================
# [14] COEFICIENT DE VARIATIE = std / medie, pe grup   (1086 C3)
# =====================================================================
def s14():
    titlu("[14] Coeficient de variatie pe regiune")
    g = df_merge[ind + ["Regiune"]].groupby("Regiune")
    print((g.std() / g.mean()).round(3))                 # pandas std: ddof=1 (de selectie)
    # np.std are ddof=0 -> alt rezultat! Pe pandas ramai cu .std()
    # grup cu 1 singur rand -> std = NaN; grup cu medie 0 -> NaN (0/0). E normal.
    print("\nCV pe fiecare COLOANA a tabelului (fara grup):")
    print(df[ind].std() / df[ind].mean())


# =====================================================================
# [15] INDICE DE LOCALIZARE   (Seminar 3, cerinta 6 - neterminata la prof)
#      (judet / tara pe activitate) / (populatie judet / populatie tara)
# =====================================================================
def s15():
    titlu("[15] Indice de localizare pe judet")
    g = df_merge[ind + ["Judet", "Populatie"]].groupby("Judet").sum()
    pondere_act = g[ind] / g[ind].sum()                  # DataFrame / Series -> pe COLOANE (bine aici)
    pondere_pop = g["Populatie"] / g["Populatie"].sum()  # ["..."] SIMPLE -> Series
    out = pondere_act.div(pondere_pop, axis=0)           # fiecare RAND la ponderea judetului
    out.index = out.index.str.upper()
    print(out)


# =====================================================================
# [16] RAND DE TOTAL / COLOANA NOUA
# =====================================================================
def s16():
    titlu("[16] df.loc['Total'] = rand nou ; df['X'] = coloana noua")
    g = df_merge[ind + ["Judet"]].groupby("Judet").sum()
    g["Total"] = g[ind].sum(axis=1)                       # COLOANA: suma pe rand
    g.loc["Tara"] = g.sum()                               # RAND: suma pe coloane
    print(g)
    print("\nScoti randul inapoi:", list(g.drop(index="Tara").index))


# =====================================================================
# [17] FORMATAREA OUTPUT-ULUI (copiaza exact exemplul!)
# =====================================================================
def s17():
    titlu("[17] Formatare: upper, name, rename, round, index=False")
    g = df_merge[["Judet", "A"]].groupby("Judet").sum()
    s = g["A"].copy()
    s.index = s.index.str.upper()          # ab -> AB
    s.name = "Total A"                     # antetul coloanei unei Series
    print(s.to_frame())                    # Series -> DataFrame (sau .to_frame(name="..."))
    d = g.rename(columns={"A": "Suma A"})  # FARA inplace cand atribui
    d.index.name = "Judet"                 # antetul primei coloane
    print(d)
    print(df.reset_index().head(2))        # Siruta din index -> coloana normala
    # to_csv("data_out/X.csv")                -> indexul e prima coloana
    # to_csv("data_out/X.csv", index=False)   -> cand exemplul NU incepe cu cheia
    # .round(3)                               -> cand exemplul are 3 zecimale
    # df["X"] vs df[["X"]]: Series (calcule, weights, map) vs DataFrame (output la care adaugi coloane)


# =====================================================================
# [18] VALORI LIPSA   (Seminar 2, functii.py:5-11)
# =====================================================================
from pandas.api.types import is_numeric_dtype


def nan_replace_df(t: pd.DataFrame):
    for col in t.columns:
        if t[col].isna().any():
            if is_numeric_dtype(t[col]):
                t.fillna({col: t[col].mean()}, inplace=True)       # numeric -> media
            else:
                t.fillna({col: t[col].mode()[0]}, inplace=True)    # text -> valoarea cea mai frecventa


def s18():
    titlu("[18] NaN -> media (numeric) / modul (text)")
    t = df.copy().astype({"A": float})
    t.loc[101, "A"] = np.nan
    print("NaN-uri inainte:", int(t.isna().sum().sum()))
    nan_replace_df(t)                                         # modifica pe loc, NU atribui
    print(t.head(3))


# =====================================================================
# [19] DIAGNOSTIC - foloseste-le in codul tau cand nu intelegi ce ai
# =====================================================================
def arata(x, nume="x"):
    """arata(df_merge) -> tip, forma, index, coloane, primele randuri"""
    print(f"--- {nume}: {type(x).__name__}, shape={x.shape}, index='{x.index.name}'")
    if isinstance(x, pd.DataFrame):
        print("coloane:", list(x.columns))
    else:
        print("name:", x.name)
    print(x.head(3))


def verifica_exemplu(cale_csv, *linii_exemplu):
    """verifica_exemplu("data_out/Output1.csv", "Judet,Coeficient mediu", "dj,2.300375")"""
    with open(cale_csv) as f:
        continut = f.read().splitlines()
    for linie in linii_exemplu:
        print(("OK      " if linie in continut else "LIPSESTE") + "  " + linie)


def s19():
    titlu("[19] arata(...) si verifica_exemplu(...)")
    arata(df_merge, "df_merge")
    arata(df_merge["A"], "df_merge['A']")


SECTIUNI = {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7, 8: s8, 9: s9, 10: s10,
            11: s11, 12: s12, 13: s13, 14: s14, 15: s15, 16: s16, 17: s17, 18: s18, 19: s19}

if __name__ == "__main__":
    alese = [int(a) for a in sys.argv[1:]] or list(SECTIUNI)
    for k in alese:
        SECTIUNI[k]()
