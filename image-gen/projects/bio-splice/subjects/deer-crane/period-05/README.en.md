# Period 05 · Deer and Crane in Spring (finale)

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/dc-r6-review.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**seed 7101 onward (multiple takes, see the provenance table)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Spring plum grove · soft diffused light · wide angle · landscape 1280×1024**

Back to the pattern itself: **a deer beneath a blossoming tree in spring** is the classic composition of "deer and crane share spring", and the soft diffused light with falling petals gives the finale a breath of "auspicious pattern".

> The presentation layer is **constant within a period** (every shot in that period, controls included, shares one set) and **varies between periods** (each of the five periods has its own identity).

## 2. This period's subject and result

**Base = deer**　**Transplant = crane neck G1 + crane legs G2 + crane tail feathers G6 (the base does not write legs or tail)**

| Part | ID | Result |
|------|------|------|
| Long neck | G1 | ⚠️ partial |
| Slender legs | G2 | ⚠️ partial |
| Tail feathers | G6 | ✅ fully established (both seeds in this period have the feather fan) |
| Three parts in one body | G1+G2+G6 | ✅ one individual, no second one |

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-deer-crane-3parts.png`](01-deer-crane-3parts.png) | G1+G2+G6 (**main image**) | **4.25** ✅ final | `03f3fa4b` | `510077639c` |
| 2 | [`02-deer-crane-3parts-b.png`](02-deer-crane-3parts-b.png) | G1+G2+G6 (seed 7102) | **4.25** ✅ final | `1e147177` | `2a0a716d2d` |

Control: [`controls/deer.png`](controls/deer.png) —— the pure-deer base from the **same round** (same seed, same presentation, same sentence skeleton).

## 4. What this period verified

1. **The finale honestly labels that "the same body only counts as half"**: all three parts are present, but the neck and the legs only reach partial, and the whole still reads as leaning toward "a lanky deer".
2. This is the project's **only sub-theme whose average score did not reach 4.5** — the reason lies in donor selection: the neck/legs are **the same form** as the base, so the form changes without the material changing (rule 91).

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject deer-crane 6 --dry
python3 run_round.py --subject deer-crane 6
python3 score.py --round work/deer-crane/r6/round.json --scores work/deer-crane/r6/scores.json \
    --control base-deer --region neck=450,150,380,380 --region legs=420,600,420,380 \
    --audit-sheet subjects/deer-crane/rounds/dc-r6-audit.jpg \
    --subject deer-crane -o subjects/deer-crane/rounds/dc-r6-review.md
python3 curate.py --period subjects/deer-crane/period-05 --from work/deer-crane/r6/round.json \
    --pick deer-crane-3parts=01-deer-crane-3parts --pick deer-crane-3parts-b=02-deer-crane-3parts-b \
    --control base-deer=controls/deer --note "…" --force
bash make_sheet.sh period subjects/deer-crane/period-05
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 05 "Deer and Crane in Spring" delivered 2 images (finale, mostly partially established) | 小七 |
