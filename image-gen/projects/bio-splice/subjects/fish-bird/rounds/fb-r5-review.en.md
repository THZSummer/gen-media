# Score review · R5 (fish-bird)

> 🌐 Language: **English** | [中文](fb-r5-review.md)

> Engine: `zimage`　round description: Kunpeng · out-of-water completion: tail feathers (tail position / above the tail) / feathers covering the back / wings + tail feathers combined; includes same-round base control
> Base control: **same-round base control base-fish (**out of water**)** (same round, same seed; objective metrics are not disturbed by pose)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomical credibility .20 ｜ D photographic consistency .15 ｜ E concept readability .15
> Threshold: `fatal` non-empty / A<3 / B<3 → fail; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not included as finals**)
> Objective metrics are used only for alerting (region difference < 1.5 = transplant sentence is a no-op), and do not contribute to the score

| Camera | A | B | C | D | E | Total | Verdict | Global difference vs base | Region difference |
|------|---|---|---|---|---|------|------|--------------|--------|
| `fish-wings-tail` | 4 | 5 | 5 | 5 | 5 | **4.70** | ✅ final (preferred) | 42.17 | body 59.9 |
| `fish-tail` | 1 | 5 | 5 | 5 | 2 | **3.35** | ❌ fail (transplant not in place) | 13.10 | body 21.2 |
| `fish-tail-above` | 1 | 5 | 5 | 5 | 2 | **3.35** | ❌ fail (transplant not in place) | 24.42 | body 44.0 |
| `fish-feathercoat` | 1 | 5 | 5 | 5 | 2 | **3.35** | ❌ fail (transplant not in place) | 11.58 | body 14.5 |

## Item-by-item pros and cons

### `fish-wings-tail` — ✅ final (preferred) (total 4.70)
- **A transplant in place**: 4/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 5/5
- 👍 Wings landed (third reproduction)
- 👎 The same round's tail feathers did not land, so A is 4

### `fish-tail` — ❌ fail (transplant not in place) (total 3.35)
- **A transplant in place**: 1/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 2/5
- 👍 The fish anatomy and the underwater lighting both hold up
- 👎 Tail feathers still do not land in the out-of-water scene → the tail position is a canonical fish structure (Rule 83 high-dependency tier)

### `fish-tail-above` — ❌ fail (transplant not in place) (total 3.35)
- **A transplant in place**: 1/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 2/5
- 👍 The fish anatomy and the underwater lighting both hold up
- 👎 Tail feathers above the tail likewise do not land

### `fish-feathercoat` — ❌ fail (transplant not in place) (total 3.35)
- **A transplant in place**: 1/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 2/5
- 👍 The fish anatomy and the underwater lighting both hold up
- 👎 Feathers covering the back failed to land both times

## Conclusion

- Finals included: **1** — `fish-wings-tail`
- Fails: 3; alternates (also not included as finals): 0
- Suggested main image: `fish-wings-tail`

> See [`fb-r5-audit.jpg`](fb-r5-audit.jpg) for the basis of the verdict (zoomed-in audit sheet)
