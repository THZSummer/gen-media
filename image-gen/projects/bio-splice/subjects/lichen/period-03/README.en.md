# Period 03 · Fruticose Lichen

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/lc-r3-review.en.md)
> Engine: Z-Image-Turbo　**1024×1280**　steps 12　**seed 8101 / 8103**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Tundra · backlight · macro low camera · vertical 1024×1280**

Fruticose lichen **stands up** (like a small shrub), so a low camera in a vertical canvas is used to look at its height;
the tundra backlight brightens the white frost on the tips.

## 2. This period's subject and result

**Base = fungal mycelium**　**Transplant = fruticose thallus FR1**

| Part | ID | Result |
|------|------|------|
| Fruticose thallus | FR1 | ✅ established: densely branching, with white frost on the tips, like a clump of Cladonia |

⚠️ **The base already branches on its own**: the mycelium description already contains `branching threads`,
and on the tundra it grew into a coral shape by itself — so the fruticose part only contributed "denser + white frost", and A is given 4.

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-mycelium-fruticose.png`](01-mycelium-fruticose.png) | FR1 (**main image**) | **4.55** ✅ preferred | `0bb08aee` | `acf842d977` |
| 2 | [`02-mycelium-fruticose-b.png`](02-mycelium-fruticose-b.png) | FR1 (seed 8103) | **4.55** ✅ preferred | `8313748e` | `bdec631b14` |

Control: [`controls/mycelium.png`](controls/mycelium.png) —— the pure-mycelium base from the **same round**.

## 4. What this period verified

1. **If the control has already done half the work, points must be deducted** (rule 95): the base carries the branching form itself,
   so the transplanted part's marginal contribution must be assessed honestly (4.55 rather than 5.00).
2. A vertical canvas + low camera is safe on **non-animal** subjects — the pitfall of rule 80 (terminal parts drawn as another individual)
   only applies to animal bases that can "grow limbs".

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject lichen 3 --dry
python3 run_round.py --subject lichen 3
python3 score.py --round work/lichen/r3/round.json --scores work/lichen/r3/scores.json \
    --control base-mycelium --region subject=250,250,520,700 \
    --audit-sheet subjects/lichen/rounds/lc-r3-audit.jpg \
    --subject lichen -o subjects/lichen/rounds/lc-r3-review.md
python3 curate.py --period subjects/lichen/period-03 --from work/lichen/r3/round.json \
    --pick mycelium-fruticose=01-mycelium-fruticose --pick mycelium-fruticose-b=02-mycelium-fruticose-b \
    --control base-mycelium=controls/mycelium --note "…" --force
bash make_sheet.sh period subjects/lichen/period-03
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 03 "Fruticose Lichen" delivered 2 images (4.55, points honestly deducted) | 小七 |
