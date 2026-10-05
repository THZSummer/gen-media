# Score review · R9 (cat-eagle)

> 🌐 Language: **English** | [中文](r09-review.md)

> Engine: `zimage`　Round description: period 05 candidates: cat base + three eagle parts (E2 wings / E5 tail feathers / E6 neck ruff); includes a same-round base control
> Base control: **pure-cat base (same-round base-cat shot)** (same round, same seed; objective metrics unaffected by pose)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomy credible .20 ｜ D photographic unity .15 ｜ E concept legible .15
> Threshold: `fatal` non-empty / A<3 / B<3 → failed; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not included as finals**)
> Objective metrics are used only for alerts (region diff < 1.5 = the transplant sentence was a no-op); they do not enter the score

| Shot | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `c-eagle-ruff` | 5 | 5 | 5 | 5 | 5 | **5.00** | ✅ preferred final | 22.71 | head 42.3 rear 26.7 flanks 35.8 |
| `c-eagle-tail-ruff` | 5 | 5 | 5 | 5 | 4 | **4.85** | ✅ preferred final | 24.24 | head 44.5 rear 29.6 flanks 38.7 |
| `c-eagle-3parts` | 4 | 5 | 5 | 4 | 5 | **4.55** | ✅ preferred final | 32.07 | head 53.1 rear 50.5 flanks 58.9 |

## Per-shot pros and cons

### `c-eagle-ruff` — ✅ preferred final (total 5.00)
- **A Transplant in place**: 5/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 5/5
- 👍 Dark plume feathers form a complete collar, transitioning naturally into the fur
- 👍 It reads overall as a large wildcat, with no anatomical flaw
- 👎 The neck ruff makes the body look bigger, slightly off from the baseline pure cat's bulk

### `c-eagle-tail-ruff` — ✅ preferred final (total 4.85)
- **A Transplant in place**: 5/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 4/5
- 👍 The neck ruff and the feathered tail are both in place
- 👍 Both are on the same cat, with no extra individual
- 👎 The two parts are far apart, so at thumbnail size only the neck ruff may be visible (E loses 1)

### `c-eagle-3parts` — ✅ preferred final (total 4.55)
- **A Transplant in place**: 4/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 4/5
- **E Concept legible**: 5/5
- 👍 Spread wings + neck ruff + feathered tail, all three present (wings and neck ruff confirmed at magnification)
- 👍 The most information-dense image in the series
- 👎 The wingspan widens the composition, not fully consistent with the other periods' camera (D loses 1)
- 👎 The tail feathers fell outside the audit crop and were not confirmed separately (A loses 1; the region diff serves as circumstantial evidence)

## Conclusion

- Accepted as finals: **3** images — `c-eagle-ruff`, `c-eagle-tail-ruff`, `c-eagle-3parts`
- Failed: 0 images; alternates (also not included as finals): 0
- Suggested main image: `c-eagle-ruff`

> For the basis of the verdict (zoomed-in audit sheet) see [`r09-audit.jpg`](r09-audit.jpg)
