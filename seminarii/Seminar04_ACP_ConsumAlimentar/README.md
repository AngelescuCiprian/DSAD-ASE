# Seminar 4 – ACP pe ConsumAlimentar

**Date:** `ConsumAlimentar.csv`: 170 de țări × 11 categorii de alimente (procent din cantitatea totală de alimente disponibile, FAO). Descrierea coloanelor e în `ConsumAlimentar.docx`.

- `index_col=1` → indexul e `Code` (AFG, ALB...), iar `columns.values[1:]` sare peste `Country`
- NaN: alcool 10 țări, condimente 18, pește 1 → `nan_replace_df` (media coloanei)
- rândurile adună ~43%, nu 100% (fișierul are doar o parte din categoriile FAO)

**Rezultat (`data_out/Varianta.csv`):** C1 = 30.4%, Kaiser → 4 componente (63.7%), procent > 80% → 7 componente.
C1 ≈ axa „carne / ouă / lapte / alcool” ↔ „cereale” (practic o axă de nivel de trai).

Explicațiile complete: [docs/ACP_explicat.md](../../docs/ACP_explicat.md)
