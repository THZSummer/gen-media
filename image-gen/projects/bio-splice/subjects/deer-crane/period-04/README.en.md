# Period 04 · Neck and Legs Together

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/dc-r5-review.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**seed 7101 onward (multiple takes, see the provenance table)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Frosty morning meadow · cold light · eye level · landscape 1280×1024**

Frost presses the meadow into a sheet of cold white, so the deer and its parts become the only warm colour in the frame; the landscape canvas puts the vertical change of "a long neck + slender legs" into a horizontal composition.

> The presentation layer is **constant within a period** (every shot in that period, controls included, shares one set) and **varies between periods** (each of the five periods has its own identity).

## 2. This period's subject and result

**Base = deer**　**Transplant = crane neck G1 + crane legs G2 (the base does not write legs)**

| Part | ID | Result |
|------|------|------|
| Long neck | G1 | ⚠️ partially established |
| Slender legs | G2 | ⚠️ partially established |
| Both parts in one body | G1+G2 | ✅ neither crowded the other out, and no second individual appeared |

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-deer-neck-legs.png`](01-deer-neck-legs.png) | G1+G2 (**main image**) | **4.25** ✅ final | `39c69736` | `8eea44bee6` |
| 2 | [`02-deer-neck-legs-b.png`](02-deer-neck-legs-b.png) | G1+G2 (seed 7102) | **4.25** ✅ final | `8798278f` | `5756c5a9bc` |

Control: [`controls/deer.png`](controls/deer.png) —— the pure-deer base from the **same round** (same seed, same presentation, same sentence skeleton).

## 4. What this period verified

1. Cross-region stacking (neck in the head area, legs on the lower body) holds, and the two parts do not interfere with each other (rule 59).
2. But each part only reaches partial on its own, so together they are still "a lanky deer" — **stacking cannot turn partial into complete**.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject deer-crane 5 --dry
python3 run_round.py --subject deer-crane 5
python3 score.py --round work/deer-crane/r5/round.json --scores work/deer-crane/r5/scores.json \
    --control base-deer --region neck=450,150,380,380 --region legs=420,600,420,380 \
    --audit-sheet subjects/deer-crane/rounds/dc-r5-audit.jpg \
    --subject deer-crane -o subjects/deer-crane/rounds/dc-r5-review.md
python3 curate.py --period subjects/deer-crane/period-04 --from work/deer-crane/r5/round.json \
    --pick deer-neck-legs=01-deer-neck-legs --pick deer-neck-legs-b=02-deer-neck-legs-b \
    --control base-deer=controls/deer --note "…" --force
bash make_sheet.sh period subjects/deer-crane/period-04
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 04 "Neck and Legs Together" delivered 2 images (partially established) | 小七 |
