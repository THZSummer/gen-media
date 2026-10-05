# Deer-Crane Part Table (Deer + Crane · Deer and Crane in Spring)

> 🌐 Language: **English** | [中文](parts.md)

> Back to [sub-theme home](README.en.md) ｜ [project home](../../README.en.md)

**Design source**: the traditional auspicious pattern **"Deer and Crane in Spring"** (the deer puns on "emolument", the crane stands for long life)
is itself a **juxtaposition of two animals into one motif**.
So this sub-theme's approach is: **take the motif apart and mount the crane's parts onto the deer**.

**Base = deer** (red deer); donors = the crane's parts: long neck G1 / thin legs G2 / tail feathers G6.
~~Crest G3 / wings G4 / beak G5~~ removed: the crest and beak are on the head (Rule 73), and a deer has no wing base (Rule 74).

---

## 1. Part table and measurements

| ID | Part | prompt anchor | Placeholder on the deer base? | Measured result |
|------|------|-------------|------------------|----------|
| G1 | Long neck | `a long slender crane's neck with fine grey feathers` | **Canonical structure** (the deer's neck cannot be deleted) | ⚠️ **partially holds**: the neck grows longer and thinner and stands up, but has none of the crane's fine grey feathers |
| G2 | Thin legs | `a pair of long thin crane's legs` | **Canonical structure** (the deer's legs cannot be deleted) | ⚠️ **partially holds**: the legs become long and thin with a jointed look closer to a wading bird's, but are still brown + hooves |
| G6 | Tail feathers | `a fan of long white crane tail feathers` | **True empty slot** (the deer's tail is so short it is almost invisible) | ✅ **fully holds**, but with a **hit rate of 1/4** (only 1 of 4 seeds worked) |

## 2. Core finding: canonical structures "can be reshaped, but not re-materialed"

The deer's neck and legs belong to the same class as a fish's fins, a cat's paws and a snake's scales — **canonical structures** (Rule 87):

| Practice | Result |
|------|------|
| The base **does not write** legs, only "deer + head + ears + coat colour + short tail" | the deer's legs are restored by the model itself; the crane-leg sentence only makes the legs **thinner and longer** |
| The base **writes** `four long legs` as usual | the conclusion is **almost identical**: the legs likewise become long and thin |

> **Freeing a placeholder neither helps nor hurts canonical structures** (the R2 vs R3 control):
> what decides success is the **material** (brown fur + hooves vs fine grey-black legs), not whether the description contains a placeholder.
> This is exactly the same type as the "claws" in dragon-nines — **shape can be changed, material cannot**.

## 3. Hit rate: even a true empty slot is not a guaranteed success

G6 tail feathers are the only "true empty slot" (the deer's tail is too short to see), yet only one of four seeds grew a feather fan:

| seed | Result |
|------|------|
| 7101 | ✅ a white feather fan grows from the rump |
| 7102 | ❌ only the deer's own white rump patch |
| 7103 | ❌ same as above |
| 7104 | ❌ same as above |

→ **An empty slot is necessary but not sufficient**; Rule 67's "empty-slot additions succeed most easily" needs one more clause:
**the donor part's distinguishability also matters** — a strongly distinguishable piece like "a fan of white feathers" works,
whereas a piece that shares the base's shape, like "a slender neck / leg", can only change shape, not material.

---

## Revision history

| Date | Version | Change | Author |
|------|------|------|------|
| 2026-10-05 | v0.1 | Deer-crane part table G1/G2/G6 + five-period measurements; added "canonical structures can be reshaped, not re-materialed" and "the hit rate of an empty slot" | 小七 |
