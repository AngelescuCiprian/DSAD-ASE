# Analiza în Componente Principale (ACP) – explicată de la zero

## Ideea
Ai n instanțe (țări) descrise de m variabile. ACP înlocuiește cele m coloane cu **câteva coloane noi** (componente) care păstrează aproape toată **informația** = **varianța** (cât de diferite sunt instanțele între ele).
Funcționează când variabilele sunt **corelate**, adică spun parțial același lucru.

## Exemplu cu 2 variabile (ConsumAlimentar: Meat și Cereals)
- corelația r = **−0.608** (țările cu multă carne mănâncă puține cereale)
- **standardizare**: `z = (x − medie) / abatere`. Altfel Cereals (medie 20) domină Meat (medie 4) doar prin mărime.
- axa nouă: `C1 = 0.707·z_Meat − 0.707·z_Cereals` = „carne față de cereale”
  - USA: z = (1.00, −1.49) → C1 = **+1.76** · Ethiopia: z = (−1.47, 1.73) → C1 = **−2.26** · România: **+0.24**
- valorile proprii: α₁ = 1 + |r| = **1.608** (80.4%), α₂ = 1 − |r| = 0.392 (19.6%)
- cu o singură coloană păstrezi 80% din informație
- Spices + Eggs (r = −0.099): C1 explică doar 55% → fără corelație, ACP nu are ce comprima

## Vocabular (numele din codul profului)
| În cod | Ce e | Dimensiune (n × m) |
|---|---|---|
| `x` | datele brute | n × m |
| `x_` | datele standardizate (z) | n × m |
| `r_v` | matricea de corelații | m × m |
| `alpha` | valorile proprii = **varianța** fiecărei componente | m |
| `a` | vectorii proprii = **rețetele** componentelor (pe **coloane**!) | m × m |
| `c` | componentele = **noile coloane** (valoarea fiecărei instanțe) | n × m |
| `r` | corelații variabile–componente → **interpretare** | m × m |
| `s = c / sqrt(alpha)` | **scorurile** (componente standardizate) | n × m |

## Funcția `acp`, pas cu pas
```python
n, m = x.shape
x_ = x - np.mean(x, axis=0)            # centrare (media pe COLOANE → axis=0)
x_ = x_ / np.std(x_, axis=0)           # standardizare
r_v = (1/n) * x_.T @ x_                # corelații (m × m)
valp, vecp = np.linalg.eig(r_v)        # valori + vectori proprii
valp, vecp = np.real(valp), np.real(vecp)   # eig poate returna 1.608+0j
k = np.flip(np.argsort(valp))          # pozițiile în ordine DEScrescătoare
alpha = valp[k]
a = vecp[:, k]                         # reordonezi COLOANELE (nu rândurile!)
c = x_ @ a                             # componentele
r = a * np.sqrt(alpha)                 # corelații variabile–componente
```
- `argsort([0.39, 1.61, 0.90])` → `[0, 2, 1]` (poziții, crescător) · `flip` → `[1, 2, 0]`
- varianța coloanei `c[:, k]` = `alpha[k]` (de-aia se cheamă „Varianța”)
- **suma alpha = m** (numărul de variabile) în modelul standardizat

## Câte componente păstrăm?
| Criteriu | Regula | ConsumAlimentar (11 variabile) |
|---|---|---|
| **Kaiser** | α > 1 (doar standardizat) | **4** componente → 63.7% |
| **Procent** | cele mai puține cu procent cumulat > P% | P=80 → **7** (C6 = 79.998%, nu 80!) |
| **Cattell** | „cotul” din grafic | vizual |

```python
k1 = len(np.where(alpha > 1)[0])                          # Kaiser
procent_cumulat = np.cumsum(alpha * 100 / sum(alpha))
k2 = np.where(procent_cumulat > 80)[0][0] + 1             # +1: din POZIȚIE în NUMĂR
```

## Capcane
- `np.where(...)[0][0]` dă o **poziție** → numărul de componente e `+1`
- semnul componentelor e **arbitrar** (C1 poate ieși inversat față de colegi: e la fel de corect)
- ACP nu merge cu NaN → `nan_replace_df` înainte de `.values`
- în `functii.py` al profului, ramura `std=False` folosește `np.corrcoef(x_, c)` fără `rowvar=False` → corelează rândurile, nu coloanele. Nu contează cât folosim `std=True`.
