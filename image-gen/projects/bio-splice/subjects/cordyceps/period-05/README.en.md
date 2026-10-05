# Period 05 · Cordyceps (specimen shot · finale)

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/cd-r7-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 9101 / 9102**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Features (Presentation)

**Specimen photography: neutral grey background · ring light · full focus · square**

**The only period in this sub-theme that changes the presentation medium**, and also a first for this project:
no longer a wild ecological shot but a **specimen shot** —— the framing sentence also changes from "macro close-up" to "specimen shot",
and the light becomes ring light + full focus (`f/16`).

## 2. This Period's Theme and Results

**Base ＝ moth larva**　**Transplant ＝ mycelium covering MY1 + stroma ST1 + spores SP1**

| Part | ID | Result |
|------|------|------|
| Mycelium covering | MY1 | ✅ holds |
| Stroma | ST1 | ✅ fully holds |
| Spores | SP1 | ✅ fully holds (clustered at the stroma tips) |
| Three parts on the same body | all | ✅ reads as a single **specimen**, not "an insect + a blade of grass" |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-cordyceps-specimen.png`](01-cordyceps-specimen.png) | MY1+ST1+SP1 (**main image**) | **5.00** ✅ preferred final | `201ca842` | `bc2cc76668` |
| 2 | [`02-cordyceps-specimen-b.png`](02-cordyceps-specimen-b.png) | MY1+ST1+SP1 (seed 9102) | **5.00** ✅ preferred final | `d28740af` | `bcb54576da` |

Control: [`controls/larva.png`](controls/larva.png) —— the pure larva specimen shot from the **same round**.

## 4. This Period's Verification

1. **Changing the presentation medium = a low-cost upgrade for the finale period** (Rule 98): not a word of the parts was changed,
   yet the identity of the deliverable shifts from "photographed" to "collected" ——
   the same insect on a soil surface is an ecological shot; on a grey table it is a specimen.
2. The neutral background pulls all attention back to the **structural relationships**: insect body—mycelium—stroma—spores,
   four layers of relationship read at a glance, which is exactly the value of a "specimen shot".

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject cordyceps 7 --dry
python3 run_round.py --subject cordyceps 7
python3 score.py --round work/cordyceps/r7/round.json --scores work/cordyceps/r7/scores.json \
    --control base-larva --region body=200,250,620,550 \
    --audit-sheet subjects/cordyceps/rounds/cd-r7-audit.jpg \
    --subject cordyceps -o subjects/cordyceps/rounds/cd-r7-review.md
python3 curate.py --period subjects/cordyceps/period-05 --from work/cordyceps/r7/round.json \
    --pick cordyceps-specimen=01-cordyceps-specimen \
    --pick cordyceps-specimen-b=02-cordyceps-specimen-b \
    --control base-larva=controls/larva --note "…" --force
bash make_sheet.sh period subjects/cordyceps/period-05
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-05 | v0.1 | Period 05 [Cordyceps · Specimen Shot] delivered 2 images (finale) | 小七 |
