# Period 02 · The Deer with Crane Legs

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/dc-r2-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 7101 onward (multiple takes, see the provenance table)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Shallow marsh · morning light · eye level full body 400mm · square**

A wading bird's legs only read when it stands in shallow water: the water surface provides the reference for "how long the legs are", and the morning light draws a reflection on the water that lifts the legs' outline out.

> The presentation layer is **constant within a period** (every shot in that period, controls included, shares one set) and **varies between periods** (each of the five periods has its own identity).

## 2. This period's subject and result

**Base = deer**　**Transplant = the crane's slender legs G2 (the base does **not** write legs, freeing up the leg slots)**

| Part | ID | Result |
|------|------|------|
| Slender legs | G2 | ⚠️ **partially established**: the legs become thinner and longer and the joints lean toward a wading bird; **but they are still the deer's brown fur + hooves** |

**A further version of the control was made outside this round** (R3): the base described `four long legs` as usual (no slot freed), and the result was **almost identical** to the vacated version — this control is written up in [dc-r1-r6.md](../rounds/dc-r1-r6.md).

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-deer-cranelegs.png`](01-deer-cranelegs.png) | G2 (**main image**) | **4.25** ✅ final | `ee9581d9` | `35cf81506f` |
| 2 | [`02-deer-cranelegs-b.png`](02-deer-cranelegs-b.png) | G2 (seed 7102) | **4.25** ✅ final | `2b0b1816` | `218c14f8f8` |

Control: [`controls/deer.png`](controls/deer.png) —— the pure-deer base from the **same round** (same seed, same presentation, same sentence skeleton).

## 4. What this period verified

1. **Vacating a placeholder neither adds nor subtracts for a canonical structure** (R2 vs R3): the length of the legs was changed, but the material (brown + hooves) was not — material is what decides success or failure.
2. The originally planned "low camera · vertical" was changed to eye-level full body per rule 80: at a low camera in a vertical canvas, terminal parts get drawn as another individual.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject deer-crane 2 --dry
python3 run_round.py --subject deer-crane 2
python3 score.py --round work/deer-crane/r2/round.json --scores work/deer-crane/r2/scores.json \
    --control base-deer --region legs=350,550,350,400 \
    --audit-sheet subjects/deer-crane/rounds/dc-r2-audit.jpg \
    --subject deer-crane -o subjects/deer-crane/rounds/dc-r2-review.md
python3 curate.py --period subjects/deer-crane/period-02 --from work/deer-crane/r2/round.json \
    --pick deer-cranelegs=01-deer-cranelegs --pick deer-cranelegs-b=02-deer-cranelegs-b \
    --control base-deer=controls/deer --note "…" --force
bash make_sheet.sh period subjects/deer-crane/period-02
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 02 "The Deer with Crane Legs" delivered 2 images (partially established); includes the occupied-slot control R3 | 小七 |
