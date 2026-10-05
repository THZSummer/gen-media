# Period 01 · The Turtle with a Snake's Neck

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/ts-r3-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**all 4 images share seed 5101 (plus takes at 5102/5103)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Stream rocks and shallows · morning light · eye level 600mm · square**

Foundational period: first make the snake half stand on its own. The turtle climbs out of the water onto a stream rock, facing the camera, and the eye-level telephoto makes **the length of the neck** the main information in the frame — which is exactly what this period sets out to show.

> The presentation layer is **constant within a period**: every shot in this round (including the base control) shares the same habitat/light/camera/canvas,
> so the "transplant vs base" control is clean; **it varies between periods**, and each of the five periods has its own identity.

## 2. This period's subject and result

**Base = turtle** (deliberately leaving out the neck and the tail, to keep those two places free)　**Transplant = snake neck N1**

| Part | ID | Result |
|------|------|------|
| Snake neck | N1 | ✅ **fully established**: a long, curved neck extends from the shell opening, with fine scales running all the way to the lower jaw |

Three seeds (5101 / 5102 / 5103) were tried under the same presentation, and all three held — **N1 is the most stable part in this set**.

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-turtle-snakeneck.png`](01-turtle-snakeneck.png) | N1 snake neck (**main image**) | **5.00** ✅ preferred | `fcf005fd` | `113a634362` |
| 2 | [`02-turtle-snakeneck-b.png`](02-turtle-snakeneck-b.png) | N1 snake neck (seed 5102) | **5.00** ✅ preferred | `094cd85a` | `92fa46833` |
| 3 | [`03-turtle-snakeneck-c.png`](03-turtle-snakeneck-c.png) | N1 snake neck (seed 5103) | **5.00** ✅ preferred | `c5139ad3` | `f1e071af3c` |

Control: [`controls/turtle.png`](controls/turtle.png) —— the pure-turtle base from the **same round** (same seed, same presentation, same sentence skeleton),
and every objective metric in this round was measured against it.

## 4. What this period verified

1. **Freeing up a placeholder works completely on the "neck"**: the base says nothing about the neck's length, and `a long sinuous snake's neck` grew out by itself (rule 66).
2. All three seeds held, which shows this was not a lucky draw — **part-level transplant is reproducible on this kind of base**.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject turtle-snake 3 --dry
python3 run_round.py --subject turtle-snake 3
python3 score.py --round work/turtle-snake/r3/round.json --scores work/turtle-snake/r3/scores.json \
    --control base-turtle --region neck=380,120,300,320 \
    --audit-sheet subjects/turtle-snake/rounds/ts-r3-audit.jpg \
    --subject turtle-snake -o subjects/turtle-snake/rounds/ts-r3-review.md
python3 curate.py --period subjects/turtle-snake/period-01 --from work/turtle-snake/r3/round.json \
    --pick turtle-snakeneck=01-turtle-snakeneck \
    --pick turtle-snakeneck-b=02-turtle-snakeneck-b \
    --pick turtle-snakeneck-c=03-turtle-snakeneck-c \
    --control base-turtle=controls/turtle --note "…" --force
bash make_sheet.sh period subjects/turtle-snake/period-01
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Period 01 "The Turtle with a Snake's Neck" delivered 3 images (all three seeds held) | 小七 |
