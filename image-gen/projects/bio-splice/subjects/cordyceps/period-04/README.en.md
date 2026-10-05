# Period 04 · Stroma and Spores

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/cd-r6-review.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**seed 9101 / 9102**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Features (Presentation)

**Snowline gravel · cold light · landscape 1280×1024**

Moving up to the snowline: a gravel soil surface + patchy snow press the image into a cold tone,
and **cold light does not fight the texture**, which is exactly what lets the powdery spores on the stroma surface read.

## 2. This Period's Theme and Results

**Base ＝ moth larva**　**Transplant ＝ single stroma ST1 + spores SP1**

| Part | ID | Result |
|------|------|------|
| Single stroma | ST1 | ✅ fully holds |
| Spores | SP1 | ✅ fully holds: a layer of powdery spores covers the stroma surface |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-larva-stroma-spores.png`](01-larva-stroma-spores.png) | ST1+SP1 (**main image**) | **5.00** ✅ preferred final | `5c8af570` | `f44e867a64` |
| 2 | [`02-larva-stroma-spores-b.png`](02-larva-stroma-spores-b.png) | ST1+SP1 (seed 9102) | **5.00** ✅ preferred final | `defa9e60` | `b2e4aa7d65` |

Control: [`controls/larva.png`](controls/larva.png) —— the pure larva base from the **same round**.

## 4. This Period's Verification

1. Two parts on the same body (stroma + spores) do not interfere with each other: the spores are merely an **attribute of the stroma surface**
   and take up no extra position —— this is completely different from "two parts competing for the same region" on animal bases.
2. Cold light + patchy snow make the provenance (the snowline) clear, which is the identity difference between this period and periods 02/03.

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject cordyceps 6 --dry
python3 run_round.py --subject cordyceps 6
python3 score.py --round work/cordyceps/r6/round.json --scores work/cordyceps/r6/scores.json \
    --control base-larva --region body=300,250,680,500 \
    --audit-sheet subjects/cordyceps/rounds/cd-r6-audit.jpg \
    --subject cordyceps -o subjects/cordyceps/rounds/cd-r6-review.md
python3 curate.py --period subjects/cordyceps/period-04 --from work/cordyceps/r6/round.json \
    --pick larva-stroma-spores=01-larva-stroma-spores \
    --pick larva-stroma-spores-b=02-larva-stroma-spores-b \
    --control base-larva=controls/larva --note "…" --force
bash make_sheet.sh period subjects/cordyceps/period-04
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-05 | v0.1 | Period 04 [Stroma and Spores] delivered 2 images (all preferred finals) | 小七 |
