# Score review · R7（deer-crane）

> 🌐 Language: **English** | [中文](dc-r7-review.md)

> Engine: `zimage`　Round note: deer-crane · Period 03 final (supplementary take): deer base (tail not described) + crane's tail feathers G6 (three seeds); includes a same-round base control
> Base control: **same-round base control base-deer (reed marsh · tail position vacated)** (same round, same seed; objective metrics are unaffected by pose)
> Scoring dimensions: A transplant fidelity .30 ｜ B base integrity .20 ｜ C anatomical plausibility .20 ｜ D photographic consistency .15 ｜ E concept readability .15
> Thresholds: `fatal` non-empty / A<3 / B<3 → fail; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not counted as finals**)
> Objective metrics are used only for alerts (region difference < 1.5 = the transplant sentence is a no-op) and do not contribute to the score

| Camera | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `deer-cranetait` | 5 | 5 | 5 | 5 | 5 | **5.00** | ✅ preferred final | 18.28 | tail 35.2 |
| `deer-cranetait-c` | 1 | 5 | 5 | 5 | 2 | **3.35** | ❌ Fail (transplant did not land) | 39.37 | tail 27.2 |
| `deer-cranetait-d` | 1 | 5 | 5 | 5 | 2 | **3.35** | ❌ Fail (transplant did not land) | 41.29 | tail 29.4 |

## Item-by-item pros and cons

### `deer-cranetait` — ✅ preferred final (total 5.00)
- **A Transplant fidelity**: 5/5
- **B Base integrity**: 5/5
- **C Anatomical plausibility**: 5/5
- **D Photographic consistency**: 5/5
- **E Concept readability**: 5/5
- 👍 A complete ring of white crane tail feathers grows from the rump; backlit, the feathers are semi-translucent
- 👍 This is the only "true empty slot" part in this sub-theme, and the only fully realized piece

### `deer-cranetait-c` — ❌ Fail (transplant did not land) (total 3.35)
- **A Transplant fidelity**: 1/5
- **B Base integrity**: 5/5
- **C Anatomical plausibility**: 5/5
- **D Photographic consistency**: 5/5
- **E Concept readability**: 2/5
- 👎 The third seed did not land: the white on the rump is the deer's own rump patch, not the crane's feather fan

### `deer-cranetait-d` — ❌ Fail (transplant did not land) (total 3.35)
- **A Transplant fidelity**: 1/5
- **B Base integrity**: 5/5
- **C Anatomical plausibility**: 5/5
- **D Photographic consistency**: 5/5
- **E Concept readability**: 2/5
- 👎 The fourth seed did not land either

## Conclusion

- Eligible as finals: **1** image — `deer-cranetait`
- Failures: 2; alternates (likewise not counted as finals): 0
- Suggested main image: `deer-cranetait`

> The basis for the verdict (local-magnification audit sheet) is in [`dc-r7-audit.jpg`](dc-r7-audit.jpg)
