# Score review · R5（deer-crane）

> 🌐 Language: **English** | [中文](dc-r5-review.md)

> Engine: `zimage`　Round note: deer-crane · Period 04 candidate [neck and legs together]: deer base (legs not described) + crane neck G1 + crane legs G2; includes a same-round base control
> Base control: **same-round base control base-deer (frosty-morning grassland · legs not described)** (same round, same seed; objective metrics are unaffected by pose)
> Scoring dimensions: A transplant fidelity .30 ｜ B base integrity .20 ｜ C anatomical plausibility .20 ｜ D photographic consistency .15 ｜ E concept readability .15
> Thresholds: `fatal` non-empty / A<3 / B<3 → fail; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not counted as finals**)
> Objective metrics are used only for alerts (region difference < 1.5 = the transplant sentence is a no-op) and do not contribute to the score

| Camera | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `deer-neck-legs` | 3 | 5 | 5 | 5 | 4 | **4.25** | ✅ Final | 14.21 | neck 13.4 legs 17.6 |
| `deer-neck-legs-b` | 3 | 5 | 5 | 5 | 4 | **4.25** | ✅ Final | 32.05 | neck 20.3 legs 48.9 |

## Item-by-item pros and cons

### `deer-neck-legs` — ✅ Final (total 4.25)
- **A Transplant fidelity**: 3/5
- **B Base integrity**: 5/5
- **C Anatomical plausibility**: 5/5
- **D Photographic consistency**: 5/5
- **E Concept readability**: 4/5
- 👍 Two/three parts are present at the same time without crowding each other out, and no second individual appears
- 👎 Each piece only reaches "partially established", so together they still read as "a slender deer" rather than "a deer-crane hybrid"

### `deer-neck-legs-b` — ✅ Final (total 4.25)
- **A Transplant fidelity**: 3/5
- **B Base integrity**: 5/5
- **C Anatomical plausibility**: 5/5
- **D Photographic consistency**: 5/5
- **E Concept readability**: 4/5
- 👍 Two/three parts are present at the same time without crowding each other out, and no second individual appears
- 👎 Each piece only reaches "partially established", so together they still read as "a slender deer" rather than "a deer-crane hybrid"

## Conclusion

- Eligible as finals: **2** images — `deer-neck-legs`, `deer-neck-legs-b`
- Failures: 0; alternates (likewise not counted as finals): 0
- Suggested main image: `deer-neck-legs`

> The basis for the verdict (local-magnification audit sheet) is in [`dc-r5-audit.jpg`](dc-r5-audit.jpg)
