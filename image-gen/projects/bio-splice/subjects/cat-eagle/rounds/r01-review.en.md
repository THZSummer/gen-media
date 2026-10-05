# Score review · R1 (cat-eagle)

> 🌐 Language: **English** | [中文](r01-review.md)

> Engine: `zimage`　Round description: the four corners of a 2×2 splice matrix + splice semantics A/B/C with same-seed controls (pure cat / pure eagle as the control group)
> Base control: **pure-eagle control (period-01/controls/eagle.png, an early control not from this round)**　Not scored (control / reference): `cat` (same round, same seed; objective metrics are unaffected by pose)
> Scoring dimensions: A transplant in place .30 ｜ B base intact .20 ｜ C anatomy credible .20 ｜ D photographic unity .15 ｜ E concept legible .15
> Threshold: `fatal` non-empty / A<3 / B<3 → failed; total ≥4.0 and A≥4 → preferred final; ≥3.5 → final; the rest are alternates (**not included as finals**)
> Objective metrics are used only for alerts (region diff < 1.5 = the transplant sentence was a no-op); they do not enter the score

| Shot | A | B | C | D | E | Total | Verdict | Global diff vs base | Region diff |
|------|---|---|---|---|---|------|------|--------------|--------|
| `owl-seamless` | 5 | 5 | 5 | 5 | 5 | **5.00** | ✅ Final (preferred) | 18.26 | head 28.7 |
| `owl-seam` | 5 | 5 | 4 | 5 | 5 | **4.80** | ✅ Final (preferred) | 21.25 | head 35.7 |
| `owl-surreal` | 5 | 5 | 5 | 5 | 3 | **4.70** | ✅ Final (preferred) | 17.94 | head 29.1 |
| `eaglecat-seam` | 3 | 3 | 3 | 5 | 3 | **3.30** | ❌ Failed | 28.31 | head 37.2 |
| `eaglecat-seamless` | 0 | 5 | 5 | 5 | 1 | **2.90** | ❌ Failed | 17.11 | head 17.5 |
| `eaglecat-surreal` | 0 | 5 | 5 | 5 | 1 | **2.90** | ❌ Failed | 18.41 | head 22.3 |

## Per-shot pros and cons

### `owl-seamless` — ✅ Final (preferred) (total 5.00)
- **A Transplant in place**: 5/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 5/5
- 👍 Cat head / green eyes / whiskers / tabby fur on the neck attached to the eagle torso, folded wings and yellow talons, with a seamless transition
- 👍 The same seed reused the eagle control's camera, so "the same eagle with a cat head" is readable at a glance
- 👎 The transition between the neck fur and the feathers feels slightly composited

### `owl-seam` — ✅ Final (preferred) (total 4.80)
- **A Transplant in place**: 5/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 4/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 5/5
- 👍 A longitudinal stitching line appears along the front edge of the neck and chest, making the seam semantics clear
- 👎 The stitching runs only along the front of the neck and does not go all the way around, weaker than the prompt describes
- 👎 The specimen feel lowers anatomical credibility

### `owl-surreal` — ✅ Final (preferred) (total 4.70)
- **A Transplant in place**: 5/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 3/5
- 👍 Like version A, a successful seamless splice
- 👎 mean_abs_diff against owl-seamless is only 8.9, so the "surreal" sentence is a no-op → conceptually redundant

### `eaglecat-seam` — ❌ Failed (total 3.30)
- **A Transplant in place**: 3/5
- **B Base intact**: 3/5
- **C Anatomy credible**: 3/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 3/5
- 👍 Fur on the legs and a seam on the chest; some cat elements appear
- 👎 The feet are still eagle talons
- 👎 The head is a "beak + cat ears" hybrid, not a clean eagle head
- ⛔ **Fatal**: the head is a hybrid species: an eagle beak and cat ears at the same time, reading as a broken collage

### `eaglecat-seamless` — ❌ Failed (total 2.90)
- **A Transplant in place**: 0/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 1/5
- 👍 As a pure-eagle photograph it is high quality in itself
- 👎 The feet are eagle talons (yellow scaled tarsi + black curved claws) and the hindquarters are pure eagle wing feathers
- ⛔ **Fatal**: zero cat elements: it has fully degenerated into a pure eagle; the transplant never happened

### `eaglecat-surreal` — ❌ Failed (total 2.90)
- **A Transplant in place**: 0/5
- **B Base intact**: 5/5
- **C Anatomy credible**: 5/5
- **D Photographic unity**: 5/5
- **E Concept legible**: 1/5
- 👍 As a pure-eagle photograph it is high quality in itself
- 👎 Almost identical to eaglecat-seamless
- ⛔ **Fatal**: zero cat elements: it has fully degenerated into a pure eagle

## Conclusion

- Accepted as finals: **3** images — `owl-seamless`, `owl-seam`, `owl-surreal`
- Failed: 3 images; alternates (also not included as finals): 0
- Suggested main image: `owl-seamless`

> For the basis of the verdict (zoomed-in audit sheet) see [`r01-audit.jpg`](r01-audit.jpg)
