# Score review · R1（deer-crane）

> 🌐 Language: **English** | [中文](dc-r1-review.md)

> Engine: `zimage`　Round note: deer-crane · Period 01 candidate: deer base (neck position vacated) + crane's long neck G1 (two takes); includes a same-round base control
> Base control: **same-round base control base-deer (misty bamboo grove · neck position vacated)** (same round, same seed; objective metrics are unaffected by pose)
> Scoring dimensions: A transplant fidelity .30 ｜ B base integrity .20 ｜ C anatomical plausibility .20 ｜ D photographic consistency .15 ｜ E concept readability .15
> Thresholds: `fatal` non-empty / A<3 / B<3 → fail; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not counted as finals**)
> Objective metrics are used only for alerts (region difference < 1.5 = the transplant sentence is a no-op) and do not contribute to the score

| Camera | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `deer-craneneck` | 3 | 5 | 5 | 5 | 4 | **4.25** | ✅ Final | 16.16 | neck 40.8 |
| `deer-craneneck-b` | 3 | 5 | 5 | 5 | 4 | **4.25** | ✅ Final | 36.22 | neck 45.7 |

## Item-by-item pros and cons

### `deer-craneneck` — ✅ Final (total 4.25)
- **A Transplant fidelity**: 3/5
- **B Base integrity**: 5/5
- **C Anatomical plausibility**: 5/5
- **D Photographic consistency**: 5/5
- **E Concept readability**: 4/5
- 👍 The neck is clearly longer and thinner and stands upright; the pose leans toward a wading bird
- 👍 The deer's torso, coat color, and ear shape are intact — it is still a deer
- 👎 No gray fine feathers of the crane grew in; the neck still reads mostly as a deer — this counts as "partially established"
- 👎 The deer's neck is a canonical structure; removing its description still gets it filled back in by the model (Rule 87)

### `deer-craneneck-b` — ✅ Final (total 4.25)
- **A Transplant fidelity**: 3/5
- **B Base integrity**: 5/5
- **C Anatomical plausibility**: 5/5
- **D Photographic consistency**: 5/5
- **E Concept readability**: 4/5
- 👍 The neck is clearly longer and thinner and stands upright; the pose leans toward a wading bird
- 👍 The deer's torso, coat color, and ear shape are intact — it is still a deer
- 👎 No gray fine feathers of the crane grew in; the neck still reads mostly as a deer — this counts as "partially established"
- 👎 The deer's neck is a canonical structure; removing its description still gets it filled back in by the model (Rule 87)

## Conclusion

- Eligible as finals: **2** images — `deer-craneneck`, `deer-craneneck-b`
- Failures: 0; alternates (likewise not counted as finals): 0
- Suggested main image: `deer-craneneck`

> The basis for the verdict (local-magnification audit sheet) is in [`dc-r1-audit.jpg`](dc-r1-audit.jpg)
