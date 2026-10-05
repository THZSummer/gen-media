# Nine-resemblances Part List (dragon · nine resemblances)

> 🌐 Language: **English** | [中文](parts.md)

> Back to the [sub-theme home page](README.en.md) ｜ [project home page](../../README.en.md)

**Design source**: this is a part table written by the ancients, not one we defined. The traditional dragon-painting mnemonic "three pauses, nine resemblances":

> antlers like a deer, head like a camel, eyes like a rabbit, neck like a snake, belly like a shen, scales like a fish, claws like an eagle, paws like a tiger, ears like an ox

---

## 1. Part List and Mechanism Predictions

| No. | Nine resemblances | Donor | prompt anchor (the donor contributes only the part) | placeholder on the snake base | Prediction |
|------|------|------|------------------------------|------------------|------|
| D1 | antlers like a deer | deer | `a pair of branching deer antlers` | empty slot ✅ | easy (**measured successful**) |
| D2 | head like a camel | camel | `an elongated camel's head with a blunt muzzle` | empty slot, but **the head is a whole-noun slot** | ❌ **unsuccessful** (measured): still appears 0% after freeing the placeholder; deleting the base's species noun drags out **a whole camel** |
| D3 | eyes like a rabbit | rabbit | `a pair of round dark rabbit's eyes` | **occupied** (the base writes `dark lidless eyes`) | ❌ **unsuccessful** (measured): still does not land after freeing the eye slot; a small-part transplant has no available technique |
| D4 | neck like a snake | — | the base itself | — | base |
| D5 | belly like a shen | shen (**mythical**) | — | no real counterpart | **a visual proxy must be defined first**; not executed for now |
| D6 | scales like a fish | fish | `large overlapping fish scales` | occupied but **can be freed** (just delete the scale description from the base) | ⚠️ partial (**measured**): the scales become larger and more regular, but without the fish scale's fan pattern/iridescence |
| D7 | claws like an eagle | eagle | `sharp curved eagle talons on its front feet` | empty slot, **but limbs are needed** | snake base ❌ failure; **lizard base partial** (see D8 for the L-shaped comparison) |
| D8 | paws like a tiger | tiger | `broad tiger paws with heavy pads on its hind feet` | empty slot, **but limbs are needed** | **unsuccessful** on a lizard base (the foot form is occupied by the lizard: the claw shape can change, the foot pads cannot) |
| D9 | ears like an ox | ox | `a small pointed ox's ear` | empty slot ✅ | easy (**measured successful**) |

## 2. Base Selection (the most important engineering conclusion of this round)

| Part type | Base needed | Basis |
|----------|-----------|------|
| head parts (D1 antlers / D3 eyes / D9 ears) | **a snake** suffices | the snake has a head, and head parts are local additions |
| limb parts (D7 claws / D8 paws) | **must have limbs** (lizard / crocodile) | R1 measured: on a snake base the eagle talons **never appeared at all**—not overridden by a placeholder, but with **nowhere to grow** |
| torso parts (D6 scales) | a snake, but of the "already occupied" kind | expected to be overridden by the base's own scale description |

> **Rule supplement (a narrowing of rule 56)**: rule 56 says "a part the base has no placeholder for can be transplanted in",
> but that assumes by default that **the bearing structure the part needs exists**. A snake has no forelimbs → the eagle talons have no landing site.
> **The base's anatomy must be able to bear the transplant piece.**
>
> This matches the dragon's image: **the Chinese dragon is a four-legged snake body**—"neck like a snake" takes the snake, the "four legs" find another.

## 3. Phrasing Discipline for Transplant Pieces (following rule 57)

```
✅ a pair of branching deer antlers              ← 部位修饰语，安全
✅ sharp curved eagle talons on its front feet    ← 部位修饰语，安全
❌ whose body is entirely a deer's                ← 整体名词，会拖出整只鹿
```

And **the base description must deliberately leave the target part blank**: the lizard base writes `four stout legs` (not `clawed`),
leaving the foot position to D7, otherwise it will be overridden by the base's own description, as with cat-eagle's "cat paws".

---

## 4. Topic Priority (summarized after five periods)

| Priority | Type | Example | Measured |
|--------|------|------|------|
| 1 | **add into an empty slot** (the base simply does not have this part) | antlers, ears | ✅ fully successful |
| 2 | **free a placeholder** (first delete the corresponding description from the base) | claws (rewriting the base to `four stout legs`), scales (deleting keeled scales) | ⚠️ partial |
| 3 | **same-material replacement** (the base already has a part of the same kind) | scale for scale | ⚠️ partial and **hard to read**, low conceptual legibility |
| ❌ | **head parts / small parts** (where the species identity lies) | camel head D2, rabbit eyes D3 | **0%—do not write into final targets** |

> When two parts are of similar difficulty, **prefer the one the base simply does not have**.
> But "an empty slot" is only a necessary condition: **head parts cannot be swapped out even in an empty slot** (see below).

### Coverage of the nine resemblances

| Successful | Partial | Unsuccessful | Not executed |
|--------|----------|--------|--------|
| D1 antlers, D9 ears | D6 scales, D7 claws, D4 neck (the base itself) | D8 paws, **D2 camel head**, **D3 rabbit eyes** | D5 shen (needs a visual proxy) |

### Head Parts Are a Two-Way Dead End (measured at R8/R9)

| Base phrasing | Transplant piece | Result |
|----------|--------|------|
| `a large wild snake …` (with a species noun) | camel head | **camel head 0%**—suppressed by the base's prior (freeing the placeholder is also ineffective) |
| `a long muscular low body with keeled scales …` (without a species noun) | camel head | **a whole camel**—the donor takes over the entire individual and the base is destroyed |

**The base's species noun is both a "placeholder" and an "anchor"**: keep it and the transplant piece cannot get in; delete it and the donor takes over the base along with everything else.
→ Head swaps / beak swaps / face swaps are **not a final target for any sub-theme**.

---

## Document Revision History

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Nine-resemblances part list D1–D9 + mechanism predictions + base-selection conclusion | 小七 |
| 2026-10-04 | v0.2 | Five-period finale: added the D2/D3 measurements (neither successful) and the section on head parts being a two-way dead end; corrected D3's original "empty slot" verdict to "occupied" | 小七 |
