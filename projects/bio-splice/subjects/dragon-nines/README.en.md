# Sub-theme: dragon · nine resemblances

> 🌐 Language: **English** | [中文](README.md)

> Back to the [project home page](../../README.en.md) ｜ Part list in [`parts.md`](parts.en.md) ｜ Development records in [`rounds/`](rounds/)

> **Whole sub-theme overview sheet**: [`sheet.jpg`](sheet.jpg) —— one row per period, assembling that period's finals (reproducible with `bash make_sheet.sh subject dragon-nines`)

## 1. Concept: The Ancients' **Part Table**

The traditional **dragon-painting mnemonic "three pauses, nine resemblances" is itself a nine-item part table**:

> antlers like a deer, head like a camel, eyes like a rabbit, neck like a snake, belly like a shen, scales like a fish, claws like an eagle, paws like a tiger, ears like an ox

(Wang Fu, Luo Yuan's *Erya Yi*, Li Shizhen's *Compendium of Materia Medica* and others all record it; the saying "three pauses, nine resemblances" appears in *Yi Xia Zhi Yan* and elsewhere.
See ["antlers like a deer, neck like a snake… let's find the 'true dragon' image"](https://baijiahao.baidu.com/s?id=1790105790609233561))

So this sub-theme does not invent a splice; it **executes a part table the ancients had already written out**—
isomorphic to the cat-eagle sub-theme (taking apart the single word "owl"), but with the donors growing from 1 animal to 8.

**Base = snake** (the "neck like a snake" entry is the body's main axis).

## 2. Why This Sub-theme Is Especially Suitable Mechanically

The rules pinpointed in this repo's r02–r04 all point exactly at the "part table" route:

| Rule | Meaning for this sub-theme |
|------|------------------|
| 57 what is dangerous is **naming a whole as a noun**, not mentioning a species | transplant pieces are always written `X's <part>`, never `X's body` |
| 56 transplant success depends on **whether the base has a placeholder** | the snake **has no** antlers, ears, claws or paws → all empty slots, the easiest to succeed |
| supplement to 56 (new in this round) | but the **existence of the bearing structure this part needs** must also be checked (see below) |
| 59 at most two stacked in the same region | head parts (antlers/ears/eyes/head) must be split across periods or staggered |

## 3. Core Finding: **A Part Needs a Bearing Structure**

### Period 01: snake base + deer antlers — successful

"The horned snake" **worked at the first try**: the branching antlers grow out of the skull naturally and read as a **dragon** at a glance. Adding ox ears also works.

### But "claws like an eagle" **fails completely** on a snake

The snake **has no limbs**—the claws are not overridden by the base description (the kind of failure in rule 56), they have **nowhere to grow**.

> **Rule supplement**: rule 56 only said "the base has no placeholder, so a transplant is possible", but that assumes by default that **the bearing structure the part needs exists**.
> A snake has no forelimbs → the eagle talons cannot land. **The base's anatomy must be able to bear the transplant piece.**

### Period 02: switching to a lizard base with limbs — partial success

After switching to `lizard` (it has limbs and likewise a snake-shaped torso), the claws are **partially successful**: the claw shape changes from the baseline's **short blunt lizard claws**
to **long, curved, raised raptor-style claws in a grasping pose**; but it does not reach a complete eagle talon (the foot is still dark and scaly,
not the eagle's yellow scaled tarsus). Tiger paws D8 did not succeed.

> This matches the Chinese dragon's image: **the dragon is a four-legged snake body**—"neck like a snake" takes the snake, while the "four legs" must find another base.

## 4. Constant Within a Period, Different Across Periods

| Scope | Requirement | Why |
|------|------|--------|
| **within a period** | habitat / light / camera / canvas **must be constant** | guarantees that the period's "transplant vs base control" is comparable (same seed, same skeleton, the only variable being the transplant piece) |
| **across periods** | these four **should differ** | gives each period its own identity, otherwise the whole set reads as "the same image with swapped accessories" |

The series-constant layer keeps only two items (so that two sub-themes can still be placed side by side as one set): the **CN framing sentence** + **the foundation of realistic wildlife photography**.

> This was hard-won: R1–R4 applied "layer-constant" across periods, so the four periods looked different only in the transplant piece.
> After changing to "different across periods" and **choosing the camera for the subject** (period 02 aimed at the claws, period 03 at the scales),
> the two periods' parts that were originally "partial and hard to read" became recognizable at a glance.

## 5. Periods

**Each period has its own identity**: the base and transplant part decide "what it is", while **habitat / light / camera / canvas** decide "what it looks like".
The latter are chosen for the subject (period 02's camera aims at the claws, period 03's at the scales); details in [`rounds/dn-r5-r7.md`](rounds/dn-r5-r7.en.md).

| Period | Theme | Base + transplant part | **Habitat · light · camera · canvas** | Finals | Score |
|----|------|-----------------|-------------------------------|------|------|
| [period-01](period-01/README.en.md) | **Horned snake** | snake + D1 deer antlers (+D9 ox ears) | dawn mist reeds · overcast soft light · eye-level 600mm · square | 2 | 5.00 / 4.65 |
| [period-02](period-02/README.en.md) | **Clawed lizard** | lizard + D7 eagle talons (+D8 tiger paws) | **post-rain pebble riverbank · damp side-backlight · low camera on the ground 85mm focused on the front feet · vertical** | 2 | 4.55 / 4.40 |
| [period-03](period-03/README.en.md) | **Fish-scaled snake** | snake (scale placeholder freed) + D6 fish scales | **forest floor leaf litter · dappled forest light · side-high body-hugging 100mm macro · square** | 2 | 5.00 / 4.55 |
| [period-04](period-04/README.en.md) | **Composite dragon** | lizard + D1 antlers + D9 ears + D7 talons + D8 paws | **rain-soaked rock · dusk backlight + rain streaks · wide-angle low camera 35mm · landscape** | 2 | 4.70 / 4.40 |
| [period-05](period-05/README.en.md) | **Dragon-head close-up** (finale) | snake + D1 antlers + D9 ears (+D6 fish scales) | **dawn mist reeds · side-backlight outlining the silhouette · face-on close-up 200mm · square** (the only close-up in the whole sub-theme) | 2 | 5.00 / 4.70 |

**All five periods are in** (10 finals). Of the nine resemblances: **2 fully successful** (antlers D1, ears D9),
**3 partial** (scales D6, claws D7, neck D4 = the base itself), **3 unsuccessful** (paws D8, head D2, eyes D3),
**1 not executed** (belly D5 shen—a mythical creature; a visual proxy must be defined first).

> The shen of "belly like a shen" has no real animal counterpart, so it is **not executed for now**; define a visual proxy first
> (candidates: the ribbed ventral face of a giant clam / iridescent belly scales like a mirage) before starting the period.

## 6. Sub-theme Summary (self-assessment after the finale)

### 1. Of this nine-resemblances table, only the "empty slot + has a carrier" class can be executed

| Type | Part | Result | Mechanism |
|------|------|------|------|
| **add into an empty slot** (the base lacks that part) | D1 antlers, D9 ears | ✅ fully successful (5.00) | the easiest, works at the first try |
| **free a placeholder** (first delete the corresponding description from the base) | D6 scales, D7 claws | ⚠️ partial | effective, but only the shape changes, not the material |
| **same-material replacement** | D6 scales (scale for scale) | ⚠️ partial and hard to read | the lowest conceptual legibility |
| **head parts** (where the species identity lies) | D2 head, D3 eyes | ❌ two-way dead end | see below |
| **no bearing structure** | D7 claws (on a snake base) | ❌ 0% appearance | solved by changing the base |

### 2. The two most important negative results of this sub-theme

**（1）Head parts cannot be swapped—they are the species identity itself.**
Freeing the placeholder (deleting the head-shape and eye descriptions) → the camel head appears 0% of the time, and the image instead becomes **more snake-like** (the model fills in neck folds);
deleting the base's species noun (`snake`) → **a whole camel is dragged out**, and the base is destroyed.
**The base's species noun is both a "placeholder" and an "anchor"**: delete it and the donor takes over the whole individual.

> Corollary (already written back into PLAN): **head swaps / beak swaps / face swaps must not be written into any sub-theme's final targets.**

**（2）"Freeing a placeholder" is not a master key.**
It works only for parts where **the base's prior is weak** (claws and scales both show visible change);
for parts like the head, whose prior is extremely strong, the freed slot is filled back in by the model's own species prior.

### 3. Common problems stumbled on by this sub-theme (already written back into PLAN §5)

| Problem | Consequence | Fix |
|------|------|------|
| applying "layer-constant" across periods | four periods read as "the same image with swapped accessories" | constant within a period + **different across periods** (rule 70) |
| judging "empty slot/occupied" by intuition in the plan | D3 rabbit eyes were misjudged as "an empty slot, easy to succeed", when the base actually wrote eyes | **check the base text word by word** before judging occupancy when scheduling |
| mixing several bases in one round | a same-round control is valid only for shots with the same base; the other images' objective metrics are unusable | **one base per round** (rule 76) |
| treating "head parts" as ordinary parts in the plan | period 05's original plan (camel head + rabbit eyes) failed on both, and the finale period almost came up empty | head parts are always downgraded to "expected to fail, not a final target" |
| taking the objective region difference as a success criterion | R8's region difference of 11.6–15.9 was far above the threshold, yet not one part landed | the region difference serves only as a **one-way alarm**: unchanged → definitely did not land; changed → says nothing |

### 4. Scoring and Cost

| Item | Number |
|----|----|
| Rounds | 10 rounds (R1–R4 exploration / R5–R7 finalization / R8–R9 mechanism follow-up / R10 finale finalization) |
| Images generated | 34 (zimage, 1024², steps 12, ~25 s/image) |
| Finals | 10 (5 periods × 2) |
| Mean score | 4.75 (lowest 4.40, highest 5.00) |
| Failures | R8's 3 images (A=1), R9's 2 images (base destroyed)—**none entered a period directory** |

## 7. Development Records

| File | Content |
|------|------|
| [`parts.md`](parts.en.md) | **the nine-resemblances part list** (D1–D9), base selection, mechanism predictions |
| [`rounds/dn-r1.md`](rounds/dn-r1.en.md) | R1: snake base + deer antlers, discovering that "a part needs a bearing structure" |
| [`rounds/dn-r2.md`](rounds/dn-r2.en.md) | R2: switching to a lizard base + eagle talons, verifying that changing the base works |
| [`rounds/dn-r3.md`](rounds/dn-r3.en.md) | R3: fish scales, the technique of "freeing a placeholder" and the difficulty of reading a same-material replacement |
| [`rounds/dn-r4.md`](rounds/dn-r4.en.md) | R4 [composite dragon]: a 4-piece stack, the region ceiling re-verified |
| [`rounds/dn-r5-r7.md`](rounds/dn-r5-r7.en.md) | R5–R7 **finalization rounds**: giving the "periods" their own characteristics (period style table + constant within a period/different across periods) |
| [`rounds/dn-r8.md`](rounds/dn-r8.en.md) | R8: camel head D2 / rabbit eyes D3—**freeing the placeholder is ineffective, both pieces rejected** |
| [`rounds/dn-r9.md`](rounds/dn-r9.en.md) | R9: following up "the base's species noun = a placeholder"—delete it and the donor takes over the **whole animal** |
| [`rounds/dn-r10.md`](rounds/dn-r10.en.md) | R10: finalizing period 05 [dragon-head close-up], adding only the same-round control |
| `rounds/dn-rN-review.md` | scoring review report of each round (including region audit sheets and point-by-point pros and cons) |
| [`rounds/prompts-all.md`](rounds/prompts-all.en.md) | verbatim prompt archive of every round |

---

## Document Revision History

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | New sub-theme: dragon · nine resemblances. Period 01 (horned snake) and period 02 (clawed lizard) delivered | 小七 |
| 2026-10-04 | v0.2 | **Five-period finale**: period 05 [dragon-head close-up] delivered (5.00 / 4.70); added the R8/R9 negative results (the two-way dead end of head parts, freeing a placeholder is not a master key) and the sub-theme summary | 小七 |
