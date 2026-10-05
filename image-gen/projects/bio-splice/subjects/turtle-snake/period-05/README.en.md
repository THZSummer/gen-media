# Period 05 · Xuanwu (finale)

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/ts-r6-review.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**all 3 images share seed 5101 (plus takes at 5102/5103)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Dusk water surface · backlit silhouette · eye-level wide angle 35mm · landscape 1280×1024**

The finale period puts **all three parts — neck + tail + coiled body —** on the same turtle, and gives Xuanwu the scene it deserves: a dusk water surface, backlight, a broad landscape frame, with the reflection in the water and the silhouette of the subject merging into a complete Four Symbols figure.

> The presentation layer is **constant within a period**: every shot in this round (including the base control) shares the same habitat/light/camera/canvas,
> so the "transplant vs base" control is clean; **it varies between periods**, and each of the five periods has its own identity.

## 2. This period's subject and result

**Base = turtle**　**Transplant = snake neck N1 + snake tail N2 + coiled body N3**

| Part | ID | Result |
|------|------|------|
| Snake neck | N1 | ✅ |
| Snake tail | N2 | ✅ |
| Coiled body | N3 | ✅ coiled in front of / beside the shell |
| All three on one body | N1+N2+N3 | ✅ **one individual, no second one** |

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-turtle-xuanwu.png`](01-turtle-xuanwu.png) | N1+N2+N3 (**main image**) | **5.00** ✅ preferred | `707c87f7` | `78ef41eb7c` |
| 2 | [`02-turtle-xuanwu-coiled.png`](02-turtle-xuanwu-coiled.png) | N1+N2+N3 (seed 5102) | **5.00** ✅ preferred | `d267d6c0` | `c76b0f0f04` |

Control: [`controls/turtle.png`](controls/turtle.png) —— the pure-turtle base from the **same round** (same seed, same presentation, same sentence skeleton),
and every objective metric in this round was measured against it.

## 4. What this period verified

1. **"Xuanwu" is established**: the snake neck raised, the long tail trailing out, the snake body coiled on the shell — it reads as a single composite figure rather than "three snakes stuck onto a turtle".
2. The three parts belong to three regions — head/neck, shell, tail — verifying once again that **the independent variable of the constraint is region distribution, not the number of parts** (rule 68).

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject turtle-snake 6 --dry
python3 run_round.py --subject turtle-snake 6
python3 score.py --round work/turtle-snake/r6/round.json --scores work/turtle-snake/r6/scores.json \
    --control base-turtle --region neck=400,150,300,300 --region coil=520,300,420,300 \
    --audit-sheet subjects/turtle-snake/rounds/ts-r6-audit.jpg \
    --subject turtle-snake -o subjects/turtle-snake/rounds/ts-r6-review.md
python3 curate.py --period subjects/turtle-snake/period-05 --from work/turtle-snake/r6/round.json \
    --pick turtle-all3=01-turtle-xuanwu \
    --pick turtle-all3-b=02-turtle-xuanwu-coiled \
    --control base-turtle=controls/turtle --note "…" --force
bash make_sheet.sh period subjects/turtle-snake/period-05
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Period 05 "Xuanwu" delivered 2 images: neck + tail + coiled body all on one body | 小七 |
