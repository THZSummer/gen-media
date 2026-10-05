# R9 · Follow-up: **the base's species noun is itself a slot**

> 🌐 Language: **English** | [中文](dn-r9.md)

> Back to [sub-theme home page](../README.en.md) ｜ Review report: [dn-r9-review.md](dn-r9-review.en.md) ｜ Previous round: [dn-r8](dn-r8.en.md)
> Engine: Z-Image-Turbo　1024²　steps 12　**all 5 images share seed 4201**
> Artifacts: [`work/dragon-nines/r9/`](../../../work/dragon-nines/r9/)　`unapplied` all empty

---

## 1. Hypothesis

In R8 "freeing the slot" failed. So why did the image become **more snake** after freeing it?
One explanation is: the source of the slot is **not only the words describing that part**, but also **the base's species noun itself**.
The `snake` in `a large wild snake …` carries the whole snake prior (including head shape, including eyes),
and as long as that word is still there, no matter how cleanly the head is freed it will be filled back in.

This is the **mirror image** of Rule 57 (what is dangerous is **naming the whole**):

| Side | Phenomenon | Known/to be tested |
|----|------|-----------|
| Donor side | `whose body is entirely a deer's` → drags out a whole deer | known (Rule 57) |
| **Base side** | `a snake …` → drags out the entire canonical form of a snake | **tested this round** |

Test method: the base **does not name the species at all**, describing only the observable parts:

```
a long muscular low body with keeled scales and a flickering forked tongue
```

(and asserting that `snake` / `lizard` / `head` / `eye` do not appear in it)

## 2. Results: the hypothesis holds, but the conclusion is **reversed**

| Shot | Base | Transplant part | Result |
|------|------|--------|------|
| `base-nospecies` | no species name | — | a scaled reptile (an iguana/snake hybrid)—**the prior weakened but did not disappear** |
| `nospecies-camelhead` | no species name | D2 camel head | **a whole camel was dragged out**, the base destroyed |
| `nospecies-camelhead-eye` | no species name | D2 + D3 | same as above, still a whole camel (scales remain on the side of the neck) |

**The base species noun is both a "slot" and an "anchor"**:

- keep it → the transplant part is suppressed (R8: camel head 0%)
- delete it → the donor **does not just take over one part, but takes over the whole animal** (R9: a whole camel)

So **head parts are a two-way dead end on zimage**, and transplants of the kind `head whole-noun slot` should
be **downgraded to "expected to fail, not a final target"** in the planning of all sub-themes.

## 3. The other half of the same round: usable combinations for Period 05 (no same-round control at the time)

This round also produced two usable combinations in passing (`snake-antler-oxear` / `snake-antler-oxear-scale`),
both scored 5.00, but **the base they used is not the same as the same-round control `base-nospecies`**—
by project discipline, the objective metrics are not usable for these two. **The next round, R10, added the same-round control and made them finals.**

> This step is worth remembering: when a round contains several bases, the "same-round control" is valid only for **shots sharing its base**.
> A round with mixed bases must either be split into separate rounds or explicitly note whose objective metrics are unusable.

## 4. Takeaways

75. **The base's species noun is both a "slot" and an "anchor"**: deleting it does not make the transplant part land more easily,
    it only lets the donor take over the whole individual. **Head parts (head swap/beak swap/face swap) must not be written into the planning targets.**
76. **When a round mixes multiple bases, the same-round control is valid only for shots with the same base**;
    shots with different bases must get their control in a separate round, otherwise the objective metrics are unusable.
