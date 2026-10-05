# Period 03 · Fully Out of Water · Both Wings Fully Spread

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/fb-r8-review.en.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**starting at seed 6101 (see the provenance table for the multiple takes)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Fully in the air · high-side view · backlit feather outlines · square**

The third frame of the timeline: the fish is **completely clear of the water**, both wings fully spread. The high-side view accounts for the wing surface and the fish body at the same time, and the backlight traces out every feather — this period is the most "in flight" image in the whole sub-theme.

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
| 1 | [`01-fish-wings-spread.png`](01-fish-wings-spread.png) | B1 (fully spread, **main image**) | **5.00** ✅ preferred | `cda5a7ac` | `8e65b9366c` |
| 2 | [`02-fish-wings-spread-b.png`](02-fish-wings-spread-b.png) | B1 (fully spread, seed 6102) | **5.00** ✅ preferred | `4044a13f` | `6265b5be0f` |

Control: [`controls/fish.png`](controls/fish.png) —— the pure-fish base from the **same round** (same seed, same presentation, same sentence skeleton).

## 4. What this period verified

1. **Being fully out of the water is the maximum state of compatibility**: only here does the wings' fullest spread read completely.
2. Seen together with periods 01/02, the three periods are exactly the three frames of "progressively leaving the water": spray still falling → waterline crossing → fully in the air.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject fish-bird 8 --dry
python3 run_round.py --subject fish-bird 8
python3 score.py --round work/fish-bird/r8/round.json --scores work/fish-bird/r8/scores.json \
    --control base-fish --region body=250,300,520,380 \
    --audit-sheet subjects/fish-bird/rounds/fb-r8-audit.jpg \
    --subject fish-bird -o subjects/fish-bird/rounds/fb-r8-review.md
python3 curate.py --period subjects/fish-bird/period-03 --from work/fish-bird/r8/round.json \
    --pick fish-wings-spread=01-fish-wings-spread --pick fish-wings-spread-b=02-fish-wings-spread-b \
    --control base-fish=controls/fish --note "…" --force
bash make_sheet.sh period subjects/fish-bird/period-03
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Period 03 "Fully Out of Water · Both Wings Fully Spread" delivered 2 images | 小七 |
