# Period 05 · Kunpeng (finale)

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/fb-r10-review.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**starting at seed 6101 (see the provenance table for the multiple takes)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Dusk sea surface · backlit silhouette · wide angle · landscape 1280×1024**

The finale period pushes the timeline to its **highest point**: leaping up above a dusk sea surface, both wings fully spread, the backlight flattening the whole animal into a silhouette — exactly the "it transformed into a bird" line from *Xiaoyaoyou*.

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
| 1 | [`01-kunpeng.png`](01-kunpeng.png) | B1 (fully spread, **main image**) | **5.00** ✅ preferred | `c7d00a36` | `40b6299913` |
| 2 | [`02-kunpeng-spread.png`](02-kunpeng-spread.png) | B1 (fully spread, seed 6102) | **5.00** ✅ preferred | `cf50a24b` | `d42af2cf04` |

Control: [`controls/fish.png`](controls/fish.png) —— the pure-fish base from the **same round** (same seed, same presentation, same sentence skeleton).

## 4. What this period verified

1. **The silhouette reads the contradiction of "fish body + bird wings" as a single creature**: the body outline is determined entirely by the combination of the wings and the fish body.
2. The finale uses presentation (dusk + backlight + wide angle) to gather the mechanism findings of the previous three periods into a single figure at once.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject fish-bird 10 --dry
python3 run_round.py --subject fish-bird 10
python3 score.py --round work/fish-bird/r10/round.json --scores work/fish-bird/r10/scores.json \
    --control base-fish --region body=300,400,650,350 \
    --audit-sheet subjects/fish-bird/rounds/fb-r10-audit.jpg \
    --subject fish-bird -o subjects/fish-bird/rounds/fb-r10-review.md
python3 curate.py --period subjects/fish-bird/period-05 --from work/fish-bird/r10/round.json \
    --pick fish-wings-spread=01-kunpeng --pick fish-wings-spread-b=02-kunpeng-spread \
    --control base-fish=controls/fish --note "…" --force
bash make_sheet.sh period subjects/fish-bird/period-05
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Period 05 "Kunpeng" delivered 2 images (finale) | 小七 |
