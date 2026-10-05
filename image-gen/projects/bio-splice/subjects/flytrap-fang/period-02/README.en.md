# Period 02 · The Flytrap with an Eye

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/ff-r4-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 10101 / 10102**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Features (Presentation)

**Swamp · eye level on the leaf blade · square**

The subject of this period is **that eye on the leaf blade**, so the camera changes to eye level **facing the leaf blade**,
using flat light (overcast) to keep the leaf's reflections from eating the eye's highlights.

## 2. This Period's Theme and Results

**Base ＝ Venus flytrap (wide leaf-blade version)**　**Transplant ＝ eye T2**

| Part | ID | Landing site | Result |
|------|------|------|------|
| Eye | T2 | leaf blade (a plant never had a position called an "eye") | ✅ holds: a glossy dark animal eye grows on the green leaf, with a clear iris highlight |

⚠️ **Anatomy deduction (C=4)**: this eye **has no eyelids and no eye socket**, and zoomed in it feels "pasted on".
According to Rule 101's hypothesis, adding a "socket / eyelid / seam" description might save it —— **not yet verified**.

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-flytrap-eye.png`](01-flytrap-eye.png) | T2 (**main image**) | **4.80** ✅ preferred final | `748c5634` | `ec17d89aef` |
| 2 | [`02-flytrap-eye-b.png`](02-flytrap-eye-b.png) | T2 (seed 10102) | **4.80** ✅ preferred final | `f7e08ea7` | `b35f881c02` |

Control: [`controls/flytrap.png`](controls/flytrap.png) —— the pure Venus flytrap from the **same round** (nothing at all on the leaf blade).

## 4. This Period's Verification

1. **An "eye" on a plant is a genuine new addition in an empty slot**: the leaf blade is a continuous free face with no canonical structure occupying it (Rule 99).
2. This is **the only item in this sub-theme that did not get full marks**: a single cross-kingdom part lacks an anatomical seam; recorded as it is, without embellishment.

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject flytrap-fang 4 --dry
python3 run_round.py --subject flytrap-fang 4
python3 score.py --round work/flytrap-fang/r4/round.json --scores work/flytrap-fang/r4/scores.json \
    --control base-flytrap --region lobe=250,150,550,500 \
    --audit-sheet subjects/flytrap-fang/rounds/ff-r4-audit.jpg \
    --subject flytrap-fang -o subjects/flytrap-fang/rounds/ff-r4-review.md
python3 curate.py --period subjects/flytrap-fang/period-02 --from work/flytrap-fang/r4/round.json \
    --pick flytrap-eye=01-flytrap-eye --pick flytrap-eye-b=02-flytrap-eye-b \
    --control base-flytrap=controls/flytrap --note "…" --force
bash make_sheet.sh period subjects/flytrap-fang/period-02
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-05 | v0.1 | Period 02 [The Flytrap with an Eye] delivered 2 images (4.80, anatomy honestly deducted) | 小七 |
