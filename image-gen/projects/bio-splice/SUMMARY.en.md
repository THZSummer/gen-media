# Bio Splice · Full Project Summary

> 🌐 Language: **English** | [中文](SUMMARY.md)

> Back to the [project home page](README.en.md) ｜ [full project plan](PLAN.en.md)

**Delivery: 12 sub-themes × 5 periods = 60 periods, 135 finals, 60 period contact sheets, 12 sub-theme contact sheets.**
Every final was judged ✅ by `score.py` before entering a period directory through `curate.py`, without exception.

---

## 1. Deliverables List

| Sub-theme | Group | Periods | Finals | Controls | Mean | Contact sheet | Status |
|--------|----|----|------|------|------|------|------|
| [cat-eagle](subjects/cat-eagle/README.en.md) cat + eagle | A | 5 | 14 | 6 | 4.35 | [`sheet.jpg`](subjects/cat-eagle/sheet.jpg) | ✅ |
| [dragon-nines](subjects/dragon-nines/README.en.md) dragon · nine resemblances | A | 5 | 10 | 5 | 4.24 | [`sheet.jpg`](subjects/dragon-nines/sheet.jpg) | ✅ |
| [turtle-snake](subjects/turtle-snake/README.en.md) turtle + snake (Black Tortoise) | A | 5 | 13 | 5 | 4.74 | [`sheet.jpg`](subjects/turtle-snake/sheet.jpg) | ✅ |
| [fish-bird](subjects/fish-bird/README.en.md) fish + bird (kun-peng) | A | 5 | 11 | 5 | 4.22 | [`sheet.jpg`](subjects/fish-bird/sheet.jpg) | ✅ |
| [deer-crane](subjects/deer-crane/README.en.md) deer + crane | A | 5 | 9 | 5 | 4.16 | [`sheet.jpg`](subjects/deer-crane/sheet.jpg) | ✅ |
| [lichen](subjects/lichen/README.en.md) lichen = fungus + alga | B | 5 | 11 | 5 | 4.84 | [`sheet.jpg`](subjects/lichen/sheet.jpg) | ✅ |
| [cordyceps](subjects/cordyceps/README.en.md) cordyceps = fungus + insect | B | 5 | 11 | 5 | 4.80 | [`sheet.jpg`](subjects/cordyceps/sheet.jpg) | ✅ |
| [flytrap-fang](subjects/flytrap-fang/README.en.md) Venus flytrap + animal organs | B | 5 | 11 | 5 | 4.90 | [`sheet.jpg`](subjects/flytrap-fang/sheet.jpg) | ✅ |
| [flower-bird](subjects/flower-bird/README.en.md) flower + bird | B | 5 | 12 | 5 | 4.62 | [`sheet.jpg`](subjects/flower-bird/sheet.jpg) | ✅ |
| [tree-beast](subjects/tree-beast/README.en.md) tree + beast | B | 5 | 11 | 5 | 4.59 | [`sheet.jpg`](subjects/tree-beast/sheet.jpg) | ✅ |
| [wing-atlas](subjects/wing-atlas/README.en.md) wing · atlas | C | 5 | 11 | 4 | 4.72 | [`sheet.jpg`](subjects/wing-atlas/sheet.jpg) | ✅ |
| [horn-atlas](subjects/horn-atlas/README.en.md) horn · atlas | C | 5 | 11 | 4 | **5.00** | [`sheet.jpg`](subjects/horn-atlas/sheet.jpg) | ✅ |
| **Total** | | **60** | **135** | 59 | | **72** | |

**Top three means**: `horn-atlas` 5.00 (zero failures), `flytrap-fang` 4.90, `lichen` 4.84.
**Bottom three means**: `deer-crane` 4.16, `fish-bird` 4.22, `dragon-nines` 4.24—all topics where the **donor and the base share the same shape** or that **need a canonical structure freed**.

---

## 2. Contact Sheet per Sub-theme (click a thumbnail to see the full image)

**Each contact sheet = that sub-theme's 5 periods, one row per period** (a row holds every final of that period, controls included).
For a **single period**'s large image, go to `subjects/<子主题>/period-NN/sheet.jpg`;
to regenerate all 72 contact sheets at once: `bash make_sheet.sh all`.

### Group A · cross-species (animal × animal)

| cat + eagle<br>5 periods / 14 finals | dragon · nine resemblances<br>5 periods / 10 finals | turtle + snake (Black Tortoise)<br>5 periods / 13 finals |
|---|---|---|
| [![cat-eagle](subjects/cat-eagle/sheet-thumb.jpg)](subjects/cat-eagle/sheet.jpg) | [![dragon-nines](subjects/dragon-nines/sheet-thumb.jpg)](subjects/dragon-nines/sheet.jpg) | [![turtle-snake](subjects/turtle-snake/sheet-thumb.jpg)](subjects/turtle-snake/sheet.jpg) |

| fish + bird (kun-peng)<br>5 periods / 11 finals | deer + crane (deer and crane in spring)<br>5 periods / 9 finals |  |
|---|---|---|
| [![fish-bird](subjects/fish-bird/sheet-thumb.jpg)](subjects/fish-bird/sheet.jpg) | [![deer-crane](subjects/deer-crane/sheet-thumb.jpg)](subjects/deer-crane/sheet.jpg) | |

### Group B · cross-kingdom splicing (animal × plant × fungus)

| lichen = fungus + alga<br>5 periods / 11 finals | cordyceps = fungus + insect<br>5 periods / 11 finals | Venus flytrap + animal organs<br>5 periods / 11 finals |
|---|---|---|
| [![lichen](subjects/lichen/sheet-thumb.jpg)](subjects/lichen/sheet.jpg) | [![cordyceps](subjects/cordyceps/sheet-thumb.jpg)](subjects/cordyceps/sheet.jpg) | [![flytrap-fang](subjects/flytrap-fang/sheet-thumb.jpg)](subjects/flytrap-fang/sheet.jpg) |

| flower + bird<br>5 periods / 12 finals | tree + beast<br>5 periods / 11 finals |  |
|---|---|---|
| [![flower-bird](subjects/flower-bird/sheet-thumb.jpg)](subjects/flower-bird/sheet.jpg) | [![tree-beast](subjects/tree-beast/sheet-thumb.jpg)](subjects/tree-beast/sheet.jpg) | |

### Group C · part atlas (rotating organs on one base)

| wing · atlas<br>5 parts / 11 finals | horn · atlas<br>5 parts / 11 finals |  |
|---|---|---|
| [![wing-atlas](subjects/wing-atlas/sheet-thumb.jpg)](subjects/wing-atlas/sheet.jpg) | [![horn-atlas](subjects/horn-atlas/sheet-thumb.jpg)](subjects/horn-atlas/sheet.jpg) | |

> The thumbnail is `sheet-thumb.jpg` (box resampling + JPEG, ~50–85KB);
> the full `sheet.jpg` is a 1568×2796 strip, **one row per period**.

## 3. Mechanism Findings Master Table (the core knowledge accumulated by this project)

> The numbering follows the numbers assigned during each sub-theme's measurements (51–110). The table below is re-ordered **by use**; it is the "user manual" for this mechanism set.

### A. Topic selection: first judge "can it land"

| No. | Finding |
|------|------|
| **92** | 🎯 **The base's morphological freedom determines transplant difficulty**: the more fixed (deer/fish) the harder, the more it resembles raw material (mycelium) the easier |
| **99** | 🎯 **The criterion rests on the "landing site", not the "whole"**: a fixed whole does not hinder the transplant, as long as the landing site itself is empty or merely an appendage attribute |
| **105** | 🎯 **Two independent thresholds**: ① is the landing site a canonical structure ② what bearing surface does this piece need—**both must be asked** |
| **107** | 🎯 **The donor's semantic category must match the landing site's function**: looking similar is not enough, **the semantics must be right** (fish fins vs flying-fish fins) |
| 83 / 87 / 89 | **Canonical structures can change shape, not material** (deer legs, fish fins, cat paws, snake scales, petals); deleting the description gets them restored anyway |
| 90 | An empty slot is a **necessary** condition, not a **sufficient** one; the donor piece's **recognizability** also matters |
| 91 | Donor priority: **different shape > same shape** |
| 110 | Form can **compensate** for a small semantic deviation (the narwhal's tusk is not a horn, but "a single upward spiral" was accepted) |

### B. Phrasing: how to write a sentence so it is executed

| No. | Finding |
|------|------|
| 56 / 66 | Transplant success depends first on **whether the base has a placeholder**; a placeholder can be **freed** |
| **96 / 100** | 🎯 **What can be freed is an "attribute" (body-surface texture, colour, boundary appendages); what cannot is a "structure" (organs, limbs)** |
| 57 | What is dangerous is **naming a whole as a noun** (`X's body`), not mentioning a species |
| 69 | Composite parts must be **written out separately** |
| **81** | 🎯 **Spatial-relation clauses fail; switch to a noun phrase**: `X wrapped around Y` is a no-op, `X coils around Y` is executed |
| 103 | The phrasing must be **read together with the landing site** (the same "covering form" works on the insect body surface and fails on petals) |
| 82 | When something "should have worked but did not", **suspect the phrasing first, the placeholder second** |

### C. Layout: how to place several pieces on one body

| No. | Finding |
|------|------|
| 59 / 68 | **At most two stacked in the same region**, cross-region stacking is allowed; the binding independent variable is the **regional distribution**, not the number of pieces |
| 74 / 97 | A part needs a **bearing structure**; **pieces growing from the body surface need no bearing structure** (horns, stromata, plumes) |
| 108 | **Atlas-type sub-themes need a "baseline part"** (part 1 holds no transplant piece, serving as the reference for the four later parts) |

### D. Presentation: camera, light, habitat, medium

| No. | Finding |
|------|------|
| 70 / 72 | **Constant within a period + different across periods**; changing only the presentation layer leaves the mechanism findings valid as before |
| **85 / 86** | 🎯 **Habitat is a hard constraint**: when a part conflicts with the scene's semantics, the model **keeps the scene and drops the part**; compatibility is also judged **per region** |
| **79** | A pose sentence must **stay silent** about the target part (whatever it mentions, the control grows it too) |
| **80** | The presentation layer **is not neutral**: camera/canvas change the transplant result |
| 93 | **Scale is part of the presentation layer too** (macro subjects require replacing the whole framing sentence and photography layer) |
| 94 | **Presentation can rescue a weak period** (a pseudo-section turned "algal layer" from the hardest into the best) |
| 98 | **Changing the presentation medium = a low-cost upgrade for the finale period** (ecological photo → specimen photo) |
| 95 | If the control already does half the work, **points must be deducted** |

### E. Process: how to work fast and stably

| No. | Finding |
|------|------|
| 76 | **Only one base per round** (a same-round control is valid only for shots with the same base) |
| 84 | **Multiple takes are a low-cost repeatability check** |
| 88 | A "single usable part" can carry a sub-theme too (use the **presentation layer's independent variable** as the between-period difference) |
| **102 / 106** | 🎯 **Changing the base requires re-validating the hit rate**; whether the hit rate drops **depends on the nature of the landing site** (attributes/empty faces are stable, geometrically sensitive ones are not) |
| **109** | 🎯 **Thresholds can be assembled on purpose**: align 99/97/96/107 all at once → zero failures (`horn-atlas`) |
| 51 note | **Judging must be done on local magnification**; thumbnails lie |

---

## 4. Negative-Results List (the ones that did not work—just as valuable)

| Sub-theme | Part | Result | Reason |
|--------|------|------|------|
| dragon-nines | D2 camel head / D3 rabbit eyes | **0%** | The base's species noun is **both a placeholder and an anchor**; swapping a head is a two-way dead end (73/75) |
| dragon-nines | D8 tiger paws | not successful | The foot form is occupied by the lizard: the claw shape can change, the foot pads cannot |
| fish-bird | bird tail feathers / bird feathers covering the body | **0%** | The tail slot is a **canonical structure**; feather covering is a same-material replacement |
| deer-crane | crest / beak / wings | not attempted | head parts (73), the deer has no wing base (74) |
| flower-bird | feathers replacing petals | **0%** | Petals are a canonical structure (all three phrasings wiped out) |
| tree-beast | beast feet | **0%** | The landing site is a structure + "feet" need joints (**both thresholds failed**) |
| wing-atlas | fish pectoral fins / maple seed wings | 0% / partial | **the semantic category does not match** (no flight semantics) |
| flytrap-fang | claws | not attempted | the Venus flytrap has no limbs (no bearing surface) |
| cat-eagle | eagle-headed cat (period-06) | scrapped | the head-swap direction is infeasible (73) |
| all | "eye"-type parts | not attempted | a small part + same-material replacement + the head-part family (the original `eye-atlas` was therefore rewritten as `horn-atlas`) |

---

## 5. Toolchain and Reproduction

```
projects/bio-splice/
├── PLAN.md / SUMMARY.md / README.md
├── run_round.py      entry point (--subject picks the sub-theme)
├── roundkit.py       shared machinery (run rounds / archive / prompt sentence splitting and line wrapping)
├── curate.py         final promotion work/ → period/, writes manifest.json
├── score.py          objective alarms + subjective five-dimension scoring; decides by threshold whether a shot can become a final
├── make_sheet.sh     merged sheets (round / period / subject / all)
└── subjects/<子主题>/{README.md, parts.md, rounds.py, rounds/, period-NN/}
```

```bash
# reproduce any period
python3 run_round.py --subject horn-atlas 2 --dry     # view the verbatim prompt
python3 run_round.py --subject horn-atlas 2           # generate (fixed seed)
python3 score.py --round work/horn-atlas/r2/round.json \
    --scores work/horn-atlas/r2/scores.json --control base-horse \
    --region head=350,80,400,400 --audit-sheet subjects/horn-atlas/rounds/ha-r2-audit.jpg \
    -o subjects/horn-atlas/rounds/ha-r2-review.md
python3 curate.py --period subjects/horn-atlas/period-02 \
    --from work/horn-atlas/r2/round.json --pick horse-antlers=01-horse-antlers \
    --control base-horse=controls/horse --note "…"
bash make_sheet.sh period subjects/horn-atlas/period-02
```

**Reproducibility**: every round has fixed seeds; measured that under the same prompt/seed/canvas the **decoded pixels are byte-for-byte identical**
(`work/` therefore does not enter the repo). Engine: Z-Image-Turbo (1024²/1280², steps 12, ~25 s/image).

---

## 6. Known Shortcomings and Follow-up Suggestions

1. **The presentation of `cat-eagle` periods 02–05** was redone after the fact (the original five periods shared one autumn meadow set),
   while four of `deer-crane`'s periods are "partial" and have still not been redone—**if redone, the suggestion is to change the landing site per rule 99**.
2. **`lichen` period 03 (fruticose lichen)**: the base branches on its own, so the transplant piece's marginal contribution is diluted by "the control already doing half the work",
   and the score of 4.55 is an honest deduction; to chase a full score, redo it with a non-branching base.
3. **Rule 101 (the seam decides credibility) is still a hypothesis**: the eye in `flytrap-fang` period 02 scores only 4.80 (no eyelid/eye socket);
   the hypothesis is that adding "socket/lid/seam" would raise the C score—**not yet verified**.
4. **Two things not done**: dragon-nines' D5 "belly like a shen" (a visual proxy must be defined first),
   and `tree-beast`'s "growth rings ↔ bone" (an internal structure, not done in this volume).
5. **Repository size**: this project is an image-heavy repo, and Gitee's quota is 1024MB;
   contact sheets / audit sheets already use JPEG, while finals and controls use PNG (JPEG introduces an average channel difference of ≈1.21 and eats the criterion),
   so **every 2–3 sub-themes advanced requires running Repository GC once on Gitee** (see section 9 of the project README).

---

## 7. One-Sentence Conclusion

**Whether "bio splice" can be pulled off does not depend on how strong the model is, but on whether the topic choice respects the priors it already has.**
Align "the landing site is an empty face, no bearing structure is needed, no placeholder needs freeing, the semantic category matches" all at once,
and you get zero failures like `horn-atlas`; fail any one of them and you get "partial success" like `deer-crane`.
**This project's 135 finals and 10 negative results together make up this criterion table.**

---

## Document Revision History

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-10-05 | v1.0 | Project-wide wrap-up summary: deliverables list for 60 periods / 135 finals, mechanism findings master table (51–110 re-ordered by use), negative-results list, toolchain and reproduction, known shortcomings | 小七 |
| 2026-10-05 | v1.1 | The deliverables list gained a direct "contact sheet" column; added a "contact sheet per sub-theme" section (12 thumbnails, click to see the full image, grouped A/B/C) | 小七 |
