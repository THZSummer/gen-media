# Project Template (_template)

> 🌐 Language: **English** | [中文](README.md)

> Back to [project index](../README.en.md) ｜ Technical methods see [../../methods/](../../methods/README.en.md)

> This directory is a **template**; copy it and rewrite it. Do not run a project directly inside _template.

---

## 1. Project Background

- **Project name**: <project name>
- **Objective**: <one sentence on what video to make and who it is for>
- **Publishing channel**: <e-commerce detail page / short video platform / long video / social media / …>
- **Delivery time**: <date>

---

## 2. Deliverables List

| # | Video purpose | Duration | Ratio | Resolution |
|---|----------|------|------|--------|
| 1 | <main video> | 5s | 16:9 | 1080p |
| 2 | <portrait version> | 5s | 9:16 | 1080p |

---

## 3. Method Selection

| # | Method used | Link | Input material |
|---|----------|------|----------|
| 1 | Image-to-video | [image-to-video](../../methods/image-to-video/README.en.md) | Product image first.jpg |
| 2 | Text-to-video | [text-to-video](../../methods/text-to-video/README.en.md) | - |

> Combine the methods under methods/ as needed. For quality / cost trade-offs see [quality-and-cost](../../methods/quality-and-cost/README.en.md); for multi-shot continuation see [long-video-chain](../../methods/long-video-chain/README.en.md); for shot camera movement see [cinematography](../../methods/cinematography/README.en.md).

---

## 4. Storyboard Table

| Shot no. | Shot size | Camera movement | Content | Duration | Transition | Method used |
|------|------|------|------|------|------|----------|
| 1 | Medium shot | Orbit | <content> | 5s | Continuation | I2V |
| 2 | Close-up | Fixed | <content> | 5s | Hard cut | T2V |

---

## 5. Prompt & Parameters

### Shot 1

```bash
MODEL="<完整模型 ID，如 doubao-seedance-2-0-260128>"
arkcli +gen --model "$MODEL" \
  --input @first.jpg --ratio 16:9 --resolution 1080p \
  "<prompt>" --open
```

- prompt: <…>
- parameters: ratio / resolution / duration / seed …
- reproduction: seed=<…>

---

## 6. Execution Plan

| Stage | Configuration | Purpose |
|------|------|------|
| Direction | draft + 480p | Validate the direction |
| Lock-in | 720p | Settle the plan |
| Final | 1080p + priority | Produce the final |

See [quality-and-cost](../../methods/quality-and-cost/README.en.md) for details.

---

## 7. Output Record

| Shot no. | Version | task_id | local_path | Notes |
|------|------|---------|------------|------|
| 1 | v1 | <task_id> | <path> | |

---

## 8. Checklist

- [ ] A method has been chosen for every video and linked to methods/
- [ ] The prompt has been written according to the method README's strategy
- [ ] The model ID is complete (not a family name)
- [ ] The parameters are within supported_params
- [ ] Execution is staged (Direction / Lock-in / Final)
- [ ] Outputs are saved to local_path (URLs expire after 24h)
- [ ] The content has passed review (see [content-safety](../../methods/content-safety/README.en.md))

---

## Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Initial version of the project template | 小七 |
