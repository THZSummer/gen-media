# Period 04 · Skimming Low Over the Water

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/fb-r9-review.en.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**starting at seed 6101 (see the provenance table for the multiple takes)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Flying low, close to the water · telephoto compression · flat light on grey water · landscape 1280×1024**

The fourth frame of the timeline: **it is airborne, but has not flown far** — the body almost horizontal, skimming just above the water. The telephoto compresses the distant shore into a band, which gives the subject a sense of speed.

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
| 1 | [`01-fish-wings.png`](01-fish-wings.png) | B1 (side of the body, **main image**) | **5.00** ✅ preferred | `5c6bf7aa` | `13f7206fab` |
| 2 | [`02-fish-wings-spread.png`](02-fish-wings-spread.png) | B1 (fully spread) | **5.00** ✅ preferred | `631a3c53` | `185ef692d5` |

Control: [`controls/fish.png`](controls/fish.png) —— the pure-fish base from the **same round** (same seed, same presentation, same sentence skeleton).

## 4. What this period verified

1. **Flat light + grey water** is what sets this period apart from periods 01/03: with no backlight, the wing's form is read from its outline rather than from a lit edge.
2. This frame also shows that "out of water" does not have to mean high above it — **as long as the body is above the water surface, the wings are stable**.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject fish-bird 9 --dry
python3 run_round.py --subject fish-bird 9
python3 score.py --round work/fish-bird/r9/round.json --scores work/fish-bird/r9/scores.json \
    --control base-fish --region body=300,400,650,350 \
    --audit-sheet subjects/fish-bird/rounds/fb-r9-audit.jpg \
    --subject fish-bird -o subjects/fish-bird/rounds/fb-r9-review.md
python3 curate.py --period subjects/fish-bird/period-04 --from work/fish-bird/r9/round.json \
    --pick fish-wings=01-fish-wings --pick fish-wings-spread=02-fish-wings-spread \
    --control base-fish=controls/fish --note "…" --force
bash make_sheet.sh period subjects/fish-bird/period-04
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Period 04 "Skimming Low Over the Water" delivered 2 images | 小七 |
