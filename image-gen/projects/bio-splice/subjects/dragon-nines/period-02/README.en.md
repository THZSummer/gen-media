# Period 02 · The Clawed Lizard

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/dn-r5-review.md)
> Engine: Z-Image-Turbo　1024×1024　steps 12　**all 3 images share seed 4201**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Characteristics

**Pebble river bank · post-rain side backlight · low ground-level camera focused on the forefeet · vertical 1024×1280**

This period's camera is **aimed at the "claws"**: the animal lifts its forebody and spreads its forefeet, and then a low camera plus shallow depth of field make the forefeet the visual subject.
In R2 "the claws only partly held and were hard to see"; with this presentation **the long curved raptor-style claws are recognizable at a glance** (score 3.90→4.55).
A completely different identity from Period 01's misty reeds: wet stone, water sheen, backlit silhouette.

## 2. This Period's Theme

The Nine Resemblances' **claws like an eagle (D7)** and **paws like a tiger (D8)**.

The base switches from snake to **lizard** — because Period 01's testing showed that the snake **has no limbs**, so eagle claws "have nowhere to grow".
A lizard likewise has a snake-like body, but it does have limbs.

**Key wording**: the base **deliberately does not describe claws** (it writes `four stout legs` rather than `clawed`),
leaving the foot slot to the transplant — otherwise it would be overridden by the base's own description, as happened with cat-eagle's "cat paws".

| Part | ID | Result |
|------|------|------|
| Eagle talons (forefeet) | D7 | ⚠️ **Partly holds**: the claw shape changes from short and blunt to long curved raptor style, but the feet remain dark and scaly |
| Tiger paws (hind feet) | D8 | ❌ Does not hold: the hind feet remain lizard feet, with no broad thick tiger pads |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-lizard-talons.png`](01-lizard-talons.png) | D7 (**main image**) | **4.55** ✅ preferred | `b067dd4b` | `208886912f` |
| 2 | [`02-lizard-talons-paws.png`](02-lizard-talons-paws.png) | D7+D8 | **4.40** ✅ final | `f404a726` | `000f02adb6` |

Control: [`controls/lizard.png`](controls/lizard.png) — the untransplanted pure-lizard base (same round, same seed).

> ⚠️ **This period's finals "partly hold"**: the claw shape is right, the material is not. The document states this honestly and does not treat it as a complete success.

## 4. Basis for Judgement (3× magnification)

| | Baseline · lizard | After transplant |
|---|---|---|
| Forefoot claw shape | **Short blunt** lizard claws, flat against the ground | **Long curved** raptor-style claws, raised as if gripping |

**Why only "partly"**: `eagle talons` is a **composite part** — claw curvature + yellow scaly tarsi + the black of the claws.
The model executed only the most conspicuous layer (claw curvature). For it to fully hold, the composite part must be split apart into separate clauses,
or the engine switched to one with true negatives (Qwen) to suppress the lizard-foot features.

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject dragon-nines 5 --dry
python3 run_round.py --subject dragon-nines 2
python3 score.py --round work/dragon-nines/r5/round.json --scores work/dragon-nines/r5/scores.json --control base-lizard \
    --region feet=380,560,520,420 --region head=430,120,380,260 \
    --audit-sheet subjects/dragon-nines/rounds/dn-r5-audit.jpg \
    -o subjects/dragon-nines/rounds/dn-r5-review.md
python3 curate.py --period subjects/dragon-nines/period-02 --from work/dragon-nines/r5/round.json \
    --pick lizard-talons=01-lizard-talons \
    --pick lizard-talons-paws=02-lizard-talons-paws \
    --control base-lizard=controls/lizard --note "…" --force
bash make_sheet.sh period subjects/dragon-nines/period-02
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-04 | v0.1 | Period 02 delivery: eagle talons / eagle talons + tiger paws, 2 images in total (claws partly hold, stated honestly) | 小七 |
