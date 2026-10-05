# R2 · Lizard base + eagle claws (D7) / tiger paws (D8) — partial success

> 🌐 Language: **English** | [中文](dn-r2.md)

> Back to the [sub-theme home page](../README.en.md) ｜ Review report: [dn-r2-review.md](dn-r2-review.en.md)
> Engine: Z-Image-Turbo　1024²　steps 12　**all 3 images share seed 4201**
> Outputs: [`work/dragon-nines/r2/`](../../../work/dragon-nines/r2/)　`unapplied` all empty

---

## 1. Design: change the base according to R1's finding

R1 proved that on a snake base the eagle claws **have nowhere to grow**, so this period switches to a **lizard** (it has limbs and is likewise a snake-shaped torso).

The key wording: **the base deliberately does not describe claws**—

```
✅ four stout legs            ← mentions only the legs, leaving the foot position to D7
❌ four clawed legs           ← would override the transplant part the way cat-eagle's "cat paws" did
```

| Shot | Transplant part |
|------|--------|
| `base-lizard` | — (**same-round base control**) |
| `lizard-talons` | D7 eagle claws (forefeet) |
| `lizard-talons-paws` | D7 forefeet + D8 tiger paws (hind feet) |

## 2. Results (judged at ×3 zoom)

Comparing the forefeet of the baseline and the transplanted version:

| | baseline · lizard | after transplant |
|---|---|---|
| Claw form | **short and blunt** lizard claws, lying flat on the ground | **long and curved** raptor-style claws, raised in a grasping pose |

**The claws partly hold**: the claw form has indeed changed, in the right direction; but it does not reach a complete eagle claw
(the foot is still dark and scaly, not an eagle's **yellow scaly tarsus + black curved claws**).
**Tiger paws D8 did not hold**: the hind feet are still lizard feet, with no broad thick tiger pads visible.

| Shot | Score | Verdict |
|------|------|------|
| `lizard-talons` | 3.90 | ✅ final |
| `lizard-talons-paws` | 4.05 | ✅ final |

## 3. What this round confirmed

1. **Changing the base is effective**: the same transplant part (eagle claws) appears 0% of the time on a snake base and partly appears on a lizard base.
   This directly confirms R1's "bearing structure" finding.
2. **But "partial success" is the ceiling**: `eagle talons` is a **composite part** (claws + yellow scaly tarsus + black),
   and the model only picked up the "long curved claws" layer. To hold completely, the composite part may need to be split up and written separately,
   or the engine switched to Qwen to suppress the lizard-foot features with true negatives.
3. **Tiger paws did not work**: the same kind of predicament as "cat paws"—the foot form is already occupied by the base (the lizard's foot shape),
   and the transplant can only change the **shape** (the curvature of the claws), not the **material** (scales and pads).

---

## 4. Takeaways

64. **Composite parts must be split up and written separately**: `eagle talons` actually contains three layers—claw form / tarsus colour and scaliness / the black of the claws—
    and the model executed only the most conspicuous layer (claw form). Either split it into several separate clauses, or switch to an engine that has negatives.
65. **Changing the base is the solution to "the part has nowhere to grow"**, and it is cheap: the same transplant part goes from 0% to partial success on a suitable base.
