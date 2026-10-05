# Period 03 · The Fish-Scaled Snake

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/dn-r6-review.en.md)
> Engine: Z-Image-Turbo　1024×1024　steps 12　**all 3 images share seed 4201**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Characteristics

**Forest-floor leaf litter · dappled forest light · side-high body-hugging angle, scale rows filling the frame · square 1024²**

This period's camera is **aimed at the "scales"**: the snake lays its body flat with the whole spine facing the lens,
and then a side-high angle and deeper depth of field make the **scale rows the frame's dominant texture**.
R3's problem that "a same-material swap (scales for scales) is inherently hard to read" becomes **recognizable at a glance** under the side-high body-hugging angle:
the baseline is fine granular scales, while after the transplant they are large overlapping rows (score 4.10→4.55; the one with antlers 4.55→5.00).

## 2. This Period's Theme

The Nine Resemblances' **scales like a fish (D6)** — this is the **only "already occupied" part** among the Nine Resemblances:
the snake has scales of its own, and Period 01's base description explicitly wrote `keeled scales along a long muscular body`.
Per rule 56, the transplant gets overridden by the base description.

**Countermeasure: delete the words in the base that describe that part, and free up the slot.**

```
R1 底座：... a blunt scaled head, ..., keeled scales along a long muscular body
R3 底座：... a blunt head,        ..., and a long smooth muscular body   ← 腾出鳞的占位
```

This is **the same technique** as Period 02 deliberately not writing `clawed` on the lizard base.
The base differs from R1 in this one place only, so the attribution is clear.

| Part | ID | Result |
|------|------|------|
| Fish scales | D6 | ⚠️ **Partly holds**: the body scales change from the baseline's fine scales into **larger, more regular, mutually overlapping** scale rows |
| Deer antlers + fish scales | D1+D6 | ⚠️ Same as above; the antlers fully hold and the two sites do not interfere with each other |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-snake-fishscale.png`](01-snake-fishscale.png) | D6 | **4.55** ✅ preferred | `1e2c96ad` | `1eb1737cff` |
| 2 | [`02-snake-antler-fishscale.png`](02-snake-antler-fishscale.png) | D1+D6 (**main image**) | **5.00** ✅ preferred | `e3738ba6` | `8e5c5b4eb3` |

Control: [`controls/snake-clean.png`](controls/snake-clean.png) — the pure-snake base **with the scale slot already freed** (same round, same seed).

> ⚠️ As in Period 02: **this period's finals "partly hold"**, and the document states this honestly.

## 4. Why Only "Partly", and One Difficulty in Reading

1. `large overlapping fish scales` is likewise a **composite part**: scale size + arrangement (overlapping like tiles)
   + the fan-shaped edge / iridescence specific to fish scales. The model executed the first two layers, not the third.
2. **Harder to read**: the control baseline also has scales of its own, so this transplant is a **same-material swap** rather than **adding into an empty slot**.
   Compared with Period 01's "horns" (the snake has no horns at all), the difference is inherently subtler,
   which is also why E (concept readability) can only be given 3 — someone unfamiliar with the project will not easily see that these are "fish scales".

> **Conclusion**: adding into an empty slot > adding after freeing a slot > adding into an occupied slot.
> When choosing a subject, if two parts are similar in difficulty, prefer the **part the base does not have at all**.

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject dragon-nines 6 --dry
python3 run_round.py --subject dragon-nines 3
python3 score.py --round work/dragon-nines/r6/round.json --scores work/dragon-nines/r6/scores.json \
    --control base-snake-clean --region head=430,120,380,260 --region body=430,500,400,380 \
    --audit-sheet subjects/dragon-nines/rounds/dn-r6-audit.jpg \
    -o subjects/dragon-nines/rounds/dn-r6-review.md
python3 curate.py --period subjects/dragon-nines/period-03 --from work/dragon-nines/r6/round.json \
    --pick snake-fishscale=01-snake-fishscale \
    --pick snake-fishscale-antler=02-snake-antler-fishscale \
    --control base-snake-clean=controls/snake-clean --note "…" --force
bash make_sheet.sh period subjects/dragon-nines/period-03
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-04 | v0.1 | Period 03 delivery: fish scales / deer antlers + fish scales, 2 images in total (partly hold, stated honestly) | 小七 |
