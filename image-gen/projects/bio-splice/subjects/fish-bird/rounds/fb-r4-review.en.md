# Score review · R4 (fish-bird)

> 🌐 Language: **English** | [中文](fb-r4-review.md)

> Engine: `zimage`　round description: Kunpeng · out-of-water probe: the same fish base + the same three parts, only moving the scene above the water surface; includes same-round base control
> Base control: **same-round base control base-fish (**out of water**)** (same round, same seed; objective metrics are not disturbed by pose)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomical credibility .20 ｜ D photographic consistency .15 ｜ E concept readability .15
> Threshold: `fatal` non-empty / A<3 / B<3 → fail; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not included as finals**)
> Objective metrics are used only for alerting (region difference < 1.5 = transplant sentence is a no-op), and do not contribute to the score

| Camera | A | B | C | D | E | Total | Verdict | Global difference vs base | Region difference |
|------|---|---|---|---|---|------|------|--------------|--------|
| `fish-wings-back` | 5 | 5 | 5 | 5 | 5 | **5.00** | ✅ final (preferred) | 37.10 | body 53.5 |
| `fish-wings` | 5 | 5 | 5 | 5 | 5 | **5.00** | ✅ final (preferred) | 33.50 | body 49.6 |
| `fish-feathercoat` | 1 | 5 | 5 | 5 | 2 | **3.35** | ❌ fail (transplant not in place) | 11.58 | body 14.5 |

## Item-by-item pros and cons

### `fish-wings-back` — ✅ final (preferred) (total 5.00)
- **A transplant in place**: 5/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 5/5
- 👍 **Out of water the wings land immediately**: wings growing from the back hold up
- 👍 Same sentence and same base as R3, the only difference is the scene — this is direct evidence of "scene semantic conflict"

### `fish-wings` — ✅ final (preferred) (total 5.00)
- **A transplant in place**: 5/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 5/5
- 👍 The body-side wings land as well

### `fish-feathercoat` — ❌ fail (transplant not in place) (total 3.35)
- **A transplant in place**: 1/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 2/5
- 👍 The fish anatomy and the underwater lighting both hold up
- 👎 Feathers covering the back **still** do not land in the out-of-water scene → unrelated to the scene; "same-material replacement" (scales→feathers) is itself hard

## Conclusion

- Finals included: **2** — `fish-wings-back`, `fish-wings`
- Fails: 1; alternates (also not included as finals): 0
- Suggested main image: `fish-wings-back`

> See [`fb-r4-audit.jpg`](fb-r4-audit.jpg) for the basis of the verdict (zoomed-in audit sheet)
