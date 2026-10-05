# Bio Splice

> 🌐 Language: **English** | [中文](README.md)

> Back to the [project index](../README.en.md) ｜ Technical skills in [../../skills/](../../skills/README.md)

> 🏁 **This project is fully delivered (12 sub-themes / 60 periods / 135 finals)**; for the project-wide summary see [`SUMMARY.md`](SUMMARY.en.md).

**A splicing project**: graft A's organs onto B's body and shoot it in the realistic language of documentary photography (or microscopy / specimen imaging), as if it were a species that really exists.

**Not limited to animals**—plants, fungi, algae and lichens can all serve as base or donor;
sub-themes are divided by **biological combination**, 5 periods each, 2–3 finals per period.

The full plan is in [`PLAN.md`](PLAN.en.md) (12 sub-themes × 5 periods).

---

## 1. Directory Structure

```
bio-splice/
├── README.md                    ← this file (project overview)
├── run_round.py                 ← round driver entry point (--subject picks the sub-theme)
├── roundkit.py                  ← shared machinery of the driver (run rounds / archive / sentence splitting and line wrapping)
├── curate.py                    ← final promotion: work/ → period/, keeping the provenance
├── score.py                     ← scoring review: objective alarms + subjective dimensions; decides by threshold whether a shot can become a final
├── make_sheet.sh                ← contact sheets (round = for development / period = period finals / subject = cross-period overview / all = everything at once)
├── PLAN.md                      ← **the full sub-theme and 5-period plan**
├── subjects/                    ← sub-themes, divided by biological combination
│   ├── cat-eagle/               ← sub-theme: cat + eagle (period-01 … period-05)
│   │   ├── sheet.jpg            ← **cross-period overview sheet** (one row per period, all the sub-theme's finals in one image)
│   │   ├── sheet-thumb.jpg      ← thumbnail of the sheet above (for embedding in docs; click to see the full image)
│   │   └── ...
│   └── dragon-nines/            ← sub-theme: dragon · nine resemblances (period-01 … period-04)
│       ├── README.md            ← sub-theme concept and conclusions
│       ├── sheet.jpg            ← **cross-period overview sheet**
│       ├── sheet-thumb.jpg      ← thumbnail (same as above)
│       ├── parts.md             ← this sub-theme's **part table**
│       ├── rounds/              ← this sub-theme's development records (rounds, diagnoses, prompt archive)
│       └── period-01/           ← period: **finals only**
│           ├── README.md
│           ├── manifest.json    ← provenance of every final (round / shot / seed / prompt_id / sha256)
│           ├── sheet.jpg        ← this period's contact sheet
│           ├── 01-*.png …       ← final
│           └── controls/        ← controls (not finals of this period; the series' frame of reference)
└── work/<子主题>/rN/            ← exploration artifacts (work-in-progress / failed rounds) **not committed to the repo**
                                   round numbers are numbered within a sub-theme; two sub-themes' r1 do not conflict
```

## 2. Discipline: Finals and Work-in-Progress Are Kept Apart

| Location | Content | Enters the repo? |
|------|------|----------|
| `work/<子主题>/rN/` | **all** raw output of every round, including failed rounds (round numbers are numbered **within a sub-theme**) | ❌ **no** |
| `subjects/<子>/period-NN/` | **finals only** | ✅ yes |

- **Anything that looks fake at a glance does not enter the finals.** The criterion: would someone who knows nothing about this project think at a glance "this is fake / broken".
  Typical rejects: two heads, misalignment, obtrusive collage seams, species regression (you wanted an eagle-headed cat but got a pure eagle).
- **Work-in-progress does not have to enter the repo because it can be reproduced**: `run_round.py` fixes every seed,
  and it has been verified that under the same prompt/seed/canvas the **decoded pixels are byte-for-byte identical**.
  So clearing `work/` loses no evidence—re-running reproduces it.
- **Finals can only enter the delivery directory through `curate.py`**, which writes `manifest.json`
  (source round, shot name, seed, prompt_id, prompt verbatim, sha256). A manual `cp` loses the provenance.
- **Every round must be scored after generation** (`score.py`): A transplant in place .30 ｜ B base intact .20 ｜ C anatomy credible .20 ｜
  D photographic consistency .15 ｜ E concept legible .15; non-empty `fatal` / A<3 / B<3 → fail.
  **Only ✅ (total ≥3.5) enters the period directory**; ⚠️ alternates and ❌ never enter.
  Objective metrics (region difference against the same round's base control) serve only as an **alarm**—an unchanged region means the transplant sentence was a no-op;
  a changed region **cannot** prove that the part caused it (pose drift changes it too), so visual confirmation is required.

```bash
# pick finals from a round and promote them to a period
python3 curate.py --period subjects/cat-eagle/period-01 \
    --from work/cat-eagle/r1/round.json \
    --pick owl-seamless=01-owl-seamless \
    --control cat=controls/cat
```

## 3. Sub-themes (12 × 5 periods, see [PLAN.md](PLAN.en.md) for details)

| # | Group | Sub-theme | Concept hook | Status |
|---|----|--------|----------|------|
| 1 | A | [cat-eagle](subjects/cat-eagle/README.en.md) · cat + eagle | The word "owl" (猫头鹰 = cat + head + eagle) is itself a splice | **5 periods delivered** (each with its own presentation) |
| 2 | A | [dragon-nines](subjects/dragon-nines/README.en.md) · dragon · nine resemblances | The dragon-painting mnemonic "three pauses, nine resemblances" is itself a nine-item part table | **5 periods delivered** |
| 3 | A | [turtle-snake](subjects/turtle-snake/README.en.md) · turtle + snake | The "Black Tortoise" of the Four Symbols is a turtle-snake composite | **5 periods delivered** |
| 4 | A | [fish-bird](subjects/fish-bird/README.en.md) · fish + bird | *Zhuangzi*: in the Northern Sea there is a fish… it transforms into a bird (kun-peng) | **5 periods delivered** (schedule redone) |
| 5 | A | [deer-crane](subjects/deer-crane/README.en.md) · deer + crane | The traditional auspicious motif "deer and crane in spring" | **5 periods delivered** (mostly partial success) |
| 6 | B | [lichen](subjects/lichen/README.en.md) · lichen | **A lichen is itself a spliced organism** (a fungus + alga symbiont) | **5 periods delivered** (all 11 finals first choice) |
| 7 | B | [cordyceps](subjects/cordyceps/README.en.md) · cordyceps | The insect-and-fungus composite in the *Materia Medica* | **5 periods delivered** (all 11 finals first choice) |
| 8 | B | [flytrap-fang](subjects/flytrap-fang/README.en.md) · Venus flytrap + animal organs | A plant growing animal organs (teeth / eyes / tongue) | **5 periods delivered** (all 11 finals first choice) |
| 9 | B | [flower-bird](subjects/flower-bird/README.en.md) · flower + bird | "Flower-and-bird" is the basic unit of Chinese painting | **5 periods delivered** (all 12 finals first choice) |
| 10 | B | [tree-beast](subjects/tree-beast/README.en.md) · tree + beast | Bark ↔ beast hide, roots ↔ feet, growth rings ↔ bone | **5 periods delivered** |
| 11 | C | [wing-atlas](subjects/wing-atlas/README.en.md) · wing · atlas | Fix one bird and **add one more pair** beyond the original wings (a new pair in an empty slot) | **5 periods delivered** (all 11 finals first choice) |
| 12 | C | [horn-atlas](subjects/horn-atlas/README.en.md) · horn · atlas | Fix one **hornless** horse and grow five kinds of "horn" in turn | **5 periods delivered** (**zero failures**, mean 5.00) |

> **One contact sheet per period** (`make_sheet.sh period`), **one contact sheet per sub-theme** (`make_sheet.sh subject`);
> to generate everything at once use `bash make_sheet.sh all`.

## 4. Execution Plan

| Stage | Engine | Purpose |
|------|------|------|
| Targeting | Z-Image-Turbo (~10 s/image, **no negative prompt**) | try sentence patterns, fix composition, control cost |
| Final | Qwen-Image 2512 (6–13 min/image, **real negatives**) | material and anatomical detail, suppress what must not appear |
| Structure lock | [image-edit-comfyui](../../skills/image-edit-comfyui/SKILL.md) (ControlNet) | when the prompt cannot hold it down, lock the body structure with a control image |

> ⚠️ **On an engine without negative prompts there is no solution for "what to remove"** (both the positive `no X` and
> `exactly one X` were measured ineffective). Such needs must switch to Qwen, or use a ControlNet structure lock. See
> [the sub-theme's first-round diagnosis](subjects/cat-eagle/rounds/r02.md).

## 5. Output Log (across sub-themes)

| Sub-theme | Period | Finals | Content | Record |
|--------|----|--------|------|------|
| cat-eagle | period-01 | 3 (+2 controls) | Owl: one image for each of the three splicing semantics | [period-01](subjects/cat-eagle/period-01/README.en.md) |
| cat-eagle | period-02 | 3 | Eagle with beast ears and beast tail: eagle base + cat ears / cat tail (dusk wetland · warm side-backlight · eye-level 400mm) | [period-02](subjects/cat-eagle/period-02/README.en.md) |
| cat-eagle | period-03 | 3 | Winged cat: cat base + eagle wings / eagle tail feathers (post-rain woodland · backlight · wide-angle low camera wingspan) | [period-03](subjects/cat-eagle/period-03/README.en.md) |
| cat-eagle | period-04 | 2 | Whiskered eagle: eagle base + cat whiskers / ears + whiskers (dark background · single-side light · face-on close-up) | [period-04](subjects/cat-eagle/period-04/README.en.md) |
| cat-eagle | period-05 | 3 | Thrice eagle-ized cat: cat base + eagle neck ruff / tail feathers / wings (snowfield rain mist · long-lens compression) | [period-05](subjects/cat-eagle/period-05/README.en.md) |
| dragon-nines | period-01 | 2 | Horned snake: snake base + deer antlers / antlers + ox ears | [period-01](subjects/dragon-nines/period-01/README.en.md) |
| dragon-nines | period-02 | 2 | Clawed lizard: lizard base + eagle talons (partial) / eagle talons + tiger paws | [period-02](subjects/dragon-nines/period-02/README.en.md) |
| dragon-nines | period-03 | 2 | Fish-scaled snake: first free the base's scale slot, then transplant fish scales | [period-03](subjects/dragon-nines/period-03/README.en.md) |
| dragon-nines | period-04 | 2 | Composite dragon: lizard base + 3~4 stacked parts (antlers / ears / talons / paws) | [period-04](subjects/dragon-nines/period-04/README.en.md) |
| dragon-nines | period-05 | 2 | Dragon-head close-up (finale): snake base + deer antlers / ox ears (+ fish scales), the only close-up in the whole sub-theme | [period-05](subjects/dragon-nines/period-05/README.en.md) |
| turtle-snake | period-01 | 3 | Snake-necked turtle: turtle base + snake neck N1 (all three seeds succeeded) | [period-01](subjects/turtle-snake/period-01/README.en.md) |
| turtle-snake | period-02 | 3 | Snake-tailed turtle: turtle base + snake tail N2 (wetland mud bank · eye level) | [period-02](subjects/turtle-snake/period-02/README.en.md) |
| turtle-snake | period-03 | 3 | Coiled turtle: turtle base + snake body coiled around it (three phrasings, rule 81) | [period-03](subjects/turtle-snake/period-03/README.en.md) |
| turtle-snake | period-04 | 2 | Neck and tail complete: N1+N2 stacked across regions | [period-04](subjects/turtle-snake/period-04/README.en.md) |
| turtle-snake | period-05 | 2 | **Black Tortoise** (finale): neck + tail + coil, all three on one body, dusk water-surface silhouette | [period-05](subjects/turtle-snake/period-05/README.en.md) |
| fish-bird | period-01 | 2 | **Leaping out of the water**: fish + bird wings, just clear of the water, the splash not yet fallen | [period-01](subjects/fish-bird/period-01/README.en.md) |
| fish-bird | period-02 | 3 | **Half out of water**: the waterline crosses the body, the half-open wing on the side above water | [period-02](subjects/fish-bird/period-02/README.en.md) |
| fish-bird | period-03 | 2 | **Fully clear of the water, both wings spread**: high-side view, backlight rimming the feathers | [period-03](subjects/fish-bird/period-03/README.en.md) |
| fish-bird | period-04 | 2 | **Skimming low over the water**: long-lens compression, flat light on grey water | [period-04](subjects/fish-bird/period-04/README.en.md) |
| fish-bird | period-05 | 2 | **Kun-peng** (finale): dusk sea surface, backlit silhouette, fully spread bird wings | [period-05](subjects/fish-bird/period-05/README.en.md) |
| deer-crane | period-01 | 2 | Long-necked deer: deer base + crane neck (partial) | [period-01](subjects/deer-crane/period-01/README.en.md) |
| deer-crane | period-02 | 2 | Crane-legged deer: deer base + crane legs (partial, with an occupied-version control) | [period-02](subjects/deer-crane/period-02/README.en.md) |
| deer-crane | period-03 | 1 | Crane-tailed deer: **the only fully successful piece**, hit rate 1/4 | [period-03](subjects/deer-crane/period-03/README.en.md) |
| deer-crane | period-04 | 2 | Neck and legs complete: G1+G2 stacked across regions | [period-04](subjects/deer-crane/period-04/README.en.md) |
| deer-crane | period-05 | 2 | Deer and crane in spring (finale): neck + legs + tail, all three on one body | [period-05](subjects/deer-crane/period-05/README.en.md) |
| lichen | period-01 | 3 | Crustose lichen: mycelium + crustose form + green algal cells (a cross-kingdom piece lands 100% for the first time) | [period-01](subjects/lichen/period-01/README.en.md) |
| lichen | period-02 | 2 | Foliose lichen: leaf-like lobes on bark + algal filaments | [period-02](subjects/lichen/period-02/README.en.md) |
| lichen | period-03 | 2 | Fruticose lichen: branching fruticose thallus backlit on the tundra | [period-03](subjects/lichen/period-03/README.en.md) |
| lichen | period-04 | 2 | Algal layer visible: green spheres and algal filaments in a pseudo-section (a presentation rescue period) | [period-04](subjects/lichen/period-04/README.en.md) |
| lichen | period-05 | 2 | Symbiont (finale): a composite lichen of foliose + fruticose + algal cells | [period-05](subjects/lichen/period-05/README.en.md) |
| cordyceps | period-01 | 3 | Mycelium-covered insect: moth larva + mycelial covering (body surface freed) | [period-01](subjects/cordyceps/period-01/README.en.md) |
| cordyceps | period-02 | 2 | Single stroma: a club-shaped stroma rising out of the insect body | [period-02](subjects/cordyceps/period-02/README.en.md) |
| cordyceps | period-03 | 2 | Multiple stromata: four stromata growing at once | [period-03](subjects/cordyceps/period-03/README.en.md) |
| cordyceps | period-04 | 2 | Stromata and spores: powdery spores coating the stroma surface | [period-04](subjects/cordyceps/period-04/README.en.md) |
| cordyceps | period-05 | 2 | **Cordyceps** (specimen-photo finale): mycelium + stromata + spores, neutral background with ring light | [period-05](subjects/cordyceps/period-05/README.en.md) |
| flytrap-fang | period-01 | 3 | Toothed Venus flytrap: white beast teeth extruded along the trap margin (margin teeth freed) | [period-01](subjects/flytrap-fang/period-01/README.en.md) |
| flytrap-fang | period-02 | 2 | Eyed Venus flytrap: an animal eye grows out of the leaf surface | [period-02](subjects/flytrap-fang/period-02/README.en.md) |
| flytrap-fang | period-03 | 2 | Tongue-flicking Venus flytrap: a pink beast tongue unrolls from the trap cavity | [period-03](subjects/flytrap-fang/period-03/README.en.md) |
| flytrap-fang | period-04 | 2 | Teeth and tongue complete: fangs + beast tongue on one body (post-rain hard side light) | [period-04](subjects/flytrap-fang/period-04/README.en.md) |
| flytrap-fang | period-05 | 2 | Carnivorous plant (finale): teeth + eye + tongue, dawn mist swamp backlight | [period-05](subjects/flytrap-fang/period-05/README.en.md) |
| flower-bird | period-01 | 3 | Plume-stemmed flower: a sheaf of plumes rises from the flower's centre (magnolia morning dew) | [period-01](subjects/flower-bird/period-01/README.en.md) |
| flower-bird | period-02 | 2 | Down-hearted flower: the stamens are read as down feathers (partial) | [period-02](subjects/flower-bird/period-02/README.en.md) |
| flower-bird | period-03 | 2 | Plumes and down complete: plume feathers + downy centre on one body (dark background hard light) | [period-03](subjects/flower-bird/period-03/README.en.md) |
| flower-bird | period-04 | 3 | Down and plumes of the lily: switched flower species, hit rate fell to 1/2, then extra takes | [period-04](subjects/flower-bird/period-04/README.en.md) |
| flower-bird | period-05 | 2 | Flower-and-bird (finale): every flower on the loaded branch grows a plume | [period-05](subjects/flower-bird/period-05/README.en.md) |
| tree-beast | period-01 | 3 | Beast-hided tree: the trunk is covered with beast hide / fur (bark freed) | [period-01](subjects/tree-beast/period-01/README.en.md) |
| tree-beast | period-02 | 2 | Horned tree: a pair of huge curved horns borne on the trunk | [period-02](subjects/tree-beast/period-02/README.en.md) |
| tree-beast | period-03 | 2 | Hide and horns complete: beast hide + beast horns (post-rain hard light) | [period-03](subjects/tree-beast/period-03/README.en.md) |
| tree-beast | period-04 | 2 | Hide and horns of dead wood: still works after changing the base (standing dead tree) | [period-04](subjects/tree-beast/period-04/README.en.md) |
| tree-beast | period-05 | 2 | Tree-beast (finale): dusk backlit silhouette, **the beast feet never touch the ground** | [period-05](subjects/tree-beast/period-05/README.en.md) |
| wing-atlas | period-01 | 3 | **Baseline**: the unified base bird (no transplant piece, the reference for the four later parts) | [period-01](subjects/wing-atlas/period-01/README.en.md) |
| wing-atlas | period-02 | 2 | Four wings (membrane): add a pair of insect membranous wings on the back | [period-02](subjects/wing-atlas/period-02/README.en.md) |
| wing-atlas | period-03 | 2 | Four wings (skin): add a pair of bat skin wings on the back | [period-03](subjects/wing-atlas/period-03/README.en.md) |
| wing-atlas | period-04 | 2 | Four wings (flying-fish fins): add a pair of long flying-fish fins on the back (carrying "flight" semantics of its own) | [period-04](subjects/wing-atlas/period-04/README.en.md) |
| wing-atlas | period-05 | 2 | Four wings (crane feathers): add a pair of white crane wings on the back (finale) | [period-05](subjects/wing-atlas/period-05/README.en.md) |
| horn-atlas | period-01 | 3 | **Baseline**: the hornless horse (no transplant piece, the reference for the four later parts) | [period-01](subjects/horn-atlas/period-01/README.en.md) |
| horn-atlas | period-02 | 2 | Deer antlers: a pair of branching antlers grows from the top of the forehead | [period-02](subjects/horn-atlas/period-02/README.en.md) |
| horn-atlas | period-03 | 2 | Ox horns: a pair of thick ox horns grows from the top of the forehead | [period-03](subjects/horn-atlas/period-03/README.en.md) |
| horn-atlas | period-04 | 2 | Ram horns: a pair of curled ram horns grows from the top of the forehead | [period-04](subjects/horn-atlas/period-04/README.en.md) |
| horn-atlas | period-05 | 2 | Narwhal tusk + rhino horn (finale): frosty morning face-on close-up | [period-05](subjects/horn-atlas/period-05/README.en.md) |

## 6. Checklist

- [ ] **Within a period** habitat/light/camera/canvas are constant (preserving that period's control), **across periods** they all differ (each period has an identity)
- [ ] **Every round has been run through `score.py`**, and the period directory holds only ✅ shots (⚠️ alternates and ❌ never enter)
- [ ] The period directory contains **no** work-in-progress (two heads / extra individuals / regression / obviously fake)
- [ ] Every final's provenance can be found in `manifest.json` (seed / prompt_id / prompt)
- [ ] This round has a **same-round base control shot** (otherwise the objective metrics are unusable)
- [ ] The period contact sheet from `bash make_sheet.sh period <期目录>` is up to date
- [ ] The **cross-period overview sheet** from `bash make_sheet.sh subject <子主题>` (including the `sheet-thumb.jpg` thumbnail) is up to date
- [ ] The thumbnails embedded in [`SUMMARY.md`](SUMMARY.en.md) match `subjects/*/sheet-thumb.jpg` (just re-run `make_sheet.sh all`)
- [ ] `work/` has not slipped into the repo (`git status` clean)
- [ ] Round records are written into `subjects/<子>/rounds/`

---

## 9. Repository Size Maintenance (**read this first whenever a push fails**)

This project is an **image-heavy** repository: each delivered sub-theme adds roughly 25–30MB (final PNGs + controls + contact sheets + audit sheets).
Gitee's repository quota is **1024MB**; when it is exceeded, `git push` is **rejected by the pre-receive hook**
(`Push rejected for repository [size exceeds limit]`)——**this is not a local problem**.

| Symptom | Cause | Action |
|------|------|------|
| push rejected, message `Repo size: … exceeds quota 1024MB` | old version objects have accumulated in the remote history (a local `git gc` does not affect the remote) | open **<https://gitee.com/thz_summer/gits/settings#git-gc>** and click **Repository GC** once, then push again |

**Cadence**: run GC roughly every **2–3 sub-themes** (one GC compresses the remote from ~1400MB back to ~460MB).

**Why not save size by "converting the finals to JPEG"**: measured JPEG q2 introduces into the same image an
**average channel difference ≈ 1.21**, and this repo's threshold "a region difference < 1.5 means the transplant sentence was a no-op" sits right beside it—
the noise floor would eat the criterion outright. So **contact sheets / audit sheets use JPEG, while finals and controls must be PNG**
(see [image-tools/SKILL.md](../../skills/image-tools/SKILL.md)).

## Document Revision History

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Refactored from `owl-splice` into a splicing project: project → sub-theme (by animal pair) → period (finals only); added `curate.py` and the finals threshold, moved `work/` out of the repo | 小七 |
| 2026-10-05 | **v1.0** | `horn-atlas` **five parts completed (zero failures)** —— **all 12 sub-themes / 60 periods / 135 finals delivered**; added the [`SUMMARY.md`](SUMMARY.en.md) project-wide summary (mechanism finding master table 51–110 / negative-results list / follow-up suggestions); added rules 109–110 | 小七 |
| 2026-10-05 | v0.14 | `wing-atlas` **five parts completed** (Group C 1/2, all 11 finals first choice); proposed **rule 107 (the semantic category must match the landing site's function, fish pectoral fins 0%)** and 108 (the baseline part of an atlas) | 小七 |
| 2026-10-05 | v0.13 | `tree-beast` **five periods completed** (**Group B finished**, 11 finals); **the negative result that beast feet are 0%**; added rules 105/106 (two independent thresholds / whether changing the base lowers the hit rate depends on the nature of the landing site) | 小七 |
| 2026-10-05 | v0.11 | `flower-bird` **five periods completed** (Group B 4/5, all 12 finals first choice); petals a third time confirm "the canonical structure cannot be swapped out"; added rules 102–104 (changing the base requires re-validating the hit rate / read the phrasing together with the landing site / **mechanism limits often give a better composition**) | 小七 |
| 2026-10-05 | v0.10 | `flytrap-fang` **five periods completed** (Group B 3/5, all 11 finals first choice); proposed **rule 99 (the criterion rests on the landing site, not the whole)**, 100 (boundary appendages ≈ attributes), 101 (the seam decides credibility · hypothesis) | 小七 |
| 2026-10-05 | v0.9 | `cordyceps` **five periods completed** (Group B 2/5, all 11 finals first choice); added rules 96–98 (**attributes can be freed, structures cannot**, pieces growing from the body surface need no bearing structure, changing the presentation medium = a finale upgrade) | 小七 |
| 2026-10-05 | v0.8 | `lichen` **five periods completed** (Group B started, all 11 finals first choice); proposed **rule 92 (the base's morphological freedom determines transplant difficulty)** and 93–95 (scale is presentation / presentation can rescue a weak period / a control that already does half the work must lose points) | 小七 |
| 2026-10-05 | v0.7 | `deer-crane` **five periods completed** (Group A finished, 9 finals, mostly partial success); added rules 89–91 (**change the shape, not the material** / an empty slot is not sufficient / **different shapes first**); fixed the `--force` semantics of `curate.py` (it used to merge old final entries with new ones, producing two same-source entries in a period directory) | 小七 |
| 2026-10-04 | v0.6 | `fish-bird` **five periods completed** (11 finals); discovered rules 85–88 (**habitat is a hard constraint**, scene compatibility judged per region, canonical structures cannot free a slot, a "single usable part" can also carry a sub-theme), and on that basis changed the schedule's main axis to "stages of leaving the water" | 小七 |
| 2026-10-04 | v0.5 | `turtle-snake` **five periods completed** (13 finals, including the "Black Tortoise" finale); added rules 81–84 (spatial-relation phrasing, suspect the phrasing first, freeing a slot in tiers, multi-take validation) | 小七 |
| 2026-10-04 | v0.4 | `cat-eagle` periods 02–05 **presentation redone** (each of the five periods has an identity); based on R10–R17 added rules 79/80 (a pose sentence must not mention the part; the presentation layer is not neutral); `cat-eagle` period-06 eagle-headed cat formally scrapped | 小七 |
| 2026-10-04 | v0.3 | `dragon-nines` five periods completed (period 05 [dragon-head close-up]); based on measurements rules 73–78 **re-ordered the period content of 7 sub-themes** (clearing head parts and carrier-less parts), rewrote `eye-atlas` as `horn-atlas` and changed `wing-atlas` to "a second pair of wings" | 小七 |
| 2026-10-04 | v0.2 | Renamed `animal-splice` → `bio-splice`: the concept expanded from "animal splicing" to "biological splicing" (plants/fungi/algae/lichens can be base or donor), sub-themes expanded to 12; final prefix `as-*` → `bs-*`; `make_sheet.sh` gained an `all` mode | 小七 |
| 2026-10-05 | v0.12 | Added the "Repository Size Maintenance" section: Gitee's 1024MB quota and the cadence for handling Repository GC | 小七 |
| 2026-10-05 | v1.1 | The deliverables convention gained the "sub-theme contact-sheet thumbnail" `sheet-thumb.jpg` (`make_sheet.sh` produces it as well); the SUMMARY first page embeds 12 thumbnails | 小七 |
