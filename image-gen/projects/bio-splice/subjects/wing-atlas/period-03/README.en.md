# Period 03 · Four Wings (Leathery)

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [review report](../rounds/wa-r3-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 13101 / 13102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Cave mouth · hard light · square**

The atlas's third page: **a pair of bat leathery wings on the back**. The hard light at the cave mouth plus the deep background
make the leathery membrane and the long thin finger bones very readable —— the "skeletal feel" of leathery wings is their identifying mark.

## 2. This period's subject and result

**Base = medium-sized bird (keeping its own wings)**　**Transplant = bat leathery wings W3**

| Part | ID | Landing site | Result |
|------|------|------|------|
| Bat leathery wings | W3 | back (**empty surface**) | ✅ **fully established** |

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-bird-bat.png`](01-bird-bat.png) | **5.00** ✅ preferred | `605234aa` | `a8847bfeb3` |
| 2 | [`02-bird-bat-b.png`](02-bird-bat-b.png) | **5.00** ✅ preferred | `c17087cf` | `0d04e7dfa3` |

Control: [`controls/bird.png`](controls/bird.png) —— the pure bird from the **same round**.

## 4. What this period verified

Leathery wings and membranous wings are both "real wings", but their **materials are completely different** (leather vs translucent membrane),
which shows that this volume's differences come from **the donors' own forms**, not from differences in presentation.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject wing-atlas 3 --dry
python3 run_round.py --subject wing-atlas 3
python3 score.py --round work/wing-atlas/r3/round.json --scores work/wing-atlas/r3/scores.json \
    --control base-bird --region back=250,200,550,500 \
    --audit-sheet subjects/wing-atlas/rounds/wa-r3-audit.jpg \
    --subject wing-atlas -o subjects/wing-atlas/rounds/wa-r3-review.md
python3 curate.py --period subjects/wing-atlas/period-03 --from work/wing-atlas/r3/round.json \
    --pick bird-bat=01-bird-bat --pick bird-bat-b=02-bird-bat-b \
    --control base-bird=controls/bird --note "…" --force
bash make_sheet.sh period subjects/wing-atlas/period-03
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 03 "Four Wings (Leathery)" delivered 2 images | 小七 |
