# Reference Video Generation (Reference-to-Video, R2V)

> 🌐 Language: **English** | [中文](README.md)

> Input: one reference video + a prompt. Output: a new video that keeps the reference video's motion trajectory and replaces the content according to the prompt.
> Back to [methods overview](../README.en.md) ｜ Applicable model: `doubao-seedance-2-0-r2v` (R2V-specific)

---

## 1. Topic Positioning

Reference video is the **borrow the motion, swap the content** path: you have an existing video with camera movement / action you are happy with (shot yourself, or from a stock library), and you want the model to **replicate its motion trajectory** while replacing the protagonist / scene with what you want. In essence it is "motion transfer + content replacement".

### When to choose R2V

- You like the camera movement / rhythm of some video and want it applied to your own subject
- The action is complex and hard to describe precisely with a prompt (dance, martial arts, complex hand gestures)
- You need "the same sense of motion as that video"
- Cross-subject transfer: apply a person's action to a robot / cartoon character

### When not to choose it

- You only want a still image to move -> [image-to-video](../image-to-video/README.en.md)
- You only want to try from text -> [text-to-video](../text-to-video/README.en.md)
- You want to follow a musical rhythm -> [audio-driven](../audio-driven/README.en.md)

---

## 2. Capability Mapping

| Control dimension | Means under R2V |
|----------|-------------|
| Motion trajectory | Strong constraint from the reference video (the core value) |
| Subject / content | The prompt describes what it should be replaced with |
| Style | Style description in the prompt |
| Camera | Follows the reference video; `--camera-fixed` is generally not used |

### Core value

```
参考视频的运动 ──保留──►  新视频的运动
参考视频的内容 ──替换──►  prompt 描述的内容
```

What the model learns is the reference video's **motion field** (how it moves), not its pixels (what it looks like).

---

## 3. Reference Video Selection Strategy

The quality of the reference video directly decides whether R2V succeeds or fails.

### Good reference videos

| Feature | Description |
|------|------|
| Clear motion | The subject's motion is well defined; not a long stretch of stillness |
| Single subject | One clearly defined subject; multiple subjects easily cause transfer confusion |
| Stable lighting | Flickering light interferes with motion extraction |
| Moderate length | Close to the target duration; for longer ones, cut the key segment |
| No occlusion | The subject is not frequently occluded |

### Bad reference videos

- Violent camera shake (lots of motion-field noise)
- Fast cuts and splicing (motion is not continuous)
- The subject is too small or heavily occluded
- A lot of text / UI overlays

### Making your own reference video

When you have no existing footage, you can **shoot it yourself / first use T2V to generate a video whose motion you are happy with** and use it as the reference:

```
1) T2V 生成一段运动满意但内容一般的视频
2) 用它当 R2V 参考视频，替换成目标内容
```

---

## 4. Prompt Strategy

For R2V the prompt focuses on **describing the target content / subject / style**; the motion is left to the reference video.

### Recommended structure

```
[新主体描述] + [新场景/环境] + [风格]
```

**Example**:
> 参考视频保持运动不变，主角替换为一个银色机器人，赛博朋克城市背景，金属质感，电影色调

### Key points

- **State "keep the reference motion" explicitly**: mention "keep the motion trajectory / rhythm of the reference video" in the prompt
- **The new subject must be specific**: colour, material, clothing; avoid vagueness
- **Do not describe motion**: the motion comes from the reference video; writing motion in the prompt conflicts with the reference
- **Unified style**: the style description must cover both subject and scene, otherwise it falls apart

---

## 5. Parameter Selection

| Parameter | R2V recommendation | Description |
|------|----------|------|
| `--input` | `ref:@reference.mp4` | Use the `ref:` prefix to make clear it is a reference video |
| `--ratio` | Same aspect ratio as the reference video | Avoid motion-field misalignment |
| `--resolution` | As needed; 1080p for the final | |
| `--duration` | Close to the reference video's duration | Motion alignment is more natural |
| `--draft` | Use when testing the transfer effect | |

> ⚠️ R2V-specific models (`...-r2v-...`) go through the reference video channel; passing a video as `--input` to an ordinary seedance model may also be recognised as a reference video, but **prefer the r2v-specific model** — transfer quality is more reliable.

---

## 6. Command Templates

```bash
# R2V 专用模型补全
VER=$(arkcli models get doubao-seedance-2-0-r2v --transform 'primary_version' | tr -d '"')
R2V="doubao-seedance-2-0-r2v-${VER:-260128}"

# 1) 标准参考视频生成
arkcli +gen --model "$R2V" \
  --input ref:@reference.mp4 --ratio 16:9 \
  "保持参考视频的运动轨迹，主角替换为银色机器人，赛博朋克城市，金属质感" --open

# 2) 风格迁移（保留运动换画风）
arkcli +gen --model "$R2V" \
  --input ref:@dance.mp4 \
  "保持舞蹈动作，角色改为水彩画风格，柔和水墨晕染" --open

# 3) 自制参考：先 T2V 再 R2V
arkcli +gen --model "$MODEL" "一段镜头环绕产品旋转的运动" --wait --open
# (得到 ref.mp4)
arkcli +gen --model "$R2V" --input ref:@ref.mp4 \
  "保持环绕运动，产品替换为新型耳机，纯白背景，影棚光" --open
```

---

## 7. Pitfalls

| Symptom | Cause | Handling |
|------|------|------|
| Motion is not transferred | A non-r2v model was used / the reference video quality is poor | Prefer the `...-r2v-...` model; switch to a clearer reference video |
| Subject confusion | The reference video has multiple subjects | Crop to a single-subject segment |
| Motion misalignment | `--ratio` does not match the reference | Align the aspect ratio |
| The prompt's motion description conflicts | Describing motion interferes with the reference | Write only the content in the prompt; delete the motion description |
| Video extension not recognised | Non-standard extension | Use a standard format such as `.mp4` |
| Content blocked by moderation | The new subject / scene violates the rules | See [content-safety](../content-safety/README.en.md) |

---

## 8. Checklist

- [ ] An R2V-specific model is used (`...-r2v-...`)
- [ ] The reference video has clear motion, a single subject and stable lighting
- [ ] `--input ref:@video.mp4` uses the `ref:` prefix
- [ ] `--ratio` matches the reference video
- [ ] The prompt describes only the new content / style, with no motion
- [ ] The prompt states "keep the reference motion"
- [ ] When no reference is at hand, one is made with T2V

---

## Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Initial topic plan | 小七 |
