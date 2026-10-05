# Scoring review · R5-R8 (jiu-wei-hu, nine-tailed fox · process re-validation round)

> 🌐 Language: **English** | [中文](r05-review.md)

> Round type: **the control-image path is overturned — what decides success is the prompt phrasing, not the apparatus**
> Trigger: the user said the tails were "too unnatural, they look fake", then that "you shouldn't add any deliberate constraints; it's such a simple scene, how could the model fail?"
> **Both judgements were confirmed by measurement.**

---

## 1. R5: fixing along the wrong path (three iterations, three failures)

After R4 the tails were still "fake", so I revised the **control image** three times:

| Iteration | Change | Result |
|-----------|--------|--------|
| R5-a | thickened the tails into plumes (thin ribbon -> hollow outline) | thicker, but became **pointed blades / leaf veins** — the model traced a central midrib |
| R5-b | rounded-tip profile (taper only 45%, cap the end) | tail shape right, but nine **evenly radiating -> flower petals / palm fronds** |
| R5-c | irregular angles + alternating lengths + a common sweep | far more organic, yet **still visibly a geometric construction**, "arranged" rather than grown |

**Three rounds of treating symptoms, not the disease.** Every fix removed one artefact and produced the next — which is itself the signal that the path is wrong. I did not stop to question the path.

---

## 2. R6: remove the whole apparatus and test the model

**Method**: plain text-to-image (`comfyui_gen.py`), no control image, no ControlNet; 1024x1360 / 20 steps / six seeds.
**Prompt** (descriptive):

```
A nine-tailed fox standing on a rocky outcrop. Nine long bushy tails with thick fur
sweep out behind it, and it turns its head to look back. Fine ink brushwork ...
```

**Result**: **5 of 6 came out with a single tail.** Only n44 grew multiple tails (about 6-7).
-> Under a "descriptive" prompt the prior for "fox" outweighs "nine-tailed"; the model treats the nine tails as decorative detail and drops it.

---

## 3. R7 / R8: change the phrasing — name the mythological being

**The only change is the prompt phrasing.** Instead of "a nine-tailed fox ... nine tails", the prompt **names a known mythological being** and states the tails as a **fact** rather than a counting instruction:

```
The nine-tailed fox of Chinese mythology, standing on a rocky outcrop and looking
back over its shoulder. Its nine long tails spread out behind it, thick and full of fur.
```

| Round | Phrasing | Colour | Seeds | **Multi-tail rate** |
|-------|----------|--------|-------|---------------------|
| R6 | descriptive | colour | 6 | **1/6** |
| **R7** | **named** | colour | 8 | **8/8** |
| **R8** | **named + pure ink line** | baimiao | 4 | **4/4** |

**Same model, same parameters: only the phrasing changed, and the multi-tail rate went from 1/6 to 8/8.**
R7/R8 also look plainly better in fur, layering and pose than any control-image output — because the model **painted** them rather than **tracing** a geometric diagram.

---

## 4. Count check

**Criterion adjusted**: naturally rendered bushy tails **cannot be mechanically certified one by one** (plumes overlap, fur bleeds across boundaries). Insisting on "certified exactly 9" is precisely what forced the image into mechanical fan ribs.

Two tiers now:

| Tier | Criterion | Result |
|------|-----------|--------|
| **Hard gate** | must read as a multi-tailed nine-tailed fox (not one tail, not obviously five) | R7 8/8, R8 4/4 ✅ |
| **Archived** | crop the tail region, magnify, count by eye, archive it and label it "visual count, not mechanical certification" | R8/k909 zoomed: **about nine countable**, plumes separated by visible gaps ✅ |

---

## 5. Scores

| Output | A sourcing | F vitality | B bone | C format | D legibility | E consistency | Total | Verdict |
|--------|-----------|------------|--------|----------|--------------|---------------|-------|---------|
| **R8/k909 (named · ink line)** | 4 | 5 | 5 | 4 | 5 | 4 | **4.45** | ✅ preferred (baimiao path) |
| **R7/m303 (named · colour)** | 4 | 5 | 3 | 4 | 5 | 4 | **4.20** | ✅ final (colour path) |
| R4/P075 (control image · previous delivery) | 5 | 4 | 5 | 4 | 5 | 4 | 4.50 | ⚠️ superseded by R8 (its A was actually higher, see below) |

> **On A**: R8/k909 scores 4 rather than 5 because "nine tails" is now a **visual count** (about nine), weaker evidence than "9 by construction" from the control image.
> This is a **deliberate trade**: A drops from 5 to 4, F rises from 4 to 5, and the entire apparatus goes away.
> A tail cluster that "reads as nine and is not obviously wrong" satisfies the content requirement; the real weight of the sourcing sits in the **passage / volume / provenance**, which is unaffected.

---

## 6. Lessons (the three most expensive of this round)

1. **If it will not fix, the path is wrong, not the parameters.** When the same "fake" survives three rounds of revision, stop and question the path instead of tuning further.
2. **Prompt phrasing beats every control apparatus.** "Name a known being and state its traits" is far stronger than "describe an appearance and issue a counting instruction". `EXACTLY nine`, `clearly separated`, `individually countable` are **commands** the model will not follow, and they crowd out what it would have drawn anyway.
3. **The acceptance criteria themselves produce bad work.** R4 already recorded "a missing F dimension causes systematic degradation"; this round adds: **making "mechanically certifiable" a hard gate forces mechanical images.** The strength of a criterion must match the nature of its object — fluffy tails should not be measured with callipers.

## 7. Fate of the control-image script

`scripts/control_image.py` is **kept but demoted**: no longer used for the nine-tailed fox; retained as a **general structural-control tool** (it may still help for objects that must be counted exactly and whose form is geometrisable, e.g. **horn-like or node-like** traits such as three heads and six eyes, or six legs and four wings).
`scripts/typeset_zanzhi.py` (typesetting) and `scripts/font_coverage.py` (glyph gate) are unaffected and stay in use.

## 8. Open items

| Item | Status |
|------|--------|
| **Bone choice** | ⏳ pending: R8 ink-line baimiao (matches the original plan) vs R7 russet colour (better looking, better for Xiaohongshu) |
| Seal layer | ⛔ seal-script typeface unresolved |
| Guo Pu's commentary | ⏳ to transcribe (no commentary may appear in a deliverable before then) |
