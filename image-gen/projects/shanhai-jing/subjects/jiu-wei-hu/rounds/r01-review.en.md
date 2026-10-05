# Scoring review · R1 (jiu-wei-hu, nine-tailed fox)

> 🌐 Language: **English** | [中文](r01-review.md)

> Engine: `zimage` (Z-Image-Turbo)　Round type: **craft validation round (not a finals round)**
> Base control: **none** (no finals this round, so no control; finals rounds must add one)
> Dimensions: A sourcing accuracy .30 ｜ B bone purity .20 ｜ C format completeness .20 ｜ D legibility .15 ｜ E series consistency .15
> Thresholds: non-empty `fatal` / A<3 / C<3 -> fail; total >=4.0 with A>=4 -> preferred final; >=3.5 -> final
> Purpose: validate the two premises "baimiao bone" and "countable traits controllable"; **no finals produced**

---

## 1. Round setup

| Item | Value |
|------|-------|
| Size | 768x1024 (3:4) |
| Steps | 12 |
| Seeds | 101 / 202 / 303 / 404 / 505 / 606 |
| Control | prompt only (no ControlNet) |
| Prompt highlights | baimiao ink line, aged paper, centred with margin; **`EXACTLY nine tails`**, plus nine tails separated from each other, fully in frame, individually countable |
| Output | `work/shanhai-jing/jiu-wei-hu/r01/` (intermediate, not committed) |
| Contact sheet | `sheet.jpg` in the same directory |

---

## 2. Recount (the project's most critical acceptance item)

**Method**: view the whole image, then `ffmpeg crop+scale` the countable region to 2x and count each tail.
**Result**: ❌ **not one of the six can be certified as "exactly 9".**

| Shot | seed | Whole-image estimate | 2x zoom check | Verdict |
|------|------|----------------------|---------------|---------|
| `s101` | 101 | about 7-8 | not zoomed individually | ❌ count not certifiable |
| `s202` | 202 | about 7-8 | not zoomed individually | ❌ count not certifiable |
| `s303` | 303 | about 7-8 | not zoomed individually | ❌ count not certifiable |
| `s404` | 404 | about 7-8 | not zoomed individually | ❌ count not certifiable |
| `s505` | 505 | about 6-7 (narrow fan) | not zoomed individually | ❌ count not certifiable |
| `s606` | 606 | about 8 | **zoomed 2x (`s606-tails-zoom.png`): tails overlap and the feathery rendering blurs boundaries; still estimated at 8-9** | ❌ count not certifiable |

> FATAL: a countable trait that cannot be certified does not match the source text's "nine tails". None enters the final set.
>
> Note: only `s606` was zoom-checked; the other five were already uncountable before zooming, and that alone is disqualifying, so no further review time was spent on them.

---

## 3. Item-by-item conclusions

### The three that hold

- **B bone purity**: all six are unmistakably baimiao ink line — even thin strokes, no impasto, no ink wash, no Western print hatching; consistent aged paper and margins. This is **highly stable across seeds** and can serve as the series baseline.
- **C format completeness**: upright composition, generous margins, no stray elements occupying space; suitable for typesetting a cartouche and a source card later.
- **E series consistency**: line density, paper tone and subject scale are consistent across the six, showing that **changing the seed under one prompt does not drift the style** — a key advantage for a serial.

### The two that fail

- **A sourcing accuracy (`fatal`)**: the prompt said `EXACTLY nine tails` and **not one of the six got it right**. The model has no reliable control over countable attributes, and the tail count drifts randomly between 6 and 9.
- **Model stays on brief**: the probe round (`work/shanhai-probe/`) measured that despite `monochrome` / `no colour`, it **added orange to the fox's ears**; the version asked for a vermilion seal produced a **seal with garbled glyphs** plus a stray red dot.

---

## 4. What this round settles (written into PLAN.md)

1. **The baimiao bone is settled**: no further style validation is needed; v3 baimiao plus aged paper is the series baseline.
2. **Countable traits need structural control**: the prompt route's rejection rate this round was **6/6 = 100%**, unusable for a serial.
3. **Two iron rules**: the model does not write (a garbled seal is a hard defect); the model does not count (ControlNet or a human recount is mandatory).
4. **Cover vs inner plate**: woodblock print (probe v1/v2) for covers, baimiao for inner plates — both hold, but **never mixed**.

---

## 5. Next step (decision pending)

Two options for structural control, see [PLAN.en.md](../../../PLAN.en.md) section 3 "open decision on structural control":

- **A Large-sample screening**: sweep 40-60, zoom and count each, keep the true nines. Low cost, medium evidence strength.
- **B Programmatic control image**: script draws 9 clearly separated strokes -> Canny -> ControlNet. High cost, **every image guaranteed 9**, reproducible.

> No finals this round, so **no A-E total** (item A is already `fatal`; a total would be meaningless).
