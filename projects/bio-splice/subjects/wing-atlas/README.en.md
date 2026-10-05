# Sub-theme: wing · atlas

> 🌐 Language: **English** | [中文](README.md)

> Back to the [project home](../../README.en.md) ｜ part table in [`parts.md`](parts.en.md) ｜ development log in [`rounds/`](rounds/)

> **Whole-sub-theme overview sheet**: [`sheet.jpg`](sheet.jpg) —— one row per period, all finals of that period stitched together (`bash make_sheet.sh subject wing-atlas` reproduces it)

## 1. Concept: treating a "wing" as an **addable organ**

**Fix one bird (keeping its own wings), then add another creature's pair of wings on its back.**
This volume is the **only sub-theme in the whole project that does not change the base** —— so it is a true "atlas":
one and the same individual, one and the same camera spec, only the pair of wings on the back changes.

- **Base ＝ medium-sized bird** (keeps its own wings)
- Donor ＝ four kinds of "second pair of wings": insect membranous wings / bat leathery wings / flying fish long fins / crane white wings

> The original plan was "replace the bird's wings **with** other wings" (same-material replacement, Rule 67 tier 3),
> and per Rule 99 it was changed to "**add another pair on the back**" (landing site = the empty face of the back) —— this is the precondition for this volume to work.

## 2. Results: 11 finals / 5 sections, three of four parts fully work

| Section | Donor | **Semantic category** | Presentation | Finals | Score |
|------|------|--------------|------|------|------|
| [period-01](period-01/README.en.md) | **Baseline** (no transplanted part) | — | branch tip · side backlight · eye level · square | 3 | **5.00 ×3** |
| [period-02](period-02/README.en.md) | Insect membranous wings | **is a wing** | branch tip · top light · square | 2 | **5.00 ×2** |
| [period-03](period-03/README.en.md) | Bat leathery wings | **is a wing** | cave mouth · hard light · square | 2 | **5.00 ×2** |
| [period-04](period-04/README.en.md) | Flying fish long fins | **carries the sense of "flying"** | waterside · moist light · square | 2 | **5.00 ×2** |
| [period-05](period-05/README.en.md) | Crane white wings | **is a wing** | autumn forest · backlight · wide-angle · landscape | 2 | **5.00 ×2** |

| Not included | Donor | Semantics | Result |
|--------|------|------|------|
| ❌ | Fish pectoral fins | merely fins | **0%** (zoomed ×1.7 only ordinary feathered wings) |
| ⚠️ | Maple samara wings | merely seeds | partial (spread out and paler, no samara shape) |

## 3. Rule 107: **the donor's semantic category must match the landing site's function**

Same landing site (the back), same sentence pattern, same seed, **only the donor changed**:

| Donor | Semantics | Result |
|------|------|------|
| Insect membranous wings / bat leathery wings | wings that fly | ✅ |
| **Flying fish** long fins | fins, but **carrying "flight" in themselves** | ✅ |
| Fish pectoral fins | fins, unrelated to flight | ❌ |
| Maple samara wings | plant seeds | ⚠️ |

> **A "wing-like shape" alone is not enough** (fish fins and samaras also look like wings); the donor **must carry the semantics of "being able to fly"**.
> This is Rule 85 (habitat semantic compatibility) at the **part–landing-site** level.

## 4. Design point: the **baseline section** (Rule 108)

The first section **contains no transplanted part**, only three takes of the unified base:
it is both "the first page of the atlas" and the **frame of reference** for the next four sections.
→ Atlas-type sub-themes (this volume and `horn-atlas`) both use this structure.

## 5. Self-assessment

| Item | Value |
|----|----|
| Rounds | 8 rounds (R1 baseline / R2–R5 four kinds of wings / R6 semantic questioning / R7–R8 finalizing) |
| Images generated | 25 images (zimage, 1024² / 1280×1024, steps 12) |
| Finals | **11 images / 5 sections** |
| Average score | **5.00** (all first choice) |
| Disqualified | 2 images (fish pectoral fins ×2) + 3 partial images (samara wings) |

**In one sentence**: this volume used all three favourable conditions —— "empty face at the landing site + different form + high recognizability" —— at once,
and the only pitfall was **semantics** —— which is also the first time in the whole project that "semantic category" and "shape similarity" were looked at separately.

## 6. Development log

| File | Content |
|------|------|
| [`parts.md`](parts.en.md) | **Wing atlas part table** (five kinds of wings + two negative/uncertain) + Rules 107/108 |
| [`rounds/wa-r1-r6.md`](rounds/wa-r1-r6.en.md) | R1–R6: baseline and four kinds of wings, semantic questioning |
| [`rounds/wa-r7-r8.md`](rounds/wa-r7-r8.en.md) | R7–R8: finalizing periods 04/05 |
| `rounds/wa-rN-review.md` | scoring review report for each round |
| [`rounds/prompts-all.md`](rounds/prompts-all.en.md) | verbatim prompt archive for every round |

---

## Document revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.2 | **Five-section finale**: all 11 finals are first choice; proposed **Rule 107 (the semantic category must match the landing site's function)** and 108 (the baseline section of an atlas volume); two donors honestly recorded as negative/uncertain | 小七 |
| 2026-10-04 | v0.1 | Plan: five-period schedule (planning first, not yet generated) | 小七 |
