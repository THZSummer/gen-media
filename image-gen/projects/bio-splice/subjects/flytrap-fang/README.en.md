# Sub-theme: Venus flytrap + animal organs

> 🌐 Language: **English** | [中文](README.md)

> Back to the [project home](../../README.en.md) ｜ part table in [`parts.md`](parts.en.md) ｜ development log in [`rounds/`](rounds/)

> **Whole-sub-theme overview sheet**: [`sheet.jpg`](sheet.jpg) —— one row per period, all finals of that period stitched together (`bash make_sheet.sh subject flytrap-fang` reproduces it)

## 1. Concept: what is crossed is not the species but **the kingdom**

**A plant growing animal organs** —— the most striking direction within "biological splicing".
lichen / cordyceps are "two organisms that were already together"; this sub-theme is **mounting animal parts onto a plant**:
**plant kingdom ↔ animal kingdom**.

- **Base ＝ Venus flytrap** (its form is highly set: two traps + stiff marginal teeth + a red inner face)
- Donor ＝ animal parts: mammal fangs T1 (trap edge) / eye T2 (leaf blade) / tongue T4 (trap cavity)
- ~~Claw T3~~ removed: the Venus flytrap has no limbs (Rules 74/97)

## 2. Results: **all three parts fully work**

| Period | Theme | Part (landing site) | Presentation | Finals | Score |
|----|------|--------------|------|------|------|
| [period-01](period-01/README.en.md) | **The flytrap with fangs** | T1 mammal fangs (trap edge) | swamp · side backlight · macro 100mm · square | 3 | **5.00 ×3** |
| [period-02](period-02/README.en.md) | **The flytrap with an eye** | T2 eye (leaf blade) | swamp · eye level on the leaf blade · square | 2 | 4.80 ×2 |
| [period-03](period-03/README.en.md) | **The flytrap flicking its tongue** | T4 tongue (trap cavity) | moss · low camera · vertical | 2 | **5.00 ×2** |
| [period-04](period-04/README.en.md) | **Fangs and tongue complete** | T1 + T4 | after rain · hard side light · square | 2 | **5.00 ×2** |
| [period-05](period-05/README.en.md) | **Carnivorous plant** (finale) | T1 + T2 + T4 | misty swamp at dawn · backlight · wide-angle · landscape | 2 | 4.55 / **5.00** |

**Average 4.91**, all 11 finals ✅ first choice.

## 3. Rule 99: the criterion lies in the "landing site", not the "whole"

Before starting I used the "three questions" to predict that **this would be the hardest in Group B**: the flytrap's form is highly set (Rule 92 unfavourable).
Measured: **all three worked**. The difference lies in ——

| Part | Landing site | Nature of landing site | Result |
|------|------|----------|------|
| T1 mammal fangs | trap edge | boundary appendage (**property**) | ✅ fully works after vacating |
| T2 eye | leaf blade | empty face (a plant never had an eye) | ✅ works |
| T4 tongue | trap cavity | empty face (the cavity is empty) | ✅ fully works |
| — (control) deer neck / fish fin | neck / fin | **canonical structure** | ❌ form changes but not substance / 0% |

> **Rule 99: transplant difficulty depends on "whether the landing site is occupied by a canonical structure".**
> 92 is the whole-organism view (how set the base is); 99 brings it down to the local level:
> **a set overall form does not hinder transplantation, as long as the landing site itself is empty or is merely an appendage property.**

## 4. Adding the third category of "vacating a slot" (Rule 100)

R1/R2 ran a control with the same seed, the same presentation and only the base wording changed —— occupied version 4.55, vacated version **5.00**:

| Type | Example | Is vacating effective |
|------|---------|--------------|
| **Structure** (organs, limbs) | deer neck/deer legs, fish fin, cat paw, snake scales | ❌ deleting it just gets restored (87/89) |
| **Property** (surface texture, colour) | mycelium on the insect body (cordyceps) | ✅ effective |
| **Boundary appendage** (marginal teeth, marginal hairs) | the flytrap's marginal teeth (this sub-theme) | ✅ effective |

## 5. One shortfall recorded as it is

The **eye** in period 02 only reached 4.80: the eyeball is complete and the iris highlight is clear, but there are **no eyelids and no eye socket**,
and zoomed in it feels "pasted on" (C=4).
→ **Rule 101 (hypothesis, unverified)**: for cross-kingdom parts the "seam" decides credibility ——
adding an anatomical description of a "socket / eyelid / seam" may significantly raise the C score. Left for later verification.

## 6. Self-assessment

| Item | Value |
|----|----|
| Rounds | 7 rounds (R1–R2 occupied/vacated control / R3–R7 finalizing the five periods) |
| Images generated | 20 images (zimage, 1024² / 1280×1024 / 1024×1280, steps 12) |
| Finals | **11 images / 5 periods** |
| Average score | **4.91** (lowest 4.55, highest 5.00) |
| Disqualified | 0 images |

**In one sentence**: this is the sub-theme that was **predicted hardest but turned out easiest** ——
the lesson is: **do not judge by "how set the base is as a whole"; look at the "landing site"** (Rule 99).

## 7. Development log

| File | Content |
|------|------|
| [`parts.md`](parts.en.md) | **Venus flytrap part table** (T1/T2/T4) + Rules 99/100 |
| [`rounds/ff-r1-r2.md`](rounds/ff-r1-r2.en.md) | R1–R2: are the marginal teeth a structure or a property (same-seed control) |
| [`rounds/ff-r3-r7.md`](rounds/ff-r3-r7.en.md) | R3–R7: finalizing the five periods |
| `rounds/ff-rN-review.md` | scoring review report for each round |
| [`rounds/prompts-all.md`](rounds/prompts-all.en.md) | verbatim prompt archive for every round |

---

## Document revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.2 | **Five-period finale**: all 11 finals are first choice; proposed **Rule 99 (the criterion lies in the landing site, not the whole)**, 100 (boundary appendages ≈ properties), 101 (the seam decides credibility · hypothesis) | 小七 |
| 2026-10-04 | v0.1 | Plan: five-period schedule (planning first, not yet generated) | 小七 |
