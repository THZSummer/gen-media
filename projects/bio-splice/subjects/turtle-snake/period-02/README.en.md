# Period 02 · The Turtle with a Snake's Tail

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/ts-r4-review.en.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**all 4 images share seed 5101 (plus takes at 5102/5103)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Wetland mud bank · overcast · eye-level full body 400mm · square**

A tail only reads as a snake's tail if it **lies flat on the ground**, so this period uses a wetland mud bank + eye-level full body: the mud surface gives the tail somewhere to spread out, and the flat overcast light preserves the detail of the scale rows.

> ⚠️ The PLAN originally called for "low camera hugging the ground · vertical", **changed to eye-level full body per rule 80**: on cat-eagle, a low vertical shot turned the "tail sentence" into a second complete animal.

> The presentation layer is **constant within a period**: every shot in this round (including the base control) shares the same habitat/light/camera/canvas,
> so the "transplant vs base" control is clean; **it varies between periods**, and each of the five periods has its own identity.

## 2. This period's subject and result

**Base = turtle**　**Transplant = snake tail N2**

| Part | ID | Result |
|------|------|------|
| Snake tail | N2 | ✅ **fully established**: a long, tapering tail extends from behind the shell, with segmented rows of scales |

Control R1 (on stream rocks, tail raised) → this period's eye-level mud-bank version is **clearly more natural**: the tail lies flat on the mud surface and the scales are visible segment by segment.

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-turtle-snaketail.png`](01-turtle-snaketail.png) | N2 snake tail (**main image**) | **5.00** ✅ preferred | `ef036bd4` | `7c251a9c88` |
| 2 | [`02-turtle-snaketail-b.png`](02-turtle-snaketail-b.png) | N2 snake tail (seed 5102) | **4.85** ✅ preferred | `efb648cc` | `c8710666ee` |
| 3 | [`03-turtle-snaketail.png`](03-turtle-snaketail.png) | N2 snake tail (seed 5101) | **4.55** ✅ preferred | `fbfbb314` | `e7687746b4` |

Control: [`controls/turtle.png`](controls/turtle.png) —— the pure-turtle base from the **same round** (same seed, same presentation, same sentence skeleton),
and every objective metric in this round was measured against it.

## 4. What this period verified

1. **The same part reads very differently under different presentations**: in R1 the stream-rock version had the tail raised in the air and looked unnatural (4.35); this period's eye-level mud-bank version shows the scale rows segment by segment (5.00).
2. The eye-level camera **also avoids the pitfall of rule 80**: a low vertical shot makes an extremity get drawn as a separate individual, and this period has no extra individuals at all.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject turtle-snake 4 --dry
python3 run_round.py --subject turtle-snake 4
python3 score.py --round work/turtle-snake/r4/round.json --scores work/turtle-snake/r4/scores.json \
    --control base-turtle --region neck=300,200,300,250 --region tail=250,420,450,300 \
    --audit-sheet subjects/turtle-snake/rounds/ts-r4-audit.jpg \
    --subject turtle-snake -o subjects/turtle-snake/rounds/ts-r4-review.md
python3 curate.py --period subjects/turtle-snake/period-02 --from work/turtle-snake/r4/round.json \
    --pick turtle-snaketail-c=01-turtle-snaketail \
    --pick turtle-snaketail-b=02-turtle-snaketail-b \
    --pick turtle-snaketail=03-turtle-snaketail \
    --control base-turtle=controls/turtle --note "…" --force
bash make_sheet.sh period subjects/turtle-snake/period-02
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Period 02 "The Turtle with a Snake's Tail" delivered 3 images; presentation changed from low vertical to eye-level full body per rule 80 | 小七 |
