# Period 01 · Hornless Baseline

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [review report](../rounds/ha-r1-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 14101 / 14102 / 14103**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Misty morning meadow · soft light · eye level 400mm · square**

The atlas's **first page**: a horse that **originally has no horns**. The morning mist and soft light make the horse's body the only solid thing,
and the eye-level camera is the camera spec shared by the next four parts.

## 2. This period's subject and result

**Base = a standard horse**　**Transplant = none (baseline part)**

⚠️ This part **deliberately carries no transplanted part** (Rule 108): it is the **frame of reference** for the next four parts ——
"one more horn" cannot be read without the baseline.

So this part has **no control shot** (the baseline is itself the control), and the objective-metrics column is empty; this is noted in the review.

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-horse-baseline.png`](01-horse-baseline.png) | **5.00** ✅ preferred | `e583728c` | `1353e1632e` |
| 2 | [`02-horse-baseline-b.png`](02-horse-baseline-b.png) | **5.00** ✅ preferred | `55b60755` | `55278e9261` |
| 3 | [`03-horse-baseline-c.png`](03-horse-baseline-c.png) | **5.00** ✅ preferred | `542be338` | `5adc76e8c7` |

## 4. What this period verified

**"Hornless" is itself this volume's key design** (Rule 99):
the horse has no horns → the top of the forehead / the bridge of the nose are **empty surfaces** → the horns of the next four parts need no slot freed
and no bearing structure, and "all five thresholds passed" starts here.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject horn-atlas 1 --dry
python3 run_round.py --subject horn-atlas 1
python3 score.py --round work/horn-atlas/r1/round.json --scores work/horn-atlas/r1/scores.json \
    --region head=350,100,400,400 \
    --audit-sheet subjects/horn-atlas/rounds/ha-r1-audit.jpg \
    --subject horn-atlas -o subjects/horn-atlas/rounds/ha-r1-review.md
python3 curate.py --period subjects/horn-atlas/period-01 --from work/horn-atlas/r1/round.json \
    --pick base-horse=01-horse-baseline --pick base-horse-b=02-horse-baseline-b \
    --pick base-horse-c=03-horse-baseline-c --note "…"
bash make_sheet.sh period subjects/horn-atlas/period-01
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 01 "Hornless Baseline" delivered 3 images (the atlas's frame of reference) | 小七 |
