# Sub-theme: Fish + Bird (Kunpeng)

> 🌐 Language: **English** | [中文](README.md)

> Back to [project home](../../README.en.md) ｜ part table in [`parts.md`](parts.en.md) ｜ development log in [`rounds/`](rounds/)

> **Whole-sub-theme overview sheet**: [`sheet.jpg`](sheet.jpg) — one row per period, with that period's finals assembled together (reproducible with `bash make_sheet.sh subject fish-bird`)

## 1. Concept: a single **form transformation**

**《Zhuangzi · Xiaoyaoyou》: in the Northern Sea there is a fish… it transforms into a bird** — a form transformation explicitly stated in the classics.
So the hook of this sub-theme is not "add one part" but **a single transformation**:
bird flight parts grow on a fish's trunk, **from water into the air**.

**Base = big fish (carp)**; donors = the bird's flight parts: wings B1 / tail feathers B2 / plumage B5.
~~Beak B3 / claws B4~~ removed (head parts 73 / a fish has no limbs 74).

## 2. The most important finding of this sub-theme: **habitat is a hard constraint**

Same base, same sentence, same seed — **only the scene moves from underwater to above the water surface**:

| Scene | Result |
|------|------|
| Underwater (`in shallow clear water over pale gravel`) | ❌ wings 0% — all three wordings wiped out (7 images across R1/R2/R3) |
| **Out of water** (`in open air above the water surface`) | ✅ wings appear **immediately** (from R4 on, 5 independent reproductions) |

> **Rule 85: when a transplanted part conflicts semantically with the habitat, the model keeps the scene and drops the part.**
> "Feathers / wings underwater" is a semantic contradiction — the model would rather turn the transplant sentence into a no-op
> than paint a fish with wings underwater.
>
> **Corollary (applies to every sub-theme)**: **first choose a habitat semantically compatible with the transplanted part, then talk about wording and placeholders.**
> This ranks before writing discipline — it comes earlier than "how to write it".

**Rule 86: scene compatibility is judged region by region.** In period 02 "half out of water",
a wing written on the flank (below the waterline) **gets eaten**; written as "half-open, positioned high" (on the side above the surface) it **lands**.

## 3. How this finding changed the sub-theme's schedule

Original plan (PLAN v0.1): 5 periods doing wings / tail feathers / plumage covering / wings + tail feathers / all three.
Measurement: **only the wings work** (tail feathers and plumage covering land in neither scene — Rule 87 canonical structure + Rule 67 same-material replacement).

So the schedule was redone — **the main axis changed from "swap parts" to "stages of leaving the water"**:

| Period | Stage | Presentation | Finals | Score |
|----|------|------|------|------|
| [period-01](period-01/README.en.md) | **Leaping out of the water** (just left the water, spray not yet fallen) | backlit spray · eye level 100mm · landscape | 2 | 5.00 / 5.00 |
| [period-02](period-02/README.en.md) | **Half out of water** (the waterline crosses the body) | side light · eye level 135mm · square | 3 | 5.00 ×3 |
| [period-03](period-03/README.en.md) | **Fully out of water · both wings fully spread** | high-side angle · backlight rimming the feathers · square | 2 | 5.00 / 5.00 |
| [period-04](period-04/README.en.md) | **Skimming low over the water** | telephoto compression · flat light on grey water · landscape | 2 | 5.00 / 5.00 |
| [period-05](period-05/README.en.md) | **Kunpeng** (finale) | dusk sea surface · backlit silhouette · wide angle · landscape | 2 | 5.00 / 5.00 |

> Constant within a period: each period has one **water-exit moment** and one fixed presentation;
> varying between periods: waterline position, camera, lighting and canvas all differ, so the five periods read as **one timeline**.

## 4. Sub-theme summary (self-assessment after the finale)

### 1. Measurement ledger

| Part | Underwater | Out of water | Conclusion |
|------|------|------|------|
| B1 bird wings | ❌ 0% (three wordings) | ✅ **Fully holds** (5 reproductions) | The only usable part; success is decided by the scene |
| B2 bird tail feathers | ❌ 0% | ❌ 0% | The tail position is a canonical structure (Rule 87) |
| B5 plumage over the back | ❌ 0% | ❌ 0% | Same-material replacement (Rule 67, tier 3) |

### 2. The three rules contributed

- **85 Habitat is a hard constraint**: when a part conflicts semantically with the scene, the model keeps the scene and drops the part.
  **This is the project's first rule that "ranks before writing discipline".**
- **86 Scene compatibility is judged region by region**: within one image, the exposed part can grow a piece, while the part soaking in water cannot.
- **87 Canonical structures cannot free a placeholder**: fish fins / cat paws / snake scales get restored even if their description is deleted;
  this forms an exact control against the turtle's neck and tail (where deletion does not hurt the base), completing the tiering of Rule 83.

### 3. Self-criticism (where this sub-theme fell short)

1. **The first 3 rounds (R1–R3) wasted 11 images**. R1 should have started with **one minimal probe**:
   the same sentence, only the scene swapped (underwater vs out of water). Then Rule 85 would have been hit in the first round,
   instead of trying three wordings underwater, then an empty slot, and only then thinking of changing the scene.
   → **Suggested new process**: in a new sub-theme's first round, first run a "**scene × part semantic compatibility**" probe
   (one image of the same part for each candidate habitat per period), then move on to tuning wording and placeholders.
2. **Tail feathers and plumage covering were each tried twice and then dropped**, without trying "put the tail feathers in a non-canonical position"
   (e.g. the rear end of the dorsal ridge). If either is revisited later, that is the place to start.

### 4. Scoring and cost

| Item | Count |
|----|----|
| Rounds | 11 rounds (R1–R3 underwater exploration / R4–R5 out-of-water probe / R6–R11 finalizing the five periods) |
| Images generated | 37 (zimage, 1024² or 1280×1024, steps 12) |
| Finals | **11 images / 5 periods** |
| Average score | 5.00 (all first-pick) |
| Rejected | 15 (the underwater probes and the tail-feather / plumage-covering probes), **none entered a period directory** |

## 5. Development log

| File | Content |
|------|------|
| [`parts.md`](parts.en.md) | **Kunpeng part table** (B1/B2/B5) + Rules 85/86/87 |
| [`rounds/fb-r1-r5.md`](rounds/fb-r1-r5.en.md) | R1–R5: total wipeout underwater → landing out of water (the source of the habitat hard constraint) |
| [`rounds/fb-r6-r11.md`](rounds/fb-r6-r11.en.md) | R6–R11: the rounds finalizing the five water-exit stages |
| `rounds/fb-rN-review.md` | Review reports for each round's scoring |
| [`rounds/prompts-all.md`](rounds/prompts-all.en.md) | Verbatim prompt archive for every round |

---

## Revision history

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.2 | **Five periods finalized**: 11 finals; Rules 85–87 discovered (habitat hard constraint / region-by-region judgement / canonical structures cannot be freed); the schedule's main axis changed from "swap parts" to "water-exit stages" | 小七 |
| 2026-10-04 | v0.1 | Planning: five-period schedule (planning first, not yet generated) | 小七 |
