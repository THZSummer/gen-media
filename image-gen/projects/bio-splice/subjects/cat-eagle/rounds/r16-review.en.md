# Score review · R16 (cat-eagle)

> 🌐 Language: **English** | [中文](r16-review.md)

> Engine: `zimage`　Round description: period 04 final [dark background · side light picking out the whiskers · face-on close-up] correction: replace the hard light so the whiskers become readable, otherwise the same as R12
> Base control: **same-round base control base-eagle (dark background · side light · face-on close-up)** (same round, same seed; objective metrics unaffected by pose)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomy credible .20 ｜ D photographic unity .15 ｜ E concept legible .15
> Threshold: `fatal` non-empty / A<3 / B<3 → failed; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not included as finals**)
> Objective metrics are used only for alerts (region diff < 1.5 = the transplant sentence was a no-op); they do not enter the score

| Shot | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `e-cat-whiskers` | 5 | 5 | 5 | 5 | 5 | **5.00** | ✅ preferred final | 21.80 | whiskers 38.2 |
| `e-cat-ears-whiskers` | 4 | 5 | 5 | 5 | 4 | **4.55** | ✅ preferred final | 22.27 | whiskers 48.2 |

## Per-shot pros and cons

### `e-cat-whiskers` — ✅ preferred final (total 5.00)
- **A Transplant in place**: 5/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 5/5
- 👍 The cat's long whiskers are lit into bright lines by the side light against the dark background and are identifiable at a glance—which is exactly what replacing the hard light bought
- 👍 The eagle head itself is intact, with whiskers growing from both sides of the beak base in a credible position

### `e-cat-ears-whiskers` — ✅ preferred final (total 4.55)
- **A Transplant in place**: 4/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 4/5
- 👍 Whiskers + ears, both in frame
- 👎 Under side-backlight the ear outline falls into shadow, so the cat ears are less distinct than the whiskers

## Conclusion

- Accepted as finals: **2** images — `e-cat-whiskers`, `e-cat-ears-whiskers`
- Failed: 0 images; alternates (also not included as finals): 0
- Suggested main image: `e-cat-whiskers`

> For the basis of the verdict (zoomed-in audit sheet) see [`r16-audit.jpg`](r16-audit.jpg)
