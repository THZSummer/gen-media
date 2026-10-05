# R8 · The Nine Resemblances largely achieved (originally planned: camel head D2 + rabbit eyes D3) — **both parts failed**

> 🌐 Language: **English** | [中文](dn-r8.md)

> Back to [sub-theme home page](../README.en.md) ｜ Review report: [dn-r8-review.md](dn-r8-review.en.md) ｜ Final see [dn-r10](dn-r10.en.md)
> Engine: Z-Image-Turbo　1024²　steps 12　**all 4 images share seed 4201**
> Artifacts: [`work/dragon-nines/r8/`](../../../work/dragon-nines/r8/)　`unapplied` all empty

---

## 1. Design: first correcting a misjudgement in the plan

PLAN recorded D3 rabbit eyes as "empty-slot addition → easy to achieve". **This was a misjudgement at planning time**:
the base `FULL_SNAKE` explicitly wrote `dark lidless eyes`, so the eye slot was already occupied.
So D3 is in fact in the same "**free the slot**" category as D6 scales.

So this round freed both the **head shape** and the **eyes** at once, making a 2×2 ablation:

| Shot | Base | Part | What is tested |
|------|------|------|--------|
| `base-snake-open` | head+eyes freed | — | control |
| `snake-camelhead` | head+eyes freed | D2 camel head | whether the camel head can land on its own |
| `snake-rabbiteyes` | head+eyes freed | D3 rabbit eyes | whether the rabbit eyes can land on their own |
| `dragon-head-eyes` | head+eyes freed | D2 + D3 | whether two parts in the same region squeeze each other out |

The base differs from the original text **only by deleting three descriptions** (head shape, eyes, `its head raised` → `its neck lifted`), with not one other character changed.

This round also changed `_styled()` in passing: a new `frame` parameter. Because this period is a **face-on close-up** period,
if the CN framing sentence is still 「全身像」 while the photographic layer writes `tight close-up`, the two sentences fight each other.

## 2. Results: all four images are the same snake

| Shot | A | Total | Verdict |
|------|---|---|------|
| `snake-camelhead` | 1 | 3.35 | ❌ transplant not in place |
| `snake-rabbiteyes` | 1 | 3.35 | ❌ transplant not in place |
| `dragon-head-eyes` | 1 | 3.35 | ❌ transplant not in place |

- **Camel head 0% present**; the head is still a cobra-style blunt head
- **Rabbit eyes 0% present**; the eyes are still snake eyes
- among the four images there is only slight posture drift; **the transplant sentence is a no-op**

It is worth noting more: after freeing the slots the image became **more "snake"** than the original (the model filled in neck folds).
That is, the freed positions **were not taken over by the transplant parts but filled back in by the model's own species prior**.

> ⚠️ The objective metrics **failed once again** this round: region diffs for head 11.6–15.9, all far above the 1.5
> "no-op" threshold, yet not one part landed—the diff comes from posture drift.
> This is yet another example of "region diff is only a **one-way** alarm": **region unchanged → definitely did not land;
> region changed → tells you nothing**, and visual confirmation is required.

## 3. Takeaways

73. **Freeing the slot is not a master key**: it works only for parts where "the base prior is weak" (R5's claws,
    R6's scales both changed); when it meets a part like the **head** with a very strong prior, the freed slot is filled back in by the model's
    own species prior.
74. **Head parts and limb parts are not the same class of problem**: limb parts can be solved by swapping the base (R2);
    head parts cannot be swapped away—they are the species identity itself.
