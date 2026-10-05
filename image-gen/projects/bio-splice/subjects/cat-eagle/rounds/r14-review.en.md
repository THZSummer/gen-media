# Score review · R14 (cat-eagle)

> 🌐 Language: **English** | [中文](r14-review.md)

> Engine: `zimage`　Round description: period 02 final [post-rain pebble riverbank · low camera focused on ears and tail] correction: the pose does not mention the tail, otherwise the same as R10
> Base control: **same-round base control base-eagle (post-rain pebble riverbank · low camera 85mm vertical)** (same round, same seed; objective metrics unaffected by pose)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomy credible .20 ｜ D photographic unity .15 ｜ E concept legible .15
> Threshold: `fatal` non-empty / A<3 / B<3 → failed; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not included as finals**)
> Objective metrics are used only for alerts (region diff < 1.5 = the transplant sentence was a no-op); they do not enter the score

| Shot | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `e-cat-ears` | 4 | 5 | 5 | 5 | 4 | **4.55** | ✅ preferred final | 25.21 | head 27.0 extra 20.3 |
| `e-cat-tail` | 1 | 3 | 2 | 4 | 2 | **2.20** | ❌ Failed | 28.11 | head 32.5 extra 42.0 |
| `e-cat-ears-tail` | 1 | 3 | 2 | 4 | 2 | **2.20** | ❌ Failed | 47.78 | head 72.3 extra 78.4 |

## Per-shot pros and cons

### `e-cat-ears` — ✅ preferred final (total 4.55)
- **A Transplant in place**: 4/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 4/5
- 👍 The cat's tufted ears hold on the eagle head
- 👎 This round's main problem is not in this image

### `e-cat-tail` — ❌ Failed (total 2.20)
- **A Transplant in place**: 1/5
- **B Base intact**: 3/5
- **C Anatomy credible**: 2/5
- **D Photographic unity**: 4/5
- **E Concept legible**: 2/5
- 👍 The low-camera 85mm rendering of the water surface and pebble texture is very good
- 👎 Under a **low camera vertical frame** the cat-tail sentence drags out a whole cat (the same sentence held in R6's eye-level full-body shot)
- ⛔ **Fatal**: an extra complete cat appears in the image—the donor was drawn as a separate individual rather than growing on the eagle

### `e-cat-ears-tail` — ❌ Failed (total 2.20)
- **A Transplant in place**: 1/5
- **B Base intact**: 3/5
- **C Anatomy credible**: 2/5
- **D Photographic unity**: 4/5
- **E Concept legible**: 2/5
- 👍 The cat ears themselves hold
- 👎 Same cause as e-cat-tail: the camera/canvas triggered donor individualization
- ⛔ **Fatal**: an extra cat appears as well (lower-left corner)

## Conclusion

- Accepted as finals: **1** image — `e-cat-ears`
- Failed: 2 images; alternates (also not included as finals): 0
- Suggested main image: `e-cat-ears`

> For the basis of the verdict (zoomed-in audit sheet) see [`r14-audit.jpg`](r14-audit.jpg)
