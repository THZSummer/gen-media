# Scoring review · R3 (cat-eagle)

> 🌐 Language: **English** | [中文](dn-r3-review.md)

> Engine: `zimage`　Round description: Nine Resemblances · Period 03 candidate: fish scales D6 (delete the scale description in the base to free the placeholder); includes a same-round base control
> Base control: **pure snake base (same-round `base-snake-clean`: the scale description has been deleted** to free the placeholder)** (same round, same seed, so the objective metrics are not disturbed by posture)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomy credible .20 ｜ D photographic unity .15 ｜ E concept readable .15
> Threshold: `fatal` non-empty / A<3 / B<3 → not qualified; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternatives (**not included in the finals**)
> Objective metrics are used only for alarms (region diff < 1.5 = the transplant sentence is a no-op), and do not contribute to the score

| Shot | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `snake-fishscale-antler` | 4 | 5 | 5 | 5 | 4 | **4.55** | ✅ final (preferred) | 18.60 | head 39.3 body 17.9 |
| `snake-fishscale` | 3 | 5 | 5 | 5 | 3 | **4.10** | ✅ final | 11.99 | head 16.3 body 18.5 |

## Point-by-point pros and cons

### `snake-fishscale-antler` — ✅ final (preferred) (total 4.55)
- **A transplant in place**: 4/5
- **B base intact**: 5/5
- **C anatomy credible**: 5/5
- **D photographic unity**: 5/5
- **E concept readable**: 4/5
- 👍 antlers D1 hold completely
- 👍 the change in the scales is consistent with "+fish scales", and the two transplants do not interfere with each other
- 👎 the scales are as before, still a partial success

### `snake-fishscale` — ✅ final (total 4.10)
- **A transplant in place**: 3/5
- **B base intact**: 5/5
- **C anatomy credible**: 5/5
- **D photographic unity**: 5/5
- **E concept readable**: 3/5
- 👍 the body scales change from the baseline's fine granular scales to **larger, more regular, mutually overlapping** scale rows, the right direction
- 👎 it stops at "large and orderly scales", without the key features of fish scales (fan-shaped edges / overlapping like roof tiles / iridescence)
- 👎 the control baseline has scales of its own, so this part's difference is naturally harder to interpret than an empty-slot transplant such as "antlers"

## Conclusion

- Can be included in the finals: **2** images — `snake-fishscale-antler`, `snake-fishscale`
- Not qualified: 0; alternatives (likewise not included in the finals): 0
- Suggested main image: `snake-fishscale-antler`

> The basis for the verdict (zoomed-in audit sheet) is in [`dn-r3-audit.jpg`](dn-r3-audit.jpg)
