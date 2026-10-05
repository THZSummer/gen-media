# Period 05 · Narwhal Tusk / Rhino Horn (finale)

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [review report](../rounds/ha-r5-review.en.md)
> Engine: Z-Image-Turbo　**1024×1280**　steps 12　**seed 14101 / 14102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Frosty morning grassland · side backlight · tight face close-up · vertical 1024×1280**

The finale moves from "paired horns" to **a single horn**, and switches to a **tight face close-up**:
under the side backlight of the frosty morning, the spiral ridges and the keratin on the bridge of the nose are enlarged enough to read their texture.

## 2. This period's subject and result

**Base = a hornless horse**　**Transplant = narwhal tusk H5 + rhino horn H4**

| Part | ID | Landing site | Result |
|------|------|------|------|
| Narwhal tusk | H5 | top of the forehead (**empty surface**) | ✅ **fully established**: a single long spiral tusk |
| Rhino horn | H4 | **bridge of the nose** (empty surface) | ✅ **fully established**: a single heavy keratinous horn |

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-horse-narwhal.png`](01-horse-narwhal.png) | **5.00** ✅ preferred | `b72a2d5c` | `04ffb9b2a0` |
| 2 | [`02-horse-rhino.png`](02-horse-rhino.png) | **5.00** ✅ preferred | `ab66b26e` | `58a184dc02` |

Control: [`controls/horse.png`](controls/horse.png) —— the pure horse from the **same round** (close-up camera).

## 4. What this period verified

1. **A tusk is not a horn, but the form rescues the semantics** (Rule 110): the narwhal's tusk is anatomically a "tooth",
   but the form of "a single upward spiral" was accepted by the model —— **when form and semantics both hold, a small semantic deviation is carried through**.
2. The closing page completes the atlas's closure: **from hornless → paired horns (deer / cattle / sheep) → a single horn (top of the forehead / on the nose)**.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject horn-atlas 5 --dry
python3 run_round.py --subject horn-atlas 5
python3 score.py --round work/horn-atlas/r5/round.json --scores work/horn-atlas/r5/scores.json \
    --control base-horse --region head=300,80,450,500 \
    --audit-sheet subjects/horn-atlas/rounds/ha-r5-audit.jpg \
    --subject horn-atlas -o subjects/horn-atlas/rounds/ha-r5-review.md
python3 curate.py --period subjects/horn-atlas/period-05 --from work/horn-atlas/r5/round.json \
    --pick horse-narwhal=01-horse-narwhal --pick horse-rhino=02-horse-rhino \
    --control base-horse=controls/horse --note "…" --force
bash make_sheet.sh period subjects/horn-atlas/period-05
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 05 "Narwhal Tusk / Rhino Horn" delivered 2 images (finale) | 小七 |
