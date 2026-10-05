# Period 01 · The Mycelium-Covered Insect

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/cd-r3-review.en.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 9101 / 9102 / 9103**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Features (Presentation)

**Soil surface · soft light · macro eye-level 100mm · square**

The first period shoots "the most basic half" first: an insect body covered by mycelium.
A forest-floor soil surface + soft diffused light gives the white mycelium the most direct contrast against the dark soil.

## 2. This Period's Theme and Results

**Base ＝ moth larva (freed version: only head and legs are described, no body-surface texture)**　**Transplant ＝ mycelium covering MY1**

⚠️ **Using the "freed version" as the base is intentional** (Rule 96): in R1's occupied version (`segmented pale body`)
the insect itself is already pale and fuzzy, so the mycelium covering's marginal contribution cannot be seen;
once the body-surface description is freed, the white mycelium covering becomes **obvious at a glance**. All three seeds hold.

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-larva-mycelium.png`](01-larva-mycelium.png) | MY1 (**main image**) | **4.55** ✅ preferred final | `0a0d84ac` | `bc3c839810` |
| 2 | [`02-larva-mycelium-b.png`](02-larva-mycelium-b.png) | MY1 (seed 9102) | **4.55** ✅ preferred final | `fa533870` | `9a2cb8f21b` |
| 3 | [`03-larva-mycelium-c.png`](03-larva-mycelium-c.png) | MY1 (seed 9103) | **4.55** ✅ preferred final | `3e391d97` | `8cbe75747b` |

Control: [`controls/larva.png`](controls/larva.png) —— the pure larva base from the **same round** (freed version, smooth brown).

## 4. This Period's Verification

1. **What can be freed is an "attribute"; what cannot is a "structure"** (Rule 96):
   body-surface texture can be deleted, so the freed version works; compare earlier rounds —— deer legs, fish fins and cat paws are restored even when deleted.
2. The material is still a "fuzzy layer" rather than a true mycelial mat, so A=4 rather than 5 ——**partially holds, recorded as it is**.

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject cordyceps 3 --dry
python3 run_round.py --subject cordyceps 3
python3 score.py --round work/cordyceps/r3/round.json --scores work/cordyceps/r3/scores.json \
    --control base-larva --region body=200,250,620,550 \
    --audit-sheet subjects/cordyceps/rounds/cd-r3-audit.jpg \
    --subject cordyceps -o subjects/cordyceps/rounds/cd-r3-review.md
python3 curate.py --period subjects/cordyceps/period-01 --from work/cordyceps/r3/round.json \
    --pick larva-mycelium=01-larva-mycelium --pick larva-mycelium-b=02-larva-mycelium-b \
    --pick larva-mycelium-c=03-larva-mycelium-c \
    --control base-larva=controls/larva --note "…" --force
bash make_sheet.sh period subjects/cordyceps/period-01
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-05 | v0.1 | Period 01 [The Mycelium-Covered Insect] delivered 3 images (freed-version base) | 小七 |
