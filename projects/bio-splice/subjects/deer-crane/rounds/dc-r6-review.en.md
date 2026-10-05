# Score review · R6（deer-crane）

> 🌐 Language: **English** | [中文](dc-r6-review.md)

> Engine: `zimage`　Round note: deer-crane · Period 05 finale [deer and crane in spring]: deer base (legs and tail not described) + crane neck G1 + crane legs G2 + crane tail feathers G6; includes a same-round base control
> Base control: **same-round base control base-deer (spring plum grove · legs and tail not described)** (same round, same seed; objective metrics are unaffected by pose)
> Scoring dimensions: A transplant fidelity .30 ｜ B base integrity .20 ｜ C anatomical plausibility .20 ｜ D photographic consistency .15 ｜ E concept readability .15
> Thresholds: `fatal` non-empty / A<3 / B<3 → fail; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not counted as finals**)
> Objective metrics are used only for alerts (region difference < 1.5 = the transplant sentence is a no-op) and do not contribute to the score

| Camera | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `deer-crane-3parts` | 3 | 5 | 5 | 5 | 4 | **4.25** | ✅ Final | 30.45 | neck 32.5 legs 37.1 |
| `deer-crane-3parts-b` | 3 | 5 | 5 | 5 | 4 | **4.25** | ✅ Final | 47.62 | neck 40.8 legs 38.4 |

## Item-by-item pros and cons

### `deer-crane-3parts` — ✅ Final (total 4.25)
- **A Transplant fidelity**: 3/5
- **B Base integrity**: 5/5
- **C Anatomical plausibility**: 5/5
- **D Photographic consistency**: 5/5
- **E Concept readability**: 4/5
- 👍 Two/three parts are present at the same time without crowding each other out, and no second individual appears
- 👎 Each piece only reaches "partially established", so together they still read as "a slender deer" rather than "a deer-crane hybrid"

### `deer-crane-3parts-b` — ✅ Final (total 4.25)
- **A Transplant fidelity**: 3/5
- **B Base integrity**: 5/5
- **C Anatomical plausibility**: 5/5
- **D Photographic consistency**: 5/5
- **E Concept readability**: 4/5
- 👍 Two/three parts are present at the same time without crowding each other out, and no second individual appears
- 👎 Each piece only reaches "partially established", so together they still read as "a slender deer" rather than "a deer-crane hybrid"

## Conclusion

- Eligible as finals: **2** images — `deer-crane-3parts`, `deer-crane-3parts-b`
- Failures: 0; alternates (likewise not counted as finals): 0
- Suggested main image: `deer-crane-3parts`

> The basis for the verdict (local-magnification audit sheet) is in [`dc-r6-audit.jpg`](dc-r6-audit.jpg)
