# Period 02 · A Single Stroma

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/cd-r4-review.md)
> Engine: Z-Image-Turbo　**1024×1280**　steps 12　**seed 9101 / 9102**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Features (Presentation)

**Alpine meadow · morning light · low camera macro · portrait 1024×1280**

The stroma is a structure that **stands upright**, so a portrait frame + a ground-hugging low camera shows its height;
the morning light and grass blades give the image a real sense of provenance.

## 2. This Period's Theme and Results

**Base ＝ moth larva**　**Transplant ＝ single stroma ST1**

| Part | ID | Result |
|------|------|------|
| Single stroma | ST1 | ✅ **fully holds**: a single club-shaped stroma rises from the insect body, the most iconic "grass" of cordyceps |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-larva-stroma.png`](01-larva-stroma.png) | ST1 (**main image**) | **5.00** ✅ preferred final | `378a77d6` | `aa2f01482e` |
| 2 | [`02-larva-stroma-b.png`](02-larva-stroma-b.png) | ST1 (seed 9102) | **5.00** ✅ preferred final | `446977d1` | `7820e78aa3` |

Control: [`controls/larva.png`](controls/larva.png) —— the pure larva base from the **same round**.

## 4. This Period's Verification

1. **The stroma works on the first try**: a new addition in an empty slot (67) + a different form (91) + high recognisability (90), all three satisfied at once.
2. **It does not need a bearing structure** (Rule 97): it grows straight out of the body surface, and a landing site exists as long as there is a "body surface" ——
   compare dragon-nines' eagle talons, which must "have limbs first".

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject cordyceps 4 --dry
python3 run_round.py --subject cordyceps 4
python3 score.py --round work/cordyceps/r4/round.json --scores work/cordyceps/r4/scores.json \
    --control base-larva --region body=250,300,520,700 \
    --audit-sheet subjects/cordyceps/rounds/cd-r4-audit.jpg \
    --subject cordyceps -o subjects/cordyceps/rounds/cd-r4-review.md
python3 curate.py --period subjects/cordyceps/period-02 --from work/cordyceps/r4/round.json \
    --pick larva-stroma=01-larva-stroma --pick larva-stroma-b=02-larva-stroma-b \
    --control base-larva=controls/larva --note "…" --force
bash make_sheet.sh period subjects/cordyceps/period-02
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-05 | v0.1 | Period 02 [A Single Stroma] delivered 2 images (all preferred finals) | 小七 |
