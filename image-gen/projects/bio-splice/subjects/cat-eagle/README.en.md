# Sub-theme: cat + eagle

> 🌐 Language: **English** | [中文](README.md)

> Back to the [project home page](../../README.en.md) ｜ Development records in [`rounds/`](rounds/) ｜ Finals in [`period-01/`](period-01/README.en.md)

> **Whole sub-theme overview sheet**: [`sheet.jpg`](sheet.jpg) —— one row per period, assembling that period's finals (reproducible with `bash make_sheet.sh subject cat-eagle`)

## 1. Concept

**The word "owl" (猫头鹰) is itself an animal splice** (cat + head + eagle). So this sub-theme does not build a monster,
but translates the word literally into a `{cat, eagle} × {cat, eagle}` **head-body splice matrix**:

|              | cat body | eagle body |
|--------------|----------|----------|
| **cat head**   | cat (**degenerate corner**: control group) | **owl** (literal translation of the word)✅ |
| **eagle head** | **eagle-headed cat** (reverse splice)❌ | eagle (**degenerate corner**: control group) |

The two degenerate corners are the **control group**: if a pure cat, a pure eagle and the spliced body are "equally real" under the same photographic language,
that proves the sense of splicing comes from **the head-body mismatch itself**, not from the art style.

## 2. Conclusion (looking back after two periods)

### ✅ Cat head + eagle body — successful (period 01 final)

It worked at the first try. The cat head (a small, generic, round part) placed on an eagle body does not conflict with the eagle's body plan;
under the same seed it even **reuses the composition of the eagle control**, and "the same eagle with a cat head" is readable at a glance.

### ❌ Eagle head + cat body — impossible on Z-Image-Turbo (no period for now)

All four routes were tried, and all failed:

| Route | Result |
|---|---|
| head first | **pure eagle** (no cat element at all) |
| body first | a complete cat + an appended eagle head → **two heads** |
| unname the body (write only parts) | falls back to **pure eagle** (`cat` is a load-bearing word) |
| bind the name to a part / positive single-head count / remove the coordination structure | still **two heads** |

> **Later correction (R6/R7)**: what is dangerous is not "mentioning an eagle", but **naming the animal as a whole noun**.
> `eagle wings` (a part modifier) is safe, `an eagle's body` (a whole noun) is dangerous ——
> therefore **splitting into parts is the way around this blockage**. See [r03.md](rounds/r03.md) §3.

**Mechanism** (pinpointed by four single-variable rounds + same-seed controls):

1. **A named animal renders as a whole**: the head slot → only one head; the body slot → a whole animal (its own head included)
2. **Neither a positive exclusion sentence (`no X`) nor a positive count (`exactly one X`) is executed** ——
   Z-Image-Turbo uses `ConditioningZeroOut`, which has no negative prompt
3. **The strong species' whole-body prior eats the weak species' body**: eagle (wings/talons/feathers are a recognizable whole plan) vs cat (a generic quadruped)

> To make it work, the tool must change: **Qwen-Image's real negatives** (excluding `two heads, cat head, wings, talons`),
> or a **ControlNet structure lock** (using the pure-cat control as a control image to lock the body).
> Full evidence and the audit method are in [`rounds/r02.md`](rounds/r02.md).

## 3. Periods (all five present, each with its own presentation)

| Period | Theme | Base + transplant part | **Presentation (habitat · light · camera · canvas)** | Finals | Score |
|----|------|-----------------|----------------------------------------|------|------|
| [period-01](period-01/README.en.md) | **Owl** (literal translation of the word) | eagle base + cat head C2 | dawn mist autumn meadow · overcast soft light · eye-level 600mm · square | 3 (+2 controls) | ✅ 5.00 / 4.80 / 4.70 |
| [period-02](period-02/README.en.md) | **Eagle with beast ears and beast tail** | eagle base + cat ears C1 · cat tail C5 | **dusk wet grass · warm side-backlight · eye-level full body 400mm · square** | 3 | ✅ 5.00 / 4.85 / 5.00 |
| [period-03](period-03/README.en.md) | **Winged cat** | cat base + eagle wings E2 · eagle tail feathers E5 | **post-rain woodland · backlight · wide-angle low camera wingspan · vertical** | 3 | ✅ 5.00 / 4.35 / 4.80 |
| [period-04](period-04/README.en.md) | **Whiskered eagle** | eagle base + cat whiskers C6 (+ cat ears C1) | **dark background · single-side low-angle light · face-on close-up 200mm · square** | 2 | ✅ 5.00 / 4.55 |
| [period-05](period-05/README.en.md) | **Thrice eagle-ized cat** | cat base + eagle neck ruff E6 · tail feathers E5 · wings E2 | **snowfield rain mist · flat light · long-lens compression 600mm · landscape** | 3 | ✅ 4.55 / 4.55 / 4.70 |
| ~~period-06~~ | ~~**eagle-headed cat** (reverse splice)~~ | ~~cat base + eagle head E1~~ | — | — | ⛔ **judged infeasible** |

> **period-06 (eagle-headed cat) is formally scrapped**: what it needs is precisely "a head swap", and on zimage a head swap is a **two-way dead end**
> (rule 73: keep the base's species noun → the head part lands 0%; delete it → the donor takes over the whole animal).
> This finding was later independently reproduced by `dragon-nines`' D2 camel head / D3 rabbit eyes (R8/R9),
> so it is no longer "blocked, waiting for a different engine", but **a direction not to pursue**.

> Every period comes with a **scoring review report** (`rounds/rNN-review.md`): A transplant in place / B base intact / C anatomy credible /
> D photographic consistency / E concept legible, a weighted total + a threshold verdict. **Only ✅ may enter the period directory.**

> The period threshold is **all finals**. If there are no finals, no period directory is created.
> For part numbers see the [part list](parts.en.md); the combination order follows difficulty: strong base + small piece → weak base + strong local piece → multiple parts.

## 3.2. Presentation Was Hard-Won (R10–R17)

Periods 01–05 originally shared the same "dawn mist autumn meadow · overcast soft light · eye-level 600mm · square",
and the five periods read like "the same photo with swapped accessories". The four rounds that added the presentation layer (R10–R13) **hit three pitfalls in a row**,
and each pitfall became a rule down the line:

| Pitfall | Symptom | Rule |
|----|------|------|
| **camera/canvas change the transplant result** | the same cat-tail sentence: eye-level full body **works**; low camera 85mm vertical **draws an extra complete cat** | after changing camera/canvas, re-check whether the part still lands (80) |
| **a pose sentence pollutes the base control** | the pose read "it spreads both wings to the maximum" → **the control cat grew eagle wings too**, voiding the objective metrics | a pose sentence must stay silent about the target part (79) |
| **light decides whether a fine part lives or dies** | cat whiskers: **completely unreadable** in midday hard light; clearly successful in dark-background single-side light | choose the light for the part's material (80) |

> All three corrections (R14–R17) touched only the presentation layer, with not one word of the base or the transplant piece changed,
> so all earlier mechanism findings remain valid—**this is exactly the value of "constant within a period"**: when changing the presentation you can see the variable at a glance.

## 3.3. Sub-theme Summary (looking back after the whole project wrapped up)

This volume is **the first sub-theme of the whole project**, and the **source** of the entire mechanism finding set—
half of the rules used by the following 11 volumes were first stumbled on here.

### 1. The measured account

| Item | Number |
|----|----|
| Rounds | 17 rounds (R1–R5 single-variable diagnosis of the eagle-headed-cat direction / R6–R9 part splitting / R10–R17 presentation rounds) |
| Finals | **14 images / 5 periods** (+ 6 controls) |
| Mean | **4.35**—on the low side for the whole project, because three of periods 01–05 have parts that only reach "partial" |
| Failures | several (the failed rounds in the eagle-headed-cat direction, and the "extra cat drawn" of R10/R14) |

### 2. Mechanism findings contributed by this volume (later cited again and again)

| Rule | Content | Where it was later re-validated |
|------|------|----------------------|
| **57** | What is dangerous is **naming a whole as a noun** (`X's body`), not mentioning a species | dragon-nines' D2 camel head (a two-way dead end for head swaps) |
| **59** | **At most two stacked in the same region**, cross-region stacking is allowed | dragon-nines R4's four-piece stack, turtle-snake's Black Tortoise |
| **62** | **A part needs a bearing structure** (a snake has no limbs → eagle talons have nowhere to grow) | fish-bird's fish fins, tree-beast's beast feet |
| **67** | Topic priority: add into an empty slot > free a placeholder > same-material replacement | the topic selection of every sub-theme in the project |
| **79** | **A pose sentence must stay silent about the target part** (otherwise the control grows the part too) | the guard assert of every later sub-theme |
| **80** | **The presentation layer is not neutral** (camera/canvas change the transplant result) | turtle-snake period 02 changed to eye level, fish-bird's re-ordering |

### 3. Three self-criticisms of this volume

1. **The presentation of periods 01–05 was patched in afterwards**: the five periods originally shared one autumn meadow set, and only later was it realized that "constant within a period" had been misapplied across periods
   (rule 70 was established right here). The originals' finals were kept, but the presentation was redone.
2. **The eagle-headed-cat direction (period-06) went 5 rounds the wrong way**: only after dragon-nines independently reproduced it with D2/D3
   did it become possible to judge "a head swap is infeasible" (rule 73)—**at the time a minimal probe should have been run first, instead of four single-variable rounds in a row**.
3. **The reason for the cat paws' failure was misattributed at first**: it was first blamed on "the missing negative prompt", and only later pinned down to "base placeholder + no negatives"
   as two causes stacking (rules 56/58).

### 4. One sentence

**Without the pitfalls this volume hit, there would be no criterion table for the following 11 volumes**—
it is the most "expensive" volume in the whole project (17 rounds for 14 images), and also the one most worth it.

## 4. Development Records

| File | Content |
|------|------|
| [`parts.md`](parts.en.md) | **Part list** (cat C1–C6 / eagle E1–E6) and the mechanism predictions for the combinations |
| [`rounds/r01.md`](rounds/r01.md) | R1: the four corners of the matrix + splicing semantics A/B/C with same-seed controls |
| [`rounds/r02.md`](rounds/r02.md) | R2–R5: four single-variable diagnostic rounds on the eagle-headed-cat direction (including the magnified-crop audit method) |
| [`rounds/r03.md`](rounds/r03.md) | R6–R7: combinations after splitting into parts, producing periods 02 / 03 |
| [`rounds/r04.md`](rounds/r04.md) | R8–R9: the boundary of three stacked parts (conflict in the same region summons a second individual), producing periods 04 / 05 |
| [`rounds/r05.md`](rounds/r05.md) | **R10–R17 presentation rounds**: giving periods 02–05 their own identities; three pitfalls (camera changes the result / pose pollutes the control / light decides life or death) |
| [`rounds/r01-review.md`](rounds/r01-review.md) etc. | the **scoring review report** of each round (including region audit sheets) |
| [`rounds/prompts-all.md`](rounds/prompts-all.md) | verbatim prompt archive of every round (sentence-split with line breaks, losslessly restorable) |

---

## Document Revision History

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Split out of the single project `owl-splice` into a sub-theme; added the conclusions and blockage notes for both directions | 小七 |
| 2026-10-04 | **v0.2** | **All five periods + presentation redone**: periods 02–05 each got their own presentation (dusk wetland / post-rain woodland / dark-toned close-up / snowfield telephoto); period-06 eagle-headed cat formally scrapped (rule 73); added the "presentation was hard-won" section and the R10–R17 records | 小七 |
| 2026-10-05 | v0.3 | Looking back after the whole project wrapped up: added the "sub-theme summary" section (measured account / six rules contributed / three self-criticisms) | 小七 |
