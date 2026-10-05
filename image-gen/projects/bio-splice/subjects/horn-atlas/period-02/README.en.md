# Period 02 · Deer Antlers

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [review report](../rounds/ha-r2-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 14101 / 14102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Misty morning meadow · side backlight · eye level · square**

The side backlight traces the antlers' forks against the sky —— this page's protagonist is **the forked structure of the antlers**,
so the light comes from behind and to the side, giving every tine its own separate outline.

## 2. This period's subject and result

**Base = a hornless horse**　**Transplant = branching deer antlers H1**

| Part | ID | Landing site | Result |
|------|------|------|------|
| Deer antlers | H1 | top of the forehead (**empty surface**) | ✅ **fully established**: a complete pair of forked deer antlers, joining the skull naturally |

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-horse-antlers.png`](01-horse-antlers.png) | **5.00** ✅ preferred | `f2fe91d6` | `c1e6a90a26` |
| 2 | [`02-horse-antlers-b.png`](02-horse-antlers-b.png) | **5.00** ✅ preferred | `ab8b8a67` | `4ed1f3f244` |

Control: [`controls/horse.png`](controls/horse.png) —— the pure horse from the **same round** (hornless).

## 4. What this period verified

**All five thresholds pass** (Rules 105/107): the landing site is an empty surface (the horse is originally hornless), no bearing structure is needed,
no slot needs freeing, the shape differs and is highly recognisable, and the donor **is itself a horn**.
→ This is the first-page evidence for this volume's "zero failures".

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject horn-atlas 2 --dry
python3 run_round.py --subject horn-atlas 2
python3 score.py --round work/horn-atlas/r2/round.json --scores work/horn-atlas/r2/scores.json \
    --control base-horse --region head=350,80,400,400 \
    --audit-sheet subjects/horn-atlas/rounds/ha-r2-audit.jpg \
    --subject horn-atlas -o subjects/horn-atlas/rounds/ha-r2-review.md
python3 curate.py --period subjects/horn-atlas/period-02 --from work/horn-atlas/r2/round.json \
    --pick horse-antlers=01-horse-antlers --pick horse-antlers-b=02-horse-antlers-b \
    --control base-horse=controls/horse --note "…" --force
bash make_sheet.sh period subjects/horn-atlas/period-02
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 02 "Deer Antlers" delivered 2 images | 小七 |
