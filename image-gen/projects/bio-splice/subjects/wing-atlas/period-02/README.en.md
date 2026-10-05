# Period 02 · Four Wings (Membranous)

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [review report](../rounds/wa-r2-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 13101 / 13102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Branch tip · top light · square**

The atlas's second page: **a pair of insect membranous wings appears on the back**. The top light makes the translucent membrane glow,
and the wing veins form a grid in the light —— this is the most direct material difference between "membranous wings" and the bird's own feathers.

## 2. This period's subject and result

**Base = medium-sized bird (keeping its own wings)**　**Transplant = insect membranous wings W2**

| Part | ID | Landing site | Result |
|------|------|------|------|
| Insect membranous wings | W2 | back (**empty surface**) | ✅ **fully established**: a pair of translucent membranous wings grows from the back |

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-bird-membrane.png`](01-bird-membrane.png) | **5.00** ✅ preferred | `9a71f344` | `f829f76dc8` |
| 2 | [`02-bird-membrane-b.png`](02-bird-membrane-b.png) | **5.00** ✅ preferred | `7e64c765` | `77266258c2` |

Control: [`controls/bird.png`](controls/bird.png) —— the pure bird from the **same round** (the same-spec version of the one in part 1).

## 4. What this period verified

1. **Both thresholds pass** (Rule 105): the landing site is the empty surface of the back; the donor **is itself a wing** (Rule 107).
2. Membranous wings and feathered wings are **not the same shape** (Rule 91) + high recognisability (Rule 90) → at a glance you can read that "a pair has been added".

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject wing-atlas 2 --dry
python3 run_round.py --subject wing-atlas 2
python3 score.py --round work/wing-atlas/r2/round.json --scores work/wing-atlas/r2/scores.json \
    --control base-bird --region back=250,200,550,500 \
    --audit-sheet subjects/wing-atlas/rounds/wa-r2-audit.jpg \
    --subject wing-atlas -o subjects/wing-atlas/rounds/wa-r2-review.md
python3 curate.py --period subjects/wing-atlas/period-02 --from work/wing-atlas/r2/round.json \
    --pick bird-membrane=01-bird-membrane --pick bird-membrane-b=02-bird-membrane-b \
    --control base-bird=controls/bird --note "…" --force
bash make_sheet.sh period subjects/wing-atlas/period-02
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 02 "Four Wings (Membranous)" delivered 2 images | 小七 |
