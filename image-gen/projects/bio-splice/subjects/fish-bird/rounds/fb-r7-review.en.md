# Score review · R7 (fish-bird)

> 🌐 Language: **English** | [中文](fb-r7-review.md)

> Engine: `zimage`　round description: Period 02 final [half out of water · waterline crossing the body]: fish + bird wings (two takes); includes same-round base control
> Base control: **same-round base control base-fish (half out of water)** (same round, same seed; objective metrics are not disturbed by pose)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomical credibility .20 ｜ D photographic consistency .15 ｜ E concept readability .15
> Threshold: `fatal` non-empty / A<3 / B<3 → fail; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not included as finals**)
> Objective metrics are used only for alerting (region difference < 1.5 = transplant sentence is a no-op), and do not contribute to the score

| Camera | A | B | C | D | E | Total | Verdict | Global difference vs base | Region difference |
|------|---|---|---|---|---|------|------|--------------|--------|
| `fish-wings-half` | 5 | 5 | 5 | 5 | 5 | **5.00** | ✅ final (preferred) | 51.13 | body 61.0 |
| `fish-wings` | 1 | 5 | 5 | 5 | 2 | **3.35** | ❌ fail (transplant not in place) | 31.63 | body 28.8 |

## Item-by-item pros and cons

### `fish-wings-half` — ✅ final (preferred) (total 5.00)
- **A transplant in place**: 5/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 5/5
- 👍 The **half-opened, higher-positioned** wings land — the landing site is on the side above the water

### `fish-wings` — ❌ fail (transplant not in place) (total 3.35)
- **A transplant in place**: 1/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 2/5
- 👍 The fish anatomy and the underwater lighting both hold up
- 👎 When the waterline crosses the body, the body-side wings are eaten by the scene

## Conclusion

- Finals included: **1** — `fish-wings-half`
- Fails: 1; alternates (also not included as finals): 0
- Suggested main image: `fish-wings-half`

> See [`fb-r7-audit.jpg`](fb-r7-audit.jpg) for the basis of the verdict (zoomed-in audit sheet)
