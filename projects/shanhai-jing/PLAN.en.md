# Shan Hai Jing · Baimiao Illustrated Verses — Full Project Plan

> 🌐 Language: **English** | [中文](PLAN.md)

> Back to [project entry](README.en.md) ｜ Techniques in [../../.agents/skills/README.md](../../.agents/skills/README.md)

---

## 1. Positioning

| Item | Content |
|------|---------|
| One line | A baimiao illustrated-verse series driven by the verbatim *Shan Hai Jing*, one creature per period, verifiable character by character |
| Platform | Xiaohongshu image posts (vertical 3:4) |
| Differentiation | **Verifiable scholarship**: volume + original passage + commentary, and **countable traits must be counted correctly** |
| Not doing | No spectacle-driven "AI restores the Shan Hai Jing"; no unsourced invention; no text written by the model |

**Why scholarship is the only way**: the subject is saturated in AI art — users have already seen a thousand nine-tailed foxes. The visuals are no longer scarce; **being checkable is**.

---

## 2. Source edition and citation format

### Source

- **Base text**: the Guo Pu annotated *Shan Hai Jing* (verified; from [識典古籍](https://www.shidianguji.com/zh/book/SK2098/chapter/1m12x7ij5mwp6), cross-checked against the [Chinese Text Project](https://ctext.org/shan-hai-jing/nan-shan-jing/zh))
- **Verified word by word**, no character changed or omitted; variant forms (e.g. 謡, 蠱) follow the source edition
- ⚠️ **Guo Pu's commentary has not been transcribed yet**: this round verified the base text only. Until it is transcribed from the same edition, **no commentary may appear in any deliverable** (never fill it in from memory)

### Citation format (three fixed blocks per period)

```
【Volume】Shan Hai Jing · Nan Shan Jing
【Text】又東三百里，曰青丘之山。……有獸焉，其狀如狐而九尾，其音如嬰兒，能食人。食者不蠱。
【Guo Pu】 (to be transcribed)
```

### Verified passages (first batch)

| Creature | Volume | Verified key passage |
|----------|--------|----------------------|
| Nine-tailed fox | Nan Shan Jing · Qingqiu Mountain | 有獸焉，其狀如狐而九尾，其音如嬰兒，能食人。食者不蠱。 |
| Lu Shu | Nan Shan Jing · Niuyang Mountain | 有獸焉，其狀如馬而白首，其文如虎而赤尾，其音如謡，其名曰鹿蜀，佩之宜子孫。 |
| Xing Xing | Nan Shan Jing · Zhaoyao Mountain | 有獸焉，其狀如禺而白耳，伏行人走，其名曰狌狌，食之善走。 |
| Lu (fish) | Nan Shan Jing · Di Mountain | 有魚焉，其狀如牛，陵居，蛇尾有翼，其羽在魼下……冬死而夏生 |
| Lei | Nan Shan Jing · Danyuan Mountain | 有獸焉，其狀如貍而有髦，其名曰類，自爲牝牡 |
| Bo Shi | Nan Shan Jing · Ji Mountain | 有獸焉，其狀如羊，九尾四耳，其目在背，其名曰猼訑 |
| Chang You | Nan Shan Jing · Changyou Mountain | 有獸焉，其狀如禺而四耳，其名長右，其音如吟 |
| Gu Diao | Nan Ci Er Jing · Luwu Mountain | 其狀如雕而有角，其音如嬰兒之音，是食人 |
| Qu Ru | Nan Ci San Jing · Daoguo Mountain | 有鳥焉，其狀如鵁而白首三足，人面，其名曰瞿如 |

> All from the verified Nan Shan Jing volume (including Nan Ci Er Jing and Nan Ci San Jing). Xi Shan Jing and later volumes will be scheduled after the same verification.

---

## 3. Plate craft

### Settled process (after the R6-R8 correction)

```
1) Generation  Z-Image-Turbo text-to-image — the "name the mythological being" phrasing, no control image   ✅ 4/4 and 8/8
2) Typesetting typeset_zanzhi.py: cartouche + source + volume + frame   ✅ implemented (5 layout self-checks; seal pending the typeface)
3) Count check visual counting with archived crops — "reads as nine" is enough, no mechanical certification
4) Seal screen  all four corners magnified 4x and inspected (seal_check.py shortlists) -> if sealed, erase with patch_region.py and archive   ✅ established in the lu-shu period
5) Scoring     six dimensions A-F (F vitality .25); `fatal` reserved for hard defects
```

### Wording rules (measured on lu-shu R1-R4; write every later period this way)

| Rule | Evidence |
|------|----------|
| English naming + **itemised traits** | the lu-shu v5 wording (`pure white head` / `bold black tiger stripes` / `only its long tail is cinnabar red`) landed all four traits |
| **Do not use a Chinese direct description** | the Chinese group failed 6/6 across two rounds: tiger markings collapse into spots, the coat drifts brown, the ochre oversaturates |
| **"Do not draw X" does not work** | R3's three no-seal wordings were ignored by all nine images; suppressing seals needs a reworded style or tool erasure |
| Confine the red explicitly | only `only its long tail is …` removed the mane the model otherwise invents |

> WARNING: **this process differs substantially from the first version.** The first version treated "lock the
> countable trait" as step one and invested in a whole apparatus of programmatic control images + Canny +
> ControlNet. R6-R8 measured that **this apparatus was machinery for a problem that did not exist** — what
> actually decides success is the **prompt phrasing**. See [rounds/r05-review.en.md](subjects/jiu-wei-hu/rounds/r05-review.en.md).

### Probe findings (2026-10-05)

| Check | Result | Evidence |
|-------|--------|----------|
| Baimiao bone works | ✅ | v3 sample: even thin ink lines, generous margin, correct Chinese idiom |
| Woodcut texture works | ✅ | v1/v2 samples: crisp knife-cut hatching, aged paper (for covers) |
| Style stable across seeds | ✅ | R1 six-seed sweep, highly consistent language |
| **Countable traits controllable** | ❌ | **all six failed**: prompt said `EXACTLY nine tails`, results had 7-9 with overlapping boundaries; still uncountable at 2x zoom |
| Model adds things unbidden | ❌ | asked for monochrome, added orange on the ears; v2 produced a **garbled seal** and a stray red dot |

**Two iron rules follow**:
1. **The model does not write** — cartouche, source and seal are typeset with real glyphs (model-drawn seals are garbled, a hard defect)
2. **The model does not count** — countable traits need structural control or human recount, never a prompt gamble

### RETIRED: a programmatic control image (R6-R8 disproved its necessity)

> **This section is kept as a record of the lesson; it is no longer a process step.**
> The first version assumed "the prompt cannot control counting" and forced the count with a geometric
> construction image plus ControlNet. In practice every fix of one artefact produced the next
> (thin ribbon -> hollow outline; pointed blade -> leaf veins; thickening -> flower petals;
> de-mechanising -> still fan ribs), while **plain text-to-image in the same period, with the prompt
> rephrased to name the being, produced nine tails 4/4 and 8/8 and looked plainly better**.
> The real fault was the prompt (descriptive phrasing + `EXACTLY nine` + `no hatching`), not the model.

The nine-tailed fox's countable trait is **nine tails**, and the first version concluded path B from it:
counting moves from "gambling on the model" to "guaranteed by geometric construction".

```bash
python3 scripts/control_image.py --creature jiu-wei-hu --width 864 \
  --out work/shanhai-jing/jiu-wei-hu/r02/control-nine-tails.png
# -> tail_count: 9 (by construction) / min_gap_px: 31.52 / border_ink_px: 0 -> OK
```

`scripts/control_image.py` carries two **self-checks** (exit code 0 is the only pass):

| Self-check | Criterion | Measured |
|------------|-----------|----------|
| Separation | beyond `disentangle_r` (0.20) all nine tails are pairwise disjoint, min gap > 0 | ✅ 31.52 px |
| Framing | ink pixels inside the outer 7px ring = 0 (so the render is never cropped) | ✅ 0 px |

Pipeline: `control_image.py` -> Canny -> ControlNet (`comfyui_edit.py`) -> baimiao final.
The control image is **deterministic** (same parameters reproduce identical pixels; `pngdiff` reports `SAME`),
so "nine tails" is reproducible and auditable along the whole chain.

> Retired: **A large-sample screening** (sweep 40-60 and count by eye). Its evidence is too weak — zoomed
> tail boundaries stay fuzzy, so "I counted right" remains a subjective claim and cannot carry a
> strict-sourcing banner.

### Seal: seal-script typeface (PAUSED, unresolved)

Requirement: open source and commercially usable (OFL class) **and covering the characters the seal
needs**. That "and" was learned the hard way:

| Candidate | Licence | Measured | Verdict |
|-----------|---------|----------|---------|
| [lxgw/LxgwSeal](https://github.com/lxgw/LxgwSeal) | SIL OFL 1.1 | **only 375 codepoints**: 九 present, 尾 and 狐 missing (they render as substitution boxes) | ❌ **unusable** (covers essentially only the Unicode Small Seal block) |
| [SuperMate-Ai/JFZSKSealScript](https://github.com/SuperMate-Ai/JFZSKSealScript) V3.5 | SIL OFL 1.1 | 2.4 MB; the release CDN times out after a 302 | ⏸ retry from another mirror |

**Run the coverage check before adopting any typeface**:

```bash
python3 scripts/font_coverage.py --font F.ttf --text 九尾狐
# -> missing characters are listed one by one; a gap exits 1
```

This gate is necessary because the eye **cannot tell "seal script" from "missing-glyph boxes"** inside a
rendered image — the first render test fooled exactly that way.

Current state: **the seal layer is missing**, which does not block the plate, the cartouche or the source
passage. **A model-generated garbled seal is never acceptable** (probe v2 already produced one).

---

## 4. Creature schedule

### Grouping

Serialise by **volume**, one volume per period or a few periods, so the citation format stays consistent within a period:

| Group | Volume | Note |
|-------|--------|------|
| A | Nan Shan Jing (incl. Nan Ci Er Jing, Nan Ci San Jing) | text verified, can start now |
| B | Xi Shan Jing | to verify |
| C | Bei Shan Jing | to verify |
| D | Dong Shan Jing / Zhong Shan Jing | to verify |
| E | Haiwai / Hainei / Dahuang volumes | to verify (mostly deities, more abstract shapes, harder) |

### Tuning period (done)

**`jiu-wei-hu`, the nine-tailed fox (Nan Shan Jing · Qingqiu Mountain)** — chosen as a stress test because **nine tails is the hardest countable trait in the book**; lock nine tails and you can lock three heads and six eyes, or six legs and four wings.

### First period (done)

**`lu-shu` (Nan Shan Jing · Niuyang Mountain)** — chosen as the first regular entry: its three verifiable traits
(white head / tiger markings / red tail) **involve no counting**, so it tests whether the tuning-period conclusions
transfer to a second creature. Findings:

* the wording settled down (English naming + itemised traits + red confined to one part); the Chinese direct
  description was disproved a second time;
* **the seal problem surfaced**: under this brushwork 19 of 20 spot-checked Z-Image images stamp their own garbled
  seals → two new process steps, a four-corner visual gate and tool erasure;
* **cross-engine comparison** (Seedream 5.0 Pro, six paid images): stronger traits, but 6/6 carry an inscription
  and seals → **no engine switch** (see `subjects/lu-shu/rounds/r04-review.en.md`).

---

## 5. Acceptance criteria

### Scoring dimensions (out of 5, weighted)

| Dimension | Weight | Criterion |
|-----------|--------|-----------|
| **A Sourcing accuracy** | .25 | passage verbatim, volume correct; **every countable trait counted and matching**; every described feature realised |
| **F Vitality of brushwork** | .25 | fur texture, lines with brush intent and variation in density, a natural pose, a composition that breathes; **not a hollow outline drawing** |
| **B Bone purity** | .15 | it is baimiao ink line; not ink wash, not guochao impasto, not Western print hatching |
| **C Format completeness** | .15 | generous margin, upright composition, cartouche space and frame, fits the illustrated-verse format |
| **D Legibility** | .10 | recognisable at a glance, not confusable with another creature |
| **E Series consistency** | .10 | same line density, paper tone and margin as its batch |

> WARNING: **dimension F was added after the fact.** The first rubric had only five
> correctness/consistency dimensions A-E and **not one measuring beauty**. The consequence was
> measured, not theorised: a programmatic control image plus a high control strength plus a prompt
> saying "uniform thin weight / no hatching" produced an image that **counted correctly but looked the
> worst**, and it scored 4.65 on the old rubric and was declared the preferred final.
> Lesson: **whatever dimension the acceptance table lacks is the dimension the work systematically
> degrades along** — it was not bad luck, the rubric pushed the selection to that solution.

### Thresholds (hard)

- **non-empty `fatal` -> fail.** `fatal` covers: an **obvious counting error** (only one tail, clearly not nine), a wrong character in the passage, a wrong volume, a garbled seal, model-generated Chinese characters
  - the **executable criterion** for "a garbled seal / model-generated characters" (established in the lu-shu period): magnify the four corners of every candidate 4x and look; `seal_check.py` only shortlists candidates mechanically (four automatic criteria were tried and all failed — see `subjects/lu-shu/rounds/r01-review.en.md` §4); if such an image must be kept, erase the region with `patch_region.py` and record `seal_erasure` in `manifest.json` (self-checked: residue <=5%, seam <=30)
- `A < 3`, **`F < 3`** or `C < 3` -> fail (an ugly image is equally undeliverable)
- total >= 4.0 with `A >= 4` and `F >= 4` -> preferred final; >= 3.5 -> final; otherwise alternate (**not shipped**)

### Count check procedure

1. after generation **crop the countable region** and magnify it (`ffmpeg crop+scale`, archived under `work/`)
2. **count by eye and write the process** into `rounds/rNN-review.md`
3. **only an "obvious error" is `fatal`** (one tail, clearly five ...); for bushy tails whose plumes overlap, "reads as nine" passes
4. label the criterion **"visual count, not mechanical certification"**

> WARNING: **do not restore a mechanical-certification gate.** Measured lesson: making "mechanically
> certifiable exactly 9" a hard gate forces geometric, mechanical images (R2-R5), and fluffy tails simply
> cannot be measured with callipers. The strength of a criterion must match the nature of its object.
> See [rounds/r05-review.en.md](subjects/jiu-wei-hu/rounds/r05-review.en.md).

### Base controls

Every round carries a **same-round base control** (`period-NN/controls/`), following [bio-splice](../bio-splice/README.en.md).

---

## 6. Scale and order of work

1. **Tuning period (current)**: one creature, `jiu-wei-hu`, through the full loop (generate -> lock the count -> typeset -> recount -> score)
2. **First period**: 3-5 creatures from Nan Shan Jing, validating format and throughput
3. **Open up**: verify Xi Shan Jing -> 5 creatures per period, steady cadence

> Do not scale up first: bone-china-doll's R11/R12 regression rounds already proved that the biggest cost in a serial project is **rework after style drift**.

---

## Revision history

| Date | Version | Change |
|------|---------|--------|
| 2026-10-05 | v0.1 | Plan created: positioning / source edition (Nan Shan Jing verified) / plate craft (four probe findings) / creature grouping / A-E acceptance; the structural-control path is marked open |
| 2026-10-06 | v0.2 | **The first period (lu-shu) closed the loop and the craft gained two steps**: (1) the process table gained a "seal screen" (four corners at 4x -> `seal_check.py` shortlists -> `patch_region.py` erases and archives); (2) four "wording rules" were added (English naming + itemised traits / no Chinese direct description / negative clauses are useless / confine the red to one part), each backed by measurement; (3) the `fatal` threshold's "garbled seal / model-generated characters" gained an executable criterion; (4) the creature schedule records the completed first period and the cross-engine conclusion (Seedream has stronger traits but adds an inscription in 6/6, so no engine switch) |
