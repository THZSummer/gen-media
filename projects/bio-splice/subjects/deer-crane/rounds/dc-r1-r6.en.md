# dc-R1–R6 · Five periods plus a two-version control (where the finding comes from: vacating a slot is ineffective on canonical structures)

> 🌐 Language: **English** | [中文](dc-r1-r6.md)

> Back to [sub-theme home](../README.en.md) ｜ Review reports: [r1](dc-r1-review.en.md) · [r2](dc-r2-review.en.md) · [r3](dc-r3-review.en.md) · [r4](dc-r4-review.en.md) · [r5](dc-r5-review.en.md) · [r6](dc-r6-review.en.md)
> Engine: Z-Image-Turbo　steps 12　**seed 7101 / 7102**　Output: [`work/deer-crane/r1..r6/`](../../../work/deer-crane/)
> ℹ️ Every round includes a **same-round base control** (`base-deer`; Rule 76: one base per round)

---

## 1. Six-round plan

| Round | Period | Presentation | Part | Base |
|----|----|------|------|------|
| R1 | 01 The long-necked deer | Morning-mist bamboo grove · soft light · eye level 400mm · square | G1 crane neck | neck not described |
| R2 | 02 The crane-legged deer | Shallow-water marsh · morning light · full body at eye level · square | G2 crane legs | **legs not described** (vacated version)|
| R3 | Control round for 02 | Same as above | G2 crane legs | **still describes four long legs** (occupied version)|
| R4 | 03 The crane-tailed deer | Reed marsh · backlight · eye level 600mm · square | G6 crane tail feathers | tail not described |
| R5 | 04 Neck and legs together | Frosty-morning grassland · cool light · eye level · landscape | G1+G2 | legs not described |
| R6 | 05 Deer and crane in spring (finale) | Spring plum grove · soft diffused light · wide-angle · landscape banner | G1+G2+G6 | legs and tail not described |

## 2. Results

| Round | Camera | Score | Verdict |
|----|------|------|------|
| R1 | `deer-craneneck` / `-b` | 4.25 / 4.25 | ✅ Final (partial) |
| R2 | `deer-cranelegs` / `-b` | 4.25 / 4.25 | ✅ Final (partial) |
| R3 | `deer-cranelegs` (occupied version) | 4.25 | Control: **same score, same phenomenon** as the vacated version |
| R4 | `deer-cranetait` / `-b` | **5.00** / 3.35 ❌ | Only seed 7101 succeeded |
| R5 | `deer-neck-legs` / `-b` | 4.25 / 4.25 | ✅ Final (partial) |
| R6 | `deer-crane-3parts` / `-b` | 4.25 / 4.25 | ✅ Final (partial) |

## 3. Two conclusions

### 1. Vacating a slot is neither effective nor harmful for **canonical structures** (R2 vs R3)

The same part (the crane's slender legs), the same seed, the same presentation — only **whether the base describes the legs** is changed:

| Base | Result |
|------|------|
| Legs not described (vacated) | The deer's legs are filled back in by the model itself; the crane-leg sentence makes the legs **thinner and longer** (4.25) |
| Still describes `four long legs` (occupied) | **Almost identical**: the legs likewise become slender and long (4.25) |

→ What decides success is **material** (brown fur + hooves vs. gray-black slender legs), not the vacated slot.
This is the same pattern as the "claws" of dragon-nines, the "cat paws" of cat-eagle, and the "fish fins" of fish-bird:
**Canonical structures can have their shape changed, but not their material.**

### 2. The tail feathers are the only piece that "reads at a glance as a transplant"

G6's white feather fan is **a different shape** from the deer's body, so it reads; whereas the neck and legs share the deer's own neck and leg shape, and after the edit it is still "a slender deer". → When choosing donors, **prefer parts of a different shape**.

## 4. Takeaways

89. **Canonical structures can have their shape changed but not their material**; vacating a slot neither helps nor hurts for them.
90. **An empty slot is a necessary condition, not a sufficient one** — the distinctiveness of the donor part also matters (see [dc-r7.md](dc-r7.en.md)).
91. **The donor priority narrows further: different shape > same shape.**
