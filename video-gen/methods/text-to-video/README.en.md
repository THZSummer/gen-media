# Text-to-Video

> 🌐 Language: **English** | [中文](README.md)

> Input: a single piece of text description. Output: a motion video.
> Back to [methods overview](../README.en.md) ｜ Applicable models: the Seedance series (T2V path)
> 📚 **Official tutorial (seedance-2.0 multimodal / sound effects / editing)**: <https://ark.volcengine.com/region:cn-beijing/docs/82379/2298881?lang=zh> (includes official examples of @video/@image/@audio reference inputs, sound effect descriptions, video extension editing and more)

---

## 1. Topic Positioning

Text-to-video is the **build from scratch** path: you have no image and no reference video, only a description of a picture in your head. It is the baseline capability of video generation and the most direct scenario for testing how expressive a prompt is.

### When to choose T2V

- Abstract concepts, surreal imagery (no existing footage can be shot)
- Quickly validating whether a shot idea holds up
- No image, but the text description is specific enough
- As a control baseline for the other paths

### When not to choose it

- You already have a still image and want to animate it -> go to [image-to-video](../image-to-video/README.en.md)
- You want to replicate some camera movement / action -> go to [reference-video](../reference-video/README.en.md)

---

## 2. Capability Mapping

| Control dimension | Means available under T2V |
|----------|----------------|
| Picture content | Purely described by the prompt |
| Camera movement | Described in the prompt + `--camera-fixed` for a fixed camera |
| Duration | `--duration` / `--frames` (constrained by what the model supports) |
| Resolution / ratio | `--resolution` `--ratio` |
| Reproduction | The same seed reproduces with `--seed` |
| Audio | `--generate-audio` generates synchronously | ✅ 1.5-pro / 2.0 (260128, measured 2026-08-01); ⛔ 2.0-fast / mini have no audio |
| Drafting | `--draft` draft mode for a quick preview |

---

## 3. Prompt Strategy

For text-to-video, success is **80% the prompt**. The model has no image to fall back on; if the description is not good enough the picture is a mess.

### Recommended structure (four parts)

```
[主体] + [动作/状态] + [场景/环境] + [镜头语言 + 风格 + 光影]
```

**Example (good)**:
> 一只柴犬在樱花树下奔跑，慢镜头，花瓣随风飘落，午后逆光，电影感调色，浅景深

**Example (bad, too vague)**:
> 一只狗在跑

### Key points

| Element | Description | Example |
|------|------|------|
| Subject | The more specific the better; avoid "a person" "an animal" | "穿红色卫衣的少年" |
| Action | A clear verb and tense; describe the direction of motion | "从画面左侧跑入，向镜头靠近" |
| Scene | State the environment, weather and time | "雨后城市街道，傍晚，霓虹倒影" |
| Camera | Push / pull / pan / truck / follow / fixed; slow motion / time-lapse | "镜头缓慢拉远，主体居中保持不动" |
| Style | Photorealistic / animation / cyber / film | "35mm 胶片质感，颗粒感" |
| Lighting | Backlight / side light / golden hour | "黄金时刻侧逆光" |

### Anti-patterns (easy to derail)

- A pile of adjectives with no subject action -> a static or randomly moving picture
- Multiple subjects + multiple actions -> the model cannot attend to all of them and subjects jump
- Overly long complex sentences -> key information is diluted; split into short clauses separated by commas
- Writing "do not show XX" -> the model is weak on negative descriptions; positive descriptions work better

---

## 4. Parameter Selection

### Step 2: check available parameters

```bash
arkcli models get "$MODEL" --transform supported_params
```

- `supported_params` non-empty: **use only the listed parameters**, with values inside min/max/enum
- `supported_params` empty: `+gen` automatically applies the video fallback defaults (`resolution=720p` / `duration=5` / `ratio=adaptive`); do not fill them in by hand

### Common parameters

| Parameter | Recommended value | Description |
|------|--------|------|
| `--ratio` | `16:9` / `9:16` / `1:1` | Landscape / portrait / square; choose by publishing channel |
| `--resolution` | Start at `720p`, `1080p` for the final | See [quality-and-cost](../quality-and-cost/README.en.md) |
| `--duration` | `5` (default) | The model limit is usually 5-10s; for longer, use continuation |
| `--seed` | Fix one | Reproduce picture consistency while fine-tuning the prompt |
| `--draft` | Use during the drafting stage | ⛔ not supported by fast/mini; use 480p instead |
| `--camera-fixed` | Use for a static composition | Fixes the virtual camera and avoids unexpected camera movement |

---

## 5. Command Templates

```bash
# 0. 补全完整模型 ID（不要自己猜版本号）
VER=$(arkcli models get doubao-seedance-2-0 --transform 'primary_version' | tr -d '"')
MODEL="doubao-seedance-2-0-${VER:-260128}"

# 1. 标准文生视频（异步，返回 task_id）
arkcli +gen --model "$MODEL" \
  --ratio 16:9 --resolution 720p --duration 5 \
  "一只柴犬在樱花树下奔跑，慢镜头，花瓣飘落，午后逆光，电影感，浅景深" \
  --open

# 2. 同步等结果（阻塞到完成）
arkcli +gen --model "$MODEL" --wait --open \
  "城市夜景航拍，霓虹灯流，延时摄影" 

# 3. 出样稿（草稿模式快速看方向）
arkcli +gen --model "$MODEL" --draft --resolution 480p \
  "赛博朋克街道，雨夜，主角回头" --open

# 4. 固定种子复现微调
arkcli +gen --model "$MODEL" --seed 42 \
  "森林清晨，雾气，光束穿过树冠" --open
```

### Polling after getting the task_id

```bash
arkcli gen get <task_id> --open   # 轮到 succeeded 自动下载 + 桌面弹出
```

---

## 6. Pitfalls

| Symptom | Cause | Handling |
|------|------|------|
| 404 `InvalidEndpointOrModel.NotFound` | A family name was passed to `--model` | Use `models get ... --transform primary_version` to complete the full ID |
| "No response" after submitting | Video is asynchronous; `queued` is not a failure | Poll with `gen get <task_id>`; do not resubmit |
| Subject jumping / blur | The prompt's subject and action are unclear | Strengthen the subject + action description; reduce parallel clauses |
| Unexpected camera movement | The model invents camera work on its own | Add `--camera-fixed` or state the camera in the prompt |
| Parameter rejected `param_not_supported` | The model does not support that parameter | Go back to Step 2 and check supported_params; e.g. 1.5-pro does not support `--priority` |
| Picture blocked by moderation | The prompt contains sensitive words | See [content-safety](../content-safety/README.en.md) |

---

## 7. Checklist

- [ ] `--model` is a complete versioned ID (not a family name)
- [ ] `supported_params` has been checked and all parameters are within the supported range
- [ ] The prompt has the four parts: subject + action + scene + camera style
- [ ] The ratio / resolution matches the publishing channel
- [ ] `--draft` is used during the drafting stage, upgrading to 1080p for the final
- [ ] `--seed` is locked when reproduction is needed
- [ ] The `task_id` is recorded and polled with `gen get` rather than resubmitting
- [ ] The finished output is saved to `local_path` (URLs expire after 24h)

---

## Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-07-18 | v1.0 | Initial topic plan | 小七 |
| 2026-07-18 | v1.1 | Noted that --draft is not supported by fast/mini; switched to 480p | 小七 |
| 2026-07-18 | v1.2 | Noted that --generate-audio is supported only by 1.5-pro, and that the 2.0 series has no audio output | 小七 |
| 2026-08-01 | v1.3 | Correction: seedance-2.0 (260128) measured to support --generate-audio with real audio output; 2.0-fast/mini still have no audio | 小七 |
