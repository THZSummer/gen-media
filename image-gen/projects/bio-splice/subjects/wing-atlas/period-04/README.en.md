# Period 04 · Four Wings (Flying-fish Fins)

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [review report](../rounds/wa-r7-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 13101 / 13102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Waterside · moist light · square**

The atlas's fourth page: **a pair of long flying-fish fins on the back**. The moist reflections at the waterside echo the streamline of the long fins;
this page's material is "thin, stiff fin rays", different from both the membranous wings and the leathery wings.

## 2. This period's subject and result

**Base = medium-sized bird (keeping its own wings)**　**Transplant = flying-fish long fins W4'**

| Part | ID | Landing site | Result |
|------|------|------|------|
| Flying-fish long fins | W4' | back (**empty surface**) | ✅ **fully established** |

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-bird-flyfish.png`](01-bird-flyfish.png) | **5.00** ✅ preferred | `691b86a1` | `cb1d03c7b1` |
| 2 | [`02-bird-flyfish-b.png`](02-bird-flyfish-b.png) | **5.00** ✅ preferred | `475699d5` | `d7332e52d8` |

Control: [`controls/bird.png`](controls/bird.png) —— the pure bird from the **same round**.

## 4. What this period verified: **semantics is what matters** (Rule 107)

This page's donor comes from **the same follow-up round** (R6) and differs from the failed "fish pectoral fins" by a single word:

| Donor | Semantics | Result |
|------|------|------|
| `stiff fish pectoral fins` | merely fins | ❌ **0%** (R4) |
| **`long gliding flying-fish fins`** | fins, but **carrying "flight" in themselves** | ✅ 5.00 |

→ **A "wing-like shape" alone is not enough; the donor must carry the semantics of "being able to fly".**

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject wing-atlas 7 --dry
python3 run_round.py --subject wing-atlas 7
python3 score.py --round work/wing-atlas/r7/round.json --scores work/wing-atlas/r7/scores.json \
    --control base-bird --region back=250,200,550,500 \
    --audit-sheet subjects/wing-atlas/rounds/wa-r7-audit.jpg \
    --subject wing-atlas -o subjects/wing-atlas/rounds/wa-r7-review.md
python3 curate.py --period subjects/wing-atlas/period-04 --from work/wing-atlas/r7/round.json \
    --pick bird-flyfish=01-bird-flyfish --pick bird-flyfish-b=02-bird-flyfish-b \
    --control base-bird=controls/bird --note "…" --force
bash make_sheet.sh period subjects/wing-atlas/period-04
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 04 "Four Wings (Flying-fish Fins)" delivered 2 images | 小七 |
