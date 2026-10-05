# ts-R1 / ts-R2 · Single-part exploration and following up on the coiling phrasing

> 🌐 Language: **English** | [中文](ts-r1-r2.md)

> Back to [sub-theme home](../README.en.md) ｜ review reports: [ts-r1](ts-r1-review.en.md) · [ts-r2](ts-r2-review.en.md)
> Engine: Z-Image-Turbo　1024²　steps 12　**all seed 5101**　outputs: [`work/turtle-snake/r1..r2/`](../../../work/turtle-snake/)
> ℹ️ `work/` is not committed to the repo (fixed seed allows pixel-exact reproduction)

---

## 1. R1: testing both the single parts and the combinations in one go

Base = **turtle**, and the description **deliberately omits the neck's length and the tail** (freeing up slots, Rule 66).
The pose sentence only says "it climbs from the water onto a stream stone, facing the camera head-on" — **no mention of neck, no mention of tail** (Rule 79).

| Camera | Part | Result | Score |
|------|------|------|------|
| `base-turtle` | — (control) | A normal turtle, no long neck, no tail | — |
| `turtle-snakeneck` | N1 snake neck | ✅ **fully holds up**: a long, curved neck extends from the shell opening, fine scales all the way to the lower jaw | **5.00** |
| `turtle-snaketail` | N2 snake tail | ✅ holds up: a long tail extends from behind the shell with a scale row, but on the stream stone it **tilted up too high** | 4.35 |
| `turtle-coil` | N3 coiling body | ❌ **did not appear at all** | 3.35 (A=1) |
| `turtle-neck-tail` | N1+N2 | ✅ both places hold up at once | 4.55 |

**What should have landed did not**: N3 was arranged per Rule 67 as an "add into an empty slot", which should have been the easiest to land, yet it landed 0%.

## 2. R2: one test per phrasing, all three landed

Switched to a **side-high view** (only from a high angle can you see coiling on the shell surface), but **without the low-camera portrait format** (the pitfall of Rule 80):

| Camera | Phrasing | Result | Score |
|------|------|------|------|
| `coil-rim` | `thick snake coils around the rim of its shell` | ✅ an arc rests on the shell rim | 4.55 |
| `coil-ground` | `a thick snake's body coiled on the stones beneath it, its coils visible on both sides` | ✅ coiled on the stone surface along the left side of the shell | **4.70** |
| `coil-min` | `thick snake coils around its shell` | ✅ the coiling relationship holds up (shortest and most stable) | **4.70** |

→ **R1's failure was a phrasing problem, not a slot problem.**

## 3. Takeaways

81. **Spatial relative clauses fail, switch to noun phrases**:
    `X wrapped around Y` (relative clause + long modifier) is not executed;
    `X coils around Y` (noun phrase + verb) lands.
    This extends Rule 69 (compound parts must be written separately) — **the relationship between the part and the base must also be written plainly**.
82. **When something "should have landed but did not", suspect the phrasing first, the slot second**:
    N3 in this sub-theme is the first counterexample — ranked in the "easiest" tier by mechanism, it actually failed completely because of sentence structure.
    (This points opposite to dragon-nines' "freeing up a slot fails": that was a mechanism boundary, this is a phrasing problem.)
