# fb-R1–R5 · Underwater total failure → landing out of water (where the habitat hard constraint comes from)

> 🌐 Language: **English** | [中文](fb-r1-r5.md)

> Back to [sub-theme home](../README.en.md) ｜ review reports: [r1](fb-r1-review.en.md) · [r2](fb-r2-review.en.md) · [r3](fb-r3-review.en.md) · [r4](fb-r4-review.en.md) · [r5](fb-r5-review.en.md)
> Engine: Z-Image-Turbo　1024²　steps 12　**all seed 6101**　outputs: [`work/fish-bird/r1..r5/`](../../../work/fish-bird/)
> ℹ️ `work/` is not committed to the repo (fixed seed allows pixel-exact reproduction)

---

## 1. R1–R3: underwater, three phrasings + three positions, total failure (7 images)

| Round | Probe | Result |
|----|------|------|
| R1 | wings written at the body side / at the flank / as "replacing the pectoral fin" (relative clause) | ❌ 0% ×3 |
| R2 | tail feathers (tail position) / tail feathers (relative clause) | ❌ 0% ×2 |
| R3 | wings **growing from the back** / tail feathers **spreading above the tail** / feathers covering the back | ❌ 0% ×3 |

R3 followed the "add into an empty slot" idea (both the `wing-atlas` rewrite and cat-eagle's neck feathers succeeded with it),
**and it was likewise 0% underwater** — only then did we realize the problem was not position, phrasing, or slot reservation.

## 2. R4–R5: only moving the scene above the water surface

| Round | Camera | Scene | Result |
|----|------|------|------|
| R4 | `fish-wings-back` | out of water | ✅ **5.00** |
| R4 | `fish-wings` | out of water | ✅ **5.00** |
| R4 | `fish-feathercoat` | out of water | ❌ 0% |
| R5 | `fish-wings-tail` | out of water | ✅ 4.70 (wings landed, tail feathers did not) |
| R5 | `fish-tail` / `fish-tail-above` / `fish-feathercoat` | out of water | ❌ 0% ×3 |

**Same sentence, same base, same seed, the only difference is the scene — the dividing line between 0% and 100%.**

## 3. The R7 surprise: compatibility is judged by region

In period 02's "half out of water" scene:

| Phrasing | Result |
|------|------|
| `broad feathered bird wings on both sides of its body` (body side, below the waterline) | ❌ eaten by the scene |
| `a pair of broad feathered bird wings half-opened along its flanks` (half-opened, positioned higher, breaking the surface) | ✅ landed |

→ Within the same frame, **the exposed part can grow an appendage, the part soaking in water cannot**.

## 4. Takeaways

85. **Habitat is a hard constraint**: when the transplanted part conflicts semantically with the scene, the model **keeps the scene and drops the part**.
    "Feathers/wings underwater" is a semantic contradiction, and the model would rather turn the transplant sentence into a no-op.
    → **Choose a compatible habitat first, then talk about phrasing and slot reservation**: this ranks ahead of phrasing discipline.
86. **Scene compatibility is judged by region**: it applies region by region within the same frame.
87. **Canonical structures cannot free up a slot**: fish fins, cat paws, and snake scales get restored by the model even when their descriptions are deleted
    (in exact contrast to the turtle's neck and tail, completing the tiering of Rule 83).

### Appendix: process lessons (self-assessment written into the sub-theme README)

The 11 images from the first 3 rounds could have been saved — **the first round of a new sub-theme should start with a minimal probe testing "scene × part semantic compatibility"**:
one image per candidate habitat with the same sentence. Only after hitting Rule 85 do you move on to debugging phrasing and slot reservation.
