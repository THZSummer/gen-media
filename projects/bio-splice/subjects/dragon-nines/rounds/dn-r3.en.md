# R3 · Fish scales (D6) — testing the "free the placeholder" technique

> 🌐 Language: **English** | [中文](dn-r3.md)

> Back to the [sub-theme home page](../README.en.md) ｜ Review report: [dn-r3-review.md](dn-r3-review.en.md)
> Engine: Z-Image-Turbo　1024²　steps 12　**all 3 images share seed 4201**
> Outputs: [`work/dragon-nines/r3/`](../../../work/dragon-nines/r3/)　`unapplied` all empty

---

## 1. Why this round deserved a round of its own

D6 "scales like a fish" is the **only already-occupied** part among the Nine Resemblances: the snake has scales of its own, and R1's base description
explicitly wrote `keeled scales along a long muscular body`. By Rule 56,
this kind of transplant part gets overridden by the base's own description (that is exactly how cat-eagle's "cat paws" failed).

**Hypothesis**: an occupied slot is not a dead end—**deleting the few words in the base that describe that part** frees it up.

The method (the only difference from R1's base is this one place, so attribution is clear):

```
R1 base: a blunt scaled head, ..., keeled scales along a long muscular body
R3 base: a blunt head,        ..., and a long smooth muscular body
```

## 2. Results

| Shot | Result | Score |
|------|------|------|
| `snake-fishscale` | ⚠️ partial: the body scales change from fine granular scales to **larger, more regular, mutually overlapping** scale rows | **4.10** ✅ final |
| `snake-fishscale-antler` | ⚠️ same as above + antlers D1 hold completely, the two do not interfere with each other | **4.55** ✅ preferred |

**The hypothesis holds**: after freeing the placeholder the transplant **did happen** (it was not tested on R1's original base,
but the "cat paws" control shows that it gets overridden in the occupied state).

## 3. But this part has a natural difficulty of interpretation

1. `large overlapping fish scales` is a **composite part**: the size of the scales / the arrangement (overlapping like roof tiles) /
   the fan-shaped edges and iridescence peculiar to fish scales. The model executed the first two layers.
2. **Harder to interpret**: the control baseline has scales of its own → this is a **same-material replacement**, not **adding into an empty slot**.
   Compared with R1's "antlers" (a snake has no antlers at all), the difference is naturally subtler.

So E (concept readable) was only given 3—someone who does not know this project will not easily see at a glance that those are "fish scales".

> **Priority finding**: **adding into an empty slot > adding after freeing the placeholder > adding into an occupied slot.**
> When two parts are of similar difficulty, prefer the **part the base does not have at all**.

---

## 4. Takeaways

66. **An "occupied slot" can be freed by deleting the base description**: remove the few words in the base that describe the target part,
    and the transplant part can land (this round's fish scales and R2's claws both use this technique).
    Rule 56 should therefore be read as "**whether the base description has a placeholder**", not "whether the base objectively has this part".
67. **Same-material replacement is harder to interpret than adding into an empty slot, and harder to score high**: both can hold,
    but the former (scales for scales) has a naturally subtle visual difference, so E (concept readable) will be low.
    Priority order for choosing subjects: **adding into an empty slot > freeing the placeholder > same-material replacement**.
