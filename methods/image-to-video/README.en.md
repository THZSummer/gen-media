# Image-to-Video (Image-to-Video)

> 🌐 Language: **English** | [中文](README.md)

> Input: first-frame/last-frame image + prompt. Output: a video in which the image "comes to life".
> Back to [method overview](../README.en.md) ｜ Applicable models: Seedance series (I2V path)

---

## 1. Topic positioning

Image-to-video is the path that **uses a still image to drive motion**: you have an existing image (product shot, poster, keyframe, AI-generated still) and want it to produce plausible movement. Compared with T2V, I2V has a **determined starting picture** and far more control, which makes it the most commonly used path for commercial output.

### When to choose I2V

- You already have a product shot/illustration and want to turn it into a motion ad
- Generate a satisfactory still with seedream first, then bring it to life (the two-stage image+video route is the most reliable)
- Keyframe-driven: design the start and end pictures and let the model fill in the motion between them
- Animating posters and covers

### When not to choose it

- You have no image at all and only want to try from text -> [text-to-video](../text-to-video/README.en.md)
- You want to replicate the motion of an existing video -> [reference-video](../reference-video/README.en.md)

---

## 2. Capability mapping

| Control dimension | Means under I2V |
|----------|-------------|
| Starting picture | First-frame image (strong constraint) |
| Ending picture | Last-frame image (optional, `last:` prefix) |
| Motion style | Describe the motion in the prompt + `--camera-fixed` |
| Subject consistency | The first frame locks the subject, far more stable than T2V |
| Multiple image references | Several `--input` images; the first is the first frame, the rest are references |

### Two typical usages

```
A) 单首帧：静图 -> 动起来
   arkcli +gen --model $M --input @first.jpg "镜头缓慢拉远"

B) 首尾帧：起点 + 终点 -> 模型补间
   arkcli +gen --model $M --input first:@a.jpg --input last:@b.jpg "从A平滑过渡到B"
```

---

## 3. First-frame/last-frame strategy

### Single first frame (most common)

- The first `--input` is the first frame by default
- The prompt should focus on describing **motion** rather than the subject's appearance (the appearance is already locked by the image)
- Good prompt: `"镜头缓慢拉远，主体保持不动，背景云层流动"`
- Bad prompt: `"一个穿红衣的少年"` (the appearance is already given by the image, so repeating it only interferes)

### First and last frames (in-between animation)

- Mark them explicitly with `first:` / `last:` to avoid ambiguity
- Good for **transition shots**: expression changes, object morphing, scene changes
- If the two frames differ too much -> distortion/jumps appear in between, so keep the two frames' subject and composition consistent

### Multiple image references

- The first image = first frame; the remaining images act as reference images by default (not first frames)
- To make an image a reference only and not the first frame: use the `ref:` prefix

```bash
# 第一张首帧，第二张仅参考风格
arkcli +gen --model "$MODEL" \
  --input @subject.jpg --input ref:@style.jpg \
  "主体保持，背景切换为参考图的水彩风格"
```

---

## 4. The two-stage workflow (highly recommended)

The most reliable way to produce I2V output is **seedream for images -> seedance for video**:

```
1) seedream 生成满意静图（图片便宜、可反复调）
   arkcli +gen --model doubao-seedream-5-0-260128 --size 1920x1920 "..." 
   -> 得到 first.jpg

2) seedance 用静图当首帧生成视频
   arkcli +gen --model $MODEL --input @first.jpg "镜头缓慢推近" --open
```

**Why it is recommended**:
- Image generation is fast (a few seconds) and cheap, so you can iterate repeatedly until the picture is right
- Video generation is slow and expensive; driving it with a confirmed good image has a far higher first-try success rate than pure T2V
- Subject consistency improves substantially

---

## 5. Parameter selection

| Parameter | I2V recommendation | Notes |
|------|----------|------|
| `--input` | `@first.jpg` or `first:@a.jpg last:@b.jpg` | Required; without an image it is not I2V |
| `--ratio` | Match the first-frame image's aspect ratio | A mismatch gets cropped/stretched |
| `--resolution` | Match the first-frame image's sharpness | A low-res image with a high resolution is pointless |
| `--camera-fixed` | Use for static compositions | Stops the model inventing camera moves |
| `--return-last-frame` | Use when chaining a long video | ⛔ mini does not return it; use the two-stage I2V instead (see also [long-video-chain](../long-video-chain/README.en.md)) |
| `--draft` | Use when testing the motion direction | ⛔ mini does not support it; use 480p instead |

---

## 6. Command templates

```bash
# 补全模型 ID
VER=$(arkcli models get doubao-seedance-2-0 --transform 'primary_version' | tr -d '"')
MODEL="doubao-seedance-2-0-${VER:-260128}"

# 1) 单首帧：静图动起来
arkcli +gen --model "$MODEL" \
  --input @product.jpg --ratio 16:9 --resolution 720p \
  "镜头缓慢拉远，产品居中，背景纯色渐变光影流动" --open

# 2) 首尾帧补间
arkcli +gen --model "$MODEL" \
  --input first:@start.jpg --input last:@end.jpg \
  "表情从微笑自然过渡到大笑" --open

# 3) 两段式：先图后视频
arkcli +gen --model doubao-seedream-5-0-260128 \
  --size 1920x1080 "赛博朋克街道全景，雨夜，霓虹" --open
# (满意后)
arkcli +gen --model "$MODEL" --input @ark-gen.jpeg \
  "镜头向前推进，雨滴落下，霓虹闪烁" --open

# 4) 续接：拿到上一条最后一帧作下一条首帧
arkcli +gen --model "$MODEL" --return-last-frame \
  --input @first.jpg "镜头向右摇" --open
```

---

## 7. Pitfalls

| Symptom | Cause | Fix |
|------|------|------|
| The first frame is altered beyond recognition | The prompt over-describes the appearance | Write only motion in the prompt; leave the appearance to the image |
| `--ratio` does not match the image | Cropping/stretching | Make ratio equal the original image's aspect ratio |
| The wrong first frame with multiple images | The first image is the first frame by default | Mark them explicitly with `first:` `last:` `ref:` |
| Distorted in-between with a last frame | The two frames differ too much | Keep the composition/subject consistent between the two frames |
| A low-res image at 1080p | Upscaling adds no detail | Match the resolution to the material quality |
| Non-image extensions dropped | `--input` routes by extension | Make sure you are passing an image file |

---

## 8. Checklist

- [ ] The first-frame image is good enough (sharp, well composed)
- [ ] `--ratio` matches the first-frame image
- [ ] With multiple images, mark the roles explicitly with `first:`/`last:`/`ref:`
- [ ] The prompt describes only motion and does not repeat the appearance
- [ ] Add `--camera-fixed` for static compositions
- [ ] Prefer the two-stage route (image+video) over pure T2V
- [ ] Add `--return-last-frame` in chaining scenarios

---

## Document revision history

| Date | Version | Changes | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Initial topic plan | 小七 |
| 2026-07-18 | v1.1 | Noted that mini does not support --draft/--return-last-frame | 小七 |
