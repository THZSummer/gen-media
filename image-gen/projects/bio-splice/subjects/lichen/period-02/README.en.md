# Period 02 · Foliose Lichen

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/lc-r2-review.en.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**seed 8101 / 8102**
> Overview sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. What this period is about (presentation)

**Tree bark · moist · macro side-high angle · square**

Foliose lichen is **adpressed**, and only a side-high angle can read the lobe edges and the way it attaches at the same time;
the moist bark gives the leaf surface a little sheen.

## 2. This period's subject and result

**Base = fungal mycelium**　**Transplant = foliose thallus FL1 + algal filaments AL2**

| Part | ID | Result |
|------|------|------|
| Foliose thallus | FL1 | ✅ fully established: lobes + pale margins, and the whole thing is an adpressed foliose lichen |
| Algal filaments | AL2 | ✅ established: green fine filaments run between the leaf surfaces (thinner than the algal cell clusters of period 01, hence A=4) |

## 3. Finals

| # | File | Transplanted part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-mycelium-foliose.png`](01-mycelium-foliose.png) | FL1 (**main image**) | **5.00** ✅ preferred | `66db4c27` | `248edfa2d2` |
| 2 | [`02-mycelium-foliose-algae.png`](02-mycelium-foliose-algae.png) | FL1+AL2 | **4.55** ✅ preferred | `0e70ede1` | `8a9ba9bde6` |

Control: [`controls/mycelium.png`](controls/mycelium.png) —— the pure-mycelium base from the **same round**.

## 4. What this period verified

1. Switching to another form on the same base (crustose → foliose) **also worked on the first try**; the form parts do not interfere with each other.
2. **The two wordings of the algal part differ in readability**: cell clusters are more eye-catching than fine filaments (5.00 vs 4.55) —
   from now on, prefer cell clusters when showing "symbiosis".

## 5. How to reproduce

```bash
cd ../../..
python3 run_round.py --subject lichen 2 --dry
python3 run_round.py --subject lichen 2
python3 score.py --round work/lichen/r2/round.json --scores work/lichen/r2/scores.json \
    --control base-mycelium --region surface=200,200,620,620 \
    --audit-sheet subjects/lichen/rounds/lc-r2-audit.jpg \
    --subject lichen -o subjects/lichen/rounds/lc-r2-review.md
python3 curate.py --period subjects/lichen/period-02 --from work/lichen/r2/round.json \
    --pick mycelium-foliose=01-mycelium-foliose --pick mycelium-foliose-algae=02-mycelium-foliose-algae \
    --control base-mycelium=controls/mycelium --note "…" --force
bash make_sheet.sh period subjects/lichen/period-02
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-10-05 | v0.1 | Period 02 "Foliose Lichen" delivered 2 images | 小七 |
