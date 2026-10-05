# Period 03 · The Flytrap Flicking Its Tongue

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/ff-r5-review.en.md)
> Engine: Z-Image-Turbo　**1024×1280**　steps 12　**seed 10101 / 10102**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Features (Presentation)

**Moss · low camera · portrait 1024×1280**

To see clearly "the tongue inside the trap cavity", the camera must be **low and facing straight into the cavity**; the portrait frame leaves room for the tongue's curl.
The moss and wetland colours darken the image, so the pink tongue stands out all the more.

## 2. This Period's Theme and Results

**Base ＝ Venus flytrap (wide leaf-blade version)**　**Transplant ＝ tongue T4**

| Part | ID | Landing site | Result |
|------|------|------|------|
| Tongue | T4 | trap cavity (**empty face**) | ✅ **fully holds**: a pink mammal tongue curls out of the trap |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-flytrap-tongue.png`](01-flytrap-tongue.png) | T4 (**main image**) | **5.00** ✅ preferred final | `b4b44ade` | `4e93d157ca` |
| 2 | [`02-flytrap-tongue-b.png`](02-flytrap-tongue-b.png) | T4 (seed 10102) | **5.00** ✅ preferred final | `2b35ec69` | `bb822c0c3c` |

Control: [`controls/flytrap.png`](controls/flytrap.png) —— the pure Venus flytrap from the **same round** (trap open, cavity empty).

## 4. This Period's Verification

1. **The trap cavity is an empty face**, so the tongue's landing site offers no resistance at all (Rules 97/99);
   moreover, once the tongue is there, **the trap is immediately read as a "mouth"** —— the most interesting effect of this period.
2. The tongue's material (pink, wet, curled) contrasts strongly with the plant's green, making this the most plainly readable "cross-kingdom" image.

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject flytrap-fang 5 --dry
python3 run_round.py --subject flytrap-fang 5
python3 score.py --round work/flytrap-fang/r5/round.json --scores work/flytrap-fang/r5/scores.json \
    --control base-flytrap --region lobe=250,200,520,700 \
    --audit-sheet subjects/flytrap-fang/rounds/ff-r5-audit.jpg \
    --subject flytrap-fang -o subjects/flytrap-fang/rounds/ff-r5-review.md
python3 curate.py --period subjects/flytrap-fang/period-03 --from work/flytrap-fang/r5/round.json \
    --pick flytrap-tongue=01-flytrap-tongue --pick flytrap-tongue-b=02-flytrap-tongue-b \
    --control base-flytrap=controls/flytrap --note "…" --force
bash make_sheet.sh period subjects/flytrap-fang/period-03
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-05 | v0.1 | Period 03 [The Flytrap Flicking Its Tongue] delivered 2 images (all preferred finals) | 小七 |
