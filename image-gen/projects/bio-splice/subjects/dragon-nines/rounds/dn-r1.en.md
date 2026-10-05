# R1 · Snake base + deer antlers (D1) — and the discovery that "a part needs a bearing structure"

> 🌐 Language: **English** | [中文](dn-r1.md)

> Back to the [sub-theme home page](../README.en.md) ｜ Review report: [dn-r1-review.md](dn-r1-review.en.md)
> Engine: Z-Image-Turbo　1024²　steps 12　**all 4 images share seed 4201**
> Outputs: [`work/dragon-nines/r1/`](../../../work/dragon-nines/r1/)　`unapplied` all empty
> ℹ️ `work/` is not committed to the repo (a fixed seed makes it reproducible pixel by pixel)

---

## 1. Design

In the new sub-theme's first round, aim first at the **dragon's strongest marker**—deer antlers. The base is a snake ("neck like a snake" is the body's main axis).
The habitat changes to a reed wetland (to distinguish it from cat-eagle's autumn meadow), but **the photographic language stays the same**
(600mm f/4, overcast soft light, no sharpening), so that the two sub-themes can still be juxtaposed into one set.

| Shot | Transplant part | Purpose |
|------|--------|------|
| `base-snake` | — | **same-round base control** (the reference for objective metrics) |
| `snake-antler` | D1 deer antlers | verify on its own |
| `snake-antler-oxear` | D1 + D9 ox ears | **two stacked in the same region** (the ceiling test for Rule 59) |
| `snake-antler-claw` | D1 + D7 eagle claws | **cross-region** stacking, which also exposes the problem with limb parts |

## 2. Results

| Shot | Result | Score |
|------|------|------|
| `snake-antler` | ✅ forked antlers grow naturally from the skull, **reads as a dragon at a glance** | **5.00** ✅ final |
| `snake-antler-oxear` | ✅ antlers + pointed furry ox ears both in place | **4.65** ✅ final |
| `snake-antler-claw` | ❌ the antlers hold, but **the eagle claws never appear at all** | 3.65 ❌ not qualified |

**"A snake with horns" holds on the first try**—this validates the new sub-theme's concept: the ancients' part table can be executed directly.

## 3. Core finding: **a part needs a bearing structure**

In `snake-antler-claw` the eagle claws **never appear at all**. This is **not the same kind of failure** as cat-eagle's "cat paws fail":

| Failure type | Example | Mechanism |
|----------|------|------|
| **Overridden** by the base description | cat-eagle's cat paws (the base wrote `scaled yellow legs with black talons`) | Rule 56 |
| **Missing bearing structure** | this round's eagle claws (a snake **has no limbs**) | **supplement to Rule 56** |

> Rule 56 only says "a part for which the base has no placeholder can be transplanted in", but that assumes **the bearing structure the part needs exists**.
> A snake has no forelimbs → the claws have no landing site, **nowhere to grow**.

**This finding directly yields another base-selection principle beyond Rule 59**, and explains why the Chinese dragon is a **four-legged** snake body
— "neck like a snake" takes the snake, and the "four legs" must find another donor. On this basis the second period has already been switched to a lizard base.

## 4. Methodology note: the one-way nature of region diff is confirmed again

The body region diff of `snake-antler-claw` is **17.7** (without looking at the image, one would think "something happened at the body"),
but zooming in proves **there are no claws at all on the body**—that 17.7 is entirely posture drift caused by changing the wording.

> This is why `score.py` defines region diff as a **one-way alarm**: region unchanged → definitely did not land;
> region changed → cannot prove it was caused by the part.

---

## 5. Takeaways

62. **A part needs a bearing structure** (supplement to Rule 56): it is not enough that the base has no placeholder; the anatomical structure
    the part needs **must exist** on the base. A snake has no limbs → eagle claws have nowhere to grow.
63. **The base must be chosen by part type**: head parts (antlers/eyes/ears) can use a snake; limb parts (claws/paws) need a base that has limbs.
    This matches "the Chinese dragon is a four-legged snake body"—the dragon itself is "a snake body + separately found four legs".
