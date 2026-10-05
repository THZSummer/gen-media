# Period 01 · Twin-wing Baseline

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [review report](../rounds/wa-r1-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 13101 / 13102 / 13103**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Branch tip · side backlight · eye level 400mm · square**

The atlas's **first page**: the unified base itself. The side backlight traces the bird's outline and the edges of its feathers,
and the eye-level camera is the camera spec shared by the next four parts.

## 2. This period's subject and result

**Base = medium-sized bird**　**Transplant = none (baseline part)**

⚠️ This part **deliberately carries no transplanted part** (Rule 108): it is the **frame of reference** for the next four parts ——
the "second pair of wings" is the extra pair that appears on top of this bird, and without the baseline you cannot read "extra".

So this part has **no control shot** (the baseline is itself the control),
and the objective-metrics column is empty —— this is honestly noted in the [review report](../rounds/wa-r1-review.md).

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-bird-baseline.png`](01-bird-baseline.png) | **5.00** ✅ preferred | `3d80eb6b` | `4f2884affc` |
| 2 | [`02-bird-baseline-b.png`](02-bird-baseline-b.png) | **5.00** ✅ preferred | `ac1ca1f9` | `33e5fd555f` |
| 3 | [`03-bird-baseline-c.png`](03-bird-baseline-c.png) | **5.00** ✅ preferred | `62cb1c60` | `99fdabc314` |

## 4. What this period verified

**The "baseline part" is the skeleton of an atlas volume** (Rule 108):
both this volume and `horn-atlas` use the structure "part 1 = baseline, parts 2–5 = four candidate organs".
→ Benefit: the reader sees at a glance "what was added", and it is a natural anchor for the A/B controls that follow.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject wing-atlas 1 --dry
python3 run_round.py --subject wing-atlas 1
python3 score.py --round work/wing-atlas/r1/round.json --scores work/wing-atlas/r1/scores.json \
    --region back=250,200,550,500 \
    --audit-sheet subjects/wing-atlas/rounds/wa-r1-audit.jpg \
    --subject wing-atlas -o subjects/wing-atlas/rounds/wa-r1-review.md
python3 curate.py --period subjects/wing-atlas/period-01 --from work/wing-atlas/r1/round.json \
    --pick base-bird=01-bird-baseline --pick base-bird-b=02-bird-baseline-b \
    --pick base-bird-c=03-bird-baseline-c --note "…"
bash make_sheet.sh period subjects/wing-atlas/period-01
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 01 "Twin-wing Baseline" delivered 3 images (the atlas's frame of reference) | 小七 |
