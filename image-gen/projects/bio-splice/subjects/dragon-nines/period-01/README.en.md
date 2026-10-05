# Period 01 · The Horned Snake

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/dn-r1-review.md)
> Engine: Z-Image-Turbo　1024×1024　steps 12　**all 3 images share seed 4201**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Theme

The first item of the Nine Resemblances, and the dragon's **strongest hallmark**: **horns like a deer (D1)**.

Base = **snake** (the "neck like a snake" item, i.e. the body's main axis)

| Part | ID | Result |
|------|------|------|
| Deer antlers | D1 | ✅ Forked deer antlers grow naturally from the skull; **reads as a dragon at a glance** |
| Deer antlers + ox ears | D1+D9 | ✅ Both present at once (**two sites in the same region**, within rule 59's ceiling) |

## 2. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-snake-antler.png`](01-snake-antler.png) | D1 deer antlers (**main image**) | **5.00** ✅ preferred | `156422e9` | `dc000f115c` |
| 2 | [`02-snake-antler-ox-ear.png`](02-snake-antler-ox-ear.png) | D1+D9 | **4.65** ✅ preferred | `30dc0dfd` | `1a7924340d` |

Control: [`controls/snake.png`](controls/snake.png) — the untransplanted pure-snake base (same round, same seed).

## 3. One Image Excluded from This Period

`snake-antler-claw` (D1 deer antlers + D7 eagle talons) was **not included**: the antlers hold, but the **eagle talons never appeared at all**.

The reason is not that it was overridden by the base description, but that the snake **has no limbs** — the claws **have nowhere to grow**.
This finding directly changed the planning of the following periods (see §3 of the [sub-theme README](../README.en.md));
Period 02 therefore switched to a lizard base.

## 4. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject dragon-nines 1 --dry
python3 run_round.py --subject dragon-nines 1
python3 score.py --round work/dragon-nines/r1/round.json --scores work/dragon-nines/r1/scores.json --control base-snake \
    --region head=430,120,380,260 --region body=380,560,520,420 \
    --audit-sheet subjects/dragon-nines/rounds/dn-r1-audit.jpg \
    -o subjects/dragon-nines/rounds/dn-r1-review.md
python3 curate.py --period subjects/dragon-nines/period-01 --from work/dragon-nines/r1/round.json \
    --pick snake-antler=01-snake-antler \
    --pick snake-antler-oxear=02-snake-antler-ox-ear \
    --control base-snake=controls/snake --note "…" --force
bash make_sheet.sh period subjects/dragon-nines/period-01
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-04 | v0.1 | Period 01 delivery: deer antlers / deer antlers + ox ears, 2 images in total | 小七 |
