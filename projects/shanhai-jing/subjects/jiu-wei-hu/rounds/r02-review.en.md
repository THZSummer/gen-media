# Scoring review · R2 (jiu-wei-hu, nine-tailed fox)

> 🌐 Language: **English** | [中文](r02-review.md)

> Engine: `z-image-turbo-fun-controlnet`
> Round type: **structural-control validation round -> a preferred plate produced** (typesetting layer pending)
> Base control: the structural control image is this round's control (`period-01/controls/nine-tails-control.png`); a biological base control does not apply
> Dimensions: A sourcing accuracy .30 ｜ B bone purity .20 ｜ C format completeness .20 ｜ D legibility .15 ｜ E series consistency .15
> Thresholds: non-empty `fatal` / A<3 / C<3 -> fail; total >=4.0 with A>=4 -> preferred final; >=3.5 -> final
> **Purpose: test whether "programmatic control image + ControlNet" can lock the count that R1 lost control of**

---

## 1. Round setup

| Item | Value |
|------|-------|
| Control image | produced by `scripts/control_image.py` (9 tails guaranteed by construction, min gap 31.52px, no ink touching the border) |
| Size | 864x1152 (follows the control image, 3:4) |
| Steps / seed | 12 / 7 |
| Variable | `--control-strength` = 0.65 / 0.80 / 0.95 (single variable, everything else identical) |
| Output | `work/shanhai-jing/jiu-wei-hu/r02/` (intermediate, not committed) |
| Contact sheet | `sheet-r02.jpg` in the same directory |

---

## 2. Recount (this round's pass/fail criterion)

**Method**: crop the whole tail fan (540x820) -> magnify 1.5x -> count one by one, anticlockwise from the lower left.

| Shot | Control strength | Recount | Verdict |
|------|------------------|---------|---------|
| `cs065` | 0.65 | **not zoom-checked** (its bone already fails, see below) | ❌ count not certified |
| `cs080` | 0.80 | ✅ **zoomed and checked: 1...9, exactly nine**, all springing from the tail root and separated | ✅ count certified |
| `cs095` | 0.95 | ✅ **zoomed and checked: 1...9, exactly nine**, all springing from the tail root and separated | ✅ **count certified (preferred)** |

> Compared with R1: the prompt route scored 0/6; the programmatic control-image route scores 2/2. Counting has moved from "gambling on the model" to "guaranteed by construction plus a human certificate".

---

## 3. Scores

| Shot | A sourcing | B bone | C format | D legibility | E consistency | Total | Verdict |
|------|-----------|--------|----------|--------------|---------------|-------|---------|
| `cs095` | 5 | 5 | 3 | 5 | 4 | **4.45** | ✅ **preferred plate** (re-score C after typesetting) |
| `cs080` | 5 | 4 | 3 | 5 | 4 | **4.25** | final (second choice) |
| `cs065` | — | 3 | — | 5 | — | — | ❌ fail (count uncertified + bone impure) |

> `cs065`'s A item is **`fatal` outright** under this project's thresholds: an uncertifiable count does not match the source text's "nine tails", so the remaining dimensions need not be scored (same criterion as R1).

### Item-by-item notes

#### `cs095` — ✅ preferred plate (total 4.45)
- 👍 **A sourcing 5/5**: both clauses of 其狀如狐而九尾 land — an unmistakable fox, and nine tails certified by counting
- 👍 **B bone 5/5**: pure baimiao fine line, no hatching, no wash, no impasto; even aged paper
- 👍 **D legibility 5/5**: reads as a fox at a glance, with the tail count prominent
- 👎 **C format 3/5**: **cartouche, frame, source text and seal are not yet overlaid**, so the illustrated-verse format is incomplete -> C must be re-scored after typesetting
- 👎 **E consistency 4/5**: consistent with R1's baimiao language, but one plate is too small a sample to judge series stability
- ⚠️ **Structural cost**: the nine tails form an **evenly spaced, mechanical fan** — a direct consequence of the control image. Countability was bought with naturalness; see below.

#### `cs080` — final (second choice) (total 4.25)
- 👍 count certified, baimiao holds, same origin as cs095 (same seed, only control strength differs)
- 👎 **stray hatching** on the hind leg and haunch; baimiao purity below cs095

#### `cs065` — ❌ fail
- 👍 the skeleton clearly follows the control image
- 👎 **bone drifts**: tonal hatching appears and the language slides from baimiao toward copperplate engraving — at too low a control strength the model improvises and the style escapes
- ⛔ **fatal**: count uncertified

---

## 4. What this round settles (written into [PLAN.en.md](../../../PLAN.en.md))

1. **Path B is validated**: the programmatic control image plus ControlNet turns "nine tails" from R1's 0/6 into a certifiable 2/2. Counting no longer depends on the prompt.
2. **Control strength 0.95**: 0.95 gives the purest bone; 0.80 lets the model add stray hatching; 0.65 slides straight into copperplate engraving. **Control strength is the first gate on bone purity.**
3. **⚠️ A cost to face squarely: countability was bought with naturalness.** cs095's nine tails are evenly spaced with identical curvature and read as mechanical. Future improvement (without losing countability):
   - perturb the control image's **lengths and bows** with deterministic pseudo-randomness (fixed seed, still reproducible)
   - keep the hard constraint that **the tips stay pairwise separated**; perturb only the mid-sections
4. **Typeface setback (open)**: `LXGWSeal` measures only **375 codepoints** and barely covers regular CJK (九 is present, 尾 and 狐 are missing and render as substitution boxes) -> **the typeface is unusable for the seal**. The checking tool is `scripts/font_coverage.py`; the alternative typeface (JFZSKSealScript V3.5) is blocked by the network, so the typesetting layer is on hold.

---

## 5. Next steps

1. **Typesetting**: overlay cartouche (creature name) + volume + source passage + seal -> re-score C -> publish a layout proof
2. **Seal**: resolve the seal-script typeface (another mirror / another typeface / fall back to a serif face with a clear note)
3. **Control-image perturbation**: remove the mechanical feel without breaking the separability of the nine tails
