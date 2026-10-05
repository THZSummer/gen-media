# Score review · R3（deer-crane）

> 🌐 Language: **English** | [中文](dc-r3-review.md)

> Engine: `zimage`　Round note: deer-crane · Period 02 control [occupied version]: deer base (still describes four long legs) + crane's slender legs G2; includes a same-round base control
> Base control: **same-round base control base-deer (shallow-water marsh · **still describes four long legs**)** (same round, same seed; objective metrics are unaffected by pose)
> Scoring dimensions: A transplant fidelity .30 ｜ B base integrity .20 ｜ C anatomical plausibility .20 ｜ D photographic consistency .15 ｜ E concept readability .15
> Thresholds: `fatal` non-empty / A<3 / B<3 → fail; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not counted as finals**)
> Objective metrics are used only for alerts (region difference < 1.5 = the transplant sentence is a no-op) and do not contribute to the score

| Camera | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `deer-cranelegs` | 3 | 5 | 5 | 5 | 4 | **4.25** | ✅ Final | 7.29 | legs 13.6 |

## Item-by-item pros and cons

### `deer-cranelegs` — ✅ Final (total 4.25)
- **A Transplant fidelity**: 3/5
- **B Base integrity**: 5/5
- **C Anatomical plausibility**: 5/5
- **D Photographic consistency**: 5/5
- **E Concept readability**: 4/5
- 👍 The legs became slender and long; the joints read more like a wading bird's
- 👎 The occupied version's conclusion is **almost identical** to the vacated version: the legs' length and thickness were changed, but the material (brown + hooves) was not
- 👎 So "vacating a slot" neither helps nor hurts for canonical structures — what decides success is material, not the vacated slot

## Conclusion

- Eligible as finals: **1** image — `deer-cranelegs`
- Failures: 0; alternates (likewise not counted as finals): 0
- Suggested main image: `deer-cranelegs`

> The basis for the verdict (local-magnification audit sheet) is in [`dc-r3-audit.jpg`](dc-r3-audit.jpg)
