# Period 03 · Cattle Horns

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [review report](../rounds/ha-r3-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 14101 / 14102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Misty morning meadow · top light · eye level · square**

This page switches to **flat top light**: cattle horns are a solid structure that is "thick, smooth and ringed with keratin",
so the top light explains their volume and the rings at the base clearly, which exactly complements the deer antlers (recognised by outline).

## 2. This period's subject and result

**Base = a hornless horse**　**Transplant = thick cattle horns H2**

| Part | ID | Landing site | Result |
|------|------|------|------|
| Cattle horns | H2 | top of the forehead (**empty surface**) | ✅ **fully established** |

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-horse-oxhorns.png`](01-horse-oxhorns.png) | **5.00** ✅ preferred | `b6b9275d` | `399a5c969a` |
| 2 | [`02-horse-oxhorns-b.png`](02-horse-oxhorns-b.png) | **5.00** ✅ preferred | `2c6bbd3c` | `5583ca598f` |

Control: [`controls/horse.png`](controls/horse.png) —— the pure horse from the **same round**.

## 4. What this period verified

**The same base, the same meadow, only the horns swapped** —— the atlas's "constant within a period, varied between periods" shows most clearly here:
the base and the camera do not move, and **only the horns and the light change**, so it reads as two adjacent pages of the same volume.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject horn-atlas 3 --dry
python3 run_round.py --subject horn-atlas 3
python3 score.py --round work/horn-atlas/r3/round.json --scores work/horn-atlas/r3/scores.json \
    --control base-horse --region head=350,80,400,400 \
    --audit-sheet subjects/horn-atlas/rounds/ha-r3-audit.jpg \
    --subject horn-atlas -o subjects/horn-atlas/rounds/ha-r3-review.md
python3 curate.py --period subjects/horn-atlas/period-03 --from work/horn-atlas/r3/round.json \
    --pick horse-oxhorns=01-horse-oxhorns --pick horse-oxhorns-b=02-horse-oxhorns-b \
    --control base-horse=controls/horse --note "…" --force
bash make_sheet.sh period subjects/horn-atlas/period-03
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 03 "Cattle Horns" delivered 2 images | 小七 |
