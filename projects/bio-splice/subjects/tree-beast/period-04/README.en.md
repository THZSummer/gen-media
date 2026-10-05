# Period 4 · The dead tree's hide and horns

> 🌐 Language: **English** | [中文](README.md)

> Back to the [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [scoring review report](../rounds/tb-r9-review.en.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 12101 / 12102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Source: [`manifest.json`](manifest.json)

---

## 1. Features of this period (presentation)

**Frosty morning · flat light · square —— base change (old tree → standing dead tree)**

This is the only period that **changes the base**: the old tree is replaced by a **standing dead tree** (a split dead trunk + exposed roots),
without a single leaf —— so the layer of hide on the trunk and that pair of curved horns become the only "living" thing in the image.

## 2. Theme and results of this period

**Base ＝ standing dead tree**　**Donor ＝ hide pattern K1 + beast horns K4**

| Part | No. | Result |
|------|------|------|
| Hide pattern | K1 | ✅ works |
| Beast horns | K4 | ✅ fully works |

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-deadwood-hide-horns.png`](01-deadwood-hide-horns.png) | **5.00** ✅ first choice | `259c4335` | `835d75520e` |
| 2 | [`02-deadwood-hide-horns-b.png`](02-deadwood-hide-horns-b.png) | **5.00** ✅ first choice | `23348b95` | `d15c530971` |

Control: [`controls/tree.png`](controls/tree.png) —— the **same-round** pure standing dead tree (no hide, no horns).

## 4. Verification in this period

**The first base change that "did not drop but held"** (the source of Rule 106):
old tree → standing dead tree, and K1 + K4 **both still work**;
whereas flower-bird's magnolia → lily dropped the hit rate from 5/5 to 1/2.

> **Conjecture**: **property replacement (hide pattern) and empty-face addition (beast horns) depend little on the base's form**;
> landing sites that need geometric fit (the depth of the flower centre, the petal shape) are more sensitive.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject tree-beast 9 --dry
python3 run_round.py --subject tree-beast 9
python3 score.py --round work/tree-beast/r9/round.json --scores work/tree-beast/r9/scores.json \
    --control base-tree --region trunk=350,200,600,600 \
    --audit-sheet subjects/tree-beast/rounds/tb-r9-audit.jpg \
    --subject tree-beast -o subjects/tree-beast/rounds/tb-r9-review.md
python3 curate.py --period subjects/tree-beast/period-04 --from work/tree-beast/r9/round.json \
    --pick deadwood-hide-horns=01-deadwood-hide-horns \
    --pick deadwood-hide-horns-b=02-deadwood-hide-horns-b \
    --control base-tree=controls/tree --note "…" --force
bash make_sheet.sh period subjects/tree-beast/period-04
```

---

## Document revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 4 "The dead tree's hide and horns" delivered 2 images (base-change verification) | 小七 |
