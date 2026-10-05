# Period 04 · Sheep Horns

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [review report](../rounds/ha-r4-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 14101 / 14102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Misty morning meadow · side backlight · eye level · square**

Sheep horns are **curled** (spiralling beside the ears), so this page returns to the side backlight:
it gives every coil of the curl its own light-shadow boundary —— **the most recognisable piece in this volume**.

## 2. This period's subject and result

**Base = a hornless horse**　**Transplant = curled sheep horns H3**

| Part | ID | Landing site | Result |
|------|------|------|------|
| Sheep horns | H3 | top of the forehead (**empty surface**) | ✅ **fully established**: a pair of curled sheep horns spiralling beside the ears |

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-horse-ramhorns.png`](01-horse-ramhorns.png) | **5.00** ✅ preferred | `6ed1cad0` | `9552daafa3` |
| 2 | [`02-horse-ramhorns-b.png`](02-horse-ramhorns-b.png) | **5.00** ✅ preferred | `53cc94ad` | `a2f498cf0e` |

Control: [`controls/horse.png`](controls/horse.png) —— the pure horse from the **same round**.

## 4. What this period verified

All are "horns", but **deer antlers fork, cattle horns curve straight, sheep horns curl** ——
the three forms do not blur into one another on the same base, which shows that this volume's atlas value comes from
**differences in the donors' forms**, and not from tricks of presentation.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject horn-atlas 4 --dry
python3 run_round.py --subject horn-atlas 4
python3 score.py --round work/horn-atlas/r4/round.json --scores work/horn-atlas/r4/scores.json \
    --control base-horse --region head=350,80,400,400 \
    --audit-sheet subjects/horn-atlas/rounds/ha-r4-audit.jpg \
    --subject horn-atlas -o subjects/horn-atlas/rounds/ha-r4-review.md
python3 curate.py --period subjects/horn-atlas/period-04 --from work/horn-atlas/r4/round.json \
    --pick horse-ramhorns=01-horse-ramhorns --pick horse-ramhorns-b=02-horse-ramhorns-b \
    --control base-horse=controls/horse --note "…" --force
bash make_sheet.sh period subjects/horn-atlas/period-04
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 04 "Sheep Horns" delivered 2 images | 小七 |
