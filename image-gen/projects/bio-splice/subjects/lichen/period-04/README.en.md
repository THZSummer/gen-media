# Period 04 · The Algal Layer Made Visible

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/lc-r4-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 8101 / 8102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Simulated cross-section · ring light · deep depth of field · square**

The algal layer is normally hidden inside the lichen, which makes this **the hardest period to show**. So the presentation was simply written as
"the surface layer lifted away, revealing the internal structure" — once the cross-section holds, the green spheres and algal filaments **become the protagonists of the frame**.

## 2. This period's subject and result

**Base = fungal mycelium**　**Transplant = green algal cells AL1 + algal filaments AL2 (simulated cross-section)**

| Part | ID | Result |
|------|------|------|
| Green algal cells | AL1 | ✅ fully established: the cup-shaped cross-section is packed with green spheres |
| Algal filaments | AL2 | ✅ fully established: fine filaments thread between the green spheres |

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-mycelium-algal-layer.png`](01-mycelium-algal-layer.png) | AL1+AL2 (**main image**) | **5.00** ✅ preferred | `dc6d41cb` | `cb9d81c1eb` |
| 2 | [`02-mycelium-algal-layer-b.png`](02-mycelium-algal-layer-b.png) | AL1+AL2 (seed 8102) | **5.00** ✅ preferred | `b5af9b8f` | `2af32f0c81` |

Control: [`controls/mycelium.png`](controls/mycelium.png) —— the pure-mycelium base from the **same round**.

## 4. What this period verified

1. **Presentation can rescue a weak period** (rule 94): mechanically this period belongs to the "internal structure / same material" tier and should have been the hardest;
   after switching to a simulated cross-section both images are 5.00.
2. This shows that **"invisible" is often a presentation problem, not a transplant problem** — change the presentation first, then consider swapping the part.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject lichen 4 --dry
python3 run_round.py --subject lichen 4
python3 score.py --round work/lichen/r4/round.json --scores work/lichen/r4/scores.json \
    --control base-mycelium --region surface=200,200,620,620 \
    --audit-sheet subjects/lichen/rounds/lc-r4-audit.jpg \
    --subject lichen -o subjects/lichen/rounds/lc-r4-review.md
python3 curate.py --period subjects/lichen/period-04 --from work/lichen/r4/round.json \
    --pick mycelium-algal-layer=01-mycelium-algal-layer \
    --pick mycelium-algal-layer-b=02-mycelium-algal-layer-b \
    --control base-mycelium=controls/mycelium --note "…" --force
bash make_sheet.sh period subjects/lichen/period-04
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 04 "The Algal Layer Made Visible" delivered 2 images (a simulated cross-section rescued a weak period) | 小七 |
