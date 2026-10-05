# Period 04 · The Whiskered Eagle

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/r16-review.md)
> Engine: Z-Image-Turbo　**1024×1024**　steps 12　**all 3 images share seed 4201** (including the same-round base control)
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Characteristics (Presentation)

**Dark background · single-side low-angle light · tight face close-up 200mm · square**

Whiskers are a **thin-line** part, and whether they read at all is almost entirely decided by the light. The plan was to use hard noon light, but testing showed that **whiskers are completely unreadable under hard light** (R12); after switching to a **dark background + single-side light**, the thin whiskers are lit into bright strands — this period therefore takes "low-key close-up" as its identity, unlike any of the other four periods.

> The presentation layer is **constant within a period**: every shot in this round (including the base control) shares the same habitat/light/camera/canvas,
> so the "transplant vs base" control stays clean. **It varies between periods** — each of the five periods has its own identity, see
> the period style table on the [sub-theme home page](../README.en.md).

## 2. This Period's Theme and Results

**Base = eagle**　**Transplant parts = facial parts of the cat**

| Part | ID | Result |
|------|------|------|
| Cat whiskers | C6 | ✅ Long thin cat whiskers grow on both sides of the beak base (**main image**) |
| Cat ears + cat whiskers | C1+C6 | ✅ Both in frame; under side backlight the ear outline falls into shadow and is less distinct than the whiskers |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-eagle-cat-whiskers.png`](01-eagle-cat-whiskers.png) | C6 cat whiskers (**main image**) | **5.00** ✅ preferred | `23eb6fdd` | `b5254b6f83` |
| 2 | [`02-eagle-cat-ears-whiskers.png`](02-eagle-cat-ears-whiskers.png) | C1+C6 | **4.55** ✅ preferred | `a918515a` | `4a009cd088` |

Control: [`controls/eagle.png`](controls/eagle.png) — the **same-round** pure-eagle base (same seed, same presentation, same sentence skeleton);
every objective metric in this round is measured against it.

## 4. Verification in This Period

1. **The success or failure of a thin part is decided directly by the light**: the same whisker clause is completely unreadable under hard noon light (R12) and clearly holds under a dark background with single-side light (this round) → choose light **aimed at the part's material**.
2. In a close-up period the CN framing clause must be changed along with it ("head close-up" rather than "full-body portrait"), otherwise the CN layer and the photography layer fight each other (rule 78).

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject cat-eagle 16 --dry
python3 run_round.py --subject cat-eagle 16
python3 score.py --round work/cat-eagle/r16/round.json --scores work/cat-eagle/r16/scores.json \
    --control base-eagle --region whiskers=250,150,520,380 \
    --audit-sheet subjects/cat-eagle/rounds/r16-audit.jpg \
    --subject cat-eagle -o subjects/cat-eagle/rounds/r16-review.md
python3 curate.py --period subjects/cat-eagle/period-04 --from work/cat-eagle/r16/round.json \
    --pick e-cat-whiskers=01-eagle-cat-whiskers \
    --pick e-cat-ears-whiskers=02-eagle-cat-ears-whiskers \
    --control base-eagle=controls/eagle.png --note "…" --force
bash make_sheet.sh period subjects/cat-eagle/period-04
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-04 | v0.1 | Period 02 delivery: cat ears / cat tail / ears + tail, 3 images in total (original presentation = autumn meadow) | 小七 |
| 2026-10-04 | **v0.2** | **Presentation redone**: replaced "hard noon light" with "dark background + single-side light" (whiskers are unreadable under hard light), and switched to a true tight face close-up | 小七 |
