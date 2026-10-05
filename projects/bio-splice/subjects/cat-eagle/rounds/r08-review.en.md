# Score review · R8 (cat-eagle)

> 🌐 Language: **English** | [中文](r08-review.md)

> Engine: `zimage`　Round description: period 04 candidates: eagle base + three cat parts (C1 ears / C5 tail / C6 whiskers); includes a same-round base control
> Base control: **pure-eagle base (same-round base-eagle shot)** (same round, same seed; objective metrics unaffected by pose)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomy credible .20 ｜ D photographic unity .15 ｜ E concept legible .15
> Threshold: `fatal` non-empty / A<3 / B<3 → failed; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not included as finals**)
> Objective metrics are used only for alerts (region diff < 1.5 = the transplant sentence was a no-op); they do not enter the score

| Shot | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `e-cat-whiskers` | 5 | 5 | 5 | 5 | 4 | **4.85** | ✅ preferred final | 19.94 | head 19.3 rear 29.5 feet 36.9 |
| `e-cat-ears-whiskers` | 5 | 4 | 4 | 5 | 5 | **4.60** | ✅ preferred final | 24.84 | head 25.4 rear 32.2 feet 48.7 |
| `e-cat-3parts` | 3 | 3 | 2 | 5 | – | **2.65** | ❌ Failed | 25.63 | head 28.0 rear 34.2 feet 46.8 |

## Per-shot pros and cons

### `e-cat-whiskers` — ✅ preferred final (total 4.85)
- **A Transplant in place**: 5/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 4/5
- 👍 The long whiskers are fine and clear, growing naturally from the sides of the beak
- 👍 The eagle head / folded wings / yellow talons are all intact
- 👍 The photographic language is of the same origin as the baseline
- 👎 Whiskers are a fine part and become hard to notice at thumbnail size (hence E loses 1)

### `e-cat-ears-whiskers` — ✅ preferred final (total 4.60)
- **A Transplant in place**: 5/5
- **B Base intact**: 4/5
- **C Anatomy credible**: 4/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 5/5
- 👍 Cat ears and cat whiskers are both in place
- 👍 The beak is still there (confirmed after magnification; the thumbnail was once misread as a pure cat head)
- 👍 "A cat-ized eagle" is readable at a glance
- 👎 The head fur proliferated into cat cheek fur, weakening the eagle head's original sharpness (B/C each lose 1)

### `e-cat-3parts` — ❌ Failed (total 2.65)
- **A Transplant in place**: 3/5
- **B Base intact**: 3/5
- **C Anatomy credible**: 2/5
- **D Photographic unity**: 5/5
- 👍 The cat ears and whiskers on the subject hold
- 👎 After stacking three parts the subject's head is over-cat-ized
- ⛔ **Fatal**: a second animal (a small cat) appears in the lower-right corner, violating "a single animal occupies the frame alone"

## Conclusion

- Accepted as finals: **2** images — `e-cat-whiskers`, `e-cat-ears-whiskers`
- Failed: 1 image; alternates (also not included as finals): 0
- Suggested main image: `e-cat-whiskers`

> For the basis of the verdict (zoomed-in audit sheet) see [`r08-audit.jpg`](r08-audit.jpg)
