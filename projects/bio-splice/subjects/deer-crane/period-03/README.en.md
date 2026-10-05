# Period 03 · The Deer with a Crane's Tail

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/dc-r7-review.en.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 7101 onward (multiple takes, see the provenance table)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Reed beds · backlight · eye level 600mm · square**

Backlight brings out the semi-translucent texture of the feathers — this period's protagonist is the **feather fan**, and only backlight lets you read at a glance that "this is a bird's plumage" rather than deer fur.

> The presentation layer is **constant within a period** (every shot in that period, controls included, shares one set) and **varies between periods** (each of the five periods has its own identity).

## 2. This period's subject and result

**Base = deer**　**Transplant = the crane's tail feathers G6 (**a true empty slot**: the deer's tail is too short to see)**

| Part | ID | Result |
|------|------|------|
| Tail feathers | G6 | ✅ **fully established**: a ring of white feather fan grows out of the rump, semi-translucent in the backlight |

But the **hit rate is only 1/4**: of the four seeds (7101/7102/7103/7104) only 7101 grew the feather fan; the other three had only the deer's own white patch on the rump. So this period has **only 1 final** — better to deliver one than to pad the count.

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-deer-cranetait.png`](01-deer-cranetait.png) | G6 (**main image**) | **5.00** ✅ preferred | `96e6fe31` | `fc634c0383` |

Control: [`controls/deer.png`](controls/deer.png) —— the pure-deer base from the **same round** (same seed, same presentation, same sentence skeleton).

## 4. What this period verified

1. **An empty slot is a necessary condition, not a sufficient one** (rule 90): the tail slot is the only "true empty slot" globally, and the hit rate is still only 1/4.
2. This is also the **only piece in this sub-theme that reads as a transplant at a glance** — because the feather fan and the deer body are **not the same form** (rule 91).

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject deer-crane 7 --dry
python3 run_round.py --subject deer-crane 7
python3 score.py --round work/deer-crane/r7/round.json --scores work/deer-crane/r7/scores.json \
    --control base-deer --region tail=520,300,350,350 \
    --audit-sheet subjects/deer-crane/rounds/dc-r7-audit.jpg \
    --subject deer-crane -o subjects/deer-crane/rounds/dc-r7-review.md
python3 curate.py --period subjects/deer-crane/period-03 --from work/deer-crane/r7/round.json \
    --pick deer-cranetait=01-deer-cranetait \
    --control base-deer=controls/deer --note "…" --force
bash make_sheet.sh period subjects/deer-crane/period-03
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 03 "The Deer with a Crane's Tail" delivered 1 image (fully established, hit rate 1/4) | 小七 |
