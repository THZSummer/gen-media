# Project Template (_template)

> 🌐 Language: **English** | [中文](README.md)

> Back to [project index](../README.en.md) ｜ Technical skills in [../../skills/](../../skills/README.md)

> This directory is a **template**; copy it and adapt. Do not work on a project directly inside _template.

---

## 1. Project background

- **Project name**: <project name>
- **Goal**: <one sentence making clear what images to produce, who they are for, where they are used>
- **Use**: <storyboard upstream / poster cover / character design / e-commerce detail / social media illustration …>
- **Delivery time**: <date>

---

## 2. Deliverables list

| # | Image purpose | Size | Ratio | Quantity |
|---|--------|------|------|------|
| 1 | <main image> | 2560x1440 | 16:9 | 1 |
| 2 | <vertical> | 1440x2560 | 9:16 | 1 |

---

## 3. Skill selection

| # | Skill used | Link | Input material |
|---|----------|------|----------|
| 1 | Text-to-image | [text-to-image-comfyui](../../skills/text-to-image-comfyui/SKILL.md) | - |
| 2 | Control-image edit | [image-edit-comfyui](../../skills/image-edit-comfyui/SKILL.md) | base.jpg (control image) |
| 3 | Contact sheet / compare / metadata strip | [image-tools](../../skills/image-tools/SKILL.md) | Final images |

> Combine the skills under [skills/](../../skills/README.md) as needed (currently 3 in total, all with scripts and self-check entry points).
> The first thing to do with every skill is a **self-check**: `--check` or `test_skill.py`; if the environment is not healthy, do not submit a job.

---

## 4. Image list

| Image no. | Subject | Scene | Viewpoint | Style/tone | Skill used |
|------|------|------|------|-----------|----------|
| 1 | <subject description> | <scene> | Front | <style> | T2I |
| 2 | Same as 1 | Same as 1 | Back | Same as 1 | Multi-view |
| 3 | Same as 1 | <new scene> | Front | Same as 1 | Multi-image reference |

---

## 5. Prompt & parameters

### Image 1

```bash
MODEL="<完整模型 ID，如 doubao-seedream-5-0-lite>"
arkcli +gen --model "$MODEL" \
  --size "2560x1440" --output-format jpeg --seed 42 \
  "<prompt，覆盖主体/场景/风格/构图四要素>" --save-to out/
```

- prompt: <…>
- parameters: size / output-format / seed / guidance-scale …
- reproduction: seed=<…> (record the quadruple model + prompt + seed + size)

### Image 2 (edit, pro example)

```bash
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @out/img1.jpg --size "2560x1440" --output-format jpeg \
  "把背景改成<新场景>，主体保持完全不变" --save-to out/edited/
```

---

## 6. Execution plan

| Stage | Engine | Size | Purpose |
|------|------|------|------|
| Targeting | Z-Image-Turbo (12 steps, ~25s/image) | Small image at the target ratio | Validate subject / style / composition |
| Shaping | Z-Image-Turbo | Target size | Fix prompt and seed |
| Final | Z-Image-Turbo; switch to Qwen-Image if detail is insufficient (7–10 min/image) | Target size | Produce finals |
| Derivative | `image-edit-comfyui` (using the final as control image) | Target size | Change scene / change outfit / add angles |

See "Runtime prerequisites and self-check" in [skills/README.md](../../skills/README.md) for details.

---

## 7. Output record

| Image no. | Version | Model | seed | local_path | Notes |
|------|------|------|------|------------|------|
| 1 | v1 | seedream-5.0-lite | 42 | out/img1.jpg | Final |
| 2 | v1 | seedream-5.0-pro | 7 | out/views/back_v1.jpg | Derived from image 1 |

---

## 8. Checklist

- [ ] Model ID + profile match correctly
- [ ] Size uses `--size` and meets the minimum pixel requirement
- [ ] prompt covers the four elements
- [ ] All artifacts are written to disk; not dependent on 24h URLs
- [ ] Final records model + prompt + seed + size
- [ ] Editor artifacts record the source version
- [ ] If interfacing with video, the image ratio matches the target video

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-02 | v1.0 | Created the image project template | 小七 |
| 2026-10-02 | v1.1 | Following the `methods/`→`skills/` reorganization: links point to SKILL.md, terminology changed to "skill" | 小七 |
