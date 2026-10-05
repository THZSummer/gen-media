# Period 05 · Carnivorous Plant (finale)

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/ff-r7-review.en.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**seed 10101 / 10102**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Features (Presentation)

**Misty swamp at dawn · backlight · wide-angle 45mm · landscape 1280×1024**

The finale does not shoot a single plant but **a whole clump**: the mist at dawn + backlight make every red inner face light up,
and the wide-angle landscape frame conveys the presence of "a patch of carnivorous plants".

## 2. This Period's Theme and Results

**Base ＝ Venus flytrap (wide leaf-blade version)**　**Transplant ＝ mammal fangs T1 + eye T2 + tongue T4**

| Part | ID | Landing site | Result |
|------|------|------|------|
| Mammal fangs | T1 | trap edge | ✅ |
| Eye | T2 | leaf blade | ✅ (smaller in this image, less striking than in period 02) |
| Tongue | T4 | trap cavity | ✅ |
| Three parts on the same body | all | three different faces | ✅ reads as a clump of **plants with eyes and an open mouth** |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-flytrap-all3.png`](01-flytrap-all3.png) | T1+T2+T4 (**main image**) | **5.00** ✅ preferred final | `517319cd` | `d1dbf9cbc7` |
| 2 | [`02-flytrap-all3-b.png`](02-flytrap-all3-b.png) | T1+T2+T4 (seed 10101) | **4.55** ✅ preferred final | `e796d791` | `0af2711e81` |

Control: [`controls/flytrap.png`](controls/flytrap.png) —— the pure Venus flytrap clump from the **same round**.

## 4. This Period's Verification

1. **The three parts fall on three different faces** (edge / leaf blade / cavity), so stacking them did not squeeze one another out ——
   once again verifying that "the independent variable of the constraint is the distribution of regions (faces), not the number of parts" (Rules 59/68/99).
2. In the second image (the `-b` one) the eye is rather small on the leaf blade and slightly less readable, so 4.55 is given as it is.

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject flytrap-fang 7 --dry
python3 run_round.py --subject flytrap-fang 7
python3 score.py --round work/flytrap-fang/r7/round.json --scores work/flytrap-fang/r7/scores.json \
    --control base-flytrap --region lobe=300,150,680,600 \
    --audit-sheet subjects/flytrap-fang/rounds/ff-r7-audit.jpg \
    --subject flytrap-fang -o subjects/flytrap-fang/rounds/ff-r7-review.md
python3 curate.py --period subjects/flytrap-fang/period-05 --from work/flytrap-fang/r7/round.json \
    --pick flytrap-all3-b=01-flytrap-all3 --pick flytrap-all3=02-flytrap-all3-b \
    --control base-flytrap=controls/flytrap --note "…" --force
bash make_sheet.sh period subjects/flytrap-fang/period-05
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|--------|------|
| 2026-10-05 | v0.1 | Period 05 [Carnivorous Plant] delivered 2 images (finale) | 小七 |
