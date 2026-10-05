# Period 02 · The Eagle with Beast Ears and Tail

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/r17-review.en.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**all 4 images share seed 4201** (including the same-round base control)
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Characteristics (Presentation)

**Dusk wet grassland · warm side backlight · eye-level full body 400mm · square**

This period showcases the two small parts **ears and tail**: the ears are on the head and the tail behind the body, the two ends far apart, so the camera stays at **eye-level full body** to take both ends into the frame; identity is instead carried by **light** — the warm side backlight on the dusk wetland picks out the ear tips and the tail base, completely separating this period from Period 01's misty soft light.

> The presentation layer is **constant within a period**: every shot in this round (including the base control) shares the same habitat/light/camera/canvas,
> so the "transplant vs base" control stays clean. **It varies between periods** — each of the five periods has its own identity, see
> the period style table on the [sub-theme home page](../README.en.md).

## 2. This Period's Theme and Results

**Base = eagle** (a strong species, so the whole holds together)　**Transplant parts = small cat parts**

| Part | ID | Result |
|------|------|------|
| Cat ears | C1 | ✅ Pointed cat ears grow on the eagle's head |
| Cat tail | C5 | ✅ A **tabby-ringed cat tail** extends from the tail base (curled upward) |
| Cat ears + cat tail | C1+C5 | ✅ Both hold at once (**main image**) |
| Cat paws (not included) | C4 | ❌ The feet remain eagle talons; `soft furry paws` was not executed |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-eagle-cat-ears.png`](01-eagle-cat-ears.png) | C1 cat ears | **5.00** ✅ preferred | `430f0453` | `32467573ac` |
| 2 | [`02-eagle-cat-tail.png`](02-eagle-cat-tail.png) | C5 cat tail | **4.85** ✅ preferred | `06115702` | `cb0485ce3d` |
| 3 | [`03-eagle-cat-ears-tail.png`](03-eagle-cat-ears-tail.png) | C1+C5 (**main image**) | **5.00** ✅ preferred | `538f8462` | `3f64c94f5b` |

Control: [`controls/eagle.png`](controls/eagle.png) — the **same-round** pure-eagle base (same seed, same presentation, same sentence skeleton);
every objective metric in this round is measured against it.

## 4. Verification in This Period

1. **Whether a transplant holds depends on whether the base has a "placeholder"**: the eagle's description has no ears and no cat-style tail, so both parts hold; but the feet are occupied by `scaled yellow legs with black talons`, so the cat paws do not hold.
2. **⚠️ The presentation layer is not neutral**: the same cat-tail clause **holds** in R6's eye-level 600mm full-body portrait, yet in R10/R14's **low-camera 85mm vertical** it instead **draws an extra complete cat** (the donor is turned into an individual); returning the camera to eye level (this round) makes it hold again → when changing camera/canvas you must re-check whether the part still lands (rule 80).

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject cat-eagle 17 --dry
python3 run_round.py --subject cat-eagle 17
python3 score.py --round work/cat-eagle/r17/round.json --scores work/cat-eagle/r17/scores.json \
    --control base-eagle --region ears=400,60,320,300 --region tail=560,200,400,500 \
    --audit-sheet subjects/cat-eagle/rounds/r17-audit.jpg \
    --subject cat-eagle -o subjects/cat-eagle/rounds/r17-review.md
python3 curate.py --period subjects/cat-eagle/period-02 --from work/cat-eagle/r17/round.json \
    --pick e-cat-ears=01-eagle-cat-ears --pick e-cat-tail=02-eagle-cat-tail \
    --pick e-cat-ears-tail=03-eagle-cat-ears-tail \
    --control base-eagle=controls/eagle.png --note "…" --force
bash make_sheet.sh period subjects/cat-eagle/period-02
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-04 | v0.1 | Period 02 delivery: cat ears / cat tail / ears + tail, 3 images in total (original presentation = autumn meadow) | 小七 |
| 2026-10-04 | **v0.2** | **Presentation redone**: the camera returns to eye-level full body and identity is instead carried by dusk warm side backlight; the evidence that `e-cat-tail` drags out a second cat under the low-camera vertical is kept in R10/R14 | 小七 |
