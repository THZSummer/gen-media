# R4 · Dragon assembled — stacking the workable parts onto one individual (finale)

> 🌐 Language: **English** | [中文](dn-r4.md)

> Back to the [sub-theme home page](../README.en.md) ｜ Review report: [dn-r4-review.md](dn-r4-review.en.md)
> Engine: Z-Image-Turbo　1024²　steps 12　**all 3 images share seed 4201**
> Outputs: [`work/dragon-nines/r4/`](../../../work/dragon-nines/r4/)　`unapplied` all empty

---

## 1. Design

Up to R3, the workable parts among the Nine Resemblances are: **antlers D1 (head), ears D9 (head), claws D7 (forelimbs), paws D8 (hindlimbs)**.
This round stacks them onto the same individual, while **deliberately pressing against the region boundary of Rule 59**:

| Variant | Stacked parts | Region distribution |
|------|--------|----------|
| `dragon-3parts` | antlers + claws + paws | head 1 · forelimbs 1 · hindlimbs 1 |
| `dragon-4parts` | antlers + ears + claws + paws | **head 2** · forelimbs 1 · hindlimbs 1 (the head is exactly at the ceiling) |

The base reuses R2's lizard (it has limbs and **does not describe claws**).

## 2. Results

| Shot | Per-part result | Score |
|------|----------|------|
| `dragon-3parts` | antlers ✅ complete · claws ⚠️ partial · paws ❌ did not hold | **4.40** ✅ final |
| `dragon-4parts` | antlers ✅ · ears ✅ · claws ⚠️ · paws ❌ | **4.70** ✅ preferred |

**"Dragon assembled" holds**: the lizard grows a complete pair of forked deer antlers (the 4-part version also has pointed furry ox ears),
reading as a dragon-like creature rather than a collage.

## 3. Two confirmations

### 1. The region ceiling still holds with 4 parts stacked (Rule 59 confirmed again)

`dragon-4parts` puts all four parts on (head 2 + forelimbs 1 + hindlimbs 1), and **no "extra individual drawn" appeared**.
Against the counter-example in cat-eagle's fifth period (the same region had to carry three parts → the model drew another individual),
this shows that **"at most 2 in the same region" can be used directly as a design rule**: when laying out, count regions first, not the total.

### 2. The difference between limb parts on a snake base vs a lizard base is decisive

The same D7 eagle claws:

| Base | Result |
|------|------|
| snake (R1) | appears **0%** of the time—no forelimbs, so the claws have nowhere to grow |
| lizard (R2 / R4) | appears **partly**—the claw form goes from short and blunt to long curved raptor-style |

This is a **repeatable confirmation** of the "bearing structure" finding (r1 takeaway 62): changing the base is a low-cost solution.

---

## 4. Takeaways

68. **"At most 2 in the same region" can be used directly as a design rule**: 4 parts stacked (head 2 + one each on fore- and hindlimbs) holds,
    showing that the independent variable of the constraint is the **region distribution**, not the number of parts. When laying out a subject, count how many parts go in each region first.
69. **The correct order for assembling the dragon is "verify single parts first, then stack"**: D1/D9 were each verified in R1,
    D7 was verified in R2, and R4 merely arranges them into non-conflicting regions, succeeding at the first try.
    The other way round (stacking 4 parts from the start) makes failure impossible to attribute.
