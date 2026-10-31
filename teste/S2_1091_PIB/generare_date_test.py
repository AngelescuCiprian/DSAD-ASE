import numpy as np, pandas as pd
rng = np.random.default_rng(1091)
ani = [str(a) for a in range(1995, 2022)]
n = len(ani)

# cod, nume, regiune, euro, populatie, PIB 1995, PIB 2021 (mil. EUR, aproximativ realist)
tari = [
 ("BE","Belgium","WesternE","Yes",None,None,None),
 ("BG","Bulgaria","EasternE","No",6916548,10000,71000),
 ("CZ","Czechia","EasternE","No",10494836,45000,238000),
 ("DK","Denmark","NorthernE","No",5840045,140000,342000),
 ("DE","Germany","WesternE","Yes",83155031,1960000,3600000),
 ("EE","Estonia","EasternE","Yes",1330068,2900,31000),
 ("IE","Ireland","NorthernE","Yes",5006324,52000,434000),
 ("EL","Greece","SouthernE","Yes",10678632,95000,181000),
 ("ES","Spain","SouthernE","Yes",47398695,450000,1220000),
 ("FR","France","WesternE","Yes",67656682,1220000,2500000),
 ("HR","Croatia","EasternE","Yes",4036355,15000,58000),
 ("IT","Italy","SouthernE","Yes",59236213,930000,1790000),
 ("CY","Cyprus","SouthernE","Yes",896005,7500,24000),
 ("LV","Latvia","EasternE","Yes",1893223,3900,33000),
 ("LT","Lithuania","EasternE","Yes",2795680,5800,56000),
 ("LU","Luxembourg","WesternE","Yes",634730,15000,73000),
 ("HU","Hungary","EasternE","No",9730772,35000,154000),
 ("MT","Malta","SouthernE","Yes",516100,2800,15000),
 ("NL","Netherlands","WesternE","Yes",17475415,320000,870000),
 ("AT","Austria","WesternE","Yes",8932664,180000,405000),
 ("PL","Poland","EasternE","No",37840001,None,None),
 ("PT","Portugal","SouthernE","Yes",10298252,90000,214000),
 ("RO","Romania","EasternE","No",19201662,28000,241000),
 ("SI","Slovenia","EasternE","Yes",2108977,16000,52000),
 ("SK","Slovakia","EasternE","Yes",5459781,15000,100000),
 ("FI","Finland","NorthernE","Yes",5533793,100000,251000),
 ("SE","Sweden","NorthernE","No",10379295,190000,537000),
 ("NO","Norway","NorthernE","No",5391369,115000,415000),
 ("CH","Switzerland","WesternE","No",8670300,250000,690000),
]

def serie(p95, p21, dip96=False):
    t = np.arange(n)
    s = p95 * (p21 / p95) ** (t / (n - 1))
    s = s * (1 + rng.normal(0, 0.012, n))
    s[ani.index("2009")] *= 0.93
    s[ani.index("2020")] *= 0.95
    if dip96:
        s[ani.index("1996")] = s[0] * 0.92          # anul minim 1996
    else:
        s[1:] = np.maximum(s[1:], s[0] * 1.01)       # anul minim 1995
    return s

gdp, pop = {}, {}
for cod, nume, reg, eur, p, a, b in tari:
    if a is not None:
        gdp[cod] = serie(a, b, dip96=(cod == "BG"))
        pop[cod] = p

# --- exemplele din enunt ---
# Belgium: PIB/locuitor dat exact pe toti anii + PIB mediu 344422.97
pc_be = np.array([20021.702,19995.686,20274.524,21000.209,22026.686,23305.594,24029.052,24840.005,25562.172,26982.044,28183.602,29557.513,31236.27,31974.791,31495.701,33010.822,34176.909,35104.755,35714.292,36634.539,37879.748,39096.396,40456.754,41820.374,43510.658,41799.967,45662.043])
pop["BE"] = 344422.97037037037 * 1e6 / pc_be.mean()
gdp["BE"] = pc_be * pop["BE"] / 1e6
# Bulgaria si Czechia: PIB mediu din exemplu
gdp["BG"] *= 33765.04074074075 / gdp["BG"].mean()
gdp["CZ"] *= 133721.8074074074 / gdp["CZ"].mean()
# EasternE: suma pe ani din exemplu -> Polonia = restul
est = np.array([294850.2,323161.3,356920.2,393291.6,398888.1,455204.2,512717.8,549067.2,549832.7,604047.2,702378.7,788477.9,919314.0,1046586.4,929751.8,994928.8,1046451.0,1057749.3,1067162.5,1102279.2,1165069.6,1189753.1,1296621.9,1397425.1,1496347.9,1460292.5,1609430.5])
altele = sum(gdp[c] for c, *_ in [t for t in tari if t[2] == "EasternE" and t[0] != "PL"])
gdp["PL"] = est - altele
pop["PL"] = 37840001
# Slovenia trebuie sa aiba cel mai mare PIB/locuitor din EasternE in fiecare an (exemplul 5)
est_cod = [t[0] for t in tari if t[2] == "EasternE"]
for _ in range(20):
    pc = {c: gdp[c] * 1e6 / pop[c] for c in est_cod}
    max_altii = np.max([pc[c] for c in est_cod if c != "SI"], axis=0)
    tinta = np.maximum(pc["SI"], max_altii * 1.04) * pop["SI"] / 1e6
    gdp["PL"] = gdp["PL"] - (tinta - gdp["SI"])
    gdp["SI"] = tinta

df_gdp = pd.DataFrame({a: [round(gdp[t[0]][i], 1) for t in tari] for i, a in enumerate(ani)},
                      index=pd.Index([t[0] for t in tari], name="CODE"))
df_gdp.insert(0, "Country", [t[1] for t in tari])
# corectie de rotunjire pentru PL ca suma EasternE sa iasa exact
est_cod = [t[0] for t in tari if t[2] == "EasternE"]
for i, a in enumerate(ani):
    dif = round(est[i] - df_gdp.loc[est_cod, a].sum(), 1)
    df_gdp.loc["PL", a] = round(df_gdp.loc["PL", a] + dif, 1)
df_gdp.to_csv("data_in/gdp.csv")

df_pop = pd.DataFrame({"COUNTRY": [t[1] for t in tari],
                       "POPULATION": [int(round(pop[t[0]])) for t in tari],
                       "EURO": [t[3] for t in tari],
                       "REGION": [t[2] for t in tari]},
                      index=pd.Index([t[0] for t in tari], name="CODE"))
df_pop.to_csv("data_in/populatie.csv")
