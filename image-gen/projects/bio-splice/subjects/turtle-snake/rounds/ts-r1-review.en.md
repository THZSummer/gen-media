# Score review · R1 (turtle-snake)

> 🌐 Language: **English** | [中文](ts-r1-review.md)

> Engine: `zimage`　round description: Xuanwu · first-period candidate: turtle base + snake neck N1 / snake tail N2 / coiling body N3 (includes same-round base control)
> Base control: **same-round base control base-turtle (turtle, neck and tail slots freed) (stream stone shallows · morning light · eye-level 600mm)** (same round, same seed; objective metrics are not disturbed by pose)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomical credibility .20 ｜ D photographic consistency .15 ｜ E concept readability .15
> Threshold: `fatal` non-empty / A<3 / B<3 → fail; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not included as finals**)
> Objective metrics are used only for alerting (region difference < 1.5 = transplant sentence is a no-op), and do not contribute to the score

| Camera | A | B | C | D | E | Total | Verdict | Global difference vs base | Region difference |
|------|---|---|---|---|---|------|------|--------------|--------|
| `turtle-snakeneck` | 5 | 5 | 5 | 5 | 5 | **5.00** | ✅ final (preferred) | 19.92 | neck 27.3 tail 28.0 |
| `turtle-neck-tail` | 4 | 5 | 5 | 5 | 4 | **4.55** | ✅ final (preferred) | 22.66 | neck 36.2 tail 53.7 |
| `turtle-snaketail` | 4 | 5 | 4 | 5 | 4 | **4.35** | ✅ final (preferred) | 28.68 | neck 40.6 tail 54.3 |
| `turtle-coil` | 1 | 5 | 5 | 5 | 2 | **3.35** | ❌ fail (transplant not in place) | 17.32 | neck 21.7 tail 34.4 |

## Item-by-item pros and cons

### `turtle-snakeneck` — ✅ final (preferred) (total 5.00)
- **A transplant in place**: 5/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 5/5
- 👍 The long, curved snake neck extends from the shell opening, with fine scales all the way to the lower jaw, and the turtle head growing on top is seamless
- 👍 This is the piece that establishes this sub-theme: the "snake" half of Xuanwu holds up

### `turtle-neck-tail` — ✅ final (preferred) (total 4.55)
- **A transplant in place**: 4/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 4/5
- 👍 Neck and tail hold up at the same time; cross-region stacking is no problem
- 👎 The tail is still in a tilted-up pose

### `turtle-snaketail` — ✅ final (preferred) (total 4.35)
- **A transplant in place**: 4/5
- **B base intact**: 5/5
- **C anatomical credibility**: 4/5
- **D photographic consistency**: 5/5
- **E concept readability**: 4/5
- 👍 The snake tail extends from behind the shell, with a clear scale row and a tapering tip
- 👎 On the stream stone the tail tilts up too high; the pose is unnatural

### `turtle-coil` — ❌ fail (transplant not in place) (total 3.35)
- **A transplant in place**: 1/5
- **B base intact**: 5/5
- **C anatomical credibility**: 5/5
- **D photographic consistency**: 5/5
- **E concept readability**: 2/5
- 👎 The coiling body did not appear at all — `the thick coiled body of a large snake wrapped around its shell` was a no-op
- 👎 It was arranged as an "add into an empty slot" (which should have been the easiest to land), so the next round specifically chased its phrasing

## Conclusion

- Finals included: **3** — `turtle-snakeneck`, `turtle-neck-tail`, `turtle-snaketail`
- Fails: 1; alternates (also not included as finals): 0
- Suggested main image: `turtle-snakeneck`

> See [`ts-r1-audit.jpg`](ts-r1-audit.jpg) for the basis of the verdict (zoomed-in audit sheet)
