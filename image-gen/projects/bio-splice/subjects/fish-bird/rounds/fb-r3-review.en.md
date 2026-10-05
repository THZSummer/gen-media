# Score review · R3 (fish-bird)

> 🌐 Language: **English** | [中文](fb-r3-review.md)

> Engine: `zimage`　round description: Kunpeng · empty-slot probe: wings growing from the back / tail feathers spreading above the tail / feathers covering the back (same base); includes same-round base control
> Base control: **same-round base control base-fish (underwater · neither pectoral fins nor tail described)** (same round, same seed; objective metrics are not disturbed by pose)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomical credibility .20 ｜ D photographic consistency .15 ｜ E concept readability .15
> Threshold: `fatal` non-empty / A<3 / B<3 → fail; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not included as finals**)
> Objective metrics are used only for alerting (region difference < 1.5 = transplant sentence is a no-op), and do not contribute to the score

| Camera | A | B | C | D | E | Total | Verdict | Global difference vs base | Region difference |
|------|---|---|---|---|---|------|------|--------------|--------|
| `fish-wings-back` | 1 | 5 | 5 | 5 | 2 | **3.35** | ❌ fail (transplant not in place) | 15.48 | body 32.4 |
| `fish-tail-above` | 1 | 5 | 5 | 5 | 2 | **3.35** | ❌ fail (transplant not in place) | 25.16 | body 39.5 |
| `fish-feathercoat` | 1 | 5 | 5 | 5 | 2 | **3.35** | ❌ fail (transplant not in place) | 7.47 | body 10.8 |

## Item-by-item pros and cons

### `fish-wings-back` — ❌ fail (transplant not in place) (total 3.35)
- **A transplant in place**: 1/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 2/5
- 👍 The fish anatomy and the underwater lighting both hold up
- 👎 Changing the wings to grow from the back still landed 0%

### `fish-tail-above` — ❌ fail (transplant not in place) (total 3.35)
- **A transplant in place**: 1/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 2/5
- 👍 The fish anatomy and the underwater lighting both hold up
- 👎 Changing the tail feathers to spread above the tail still landed 0%

### `fish-feathercoat` — ❌ fail (transplant not in place) (total 3.35)
- **A transplant in place**: 1/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 2/5
- 👍 The fish anatomy and the underwater lighting both hold up
- 👎 Feathers covering the back landed 0%

## Conclusion

- Finals included: **0** — (none)
- Fails: 3; alternates (also not included as finals): 0
- Suggested main image: none (no deliverable final this round)

> See [`fb-r3-audit.jpg`](fb-r3-audit.jpg) for the basis of the verdict (zoomed-in audit sheet)
