# Sub-theme: turtle + snake (Black Tortoise)

> 🌐 Language: **English** | [中文](README.md)

> Back to the [project home page](../../README.en.md) ｜ Part list in [`parts.md`](parts.en.md) ｜ Development records in [`rounds/`](rounds/)

> **Whole sub-theme overview sheet**: [`sheet.jpg`](sheet.jpg) —— one row per period, assembling that period's finals (reproducible with `bash make_sheet.sh subject turtle-snake`)

## 1. Concept: A Composite That **Already Exists**

**The "Black Tortoise" of the Four Symbols is a turtle-snake composite**—a composite in the classics (*Book of Rites*, *Chu Ci* and others speak of turtle and snake).
Unlike `cat-eagle` (taking apart one word) and `dragon-nines` (executing the ancients' part table),
this sub-theme's hook is **copying an existing figure**: the Black Tortoise is by nature one turtle and one snake coiled together.

**Base = turtle**; donors = the snake's **body parts**: neck N1 / tail N2 / coil N3 (+ scales N5 in reserve).
**No snake head**—head parts cannot be transplanted (rule 73, measured by dragon-nines' D2/D3).

## 2. Why This Sub-theme Is Mechanically Suitable

| Rule | Meaning for this sub-theme |
|------|------------------|
| 66 a placeholder can be **freed** | the turtle has a short neck and a small tail → the base deliberately does not write these two, freeing the positions for N1 / N2 |
| 67 **add into an empty slot > free a placeholder** | the coil N3 (the shell top is empty to begin with) should be the easiest to succeed—but in measurement what it fears is the phrasing, see below |
| 73 head parts cannot be transplanted | the Black Tortoise does only **neck / tail / coil**, no snake head |
| 79 a pose sentence must not mention the transplant piece | no pose sentence mentions "neck", "tail" or "coil" |
| 80 the presentation layer is not neutral | period 02 was **changed from PLAN's "low camera vertical" to eye-level full body**, avoiding the pitfall of a terminal part being individualized |

## 3. Core Finding: **Spatial-Relation Clauses Fail** (rule 81)

The N3 coil **did not appear at all** in the first round. It was not a placeholder problem but a phrasing problem:

| Phrasing | Result |
|------|------|
| ❌ `the thick coiled body of a large snake wrapped around its shell` | no-op |
| ✅ `thick snake coils around its shell` | lands (the shortest and most stable) |

> **A relative clause (`X wrapped around Y`) is not executed; a noun phrase (`X coils around Y`) is.**
> This is an extension of rule 69: not only must "composite parts be written out separately", **the spatial relation between the part and the base must be written plainly too**.

## 4. Constant Within a Period, Different Across Periods

| Period | Theme | Part | **Presentation (habitat · light · camera · canvas)** | Finals | Score |
|----|------|------|----------------------------------------|------|------|
| [period-01](period-01/README.en.md) | **Snake-necked turtle** | N1 snake neck ×3 takes | stream stones in the shallows · morning light · eye-level 600mm · square | 3 | 5.00 / 5.00 / 5.00 |
| [period-02](period-02/README.en.md) | **Snake-tailed turtle** | N2 snake tail ×3 takes | **wetland mud bank · overcast · eye-level full body 400mm · square** | 3 | 5.00 / 4.85 / 4.55 |
| [period-03](period-03/README.en.md) | **Coiled turtle** | N3 coil (three phrasings) | **old well stone platform · side light · side-high view 100mm · square** | 3 | 4.70 / 4.70 / 4.55 |
| [period-04](period-04/README.en.md) | **Neck and tail complete** | N1 + N2 | **post-rain stream stones · backlight · eye-level 400mm · landscape** | 2 | 5.00 / 5.00 |
| [period-05](period-05/README.en.md) | **Black Tortoise** (finale) | N1 + N2 + N3 | **dusk water surface · backlit silhouette · eye-level wide-angle 35mm · landscape** | 2 | 5.00 / 5.00 |

> The presentation of period 02 **differs from the original plan**: PLAN wrote "low camera on the ground · vertical",
> and because on cat-eagle "low camera vertical + a terminal part" had produced the problem of "dragging out the whole donor" (rule 80), it was changed to eye-level full body.

## 5. Sub-theme Summary (self-assessment after the finale)

### 1. Among the snake's body parts, everything doable was done

| Type | Part | Result |
|------|------|------|
| free a placeholder | N1 snake neck, N2 snake tail | ✅ **fully successful** (and reproducible with a different seed) |
| add into an empty slot | N3 coil | ✅ successful, but **phrasing-sensitive** (rule 81) |
| cross-region stacking | N1+N2, N1+N2+N3 | ✅ three pieces on one body and still a single individual |
| head parts | N4 snake head | ⛔ not attempted (rule 73) |

### 2. Two lessons contributed by this sub-theme

**（1）This is the first time "freeing a placeholder" fully succeeded.**
dragon-nines' freed placeholders (claws, scales) reached only "partial", so for a while freeing was thought inferior to an empty slot;
in this sub-theme N1/N2 both landed completely, showing that **whether freeing a placeholder works depends on how much the base depends on that part**:
the turtle's neck and tail **can be deleted from the description without hurting the base** (delete them and the turtle is still a turtle),
while a cat's paws and a snake's scales **hurt the base's credibility when deleted** (so the model restores them).

**（2）Phrasing sensitivity is higher than expected.**
Same part, same base, same seed: only the sentence structure changed and it went from 0% to 100% (rule 81).
→ From now on, for any part that "should have worked but did not", **suspect the phrasing first, the placeholder second**.

### 3. Self-assessment and Scoring

| Item | Number |
|----|----|
| Rounds | 6 rounds (R1 exploration / R2 coil-phrasing follow-up / R3–R6 the four finalization rounds) |
| Images generated | 23 (zimage, 1024² or 1280×1024, steps 12) |
| Finals | **13 images / 5 periods** |
| Mean score | 4.87 (lowest 4.55, highest 5.00) |
| Failures | 1 image of R1's `turtle-coil` (A=1, did not enter a period directory) |

## 6. Development Records

| File | Content |
|------|------|
| [`parts.md`](parts.en.md) | **the Black Tortoise part list** (N1–N5), freeing placeholders, rule 81 |
| [`rounds/ts-r1-r2.md`](rounds/ts-r1-r2.md) | R1–R2: single-piece exploration + the coil-phrasing follow-up (where rule 81 comes from) |
| [`rounds/ts-r3-r6.md`](rounds/ts-r3-r6.md) | R3–R6: the four finalization rounds |
| `rounds/ts-rN-review.md` | scoring review report of each round (including region audit sheets and point-by-point pros and cons) |
| [`rounds/prompts-all.md`](rounds/prompts-all.md) | verbatim prompt archive of every round |

---

## Document Revision History

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-10-04 | v0.2 | **Five-period finale**: snake neck / snake tail / coil / neck and tail / Black Tortoise, 13 images in total; added rule 81 (spatial-relation phrasing) and the sub-theme summary | 小七 |
| 2026-10-04 | v0.1 | Planning: the five-period schedule (planning first, not yet generated) | 小七 |
