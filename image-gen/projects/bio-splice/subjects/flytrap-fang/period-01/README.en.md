# Period 01 · The Flytrap with Fangs

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/ff-r3-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 10101 / 10102 / 10103**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Features (Presentation)

**Swamp · side backlight · macro 100mm · square**

The grazing side backlight makes the red inner face glow and outlines the fangs along the edge ——
the subject of this period is **that row of fangs along the trap edge**, so the light must come in at an angle from the edge.

## 2. This Period's Theme and Results

**Base ＝ Venus flytrap (freed version: marginal teeth not described)**　**Transplant ＝ mammal fangs T1**

| Part | ID | Result |
|------|------|------|
| Mammal fangs | T1 | ✅ **fully holds**: a bare trap edge lines up a whole row of white triangular fangs |

⚠️ **Using the "freed version" as the base is intentional** (Rule 100): R1's occupied version (the base already said `a fringe of
stiff marginal teeth`) only showed "the marginal teeth turning thicker and whiter" (4.55); once the marginal teeth are freed, the fangs **appear out of nothing** (5.00).

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-flytrap-fangs.png`](01-flytrap-fangs.png) | T1 (**main image**) | **5.00** ✅ preferred final | `10d93ab2` | `6a684ffd56` |
| 2 | [`02-flytrap-fangs-b.png`](02-flytrap-fangs-b.png) | T1 (seed 10102) | **5.00** ✅ preferred final | `06522e4e` | `b32fb3ea87` |
| 3 | [`03-flytrap-fangs-c.png`](03-flytrap-fangs-c.png) | T1 (seed 10103) | **5.00** ✅ preferred final | `36512398` | `75787548b2` |

Control: [`controls/flytrap.png`](controls/flytrap.png) —— the pure Venus flytrap from the **same round** (freed version, no fangs along the edge).

## 4. This Period's Verification

1. **Boundary appendages ≈ attributes, and can be freed** (Rule 100): the marginal teeth are the morphology of the edge, not an organ,
   so deleting them does not affect "this is a Venus flytrap" —— in contrast with deer legs and fish fins (structures).
2. The landing site is the **trap edge** (the position of an appendage attribute) rather than a canonical structure (Rule 99).

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject flytrap-fang 3 --dry
python3 run_round.py --subject flytrap-fang 3
python3 score.py --round work/flytrap-fang/r3/round.json --scores work/flytrap-fang/r3/scores.json \
    --control base-flytrap --region lobe=250,150,550,500 \
    --audit-sheet subjects/flytrap-fang/rounds/ff-r3-audit.jpg \
    --subject flytrap-fang -o subjects/flytrap-fang/rounds/ff-r3-review.md
python3 curate.py --period subjects/flytrap-fang/period-01 --from work/flytrap-fang/r3/round.json \
    --pick flytrap-fangs=01-flytrap-fangs --pick flytrap-fangs-b=02-flytrap-fangs-b \
    --pick flytrap-fangs-c=03-flytrap-fangs-c \
    --control base-flytrap=controls/flytrap --note "…" --force
bash make_sheet.sh period subjects/flytrap-fang/period-01
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-05 | v0.1 | Period 01 [The Flytrap with Fangs] delivered 3 images (freed-version base, all preferred finals) | 小七 |
