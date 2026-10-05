# Sub-theme: flower + bird

> 🌐 Language: **English** | [中文](README.md)

> Back to the [project home](../../README.en.md) ｜ part table in [`parts.md`](parts.en.md) ｜ development log in [`rounds/`](rounds/)

> **Whole-sub-theme overview sheet**: [`sheet.jpg`](sheet.jpg) —— one row per period, all finals of that period stitched together (`bash make_sheet.sh subject flower-bird` reproduces it)

## 1. Concept: turning a **painting genre** into one body

**"Flower-and-bird" is the basic unit of Chinese painting** —— the corolla and the bird's plumage mimic each other (a hummingbird like a flower, an orchid like a bee).
This sub-theme turns that painting genre into **one body**: bird feathers grow in the places of the flower's parts.

- **Base ＝ large flower** (magnolia / lily)
- Donor ＝ three feather-type bird parts, **split by landing site**: P1 feather → petal ring / P5 down feather → flower centre / P6 plume feather → flower axis

## 2. Results: **two landing sites work, one does not**

| Period | Theme | Part (landing site) | Presentation | Finals | Score |
|----|------|--------------|------|------|------|
| [period-01](period-01/README.en.md) | **The flower of plume branches** | P6 plume feather (flower axis) | morning dew · soft light · macro 100mm · square | 3 | **5.00 ×3** |
| [period-02](period-02/README.en.md) | **The flower with a down centre** | P5 down feather (flower centre) | side light · square | 2 | 4.55 ×2 |
| [period-03](period-03/README.en.md) | **Both plume and down** | P6 + P5 | dark background · hard light · square | 2 | **5.00 ×2** |
| [period-04](period-04/README.en.md) | **The lily's down and plume** | P5 + P6 (flower species changed) | backlight · vertical | 3 | **5.00 ×3** |
| [period-05](period-05/README.en.md) | **Flower-and-bird** (finale · a full branch) | P6 + P5 | backlight · wide-angle · landscape | 2 | **5.00 ×2** |

**Average 4.93**, all 12 finals ✅ first choice.

## 3. Petals are a "canonical structure" —— third verification (P1 wiped out)

P1 "feather replacing petals" was tried with **three wordings**, and on **both the vacated version and the occupied version it was 0%**:

| Wording | Result |
|------|------|
| `in place of the petals` (relative clause) | ❌ |
| `a ring of broad pale bird feathers` (plain noun phrase) | ❌ |
| `…covering the flower` (covering style) | ❌ |

Yet **the very same "covering" wording works on the cordyceps larva** (mycelium coating 4.55).
→ The difference is the landing site: **the insect's body surface is a "property", the flower's petal ring is a "structure"** (third verification of Rules 96/99).

## 4. Why the plume feather is so strong (the only part of this sub-theme that works straight away)

1. The landing site is the **flower axis (a surface)** —— a part growing out of a surface needs no bearing structure (Rule 97)
2. **Different in form + high recognizability**: an upright plume feather vs. flat-spread petals (Rules 91/90)
3. Strong material contrast: white petals vs. semi-translucent feather filaments, which catch the light under backlight

All 10 single-part images scored 5.00.

## 5. Rule 102: a new base must have its hit rate re-verified

Same wording (P5 + P6), the same presentation, **only the flower species changed from magnolia to lily**:

| Base | Hit rate |
|------|--------|
| Magnolia | 5/5 |
| **Lily** | **1/2** (took three extra seeds to make up the numbers, R9) |

→ **"The wording is verified" ≠ "it works everywhere"**.

## 6. A counter-intuitive gain

Mechanically, "the petals cannot be swapped out" is a limitation, but **the limitation gave back a better composition**:
after the landing site retreated from the "petal ring" to the "flower centre", the image actually looked more like "flower-and-bird" ——
**not turning the flower into a bird, but letting a bird's feather grow out of the flower's "heart"** (Rule 104).

## 7. Self-assessment

| Item | Value |
|----|----|
| Rounds | 9 rounds (R1–R2 three petal wordings / R3–R4 empty-face landing-site probes / R5–R9 finalizing the five periods and extra takes) |
| Images generated | 29 images (zimage, 1024² / 1280×1024 / 1024×1280, steps 12) |
| Finals | **12 images / 5 periods** |
| Average score | **4.93** (lowest 4.55, highest 5.00) |
| Disqualified | 6 images (4 feather-replacing-petals + 1 lily miss + …), none of which entered the period directories |

## 8. Development log

| File | Content |
|------|------|
| [`parts.md`](parts.en.md) | **Flower-and-bird part table** (by landing site) + Rule 102 |
| [`rounds/fb2-r1-r4.md`](rounds/fb2-r1-r4.md) | R1–R4: feather-replacing-petals wiped out → moved to an empty-face landing site |
| [`rounds/fb2-r5-r9.md`](rounds/fb2-r5-r9.md) | R5–R9: finalizing the five periods and extra takes |
| `rounds/fb2-rN-review.md` | scoring review report for each round |
| [`rounds/prompts-all.md`](rounds/prompts-all.md) | verbatim prompt archive for every round |

---

## Document revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.2 | **Five-period finale**: all 12 finals are first choice; petals verified a third time as "cannot be swapped out"; added Rule 102 (a new base must have its hit rate re-verified) and 104 (the limitation gave a better composition) | 小七 |
| 2026-10-04 | v0.1 | Plan: five-period schedule (planning first, not yet generated) | 小七 |
