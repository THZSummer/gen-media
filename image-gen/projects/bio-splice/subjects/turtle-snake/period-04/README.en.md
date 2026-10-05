# Period 04 · Neck and Tail Together

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/ts-r5-review.en.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**all 3 images share seed 5101 (plus takes at 5102/5103)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Stream rocks after rain · backlight · eye level 400mm · landscape 1280×1024**

With each part verified one by one, this period puts **the neck and the tail on at the same time**, and uses a landscape frame to bring both ends into a single image; the backlight traces the two serpentine outlines against the sky light, which is exactly the test of whether they **interfere with each other**.

> The presentation layer is **constant within a period**: every shot in this round (including the base control) shares the same habitat/light/camera/canvas,
> so the "transplant vs base" control is clean; **it varies between periods**, and each of the five periods has its own identity.

## 2. This period's subject and result

**Base = turtle**　**Transplant = snake neck N1 + snake tail N2**

| Part | ID | Result |
|------|------|------|
| Snake neck | N1 | ✅ fully established |
| Snake tail | N2 | ✅ fully established |
| Both parts on one body | N1+N2 | ✅ **neither squeezed the other out**, and no second individual appeared |

The neck is at the head end and the tail behind the shell, belonging to two separate regions — exactly the case in which rule 59 (≤2 within a region, stackable across regions) is expected to hold.

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-turtle-neck-tail.png`](01-turtle-neck-tail.png) | N1+N2 (**main image**) | **5.00** ✅ preferred | `6656eff3` | `adb819cfb0` |
| 2 | [`02-turtle-neck-tail-b.png`](02-turtle-neck-tail-b.png) | N1+N2 (seed 5102) | **5.00** ✅ preferred | `1f3237a5` | `717c3ce298` |

Control: [`controls/turtle.png`](controls/turtle.png) —— the pure-turtle base from the **same round** (same seed, same presentation, same sentence skeleton),
and every objective metric in this round was measured against it.

## 4. What this period verified

1. **Cross-region stacking holds under both seeds**: a part verified on its own stays stable when stacked, as long as the regions do not conflict (rule 69).
2. The backlight did not eat the scale rows — **solid parts withstand backlight** (unlike thin-line parts; see cat-eagle's whisker period).

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject turtle-snake 5 --dry
python3 run_round.py --subject turtle-snake 5
python3 score.py --round work/turtle-snake/r5/round.json --scores work/turtle-snake/r5/scores.json \
    --control base-turtle --region neck=380,150,340,300 --region tail=620,350,420,300 \
    --audit-sheet subjects/turtle-snake/rounds/ts-r5-audit.jpg \
    --subject turtle-snake -o subjects/turtle-snake/rounds/ts-r5-review.md
python3 curate.py --period subjects/turtle-snake/period-04 --from work/turtle-snake/r5/round.json \
    --pick turtle-neck-tail=01-turtle-neck-tail \
    --pick turtle-neck-tail-b=02-turtle-neck-tail-b \
    --control base-turtle=controls/turtle --note "…" --force
bash make_sheet.sh period subjects/turtle-snake/period-04
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Period 04 "Neck and Tail Together" delivered 2 images | 小七 |
