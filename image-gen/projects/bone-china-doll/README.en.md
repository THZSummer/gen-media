# Bone China Princess (骨瓷国公主)

> 🌐 Language: **English** | [中文](README.md)

> Back to [project index](../README.en.md) ｜ Skills in [../../skills/text-to-image-comfyui/SKILL.md](../../skills/text-to-image-comfyui/SKILL.md)
> **Six-stage iteration** (the directory name remains `bone-china-doll`; the theme has changed):
> - **Stage 1 R1–R6**: 5 images per round, Z-Image-Turbo, working out composition/ratio/material vocabulary
> - **Stage 2 R7–R16**: 3 images per round, switched to Qwen-Image 2512, focused on detail richness and realism
> - **Stage 3 R17–R21**: **theme changed to "Bone China Princess" — Eastern classical beauty** (Eastern classical face / hair bun / crossed-collar gold-woven robe / jade and gold filigree)
> - **Stage 4 R22–R26**: **de-figurinization + half-real half-bone-china** — from "a doll in a museum" to **a living princess**,
>   skin **half-real half-bone-china** (fired glaze sheen + real human blood colour + named glaze defects), garments **half-gauze half-bone-china** (several layers of fine gauze, translucent, edges crisp like porcelain);
>   prompt changed to **Chinese baimiao in the brushwork of a Dream of the Red Chamber entrance + an English material layer**
> - **Stage 5 R27–R29**: **natural makeup + languid daily-life poses** — remove the deliberate blush, replace it with natural blood colour;
>   composition changed to **full-body** daily-life moments (sitting slantwise on a low couch / lying on one's side / lying prone / half-reclining with tea / hugging knees by the window / dozing over a desk);
>   key techniques: **pose sentence placed up front + minimal base prompt + canvas matched to the pose**
> - **Stage 6 R30–R32**: **material recovery** — a re-check found that phase-5's bone china texture had been cut away together with R28's "trimming of the base prompt"
>   (the same mechanism as R11). R30 moved phase-4's named defect list back into the short pose base prompt; R31 restored
>   the `crisp specular highlights` glaze sentence and switched to a **tight-portrait audit sheet**; R32 changed the material assertion from
>   "half real half porcelain" to "the material is bone china" — a three-step ladder at the same seed proving that **the material assertion is a lever with adjustable dosage**
> - **Stage 7 R33–R34**: **return of the princess temperament** — user feedback "she has no princess temperament, a bit old-looking";
>   the audit found that R28's cut had also removed **the whole block of facial description** (facial features/eyebrows and lashes/blood-colour words all had 0 occurrences in the base prompt).
>   R33 restored phase-2's facial feature definition + a Chinese temperament sentence and removed the blanket blush ban; R34 moved **the age anchor up front** into the subject,
>   changed `adult`→`youthful`, added anti-aging words to the negative → the old look was essentially eliminated

> - **Stage 8 R35**: **attribution correction + glaze recovery** — auditing R25 overturned R34's attribution (the real culprit for the old look is `adult`,
>   not the defect list); after removing the anti-aging negatives, **the glaze returned without the age bouncing back**, yielding a landing site where "young + princess temperament + porcelain surface" all hold at once

>
> Every round: generate → self-check → optimize prompt/parameters/engine → next round, all recorded in [`docs/`](docs/).
> ⚠️ **The stage-2 quality highland is R8–R10**: R11 and R12 are both degeneration rounds (causes located and distilled into a negative checklist).
> **Stage-2 main final R10 `window-light`** ｜ **Stage 3 [`out/final-set-east/`](out/final-set-east/)** ｜
> **Stage 4 [`out/final-set-gauze/`](out/final-set-gauze/)** ｜
> **Stage 5 [`out/final-set-life/`](out/final-set-life/) (current direction)**.
> Conclusions in [R16](docs/r16.en.md) / [R21](docs/r21.en.md) / [R26](docs/r26.en.md) / [R29](docs/r29.en.md) / [R30](docs/r30.en.md) / [R31](docs/r31.en.md) / [R32](docs/r32.en.md) / [R33](docs/r33.en.md) / [R34](docs/r34.en.md) / [R35](docs/r35.en.md).

> 📦 **Size convention (2026-10-05)**: to push the repository size back below Gitee's warning threshold,
> **per-round intermediate artifacts are no longer committed** (local files are kept; fixed seeds make them reproducible):
> - `out/r1 … out/r35/`: each round's prompt and conclusions are fully preserved in `docs/rNN.md`, and the images can be regenerated from that round's seed

> So the related links in this document point to **local files** that do not exist in the remote repository.

---

## 1. Project background

- **Goal**: generate images of a bone china princess (fine bone china doll) that are **rich in detail, strongly realistic and carry an Eastern classical princess temperament**
- **Theme**: **Eastern classical beauty** (from R17) — Eastern classical face, black hair in a high bun, crossed-collar wide-sleeve gold-woven robe, cloud collar, jade and gold filigree jewellery
- **Generation method**: ComfyUI (`192.168.3.5:18000`) × Qwen-Image 2512 (from R7; R1–R6 used Z-Image-Turbo)
- **Driver script**: [`run_round.py`](run_round.py) (`python3 run_round.py <round>`, prompts versioned inside the script)

### Acceptance criteria (scored item by item every round)

| Dimension | Pass line |
|------|--------|
| **Detail richness** | Gold-woven and embroidered thread patterns, pearl strings, gold filigree and jade carving detail, hand-painted brushwork discernible, not smeared into one blur |
| **Realism** | Bone china material characteristics hold: translucency, glaze highlights; **eyeballs have iris + pupil + catchlight**; skin is fired lustre rather than plastic matte |
| **Eastern classical / princess** | **Eastern classical face** (willow-leaf eyebrows, slightly upturned almond eyes, fine straight nose bridge, cherry lips), black hair in a high bun, hairpin and buyao, crossed-collar wide-sleeve gold-woven robe, cloud collar, jade belt, full bearing and not cheap-looking |
| **No distortion** | Finger count/proportion normal, shoulders and neck not cut badly, pearl chain not floating, no extra limbs or floating fragments |
| **Image** | Composition complete (hands not cut off), light ratio with hierarchy, background not competing with the subject, no lighting fixture in frame |

---

## 2. Method selection

| Step | Skill/tool used | Notes |
|------|--------------|------|
| Image generation (R1–R6) | [text-to-image-comfyui](../../skills/text-to-image-comfyui/SKILL.md) → `scripts/comfyui_gen.py` | Z-Image-Turbo; ⚠️ the negative is `ConditioningZeroOut`, **no negative prompt** |
| Image generation (R7–R21) | Same as above → `scripts/comfyui_qwen.py` | **Qwen-Image 2512**; ✅ supports real negative prompts; noticeably stronger on detail/realism, but about 13 min/image (about 50 min at 3.43MP) |
| Round driver | [`run_round.py`](run_round.py) | Dual engine, switched via the `engine` field; **all prompts are versioned inside the script**; supports per-image overrides of `size/steps/cfg/timeout` |
| **True macro (stage 2)** | [`make_macro.sh`](make_macro.sh) | **Cropping method** (not generation): crop the tiara/wrist joint from the R14 3.43MP final |
| **True macro (stage 3)** | [`make_macro_east.sh`](make_macro_east.sh) | **Cropping method**: crop 5 Eastern craft macros from the R20 base image (buyao hairpin / yingluo necklace / jade bi disc / porcelain slipper / ball joint) |
| **True macro (stage 4)** | [`make_macro_gauze.sh`](make_macro_gauze.sh) | **Cropping method**: crop **skin macros** from the R25 **2048²** base image (glaze sheen / red flush / pinholes), and **gauze macros** from R26 (warp and weft / translucency / gauze edge) |

---

## 3. Where the prompt originals live

| Layer | Location | Content |
|----|------|------|
| 📄 **Verbatim digest (read this first)** | **[docs/prompts-all.md](docs/prompts-all.en.md)** | **All prompts + negatives for 29 rounds**, verbatim originals + seed + file names + per-image size overrides (already wrapped at clause boundaries, for easy reading and round-by-round comparison) |
| Authoritative source | the `BASE*` constants + `ROUNDS` / `LEGACY_ROUNDS` in [`run_round.py`](run_round.py) | The strings actually submitted to ComfyUI |
| Readable documentation | [`docs/rN.md`](docs/) | Per-round change notes, BASE originals, per-image appended fragments, self-check conclusions |
| Machine record | `out/rN/round.json` | File name / seed / prompt_id / engine / parameters / **prompt original** |
| **Execution-graph retention** | `out/rN/<image name>.api.json` + `out/rN/requests.jsonl` | **The complete graph actually submitted to ComfyUI** (verbatim prompt, sampler, model, seed) + request ledger; the 35 records of R3–R11 were backfilled from the server history, and R12–R21 are written automatically by the skill's default retention |
| Server side | `GET /history/{prompt_id}` | The complete graph ComfyUI actually executed (final basis) |

> Regenerate the digest: `python3 run_round.py --prompts docs/prompts-all.md`
> The line breaks inside the digest are **layout only**: when the line ends with an ASCII character, that break equals one space; otherwise there was originally no character at the break;
> `unwrap_prompt()` in `run_round.py` implements exactly this rule, and generation asserts clause by clause that "restored == original" (all 114 segments pass).
> Get the verbatim single-line original: `python3 run_round.py <N> --dry`, or read `out/rN/round.json`.
> Verified: **all 6 images of R16 and R21** — the `CLIPTextEncode` text executed on the server matches this archive **character for character**
> (positive 2523–2699 characters / negative 360 characters).
> On the skill side (`comfyui_gen.py` / `comfyui_qwen.py`), since v1.2 retention is **on by default**: every generation writes `<prefix>.api.json` + `requests.jsonl`, so later rounds need no extra operation.

---

## 4. Iteration record (each round is its own document)

| Round | Theme | Parameters | Conclusion summary | Record |
|------|------|------|----------|------|
| R1 | Baseline (museum-quality porcelain princess) | 1024² · 8 steps · seed 100 · batch 5 | All the princess elements are present, but a **plastic doll feel**, flat painted eyes, square composition cutting off the hands | [docs/r1.md](docs/r1.en.md) |
| R2 | Material realism + glass eyeballs + 3:4 | 1024×1360 · seed 200 · batch 5 | **Catchlight/iris achieved**; background softbox in frame; face shape too infantile | [docs/r2.md](docs/r2.en.md) |
| R3 | Five camera positions + character consistency lock | 1024×1360 · seed 300/310/320/330/340 (per image) | **Camera diversity achieved**; facial colour-block artifacts, pearl chain floating, lighting fixture still in frame | [docs/r3.md](docs/r3.en.md) |
| R4 | Remove fixture words + consolidate pearls + adult proportions | 1024×1360 · seed 400–440 (per image) | **No more fixture in frame, single pearl strand, no floating fragments**; face shape still infantile | [docs/r4.md](docs/r4.en.md) |
| R5 | Change the `figurine` wording + adult facial features + steps 12 | 1024×1360 · steps 12 · seed 500–540 | **Adult princess temperament achieved** (the qualitative-change round), fixed as BASE5 | [docs/r5.md](docs/r5.en.md) |
| R6 | Final round (z-image stage): steps 16 + microscope-level detail | 1024×1360 · steps 16 · seed 600–640 | **Richest detail**: hand-painted rose patterns, porcelain flower bouquet, crystal bead ornaments | [docs/r6.md](docs/r6.en.md) |
| R7 | **Engine switch → Qwen-Image 2512** (3 images/round) | 1024×1360 · steps 24 · cfg 3.0 · seed 700–720 | **Generational leap**: lace warp and weft, embroidery thread patterns, gem settings, ball-joint seams; real negative prompts now usable | [docs/r7.md](docs/r7.en.md) |
| R8 | Higher resolution + sculptural lighting + gold-thread brocade | 1152×1536 · steps 28 · cfg 3.2 · seed 800–820 | The gown upgrades to a coronation gown and the light ratio gains a sculptural feel; the face is slightly CGI-smooth | [docs/r8.md](docs/r8.en.md) |
| R9 | Microscopic glaze + anti-CGI + macro composition | 1152×1536 · steps 30 · cfg 3.5 · seed 900–920 | Folding-fan weave / gold thread embroidery / bead settings clear; "microscopic glaze" was not executed | [docs/r9.md](docs/r9.en.md) |
| R10 | Jewelry metalwork + fabric macro + window light | 1280×1712 · steps 32 · cfg 3.5 · seed 1000–1020 | The detail level stays consistently very high, but **the three compositions degenerate into near-identical frames** (Qwen ignores the macro cropping instruction) | [docs/r10.md](docs/r10.en.md) |
| R11 | Composition up front + deliberately pull the three apart | 1280×1712 · steps 32 · cfg 3.5 · seed 1100–1120 | ⚠️ **Degeneration round**: cropping succeeded, but to let cropping dominate, the three material passages "microscopic glaze / jewelry metalwork / fabric macro" were deleted wholesale → clothing went flat, macros had no eyes, hands with ten fingers | [docs/r11.md](docs/r11.en.md) |
| R12 | De-CGI (describe physical glaze + a single hand + save the eyes) | 1280×1712 · steps 32 · cfg 3.5 · seed 1200–1220 | ⚠️ **Half degeneration**: `one crisp key light` caused **a lighting fixture to be painted into the frame**, skin became "wet plastic" with broad highlights, the face was infantilized; only `hand-single` worked (single hand with five fingers + ball-joint seam + clean nails) | [docs/r12.md](docs/r12.en.md) |
| R13 | **Return to the `BASE_Q10` baseline** + true-macro boundary test | 1280×1712 · steps 32 · cfg 3.5 · seed 1300–1320 | ✅ **A control experiment proves the R10 level reproduces across seeds** (the quality comes from the material vocabulary, not luck); ❌ with the full material vocabulary **macros are still unattainable** → establishes the hard constraint: **vocabulary volume and cropping cannot be had at the same time** | [docs/r13.md](docs/r13.en.md) |
| R14 | Resolution ablation (same prompt, same seed, only resolution varies) | 2.19 / 3.43 / 4.30 / 4.92 MP · same seed 1400 | ❌ **Negative result**: pixels up 2.25×, **detail density (bytes/px) essentially flat**; 4.92MP is actually the lowest and takes 5× as long → **resolution is not a detail lever**. ✅ Side finding: 8GB of VRAM can run 4.92MP without OOM | [docs/r14.md](docs/r14.en.md) |
| R15 | **Control composition with the canvas aspect ratio** + true macro by cropping | 1:2 / 3:4 / 1:1 · steps 32 · seed 1500–1520 | ✅ **Full-figure (1:2) and seated (1:1) succeeded** — the project's first genuine camera diversity; ❌ `seen from behind` was ignored → conclusion: **composition comes from canvas shape, viewpoint via wording does not work**. ✅ True macro solved by switching to **cropping** (`make_macro.sh`) | [docs/r15.md](docs/r15.en.md) |
| R16 | **Final round**: three-composition delivery set + steps 40 | 3:4 / 1:2 / 1:1 · **steps 40** · seed 1600–1620 | ✅ **The three compositions are completely different** (the definitive fix for the R10/R13 "three near-identical frames" defect); steps 40 shows no degeneration. Produced [`out/final-set/`](out/final-set/) (portrait/full-figure/seated + 2 macros) | [docs/r16.md](docs/r16.en.md) |
| **R17** | **Opening of stage 3: theme change → Bone China Princess / Eastern classical beauty** | 3:4 / 1:2 / 1:1 · steps 32 · seed 1700–1720 | ✅ **Landed in one round**: only the cultural elements were replaced while the material core inherits `BASE_Q10` verbatim → Eastern classical face, black hair in a high bun, gold-set jade buyao, crossed-collar wide-sleeve gold-woven robe, cloud collar and gold-set jade belt all landed with no loss of realism. ⚠️ `full-figure` only reaches the waist | [docs/r17.md](docs/r17.en.md) |
| R18 | Fix the full-figure (**trim the clothing list + push the canvas to 1:2.33**) + add `璎珞`/cloud-collar colour matching | 1280×1712 / **880×2048** / 1600×1600 · seed 1800–1820 | ✅ **Full-figure fixed** (hair bun → porcelain slippers, carved wooden stand) → confirms **"a long clothing list pulls the camera in" is unrelated to the theme**; `璎珞` and the ivory cloud collar landed. ⚠️ `花钿` was not drawn | [docs/r18.md](docs/r18.en.md) |
| R19 | **Tang-style form variant** (high-waist ruqun + draped silk gauze + huadian) | 1280×1712 / 880×2048 / 1600×1600 · seed 1900–1920 | ✅ Replacing just **one form sentence** produced a second Eastern silhouette (high waist with a fitted bodice, gauze trailing on the ground); material/face/jewellery inherited stably. ⚠️ `花钿` **failed all three times** → conclusion: **subtle facial makeup decoration is unreliable; named objects are reliable** | [docs/r19.md](docs/r19.en.md) |
| R20 | Eastern craft macros (**cropping method**, no new wording) | 1600×2144 / 1600×1600 / 1200×2560 · seed 2000–2020 | ✅ Cropped 5 craft macros: **gold-set jade buyao / yingluo + coiled gold embroidery / jade bi disc / celadon-glazed porcelain slipper / wrist ball joint (with metal tension pin)**. ⚠️ Scene props (round fan / screen / wooden side table) were not executed this round → less reliable than named jewellery | [docs/r20.md](docs/r20.en.md) |
| R21 | **Eastern final round**: medium-density base + three compositions | 3:4 / **880×2048** / 1:1 · seed 2100–2120 | ✅ **R19's "either-or" has a middle solution**: keeping "the form sentence + 3–5 key ornaments" holds both the full-body composition and the clothing layering. Produced [`out/final-set-east/`](out/final-set-east/) | [docs/r21.md](docs/r21.en.md) |
| **R22** | **Opening of stage 4: de-figurinization + Dream of the Red Chamber entrance brushwork (direct Chinese)** | 3:4 / 1:2 / 3:4 · seed 2200–2220 | ✅ **No longer looks like a figurine** (a living person + Boshan censer smoke / screen / yingluo all landed) → Chinese has extremely strong controllability over "objects and scenes".<br>❌ But it **deleted the bone china skin as well** (over-correction), and the makeup drifted toward a photo-studio look | [docs/r22.md](docs/r22.en.md) |
| R23 | **Mixed Chinese-English writing**: Chinese writes "what there is", English writes "what it is made of" | 3:4 / 1:2 / 3:4 · seed 2300–2320 | ✅ Makeup fixed (nearly bare-faced); ✅ the full-figure "a living person in an interior" is excellent.<br>❌ The English material passage was **diluted** by the 450-character Chinese passage, and the skin is still photo-studio-grade real-human skin | [docs/r23.md](docs/r23.en.md) |
| R24 | **Material up front** (the English material passage moved to the very front of the prompt) | same · seed 2400–2420 | ✅ **The glaze was finally obtained** (glaze sheen on the forehead/nose bridge, lustrous and translucent) → position-is-weight verified for the 3rd time.<br>❌ Side effect: **elf pointed ears** (`translucency of the ears` executed literally), skin too uniform, like a porcelain mask | [docs/r24.md](docs/r24.en.md) |
| R25 | **Named porcelain-surface defects + fix the pointed ears + 2048² square canvas** | 3:4 / 1:2 / **2048²** · seed 2500–2520 | ✅ **Skin meets the bar (half-real half-bone-china)**: glaze sheen + real human warm flush + **genuine pinholes/craters on the forehead**, orange-peel ripple, uneven glaze colour, fine polishing marks. ✅ Pointed ears gone | [docs/r25.md](docs/r25.en.md) |
| R26 | **Change only the clothing**: heavy gold weave → several layers of fine gauze (half-gauze half-bone-china) | 3:4 / 1:2 / 1:1 · seed 2600–2620 | ✅ **"Lightness" achieved**: several layers of gauze thin as cicada wings, translucent enough to show the layer beneath, the skirt trailing like smoke, **edges crisp with the sinew of porcelain**. Produced [`out/final-set-gauze/`](out/final-set-gauze/) | [docs/r26.md](docs/r26.en.md) |
| **R27** | **Natural makeup + languid full body** (sitting/prone/lying) | 3:4 / 2:1 / 1.56:1 · seed 2700–2720 | ✅ **Makeup fixed** (the deliberate circular blush is gone, only natural blood colour remains); ✅ relaxed expression.<br>❌ **All three full-body attempts failed** (still half-body); ❌ new artifact: **hands glowing orange** (`translucency ... of the fingertips`); ❌ a landscape canvas cannot force a reclining pose | [docs/r27.md](docs/r27.en.md) |
| R28 | **Pose up front + minimal base prompt (1802→635 characters) + 2.67:1** | 2048×768 ×2 / 1200×1600 · seed 2800–2820 | ✅ **All three achieved a true full body** (lying on one's side propping the cheek / lying prone with the feet raised / sitting slantwise with the chin on one hand); ✅ glowing hands gone → **position-is-weight verified for the 4th time**: the pose was not obtained by adding words but by **reducing competing description** | [docs/r28.md](docs/r28.en.md) |
| R29 | Wrap-up: three everyday moments + **restore the crossed collar/yingluo/jade belt** | 2048×768 ×2 / 1200×1600 · seed 2900–2920 | ✅ Half-reclining with tea / hugging the knees by the window / dozing over a desk all landed; ✅ proves a **short base prompt can fully carry named ornaments** without affecting the full-body composition. Produced [`out/final-set-life/`](out/final-set-life/) | [docs/r29.md](docs/r29.en.md) |
| **R30** | **Recover the material phase-5 lost**: move phase-4's named defect list back into the short pose base prompt | 2048×768 / 1200×1600 / 1600² · seed 3000–3020 | ✅ **Material density does not pull the camera in** (base prompt 776→1178, whole prompt 1254 ≈ the 1283 at which R27 failed, and all three are still full-body) → what pulls the camera in is the **clothing list**, not the total length; ✅ **the glaze sheen on the hands came back** (same-region crop vs R29).<br>❌ **The named defects were not executed**, in exchange for a more uniform surface; ❌ framing mistake on the square canvas (full body, face only ~180px, glaze cannot be judged) | [docs/r30.md](docs/r30.en.md) |
| **R31** | **Restore the `crisp specular highlights` glaze sentence + switch to a tight-portrait audit sheet** | 1200×1600 / **2048²** / 1280×1712 · seed 2910/2520/3030 | ✅ A strict **same-seed** ablation proves the material sentence really changes the skin (R29 warm matte → R31 cool with glaze sheen); ✅ produced **this project's best portrait** (2048² tight portrait).<br>❌ Side by side with the R25 audit sheet: **hard glaze sheen and pinholes are still absent** — "a real-human portrait + satin sheen" rather than a fired glaze. → The difference is localized to **assertion strength** | [docs/r31.md](docs/r31.en.md) |
| **R32** | **Change the material assertion** (`half real skin` → R25's `made of ... the material itself, not a mask` + `Her face is human; her skin is porcelain.`) | same as R31 · seed 2910/2520/3030 (fully controlled A/B) | ✅ **Monotonic progression along a three-step, same-seed ladder** (R29 matte real human → R31 satin sheen → R32 clear glaze) → the assertion is **a dosage lever with adjustable levels**; ✅ the R32 tight portrait **is the closest yet to the "half-real half-bone-china" brief**.<br>⚠️ It still does not reach R25's hard glaze sheen/pinholes — **but R25 is actually "more porcelain" than the brief**, and R32 lands in the middle, leaning porcelain | [docs/r32.md](docs/r32.en.md) |
| **R33** | **Restore the "face + bearing" removed by the same cut** (recover phase-2's facial feature definition + age anchor + Chinese bearing sentence + remove the blanket blush ban) | same as R32 · seed 2910/2520/3030 (same-seed A/B) | ✅ **Every item landed**: eyelashes in rows (`painted eyelashes`), eyebrows formed (`painted hair by hair`), eye shape larger and more refined, **lip colour and a faint red on the cheeks came back**, a clear gaze and a composed bearing.<br>❌ **Still on the mature side**: fine lines around the eyes / nasolabial folds / fine forehead lines visible — `adult proportions` executed literally | [docs/r33.md](docs/r33.en.md) |
| **R34** | **Age anchor up front + exclude aging in the negative** (`young` moved into the subject, `adult`→`youthful`, added `in her early twenties / dewy clear skin`, negatives extended with `wrinkles/法令纹/眼袋/老气`) | same as R33 · seed 2910/2520/3030 (same-seed A/B) | ✅ **The old look is essentially eliminated**: fine lines gone in the tight portrait, skin dewy, lips fuller, red on the cheeks → reads as early twenties; ✅ **position-is-weight verified for the 5th time** (the same sentence only took effect once moved from the end of the facial sentence to the subject).<br>⚠️ Cost: the anti-aging negatives also suppressed the porcelain-surface defects, so **the porcelain feel receded slightly** — exposing that "porcelain-surface defects ↔ old look" are two ends of the same lever | [docs/r34.md](docs/r34.en.md) |
| **R35** | **Remove the anti-aging negatives** (the 124 characters R34 added: `wrinkles/aged skin/法令纹/老气` and so on), everything else unchanged character for character | same as R34 · seed 2910/2520/3030 (**only the negative differs**) | ✅ **The glaze returned and the age did not bounce back** → proves the anti-aging negatives were suppressing the glaze while the age is controlled by the **positive anchor**; ✅ incidentally completed a **determinism verification** (same prompt/seed/negative → decoded pixels byte-identical, PNGs differing only because of embedded metadata).<br>⚠️ At the same time it **overturns R34's attribution**: the real culprit for the old look is the word `adult`, not the defect list (disproved using R25 as control) | [docs/r35.md](docs/r35.en.md) |

### Cumulative effective improvements (distilled across rounds)

1. **Eyeballs**: `painted eyes` → `glass doll eyes with iris/pupil/catchlight` (effective from R2, the single most effective change)
2. **Material**: add `fired glaze / specular highlight / craquelure`; avoid using `subsurface scattering` directly (R3 image 2 triggered colour-block artifacts)
3. **Composition**: 1:1 → 3:4/4:5 portrait composition, to avoid cutting shoulders and hands
4. **Lighting**: **do not write specific lighting fixtures** ("large softbox" gets painted into the frame); describe the direction and quality of the light instead
5. **Diversity**: a single batch of 5 converges → switch to **one independent request per image + different camera positions**

### ⚠️ Negative distillation: causes of the two degeneration rounds (R11 / R12)

6. **Do not cut material vocabulary for the sake of composition** (R11's mistake): Qwen's clothing/material vocabulary is **the quality itself**.
   To make "cropping up front" take effect, R11 deleted `BASE_Q9` microscopic glaze + `BASE_Q10` jewelry metalwork/fabric macro,
   and the result was that cropping was obtained but the clothing went flat and the face lost texture — **a composition problem should not be traded away with quality vocabulary**.
7. **Do not issue a standalone "sharp highlight" lighting instruction** (R12's mistake; R13 corrected the attribution):
   R12 pulled `one crisp key light ... every highlight is small and sharp` out into a standalone lighting instruction,
   and the result was **a lamp appeared in the frame**. But R13 found that `BASE_Q10` **already contains** `one strong key light`
   (inside `sculptural chiaroscuro lighting with one strong key light and deep natural falloff`)
   and never painted a fixture → the real trigger is **asking for a visible sharp strong light source**, not the term `key light` itself.
   Light should **be woven into the scene description**; concrete fixture nouns such as `softbox / lamp / strobe` remain banned (R4's earlier conclusion).
8. **Do not chase the glaze feel with "like glass / sharp highlights"** (R12's mistake): you get **wet plastic**-like broad, continuous highlights.
   Bone china glaze comes from **soft, contained reflection** (R10's window light already met the bar); to add texture, add **craft marks**
   (milled edges, polishing marks, fabric weave), not stronger reflections.
9. **Do not emphasize the eyes as a standalone "key subject"** (R12's mistake): `open glass doll eyes of realistic size`
   instead **infantilized all three faces**; R10's adult eye shape came from **overall proportion descriptions** like
   `refined adult proportions ... almond eyes of realistic size`.
10. **Reading discipline**: a single composition (R10) and quality degeneration (R11/R12) are **two different classes of problem** and must not be conflated.
    The final must be compared across the four items "facial proportion / glaze / clothing craft / image cleanliness", rather than only looking at the new capability obtained in the current round.

### ✅ Positive methodology distilled (R13–R15)

11. **Material vocabulary is the quality itself, not a bargaining chip to be traded away** (proved by R13): changing only the seed of `BASE_Q10`
    reproduces the R10 level → **the R11/R12 degeneration is the deterministic consequence of deleting words, not random fluctuation**.
    Once the baseline is established, later rounds should **only make increments on top of it**; do not start a separate BASE.
12. **Resolution is not a detail lever** (proved by R14): pixels ×2.25, `bytes/px` (the detail-density proxy) essentially flat,
    4.92 MP actually the lowest and 5× the time. To raise detail you must change the mechanism (more steps / two-stage refinement / a different model),
    not add pixels. Side data: **an RTX 4060 Ti 8GB can run Qwen-Image 2512 at 4.92 MP without OOM**.
13. **Composition is controlled by the canvas aspect ratio, not by wording** (proved by R15):
    - ✅ **1:2 ultra-portrait → full figure**; **1:1 square → seated/medium shot**
    - ❌ `extreme close-up` (R10), `ONLY ... fill the frame` (R11), `seen from behind` (R15) **were all ignored**
    > Mechanism: the aspect ratio changes the geometry of the latent space, and the model **can only** fill the canvas with it → the composition is forcibly rearranged;
    > wording is merely a semantic condition, which the model can "choose to disobey".
14. **When a composition is systematically rejected at the semantic layer, move to the geometric layer to solve it** (R15's general lesson):
    three rounds of true macro failed; it was finally solved in one go by **cropping** (`make_macro.sh`, cropping from the high-resolution final),
    which incidentally sidestepped R11's "macro with no eyes" pitfall — because cropping preserves the original image's complete eyes.
    **Do not keep adding words to the prompt; change the layer.**

### ✅ New distillation for stage 3 (Eastern theme) (R17–R21)

15. **Changing the theme only requires replacing the "cultural sentences"; the material core is inherited verbatim** (proved by R17): split `BASE_Q10` into
    two classes, "material core sentences / cultural sentences", and replace only the cultural sentences → Eastern classical face, hair bun, crossed-collar gold weave, jade and gold filigree
    **landed in one round**, with **zero loss** of the material realism established in stage 2. The converse also holds: **do not rebuild the quality baseline**.
16. **The length of the clothing description is the enemy of composition** (proved by R18, independent of theme):
    R10/R13 (European) and R17 (Eastern) reproduced "a long clothing list pulls the camera in" three times;
    R18 trimmed the list and immediately got the full figure. **But R21 proved you do not have to choose**:
    > Keep "**the form sentence + 3–5 key ornaments**" and you hold both the wide composition and the clothing layering.
    > The trigger is **the length of the exhaustive list**, not "mentioning clothing" itself.
17. **Description reliability is layered** (distilled from R19/R20):
    | Tier | Examples | Result |
    |---|---|---|
    | High | `璎珞 / 步摇 / 云肩 / 金镶玉带 / 瓷鞋` | ✅ Essentially lands first try |
    | Medium | `团扇 / 屏风 / 木几` | ⚠️ Sometimes works, sometimes not (worked in R17/R18, failed in R20) |
    | Low | `花钿` (facial makeup decoration) | ❌ Failed all 3 times |
    | None | viewpoint/cropping wording (`behind` / `macro` / `ONLY`) | ❌ Ignored without exception |
    > **If you want something, give it "an object that can take shape on its own"; do not give it "makeup detail" or "framing constraints".**
18. **Forms can be swapped like parts** (proved by R19): moving only **one** form sentence (crossed-collar wide sleeves ↔ Tang-style high-waist ruqun)
    yields a whole different silhouette, while face/jewellery/material/light are all inherited stably → the **layered structure** of `BASE_E` is
    extensible; expanding to Han/Song/Ming forms later requires no change to the other sentences.

### ✅ New distillation for stage 4 (half-real half-bone-china) (R22–R26)

19. **The subject decides whether it "is a figurine"** (R22's lesson): the first 21 rounds looked more and more like a figurine because the prompt kept saying
    `doll / ball-jointed / museum-vitrine realism / display stand / porcelain slippers`.
    **Removing these words + banning dolls/joints/display stands in the negative** brought her back to life as a living person.
    ⚠️ But **do not delete the "bone china material" along with them** — **the subject is a living person and the material is still bone china**, and the two do not conflict (corrected in R23/R24).
20. **Chinese-English division of labour** (proved by R23):
    - **Chinese** writes "**what there is**" — character, expression, jewellery, clothing, environment, props (the Chinese passage landed the Boshan censer smoke,
      the screen's pictorial feel, yingluo, jade rings and the gold-woven collar in one try, with higher precision than English)
    - **English** writes "**what it is made of**" — glaze, translucency, microscopic texture (the material vocabulary validated over 21 rounds)
21. **Position is weight** (proved by R24, the 3rd independent verification): the same material text, moved from last place to **first**,
    changed the result from "no glaze" to "obvious glaze". **Write the most important requirement first.**
22. **"Fine" ≠ "smooth"** (proved by R25, this project's most valuable item about detail):
    writing `microscopic texture` in general terms only yields a **clean, smooth** surface. To give detail you must **give a defect list**:
    `pinholes where the glaze pulled back` / `trapped bubbles and blisters` /
    `polishing marks and hairline drag lines` / `orange-peel ripple` /
    `glaze slightly uneven in thickness and colour` / `kiln grit` + `never a uniform flat surface`.
23. **For translucency, do not name the ears** (R24's pitfall): `warm translucency ... of the ears` is executed literally,
    growing **elf pointed ears**. Point at `temples / fingertips` instead, and put `pointed ears / elf ears / 尖耳 / 精灵耳` into the negative.
24. **A square canvas is the cheapest way to "get microscopic"** (R25): 2048² doubles the pixels the face occupies, and only after cropping are the glaze's pinholes visible.
    This does not contradict R14 — raising resolution does not raise **whole-image** density, but it does raise the usable pixels of the **cropping target**.
25. **"Lightness" must be written as physical items, not style words** (R26): number of layers + thickness (thin as cicada wings) + translucency (the light and shadow of the layer beneath showing through)
    + edges (crisp and clean) + motion (drifting as if about to rise, trailing like smoke); writing these out item by item yields fine gauze;
    writing only "flowing" yields ordinary cloth. **The key to "half-gauze half-bone-china" is giving the fabric a "property of porcelain"**
    (`crisp fine weave / cleanly cut edge / the stiffness of porcelain rather than the softness of cloth`).
26. **Makeup needs a reverse constraint** (R22's pitfall): without writing "light makeup/bare makeup", the default is heavy lipstick and modern eyebrows, producing a "photo-studio feel".
    Write positively `妆极淡，近乎素面`, and ban `heavy makeup / red lipstick / 浓妆 / 影楼 / 网红妆` in the negative.

### ✅ New distillation for stage 5 (natural makeup + languid life) (R27–R29)

27. **The "deliberateness" of blush is a question of position, not of wording** (proved by R27): the obvious circular blush in R26 came from
    the sentence `a soft blush of warm colour across the cheeks` in the **up-front** material passage (the highest weight).
    Rewriting it in place as "blood colour showing through from within, uneven in depth, absolutely not applied rouge" + banning blush-type words in the negative → fixed in one round.
    **To weaken a feature, first find its position in the prompt.**
28. **The canvas lever is directional** (R27's qualification, confirmed by R28):
    - ✅ an ultra-**portrait** ratio (1:2, 1:2.33) can force **a taller subject** (standing full figure)
    - ❌ an ultra-**landscape** ratio (2:1) **cannot** force **a wider subject** — the model fills both sides with background and still returns a bust in a wide frame
    > A reclining full body **can only be obtained through wording**; the canvas is only responsible for not cropping it away (2.67:1 merely leaves room).
29. **A pose is obtained not by "adding words" but by "reducing competing description"** (proved by R28, the 4th verification of "position is weight"):
    with the same batch of pose sentences, R27 placed them after an 1802-character base prompt → **0/3 success**;
    R28 put them **at the very front** and cut the base prompt to **635 characters** → **3/3 success**.
30. **Naming a body part for translucency = turning that part into a light source** (2nd verification, after R24):
    R24 `the ears` → elf pointed ears + orange translucency; R27 `the fingertips` → fingers and palm glowing orange.
    > **Rule**: when writing "translucent", **do not specify which part it is**; and put `glowing hands / 发光的手 / 尖耳`
      and the like into the negative.
31. **A short base prompt can fully carry named ornaments** (proved by R29): R19's "wide composition ↔ clothing detail cannot be had together",
    R21 found the medium-density solution and R29 further confirmed it — adding **three named ornaments** to the **pose-up-front** short base prompt
    (crossed collar / yingluo / jade belt) **does not affect the full-body composition at all**.
    > **The real enemy is always "the length of the exhaustive list", not "mentioning clothing".**
32. **Desk-type poses naturally lose the lower body** (R29): this is not a failure but the inevitable framing of that pose.
    If you want "head to toe", do not choose poses like leaning over a desk, lying prone, or hugging the knees, which hide the lower limbs.

### ✅ New distillation for stage 6 (material recovery) (R30–R31)

33. **A downgrade is caused by "deleting vocabulary", not by "a drop in skill"** (R30's diagnosis): the reason phase-5 regressed from "living porcelain"
    to "a real person in hanfu having her photo taken" is that when R28 cut the base prompt it also cut phase-4's **named defect list**.
    **This is the same mechanism as R11** — deleting material vocabulary so that composition dominates.
    > **Discipline**: for any change that "cuts the prompt for the sake of another goal", list item by item what was cut,
    > and confirm that none of it is a **validated lever**. The short base prompt was proven effective at the time and thereby masked what else it deleted.
34. **The enemy of composition is the "exhaustive clothing list", not "total length"** (proved by R30, tying together R10/R13/R17/R18/R21/R27/R29):
    the material sentences went from 776 → 1178 characters (1254 for the whole prompt, **close to the 1283 at which R27 got 0/3 full bodies**),
    and all three **still held the full body**. Together with the conclusions of R21/R29 this settles it:
    - ❌ what pulls the camera in is a **long clothing list**
    - ✅ adding **material density** does not affect composition (as long as the pose is up front)
35. **Judging "fineness" requires enough pixels on the target** (R30's lesson): in the 1600² **full-body** square canvas,
    the face occupies only about 180px; when magnified, the detail is smoothed away by interpolation, and **the glaze cannot be judged**.
    R25 was able to conclude anything about "pinholes" back then because it used a 2048² **tight portrait**.
    > **A big canvas ≠ a qualified audit sheet**: the framing of the audit sheet must let the target occupy enough pixels.
36. **A named defect list is not executed automatically** (R30, the 2nd time after R9): `pinholes / orange-peel / polishing marks / kiln grit` were written,
    yet none of them is visible in the image, which is instead more uniform —
    exactly the `never a uniform flat surface` that the prompt explicitly forbids.
    > For the list to take effect it seems to also need **conditions that make it visible** (see R31's `crisp specular highlights`).
37. **The material sentence really does change the skin, provable by a same-seed ablation** (proved by R31): same seed, same canvas, same negative,
    differing only in the material sentence → the skin goes from "warm-toned matte real-human skin" to "cool-toned, uniform, with glaze sheen". **This is not seed noise.**
38. **The framing of the audit sheet and the canvas size are two different things** (R30's lesson, corrected by R31): in the 1600² **full-body** square canvas,
    the face occupies only about 180px, and **the glaze cannot be judged**; R25 could conclude anything about "pinholes" because it used a 2048² **tight portrait**.
    > To judge the microscopic, **first let the target occupy enough pixels** — a big canvas ≠ a qualified audit sheet.
39. **The material assertion is a dosage lever with adjustable levels** (proved by R32): a three-step ladder at the same seed progresses **monotonically** —
    R29 matte real-human skin → R31 satin sheen → R32 clear glaze.
    Key wording: `half real skin and half porcelain` literally leaves half of it as a real person;
    only replacing it with `made of bone china -- the material itself, not a mask` + `Her face is human; her skin is porcelain.`
    kept moving it toward the porcelain end.
40. **The same subordinate clause means the opposite in different contexts** (R27 vs R25 comparison): `a soft blush of warm colour across the cheeks`
    reads as "applied blush" (deliberate) in R27's **living-person context**, yet reads as "painting on porcelain" (correct) in R25's **porcelain context**.
    > **Do not blacklist something forever just because it was a pitfall in one round** — first look at what the subject of that round was.
41. **"No temperament" is often a lack of description, not something the model cannot do** (proved by R33): when the base prompt had not a single facial-feature word,
    the model could only improvise a face from the generic word `princess`, producing a **mature, bland, generic face**.
    After restoring phase-2's facial feature sentence, **eyelashes, eyebrows, eye shape and lip shape each took effect** —
    the same root as R19's "named objects are reliable": **whatever you want, write it out by name**.
42. **A word introduced to cure one fault becomes a new fault in another context** (found in R33): `adult proportions`
    was introduced in R4/R5 to cure an "infantile face shape" and stayed in the facial sentence ever since; in a tight portrait it was executed literally as
    **wrinkles and nasolabial folds**, becoming the source of the "old look".
    > **Discipline**: whenever the goal turns (from "want adult" to "want young"), go back and review **the words written for the old goal**.
43. **Attribute words like age/temperament must be placed where they have weight** (R33's lesson → corrected by R34):
    R33 wrote `a young woman ... never matronly` at the **end** of the facial sentence (the middle of the whole prompt),
    where it had almost no weight. By "position is weight" (verified four times), the age anchor should sit at the very front together with the subject.
44. **What the positive asks for, the negative must not simultaneously ban** (R33's direct lesson): to cure "deliberate blush", R27 swept
    `blush / rouge / 腮红` wholesale into the negative; by R33, when a "very faint blood colour" was wanted, the positive wrote `the faintest soft blush`
    while the negative was still banning it — a contradiction.
    > **Rule**: the negative should only ban **the form you want to drive out** (`heavy / circular / doll-like blush`),
      not the **whole concept**.

45. **An attribute word at the end is as good as not written** (proved by R34, the 5th "position is weight"): the same age meaning,
    placed at the **end** of the facial sentence (R33, the middle of the whole prompt) was almost ineffective; moved into the **subject sentence** (R34, character 41) it took effect immediately.
46. **To exclude a class of features, write it in the negative, not the positive** (R34): after placing `wrinkles / 法令纹 / 眼袋 / 老气`
    in the negative, the fine lines in the tight portrait decreased significantly; writing "no wrinkles" in the positive is unreliable.
47. ⚠️ **~~"Porcelain-surface defects" and the "old look" are two ends of the same lever~~ → overturned** (corrected by the R25 audit before R35):
    R34 once inferred that the old look came from the defect list. Auditing the phase-4 highland R25 proved **that inference wrong** —
    R25's defect list is **character-for-character identical to R30–R34** and has **no age words at all**, yet the final is
    **early twenties + hard glaze sheen + pinholes on the cheeks + a faint blush on the cheeks**. Therefore:
    - **The real culprit for the old look is `adult`** (a word R33 recovered from phase-2, originally introduced in R4/R5 to cure "too infantile" and never re-reviewed)
    - **The porcelain feel receding in R34 is more likely the anti-aging negatives (`aged skin / mature face / wrinkles`) suppressing the glaze**,
      rather than the defect list
    > **Lesson**: attribution must use a **validated successful sample** as control. R25 had been sitting in the repository all along; checking it first would have saved a whole round of wrong attribution.
48. **Attribution must use a "validated successful sample" as control** (R35's lesson): R34 attributed the "porcelain feel receding" to the defect list;
    before R35, the audit looked at R25, which had been lying in the repository all along — **the same five defects, zero age words, yet the final is young + hard glaze surface**,
    and that single comparison overturned the attribution, saving a whole round of trial and error.
    > **Discipline**: when complaining that "a round got worse", **first find the round that got it right historically and diff it word by word**, then guess at causes.
49. **The positive defines the goal; the negative should not define it a second time** (proved by R35): R34 used anti-aging negatives to suppress the fine lines,
    but suppressed the **glaze's surface variation** along with them; after R35 removed those negative words the glaze returned and **the age did not bounce back** —
    because the age is controlled by the positive anchor (`young` / `youthful` / `early twenties`).
    > The negative should only exclude **the specific forms to be driven out**, not carry the job of "defining an attribute".
50. **Qwen is deterministic on this server** (empirically established by R35): same prompt / negative / seed / canvas / steps / cfg
    → decoded pixels **byte-identical** (rgb24 sha identical); PNG file shas differ **only because of the embedded execution graph and metadata**.
    > This empirically confirms the discipline recorded earlier in this project: **compare pixels for reproducibility, not file shas**.

51. **"More porcelain" does not equal "more correct"** (R32's reflection): the user brief was "**half real, half bone china**",
    yet R25 (this project's acknowledged material highland) is actually **more porcelain than the brief** (close to fully porcelain).
    R32 lands in the middle, leaning porcelain, and is therefore a better fit for the brief. **The goal is not an extremum in one direction but an interval.**

---

## 5. Output record

| Round | Artifact directory | Count | round.json |
|------|----------|------|-----------|
| R1 | `out/r1/` | 5 | - (single batch) |
| R2 | `out/r2/` | 5 | - (single batch) |
| R3 | `out/r3/` | 5 | ✅ includes prompt_id |
| R4 | `out/r4/` | 5 | ✅ includes prompt_id |
| R5 | `out/r5/` | 5 | ✅ includes prompt_id |
| R6 | `out/r6/` | 5 | ✅ includes prompt_id |
| R7 | `out/r7/` | **3** | ✅ includes prompt_id (engine=qwen) |
| R8 | `out/r8/` | **3** | ✅ includes prompt_id (engine=qwen) |
| R9 | `out/r9/` | **3** | ✅ includes prompt_id (engine=qwen) |
| R10 | `out/r10/` | **3** | ✅ includes prompt_id (engine=qwen) |
| R11 | `out/r11/` | **3** | ✅ includes prompt_id (engine=qwen) |
| R12 | `out/r12/` | **3** | ✅ includes prompt_id (engine=qwen) |
| R13 | `out/r13/` | **3** | ✅ includes prompt_id (engine=qwen) |
| R14 | `out/r14/` | **3** | ✅ includes prompt_id (engine=qwen) · 2.19–4.92 MP resolution ablation |
| R15 | `out/r15/` | **3** | ✅ includes prompt_id (engine=qwen) · three aspect ratios |
| R16 | `out/r16/` | **3** | ✅ includes prompt_id (engine=qwen) · steps 40 |
| **Delivery set** | **`out/final-set/`** | 5 | portrait / full-figure / seated (R16) + tiara macro / wrist-joint macro (cropped) |
| R17 | `out/r17/` | **3** | ✅ includes prompt_id · Eastern classical baseline (`BASE_E`) |
| R18 | `out/r18/` | **3** | ✅ includes prompt_id · full-figure fix (880×2048) |
| R19 | `out/r19/` | **3** | ✅ includes prompt_id · Tang-style form variant |
| R20 | `out/r20/` | **3** | ✅ includes prompt_id · high-resolution base image (3.43 / 2.56 / 3.07 MP) |
| R21 | `out/r21/` | **3** | ✅ includes prompt_id · Eastern final round |
| **Eastern delivery set** | **`out/final-set-east/`** | 10 | hero / portrait / full-figure / seated / tang-portrait + **5 craft macros** |
| — | `out/macro-east/` | 5 | **True macro by cropping** (not generation): cropped from the R20 base image by `make_macro_east.sh` |
| R22–R26 | `out/r22/` … `out/r26/` | **3 each** | ✅ all include prompt_id · stage 4 (de-figurinization / mixed Chinese-English / material up front / named defects / fine gauze) |
| **Stage-4 delivery set** | **`out/final-set-gauze/`** | 6 | hero / portrait / full-figure / airy-turn + **skin-macro / gauze-macro** |
| — | `out/macro-gauze/` | 2 | Skin macro (cropped from R25 2048²) and gauze macro (cropped from R26): `make_macro_gauze.sh` |
| R27–R29 | `out/r27/` … `out/r29/` | **3 each** | ✅ all include prompt_id · stage 5 (natural makeup / languid full body / everyday moments) |
| R30 | `out/r30/` | **3** | ✅ includes prompt_id · stage 6 (material recovery: moving the phase-4 named defect list back into the short pose base prompt; includes same-region A/B crops `out/macro-material/`) |
| R31 | `out/r31/` | **3** | ✅ includes prompt_id · stage 6 (restore the glaze sentence + tight-portrait audit sheet; includes strict same-seed ablation crops and a comparison with the R25 audit sheet) |
| R32 | `out/r32/` | **3** | ✅ includes prompt_id · stage 6 (change the material assertion; all three are strict same-seed A/B against R31, including the three-step ladder and a three-way audit-sheet comparison) |
| R33 | `out/r33/` | **3** | ✅ includes prompt_id · stage 7 (restore face/bearing; includes same-seed A/B crops against R32 `face-r32-vs-r33.png` / `face-square-r32-vs-r33.png`) |
| R34 | `out/r34/` | **3** | ✅ includes prompt_id · stage 7 (age anchor up front + anti-aging negatives; includes same-seed A/B against R33 `face-r33-vs-r34.png` / `face-square-r33-vs-r34.png`) |
| R35 | `out/r35/` | **3** | ✅ includes prompt_id · stage 8 (remove the anti-aging negatives; includes the three-way audit sheet `verdict3-r25-r34-r35.png` and determinism verification) |
| **Stage-5 delivery set** | **`out/final-set-life/`** | 8 | hero / seated / recline / prone / mat-by-window / doze + skin-macro / gauze-macro |
| — | `out/macro/` | 2 | **True macro by cropping** (not generation): cropped from the R14 3.43 MP final by `make_macro.sh` |

---

## 6. Finals

### Stage-2 final (Qwen-Image) — corrected after user review

> ⚠️ **R11 was once chosen by mistake**. The user pointed out that R11 is a sudden degeneration; after re-checking R8–R10 it was confirmed and the final was changed back to **R10 `window-light`**.
> Basis (four-way comparison): adult facial proportions, glaze translucency, clothing craft, image cleanliness — R10 is comprehensively better than R11/R12.

| Item | Value |
|----|----|
| **Final** | `out/final-bone-china-princess-v2.png` (from **[out/r10/bc-r10-window-light_00001_.png](out/r10/)**) |
| Reason for choice | The most balanced image in the whole project: **adult princess** facial proportions and refined features, porcelain **translucency** (neck/collarbone/ear), **contained window-light reflection** (not wet plastic), fully readable **gold-thread brocade + gold-set sapphire + pearl + lace** craft, clean frame with no clutter |
| Engine / seed / size / steps / cfg | Qwen-Image 2512 / **1020** / 1280×1712 / 32 / 3.5 |
| prompt | `BASE_Q10` + `, three-quarter portrait in soft north window light with a pale rose brocade gown, gentle shadow gradient across the porcelain cheek, quiet interior backdrop` (original in [docs/prompts-all.md](docs/prompts-all.en.md)) |
| Negative | `NEG_Q` |
| Detail study image | `out/detail-study-joint-hand.png` = **R12 `hand-single`** (single hand with five fingers + knuckle/wrist ball-joint seams + clean nails + lace weave); for the tiara detail see `out/r11/bc-r11-tiara-macro_00001_.png` (silver filigree is excellent, but that image's face has no eyes, so it can only serve as a tiara study) |
| Alternatives | `out/r10/bc-r10-embroidery-macro_00001_.png`, `out/r9/bc-r9-fan-portrait_00001_.png`, `out/r8/bc-r8-rembrandt-portrait_00001_.png` |
| ~~Once chosen~~ | ~~`out/r11/bc-r11-portrait-velvet_00001_.png` (seed 1120)~~ —— void, see [docs/r11.md correction](docs/r11.en.md) |

### Final delivery set (R16, multiple compositions)

A single "final" is no longer enough to represent the project's results — R15/R16 solved the single-composition problem, so the deliverable is a set:

| File (`out/final-set/`) | Source | Size | Notes |
|---|---|---|---|
| `portrait.png` | R16 `final-portrait` (seed 1600, steps 40) | 1280×1712 | Portrait main image, a direct descendant of the R10 window-light formula |
| `full-figure.png` | R16 `final-full-figure` (seed 1610, steps 40) | 1024×2048 | **Best full figure**: tiara→porcelain slippers, gold velvet cushion, ball-joint seams at both wrists |
| `seated.png` | R16 `final-seated` (seed 1620, steps 40) | 1600×1600 | Seated, hands folded on the knees, lace fan placed on the side table as instructed |
| `macro-tiara.png` | `make_macro.sh` crop | 1120×1280 | True tiara macro (silver filigree/prong settings/sapphire), **with complete eyes** |
| `macro-wrist.png` | `make_macro.sh` crop | 960×1260 | True wrist ball-joint macro, **internal metal tension ring visible** |

**Final formula** (reproducible): `BASE_Q10` + `NEG_Q` · 32–40 steps · cfg 3.5 · composition via the canvas aspect ratio ·
macro via cropping. See [docs/r16.md](docs/r16.en.md) for details.

### Stage-3 final / Eastern theme delivery set (R17–R21)

**The theme has changed to "Bone China Princess · Eastern classical beauty"**, with the material core inherited verbatim from `BASE_Q10`.

| File (`out/final-set-east/`) | Source | Size | Notes |
|---|---|---|---|
| **`hero.png`** | **R20 `plate-portrait`** (seed 2000) | 1600×2144 | **Eastern theme final** (`out/final-bone-china-princess-east.png`): gold-set jade crown ornament + buyao, jade earrings, yingluo, cloud collar, gold-thread embroidered collar, gold-set jade waist seal, and it is the macro base image (richest in detail) |
| `portrait.png` | R21 `final-portrait` (seed 2100) | 1280×1712 | The most complete portrait of the Eastern stage |
| `full-figure.png` | R21 `figure-medium` (seed 2110) | 880×2048 | **Medium-density base**: complete full figure (hair bun→celadon-glazed porcelain slippers→carved wooden stand) **while keeping** the gold-thread embroidered chest band and gold-set jade waist seal |
| `seated.png` | R21 `final-seated` (seed 2120) | 1600×1600 | Long hair hanging down variant, gold filigree jade-inlaid crown ornament |
| `tang-portrait.png` | R19 `portrait` (seed 1900) | 1280×1712 | **Tang-style form** variant (high waist with a fitted bodice, gauze) |
| `macro-hairpin.png` | `make_macro_east.sh` | 1020×1140 | Gold-set jade buyao: openwork gold filigree, prong-set baroque pearl, bead→jade→teardrop-pearl pendants |
| `macro-necklace.png` | same as above | 1400×860 | Yingluo + crossed-collar coiled gold embroidery + cloud collar + double fine-bead piping |
| `macro-chest.png` | same as above | 1120×880 | Coiled gold embroidery thread curls + **translucent waxy sheen of the jade bi disc** |
| `macro-slipper.png` | same as above | 980×1050 | Celadon-glazed porcelain slipper + gold filigree + gold-flower-set pearl + rosewood stand |
| `macro-wrist.png` | same as above | 840×1320 | Wrist ball joint + **internal metal tension pin** + gauze weave |

**Eastern formula** (reproducible): `BASE_E18` (portrait/seated) · `BASE_E21_MED` (full figure) · `BASE_E19` (Tang style) +
`NEG_Q` · 32 steps · cfg 3.5 · composition via the canvas aspect ratio · macro via `make_macro_east.sh` cropping.
See [docs/r21.md](docs/r21.en.md) for details.

### Stage-4 final / half-real half-bone-china delivery set (R22–R26, **current direction**)

**Direction**: she has shed every trace of the "museum doll" and become **a living princess**;
**skin half-real half-bone-china** (fired glaze sheen + real human blood colour + named glaze defects); **garments half-gauze half-bone-china** (several layers of fine gauze, translucent, edges crisp like porcelain).

| File (`out/final-set-gauze/`) | Source | Size | Notes |
|---|---|---|---|
| **`hero.png`** | **R26 `full-figure`** (seed 2610) | 880×2048 | **Current final** (`out/final-bone-china-princess-gauze.png`): standing full figure, several layers of fine gauze almost weightless, the skirt trailing like smoke, wide sleeves lifting; an interior (rosewood screen/lattice window/censer smoke); porcelain-glaze skin with a warm flush |
| `portrait.png` | R26 `portrait` (seed 2600) | 1280×1712 | Half-body, the gauze layering and translucency clear, a porcelain hand in the foreground |
| `airy-turn.png` | R26 `airy-turn` (seed 2620) | 1600×1600 | Turning to look back, gauze lifting in the light, almost luminous |
| `skin-macro.png` | `make_macro_gauze.sh` | 936×1140 | **Skin macro** (cropped from the R25 **2048²** base image): fired glaze sheen + real human warm flush + **glaze pinholes/orange-peel ripple** + iris fibres and individual eyelashes |
| `gauze-macro.png` | same as above | 860×1360 | **Gauze macro**: individual warp and weft discernible, several translucent layers forming a gradient, gauze edges clean and crisp |

**Stage-4 formula** (reproducible, order is weight):
`BASE_H4_EN` (English material layer, **must go first**) → `BASE_H5_FABRIC_EN` (gauze layer) → Chinese Dream of the Red Chamber baimiao passage →
camera sentence; negative `NEG_H5` (ban figurines / ban heavy makeup / ban matte real-human skin / ban pointed ears / ban heavy cloth).
See [docs/r26.md](docs/r26.en.md) for details.

**A reproducible way to write "half-real half-bone-china" skin**:
glaze material passage (`fired glaze` / `crisp specular highlights` / `warm translucency`) **up front**
+ real human blood colour (`a soft blush of warm colour across the cheeks`) + real human hair (stray strands)
+ **a named defect list** (`microscopic pinholes where the glaze pulled back` / `trapped bubbles and blisters` /
`polishing marks and hairline drag lines` / `a fine orange-peel ripple` / `glaze slightly uneven in
thickness and colour` / `kiln grit`) + `never a uniform flat surface` − uniform smoothness.

**A reproducible way to write "half-gauze half-bone-china" garments**:
number of layers (`several layers`) + thickness (`as thin as cicada wings`) + translucency (`so sheer that the layers beneath
and the light behind show through`) + edge and sinew (`the crisp fine weave and the cleanly cut edge of
porcelain rather than the softness of ordinary cloth`) + motion (`drifting and floating` / `sleeves and
hems lifting`) − dense gold weave (`heavy gold embroidery` into the negative).

### Stage-5 final / languid life delivery set (R27–R29, **current direction**)

**Direction**: natural makeup (**not applied rouge**) + **full-body** daily-life moments (sitting / prone / lying), with a languid everyday feel.

| File (`out/final-set-life/`) | Source | Size | Notes |
|---|---|---|---|
| **`hero.png`** | **R29 `propped-bolster`** (seed 2900) | 2048×768 | **Current final** (`out/final-bone-china-princess-life.png`): half-reclining on a long couch, back against a large bolster, holding a **celadon tea cup**; gold-set jade belt and bead-and-jade necklace complete, barefoot |
| `seated.png` | R28 `seated-daybed` (seed 2820) | 1200×1600 | Sitting slantwise on a low couch, chin on hand, gazing out the window, half a cup of tea on the table |
| `recline.png` | R28 `recline-side` (seed 2800) | 2048×768 | Lying on one's side propping the cheek, a book scroll spread on the couch |
| `prone.png` | R28 `prone` (seed 2810) | 2048×768 | Lying prone propped on the elbows, lower legs raised and crossed, a round fan set aside |
| `mat-by-window.png` | R29 `mat-by-window` (seed 2910) | 1200×1600 | Sitting on a mat by the window, hugging the knees |
| `doze.png` | R29 `doze-on-arms` (seed 2920) | 2048×768 | Dozing over a desk, long hair spilling across the desk surface |
| `skin-macro.png` / `gauze-macro.png` | `make_macro_gauze.sh` | — | Half-real half-bone-china skin / half-gauze half-bone-china gauze |

**Stage-5 formula** (reproducible, **order is weight**):
`pose sentence (first)` → `BASE_H7_POSE` / `BASE_H8_POSE` (**short base prompt ~640–780 characters**: subject + half-real half-bone-china skin +
half-gauze half-bone-china gauze + named ornaments + loosely coiled hairstyle + bare face) → camera sentence;
negative `NEG_H7` (on top of R26: ban glowing hands and feet, ban bust cropping, ban deliberate makeup, ban sitting upright for a posed shot).
See [docs/r29.md](docs/r29.en.md) for details.

### Stage-1 final (Z-Image-Turbo, retained)

| Item | Value |
|----|----|
| Final | `out/final-bone-china-princess.png` (from `out/r6/bc-r6-bouquet_00001_.png`) |
| Engine / seed / size / steps | Z-Image-Turbo / 610 / 1024×1360 / 16 |
| prompt | See [docs/r6.md §Final selection](docs/r6.en.md) |

> ⚠️ Video integration pending: this project's final has a ratio of 1024×1360 (≈3:4); if it later goes into video-gen's I2V, it must be regenerated at the target video ratio (see [image-to-video-fastvideo3](../../../video-gen/skills/image-to-video-fastvideo3/SKILL.md)).

---

## 7. Checklist

- [x] Every round fully written to disk (R1–R6 5 each = 30; R7–R16 3 each = 30; **60 in total**, plus 5 in the delivery set + 2 macros)
- [x] Each round's `docs/rN.md` has prompt, parameters, self-check and next-round changes filled in (**r1–r16 complete**)
- [x] Eyeball texture (iris/pupil/catchlight) meets the bar — visible in both the R10 window-light formula and the `make_macro.sh` tiara macro
- [x] Bone china material (translucency/glaze) meets the bar — adult face + translucent neck/collarbone/ear + contained window-light reflection (not wet plastic)
- [x] Hands, shoulders and neck not cut badly, no extra limbs, no floating fragments — the hands in R12/R16 all have five fingers, segmented knuckles and complete wrist ball-joint seams
- [x] A final was selected in the last round and model + prompt + seed + size recorded — main final R10 `window-light` (seed 1020) + delivery set `out/final-set/`
- [x] Macro detail usable (tiara silver filigree / wrist ball joint / lace weave / metal tension ring)
- [x] Negative prompts take effect (Qwen engine)
- [x] **Camera diversity** — R15/R16 obtained full figure/seated via the canvas aspect ratio (R10/R13 once had three near-identical frames)
- [x] **Verbatim prompt archive** matches the server execution graph (all of R3–R16; R16's three images checked character for character)
- [x] Degeneration rounds have their causes located and distilled into a negative checklist (R11 / R12)
- [x] **Eastern theme change** (R17) — Eastern classical face/high bun/crossed-collar gold weave/cloud collar/gold-set jade belt/yingluo all in place, with zero loss of material realism
- [x] **5 Eastern craft macros** (R20 cropping method): gold-set jade buyao / yingluo + coiled gold embroidery / jade bi disc / celadon-glazed porcelain slipper / wrist ball joint
- [x] **Form diversity**: two Eastern silhouettes, crossed-collar wide-sleeve gold weave (R17/R18) and Tang-style high-waist ruqun + gauze (R19)
- [x] Eastern delivery set `out/final-set-east/` (10 images) + final `out/final-bone-china-princess-east.png`
- [x] **Stage-3 verbatim prompt archive** matches the server execution graph (R3–R21; R16/R21 checked character for character)
- [x] **Stage-4 de-figurinization**: the subject changed to a living person; doll/ball joints/display stand/vitrine all moved out of the positive and into the negative
- [x] **Skin half-real half-bone-china**: fired glaze sheen + real human warm flush + **named glaze defects** (pinholes/trapped glaze bubbles/polishing marks/orange-peel ripple/uneven glaze colour)
- [x] **Garments half-gauze half-bone-china**: several layers of gauze thin as cicada wings, translucent enough to show the layer beneath, edges crisp with the sinew of porcelain
- [x] Stage-4 delivery set `out/final-set-gauze/` (6 images) + final `out/final-bone-china-princess-gauze.png`
- [x] Skin macro and gauze macro (`make_macro_gauze.sh` cropping)
- [x] **Stage-4 verbatim prompt archive** matches the server execution graph (R26's three images checked character for character)
- [x] **Stage-5 natural makeup**: the deliberate circular blush removed, replaced with uneven natural blood colour (negative bans blush/rouge marks/high-altitude flush)
- [x] **Stage-5 full body and languid poses**: sitting slantwise on a low couch / lying on one's side propping the cheek / lying prone with feet raised / half-reclining with tea / hugging knees by the window / dozing over a desk, 6 everyday moments in total
- [x] Stage-5 delivery set `out/final-set-life/` (8 images) + final `out/final-bone-china-princess-life.png`
- [x] **Stage-5 verbatim prompt archive** matches the server execution graph (R29's three images checked character for character)

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-02 | v1.0 | Established the project: acceptance criteria, round-1 prompt and self-check, iteration plan | 小七 |
| 2026-10-02 | v1.1 | Each round became its own document (docs/r1–r3); the README became an index + cross-round distillation | 小七 |
| 2026-10-02 | v2.0 | Completed R4–R6, 6 rounds and 30 images in total; each round's record written up; the final selected was R6-bouquet (seed 610) | 小七 |
| 2026-10-02 | v3.0 | The user judged detail/realism insufficient: switched to 3 images per round and continued for 5 more rounds; R7 switched the engine to Qwen-Image 2512 (added `comfyui_qwen.py`), R8 raised it to 1152×1536 + sculptural light + gold-thread brocade | 小七 |
| 2026-10-02 | v4.0 | Completed R9–R11; R11 obtained true macro with "composition up front"; the stage-2 final selected was R11-portrait-velvet (1280×1712, seed 1120) | 小七 |
| 2026-10-02 | v4.1 | Completed the prompt archive: added `docs/prompts-all.md` (37 verbatim prompts) + the `run_round.py --prompts` generator; round.json backfilled with prompt originals; verified the server execution graphs match the archive | 小七 |
| 2026-10-02 | v4.2 | Added "default retention" to the skill (`<prefix>.api.json` + `requests.jsonl`, consistent across both engines, can be turned off with `--no-record`); the 35 execution graphs of R3–R11 were backfilled from the server history into `out/rN/` | 小七 |
| 2026-10-02 | v5.0 | Completed R12 (de-CGI attempt, half degeneration); **user review pointed out that R11 is a sudden degeneration**, and after re-checking R8–R10 the quality highland was confirmed as R8–R10: the final was corrected from R11 `portrait-velvet` to **R10 `window-light`**, and the detail study image was corrected from R11's ten-finger hand to R12's single hand; post-hoc corrections added to the R11/R12 documents; 5 negative lessons added (do not cut material vocabulary / do not write fixture nouns / do not use glass metaphors for glaze / do not emphasize the eyes separately / reading discipline) | 小七 |
| 2026-10-02 | v6.0 | Completed the five-round wrap-up R13–R16: **R13** the control experiment proved the R10 level reproduces across seeds (quality comes from the material vocabulary); **R14** the resolution ablation gave a negative result (pixels ×2.25 with flat detail density; resolution is not a detail lever); **R15** controlled composition with the canvas aspect ratio and successfully obtained full figure/seated, established the methodology "if the semantic layer cannot get it, switch to the geometric layer", and solved macro by switching to the **cropping method**; **R16** the final round produced a three-composition delivery set (`out/final-set/`). Added `make_macro.sh`; `run_round.py` supports per-image overrides of size/steps/cfg/timeout; 4 positive methodology items distilled | 小七 |
| 2026-10-02 | v7.0 | **Theme changed to "Bone China Princess / Eastern classical beauty"** and five rounds R17–R21 completed: added `BASE_E` (material core inherited verbatim from `BASE_Q10`, only the cultural sentences changed); R17 landed the theme in one round; R18 trimmed the clothing list + pushed the canvas higher to fix the full figure and added `璎珞`; R19 the Tang-style form variant; R20 the cropping method produced **5 Eastern craft macros** (`make_macro_east.sh`); R21 proved that a **medium-density base** of "form + key ornaments" can hold both the wide composition and the clothing layering. Produced the Eastern delivery set `out/final-set-east/` and the final `out/final-bone-china-princess-east.png`. 4 methodology items added (cultural sentences are replaceable / clothing description length is the enemy of composition but has a middle solution / description reliability is layered / forms are pluggable) | 小七 |
| 2026-10-02 | v8.0 | **Fourth turn: de-figurinization + half-real half-bone-china**, completing five rounds R22–R26. User feedback "she looks too much like a figurine" and "the skin has a bone china texture but is not detailed enough", followed by a request that "the clothes must be light enough, half gauze half bone china". What was done: the subject changed to a living person and dolls/joints/display stands were moved into the negative; the prompt changed to a mixed Chinese-English write-up of **Chinese Dream of the Red Chamber entrance baimiao + an English material layer**; **the material passage moved up front** to obtain glaze; **named porcelain-surface defects** to obtain microscopic detail; a 2048² square canvas to make the skin crop truly "microscopic"; only the clothing layer changed (heavy gold weave → several layers of fine gauze) to obtain "half-gauze half-bone-china". Produced the stage-4 delivery set `out/final-set-gauze/`, the final `out/final-bone-china-princess-gauze.png`, and `make_macro_gauze.sh`. 8 methodology items added (the subject decides the figurine feel / Chinese-English division of labour / position is weight / fine ≠ smooth / do not name the ears for translucency / square canvas for the microscopic / write lightness as physical items / reverse-constrain makeup) | 小七 |
| 2026-10-02 | v9.0 | **Stage 5: natural makeup + languid daily-life poses**, completing three rounds R27–R29. User feedback "this makeup is too deliberate", "I want full body", "sitting or lying prone, or lying down, a languid everyday feel". R27 located the deliberate blush to the **up-front** sentence `a soft blush of warm colour`, and rewriting it in place fixed it in one round; but all three full-body attempts failed and a new "hands glowing orange" artifact appeared (`translucency ... of the fingertips` executed literally). R28 used **pose up front + a minimal base prompt (1802→635 characters) + 2.67:1** to capture all six poses, and the glowing hands disappeared. R29 added three everyday moments and **restored the crossed collar/yingluo/jade belt**, proving a short base prompt can fully carry named ornaments. Produced the stage-5 delivery set `out/final-set-life/` and the final `out/final-bone-china-princess-life.png`. 6 methodology items added (makeup depends on position / the canvas lever is directional / poses come from deleting words / do not name body parts for translucency / a short base prompt can carry ornaments / desk poses necessarily lose the lower limbs) | 小七 |
| 2026-10-03 | v10.2 | **Attribution correction (R35)**. R34 had attributed the "porcelain feel receding" to the defect list; auditing R25 (the phase-4 material highland) before R35 found that **the defect list is character-for-character identical to R30–R34 and has zero age words, yet the final is young + hard glaze surface + pinholes on the cheeks** — **one sentence overturned that attribution**: the real culprit for the old look is the word `adult` restored by R33 (originally introduced in R4/R5 to cure "too infantile" and never re-reviewed), while the porcelain feel receding in R34 was the **anti-aging negatives** (`aged skin / mature face / wrinkles`) suppressing the glaze. R35 therefore **removed only the anti-aging negatives** (124 characters), changing nothing else → **the glaze returned and the age did not bounce back**, proving that **the positive defines the goal and the negative should not define it a second time**. Incidentally it empirically established that **Qwen is deterministic on this server** (same prompt/seed/negative → decoded pixels byte-identical, PNGs differing only because of embedded metadata). Yielded a landing site where "young + princess temperament + porcelain surface" all hold at once. 3 items added (attribute against a successful sample / the positive defines the goal / determinism verification) | 小七 |
| 2026-10-03 | v10.1 | **Stage 7: return of the princess temperament (R33–R34)**. User feedback "she has no princess temperament, a bit old-looking". The audit found that R28's cut removed, besides the glaze defect list, **the whole block of facial description** — in the base prompt `eyebrow/eyelash/eye/lip/nose/cheek/blush/elegant/adult/young` **all had 0 occurrences**, so the model could only improvise a face from the generic word `princess`, producing a mature, bland, generic adult face. **R33** restored phase-2's facial feature sentence (oval face / high cheekbones / almond eyes / painted eyelashes / eyebrows painted hair by hair / the faintest soft blush) + a Chinese bearing sentence (shapely shoulders and back · chin slightly tucked · clear gaze · reserved nobility), and **removed the blanket blush ban** (R27's `blush/rouge/腮红` contradicted the "very faint blood colour" the positive asked for) → eyelashes/eyebrows/eye shape/lip colour/cheek colour **each took effect**, but the tight portrait still leaned mature. **R34** moved the age anchor **up front into the subject sentence** (character 41), changed `adult`→`youthful`, added `in her early twenties / dewy clear skin`, and extended the negatives with `wrinkles/法令纹/眼袋/老气` → **the old look was essentially eliminated** (5th verification of "position is weight"). ⚠️ It exposed a core contradiction, recorded as unresolved: **"porcelain-surface defects" and the "old look" are two ends of the same lever** — `polishing marks / drag lines` written on the skin were executed as wrinkles, and suppressing them made the porcelain feel recede; the correct fix is to confine the defects to the "glaze" level. 4 items added (an attribute word at the end is as good as not written / write exclusions in the negative / porcelain-surface defects ↔ old look are the same lever / what the positive wants the negative must not ban) | 小七 |
| 2026-10-03 | v10.0 | **Stage 6: material recovery (R30–R32)**. After the user said "back to the image project", re-checking the delivery set revealed that phase-5's bone china texture had been cut away together with R28's "trimming of the base prompt" (**the same mechanism as R11**: deleting material vocabulary for composition). R30 moved phase-4's named defect list back into the short pose base prompt → proving **material density does not pull the camera in** (whole prompt 1254 ≈ the 1283 at which R27 failed, still all full-body); what pulls the camera in is the **clothing list**, not total length; R31 restored the `crisp specular highlights` glaze sentence and added **per-image negatives** to support a **tight-portrait audit sheet** (R30 judging microscopic glaze on a full-body square canvas was a framing mistake); R32 replaced the material assertion `half real skin and half porcelain` with `made of bone china -- the material itself, not a mask` + `Her face is human; her skin is porcelain.`. All three are strict same-seed A/B against R31, yielding a **monotonic three-step ladder**: R29 matte real-human skin → R31 satin sheen → R32 clear glaze — the material assertion is **a dosage lever with adjustable levels**. ⚠️ Reflection on the conclusion: R32 still does not reach R25's hard glaze sheen and pinholes, **but R25 is actually more porcelain than the user brief (half-real half-bone-china)**, and R32 lands in the middle, leaning porcelain, and is therefore a better fit for the brief. 6 methodology items added (downgrades come from deleting vocabulary / the enemy of composition is the clothing list / audit-sheet framing / defect lists are not executed automatically / the assertion is a dosage lever / the same clause means the opposite in a different context) | 小七 |
| 2026-10-02 | v9.1 | **`docs/prompts-all.md` switched to clause-boundary wrapping** (previously each prompt was a single line of 1.8k–3.5k characters, impossible to consult or compare round by round). The wrapping is layout only and **reversible**: added `wrap_prompt()` / `unwrap_prompt()`, with generation asserting clause by clause that "restored == original" (all 114 segments pass) and a line width ≤100 columns; `--dry` supports the legacy rounds R1/R2 and can print the verbatim single-line original directly | 小七 |
