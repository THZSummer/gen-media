# Period 01 · Crustose Lichen

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/lc-r1-review.en.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**all 4 images share seed 8101**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Rock face · side light · macro eye level 100mm · square**

Foundational period: photograph the two halves, "fungus + alga", clearly and separately, then photograph what they look like together.
The rock face + grazing side light picks out every crack in the crustose surface.

> This sub-theme's constant layer differs from the animal sub-themes: **a macro framing sentence + `macro photograph, focus-stacked`**
> ——**scale is also part of the presentation layer** (rule 93).

## 2. This period's subject and result

**Base = fungal mycelium**　**Transplant = crustose form CR1 + green algal cells AL1**

| Part | ID | Result |
|------|------|------|
| Crustose form | CR1 | ✅ fully established: a cracked crustose crust with radiating edges |
| Green algal cells | AL1 | ✅ **fully established**: clusters of bright green algal cells embedded among the hyphae |
| Both parts in one body | CR1+AL1 | ✅ reads as one complete lichen, not a collage |

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-mycelium-crust.png`](01-mycelium-crust.png) | CR1 (**main image**) | **5.00** ✅ preferred | `3b2a1c5c` | `db31e693c6` |
| 2 | [`02-mycelium-algae.png`](02-mycelium-algae.png) | AL1 | **5.00** ✅ preferred | `55365538` | `9d63662222` |
| 3 | [`03-mycelium-crust-algae.png`](03-mycelium-crust-algae.png) | CR1+AL1 | **5.00** ✅ preferred | `488dbcbb` | `9c5d1ac97c` |

Control: [`controls/mycelium.png`](controls/mycelium.png) —— the pure-mycelium base from the **same round** (same seed, same presentation, same sentence skeleton).

## 4. What this period verified

1. **A cross-domain donor lands 100% for the first time**: the green algal cells are a cross-kingdom part (alga vs fungus), and this project had never had a cross-domain part fully establish before.
2. The reason lies in the base: **the mycelium is a mass with no fixed shape** (rule 92) — the model has no prior of "what it should grow into" to resist the transplanted part.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject lichen 1 --dry
python3 run_round.py --subject lichen 1
python3 score.py --round work/lichen/r1/round.json --scores work/lichen/r1/scores.json \
    --control base-mycelium --region surface=200,200,620,620 \
    --audit-sheet subjects/lichen/rounds/lc-r1-audit.jpg \
    --subject lichen -o subjects/lichen/rounds/lc-r1-review.md
python3 curate.py --period subjects/lichen/period-01 --from work/lichen/r1/round.json \
    --pick mycelium-crust=01-mycelium-crust --pick mycelium-algae=02-mycelium-algae \
    --pick mycelium-crust-algae=03-mycelium-crust-algae \
    --control base-mycelium=controls/mycelium --note "…" --force
bash make_sheet.sh period subjects/lichen/period-01
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 01 "Crustose Lichen" delivered 3 images (all preferred) | 小七 |
