# Score review · R13 (cat-eagle)

> 🌐 Language: **English** | [中文](r13-review.md)

> Engine: `zimage`　Round description: period 05 final [snowfield rain mist · telephoto compression]: cat base + eagle neck ruff E6 / tail feathers+neck ruff / three parts; includes a same-round base control
> Base control: **same-round base control base-cat (snowfield rain mist · telephoto compression · landscape)** (same round, same seed; objective metrics unaffected by pose)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomy credible .20 ｜ D photographic unity .15 ｜ E concept legible .15
> Threshold: `fatal` non-empty / A<3 / B<3 → failed; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not included as finals**)
> Objective metrics are used only for alerts (region diff < 1.5 = the transplant sentence was a no-op); they do not enter the score

| Shot | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `c-eagle-3parts` | 4 | 5 | 5 | 5 | 5 | **4.70** | ✅ preferred final | 24.01 | ears 28.9 body 44.4 |
| `c-eagle-ruff` | 4 | 5 | 5 | 5 | 4 | **4.55** | ✅ preferred final | 15.10 | ears 4.5 body 33.5 |
| `c-eagle-tail-ruff` | 4 | 5 | 5 | 5 | 4 | **4.55** | ✅ preferred final | 19.75 | ears 7.2 body 39.0 |

## Per-shot pros and cons

### `c-eagle-3parts` — ✅ preferred final (total 4.70)
- **A Transplant in place**: 4/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 5/5
- 👍 Triple eagle-ization: spread eagle wings + a neck ruff collar; the snowfield telephoto compression makes the subject pop out of the background
- 👍 Stacking three parts still yields one individual, with no second individual
- 👎 The tail feathers are indistinguishable in this image (blocked by the body)

### `c-eagle-ruff` — ✅ preferred final (total 4.55)
- **A Transplant in place**: 4/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 4/5
- 👍 A thick dark-brown eagle feather collar grows on the sides of the neck, reading as a fluffed-up mane
- 👍 The snow and flat light make the texture difference between tabby fur and feathers clear
- 👎 The feather collar and the cat's neck fur blur together in silhouette and need magnification to tell apart

### `c-eagle-tail-ruff` — ✅ preferred final (total 4.55)
- **A Transplant in place**: 4/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 4/5
- 👍 Both the tail feathers and the neck ruff are present; cross-region stacking is not a problem
- 👎 The tail feathers are partly swallowed by the snow and the coat colour, less clear than the single-piece version

## Conclusion

- Accepted as finals: **3** images — `c-eagle-3parts`, `c-eagle-ruff`, `c-eagle-tail-ruff`
- Failed: 0 images; alternates (also not included as finals): 0
- Suggested main image: `c-eagle-3parts`

> For the basis of the verdict (zoomed-in audit sheet) see [`r13-audit.jpg`](r13-audit.jpg)
