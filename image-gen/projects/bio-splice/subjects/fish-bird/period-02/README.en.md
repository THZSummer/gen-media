# Period 02 · Half Out of Water

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/fb-r11-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**starting at seed 6101 (see the provenance table for the multiple takes)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Waterline crossing the body · side light · eye level 135mm · square**

The second frame of the timeline: **the waterline still cuts across the body**. This frame is the hardest — the part above water and the part soaking in the water exist at the same time, and the "wing" can only grow on the side that is above water (rule 86).

> The emergence stage is **constant within a period** (each period stops at a single instant),
> **but varies between periods**: the waterline position, camera, light and canvas all differ — the five periods together form a timeline.

## 2. This period's subject and result

**Base = fish (out of water)**　**Transplant = bird wing B1**

| Part | ID | Result |
|------|------|------|
| Bird wing | B1 | ✅ **fully established**: a complete pair of bird wings grows from the fish's torso, and the feather structure joins naturally with the fish body |

> ⚠️ This period is the **direct product** of the "habitat hard constraint" (rule 85):
> with the same base and the same sentence, landing is 0% underwater and 100% above the water surface.
> So every fish-bird period has to be an **out-of-water** scene.

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-fish-wings-half.png`](01-fish-wings-half.png) | B1 (half-spread, positioned high, **main image**) | **5.00** ✅ preferred | `3fd434ff` | `b1d803e18c` |
| 2 | [`02-fish-wings-half-b.png`](02-fish-wings-half-b.png) | B1 (same as above, seed 6102) | **5.00** ✅ preferred | `4006ced6` | `20580afda3` |
| 3 | [`03-fish-wings-half-c.png`](03-fish-wings-half-c.png) | B1 (same as above, seed 6104) | **5.00** ✅ preferred | `08fd4153` | `1929d924f7` |

Control: [`controls/fish.png`](controls/fish.png) —— the pure-fish base from the **same round** (same seed, same presentation, same sentence skeleton).

## 4. What this period verified

1. **Scene compatibility is judged by region** (rule 86): in R7 the same wing sentence written on the **side of the body** (below the waterline) was eaten by the scene; changing it to **half-spread, positioned higher** (the side above water) made it land.
2. All three seeds succeeded, which shows this wording is stable — **once the wording is fixed, extra takes are cheap** (rule 84).

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject fish-bird 11 --dry
python3 run_round.py --subject fish-bird 11
python3 score.py --round work/fish-bird/r11/round.json --scores work/fish-bird/r11/scores.json \
    --control base-fish --region body=250,300,520,380 \
    --audit-sheet subjects/fish-bird/rounds/fb-r11-audit.jpg \
    --subject fish-bird -o subjects/fish-bird/rounds/fb-r11-review.md
python3 curate.py --period subjects/fish-bird/period-02 --from work/fish-bird/r11/round.json \
    --pick fish-wings-half=01-fish-wings-half \
    --pick fish-wings-half-b=02-fish-wings-half-b \
    --pick fish-wings-half-c=03-fish-wings-half-c \
    --control base-fish=controls/fish --note "…" --force
bash make_sheet.sh period subjects/fish-bird/period-02
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Period 02 "Half Out of Water" delivered 3 images (supplementary round R11: R7's same-sentence wording was eaten by the waterline) | 小七 |
