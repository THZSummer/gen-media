# Period 04 · Fangs and Tongue Complete

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/ff-r6-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 10101 / 10102**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Features (Presentation)

**After rain · hard side light · square**

Two parts on the same body need **hard light to separate the structures**: after the rain, water droplets hang on the trap,
and the hard side light keeps the edges of the fangs, the droplets and the tongue from smearing into one another.

## 2. This Period's Theme and Results

**Base ＝ Venus flytrap (marginal teeth not described)**　**Transplant ＝ mammal fangs T1 + tongue T4**

| Part | ID | Landing site | Result |
|------|------|------|------|
| Mammal fangs | T1 | trap edge | ✅ fully holds |
| Tongue | T4 | trap cavity | ✅ fully holds |
| Two parts on the same body | T1+T4 | edge and cavity | ✅ **no mutual contention**: one on the rim, one in the cavity |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-flytrap-fangs-tongue.png`](01-flytrap-fangs-tongue.png) | T1+T4 (**main image**) | **5.00** ✅ preferred final | `390ef57e` | `6e2c4d49ae` |
| 2 | [`02-flytrap-fangs-tongue-b.png`](02-flytrap-fangs-tongue-b.png) | T1+T4 (seed 10102) | **5.00** ✅ preferred final | `269a7ef9` | `b0c7d745a9` |

Control: [`controls/flytrap.png`](controls/flytrap.png) —— the pure Venus flytrap from the **same round**.

## 4. This Period's Verification

1. **"≤2 in the same region" is not a constraint here** (the applicable boundary of Rule 59):
   the fangs are on the **edge** and the tongue is in the **cavity**, two different faces, so they do not compete.
2. With fangs and tongue present, the whole plant reads as **a single beast's maw** —— which is the whole point of this sub-theme (what is crossed is not the species but the kingdom).

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject flytrap-fang 6 --dry
python3 run_round.py --subject flytrap-fang 6
python3 score.py --round work/flytrap-fang/r6/round.json --scores work/flytrap-fang/r6/scores.json \
    --control base-flytrap --region lobe=250,150,550,500 \
    --audit-sheet subjects/flytrap-fang/rounds/ff-r6-audit.jpg \
    --subject flytrap-fang -o subjects/flytrap-fang/rounds/ff-r6-review.md
python3 curate.py --period subjects/flytrap-fang/period-04 --from work/flytrap-fang/r6/round.json \
    --pick flytrap-fangs-tongue=01-flytrap-fangs-tongue \
    --pick flytrap-fangs-tongue-b=02-flytrap-fangs-tongue-b \
    --control base-flytrap=controls/flytrap --note "…" --force
bash make_sheet.sh period subjects/flytrap-fang/period-04
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-05 | v0.1 | Period 04 [Fangs and Tongue Complete] delivered 2 images (all preferred finals) | 小七 |
