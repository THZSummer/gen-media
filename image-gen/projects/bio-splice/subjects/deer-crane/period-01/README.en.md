# Period 01 · The Long-Necked Deer

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/dc-r1-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 7101 onward (multiple takes, see the provenance table)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Misty bamboo grove · soft light · eye level 400mm · square**

The bamboo grove's vertical lines are isomorphic with the "long neck" theme; the mist flattens the background so that the length of the neck becomes the only readable direction in the frame. The eye-level camera looks neither up nor down — the neck's length is not fooled by perspective.

> The presentation layer is **constant within a period** (every shot in that period, controls included, shares one set) and **varies between periods** (each of the five periods has its own identity).

## 2. This period's subject and result

**Base = deer**　**Transplant = the crane's long neck G1 (the base does not write a neck, freeing up the neck slot)**

| Part | ID | Result |
|------|------|------|
| Long neck | G1 | ⚠️ **partially established**: the neck is clearly longer and thinner and stands up, and the posture leans toward a wading bird; but there are **none of the crane's fine grey feathers**, and the identity still reads as deer |

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-deer-craneneck.png`](01-deer-craneneck.png) | G1 (**main image**) | **4.25** ✅ final | `671ea052` | `06af7f6eb4` |
| 2 | [`02-deer-craneneck-b.png`](02-deer-craneneck-b.png) | G1 (seed 7102) | **4.25** ✅ final | `bb2dba96` | `ac89be033f` |

Control: [`controls/deer.png`](controls/deer.png) —— the pure-deer base from the **same round** (same seed, same presentation, same sentence skeleton).

## 4. What this period verified

1. **The deer's neck is a canonical structure** (rule 87): deleting the neck description from the base does not help either — the model adds a neck back on its own; the crane-neck sentence can only **change the shape** (longer and thinner), not the material.
2. This period honestly gives A=3 (partially in place), rather than full marks just because it "looks more slender".

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject deer-crane 1 --dry
python3 run_round.py --subject deer-crane 1
python3 score.py --round work/deer-crane/r1/round.json --scores work/deer-crane/r1/scores.json \
    --control base-deer --region neck=380,150,300,300 \
    --audit-sheet subjects/deer-crane/rounds/dc-r1-audit.jpg \
    --subject deer-crane -o subjects/deer-crane/rounds/dc-r1-review.md
python3 curate.py --period subjects/deer-crane/period-01 --from work/deer-crane/r1/round.json \
    --pick deer-craneneck=01-deer-craneneck --pick deer-craneneck-b=02-deer-craneneck-b \
    --control base-deer=controls/deer --note "…" --force
bash make_sheet.sh period subjects/deer-crane/period-01
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 01 "The Long-Necked Deer" delivered 2 images (partially established) | 小七 |
