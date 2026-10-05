# Project Template (_template)

> 🌐 Language: **English** | [中文](README.md)

> Back to [project index](../README.en.md) ｜ Techniques in [../../skills/](../../skills/README.md) ｜ Video methods in [../../methods/](../../methods/README.en.md)

> This directory is a **template**; copy it and adapt. Do not work on a project directly inside _template.
> Image and video projects share this one template: keep the "image list" or the "shot list" section as needed.

---

## 1. Background

- **Name**: <project name>
- **Goal**: <one sentence on what to make, for whom, and where it is used>
- **Kind**: <image / video / image + video>
- **Channel**: <Xiaohongshu / short-video platform / e-commerce detail page / social / ...>
- **Due**: <date>

---

## 2. Deliverables

| # | Purpose | Size or duration | Ratio | Count |
|---|---------|------------------|-------|-------|
| 1 | <main image / main video> | <1024x1360 / 5s> | <3:4 / 16:9> | 1 |
| 2 | <vertical version> | <1080x1440 / 9:16> | <3:4 / 9:16> | 1 |

---

## 3. Technique / method selection

| # | Technique or method | Link | Input |
|---|---------------------|------|-------|
| 1 | Text to image | [text-to-image-comfyui](../../skills/text-to-image-comfyui/SKILL.md) | - |
| 2 | ControlNet image editing | [image-edit-comfyui](../../skills/image-edit-comfyui/SKILL.md) | base.png (control image) |
| 3 | Image to video | [image-to-video-fastvideo3](../../skills/image-to-video-fastvideo3/SKILL.md) | first.jpg |
| 4 | Contact sheet / diff / metadata strip | [image-tools](../../skills/image-tools/SKILL.md) | finals |

> All techniques live in [skills/](../../skills/README.md) (5 of them, each with scripts and a self-check).
> Cloud video methods (Seedance) live in [methods/](../../methods/README.en.md).
> Every technique starts with a **self-check**: `--check` or `test_skill.py`; do not submit work on an unhealthy environment.

---

## 4. Image list / shot list

For image projects (video projects may delete it):

| # | Subject | Scene | Angle | Style / tone | Technique |
|---|---------|-------|-------|--------------|-----------|
| 1 | <subject> | <scene> | front | <style> | T2I |

For video projects (image projects may delete it):

| Shot | Framing | Camera move | Content | Duration | Transition | Technique / method |
|------|---------|-------------|---------|----------|------------|--------------------|
| 1 | medium | orbit | <content> | 5s | match cut | I2V |

---

## 5. Prompt & parameters

### Image / shot 1 (local ComfyUI text to image)

```bash
cd skills/text-to-image-comfyui
python3 scripts/comfyui_gen.py --check          # self-check first
python3 scripts/comfyui_gen.py \
  --prompt "<prompt: subject + scene + style + composition>" \
  --width 1024 --height 1360 --steps 12 --seed 42 --out-dir out/
```

- prompt: <...>
- parameters: width / height / steps / seed
- reproducibility: record the **model + verbatim prompt + parameters + seed** tuple (`--out-dir` automatically keeps `.api.json` and `requests.jsonl`)

### Shot 2 (local ComfyUI image to video)

```bash
cd skills/image-to-video-fastvideo3
python3 scripts/comfyui_i2v.py --check
python3 scripts/comfyui_i2v.py --first first.jpg --prompt "<prompt>" --out-dir out/
```

### Alternative: cloud video (Seedance, pay per use)

```bash
arkcli resources list --modality video                    # list available models
arkcli models get "$MODEL" --transform supported_params   # inspect parameters
arkcli +gen --model "$MODEL" --input @first.jpg --ratio 16:9 --resolution 1080p "<prompt>" --open
```

---

## 6. Execution plan

| Stage | Configuration | Purpose |
|-------|---------------|---------|
| Direction | small image / few steps (or 480p draft) | validate direction: subject / style / composition |
| Shaping | target size / medium steps (or 720p) | settle prompt and seed |
| Final | target size / more steps (or 1080p) | produce the deliverable |
| Derivatives | `image-edit-comfyui` with the final as control | new scenes / outfits / angles |

> Cost trade-offs for the billed path are in [quality-and-cost](../../methods/quality-and-cost/README.en.md); multi-shot continuation in [long-video-chain](../../methods/long-video-chain/README.en.md).

---

## 7. Output log

| # / shot | Version | Model | seed / task_id | local_path | Note |
|----------|---------|-------|----------------|------------|------|
| 1 | v1 | z-image-turbo | seed 42 | out/img1.png | final |

---

## 8. Checklist

- [ ] technique `--check` / `test_skill.py` passes
- [ ] the prompt covers the four elements (subject / scene / style / composition)
- [ ] outputs are written to a **local_path**, not a URL that expires in 24h
- [ ] finals record model + verbatim prompt + parameters + seed (or task_id)
- [ ] ratios align downstream (if feeding video, the image ratio must match the target video)
- [ ] finals are stripped (`image-tools` `ffkit strip`)
- [ ] large intermediates (`work/`, `out/r*/`) are not committed
- [ ] docs are paired (`README.md` + `README.en.md`)

---

## Revision history

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-10-02 | v1.0 | Initial project template (image side) | 小七 |
| 2026-07-18 | v1.0 | Initial project template (video side) | 小七 |
| **2026-10-05** | **v2.0** | **Flattening merge**: the two `_template` directories merged into this one; examples now use the current local ComfyUI techniques, with cloud Seedance demoted to an alternative | 小七 |
