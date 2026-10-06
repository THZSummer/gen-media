# Bo-Yi R1-R4 · stress-testing countable traits and switching engines

> 🌐 Language: **English** | [中文](r01-review.md)

> Back to the [project entry](../../../README.en.md) ｜ wording and seal rules: [PLAN.en.md](../../../PLAN.en.md) §3/§5 ｜ related records: [fox r05](../../jiu-wei-hu/rounds/r05-review.en.md), [lu-shu r01](../../lu-shu/rounds/r01-review.en.md)

## 1. Why this subject is hard

Bo-yi is the first entry to stack **three countable / counter-intuitive traits** on one beast:

| Trait | Source text | Nature |
|-------|-------------|--------|
| sheep body | 其狀如羊 | ordinary |
| nine tails | 九尾 | **countable**, and in conflict with the concept "sheep" |
| four ears | 四耳 | **countable** (not two) |
| eyes on the back | 其目在背 | **counter-intuitive placement** |

And **the model does not know the name `bo-yi`** (unlike `nine-tailed fox`, a fixed phrase in its training
data). Whether lu-shu's wording conclusion (English naming + itemised traits) transfers is exactly what this
entry tests — and the answer is **no**.

## 2. R1 wording sweep (Z-Image, 9 images): **0/9**

| Variant | How the subject clause is written | Result |
|---------|----------------------------------|--------|
| v1 | `The bo-yi …, a sheep with nine tails, four ears and a pair of eyes on its back` | ordinary ram, one tail |
| v2 | `A sheep of Chinese mythology with nine long tails, four ears and a pair of eyes set in its back` | ordinary ram, one tail |
| v3 | Chinese direct description (same-round control) | one tail, coat drifts brown (the usual failure) |

All nine are **one short tail, two ears, no eyes on the back** — not a single trait landed.
Magnified check: `work/shanhai-jing/corner-inspect/bo-yi-r1-traits.jpg` (ear/head and tail regions at 3x).

> This is the project's first case where "naming + itemised traits" **fails completely**: lu-shu landed all
> four traits, and the fox's nine tails landed 8/8, because those traits do not conflict with the concept the
> model already knows (`nine-tailed fox` is itself a phrase it can draw).

## 3. R2 counting-wording round (Z-Image, 12 images): **0/12**, but one variant reacted

R1 used a **prepositional phrase** (`a sheep with nine tails`); the fox succeeded with a **compound
adjective** (`nine-tailed fox`). So R2 tried three ways of putting the count into the noun phrase / an
explicit contrast:

| Variant | Wording | Result |
|---------|---------|--------|
| w1 | compound adjectives: `The nine-tailed, four-eared bo-yi … a woolly sheep-like beast with a pair of eyes set in its back` | **drew 2-3 extra pale tail plumes** (the only variant that reacted), still not nine tails, no four ears, no back eyes |
| w2 | explicit contrast + spelled counts: `is no ordinary sheep: it has nine tails, four ears and two extra eyes on its back` | ordinary ram, one tail |
| w3 | as w2 but with digits: `9 tails, 4 ears and 2 eyes` | ordinary ram (spotted), one tail |
| w4 | Chinese control (same round) | one tail, brownish |

Evidence at magnification: `work/shanhai-jing/corner-inspect/bo-yi-r2-w1-rear.jpg` (the tail region of the
three w1 images at 3x, showing the extra pale plumes behind the body).

> Conclusion: **putting the count inside the noun phrase is a little stronger than describing it with a
> preposition, but nowhere near enough** — from one tail to 2-3, far from nine; four ears and back eyes
> **never appeared once**.

## 4. R3 engine switch (Qwen-Image + a real negative, 6 images): **it works**

The same machine has a second engine, **Qwen-Image** (`comfyui_qwen.py`): its text encoder is Qwen2.5-VL
(stronger Chinese) and it **supports a real negative** — Z-Image's negative path is `ConditioningZeroOut`
(cfg=1, so passing one does nothing), which this project had never exploited.
Negative: `an ordinary sheep, a single tail, two ears, no eyes on the back, …`.

| Variant | Wording | Result |
|---------|---------|--------|
| q1 | R2 w1's compound adjectives + the negative | **works**: sheep body + tail fan (about 8-9 plumes) + four ears (two pairs) + **one eye on the back** (both seeds 707 and 808 complete) |
| q2 | R2 w2's explicit contrast + the negative | sheep shape + a tail fan, but fewer tails and no obvious back eye (not magnified per image) |
| q3 | new Chinese wording + Chinese negative | **drawn as a fox** (orange coat, pointed muzzle) — the model associates "mythical beast + nine tails" with the nine-tailed fox it knows |

Two side findings:

1. **Qwen-Image does not carry Z-Image's "must stamp a seal" prior**: for R3's four English candidates
   `seal_check.py` shortlisted **0 candidates**, and the corners are clean at 12%/6x by eye — the project's
   first naturally seal-free candidates (see §6).
2. Chinese direct description is **falsified a third time** (6/6 failures on the first two subjects; this time
   even the species changed).

## 5. R4 adding colour (Qwen-Image, 6 images): 4 of 6 drifted into **wolves**

R3 works but renders as **baimiao ink line**, a different register from the series' **ochre colour**
(E would drop). R4 changed only "colour", two wordings x 3 seeds:

| Variant | Wording | Result |
|---------|---------|--------|
| c1 | bone sentence rewritten as "ink lines + ochre / warm brown / pale green washes" | 3 of 6 became wolves; only seed 909 kept the sheep shape (horned, plus an extra forehead eye) |
| c2 | **STYLE kept verbatim**, plus one added clause `The ink lines are washed with soft ochre and warm brown.` | 2 of 6 became wolves; **seed 909 kept the sheep shape** (no horns, four clear ears, one eye on the back, a fan of 8-9 tails) |

> WARNING: **colour words pull the species away.** `soft ochre / warm brown` makes "a brown canid"
> (wolf/fox) more likely and loosens the sheep shape. **The same seed (909) held in both variants**, so this
> is seed-dependent stability rather than a c1/c2 difference — adding colour means **generating several and
> checking the shape of every one**.

## 6. The final (c2-909) and its score

`source_round 4 / source_shot c2-909 / seed 909 / prompt_id 0ac87c38-…` (verbatim prompt in the manifest).

| Dimension (weight) | Score | Basis |
|---|---|---|
| A sourcing accuracy (.25) | 4.5 | sheep body ✓, four ears ✓ (two pairs, clearly countable), eyes on the back ✓ (one clear eye on the spine); **nine tails read as 8-9 plumes** (overlapping, not individually certifiable -> recorded as "visual count" per the R5 lesson) |
| F vitality (.25) | 4.5 | dense fur lines with brush intent, a lively tail fan; denser and more "engraved" than the two sister plates |
| B bone purity (.15) | 4 | gongbi colour (ink lines + ochre / warm brown / pale green washes) holds, but the line density is above the two sisters |
| C format completeness (.15) | 4.5 | generous margin, upright composition, the beast stands on rock |
| D legibility (.10) | 5 | four ears + a back eye + a tail fan: unmistakable at a glance |
| E series consistency (.10) | 4 | same paper, same 3:4, same palette family; one step denser in linework |
| **Weighted total** | **4.43** | >=4.0 with A>=4 and F>=4 -> **preferred final** |

**Seals**: `seal_check.py` shortlisted 9 candidates on the R4 images (x≈820-880); magnification confirmed
they are **all false positives from the warm orange tail fur** (exactly the documented "cinnabar vs ochre/fur
is indistinguishable at the pixel level" mode). Corners at 12%/6x show no seals and no pseudo-characters, so
**this period needed no erasure at all** (evidence:
`work/shanhai-jing/corner-inspect/bo-yi-r4-909-corners.jpg`).

## 7. Takeaways (four new rules, now in PLAN §3)

1. **"Naming + itemised traits" is not a master key**: it only works when the trait is compatible with the
   concept the model already knows. The fox (`nine-tailed fox` is a fixed phrase) landed 8/8; bo-yi (an
   unknown name plus a nine-tailed sheep) landed **0/21**. Wording strength must match how far the trait is
   from the model's concept.
2. **A count inside the noun phrase (compound adjectives) beats a prepositional description**: w1 moved the
   tail from 1 to 2-3 plumes — the only variant that reacted at all on Z-Image (still short of the goal).
3. **Switching engines is a legitimate tool, not a last resort**: the same prompt scored 0/21 on Z-Image and
   worked immediately on Qwen-Image. The engines differ in more than style: **Qwen-Image has a real negative**
   (Z-Image is `ConditioningZeroOut`) and **does not carry Z-Image's "must stamp a seal" prior** (the
   project's first naturally seal-free candidates).
4. **Adding colour costs shape**: `soft ochre / warm brown` pulls the species toward "brown canid" (4 of 6
   became wolves). Add colour only with **more samples plus per-image shape checks**; keeping `STYLE`
   verbatim and appending one explicit colour clause (the c2 form) works.

## 8. Open items

| Item | Status |
|------|--------|
| Certifying the tail count | ⏳ "reads as 8-9 plumes" (visual count); harder evidence needs the control-image route (`scripts/control_image.py` currently only carries a nine-tailed-fox profile) |
| Certifying four ears | ⏳ clear by eye (two pairs); no mechanical certification (per the R5 lesson, that is not a hard gate) |
| Qwen-Image's bone sentence | ⏳ this period used "STYLE + explicit colour clause"; whether the series should settle on one sentence that lands on **both engines** can only be decided by re-running the two earlier subjects in the same round |
| Real seal layer in seal script | ⛔ Still missing (font unresolved) |
| Guo Pu's commentary | ⏳ To be transcribed (no commentary may appear in deliverables before then) |
