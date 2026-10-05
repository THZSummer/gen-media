# Cordyceps Part Table (fungus + insect)

> 🌐 Language: **English** | [中文](parts.md)

> Back to the [sub-theme home](README.en.md) ｜ [project home](../../README.en.md)

**Design source**: the **caterpillar fungus** in the *Compendium of Materia Medica* —— the cordyceps fungus parasitizes moth larvae,
**the insect body and the stroma appear together**: in winter it is an insect, in summer the fungal stroma grows out of the insect body.
This is a splice explicitly recorded in the classic text and one that **really exists**.

**Base ＝ moth larva** (a highly set organism, **low-to-medium** morphological freedom).
Donor ＝ fungal parts: mycelium coating MY1 / stroma ST1 / spores SP1.

---

## 1. Part table and measured results

| No. | Part | prompt anchor | Type | Measured result |
|------|------|-------------|------|----------|
| MY1 | Mycelium coating | `a dense coating of pale fungal mycelium across the whole body` | **Same-material replacement** (insect shell → mycelium) | ⚠️ works (4.55) ｜ the contrast is clearly stronger after vacating the body-surface description |
| ST1 | Single stroma | `a single tall club-shaped fungal stroma rising from its body` | **Added into an empty slot + different form** | ✅ **fully works** (5.00 ×6) —— the mainstay part of this sub-theme |
| ST1x | Multiple stromata | `several tall club-shaped fungal stromata rising from its body` | same as above | ✅ **fully works** (5.00 ×2) |
| SP1 | Spores | `clusters of fine pale spores dusting the surface` | surface coating | ✅ fully works (5.00 ×2) |

## 2. Rule 96: vacating a slot works for **surface texture**, not for **canonical organs**

R1/R2 ran a clean control (same presentation, same seed, only the base wording changed):

| Base wording | Effect on MY1 |
|----------|-----------|
| **Occupied version**: `segmented pale body` (the insect itself is pale and fuzzy) | small marginal contribution, A=3 |
| **Vacated version**: describe only the head and the legs (smooth brown insect body) | the white mycelium coating is **visible at a glance**, A=4 |

> Compare with the earlier findings: the deer's legs and the fish's fins **cannot be vacated even by deleting the description** (Rules 89/87),
> because those are "canonical organs" —— **organs cannot be deleted, but surface texture can**.
>
> **Rule 96: what can be vacated is a "property" (surface texture, colour, grain); what cannot be vacated is a "structure" (organs, limbs).**

## 3. Why the stroma worked on the first try

The stroma satisfied three favourable conditions at once:
1. **Added into an empty slot** (this "grass" was never on the insect body to begin with) —— Rule 67, tier 1;
2. **Different in form** (club-shaped stroma vs. segmented insect body) —— Rule 91;
3. **High recognizability** (this image of the caterpillar fungus is already in the model's prior) —— Rule 90.

→ Single stroma, multiple stromata, with spores: all six images scored 5.00.

## 4. Bearing structure: the stroma grows out of the "insect body" and needs no extra organ

Unlike the claws of dragon-nines (which require limbs), the stroma **grows straight out of the body surface** ——
as long as the base has this "body surface" face, there is a landing site. This is the direct reason this sub-theme was easier than expected.

---

## Document revision history

| Date | Version | Change | Author |
|------|------|------|------|
| 2026-10-05 | v0.1 | Cordyceps part table MY1/ST1/SP1 + **Rule 96 (what can be vacated is a property, what cannot is a structure)** | 小七 |
