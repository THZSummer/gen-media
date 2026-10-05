# R5–R7 · Giving each "period" its own character (the final rounds)

> 🌐 Language: **English** | [中文](dn-r5-r7.md)

> Back to [sub-theme home page](../README.en.md) ｜ Review reports: [dn-r5](dn-r5-review.en.md) · [dn-r6](dn-r6-review.en.md) · [dn-r7](dn-r7-review.en.md)
> Engine: Z-Image-Turbo　steps 12　**all seed 4201**　Artifacts: [`work/dragon-nines/r5..r7/`](../../../work/dragon-nines/)
> ℹ️ `work/` is not committed to the repo (a fixed seed makes it reproducible pixel by pixel)

---

## 1. Problem: the four periods differed only in "which part was swapped"

In R1–R4 the four periods had **exactly the same habitat / light / camera / canvas**, and only the transplant part changed.
So the four periods read like "the same photograph with different parts added"—**they had no identity of their own**.

Root cause: I **misapplied the discipline of the within-period control** (layer constancy) **across periods**.

## 2. Principle: constant within a period, varied between periods

| Scope | Requirement | Why |
|------|------|--------|
| **Within a period** | habitat / light / camera / canvas **must be constant** | ensures that period's "transplant vs base control" is comparable (same seed + same skeleton, the only variable being the transplant part) |
| **Between periods** | these four **should differ** | gives each period its own identity; otherwise the whole set looks like the same image |

**The series constant layer** has only two items, used to keep the two sub-themes still able to be juxtaposed as one set:
1. The CN framing sentence (`全身像，一只动物独自占据画面：`)
2. The base of realistic wildlife photography (`Wildlife photograph … no digital sharpening`)

## 3. Period style table (choose the camera by subject, not at random)

| Period | Theme | What the subject should show | Habitat | Light/weather | Camera/focal length | Canvas |
|----|------|--------------|------|-----------|-----------|------|
| 01 | Snake with horns | Deer antlers | Misty-morning reed wetland | Overcast soft light | Eye level 600mm | Square 1024² |
| 02 | Lizard with claws | **Claws** | **Pebble riverbank after rain** | **Wet side-backlight** | **Low camera hugging the ground 85mm, focused on the front feet** | **Portrait 1024×1280** |
| 03 | Snake with fish scales | **Scales** | **Leaf litter in the undergrowth** | **Dappled forest light** | **Side-high body-hugging 100mm macro** | Square 1024² |
| 04 | Assembling the dragon | Overall presence | **Rain-soaked rocky high ground** | **Dusk backlight + streaks of rain** | **Wide-angle low camera 35mm** | **Landscape 1280×1024** |

> The camera positions of Periods 02/03 **aim straight at their weaknesses**: the parts in these two periods (claws, scales) only reached "partially in place" in R2/R3,
> and that "partial" was largely a **readability problem**—pointing the lens at the subject both gave the period an identity and made the part readable.

## 4. Results: with the camera changed to the right one, the weak points were made up too

| Period | Part | R2/R3 original version | **R5/R6 final version** |
|----|------|-----------|------------------|
| 02 | Eagle claws | 3.90 / 4.05 (partial) | **4.55 / 4.40** |
| 03 | Fish scales | 4.10 / 4.55 (partial and hard to read) | **4.55 / 5.00** (after the side-high body-hugging view the difference is obvious at a glance) |
| 04 | Assembling the dragon | 4.40 / 4.70 | **4.40 / 4.70** (antlers/ears silhouetted against the skylight, far more presence than the original) |

It is not that the parts got better, but that **the way of looking at them got right**.

## 5. The mechanism conclusions still hold as before

R5–R7 changed only the presentation layer, **with not one character changed in the base or the transplant part**, so all the mechanism conclusions from R1–R4 remain valid:
bearing structure (Takeaway 62), freeing the slot (66), part-selection priority (67), ≤2 per region (68).

> R1–R4 are therefore positioned as **mechanism-verification rounds** (the images stay in work/, cited by the individual round records),
> while R5–R7 are the **final rounds of the four periods** (the finals go into the period directories).

---

## 6. Takeaways

70. **"Layer constancy" is a within-period discipline, not an across-period one**: apply it across periods and the deliverable reads as "the same image with different accessories".
    The correct division of labour is **constant within a period (to preserve the control) + varied between periods (to give identity)**; the series constant layer keeps only the framing sentence and the photographic base.
71. **The camera must be chosen by subject, and preferably aimed at the weak point first**: pointing the lens at a part that only reached "partially in place"
    often solves both **identity** and **readability** at once (Period 02's claws and Period 03's scales both went from "hard to read" to "obvious at a glance").
72. **The premise for a redo final not affecting the mechanism conclusions is "changing only the presentation layer"**: with not one character changed in the base or the transplant part,
    the mechanism conclusions, scoring dimensions and thresholds all remain valid, and the old rounds need only be downgraded to "mechanism-verification rounds".
