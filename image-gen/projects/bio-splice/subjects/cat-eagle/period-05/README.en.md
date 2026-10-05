# Period 05 · The Triple-Eagle-ified Cat

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [parts table](../parts.en.md) ｜ [review report](../rounds/r13-review.md)
> Engine: Z-Image-Turbo　**1280×1024**　steps 12　**all 4 images share seed 4201** (including the same-round base control)
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. This Period's Characteristics (Presentation)

**Snowfield rain-mist · flat light · telephoto compression 600mm · horizontal 1280×1024**

The closing period is about **presence and mass**: snow plus rain-mist flatten the background into a single sheet of grey, and the 600mm telephoto compresses the cat and the spread eagle wings together; under this presentation the three eagle transplants read as one **raptor-ified beast**.

> The presentation layer is **constant within a period**: every shot in this round (including the base control) shares the same habitat/light/camera/canvas,
> so the "transplant vs base" control stays clean. **It varies between periods** — each of the five periods has its own identity, see
> the period style table on the [sub-theme home page](../README.en.md).

## 2. This Period's Theme and Results

**Base = cat**　**Transplant parts = three sites from the eagle**

| Part | ID | Result |
|------|------|------|
| Eagle neck feathers | E6 | ✅ A thick dark-brown feather ruff grows on the sides of the neck |
| Eagle tail feathers + neck feathers | E5+E6 | ✅ Two sites across regions |
| Eagle wings + tail feathers + neck feathers | E2+E5+E6 | ✅ Three sites stacked, still a single individual (**main image**) |

## 3. Finals

| # | File | Transplant part | Score | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-cat-eagle-ruff.png`](01-cat-eagle-ruff.png) | E6 neck feathers | **4.55** ✅ preferred | `6cc0e647` | `9004e88a52` |
| 2 | [`02-cat-eagle-tail-ruff.png`](02-cat-eagle-tail-ruff.png) | E5+E6 | **4.55** ✅ preferred | `743c101b` | `3254f5eaf1` |
| 3 | [`03-cat-eagle-wings-tail-ruff.png`](03-cat-eagle-wings-tail-ruff.png) | E2+E5+E6 (**main image**) | **4.70** ✅ preferred | `b985e1f1` | `dde7a2453e` |

Control: [`controls/cat.png`](controls/cat.png) — the **same-round** pure-cat base (same seed, same presentation, same sentence skeleton);
every objective metric in this round is measured against it.

## 4. Verification in This Period

1. **The "same region ≤2" constraint holds when stacking across regions**: the three sites (wings / tail feathers / neck feathers) belong to three separate regions; no second individual appeared and no parts crowded each other out.
2. **Snowfield flat light pushes the subject out of the background**: telephoto compression + flat light make both the wingspan and the ruff outlines read clearly — a period that "uses presentation to amplify a mechanism finding".

## 5. How to Reproduce

```bash
cd ../../..
python3 run_round.py --subject cat-eagle 13 --dry
python3 run_round.py --subject cat-eagle 13
python3 score.py --round work/cat-eagle/r13/round.json --scores work/cat-eagle/r13/scores.json \
    --control base-cat --region head=430,60,340,360 --region body=380,420,520,480 \
    --audit-sheet subjects/cat-eagle/rounds/r13-audit.jpg \
    --subject cat-eagle -o subjects/cat-eagle/rounds/r13-review.md
python3 curate.py --period subjects/cat-eagle/period-05 --from work/cat-eagle/r13/round.json \
    --pick c-eagle-ruff=01-cat-eagle-ruff --pick c-eagle-tail-ruff=02-cat-eagle-tail-ruff \
    --pick c-eagle-3parts=03-cat-eagle-wings-tail-ruff \
    --control base-cat=controls/cat.png --note "…" --force
bash make_sheet.sh period subjects/cat-eagle/period-05
```

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-04 | v0.1 | Period 02 delivery: cat ears / cat tail / ears + tail, 3 images in total (original presentation = autumn meadow) | 小七 |
| 2026-10-04 | **v0.2** | **Presentation redone**: switched to snowfield rain-mist + telephoto-compressed horizontal frame, to bring out the mass and presence of the closing period | 小七 |
