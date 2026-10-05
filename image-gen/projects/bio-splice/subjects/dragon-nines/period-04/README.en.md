# Period 04 · Assembling the Dragon

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/dn-r7-review.md)
> Engine: Z-Image-Turbo　1024×1024　steps 12　**all 3 images share seed 4201**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Characteristics

**Rocky highland in rain · dusk backlight + rain streaks · wide-angle low camera 35mm · horizontal 1280×1024**

The closing period is about **presence**: wet rock, rain streaks and backlight cast the antler silhouette against the sky,
and the wet scales' reflections pick out the body's texture. Under this presentation the four stacked parts (2 sites on the head + 1 each on the forelimbs and hind limbs) read as a
**genuine dragon-form creature**, rather than "the same lizard with accessories added".

## 2. This Period's Theme: Stack the Workable Parts onto One Individual

As of Period 03, the workable parts among the Nine Resemblances are: **antlers D1 (head), ears D9 (head), claws D7 (forelimbs), paws D8 (hind limbs)**.
This period's "assembling the dragon" stacks them onto one individual, while also respecting rule 59's **region boundary**:

| Variant | Stack | Region distribution | Over the line? |
|------|------|----------|----------|
| `dragon-3parts` | antlers + claws + paws | head 1 · forelimbs 1 · hind limbs 1 | No |
| `dragon-4parts` | antlers + ears + claws + paws | **head 2** · forelimbs 1 · hind limbs 1 | No (the head is exactly at the ceiling of 2) |

The base reuses Period 02's **lizard** (it has limbs, and does not describe claws).

## 3. Finals

| # | File | Stack | Score | prompt_id | sha256 |
|---|------|------|------|-----------|--------|
| 1 | [`01-dragon-3parts.png`](01-dragon-3parts.png) | antlers+claws+paws | **4.40** ✅ final | `a51afce2` | `1795a7e783` |
| 2 | [`02-dragon-4parts.png`](02-dragon-4parts.png) | antlers+ears+claws+paws (**main image**) | **4.70** ✅ preferred | `2695a1ce` | `f5ae48e7f6` |

Control: [`controls/lizard.png`](controls/lizard.png) — the pure-lizard base (same round, same seed).

**"Assembling the dragon" holds**: the lizard grows a complete pair of **forked deer antlers** (the 4-part version also has pointed furry **ox ears**),
and the whole reads as a dragon-form creature rather than a collage.

## 4. Two Things Verified in This Period

### 1. The Region Ceiling Still Holds with 4 Stacked Parts (rule 59 re-verified)

`dragon-4parts` puts all four on (head 2 + forelimbs 1 + hind limbs 1) and **no "extra individual" appeared**.
Compared with the counterexample found in cat-eagle Period 05 (three sites having to share one region → the model draws another individual),
this shows that rule 59's "region ≤2" really is an effective **layout constraint** that can be used directly as a design rule.

### 2. Record Each Part Honestly; Do Not Treat "Partly" as "Fully"

| Part | Result |
|---|---|
D1 deer antlers | ✅ Fully holds |
D9 ox ears | ✅ Fully holds (visible on the head in the 4-part version) |
D7 eagle talons | ⚠️ Partial (long curved claws on the forefeet, as in Period 02) |
D8 tiger paws | ❌ Does not hold (the hind feet remain lizard feet) |

Of the four, two are complete, one is partial and one failed → A is given 4 (two complete count as full; the partial and the failed each cost a point).

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject dragon-nines 7 --dry
python3 run_round.py --subject dragon-nines 4
python3 score.py --round work/dragon-nines/r7/round.json --scores work/dragon-nines/r7/scores.json \
    --control base-lizard --region head=380,100,400,320 --region feet=280,580,420,400 \
    --audit-sheet subjects/dragon-nines/rounds/dn-r7-audit.jpg \
    -o subjects/dragon-nines/rounds/dn-r7-review.md
python3 curate.py --period subjects/dragon-nines/period-04 --from work/dragon-nines/r7/round.json \
    --pick dragon-3parts=01-dragon-3parts --pick dragon-4parts=02-dragon-4parts \
    --control base-lizard=controls/lizard --note "…" --force
bash make_sheet.sh period subjects/dragon-nines/period-04
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-04 | v0.1 | Period 04 [Assembling the Dragon] delivery: 3-site / 4-site stacks, 2 images in total | 小七 |
