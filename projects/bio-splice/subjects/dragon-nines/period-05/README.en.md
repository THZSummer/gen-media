# Period 05 · Nine Resemblances · Dragon-Head Close-Up

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/dn-r10-review.en.md)
> Engine: Z-Image-Turbo　1024×1024　steps 12　**all 3 images share seed 4201**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Characteristics

**Morning-mist reeds · side backlight outlining the silhouette · tight face close-up 200mm · square 1024²**

This period is the sub-theme's **only close-up** — the first four periods are all full-body portraits distinguished by habitat and light;
here the lens is pushed onto the face, the background dissolves into a mass of grey, and identity is carried by the **camera**.
The light uses a **side backlight to outline**: the first low-angle sunbeam comes from behind and to the side,
rimming the antlers, ox ears and the scale rows on the sides of the neck with a bright edge, while the front of the face falls into shadow.

## 2. This Period's Theme: the Nine Resemblances, Partly Achieved (put in everything that works)

The plan was to do D2 head like a camel + D3 eyes like a rabbit in this period. **Both failed in testing** (see section 4),
so the closing period instead used the head parts among the Nine Resemblances that are **already verified to hold** to compose a set of dragon-head close-ups:

| Variant | Part | Region distribution | Over the line? |
|------|------|----------|----------|
| `dragon-head` | antlers D1 + ears D9 | **head 2** | No (exactly at the ceiling) |
| `dragon-head-scale` | antlers + ears + fish scales D6 | head 2 · body 1 | No |

The base reuses the **snake** (the "neck like a snake" item is the main axis, and head parts should by rights land on a snake head);
`dragon-head-scale` uses the base **with the scale slot freed** (the same modification as `snake-clean`).

## 3. Finals

| # | File | Part | Score | prompt_id | sha256 |
|---|------|------|------|-----------|--------|
| 1 | [`01-dragon-head.png`](01-dragon-head.png) | antlers + ears (**main image**) | **5.00** ✅ preferred | `b5470cfb` | `a65e257ffb` |
| 2 | [`02-dragon-head-scale.png`](02-dragon-head-scale.png) | antlers + ears + fish scales | **4.70** ✅ preferred | `0cab32ea` | `d74fc18bc8` |

Control: [`controls/snake.png`](controls/snake.png) — the pure-snake base (same round, same seed, same close-up camera).

**The "dragon head" holds**: a complete pair of forked deer antlers plus pointed furry ox ears grow on a snake head,
head raised and tongue flicking, reading as a dragon head rather than "a snake wearing antlers".
This is the sub-theme's **most dragon-like image**, and it also shows that
**the workable route for the Nine Resemblances is "head parts + torso parts", not "swapping the head".**

## 4. Three Things Verified in This Period (Including Two Negative Conclusions)

### 1. ❌ D2 head like a camel: freeing the slot still does not buy a head part (R8)

Both the head shape (`a blunt scaled head`) and the noun (`its head raised`) were deleted from the base,
and then `an elongated camel's head with a blunt muzzle` was written — **none of the four images showed a camel head at all**,
and the picture came out **more "snake"** than the original text (the model added cobra-style neck folds).
That is: freeing the slot is ineffective here, and the model fell back on its own snake prior.

### 2. ❌ D2 in reverse also fails: removing the species noun → the donor takes over the frame (R9)

The hypothesis was that "the source of the placeholder also includes the base's species noun itself", so the base **writes no species name at all**
(`a long muscular low body with keeled scales and a flickering forked tongue`):

| Base | Transplant | Result |
|------|--------|------|
| With species name (`snake`) | camel head | **camel head 0%** — suppressed by the base prior |
| Without species name | camel head | **an entire camel** — the donor took over the whole individual |

**Head parts are a two-way dead end on zimage**:
the base's species noun is both a "placeholder" (blocking the transplant) and an "anchor" (pinning the picture to the base species).
Delete it, and the donor does not merely take over one part — it takes over the whole animal.

> This mirrors rule 57 (`whose body is entirely a deer's` → drags out an entire deer):
> **the danger of naming a whole-body noun holds on the base side as well.**

### 3. ❌ D3 eyes like a rabbit: freeing the eye slot still did not land (R8)

The plan recorded D3 as "adding into an empty slot, likely to succeed", which was a **misjudgement at planning time** —
the base text explicitly writes `dark lidless eyes`, so the eye slot was already occupied.
After freeing it with the "free the slot" method and transplanting, it **still did not land** (the eyes remain snake eyes).
There is no usable technique on this engine for transplanting small parts (eyes).

## 5. How to Reproduce

```bash
cd ../../..
# 期 05 定稿（成品来源）
python3 run_round.py --subject dragon-nines 10 --dry
python3 run_round.py --subject dragon-nines 10
python3 score.py --round work/dragon-nines/r10/round.json --scores work/dragon-nines/r10/scores.json \
    --control base-snake --region head=280,60,480,420 --region body=380,470,320,510 \
    --audit-sheet subjects/dragon-nines/rounds/r10-audit.jpg --subject dragon-nines \
    -o subjects/dragon-nines/rounds/dn-r10-review.md
python3 curate.py --period subjects/dragon-nines/period-05 --from work/dragon-nines/r10/round.json \
    --pick dragon-head=01-dragon-head --pick dragon-head-scale=02-dragon-head-scale \
    --control base-snake=controls/snake --note "…"
bash make_sheet.sh period subjects/dragon-nines/period-05
# 两条否定结论的证据轮
python3 run_round.py --subject dragon-nines 8    # 腾出占位 → 0
python3 run_round.py --subject dragon-nines 9    # 无物种名词 → 整只骆驼
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-04 | v0.1 | Period 05 [Dragon-Head Close-Up] delivery of 2 images; records the two negative conclusions for D2 camel head / D3 rabbit eyes | 小七 |
