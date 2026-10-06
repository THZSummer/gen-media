# Score review · R1–R3 (lu-shu 鹿蜀 · pinning down the prompt wording + the seal problem)

> 🌐 Language: **English** | [中文](r01-review.md)

> Nature of these rounds: **the three opening rounds of a new sub-topic** — ① a wording sweep (which prompt
> lands all four traits: horse body / white head / tiger markings / red tail), ② convergence (confine the red,
> retry Chinese), ③ seal suppression (can a prompt stop the model from stamping its own fake seals).
> Engine: Z-Image-Turbo | canvas 1024×1360 / 20 steps | the style sentence is **byte-identical** to the R7 jiu-wei-hu final.
> Round archives: `work/shanhai-jing/lu-shu/r0{1,2,3}/` (`round-rNN-z-image-turbo.json` + `requests.jsonl`)

---

## 1. The source text (text first, images second)

Base edition: Guo Pu's annotated *Shan Hai Jing*, vol. 1 · Nan Shan Jing
([識典古籍 SK2098](https://www.shidianguji.com/zh/book/SK2098/chapter/1m12x7ij5mwp6), checked 2026-10-06).

```
又東三百七十里曰杻陽之山。其陽多赤金，其陰多白金。有獸焉，其狀如馬而白首，
其文如虎而赤尾，其音如謡，其名曰鹿蜀，佩之宜子孫。
```

| Item | Treatment |
|------|-----------|
| Verbatim check | Word-for-word identical to the "verified source text" table in [PLAN.md](../../../PLAN.en.md) §2 (variant character 「謡」 kept, punctuation untouched) |
| Excerpt boundary | In the base edition this passage is immediately followed by 「怪水出焉……其名曰旋龜……」, which describes **another** creature of the same mountain → the quotation stops at the lu-shu sentence; nothing is skipped and no ellipsis is inserted |
| Guo Pu commentary | ⏳ still not transcribed → **no commentary may appear in any deliverable** (standing project rule) |
| Verifiable traits | horse body / white head / tiger markings (其文如虎) / red tail — every one of them must land to earn a full A score |

---

## 2. R1 wording sweep (3 variants × 3 seeds)

| Variant | Wording | Representative sentence |
|---------|---------|-------------------------|
| v1 | English naming + inline traits | `The lu-shu of Chinese mythology, a white-headed horse with tiger stripes on its body and a red tail …` |
| v2 | English, traits first, itemised | `A horse of Chinese mythology with a pure white head, a body covered in black tiger stripes and a long cinnabar-red tail; it is called the lu-shu …` |
| v3 | Chinese direct description | `《山海經》中的異獸鹿蜀：馬的身子、白色的頭、虎一樣的斑紋、赤紅的尾巴……` |

Results (all 9 images inspected; a trait counts only if it can be **pointed at** in the picture):

| Variant | Horse body | White head | Tiger markings | Red tail | Extra problems |
|---------|-----------|-----------|----------------|----------|----------------|
| **v1** | 3/3 | 3/3 | **3/3 (soft)** | 3/3 | none (mane colour normal) |
| v2 | 3/3 | 3/3 | **3/3 (bold)** | 3/3 | 2/3 **added a red mane** (an addition absent from the source) |
| v3 | 3/3 | 1/3 | **0/3 (drawn as spots)** | 3/3 | 3/3 red mane; coat drifts brown; ochre oversaturated, the pale-colour feel is lost |

**Conclusion**: `虎紋` (tiger markings) can only be obtained in **English**; the Chinese direct description drops it
to spots and skews the coat colour. This points the same way as the jiu-wei-hu R7/R8 result: **the wording of the
prompt decides the outcome**, not the canvas or the step count.

---

## 3. R2 convergence round (only two variables moved)

| Variant | Difference from R1 | Result |
|---------|--------------------|--------|
| v4 | = v2 reused verbatim (seeds 404/505/606) | tiger markings / white head / red tail 3/3; used to measure seed variance |
| v5 | v2 + `only its long tail is cinnabar red, its mane and legs stay white` | **confining the red works**: 3/3 lost the red mane, kept the red tail, white legs and mane ✅ |
| v6 | Chinese rewrite (same structure as v2: itemised traits + red tail only) | still 3/3 red mane + spots (tiger markings fail) → **the Chinese route is disproved a second time** |

**Conclusion**: `v5` is the best wording for the shape description (all four traits, no extra additions); the
Chinese route failed 6/6 across two rounds and is not pursued further.

---

## 4. R3 seal-suppression round: a prompt cannot stop the fake seals

Background: **of 20 images spot-checked (five R1 images with all four corners, six R2 and nine R3 images with the
two bottom corners), only R1 v1-101 is clean** — every other one carries red seals or pseudo-characters in the
paper margins. R3 tried three "no seals / no writing" wordings, three seeds each, to see whether a prompt can
suppress it:

| Variant | Suppression clause | Result |
|---------|--------------------|--------|
| w1 | `There is no red seal, no stamp and no writing anywhere in the painting.` | bottom-corner check: w1-707 red seal, w1-808 clear red seal, w1-909 faint red seal |
| w2 | `The paper stays blank: do not paint seals, stamps, calligraphy or any characters.` | w2-707 faint seal, **w2-808 clear red seal with pseudo-characters**, w2-909 faint seal |
| w3 | `without seal or inscription` | w3-707 faint pseudo-characters, w3-808 red dot / small seal, **w3-909 red seal + pseudo-characters** |

Not one of the nine has both bottom corners as clean as v1-101.

**Conclusion**: the same lesson as R5 — **telling the model what *not* to draw simply does not take effect**.
This style sentence (`traditional Chinese album leaf … aged paper`) carries a **seal prior** (real album leaves
almost always have seals), and no prompt-level phrasing suppresses it.

### Automatic seal detection: three attempts, three failures (kept as a record)

Trying to decide "is there a fake seal" mechanically, three criteria were tested and all of them fail:

| Criterion | Idea | Measured counter-example |
|-----------|------|--------------------------|
| Cinnabar clusters in the margin band (`seal_check.py`) | seals sit in corners; count red pixel clusters | **Misses**: v5-404's faint red seal falls below the threshold. **False positives**: the ochre ground/rock warm tones are counted as seals |
| Fraction of paper around the cluster | a seal is stamped on paper, so it should be surrounded by paper | The paper itself has a vignette gradient, so the "paper" test collapses (around the real seal in v2-202 the paper fraction was only 0.18) |
| Ink fraction in the ring | a seal is separate from the subject, so no ink should be near it | The opposite holds: a real seal next to the ground ink measured 0.48, while fur areas measured 0 |
| Stroke ratio (perimeter/area) | a seal is thin strokes, a tail is a solid mass | Real seals contain solid strokes: 0.14 versus 0.13 for a tail — inseparable |

→ The final workflow is **a human reads the coordinates + a tool does the erasing**: the reviewer reads the seal
box from a 4× zoom, hands it to `scripts/patch_region.py`, which covers it with a clean piece of paper from the
*same* image (deterministic, with self-checks), and the manifest records `seal_erasure` truthfully.

> ⚠️ **The tool itself had a trap (fixed)**: its self-check counted the post-erasure cinnabar pixels inside a
> region **inset by the feather**, and when a box was smaller than 2×feather that core degenerated to 1×4 pixels —
> so **a failed erasure was reported as OK**. That is exactly what happened to the bottom-left of v5-404
> (749 → 307 pixels yet judged "pass"). Fix: the feather must be ≤ a quarter of the box's short side and the core
> must be at least 3×3, otherwise the tool errors out; the seam metric also changed from "inner-vs-outer median"
> to "median brightness difference between adjacent pixels across the boundary" (the former misread the
> painting's own tonal gradient as a seam — measured false alarm of 49).

---

## 5. Scores (A–F, weights in [PLAN.md](../../../PLAN.en.md) §5)

| Work | A research | F spirit | B brushwork | C format | D legibility | E consistency | Total | Verdict |
|------|-----------|----------|-------------|----------|--------------|---------------|-------|---------|
| **R1 v1-101 (first choice)** | 4 | 5 | 5 | 4 | 5 | 5 | **4.60** | ✅ final |
| R2 v5-404 (strongest shape) | 5 | 5 | 5 | 4 | 5 | 5 | 4.75 | ⛔ **fatal: fake seals in the corners** |
| R2 v4-404 | 4 | 4 | 5 | 4 | 5 | 5 | 4.45 | ⛔ same (two corners sealed) |
| R3 w1-707 | 4 | 4 | 5 | 4 | 5 | 5 | 4.45 | ⛔ same |
| R1 v3-101 (Chinese description) | 2 | 3 | 3 | 4 | 4 | 4 | 3.10 | ⛔ tiger markings fail, brushwork drifts |

**Why the first choice is not the prettiest image**: v5-404 has the best tiger markings, but its four corners
carry fake seals, which is `fatal` under the project's hard threshold; v1-101 lands all four traits and its four
corners were **confirmed free of seals and characters at 4× zoom**. It scores 4.60 with A=4 and F=5.
This is a **deliberate trade**: one notch of tiger-stripe strength in exchange for dropping the
"model writes garbled characters" defect.

---

## 6. Takeaways (the four most expensive lessons)

1. **Chinese direct description loses to English naming** (6 straight failures): Z-Image's text encoder is a
   Qwen3-4B, but a rare name like 鹿蜀 plus a Chinese trait sentence degrades into "a horse with spots"; English
   naming plus itemised traits is what lands.
2. **"Do not draw X" does not work** (9 images in R3). Suppressing seals requires **changing the style wording**
   (breaking the "album leaf" prior) or **erasing with a tool** — never a negative clause.
3. **The strength of a criterion must match its object** (third time this lesson appears): four different
   mechanical criteria for seals all fail — in an ochre-coloured painting, "the red of a seal" and "the warm tone
   of rock or fur" are **inseparable at pixel level**. Admitting that and moving to
   "mechanical shortlist + human reads coordinates + tool executes + self-check" is more honest than shipping a
   classifier that both over- and under-fires.
4. **A tool's self-check can lie too**: the eraser reported failure as success because its measurement region had
   degenerated. The **measurement domain must match the action domain** — once the feather eats the whole box, the
   residue cannot be measured inside the box.

---

## 7. Open items

| Item | Status |
|------|--------|
| Seals | ⚠️ Z-Image hits **19 of 20 spot-checked images** in this style (4 of 5 in R1, all 6 in R2, all 9 in R3); the already-shipped jiu-wei-hu R7 final also has faint red seals in its corners — decision pending: regenerate, or erase with `patch_region.py` |
| Seal layer (a real seal-script stamp) | ⛔ still blocked on a seal-script CJK font (see [PLAN.md](../../../PLAN.en.md) §3) |
| Guo Pu commentary | ⏳ awaiting transcription; until then no commentary appears in deliverables |
| Style wording | ⏳ next sub-topic may try wordings that **rewrite the prior**, e.g. "a single unmounted sheet of raw paper" instead of "album leaf" |
