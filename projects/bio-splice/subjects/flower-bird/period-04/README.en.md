# Period 4 · The lily's down and plume

> 🌐 Language: **English** | [中文](README.md)

> Back to the [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [scoring review report](../rounds/fb2-r9-review.en.md)
> Engine: Z-Image-Turbo　**1024×1280**　steps 12　**seed 11101 / 11103 / 11104**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Source: [`manifest.json`](manifest.json)

---

## 1. Features of this period (presentation)

**Backlight · vertical 1024×1280 · flower species changed (magnolia → lily)**

The only period that changes the **flower species**: the lily's six recurved petals are completely different in form from the magnolia's round petals,
and under backlight the petals and feather filaments are translucent together —— **change the base and the same sentence yields a new image**.

## 2. Theme and results of this period

**Base ＝ white lily (stamens and pistil vacated)**　**Donor ＝ down feather P5 + plume feather P6**

| Part | Landing site | Result |
|------|------|------|
| Plume feather | flower axis | ✅ fully works |
| Down feather | flower centre | ✅ works |

⚠️ **The hit rate drops with the flower species** (Rule 102): in the first round (R7) only one of two images worked,
and three extra seeds (R9) were needed to make up three. **The same wording is 5/5 on the magnolia.**

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-lily-down-plume.png`](01-lily-down-plume.png) | **5.00** ✅ first choice | `c66c6561` | `e83c12ed76` |
| 2 | [`02-lily-down-plume-c.png`](02-lily-down-plume-c.png) | **5.00** ✅ first choice | `2d72e3bb` | `81ccfe2d64` |
| 3 | [`03-lily-down-plume-d.png`](03-lily-down-plume-d.png) | **5.00** ✅ first choice | `9800df0a` | `5d171f38ff` |

Control: [`controls/flower.png`](controls/flower.png) —— the **same-round** pure-lily base.

## 4. Verification in this period

**Rule 102: a new base must have its hit rate re-verified.** "The wording was verified on A" does not equal "it is also stable on B" ——
so for every base change, the first round should be treated as a probe (add takes only after it hits).

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject flower-bird 9 --dry
python3 run_round.py --subject flower-bird 9
python3 score.py --round work/flower-bird/r9/round.json --scores work/flower-bird/r9/scores.json \
    --control base-flower --region axis=300,250,450,700 \
    --audit-sheet subjects/flower-bird/rounds/fb2-r9-audit.jpg \
    --subject flower-bird -o subjects/flower-bird/rounds/fb2-r9-review.md
python3 curate.py --period subjects/flower-bird/period-04 --from work/flower-bird/r9/round.json \
    --pick lily-down-plume=01-lily-down-plume --pick lily-down-plume-c=02-lily-down-plume-c \
    --pick lily-down-plume-d=03-lily-down-plume-d \
    --control base-flower=controls/flower --note "…" --force
bash make_sheet.sh period subjects/flower-bird/period-04
```

---

## Document revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 4 "The lily's down and plume" delivered 3 images (flower species changed, extra takes after the hit rate dropped) | 小七 |
