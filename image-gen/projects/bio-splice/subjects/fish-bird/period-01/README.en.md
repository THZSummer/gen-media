# Period 01 · Leaping Out of the Water

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/fb-r6-review.en.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**starting at seed 6101 (see the provenance table for the multiple takes)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Just out of the water, spray still falling · backlight · eye level 100mm · landscape 1280×1024**

The first frame of the timeline: the fish has **just** burst out of the water and the spray is still falling. The landscape frame leaves room for the arc of the leap, and the backlight makes the spray and the wing edges light up at the same time.

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
| 1 | [`01-fish-wings.png`](01-fish-wings.png) | B1 (wing on the side of the body, **main image**) | **5.00** ✅ preferred | `0e9dd46a` | `a172b859b4` |
| 2 | [`02-fish-wings-spread.png`](02-fish-wings-spread.png) | B1 (fully spread from the back) | **5.00** ✅ preferred | `1ffb64a8` | `b4876ccbe6` |

Control: [`controls/fish.png`](controls/fish.png) —— the pure-fish base from the **same round** (same seed, same presentation, same sentence skeleton).

## 4. What this period verified

1. **Out of the water means it lands**: this is the first official period after the "out-of-water probe" (R4), and both takes succeeded.
2. The spray and the backlight are **bonus points**: they make the "just emerged" instant readable at a glance, and they also prop up the presence of the wings.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject fish-bird 6 --dry
python3 run_round.py --subject fish-bird 6
python3 score.py --round work/fish-bird/r6/round.json --scores work/fish-bird/r6/scores.json \
    --control base-fish --region body=300,400,650,350 \
    --audit-sheet subjects/fish-bird/rounds/fb-r6-audit.jpg \
    --subject fish-bird -o subjects/fish-bird/rounds/fb-r6-review.md
python3 curate.py --period subjects/fish-bird/period-01 --from work/fish-bird/r6/round.json \
    --pick fish-wings=01-fish-wings --pick fish-wings-spread=02-fish-wings-spread \
    --control base-fish=controls/fish --note "…" --force
bash make_sheet.sh period subjects/fish-bird/period-01
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Period 01 "Leaping Out of the Water" delivered 2 images | 小七 |
