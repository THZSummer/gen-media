# Score review · R2（deer-crane）

> 🌐 Language: **English** | [中文](dc-r2-review.md)

> Engine: `zimage`　Round note: deer-crane · Period 02 candidate [vacated version]: deer base (legs not described) + crane's slender legs G2; includes a same-round base control
> Base control: **same-round base control base-deer (shallow-water marsh · **legs not described**)** (same round, same seed; objective metrics are unaffected by pose)
> Scoring dimensions: A transplant fidelity .30 ｜ B base integrity .20 ｜ C anatomical plausibility .20 ｜ D photographic consistency .15 ｜ E concept readability .15
> Thresholds: `fatal` non-empty / A<3 / B<3 → fail; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not counted as finals**)
> Objective metrics are used only for alerts (region difference < 1.5 = the transplant sentence is a no-op) and do not contribute to the score

| Camera | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `deer-cranelegs` | 3 | 5 | 5 | 5 | 4 | **4.25** | ✅ Final | 10.82 | legs 22.0 |
| `deer-cranelegs-b` | 3 | 5 | 5 | 5 | 4 | **4.25** | ✅ Final | 30.82 | legs 40.9 |

## Item-by-item pros and cons

### `deer-cranelegs` — ✅ Final (total 4.25)
- **A Transplant fidelity**: 3/5
- **B Base integrity**: 5/5
- **C Anatomical plausibility**: 5/5
- **D Photographic consistency**: 5/5
- **E Concept readability**: 4/5
- 👍 The legs became slender and long; the joints read more like a wading bird's
- 👎 The legs are still the deer's brown color and hoof shape, without the crane's gray-black slender legs — "length can be changed, material cannot"

### `deer-cranelegs-b` — ✅ Final (total 4.25)
- **A Transplant fidelity**: 3/5
- **B Base integrity**: 5/5
- **C Anatomical plausibility**: 5/5
- **D Photographic consistency**: 5/5
- **E Concept readability**: 4/5
- 👍 The legs became slender and long; the joints read more like a wading bird's
- 👎 The legs are still the deer's brown color and hoof shape, without the crane's gray-black slender legs — "length can be changed, material cannot"

## Conclusion

- Eligible as finals: **2** images — `deer-cranelegs`, `deer-cranelegs-b`
- Failures: 0; alternates (likewise not counted as finals): 0
- Suggested main image: `deer-cranelegs`

> The basis for the verdict (local-magnification audit sheet) is in [`dc-r2-audit.jpg`](dc-r2-audit.jpg)
