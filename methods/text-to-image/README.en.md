# Text-to-Image (T2I / Seedream)

> 🌐 Language: **English** | [中文](README.md)

> Input: a prompt. Output: a still image. Currently uses `doubao-seedream-5-0-lite` (included in Agent Plan Medium, agent-plan profile).
> Back to [methods overview](../README.en.md)

---

## 1. Topic Positioning

Text-to-image is the path of **generating a still picture from text**: give a description, get an image. In the video generation workflow it mainly serves as an **upstream step**:

| Use | Description |
|------|------|
| **Storyboard frames / keyframes** | First produce each shot's static composition, review it by hand and then animate it with I2V (a rework firewall) |
| **I2V first frame** | seedream generates the first frame → mini I2V continues the motion (two-stage workflow) |
| **Posters / covers** | Short video covers, social media images, detail page images |
| **Proof of concept** | Low-cost validation of whether the image style / tone / composition meets expectations |

### Difference from the video paths

| | Text-to-image T2I (this document) | Text-to-video T2V |
|---|------------------|--------------|
| Output | Still image | Motion video |
| Time / cost | Low (synchronous return) | High (asynchronous + many tokens) |
| Motion | None | Yes |
| Typical use | Storyboard frames, first frames, covers | Final film |

> Recommended flow: **first T2I for images and review → then I2V to animate**, rather than guessing the picture directly with T2V.

---

## 2. Models and Routing

Two Seedream image generation models are currently available (measured 2026-08-01):

| Item | `doubao-seedream-5-0-lite` | `doubao-seedream-5-0-pro` |
|----|---------------------------|---------------------------|
| Positioning | Included in Agent Plan Medium, lightweight | Standalone pay-as-you-go, **precise image editing** |
| Full ID | `doubao-seedream-5-0-lite` | `doubao-seedream-5-0-pro-260628` |
| Profile | agent-plan (default, do not use Auto) | ⚠️ **platform pay-as-you-go** (`--profile platform_cn-beijing_accountwide`, agent-plan not supported) |
| Pixel lower bound | ⚠️ ≥3,686,400 (1920×1080 is rejected) | ✅ No lower bound (1920×1080 works) |
| Core capability | Text-to-image | Text-to-image + **image-to-image editing** (change background / change elements / swap scene, subject can be preserved) |
| Return | Images return synchronously (unlike the asynchronous video path) | Same as left |
| Cost | Images are billed per image | Same as left |

> 🔀 Routing notes:
> - lite uses the **agent-plan** default profile; pro uses **platform pay-as-you-go** (calling pro with agent-plan reports "does not support the agent plan feature").
> - `doubao-seedance-2-0-mini` (video) also uses platform pay-as-you-go; seedream lite (image) uses agent-plan. Do not mix up the three routings.
> - The pro model name must use the **full version ID** `doubao-seedream-5-0-pro-260628` (the family name `doubao-seedream-5-0-pro` is NotFound on the platform data plane; it is visible on the control plane but not deployed on the data plane).

### pro's image editing capability (the core value)

```
文生图生成一张基础图 ──► 拿它当 --input 参考图 ──► 编辑指令改背景/元素/场景
                        （人物主体可保持不变）
```

Measured (2026-08-01):
- Changing the "bamboo forest girl"'s **background into a cyber city** succeeded while the person stayed consistent → a sharp tool for "change of scenery" projects: **one and the same person image, change the background to change the scene**
- For editing, use `--input @image` + an editing instruction prompt; `--size` / `--output-format` are the same as text-to-image

### pro's image-to-image extensions (new, measured 2026-08-02)

| Capability | How | Measured |
|------|------|------|
| **Single image editing** | `--input @image` + editing instruction | ✅ Change pose / background / elements while the subject is preserved |
| **Multi-image reference** | Several `--input @image`, referenced in the prompt as `@图像1/@图像2` | ✅ Character image + scene image fusion ("put the butterfly girl from @图像1 into the desk in @图像2") |
| **Generate a new viewpoint from a reference image** | `--input @front image` + "change to a back / side viewpoint, keep the appearance, clothing and wings unchanged" | ✅ Front → back, appearance stays consistent |

> **Value**: a multi-angle character gallery can be **generated recursively from reference images** (front image → generate back / side), giving far better appearance consistency than generating each one independently (drawing each from nothing). In the prompt, stress "keep the appearance / clothing / wings of @图像N unchanged, change only the viewpoint / pose".

---

## 3. Command Templates

### Single image generation

```bash
# lite（agent-plan 默认）
MODEL="doubao-seedream-5-0-lite"
arkcli +gen --model "$MODEL" \
  --size "2560x1440" --output-format jpeg \
  "<prompt>" --save-to out/

# pro（platform 按量，完整版本 ID；无像素下限，1920x1080 可用）
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --size "2560x1440" --output-format jpeg \
  "<prompt>" --save-to out/
```

> ⚠️ **For image aspect ratio use `--size`, not `--ratio`**: `--ratio` only takes effect for video tasks; when passed to an image task it is ignored (seedream outputs a 2048×2048 square by default). Write the concrete pixels in `--size`.

### pro image editing (change background / swap scene)

```bash
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @base.jpg --size "2560x1440" --output-format jpeg \
  "把背景改成赛博都市夜景，霓虹灯箱与车流光轨，人物保持完全不变" --save-to out/
```

> Applicable scenarios: changing the background for the same person (change of scenery), replacing poster elements, local retouching. Keeping the person depends on the editing instruction stressing "keep the person completely unchanged".

### Common parameters

| Parameter | Description | Example |
|------|------|------|
| `--size` | Output size (pixels, must be ≥3,686,400 pixels) | `2560x1440` (16:9) / `1440x2560` (9:16) / `2048x2048` (1:1) |
| `--output-format` | Output format | `jpeg` / `png` |
| `--image-count` / `--n` | Produce several images at once | `--image-count 4` (when >1, images are produced sequentially automatically) |
| `--seed` | Fix the random seed to reproduce | `--seed 42` |
| `--guidance-scale` | Prompt adherence (float) | `7.5` |
| `--optimize-prompt` | Server-side prompt optimisation | on/off |
| `--response-format` | Return method | `url` / `b64_json` |
| `--stream` | Streaming output (images only) | NDJSON |
| `--save-to` | Output directory | `out/storyboard/` |

> ⚠️ Write portrait / landscape as `--size` pixels; **do not hard-crop** a landscape image into a portrait one (the composition will distort).

---

## 4. Prompt Strategy

The same origin as T2V, but with emphasis on the **static composition**:

1. **Clear subject**: who + wearing what + where (e.g. "modern dancer, female, pale cyan ink-wash gradient gauze dress, simple bun")
2. **Clear scene**: background + light (e.g. "quiet tea room, wood, paper screens, warm light")
3. **Clear tone / style**: cyan-green ink wash, negative space, atmosphere
4. **Clear composition**: shot size (wide / medium / close-up) + the visual focus
5. **A static instant**: pick the most representative freeze ("raising the cup in a pose"); leave the dynamic process to I2V

### Storyboard frame scenarios

Take the shot's **most representative static instant** and do not describe motion:

```
<通用视觉锚点> + <该镜关键姿态描述，如：舞者双手捧盏低头凝神，茶烟升腾，淡雅茶室，青绿水墨色调，留白氛围>
```

> For details see [projects/tea-shake-dance §4.3](../../projects/tea-shake-dance/README.en.md) (storyboard frame generation and review checklist).

---

## 5. Pitfalls

- **Complete model ID**: `doubao-seedream-5-0-lite` (5.0 uses a dot) or `doubao-seedream-5-0-pro-260628` (pro must carry the version; the family name is NotFound on the platform data plane)
- **profile routing**: lite → agent-plan default; pro → ⚠️ **platform pay-as-you-go** (pro under agent-plan reports "does not support the agent plan feature")
- **Synchronous semantics**: images are returned synchronously, no `gen get` polling is needed (that is for video)
- **No `--input` (text-to-image)**: T2I is pure text-to-image with no reference image; only pro editing scenarios add `--input`
- **⚠️ For image aspect ratio use `--size` not `--ratio`**: `--ratio` is exclusive to video tasks; when passed to an image task it is ignored → a 2048×2048 square is output by default, inconsistent with the video aspect ratio. Use pixel values such as `--size "2560x1440"` (16:9).
- **⚠️ Pixel lower bound (lite only)**: lite requires ≥ 3,686,400 pixels (≈2048×1800); 1920×1080 is rejected; **pro has no lower bound** (1920×1080 measured to work). Common sizes: `2560x1440` (16:9), `1440x2560` (9:16), `2048x2048` (1:1)
- **I2V hand-off**: the generated storyboard frames must be saved to disk for the record (`--save-to` / manual mv), because the presigned URL expires after 24h

---

## 6. Checklist

- [ ] The model ID is complete (lite without a version / pro with -260628)
- [ ] The profile is correct (lite→agent-plan / pro→platform pay-as-you-go)
- [ ] Use `--size` to specify the pixel size (including the aspect ratio), not `--ratio`
- [ ] lite needs ≥3,686,400 pixels (pro has no lower bound)
- [ ] The prompt contains subject / scene / tone / composition
- [ ] The image is saved to disk (local_path), not relying on the 24h URL
- [ ] The storyboard frame has passed review (if applicable, see project §4.3)

---

## Revision History

| Date | Version | Change | Author |
|------|------|----------|------|
| 2026-08-01 | v1.0 | Initial version: text-to-image method (seedream-5.0-lite), covering storyboard frame / first frame / cover usage, with command templates, parameters, prompt strategy and pitfalls | 小七 |
| 2026-08-01 | v1.1 | Measured corrections: for image aspect ratio use `--size` rather than `--ratio` (`--ratio` is video-only; when ignored, a 2048×2048 square is the default); recorded the size pixel lower bound of 3,686,400 (1920×1080 rejected) and compliant sizes | 小七 |
| 2026-08-01 | v1.2 | Added seedream-5.0-pro: platform pay-as-you-go routing, full version ID, no pixel lower bound (1920×1080 works), core selling point "precise image editing" (change background / swap scene while keeping the person; bamboo forest → cyber measured successfully); model comparison table + command templates + pitfalls updated | 小七 |
| 2026-08-02 | v1.3 | Newly measured pro image-to-image extensions: multi-image reference (@图像N reference fusion) + generating a new viewpoint from a reference image (front → back while keeping the appearance); multi-angle galleries can be generated recursively | 小七 |
