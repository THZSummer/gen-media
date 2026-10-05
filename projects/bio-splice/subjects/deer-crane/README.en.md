# Sub-theme: Deer + Crane (Deer and Crane in Spring)

> 🌐 Language: **English** | [中文](README.md)

> Back to [project home](../../README.en.md) ｜ part table in [`parts.md`](parts.en.md) ｜ development log in [`rounds/`](rounds/)

> **Whole-sub-theme overview sheet**: [`sheet.jpg`](sheet.jpg) — one row per period, with that period's finals assembled together (reproducible with `bash make_sheet.sh subject deer-crane`)

## 1. Concept: taking an **auspicious motif** apart

**The traditional auspicious pattern "Deer and Crane in Spring"** (the deer puns on "emolument", the crane stands for long life)
is itself a **juxtaposition of two animals into one motif**.
So this sub-theme's approach is: take the motif apart and **mount the crane's parts onto the deer** —
to see whether "deer and crane in spring" can go from "juxtaposed" to "one body".

**Base = deer** (red deer); donors = the crane's parts: long neck G1 / thin legs G2 / tail feathers G6.
~~Crest G3 / wings G4 / beak G5~~ removed (head parts 73 / a deer has no wing base 74).

## 2. Conclusion first: **this "one body" only half counts**

| Part | Result | Notes |
|------|------|------|
| G1 long neck | ⚠️ partially holds | the neck grows longer and thinner and stands up, **but has none of the crane's fine grey feathers** |
| G2 thin legs | ⚠️ partially holds | the legs become long and thin with a sense of joints, **but are still brown fur + hooves** |
| G6 tail feathers | ✅ fully holds | a white feather fan grows from the rump (**hit rate 1/4**) |

**Five periods, 9 finals**, scores 4.25 (partial) / 5.00 (tail feathers) —
this sub-theme is **the only sub-theme without a full-score final**, recorded honestly, with no varnish.

## 3. Mechanism: canonical structures "can be reshaped, but not re-materialed"

The deer's neck and legs are **canonical structures** (Rule 87, same as fish fins, cat paws, snake scales). R2/R3 ran a control pair:

| Practice | Result |
|------|------|
| The base **does not write** legs | the deer's legs are restored by the model itself; the crane-leg sentence only makes the legs **thinner and longer** |
| The base **writes** `four long legs` as usual | the conclusion is **almost identical** |

> **Freeing a placeholder neither helps nor hurts canonical structures** — what decides success is the **material**
> (brown fur + hooves vs fine grey-black legs), not whether the description contains a placeholder.
> Same type as the "claws" in dragon-nines: **shape can be changed, material cannot**.

## 4. Hit rate: even a true empty slot is not a guaranteed success

G6 tail feathers are the only "true empty slot" (the deer's tail is too short to see); of four seeds only one worked:

| seed | 7101 | 7102 | 7103 | 7104 |
|------|------|------|------|------|
| Result | ✅ white feather fan | ❌ only the deer's own rump patch | ❌ | ❌ |

→ **An empty slot is necessary but not sufficient**. Rule 67 needs one more clause:
**also look at the donor part's distinguishability** — a highly distinguishable piece like "a fan of white feathers" works,
while a piece that shares the base's shape, like "a slender neck / leg", can only change shape, not material.

## 5. Constant within a period, varying between periods

| Period | Theme | Part | **Presentation (habitat · light · camera · canvas)** | Finals | Score |
|----|------|------|----------------------------------------|------|------|
| [period-01](period-01/README.en.md) | **The long-necked deer** | G1 | misty bamboo grove at dawn · soft light · eye level 400mm · square | 2 | 4.25 ×2 |
| [period-02](period-02/README.en.md) | **The crane-legged deer** | G2 (leg position freed) | shallow marsh · morning light · eye level full body · square | 2 | 4.25 ×2 |
| [period-03](period-03/README.en.md) | **The crane-tailed deer** | G6 (true empty slot) | reed beds · backlight · eye level 600mm · square | 1 | 5.00 |
| [period-04](period-04/README.en.md) | **Both neck and legs** | G1+G2 | frosty morning grassland · cold light · eye level · landscape | 2 | 4.25 ×2 |
| [period-05](period-05/README.en.md) | **Deer and Crane in Spring** (finale) | G1+G2+G6 | spring plum grove · soft diffused light · wide angle · landscape | 2 | 4.25 ×2 |

> Period 02 was originally "low camera · portrait", changed to **eye level, full body** per Rule 80 (a terminal part gets painted as a separate individual under a low camera in portrait format).
> Period 03 has only 1 final: the other three seeds grew no feather fan, and **we would rather deliver one than pad the count**.

## 6. Sub-theme summary (self-assessment after the finale)

### 1. Measurement ledger and self-assessment

| Item | Count |
|----|----|
| Rounds | 7 rounds (R1–R6 for the five periods + R7 tail-feather pickup takes; including R3's occupied-version control) |
| Images generated | 21 (zimage, 1024² / 1280×1024, steps 12) |
| Finals | **9 images / 5 periods** |
| Average score | **4.36** (lowest 4.25, highest 5.00) — the lowest in this project so far |
| Rejected | 5 (did not land), none entered a period directory |

**Self-criticism**: this sub-theme's finals "do not read as a splice" — four periods are just "a slender deer",
and only period 03's feather fan shows at a glance that it is a transplant. The reason is that **the donor parts chosen share the base's shape**
(neck↔neck, legs↔legs), so they can only change shape, not material.

→ **Planning lesson (written back into PLAN)**: when picking donors, **prefer pieces of a different shape from the base**
(feather fans, horns, ears, coiled bodies) over pieces that are "same name, different species" (neck for neck, legs for legs, scales for scales).

### 2. The three contributions

- **89 Canonical structures can be reshaped but not re-materialed**; freeing a placeholder **neither helps nor hurts** them
  (R2/R3 control), and what decides success is the material.
- **90 An empty slot is necessary but not sufficient**: the donor piece's **distinguishability** also matters
  (G6 feather fan hits 1/4; the same-shape pieces G1/G2 fully hold 0 times).
- **91 Donor priority narrows further**: **different shape > same shape**. One more filter inside empty-slot additions (67).

## 7. Development log

| File | Content |
|------|------|
| [`parts.md`](parts.en.md) | **Deer-crane part table** (G1/G2/G6) + hit rate and material conclusions |
| [`rounds/dc-r1-r6.md`](rounds/dc-r1-r6.en.md) | R1–R6: the five periods and the occupied-version control (the source of "freeing placeholders does not work on canonical structures") |
| [`rounds/dc-r7.md`](rounds/dc-r7.en.md) | R7: tail-feather pickup takes (the source of the 1/4 hit rate) |
| `rounds/dc-rN-review.md` | Review reports for each round's scoring |
| [`rounds/prompts-all.md`](rounds/prompts-all.en.md) | Verbatim prompt archive for every round |

---

## Revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.2 | **Five periods finalized**: 9 finals (mostly partial holds); Rules 89–91 added (shape changeable but not material / empty slot not sufficient / different shape first) | 小七 |
| 2026-10-04 | v0.1 | Planning: five-period schedule (planning first, not yet generated) | 小七 |
