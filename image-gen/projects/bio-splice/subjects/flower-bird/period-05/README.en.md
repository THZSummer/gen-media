# Period 5 · Flower-and-bird (finale)

> 🌐 Language: **English** | [中文](README.md)

> Back to the [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [scoring review report](../rounds/fb2-r8-review.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**seed 11101 / 11102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Source: [`manifest.json`](manifest.json)

---

## 1. Features of this period (presentation)

**Full branch · backlight · wide-angle 45mm · landscape 1280×1024**

The finale photographs not one flower but **a whole branch**: several flowers open on a new spring shoot,
and a plume feather stands in each flower's heart, its filaments shining under backlight ——
this is the literal meaning of the painting genre "flower-and-bird".

## 2. Theme and results of this period

**Base ＝ white magnolia branch (magnolia)**　**Donor ＝ plume feather P6 + down feather P5**

| Part | Landing site | Result |
|------|------|------|
| Plume feather | flower axis | ✅ fully works (every flower has one) |
| Down feather | flower centre | ✅ works |

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-flower-bird.png`](01-flower-bird.png) | **5.00** ✅ first choice | `13c3bc2c` | `d9b4bd4738` |
| 2 | [`02-flower-bird-b.png`](02-flower-bird-b.png) | **5.00** ✅ first choice | `319adc0c` | `f76d595e71` |

Control: [`controls/flower.png`](controls/flower.png) —— the **same-round** pure branch.

## 4. Verification in this period

1. **Many flowers on a full branch work at the same time**: the same sentence takes effect on every flower in the image, with no case of "only one grew out".
2. The point of the finale period is **to gather this set of mechanism findings into a single image**:
   the petals cannot be swapped out (P1 0%) → so let the "bird" grow out of the flower's heart —— **the limitation gave a better composition** (Rule 104).

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject flower-bird 8 --dry
python3 run_round.py --subject flower-bird 8
python3 score.py --round work/flower-bird/r8/round.json --scores work/flower-bird/r8/scores.json \
    --control base-flower --region axis=300,150,680,600 \
    --audit-sheet subjects/flower-bird/rounds/fb2-r8-audit.jpg \
    --subject flower-bird -o subjects/flower-bird/rounds/fb2-r8-review.md
python3 curate.py --period subjects/flower-bird/period-05 --from work/flower-bird/r8/round.json \
    --pick flower-bird=01-flower-bird --pick flower-bird-b=02-flower-bird-b \
    --control base-flower=controls/flower --note "…" --force
bash make_sheet.sh period subjects/flower-bird/period-05
```

---

## Document revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 5 "Flower-and-bird" delivered 2 images (finale) | 小七 |
