# Period 03 · The Winged Cat

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/r15-review.en.md)
> Engine: Z-Image-Turbo　**1024×1280**　steps 12　**all 4 images share seed 4201** (including the same-round base control)
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Characteristics (Presentation)

**Post-rain woodland · backlight · wide-angle low camera at the wingspan · vertical 1024×1280**

This period's protagonist is the **wing**, and a full spread-wing pose is needed for the structure to read clearly, so it is shot with a **wide-angle low camera** at the instant of the wingspan; the backlight of the post-rain woodland picks out every feather barb — the most "wildlife documentary" image in the whole sub-theme.

> The presentation layer is **constant within a period**: every shot in this round (including the base control) shares the same habitat/light/camera/canvas,
> so the "transplant vs base" control stays clean. **It varies between periods** — each of the five periods has its own identity, see
> the period style table on the [sub-theme home page](../README.en.md).

## 2. This Period's Theme and Results

**Base = cat** (a weak species)　**Transplant parts = local parts of the eagle**

| Part | ID | Result |
|------|------|------|
| Eagle wings | E2 | ✅ The cat spreads a complete pair of eagle wings |
| Eagle tail feathers | E5 | ✅ Fan-shaped tail feathers grow from the tail base (somewhat straight, credibility a little lower) |
| Eagle wings + eagle tail feathers | E2+E5 | ✅ Both hold at once (**main image**) |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-cat-eagle-wings.png`](01-cat-eagle-wings.png) | E2 eagle wings (**main image**) | **5.00** ✅ preferred | `34dd732b` | `6824a52ef7` |
| 2 | [`02-cat-eagle-tail.png`](02-cat-eagle-tail.png) | E5 eagle tail feathers | **4.35** ✅ final | `c5cf8636` | `b0e4ee59ee` |
| 3 | [`03-cat-eagle-wings-tail.png`](03-cat-eagle-wings-tail.png) | E2+E5 | **4.80** ✅ preferred | `10a04abd` | `eb152c4f9d` |

Control: [`controls/cat.png`](controls/cat.png) — the **same-round** pure-cat base (same seed, same presentation, same sentence skeleton);
every objective metric in this round is measured against it.

## 4. Verification in This Period

1. **The pose clause must stay silent about the target part**: R11's pose read "it spreads both wings to the maximum", and as a result **even the base control grew eagle wings** — the control was contaminated and the whole round's objective metrics were voided; after changing it to "it is about to settle, the whole body extended", the control went back to being a wingless cat (rule 79).
2. The spread-wing pose actually **improved** the wings' readability: under backlight every feather barb is distinct, another positive example of "point the camera at the subject" (rule 71).

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject cat-eagle 15 --dry
python3 run_round.py --subject cat-eagle 15
python3 score.py --round work/cat-eagle/r15/round.json --scores work/cat-eagle/r15/scores.json \
    --control base-cat --region wings=140,120,760,480 --region rear=380,600,300,500 \
    --audit-sheet subjects/cat-eagle/rounds/r15-audit.jpg \
    --subject cat-eagle -o subjects/cat-eagle/rounds/r15-review.md
python3 curate.py --period subjects/cat-eagle/period-03 --from work/cat-eagle/r15/round.json \
    --pick c-eagle-wings=01-cat-eagle-wings --pick c-eagle-tail=02-cat-eagle-tail \
    --pick c-eagle-wings-tail=03-cat-eagle-wings-tail \
    --control base-cat=controls/cat.png --note "…" --force
bash make_sheet.sh period subjects/cat-eagle/period-03
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-04 | v0.1 | Period 02 delivery: cat ears / cat tail / ears + tail, 3 images in total (original presentation = autumn meadow) | 小七 |
| 2026-10-04 | **v0.2** | **Presentation redone**: the pose clause drops "both wings spread" (it contaminated the base control); switched to shooting the wingspan instant with backlight and a wide-angle low camera | 小七 |
