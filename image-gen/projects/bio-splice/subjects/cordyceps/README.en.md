# Sub-theme: Cordyceps (Fungus + Insect)

> 🌐 Language: **English** | [中文](README.md)

> Back to [project home](../../README.en.md) ｜ part table in [`parts.md`](parts.en.md) ｜ development log in [`rounds/`](rounds/)

> **Whole-sub-theme overview sheet**: [`sheet.jpg`](sheet.jpg) — one row per period, with that period's finals assembled together (reproducible with `bash make_sheet.sh subject cordyceps`)

## 1. Concept: a **real** spliced organism explicitly stated in the classics

**Cordyceps** in the 《Bencao Gangmu》: the cordyceps fungus parasitises a ghost moth larva, and **the insect body and the stroma appear together** —
in winter it is an insect, in summer the fungus's stroma grows out of the insect body.
This is a **really existing** spliced organism explicitly stated in the classics, and along with lichen (lichen = fungus + alga) it belongs to Group B.

- **Base = moth larva** (a fixed organism, morphological freedom **low to medium**)
- Donors = the fungus's parts: mycelium covering MY1 / stroma ST1 / spores SP1

## 2. Result: 11 finals / 5 periods, **all fully hold except the mycelium covering**

| Period | Theme | Part | Presentation | Finals | Score |
|----|------|------|------|------|------|
| [period-01](period-01/README.en.md) | **The mycelium-covered insect** | MY1 (freed-version base) | soil surface · soft light · macro 100mm · square | 3 | 4.55 ×3 |
| [period-02](period-02/README.en.md) | **A single stroma** | ST1 | alpine meadow · morning light · low camera · portrait | 2 | **5.00 ×2** |
| [period-03](period-03/README.en.md) | **Multiple stromata** | ST1x | alpine meadow · backlight · square | 2 | **5.00 ×2** |
| [period-04](period-04/README.en.md) | **Stroma and spores** | ST1 + SP1 | snowline gravel · cold light · landscape | 2 | **5.00 ×2** |
| [period-05](period-05/README.en.md) | **Cordyceps** (finale · **specimen shot**) | MY1 + ST1 + SP1 | neutral background · ring light · full focus · square | 2 | **5.00 ×2** |

**Average 4.88**; all 11 finals ✅ first-pick.

## 3. Core finding: **what can be freed is an "attribute"; what cannot is a "structure"** (Rule 96)

R1/R2 ran a clean control pair (same presentation, same seed, only the base wording swapped):

| Base wording | Effect on the mycelium covering MY1 |
|----------|---------------------|
| **Occupied version**: `segmented pale body` (the insect is itself pale and fuzzy) | small marginal contribution (A=3) |
| **Freed version**: write only head and legs (the body is smooth brown) | the white mycelium covering is **visible at a glance** (A=4) |

> Against the conclusions of earlier rounds: **the deer's legs, the fish's fins and the cat's paws cannot be freed by deleting their description either** (Rules 89/87).
> The difference is that **organs are structures, while surface texture is an attribute** —
> **attributes can be freed, structures cannot.**
>
> This complements Rule 92 (base morphological freedom): 92 is about "how fixed the base is overall",
> while 96 is about "**whether the spot you want to free is a structure or an attribute**".

## 4. Why the stroma worked on the first try (this sub-theme's workhorse part)

The stroma satisfies three favourable conditions at once:
1. **Empty-slot addition** (the insect body never had this "grass") — Rule 67, tier 1
2. **Different shape** (a club-shaped stroma vs a segmented insect body) — Rule 91
3. **High distinguishability** (the cordyceps image is already in the model's prior) — Rule 90

And it **needs no extra bearing structure**: it grows straight out of the body surface, so any "body surface" face gives it a landing site
(compare dragon-nines' eagle claws, which "require limbs"). → **Rule 97**.

## 5. The finale switches presentation medium (Rule 98)

Period 05 is the project's **first change of presentation medium**: no longer a field ecology shot but a **specimen shot**
(neutral grey background + ring light + full focus, with the framing sentence also switched to "specimen shot").

Not a word of the parts changed, but the deliverable's identity shifts from "photographed" to "collected" —
**this is the least effortful upgrade for a finale**, and it is available later for `tree-beast` and for Group C's two atlases.

## 6. Self-assessment

| Item | Count |
|----|----|
| Rounds | 7 rounds (R1 probe / R2 occupied-vs-freed control / R3–R7 finalizing the five periods) |
| Images generated | 22 (zimage, 1024² / 1280×1024 / 1024×1280, steps 12) |
| Finals | **11 images / 5 periods** |
| Average score | **4.88** (lowest 4.55, highest 5.00) |
| Rejected | 0 |

**In one sentence**: the base is a "fixed insect", yet it is not as hard as imagined — because **the stroma needs no bearing structure**
and **the cordyceps prior is already in the model**. The only genuinely hard part is the "same-material replacement" mycelium covering,
and that was recovered by **freeing a body-surface attribute**.

## 7. Development log

| File | Content |
|------|------|
| [`parts.md`](parts.en.md) | **Cordyceps part table** (MY1/ST1/SP1) + Rules 96/97 |
| [`rounds/cd-r1-r2.md`](rounds/cd-r1-r2.md) | R1–R2: separate probes for the hard piece / easy piece + the occupied-vs-freed control |
| [`rounds/cd-r3-r7.md`](rounds/cd-r3-r7.md) | R3–R7: finalizing the five periods (including the specimen-shot finale) |
| `rounds/cd-rN-review.md` | Review reports for each round's scoring |
| [`rounds/prompts-all.md`](rounds/prompts-all.md) | Verbatim prompt archive for every round |

---

## Revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.2 | **Five periods finalized**: all 11 finals first-pick; Rules 96–98 added (attributes can be freed / structures cannot, a piece growing out of the body surface needs no bearing structure, changing the presentation medium = a finale upgrade) | 小七 |
| 2026-10-04 | v0.1 | Planning: five-period schedule (planning first, not yet generated) | 小七 |
