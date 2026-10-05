# Period 03 · The Turtle with a Coiled Body

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/ts-r2-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**all 4 images share seed 5101 (plus takes at 5102/5103)**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Ancient well stone platform · side light · side-high angle 100mm · square**

The coiled body is a structure **wrapped around the shell**, and only a **side-high angle** makes the relationship between the shell surface and the coils legible; the side light casts shadows that bring out the undulations of the coil. This is the classic Xuanwu composition.

> The presentation layer is **constant within a period**: every shot in this round (including the base control) shares the same habitat/light/camera/canvas,
> so the "transplant vs base" control is clean; **it varies between periods**, and each of the five periods has its own identity.

## 2. This period's subject and result

**Base = turtle**　**Transplant = coiled body N3**

| Wording | Result |
|------|------|
| ❌ `the thick coiled body of a large snake wrapped around its shell` | **0% landing** (R1) |
| ✅ `a thick snake's body coiled on the stones beneath it…` | ✅ coiled along the left side of the shell on the stone surface |
| ✅ `thick snake coils around its shell` | ✅ the coiling relationship holds (**shortest and most stable**) |
| ✅ `thick snake coils around the rim of its shell` | ✅ the curve rests on the shell rim |

All three wordings landed in the same round, so R1's failure **was not a placeholder problem but a wording problem**.

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-turtle-coil-ground.png`](01-turtle-coil-ground.png) | N3 (coiled on the stone beneath the body, **main image**) | **4.70** ✅ preferred | `a8d7b0f9` | `b1248558db` |
| 2 | [`02-turtle-coil-min.png`](02-turtle-coil-min.png) | N3 (shortest wording) | **4.70** ✅ preferred | `93223dcd` | `766047844d` |
| 3 | [`03-turtle-coil-rim.png`](03-turtle-coil-rim.png) | N3 (around the shell rim) | **4.55** ✅ preferred | `1e1960d7` | `bc71b31a12` |

Control: [`controls/turtle.png`](controls/turtle.png) —— the pure-turtle base from the **same round** (same seed, same presentation, same sentence skeleton),
and every objective metric in this round was measured against it.

## 4. What this period verified

1. **Spatial-relation clauses fail**: `X wrapped around Y` is a no-op; only when it is rewritten as the noun phrase `coils around Y` does it land → **rule 81**.
2. This generalizes rule 69 (compound parts must be written separately) from "inside a part" to "the relationship between the part and the base": **wherever the model needs to understand a spatial relationship, switch to the most direct noun phrase**.

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject turtle-snake 2 --dry
python3 run_round.py --subject turtle-snake 2
python3 score.py --round work/turtle-snake/r2/round.json --scores work/turtle-snake/r2/scores.json \
    --control base-turtle --region shell=300,150,440,320 \
    --audit-sheet subjects/turtle-snake/rounds/ts-r2-audit.jpg \
    --subject turtle-snake -o subjects/turtle-snake/rounds/ts-r2-review.md
python3 curate.py --period subjects/turtle-snake/period-03 --from work/turtle-snake/r2/round.json \
    --pick coil-ground=01-turtle-coil-ground \
    --pick coil-min=02-turtle-coil-min \
    --pick coil-rim=03-turtle-coil-rim \
    --control base-turtle=controls/turtle --note "…" --force
bash make_sheet.sh period subjects/turtle-snake/period-03
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-04 | v0.1 | Period 03 "The Turtle with a Coiled Body" delivered 3 images; pinned down that the real cause of the coil's failure was wording (rule 81) | 小七 |
