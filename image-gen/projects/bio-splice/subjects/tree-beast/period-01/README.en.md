# Period 1 · The tree with hide

> 🌐 Language: **English** | [中文](README.md)

> Back to the [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [part table](../parts.en.md) ｜ [scoring review report](../rounds/tb-r7-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 12101 / 12102 / 12103**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Source: [`manifest.json`](manifest.json)

---

## 1. Features of this period (presentation)

**Misty forest · soft light · eye level · square**

The mist flattens the woodland into a sheet of grey-green, and the trunk becomes the only "solid" in the image ——
**the subject of this period is the material on the trunk's surface**, hence soft light (hard light would throw a mass of interfering shadows across the bark grain).

## 2. Theme and results of this period

**Base ＝ old tree (vacated version: do not describe the bark)**　**Donor ＝ hide pattern K1**

| Part | No. | Landing site | Result |
|------|------|------|------|
| Hide pattern | K1 | bark (**property**) | ✅ works: an obvious hide / fur band appears on the trunk |

⚠️ Using the **vacated version** of the base is deliberate (Rules 96/100): the occupied version (describing `rough fissured bark` as usual) only reaches 4.25,
and after vacating the bark description, the material difference between the hide and the surrounding bark is visible at a glance (4.55).

## 3. Finals

| # | File | Score | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-tree-hide.png`](01-tree-hide.png) | **4.55** ✅ first choice | `9c4de578` | `a2f7354faf` |
| 2 | [`02-tree-hide-b.png`](02-tree-hide-b.png) | **4.55** ✅ first choice | `12886056` | `0a99c15554` |
| 3 | [`03-tree-hide-c.png`](03-tree-hide-c.png) | **4.55** ✅ first choice | `a2214d66` | `1e60fb1b8f` |

Control: [`controls/tree.png`](controls/tree.png) —— the **same-round** pure-tree base (vacated version).

## 4. Verification in this period

1. **Grain is a property and can be vacated**: bark grain can be deleted, so the vacated version works ——
   the same shape as the insect body surface in cordyceps and the marginal teeth in flytrap (Rules 96/100).
2. Material replacement only reaches "partially works" (A=4): a seam is still visible at the boundary between hide and bark, and the score says so honestly.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject tree-beast 7 --dry
python3 run_round.py --subject tree-beast 7
python3 score.py --round work/tree-beast/r7/round.json --scores work/tree-beast/r7/scores.json \
    --control base-tree --region bark=250,200,550,500 \
    --audit-sheet subjects/tree-beast/rounds/tb-r7-audit.jpg \
    --subject tree-beast -o subjects/tree-beast/rounds/tb-r7-review.md
python3 curate.py --period subjects/tree-beast/period-01 --from work/tree-beast/r7/round.json \
    --pick tree-hide=01-tree-hide --pick tree-hide-b=02-tree-hide-b --pick tree-hide-c=03-tree-hide-c \
    --control base-tree=controls/tree --note "…" --force
bash make_sheet.sh period subjects/tree-beast/period-01
```

---

## Document revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 1 "The tree with hide" delivered 3 images (vacated-version base) | 小七 |
