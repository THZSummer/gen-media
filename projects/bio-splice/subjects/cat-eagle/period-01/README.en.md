# Period 01 · Cat-Owl (a cat's head + an eagle's body)

> 🌐 Language: **English** | [中文](README.md)

> Back to [sub-theme](../README.en.md) ｜ [project home](../../../README.en.md) ｜ [project index](../../../../README.en.md)
> Engine: Z-Image-Turbo　Size: 1024×1024　steps: 12　**all 5 images share seed 4201**
> Contact sheet: [`sheet.jpg`](sheet.jpg)　Provenance: [`manifest.json`](manifest.json)

---

## 1. Finals of This Period

A literal word-for-word reading of "猫头鹰": **a cat's head + an eagle's body**. One image per splice semantics, three in total, for selection.

| # | File | Splice semantics | seed | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-owl-seamless.png`](01-owl-seamless.png) | **A Seamless blend** (the joint transitions naturally, "as if it had evolved this way") | 4201 | `be679edd` | `64b994f7f3` |
| 2 | [`02-owl-seam.png`](02-owl-seam.png) | **B Visible seam** (a longitudinal stitch line along the front of the neck, taxidermy feel) | 4201 | `c16ee1aa` | `768e4f2e67` |
| 3 | [`03-owl-surreal.png`](03-owl-surreal.png) | **C Surreal** (proportions deliberately wrong, still shot as documentary) | 4201 | `1ccb65b9` | `845bb12956` |

> ⚠️ **C is almost identical to A**: under the same seed the `mean_abs_diff` between the two versions is only **8.9** (the smallest among all controls),
> meaning the "surreal" clause is a **no-op**. If you only want two images, keep 1 and 2.

### Controls (not finals of this period)

| File | Notes |
|------|------|
| [`controls/cat.png`](controls/cat.png) | Degenerate corner: pure cat. Same photographic language as the finals, used to calibrate "which parts come from the splice" |
| [`controls/eagle.png`](controls/eagle.png) | Degenerate corner: pure eagle. Final 1's camera/pose almost coincides with it — **the same eagle with a cat's head swapped in** |

## 2. Single-variable Design

Assembly-style (authoritative source: `_photo()` in [`run_round.py`](../../../run_round.py)):

```
{CN 取景句}{主体定义}. {拼接语义句} {环境句} {摄影层}
     恒定        ↑变化      ↑A/B/C变化      恒定            恒定
```

- **The only variable = the splice-semantics clause**. The framing clause, the environment clause (autumn grass in mist) and the photography layer
  (600mm f/4 shallow depth of field, overcast soft light, no sharpening) are constant across the whole round
- **All 5 images share seed 4201**: the same seed lets the spliced subject reuse the control group's composition, so that A/B/C are comparable with one another
- The framing clause uses Chinese, the material and anatomy use English (following this repo's already-validated Chinese/English division of labour)

## 3. Two Key Techniques

1. **You must not write "猫头鹰" directly** — the model reads it as the species that actually exists. You must write it **decomposed**:
   `whose head is entirely a domestic cat's and whose body is entirely a golden eagle's`.
   This is isomorphic to how that word is built.
2. **The eagle's body must keep its wings** (`folded wings`), otherwise it drifts into a wingless owl plush toy.
   Note that this engine **has no negative prompt**, so every constraint can only be stated positively.

## 4. How to Reproduce

```bash
cd ../../..                      # 到项目根
python3 run_round.py 1 --dry     # 打印逐字 prompt
python3 run_round.py 1           # 重新出图到 work/cat-eagle/r1/（固定 seed，逐像素可复现）
python3 curate.py --period subjects/cat-eagle/period-01 \
    --from work/cat-eagle/r1/round.json \
    --pick owl-seamless=01-owl-seamless \
    --pick owl-seam=02-owl-seam \
    --pick owl-surreal=03-owl-surreal \
    --control cat=controls/cat --control eagle=controls/eagle \
    --note "第一期：猫头鹰（猫的头 + 鹰的身体）" --force
bash make_sheet.sh period subjects/cat-eagle/period-01
```

> The reproduction criterion is the **decoded pixels**, not the file sha (ComfyUI writes the execution graph into the PNG's `tEXt`,
> so changing `filename_prefix` changes the sha while the picture stays the same). Use
> `python3 ../../../../.agents/skills/image-tools/scripts/pngdiff.py a.png b.png`.

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-04 | v0.1 | Period 01 delivery: 3 cat-owl images + 2 controls, with provenance and reproduction steps | 小七 |
