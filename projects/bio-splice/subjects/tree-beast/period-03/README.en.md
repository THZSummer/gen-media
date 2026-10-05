# Period 3 · Hide and horns complete

> 🌐 Language: **English** | [中文](README.md)

> Back to the [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [scoring review report](../rounds/tb-r8-review.en.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**seed 12101 / 12102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Source: [`manifest.json`](manifest.json)

---

## 1. Features of this period (presentation)

**Forest after rain · hard light · landscape 1280×1024**

The hard light after rain brings out the difference in sheen between wet bark and hide; the landscape format fits "trunk + horns + roots" completely into the image.

## 2. Theme and results of this period

**Base ＝ old tree (bark vacated)**　**Donor ＝ hide pattern K1 + beast horns K4**

| Part | No. | Landing site | Result |
|------|------|------|------|
| Hide pattern | K1 | bark (property) | ✅ works |
| Beast horns | K4 | trunk (empty face) | ✅ fully works |
| Two parts in one body | K1+K4 | material + surface | ✅ they do not compete (one is a material replacement, the other a newly added structure) |

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-tree-hide-horns.png`](01-tree-hide-horns.png) | **5.00** ✅ first choice | `8f9cce53` | `b759f03394` |
| 2 | [`02-tree-hide-horns-b.png`](02-tree-hide-horns-b.png) | **5.00** ✅ first choice | `5c2dcfda` | `3e21a80c7c` |

Control: [`controls/tree.png`](controls/tree.png) —— the **same-round** pure-tree base.

## 4. Verification in this period

1. **"Material replacement" and "newly added structure" do not conflict**: one changes the surface's material (a property),
   the other adds a structure above the surface (an empty face) —— so both can work at the same time.
2. The period's identity is distinguished from the previous two by light and canvas (hard light after rain + landscape).

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject tree-beast 8 --dry
python3 run_round.py --subject tree-beast 8
python3 score.py --round work/tree-beast/r8/round.json --scores work/tree-beast/r8/scores.json \
    --control base-tree --region trunk=300,150,680,600 \
    --audit-sheet subjects/tree-beast/rounds/tb-r8-audit.jpg \
    --subject tree-beast -o subjects/tree-beast/rounds/tb-r8-review.md
python3 curate.py --period subjects/tree-beast/period-03 --from work/tree-beast/r8/round.json \
    --pick tree-hide-horns=01-tree-hide-horns --pick tree-hide-horns-b=02-tree-hide-horns-b \
    --control base-tree=controls/tree --note "…" --force
bash make_sheet.sh period subjects/tree-beast/period-03
```

---

## Document revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 3 "Hide and horns complete" delivered 2 images (all first choice) | 小七 |
