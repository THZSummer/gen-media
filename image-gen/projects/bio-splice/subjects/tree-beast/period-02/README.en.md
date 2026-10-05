# Period 2 · The tree with horns

> 🌐 Language: **English** | [中文](README.md)

> Back to the [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [scoring review report](../rounds/tb-r4-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 12101 / 12102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Source: [`manifest.json`](manifest.json)

---

## 1. Features of this period (presentation)

**Frosty forest · side backlight · square**

The side backlight hangs frost on the branches and also traces the outline of the horns;
the subject of this period is **that pair of curved horns lifting from the trunk**, so the camera sits at the middle of the trunk and lets the horns occupy the upper part of the image.

## 2. Theme and results of this period

**Base ＝ old tree**　**Donor ＝ beast horns K4**

| Part | No. | Landing site | Result |
|------|------|------|------|
| Beast horns | K4 | trunk (**empty face**) | ✅ **fully works**: a pair of huge curved horns grows out of the trunk |

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-tree-horns.png`](01-tree-horns.png) | **5.00** ✅ first choice | `b331b81c` | `e362d26313` |
| 2 | [`02-tree-horns-b.png`](02-tree-horns-b.png) | **5.00** ✅ first choice | `643fe056` | `0f4d829360` |

Control: [`controls/tree.png`](controls/tree.png) —— the **same-round** pure-tree base (no horns).

## 4. Verification in this period

1. **Empty face + different form + high recognizability**: the trunk is an empty face (Rule 97) and the horns are completely different in form from the tree shape (Rule 91) ——
   all three favourable conditions are present, and two rounds ×2 takes all worked.
2. It forms the most direct contrast with the **beast feet (0%)** of the same round: same base, same presentation, **the only difference is the landing site** (Rule 105).

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject tree-beast 4 --dry
python3 run_round.py --subject tree-beast 4
python3 score.py --round work/tree-beast/r4/round.json --scores work/tree-beast/r4/scores.json \
    --control base-tree --region horn=350,100,400,400 \
    --audit-sheet subjects/tree-beast/rounds/tb-r4-audit.jpg \
    --subject tree-beast -o subjects/tree-beast/rounds/tb-r4-review.md
python3 curate.py --period subjects/tree-beast/period-02 --from work/tree-beast/r4/round.json \
    --pick tree-horns=01-tree-horns --pick tree-horns-b=02-tree-horns-b \
    --control base-tree=controls/tree --note "…" --force
bash make_sheet.sh period subjects/tree-beast/period-02
```

---

## Document revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 2 "The tree with horns" delivered 2 images (all first choice) | 小七 |
