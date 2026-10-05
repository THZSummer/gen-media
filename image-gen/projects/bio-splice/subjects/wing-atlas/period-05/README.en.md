# Period 05 · Four Wings (Crane Feathers)

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [review report](../rounds/wa-r8-review.en.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**seed 13101 / 13102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Autumn forest · backlight · wide-angle 135mm · landscape 1280×1024**

The atlas's last page: **a pair of white crane wings on the back**. The autumn forest's warm background plus the backlight
make the white wings the brightest thing in the frame —— **double-layer wings** (its own brown wings + the white wings on the back)
are this page's clearest atlas relationship.

## 2. This period's subject and result

**Base = medium-sized bird (keeping its own wings)**　**Transplant = crane white wings W5'**

| Part | ID | Landing site | Result |
|------|------|------|------|
| Crane white wings | W5' | back (**empty surface**) | ✅ **fully established** —— the most convincing image in this volume |

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-bird-crane.png`](01-bird-crane.png) | **5.00** ✅ preferred | `16b5234d` | `bbc5d2b45c` |
| 2 | [`02-bird-crane-b.png`](02-bird-crane-b.png) | **5.00** ✅ preferred | `dd523efc` | `bf4e43b47b` |

Control: [`controls/bird.png`](controls/bird.png) —— the pure bird from the **same round**.

## 4. What this period verified

1. **"Is a wing" + "different shape" = the most stable combination**: crane wings are themselves wings (Rule 107),
   and the long white wings differ from its own short brown wings **in both shape and colour** (Rule 91).
2. The closing page condenses the whole volume's logic into one sentence:
   **one and the same bird, with the wings on its back swapped four times —— the atlas's six pages (baseline + four kinds + this page) close here.**

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject wing-atlas 8 --dry
python3 run_round.py --subject wing-atlas 8
python3 score.py --round work/wing-atlas/r8/round.json --scores work/wing-atlas/r8/scores.json \
    --control base-bird --region back=300,200,600,500 \
    --audit-sheet subjects/wing-atlas/rounds/wa-r8-audit.jpg \
    --subject wing-atlas -o subjects/wing-atlas/rounds/wa-r8-review.md
python3 curate.py --period subjects/wing-atlas/period-05 --from work/wing-atlas/r8/round.json \
    --pick bird-crane=01-bird-crane --pick bird-crane-b=02-bird-crane-b \
    --control base-bird=controls/bird --note "…" --force
bash make_sheet.sh period subjects/wing-atlas/period-05
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.5 | Period 05 "Four Wings (Crane Feathers)" delivered 2 images (finale) | 小七 |
