# Character Lookbook (角色设定图库)

> 🌐 Language: **English** | [中文](README.md)

> Back to [project index](../README.en.md) ｜ Technical skills in [../../skills/](../../skills/README.md)
> Example project: demonstrates how to build a reusable character asset library with "text-to-image + multi-view consistency + multi-image reference + image editing".

---

## 1. Project background

- **Project name**: Character Lookbook (character-lookbook)
- **Goal**: build a multi-angle, multi-scene, multi-outfit design library for an **original fictional character**, for reuse in later storyboarding, video I2V and merchandise design
- **Use**: character asset accumulation (not a one-off image batch, but a **derivable** anchor library)
- **Delivery time**: <date>

> ⚠️ **Compliance prerequisite**: the character is original and fictional and does not refer to any real person or existing IP; clothing and poses are designed as normal expression. During generation, self-check content safety and platform review rules as needed.

---

## 2. Deliverables list

| # | Image purpose | Size | Ratio | Quantity |
|---|--------|------|------|------|
| 1 | Three-view (front/side/back, full body) | 1440x2560 | 9:16 | 3 |
| 2 | Three-quarter side | 1440x2560 | 9:16 | 1 |
| 3 | Multi-scene (same character, changed background) | 2560x1440 | 16:9 | 2 |
| 4 | Multi-outfit (same character, changed clothing) | 1440x2560 | 9:16 | 2 |
| 5 | Final avatar / half-body | 2048x2048 | 1:1 | 1 |

---

## 3. Skill selection

| Stage | Skill used | Link | Input material |
|------|----------|------|----------|
| Initial front view | Text-to-image | [text-to-image-comfyui](../../skills/text-to-image-comfyui/SKILL.md) | - |
| Add side/back/half-side views | Control-image edit (using the front view as control image, Canny constrains composition and pose) | [image-edit-comfyui](../../skills/image-edit-comfyui/SKILL.md) | Front anchor image |
| Change scene | Control-image edit (character outline as control image, background changed in the prompt) | [image-edit-comfyui](../../skills/image-edit-comfyui/SKILL.md) | Front anchor image |
| Change outfit | Control-image edit | [image-edit-comfyui](../../skills/image-edit-comfyui/SKILL.md) | Front anchor image |
| Final assembly | Contact sheet / compare / metadata strip | [image-tools](../../skills/image-tools/SKILL.md) | All finals |

> ⚠️ The former three **cloud documentation skills** — "multi-view consistency", "multi-image reference (scene fusion)" and "image editing" — were removed on 2026-10-05 (no scripts, no self-check).
> The current approach is to **replace them with control-image edit (`image-edit-comfyui`)**: take the already-finalized front image as the control image, constrain the character outline and pose, and let only the prompt change the scene/outfit.
> Pure "multi-image fusion" (compositing a character image × a scene image into one) currently has **no usable skill**; add a script-backed implementation later if needed.

---

## 4. Character design and visual anchor

All derived images share the same **visual anchor** (visual anchor = the character description that must be restated in every prompt):

```
东方少女，18 岁，虚构角色；黑长直发，发间一枚青玉簪；浅青水墨渐变纱裙，腰系月白缎带；
赤足，脚踝银铃；身形纤细，气质清泠。青绿水墨画风，留白氛围。
```

> 🔒 **Single anchor**: the library uses the "front full-body image" as the **authoritative anchor**; all other angles/scenes/outfits derive from it, avoiding each being generated from scratch and drifting.

| Reusable asset | Path | Description |
|------------|------|------|
| Front anchor image | `out/views/front_v1.jpg` | Source of all later derivations |
| Visual anchor text | This section | Must accompany every prompt |

---

## 5. Image list

| Image no. | Subject | Scene | Viewpoint | Skill used |
|------|------|------|------|----------|
| 1 | Visual anchor | Plain simple background | Front full body | T2I |
| 2 | Same as 1 | Plain simple background | Front side 90° | Multi-view |
| 3 | Same as 1 | Plain simple background | Back 180° | Multi-view |
| 4 | Same as 1 | Plain simple background | Three-quarter side 45° | Multi-view |
| 5 | Same as 1 | Bamboo grove morning mist, blue-green landscape | Front | Image editing |
| 6 | Same as 1 | Cyber city night, neon light trails | Front | Image editing |
| 7 | Same as 1 | Plain background | Front, moon-white hanfu | Image editing |
| 8 | Same as 1 | Plain background | Front, blue-green dance dress | Image editing |
| 9 | Same as 1 | Plain background | Half-body close-up | T2I |

---

## 6. Prompt & parameters

### Image 1: front anchor (T2I · lite)

```bash
MODEL="doubao-seedream-5-0-lite"
arkcli +gen --model "$MODEL" \
  --size "1440x2560" --output-format jpeg --seed 42 \
  "东方少女，18 岁，虚构角色；黑长直发，发间一枚青玉簪；浅青水墨渐变纱裙，腰系月白缎带；赤足，脚踝银铃；身形纤细，气质清泠。青绿水墨画风，留白氛围。纯色简洁背景，全身正面像，中景，人物居中。" \
  --save-to out/views/
```

- Reproduction quadruple: `lite` + the prompt above + `seed 42` + `1440x2560`

### Image 2: front side view (multi-view · pro)

```bash
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @out/views/front_v1.jpg --size "1440x2560" --output-format jpeg \
  "保持@图像1中人物的形象、黑长直发、青玉簪、浅青水墨纱裙、月白缎带、银铃完全不变，改为正侧面 90° 视角全身像，纯色简洁背景。" \
  --save-to out/views/
```

### Image 3 / 4: back / three-quarter side

Use the template of image 2, replacing the viewpoint with "back 180°" and "three-quarter side 45°"; **both derive directly from `front_v1.jpg`**, do not derive again from the side image.

### Image 5 / 6: change scene (image editing · pro)

```bash
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @out/views/front_v1.jpg --size "2560x1440" --output-format jpeg \
  "人物形象、服装、发饰、配色保持完全不变，背景改为竹林晨雾、青绿山水，光线柔和一致。" \
  --save-to out/scenes/
```

### Image 7 / 8: change outfit (image editing · pro)

```bash
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @out/views/front_v1.jpg --size "1440x2560" --output-format jpeg \
  "人物形象、五官、发型、姿势、背景保持完全不变，服装换成月白色汉服，材质丝绸，配色与整体青绿水墨风一致。" \
  --save-to out/lookbook/
```

### Image 9: half-body close-up (T2I · lite)

Use the visual anchor + "half-body close-up, 1:1 square image, plain background".

---

## 7. Execution plan

| Stage | Model | Size | Purpose |
|------|------|------|------|
| Targeting | lite | 1440x2560 | Try 3–4 phrasings of the visual anchor, choose the look |
| Shaping | lite | 1440x2560 | Fix seed=42, produce the front anchor image and pass review |
| Viewpoint | pro | 1440x2560 | Derive the side/back/half-side three-view from the anchor |
| Scene | pro | 2560x1440 | Edit the background (bamboo grove / cyber) |
| Outfit | pro | 1440x2560 | Edit the clothing (hanfu / dance dress) |
| Final | lite | 2048x2048 | Half-body avatar |

---

## 8. Output record

| Image no. | Version | Model | seed | local_path | Notes |
|------|------|------|------|------------|------|
| 1 | v1 | seedream-5.0-lite | 42 | out/views/front_v1.jpg | ✅ Anchor, final |
| 2 | v1 | seedream-5.0-pro | - | out/views/side_v1.jpg | Derived from image 1 |
| 3 | v1 | seedream-5.0-pro | - | out/views/back_v1.jpg | Derived from image 1 |
| 4 | v1 | seedream-5.0-pro | - | out/views/three-quarter_v1.jpg | Derived from image 1 |
| 5 | v1 | seedream-5.0-pro | - | out/scenes/bamboo_v1.jpg | Derived from image 1 |
| 6 | v1 | seedream-5.0-pro | - | out/scenes/cyber_v1.jpg | Derived from image 1 |
| 7 | v1 | seedream-5.0-pro | - | out/lookbook/hanfu_v1.jpg | Derived from image 1 |
| 8 | v1 | seedream-5.0-pro | - | out/lookbook/dance-dress_v1.jpg | Derived from image 1 |

> Fill in the seed returned by the model and the real file names after actual execution.

---

## 9. Checklist

- [ ] The character is original and fictional, not referring to a real person / IP
- [ ] The front anchor image has passed review and its seed is locked
- [ ] All viewpoints/scenes/outfits derive **directly from the anchor image**
- [ ] Every derived image has been compared item by item with the anchor image (hair ornament, clothing, colour scheme, silver bell)
- [ ] Size uses `--size`, and the ratio matches the purpose
- [ ] All artifacts are written to disk; not dependent on 24h URLs
- [ ] The output record table has been completed with model + seed + path
- [ ] If going into video: the ratio matches the video-gen I2V target, see [image-to-video-fastvideo3](../../../video-gen/skills/image-to-video-fastvideo3/SKILL.md)

---

## Document Revision History

| Date | Version | Change | Author |
|------|---------|--------|------|
| 2026-10-02 | v1.0 | Created the example project: planning a multi-angle/multi-scene/multi-outfit design library for an original character | 小七 |
| 2026-10-02 | v1.1 | Following the `methods/`→`skills/` reorganization: skill links point to SKILL.md, terminology changed to "skill" | 小七 |
| 2026-10-05 | v1.2 | Remapped after the skill convergence: the three cloud documentation skills (text-to-image / multi-view-consistency / image-editing / multi-image-reference) were removed and replaced by a feasible route with three local skills "text-to-image + control-image edit + deterministic tools"; multi-image fusion is still missing | 小七 |
