# Score review · R5 (horn-atlas)

> 🌐 Language: **English** | [中文](ha-r5-review.md)

> Engine: `zimage`　Round description: horn atlas · part 5 [narwhal tusk / rhino horn]: unified base + two kinds of single horn (one image each); includes a same-round base control
> Base control: **same-round base control base-horse (frosty morning grassland · face-on close-up vertical)** (same round, same seed; objective metrics unaffected by pose)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomy credible .20 ｜ D photographic unity .15 ｜ E concept legible .15
> Threshold: `fatal` non-empty / A<3 / B<3 → failed; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not included as finals**)
> Objective metrics are used only for alerts (region diff < 1.5 = the transplant sentence was a no-op); they do not enter the score

| Shot | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `horse-narwhal` | 5 | 5 | 5 | 5 | 5 | **5.00** | ✅ preferred final | 26.60 | head 49.1 |
| `horse-rhino` | 5 | 5 | 5 | 5 | 5 | **5.00** | ✅ preferred final | 46.26 | head 53.1 |

## Per-shot pros and cons

### `horse-narwhal` — ✅ preferred final (total 5.00)
- **A Transplant in place**: 5/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 5/5
- 👍 A **long spiraling narwhal tusk** rises from the top of the forehead, its texture clear in the close-up
- 👍 The only piece with a slight semantic deviation (tusk vs horn), but in form it reads completely as a "horn"

### `horse-rhino` — ✅ preferred final (total 5.00)
- **A Transplant in place**: 5/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 5/5
- 👍 A **heavy rhino horn** grows on the nasal bridge—moving from "a horn on top of the forehead" to "a horn on the nose", closing out the atlas

## Conclusion

- Accepted as finals: **2** images — `horse-narwhal`, `horse-rhino`
- Failed: 0 images; alternates (also not included as finals): 0
- Suggested main image: `horse-narwhal`

> For the basis of the verdict (zoomed-in audit sheet) see [`ha-r5-audit.jpg`](ha-r5-audit.jpg)
