# Sub-theme: Lichen (Fungus + Alga)

> 🌐 Language: **English** | [中文](README.md)

> Back to [project home](../../README.en.md) ｜ part table in [`parts.md`](parts.en.md) ｜ development log in [`rounds/`](rounds/)

> **Whole-sub-theme overview sheet**: [`sheet.jpg`](sheet.jpg) — one row per period, with that period's finals assembled together (reproducible with `bash make_sheet.sh subject lichen`)

## 1. Concept: the one nature has **already spliced**

**A lichen is itself a spliced organism** — a symbiosis of fungal hyphae + algae/cyanobacteria.
This is the **most ontological example** of "bio-splice": it is not that we attach A to B,
but that we **present a symbiosis that is already spliced**.

- **Base = fungal mycelium** (form and colour deliberately unwritten, both left to the transplanted parts)
- Donors = form parts (crustose CR1 / foliose FL1 / fruticose FR1) + algal parts (green cells AL1 / algal filaments AL2)

This is also the first sub-theme of Group B (cross-kingdom splicing) — **what is crossed is not species but kingdom**.

## 2. Result: **all five parts fully hold** (the project's best set)

| Period | Theme | Part | Presentation | Finals | Score |
|----|------|------|------|------|------|
| [period-01](period-01/README.en.md) | **Crustose lichen** | CR1 + AL1 | rock face · side light · macro eye level 100mm · square | 3 | 5.00 ×3 |
| [period-02](period-02/README.en.md) | **Foliose lichen** | FL1 + AL2 | tree bark · wet · macro high side angle · square | 2 | 5.00 / 4.55 |
| [period-03](period-03/README.en.md) | **Fruticose lichen** | FR1 | tundra · backlight · macro low camera · portrait | 2 | 4.55 ×2 |
| [period-04](period-04/README.en.md) | **Algal layer visible** | AL1 + AL2 (pseudo cross-section) | ring light · deep depth of field · square | 2 | 5.00 ×2 |
| [period-05](period-05/README.en.md) | **The symbiosis** (finale) | three forms ± algae | misty forest · diffused light · wide angle · landscape | 2 | 5.00 / 4.55 |

**Average 4.87**; all 11 finals ✅ first-pick.

## 3. Core finding: **the less fixed a base's shape, the more easily transplanted parts land** (Rule 92)

| Base | Prior strength | Transplanted-part result |
|------|----------|------------|
| Deer (deer-crane) | strong: neck/legs are **canonical structures** | can only change shape, not material (4.25) |
| Fish (fish-bird) | strong: fins are canonical structures | 0% |
| Snake / turtle / lizard (Group A) | medium: body shape fixed, but part positions can be freed | empty-slot parts fully hold |
| **Fungal mycelium (this sub-theme)** | **extremely weak: a mass of hyphae with no fixed shape** | **all five parts hold** |

> **Rule 92**: transplant difficulty correlates strongly with **the base's morphological freedom**.
> The more a base looks like "an already-fixed species", the harder the transplanted part; the more it looks like "a lump of raw material" (mycelium, slime mould, coral),
> the easier the transplanted part — the model has no "what it should look like" prior to resist with.
>
> This unifies 83/87 (canonical structures), 90 (an empty slot is not sufficient) and 91 (different shape first) into one simpler criterion.

## 4. Two new practices at the presentation layer

1. **Scale is also part of the presentation layer**: this is a creature a few centimetres across, so the framing sentence becomes "macro close-up"
   and the photographic layer becomes `macro photograph, focus-stacked`, rather than reusing the animal sub-themes' "full body + 600mm telephoto".
2. **The "pseudo cross-section" turns the hardest thing to see into the subject**: period 04 "algal layer visible" was originally the hardest period
   (the algal layer sits inside the lichen), but with the presentation "the surface layer lifted to reveal the internal structure",
   the green spheres and algal filaments became the picture's leads — **presentation can rescue a mechanically weak period**.

## 5. Self-assessment

| Item | Count |
|----|----|
| Rounds | 5 rounds (one round per period, each with a same-round base control) |
| Images generated | 16 (zimage, 1024² / 1280×1024 / 1024×1280, steps 12) |
| Finals | **11 images / 5 periods** |
| Average score | **4.87** (lowest 4.55, highest 5.00) |
| Rejected | 0 |

**In one sentence**: this is currently the **least effortful, highest-yield** sub-theme —
because "splicing" is the organism's own business here, and the model only has to paint hyphae and algae together.
**The four remaining sub-themes of Group B should all benefit from it**, though each has its own difficulty:
`cordyceps` is "fungus over insect" (same-material replacement), `flytrap-fang` has to cross into animal organs,
and `tree-beast`'s base is a tree (medium morphological freedom).

## 6. Development log

| File | Content |
|------|------|
| [`parts.md`](parts.en.md) | **Lichen part table** (CR1/FL1/FR1/AL1/AL2) + Rule 92 |
| [`rounds/lc-r1.md`](rounds/lc-r1.md) | R1: single-part + combination probes (**the first 100% landing for cross-kingdom parts**) |
| [`rounds/lc-r2-r5.md`](rounds/lc-r2-r5.md) | R2–R5: the four periods foliose / fruticose / algal layer / symbiosis |
| `rounds/lc-rN-review.md` | Review reports for each round's scoring |
| [`rounds/prompts-all.md`](rounds/prompts-all.md) | Verbatim prompt archive for every round |

---

## Revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.2 | **Five periods finalized**: all 11 finals first-pick; **Rule 92 (base morphological freedom decides transplant difficulty)** proposed; the two practices "scale is also part of the presentation layer" and "a pseudo cross-section rescues a weak period" established | 小七 |
| 2026-10-04 | v0.1 | Planning: five-period schedule (planning first, not yet generated) | 小七 |
