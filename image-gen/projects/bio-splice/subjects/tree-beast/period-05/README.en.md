# Period 5 · Tree-beast (finale)

> 🌐 Language: **English** | [中文](README.md)

> Back to the [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [scoring review report](../rounds/tb-r6-review.en.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**seed 12101 / 12102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Source: [`manifest.json`](manifest.json)

---

## 1. Features of this period (presentation)

**Dusk forest · backlit silhouette · wide-angle 24mm · landscape 1280×1024**

The finale puts the whole tree into the backlight of dusk: the trunk is covered in hide, curved horns lift from the top ——
**the "tree-beast" image is most complete in silhouette** (raking light exposes the seams in the material; a silhouette does not).

## 2. Theme and results of this period

**Base ＝ old tree (bark vacated)**　**Donor ＝ hide pattern K1 + beast feet K2 + beast horns K4**

| Part | No. | Result |
|------|------|------|
| Hide pattern | K1 | ✅ works |
| Beast horns | K4 | ✅ fully works |
| **Beast feet** | **K2** | ❌ **did not land** (root-system region zoomed ×1.6 and read one by one: the roots are still roots) |

⚠️ **two of three parts work**, so the finals are collected at A=4 —— **stated honestly, without glossing over it**.

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-tree-beast.png`](01-tree-beast.png) | **4.55** ✅ first choice | `d3280536` | `83d2a25ebd` |
| 2 | [`02-tree-beast-b.png`](02-tree-beast-b.png) | **4.55** ✅ first choice | `d3875556` | `0ec6e3e829` |

Control: [`controls/tree.png`](controls/tree.png) —— the **same-round** pure-tree base.

## 4. Verification in this period: why the beast feet cannot land (negative conclusion)

Two reasons hold at the same time:

1. **The landing site is a canonical structure**: the root system is a tree organ (Rule 99);
2. **A "foot" needs a joint/limb as a bearing surface** —— a tree has no legs (Rules 74/97).

→ **Exactly the same shape** as dragon-nines' "eagle claws require a four-limbed base first".
This is the first sub-theme in the repo where, in Group B, "a certain part simply cannot be done",
and the lesson is written into **Rule 105**: **when choosing a part, ask both "is the landing site a canonical structure" and "what bearing surface does this part need".**

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject tree-beast 6 --dry
python3 run_round.py --subject tree-beast 6
python3 score.py --round work/tree-beast/r6/round.json --scores work/tree-beast/r6/scores.json \
    --control base-tree --region trunk=300,150,680,600 \
    --audit-sheet subjects/tree-beast/rounds/tb-r6-audit.jpg \
    --subject tree-beast -o subjects/tree-beast/rounds/tb-r6-review.md
python3 curate.py --period subjects/tree-beast/period-05 --from work/tree-beast/r6/round.json \
    --pick tree-beast=01-tree-beast --pick tree-beast-b=02-tree-beast-b \
    --control base-tree=controls/tree --note "…" --force
bash make_sheet.sh period subjects/tree-beast/period-05
```

---

## Document revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 5 "Tree-beast" delivered 2 images (finale; the beast feet' failure to land is noted) | 小七 |
