# Period 03 · Multiple Stromata

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/cd-r5-review.en.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 9101 / 9102**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Features (Presentation)

**Alpine meadow · backlight · square**

The same meadow and the same part family as period 02, with only the light changed to **strong backlight**:
the stromata are semi-translucent with glowing tips, and "the shape of the light" separates the layers of the multiple stromata.

## 2. This Period's Theme and Results

**Base ＝ moth larva**　**Transplant ＝ multiple stromata ST1x**

| Part | ID | Result |
|------|------|------|
| Multiple stromata | ST1x | ✅ **fully holds**: four stromata rise from the insect body at once (another seed is a small clump with umbrella-like tips) |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-larva-stromata.png`](01-larva-stromata.png) | ST1x (**main image**) | **5.00** ✅ preferred final | `46c83411` | `3b5c8aa39d` |
| 2 | [`02-larva-stromata-b.png`](02-larva-stromata-b.png) | ST1x (seed 9102) | **5.00** ✅ preferred final | `e1ac376a` | `80f7140cc9` |

Control: [`controls/larva.png`](controls/larva.png) —— the pure larva base from the **same round**.

## 4. This Period's Verification

1. **"Multiple" is equally unproblematic**: for this kind of "part growing out of the body surface", quantity is not a constraint
   (compare "≤2 in the same region" on animal bases; Rule 59 does not apply here —— the insect body surface is a single continuous face to begin with).
2. The backlight brings out the stromata's semi-translucent material, which is the main difference between this period and period 02.

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject cordyceps 5 --dry
python3 run_round.py --subject cordyceps 5
python3 score.py --round work/cordyceps/r5/round.json --scores work/cordyceps/r5/scores.json \
    --control base-larva --region body=200,250,620,550 \
    --audit-sheet subjects/cordyceps/rounds/cd-r5-audit.jpg \
    --subject cordyceps -o subjects/cordyceps/rounds/cd-r5-review.md
python3 curate.py --period subjects/cordyceps/period-03 --from work/cordyceps/r5/round.json \
    --pick larva-stromata=01-larva-stromata --pick larva-stromata-b=02-larva-stromata-b \
    --control base-larva=controls/larva --note "…" --force
bash make_sheet.sh period subjects/cordyceps/period-03
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-05 | v0.1 | Period 03 [Multiple Stromata] delivered 2 images (all preferred finals) | 小七 |
