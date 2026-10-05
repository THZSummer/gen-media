# Period 05 · The Symbiont (finale)

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/lc-r5-review.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**seed 8101 / 8102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Misty forest · scattered light · wide angle · landscape 1280×1024**

The finale returns to the origin: **a single lichen can naturally carry both foliose and fruticose structures at once**.
The scattered light of the misty forest has no hard shadows, and lays out the layers of this "composite" clearly in one go.

## 2. This period's subject and result

**Base = fungal mycelium**　**Transplant = three forms (crustose / foliose / fruticose) ± green algal cells**

| Part | ID | Result |
|------|------|------|
| Three forms | CR1+FL1+FR1 | ✅ foliose lobes + fruticose branching grow on the same individual |
| Forms + algae | FL1+FR1+AL1 | ✅ beyond the composite form, green algal cells are embedded in the crevices |

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-mycelium-3forms.png`](01-mycelium-3forms.png) | Three forms (**main image**) | **5.00** ✅ preferred | `125acdd7` | `694e593ffe` |
| 2 | [`02-mycelium-forms-algae.png`](02-mycelium-forms-algae.png) | Forms + algae | **4.55** ✅ preferred | `65a78031` | `d036280d0b` |

Control: [`controls/mycelium.png`](controls/mycelium.png) —— the pure-mycelium base from the **same round**.

## 4. What this period verified

1. **Stacking three forms on one individual did not crowd any of them out** — for this kind of base "with no fixed shape",
   rule 59 (≤2 per region) does not apply either: it never had "regions" to divide in the first place.
2. The finale image feels like "one real composite lichen" rather than "three lichens stuck together".

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject lichen 5 --dry
python3 run_round.py --subject lichen 5
python3 score.py --round work/lichen/r5/round.json --scores work/lichen/r5/scores.json \
    --control base-mycelium --region surface=300,150,680,700 \
    --audit-sheet subjects/lichen/rounds/lc-r5-audit.jpg \
    --subject lichen -o subjects/lichen/rounds/lc-r5-review.md
python3 curate.py --period subjects/lichen/period-05 --from work/lichen/r5/round.json \
    --pick mycelium-3forms=01-mycelium-3forms --pick mycelium-forms-algae=02-mycelium-forms-algae \
    --control base-mycelium=controls/mycelium --note "…" --force
bash make_sheet.sh period subjects/lichen/period-05
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 05 "The Symbiont" delivered 2 images (finale) | 小七 |
