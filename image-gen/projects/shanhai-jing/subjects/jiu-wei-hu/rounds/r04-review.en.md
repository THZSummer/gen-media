# Scoring review · R4 (jiu-wei-hu, nine-tailed fox · rework round)

> 🌐 Language: **English** | [中文](r04-review.md)

> Engine: `z-image-turbo-fun-controlnet`
> Round type: **rework round — overturns R2/R3's final selection**
> Trigger: the user said the delivered plate was "the simplest, the ugliest" and suspected `work/` held better images. **On review, that judgement holds.**
> Dimensions (revised this round): A sourcing accuracy .25 ｜ **F vitality of brushwork .25 (new)** ｜ B bone purity .15 ｜ C format completeness .15 ｜ D legibility .10 ｜ E series consistency .10
> Thresholds: `fatal` / A<3 / **F<3** / C<3 -> fail; total >=4.0 with A>=4 and **F>=4** -> preferred final

---

## 1. Confirming the problem

Tiling the nine candidates side by side made it plain:

| Candidate | Beauty | Count |
|-----------|--------|-------|
| Probe v1 / v2 (woodcut) | strong (forceful black masses) | ❌ wrong |
| Probe v3 | good (soft fine line + rock) | ❌ wrong |
| R1 `s606` and friends | **good (feathery tails + fur brushwork)** | ❌ wrong |
| R2 `cs080` / `cs095` | **poor (hollow thin line + fan-rib spacing)** | ✅ right |
| **R2 `cs095` (delivered)** | **the worst of the set** | ✅ right |

**Conclusion: the delivered cs095 is the ugliest of the batch. The user was right.**

---

## 2. Root cause (a failure of method, not luck)

1. **The acceptance table lacked a dimension.** The old A-E were all correctness/consistency and **not one measured beauty**. So "bland but countable" scored 4.65 while "beautiful but uncountable" went straight to `fatal`/zero. **The rubric pushed the selection to the ugliest solution.**
2. **The prompt forbade texture.** The old prompt said `uniform thin weight` / `no hatching` / `restrained` — an instruction not to render texture at all.
3. **Then that instruction became the yardstick.** `cs065` was visibly richer than `cs095`, yet I judged it "bone drifted" — **measuring with a ruler that bans hatching guarantees a verdict of "violation"**. Circular reasoning.
4. **I picked the extreme of a single variable.** Control strength 0.95 = maximum control = minimum model contribution = maximum blandness.
5. **The control image itself was too thin.** Tails were drawn as 11px ribbons; Canny locked that in and the model only dared draw hollow outlines -> "thin noodles". (Found this round.)

---

## 3. Corrections applied

| # | Fix | Result |
|---|-----|--------|
| 1 | **Added dimension F (vitality of brushwork) at weight .25**, tied with sourcing as the joint highest, plus `F<3 -> fail` | see [PLAN.en.md](../../../PLAN.en.md) section 5 |
| 2 | **De-mechanised the control image**: deterministic per-tail jitter of angle/length/bow/width; added a low rocky base | `control-organic.png` |
| 3 | **Thickened the control tails** (half-width roughly 11px -> 26px) into plumes; widened the fan to 48°-206°; relaxed the disentangle radius to 0.26 | `control-plume.png`, min gap 15.83px |
| 4 | **Automatic seed selection**: scan seeds from the base until one satisfies both "min gap >= 13.8px" and "no ink on the border" | seed 20261006 (base +1), reproducible |
| 5 | **Rewrote the prompt to demand texture**: thick plumes, dense fine hair strokes, layered chest ruff and tails | prompt archived below |
| 6 | **Lowered control strength** into 0.45-0.75 and re-swept | P045 / P060 / P075 / Q060 |

---

## 4. Recount (still never skipped)

| Shot | Control strength | Prompt | Recount | Verdict |
|------|------------------|--------|---------|---------|
| `P045` | 0.45 | pure line | fur halos bleed across tails, **still uncountable when magnified** | ❌ not certifiable |
| `P060` | 0.60 | pure line | not zoom-checked (P075 already qualified) | — |
| `P075` | 0.75 | pure line | ✅ **tip region cropped and magnified 2x: 6 blades clockwise from the upper left + 3 lower-left = exactly 9** | ✅ **certified** |
| `Q060` | 0.60 | line + wash | not zoom-checked (P075 already qualified) | — |

> The most important finding of this round: **countability and beauty are not zero-sum; what matters is where the fur goes.**
> `P045` spreads fur over the whole tail -> boundaries blur and counting fails.
> `P075` concentrates fur **into a mass at the tail root** and leaves the blades as clean elongated shapes -> **both beautiful and countable**. That is the real methodological gain here.

---

## 5. Scores (new rubric)

| Output | A sourcing | **F vitality** | B bone | C format | D legibility | E consistency | Total | Verdict |
|--------|-----------|----------------|--------|----------|--------------|---------------|-------|---------|
| **R4/P075 (new delivery)** | 5 | 4 | 5 | 4 | 5 | 4 | **4.50** | ✅ **preferred final** |
| R2/cs095 (old delivery, re-scored) | 5 | **2** | 5 | 4 | 5 | 4 | 4.00 | ❌ **fail** (F<3) |

> **The old delivery fails under the new rubric** — not for self-flagellation, but as evidence that the old rubric would let undeliverable work through.

### P075 item by item

- 👍 **A 5/5**: nine tails certified by counting; unmistakably a fox; passage and volume traceable verbatim
- 👍 **F 4/5**: fine fur brushwork, an ink mass at the tail root, clean blades, a rocky base, an alert natural pose.
  **Not full marks**: the blades carry a slight "grass-blade" feel and the tails could be fluffier; the torso silhouette is still constrained by the control image and reads a little stiff
- 👍 **B 5/5**: pure baimiao ink line, not ink wash or Western hatching
- 👎 **C 4/5**: the seal layer is still missing
- 👍 **D 5/5**: instantly legible, with a prominent tail count
- ➖ **E 4/5**: still a single-creature sample

### Final prompt (archived)

```
Chinese baimiao fine-brush ink painting, pure line work with rich fur texture.
A fox standing in full profile facing right, with exactly nine long tails fanned out
behind it, clearly separated from one another. Every tail is a THICK tapering plume
of long feathery fur, drawn with many fine hair strokes along its length — dense and
broad near the base, thinning to a fine point. The body is covered in soft fur
rendered as fine short strokes; the chest ruff and the tail plumes are thick and
layered. It stands on a low rocky outcrop drawn with a few crisp angular ink strokes.
Monochrome black ink on pale aged rice paper, no colour. Generous empty margins,
classical Chinese painting album leaf.
```
Parameters: `--control-strength 0.75 --steps 14 --seed 7`, control image `controls/nine-tails-control-plume.png`.

---

## 6. What this round settles

1. **Whatever dimension the acceptance table lacks is the dimension the work systematically degrades along.** Adding the dimension matters more than fiddling with the prompt — the most expensive lesson of this round.
2. **The control image's thickness sets the ceiling on the render's texture**: thin ribbon -> hollow outline; thick plume -> furry tail. A control image does not "only fix structure"; it fixes the texture budget too.
3. **Where the fur sits is the dial between countability and beauty**: spread everywhere -> blur; concentrated at the root -> both at once.
4. **Re-read prohibitive words in your own prompt**: once `no hatching` / `uniform` / `restrained` is written, it becomes the ruler you later judge images with.

## 7. Open items

| Item | Status |
|------|--------|
| Seal layer | ⛔ seal-script typeface unresolved |
| Guo Pu's commentary | ⏳ to transcribe (no commentary may appear in a deliverable before then) |
| Blades' "grass-blade" feel | ⏳ can be tuned further via prompt (fluffiness) and the torso silhouette (control-image pose) |
