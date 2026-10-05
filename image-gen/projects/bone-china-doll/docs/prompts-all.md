# 全部轮次原始 Prompt 存档

> 🌐 语言：**中文** ｜ [English](prompts-all.en.md)

> 本文件由 `python3 run_round.py --prompts` 自动生成，内容 = **实际提交给 ComfyUI 的字符串**。
> 为便于查阅与逐轮对照，代码块内已按分句换行；**换行符不属于 prompt，仅排版**。
> 还原规则：行尾是 ASCII 字符时，该换行等于一个空格；否则换行处原本没有字符。
> `run_round.py` 的 `unwrap_prompt()` 就是这条规则，生成时会逐条断言「还原 == 原文」。
> 逐字原文（单行）另见 `run_round.py` 的 `BASE*` 常量（`python3 run_round.py <N> --dry` 可直接打印）
> 与 `out/rN/round.json`（R7 起）；最终依据是服务器 `GET /history/{prompt_id}`。
> 修改 prompt 请改 `run_round.py`，然后重新生成本文件。
> 返回[项目首页](../README.md)

## 记录在哪（三层）

| 层 | 位置 | 内容 |
|----|------|------|
| 权威源 | `run_round.py`（`BASE*` + `ROUNDS` / `LEGACY_ROUNDS`） | 逐字 prompt（真正发出去的，单行） |
| 可读文档 | 本文件 / `docs/rN.md` | 分句换行的 prompt 全文；每轮改动说明与自检 |
| 机器记录 | `out/rN/round.json` | 文件名 / seed / prompt_id / 引擎 / 参数 / **prompt 原文**（R7 起） |
| 服务器侧 | `GET /history/{prompt_id}` | ComfyUI 实际执行的完整图（最终依据） |

## R1 · baseline (single batch of 5)

- 引擎：`zimage`　尺寸：1024×1024　steps：8
- 方式：**单次请求 batch=5**（5 张共用同一段 prompt，batch 内 seed 递增，起始 seed=100）
- 产物：`out/r1/bc-r1_0000{1..5}_.png`

```text
Museum-quality bone china princess doll, collector-grade photorealistic portrait photograph.
Porcelain skin with soft translucency, fine hand-painted rosy blush,
delicate hand-painted arched eyebrows, long curled eyelashes, glossy lips.
Intricate white lace gown with woven silver threads, beaded pearl bodice, soft blue satin sash,
tiny pearl buttons.
Silver tiara with small diamonds, pearl drop earrings, a single sapphire pendant.
Painted porcelain hands with slender jointed fingers.
Centered head-and-shoulders portrait,
soft diffused studio light with gentle specular highlight on the porcelain cheek,
dark blue-black velvet backdrop, shallow depth of field, 85mm macro lens,
ultra-detailed surface glaze, subtle craquelure, no text
```

## R2 · material realism + glass eyes + 3:4 (single batch of 5)

- 引擎：`zimage`　尺寸：1024×1360　steps：8
- 方式：**单次请求 batch=5**（5 张共用同一段 prompt，batch 内 seed 递增，起始 seed=200）
- 产物：`out/r2/bc-r2_0000{1..5}_.png`

```text
Photorealistic close-up photograph of a handcrafted fine bone china princess doll,
genuine material realism.
Translucent cream-white porcelain face with visible subsurface scattering,
glossy fired glaze with crisp specular highlights, faint hairline craquelure,
delicate hand-painted pink blush fading at the edges,
hand-painted eyebrows with individual hair strokes, glossy glass doll eyes with dark brown irises,
deep pupils and sharp catchlights, sculpted eyelids with soft shadow,
subtle sculpted lips with glaze pooling.
Realistic miniature ball-jointed porcelain arms.
Heavily detailed white lace gown with visible thread structure, hand-sewn pearl beading,
pale blue silk sash, silver filigree tiara set with sapphire and tiny diamonds,
real pearl drop earrings.
Soft large softbox key light from upper left, gentle rim light on porcelain cheek and tiara,
dark desaturated teal studio backdrop, medium format camera, 120mm macro lens,
shallow depth of field, visible material texture, no text, no watermark
```

## R3 · material translucency + elegant proportions + 5 distinct camera setups

- 引擎：`zimage`　尺寸：1024×1360　steps：8
- 张数：5（每张独立请求，seed 各自独立）

### front　seed=300

产物：`out/r3/bc-r3-front_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china princess doll.
Translucent cream-white porcelain with visible subsurface scattering, glossy fired glaze,
crisp specular highlights, faint hairline craquelure, hand-painted eyebrows drawn hair by hair,
glossy glass doll eyes with hazel irises and sharp catchlights, finely sculpted eyelids and lips.
Elegant serene princess face with refined oval features, slender neck, gentle expression,
not a toddler, not cartoonish.
Very subtle soft blush.
White lace gown with visible thread structure, hand-sewn pearl beading, pale blue silk sash,
silver filigree tiara set with sapphire and tiny diamonds, real pearl drop earrings.
Museum collector piece, medium format camera, 120mm macro lens, shallow depth of field,
clean seamless studio backdrop, no studio equipment visible, no text, no watermark,
centered head-and-shoulders portrait, facing camera, large softbox key light from upper left,
soft rim light on the tiara, deep muted teal backdrop
```

### three-quarter-fan　seed=310

产物：`out/r3/bc-r3-three-quarter-fan_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china princess doll.
Translucent cream-white porcelain with visible subsurface scattering, glossy fired glaze,
crisp specular highlights, faint hairline craquelure, hand-painted eyebrows drawn hair by hair,
glossy glass doll eyes with hazel irises and sharp catchlights, finely sculpted eyelids and lips.
Elegant serene princess face with refined oval features, slender neck, gentle expression,
not a toddler, not cartoonish.
Very subtle soft blush.
White lace gown with visible thread structure, hand-sewn pearl beading, pale blue silk sash,
silver filigree tiara set with sapphire and tiny diamonds, real pearl drop earrings.
Museum collector piece, medium format camera, 120mm macro lens, shallow depth of field,
clean seamless studio backdrop, no studio equipment visible, no text, no watermark,
three-quarter view, holding a white lace fan near her cheek, soft key light from the right,
gentle shadow under the jaw, warm grey backdrop
```

### profile-translucent　seed=320

产物：`out/r3/bc-r3-profile-translucent_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china princess doll.
Translucent cream-white porcelain with visible subsurface scattering, glossy fired glaze,
crisp specular highlights, faint hairline craquelure, hand-painted eyebrows drawn hair by hair,
glossy glass doll eyes with hazel irises and sharp catchlights, finely sculpted eyelids and lips.
Elegant serene princess face with refined oval features, slender neck, gentle expression,
not a toddler, not cartoonish.
Very subtle soft blush.
White lace gown with visible thread structure, hand-sewn pearl beading, pale blue silk sash,
silver filigree tiara set with sapphire and tiny diamonds, real pearl drop earrings.
Museum collector piece, medium format camera, 120mm macro lens, shallow depth of field,
clean seamless studio backdrop, no studio equipment visible, no text, no watermark,
strict side profile with the light behind the doll so light glows through the thin porcelain of the
ear,
cheek and neck, dark backdrop, strong rim light
```

### hands-lap　seed=330

产物：`out/r3/bc-r3-hands-lap_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china princess doll.
Translucent cream-white porcelain with visible subsurface scattering, glossy fired glaze,
crisp specular highlights, faint hairline craquelure, hand-painted eyebrows drawn hair by hair,
glossy glass doll eyes with hazel irises and sharp catchlights, finely sculpted eyelids and lips.
Elegant serene princess face with refined oval features, slender neck, gentle expression,
not a toddler, not cartoonish.
Very subtle soft blush.
White lace gown with visible thread structure, hand-sewn pearl beading, pale blue silk sash,
silver filigree tiara set with sapphire and tiny diamonds, real pearl drop earrings.
Museum collector piece, medium format camera, 120mm macro lens, shallow depth of field,
clean seamless studio backdrop, no studio equipment visible, no text, no watermark, waist-up,
seated with both porcelain hands resting on her lap, ball-jointed wrist seams visible,
balanced soft light, muted blue-grey backdrop
```

### full-figure　seed=340

产物：`out/r3/bc-r3-full-figure_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china princess doll.
Translucent cream-white porcelain with visible subsurface scattering, glossy fired glaze,
crisp specular highlights, faint hairline craquelure, hand-painted eyebrows drawn hair by hair,
glossy glass doll eyes with hazel irises and sharp catchlights, finely sculpted eyelids and lips.
Elegant serene princess face with refined oval features, slender neck, gentle expression,
not a toddler, not cartoonish.
Very subtle soft blush.
White lace gown with visible thread structure, hand-sewn pearl beading, pale blue silk sash,
silver filigree tiara set with sapphire and tiny diamonds, real pearl drop earrings.
Museum collector piece, medium format camera, 120mm macro lens, shallow depth of field,
clean seamless studio backdrop, no studio equipment visible, no text, no watermark,
full figure standing on a velvet cushion, complete gown with train visible,
low-key museum lighting, distant soft spotlight, dark hall backdrop
```

## R4 · no equipment words, adult proportions, single pearl strand, anti-artifact terms

- 引擎：`zimage`　尺寸：1024×1360　steps：8
- 张数：5（每张独立请求，seed 各自独立）

### beauty-portrait　seed=400

产物：`out/r4/bc-r4-beauty-portrait_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china princess doll, museum collector piece.
Uniform glossy fired glaze over cream-white porcelain, crisp specular highlights,
faint hairline craquelure,
delicate warm translucency where the porcelain is thin at the rim of the ears and fingertips.
Elegant adult princess proportions, refined oval face, defined jawline, slender tapered neck,
small head relative to the body, serene gentle expression, not a child, not cartoonish.
Hand-painted eyebrows drawn hair by hair, glossy glass doll eyes with hazel irises,
deep pupils and sharp catchlights, finely sculpted eyelids and lips, very subtle soft blush.
White lace gown with clearly visible thread structure, a single strand of pearls at the neckline,
hand-sewn beadwork, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, real pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, ultra-detailed surface, centered composition, no text, no watermark,
no floating objects, no extra limbs, tight beauty portrait, eye level, quiet grey-blue backdrop,
soft falloff on the shoulders
```

### fan-three-quarter　seed=410

产物：`out/r4/bc-r4-fan-three-quarter_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china princess doll, museum collector piece.
Uniform glossy fired glaze over cream-white porcelain, crisp specular highlights,
faint hairline craquelure,
delicate warm translucency where the porcelain is thin at the rim of the ears and fingertips.
Elegant adult princess proportions, refined oval face, defined jawline, slender tapered neck,
small head relative to the body, serene gentle expression, not a child, not cartoonish.
Hand-painted eyebrows drawn hair by hair, glossy glass doll eyes with hazel irises,
deep pupils and sharp catchlights, finely sculpted eyelids and lips, very subtle soft blush.
White lace gown with clearly visible thread structure, a single strand of pearls at the neckline,
hand-sewn beadwork, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, real pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, ultra-detailed surface, centered composition, no text, no watermark,
no floating objects, no extra limbs,
three-quarter view holding a white lace fan open beside her face, warm neutral backdrop,
gentle shadow under the jaw
```

### rimlight-profile　seed=420

产物：`out/r4/bc-r4-rimlight-profile_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china princess doll, museum collector piece.
Uniform glossy fired glaze over cream-white porcelain, crisp specular highlights,
faint hairline craquelure,
delicate warm translucency where the porcelain is thin at the rim of the ears and fingertips.
Elegant adult princess proportions, refined oval face, defined jawline, slender tapered neck,
small head relative to the body, serene gentle expression, not a child, not cartoonish.
Hand-painted eyebrows drawn hair by hair, glossy glass doll eyes with hazel irises,
deep pupils and sharp catchlights, finely sculpted eyelids and lips, very subtle soft blush.
White lace gown with clearly visible thread structure, a single strand of pearls at the neckline,
hand-sewn beadwork, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, real pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, ultra-detailed surface, centered composition, no text, no watermark,
no floating objects, no extra limbs,
near-profile with warm light travelling along the porcelain rim of the cheek and ear,
dark charcoal backdrop
```

### seated-hands　seed=430

产物：`out/r4/bc-r4-seated-hands_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china princess doll, museum collector piece.
Uniform glossy fired glaze over cream-white porcelain, crisp specular highlights,
faint hairline craquelure,
delicate warm translucency where the porcelain is thin at the rim of the ears and fingertips.
Elegant adult princess proportions, refined oval face, defined jawline, slender tapered neck,
small head relative to the body, serene gentle expression, not a child, not cartoonish.
Hand-painted eyebrows drawn hair by hair, glossy glass doll eyes with hazel irises,
deep pupils and sharp catchlights, finely sculpted eyelids and lips, very subtle soft blush.
White lace gown with clearly visible thread structure, a single strand of pearls at the neckline,
hand-sewn beadwork, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, real pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, ultra-detailed surface, centered composition, no text, no watermark,
no floating objects, no extra limbs, seated waist-up,
both porcelain hands folded on her lap with visible ball-joint seams at the wrists,
soft even light, muted blue-grey backdrop
```

### full-figure-cushion　seed=440

产物：`out/r4/bc-r4-full-figure-cushion_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china princess doll, museum collector piece.
Uniform glossy fired glaze over cream-white porcelain, crisp specular highlights,
faint hairline craquelure,
delicate warm translucency where the porcelain is thin at the rim of the ears and fingertips.
Elegant adult princess proportions, refined oval face, defined jawline, slender tapered neck,
small head relative to the body, serene gentle expression, not a child, not cartoonish.
Hand-painted eyebrows drawn hair by hair, glossy glass doll eyes with hazel irises,
deep pupils and sharp catchlights, finely sculpted eyelids and lips, very subtle soft blush.
White lace gown with clearly visible thread structure, a single strand of pearls at the neckline,
hand-sewn beadwork, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, real pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, ultra-detailed surface, centered composition, no text, no watermark,
no floating objects, no extra limbs, full figure standing on a velvet cushion,
gown and short train fully visible, low-key museum light, dark hall backdrop,
slight low camera angle
```

## R5 · figurine + adult princess face, steps 12, ivory pearls, fabric folds

- 引擎：`zimage`　尺寸：1024×1360　steps：12
- 张数：5（每张独立请求，seed 各自独立）

### portrait　seed=500

产物：`out/r5/bc-r5-portrait_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china figurine of a princess,
museum collector piece.
Uniform glossy fired glaze over cream-white porcelain, crisp specular highlights,
faint hairline craquelure,
delicate warm translucency where the porcelain is thinnest at the rim of the ears and fingertips.
The face is an elegant young woman in her early twenties: refined oval face, high cheekbones,
defined jawline, straight nose bridge, serene closed lips with a faint smile,
proportionally sized almond eyes with a subtle eyelid crease,
glossy glass eyes with warm hazel irises, deep pupils and sharp catchlights,
finely sculpted eyelids.
Slender tapered neck, small head relative to the body, poised posture, not a child, not cartoonish,
not a toy.
Hand-painted eyebrows drawn hair by hair, very subtle soft blush.
White lace gown with clearly visible thread structure and soft fabric folds,
a single strand of warm ivory pearls at the neckline, hand-sewn beadwork, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, ultra-detailed surface, centered composition, no text, no watermark,
no floating objects, no extra limbs, no skin blemishes, tight beauty portrait, eye level,
cool grey backdrop
```

### bouquet　seed=510

产物：`out/r5/bc-r5-bouquet_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china figurine of a princess,
museum collector piece.
Uniform glossy fired glaze over cream-white porcelain, crisp specular highlights,
faint hairline craquelure,
delicate warm translucency where the porcelain is thinnest at the rim of the ears and fingertips.
The face is an elegant young woman in her early twenties: refined oval face, high cheekbones,
defined jawline, straight nose bridge, serene closed lips with a faint smile,
proportionally sized almond eyes with a subtle eyelid crease,
glossy glass eyes with warm hazel irises, deep pupils and sharp catchlights,
finely sculpted eyelids.
Slender tapered neck, small head relative to the body, poised posture, not a child, not cartoonish,
not a toy.
Hand-painted eyebrows drawn hair by hair, very subtle soft blush.
White lace gown with clearly visible thread structure and soft fabric folds,
a single strand of warm ivory pearls at the neckline, hand-sewn beadwork, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, ultra-detailed surface, centered composition, no text, no watermark,
no floating objects, no extra limbs, no skin blemishes,
three-quarter view holding a small bouquet of white porcelain flowers, warm neutral backdrop,
soft shadow under the jaw
```

### fan　seed=520

产物：`out/r5/bc-r5-fan_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china figurine of a princess,
museum collector piece.
Uniform glossy fired glaze over cream-white porcelain, crisp specular highlights,
faint hairline craquelure,
delicate warm translucency where the porcelain is thinnest at the rim of the ears and fingertips.
The face is an elegant young woman in her early twenties: refined oval face, high cheekbones,
defined jawline, straight nose bridge, serene closed lips with a faint smile,
proportionally sized almond eyes with a subtle eyelid crease,
glossy glass eyes with warm hazel irises, deep pupils and sharp catchlights,
finely sculpted eyelids.
Slender tapered neck, small head relative to the body, poised posture, not a child, not cartoonish,
not a toy.
Hand-painted eyebrows drawn hair by hair, very subtle soft blush.
White lace gown with clearly visible thread structure and soft fabric folds,
a single strand of warm ivory pearls at the neckline, hand-sewn beadwork, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, ultra-detailed surface, centered composition, no text, no watermark,
no floating objects, no extra limbs, no skin blemishes,
three-quarter view with an open white lace fan beside her face, soft even light, muted teal backdrop
```

### seated　seed=530

产物：`out/r5/bc-r5-seated_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china figurine of a princess,
museum collector piece.
Uniform glossy fired glaze over cream-white porcelain, crisp specular highlights,
faint hairline craquelure,
delicate warm translucency where the porcelain is thinnest at the rim of the ears and fingertips.
The face is an elegant young woman in her early twenties: refined oval face, high cheekbones,
defined jawline, straight nose bridge, serene closed lips with a faint smile,
proportionally sized almond eyes with a subtle eyelid crease,
glossy glass eyes with warm hazel irises, deep pupils and sharp catchlights,
finely sculpted eyelids.
Slender tapered neck, small head relative to the body, poised posture, not a child, not cartoonish,
not a toy.
Hand-painted eyebrows drawn hair by hair, very subtle soft blush.
White lace gown with clearly visible thread structure and soft fabric folds,
a single strand of warm ivory pearls at the neckline, hand-sewn beadwork, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, ultra-detailed surface, centered composition, no text, no watermark,
no floating objects, no extra limbs, no skin blemishes,
seated waist-up with both hands folded on her lap, visible ball-joint seams at the wrists,
soft even light, blue-grey backdrop
```

### full-figure　seed=540

产物：`out/r5/bc-r5-full-figure_00001_.png`

```text
Photorealistic photograph of a handcrafted fine bone china figurine of a princess,
museum collector piece.
Uniform glossy fired glaze over cream-white porcelain, crisp specular highlights,
faint hairline craquelure,
delicate warm translucency where the porcelain is thinnest at the rim of the ears and fingertips.
The face is an elegant young woman in her early twenties: refined oval face, high cheekbones,
defined jawline, straight nose bridge, serene closed lips with a faint smile,
proportionally sized almond eyes with a subtle eyelid crease,
glossy glass eyes with warm hazel irises, deep pupils and sharp catchlights,
finely sculpted eyelids.
Slender tapered neck, small head relative to the body, poised posture, not a child, not cartoonish,
not a toy.
Hand-painted eyebrows drawn hair by hair, very subtle soft blush.
White lace gown with clearly visible thread structure and soft fabric folds,
a single strand of warm ivory pearls at the neckline, hand-sewn beadwork, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, ultra-detailed surface, centered composition, no text, no watermark,
no floating objects, no extra limbs, no skin blemishes, full figure standing on a velvet cushion,
complete gown with lace fabric folds and a short train, low-key museum light, dark hall backdrop
```

## R6 · final z-image round: steps 16 + micro-detail demands + macro close-up shot

- 引擎：`zimage`　尺寸：1024×1360　steps：16
- 张数：5（每张独立请求，seed 各自独立）

### macro-face　seed=600

产物：`out/r6/bc-r6-macro-face_00001_.png`

```text
Photorealistic macro photograph of a handcrafted fine bone china figurine of a princess,
museum collector piece, ultra-detailed.
Uniform glossy fired glaze over cream-white porcelain with visible micro glaze texture and fine
craquelure lines,
crisp specular highlights,
delicate warm translucency where the porcelain is thinnest at the rim of the ears and fingertips.
The face is an elegant young woman in her early twenties: refined oval face, high cheekbones,
defined jawline, straight nose bridge, serene closed lips with a faint smile,
individually rendered eyelashes, proportionally sized almond eyes with a subtle eyelid crease,
glossy glass eyes with warm hazel irises, deep pupils and sharp catchlights.
Slender tapered neck, poised posture, not a child, not cartoonish, not a toy.
Hand-painted eyebrows drawn hair by hair, very subtle soft blush.
White lace gown with clearly visible thread structure and soft fabric folds,
a hand-painted rose motif on the skirt, tiny hand-sewn beadwork,
a single strand of warm ivory pearls at the neckline, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, centered composition, no text, no watermark, no floating objects,
no extra limbs, no skin blemishes,
extreme macro close-up filling the frame with the face and tiara,
razor-sharp focus on the porcelain cheek,
individual eyelashes and glaze micro-texture clearly visible, soft grey backdrop
```

### bouquet　seed=610

产物：`out/r6/bc-r6-bouquet_00001_.png`

```text
Photorealistic macro photograph of a handcrafted fine bone china figurine of a princess,
museum collector piece, ultra-detailed.
Uniform glossy fired glaze over cream-white porcelain with visible micro glaze texture and fine
craquelure lines,
crisp specular highlights,
delicate warm translucency where the porcelain is thinnest at the rim of the ears and fingertips.
The face is an elegant young woman in her early twenties: refined oval face, high cheekbones,
defined jawline, straight nose bridge, serene closed lips with a faint smile,
individually rendered eyelashes, proportionally sized almond eyes with a subtle eyelid crease,
glossy glass eyes with warm hazel irises, deep pupils and sharp catchlights.
Slender tapered neck, poised posture, not a child, not cartoonish, not a toy.
Hand-painted eyebrows drawn hair by hair, very subtle soft blush.
White lace gown with clearly visible thread structure and soft fabric folds,
a hand-painted rose motif on the skirt, tiny hand-sewn beadwork,
a single strand of warm ivory pearls at the neckline, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, centered composition, no text, no watermark, no floating objects,
no extra limbs, no skin blemishes,
three-quarter view holding a small bouquet of white porcelain flowers, warm neutral backdrop,
soft shadow under the jaw
```

### fan　seed=620

产物：`out/r6/bc-r6-fan_00001_.png`

```text
Photorealistic macro photograph of a handcrafted fine bone china figurine of a princess,
museum collector piece, ultra-detailed.
Uniform glossy fired glaze over cream-white porcelain with visible micro glaze texture and fine
craquelure lines,
crisp specular highlights,
delicate warm translucency where the porcelain is thinnest at the rim of the ears and fingertips.
The face is an elegant young woman in her early twenties: refined oval face, high cheekbones,
defined jawline, straight nose bridge, serene closed lips with a faint smile,
individually rendered eyelashes, proportionally sized almond eyes with a subtle eyelid crease,
glossy glass eyes with warm hazel irises, deep pupils and sharp catchlights.
Slender tapered neck, poised posture, not a child, not cartoonish, not a toy.
Hand-painted eyebrows drawn hair by hair, very subtle soft blush.
White lace gown with clearly visible thread structure and soft fabric folds,
a hand-painted rose motif on the skirt, tiny hand-sewn beadwork,
a single strand of warm ivory pearls at the neckline, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, centered composition, no text, no watermark, no floating objects,
no extra limbs, no skin blemishes, three-quarter view with an open white lace fan beside her face,
soft even light, muted teal backdrop
```

### seated-hands　seed=630

产物：`out/r6/bc-r6-seated-hands_00001_.png`

```text
Photorealistic macro photograph of a handcrafted fine bone china figurine of a princess,
museum collector piece, ultra-detailed.
Uniform glossy fired glaze over cream-white porcelain with visible micro glaze texture and fine
craquelure lines,
crisp specular highlights,
delicate warm translucency where the porcelain is thinnest at the rim of the ears and fingertips.
The face is an elegant young woman in her early twenties: refined oval face, high cheekbones,
defined jawline, straight nose bridge, serene closed lips with a faint smile,
individually rendered eyelashes, proportionally sized almond eyes with a subtle eyelid crease,
glossy glass eyes with warm hazel irises, deep pupils and sharp catchlights.
Slender tapered neck, poised posture, not a child, not cartoonish, not a toy.
Hand-painted eyebrows drawn hair by hair, very subtle soft blush.
White lace gown with clearly visible thread structure and soft fabric folds,
a hand-painted rose motif on the skirt, tiny hand-sewn beadwork,
a single strand of warm ivory pearls at the neckline, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, centered composition, no text, no watermark, no floating objects,
no extra limbs, no skin blemishes, seated waist-up with both hands folded on her lap,
ball-joint seams at the wrists clearly visible, soft even light, blue-grey backdrop
```

### full-figure　seed=640

产物：`out/r6/bc-r6-full-figure_00001_.png`

```text
Photorealistic macro photograph of a handcrafted fine bone china figurine of a princess,
museum collector piece, ultra-detailed.
Uniform glossy fired glaze over cream-white porcelain with visible micro glaze texture and fine
craquelure lines,
crisp specular highlights,
delicate warm translucency where the porcelain is thinnest at the rim of the ears and fingertips.
The face is an elegant young woman in her early twenties: refined oval face, high cheekbones,
defined jawline, straight nose bridge, serene closed lips with a faint smile,
individually rendered eyelashes, proportionally sized almond eyes with a subtle eyelid crease,
glossy glass eyes with warm hazel irises, deep pupils and sharp catchlights.
Slender tapered neck, poised posture, not a child, not cartoonish, not a toy.
Hand-painted eyebrows drawn hair by hair, very subtle soft blush.
White lace gown with clearly visible thread structure and soft fabric folds,
a hand-painted rose motif on the skirt, tiny hand-sewn beadwork,
a single strand of warm ivory pearls at the neckline, pale blue silk sash,
silver filigree tiara set with sapphire and small diamonds, pearl drop earrings.
Soft directional light from the upper left with a gentle rim light, even exposure,
clean seamless studio backdrop free of any equipment, medium format camera, 120mm macro lens,
shallow depth of field, centered composition, no text, no watermark, no floating objects,
no extra limbs, no skin blemishes, full figure standing on a velvet cushion,
complete gown with lace fabric folds and a short train, low-key museum light, dark hall backdrop
```

## R7 · engine switch to Qwen-Image 2512; pristine glaze, no cracks, 3 shots

- 引擎：`qwen`　尺寸：1024×1360　steps：24　cfg：3.0
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### macro-upper　seed=700

产物：`out/r7/bc-r7-macro-upper_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop, tight three-quarter upper-body framing filling most of the frame,
the tiara and the lace bodice in sharp focus
```

### bouquet　seed=710

产物：`out/r7/bc-r7-bouquet_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop, three-quarter view holding a small bouquet of white porcelain roses,
warm neutral backdrop, soft shadow under the jaw
```

### seated-hands　seed=720

产物：`out/r7/bc-r7-seated-hands_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop, seated, both hands folded on her lap,
the ball-joint seams and painted fingernails clearly visible, soft even light, blue-grey backdrop
```

## R8 · higher resolution + more steps + chiaroscuro light + brocade/gold-thread costume

- 引擎：`qwen`　尺寸：1152×1536　steps：28　cfg：3.2
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### rembrandt-portrait　seed=800

产物：`out/r8/bc-r8-rembrandt-portrait_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture, three-quarter beauty portrait with Rembrandt lighting,
the tiara and the pearl earring catching the key light, simple dark backdrop
```

### hands-embroidery　seed=810

产物：`out/r8/bc-r8-hands-embroidery_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture, close-up of the doll's hands folded over the embroidered bodice,
macro detail of the ball-joint seams, the gold thread and the pearl beading, soft light
```

### full-figure　seed=820

产物：`out/r8/bc-r8-full-figure_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture, full figure standing on a stone plinth, complete gown with train,
dramatic side light from the left, deep shadows, dark exhibition hall backdrop
```

## R9 · microscopic glaze texture, anti-CGI, focus-stacked macro framing

- 引擎：`qwen`　尺寸：1152×1536　steps：30　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### face-macro　seed=900

产物：`out/r9/bc-r9-face-macro_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain, the porcelain face and the tiara fill the frame,
cropped just below the collarbone,
the glaze micro-texture and the painted eyelashes visible at pixel level,
soft key light from the left
```

### fan-portrait　seed=910

产物：`out/r9/bc-r9-fan-portrait_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain, three-quarter portrait with an open lace fan held near the shoulder,
warm side light, the embroidered sleeve in sharp focus
```

### bust-rimlight　seed=920

产物：`out/r9/bc-r9-bust-rimlight_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain,
bust portrait with a strong rim light behind her so the thin porcelain of the ears and neck glows,
near-black backdrop, delicate shadow detail
```

## R10 · jewellery/weave macro + window light; resolution and steps up again

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### tiara-macro　seed=1000

产物：`out/r10/bc-r10-tiara-macro_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality, extreme close-up of the tiara and the hair,
milled silver filigree and faceted sapphires filling the upper half of the frame,
razor-sharp metal edges
```

### embroidery-macro　seed=1010

产物：`out/r10/bc-r10-embroidery-macro_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality,
extreme close-up of the embroidered bodice and the doll's hands, gold thread,
seed pearls and the wrist joint seam in sharp macro focus, shallow depth of field
```

### window-light　seed=1020

产物：`out/r10/bc-r10-window-light_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality,
three-quarter portrait in soft north window light with a pale rose brocade gown,
gentle shadow gradient across the porcelain cheek, quiet interior backdrop
```

## R11 · final round: framing-first prompts, minimal costume text, three deliberately different shots

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### tiara-macro　seed=1100

产物：`out/r11/bc-r11-tiara-macro_00001_.png`

```text
Extreme macro photograph:
ONLY the silver filigree tiara and the top of the brown hair fill the entire frame,
cropped tight on the crown, nothing else visible.
Photorealistic studio photograph of a handcrafted ball-jointed bone china doll of a princess.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Ball-joint seams at the neck and wrists.
Fine art studio lighting, sharp focus, medium format camera, subtle natural sensor grain,
no digital sharpening.
Every milled silver edge, every prong and every facet of the sapphires is razor sharp,
the metal shows tiny polishing marks, the stones show internal refraction.
Dark neutral background, shallow depth of field
```

### hand-macro　seed=1110

产物：`out/r11/bc-r11-hand-macro_00001_.png`

```text
Extreme macro photograph: ONLY the doll's porcelain hands and the lace cuff fill the frame,
cropped tight on the hands, no face visible.
Photorealistic studio photograph of a handcrafted ball-jointed bone china doll of a princess.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Ball-joint seams at the neck and wrists.
Fine art studio lighting, sharp focus, medium format camera, subtle natural sensor grain,
no digital sharpening.
The ball-joint seam at the wrist, the painted fingernails,
the individual lace threads and a few seed pearls are razor sharp, shallow depth of field
```

### portrait-velvet　seed=1120

产物：`out/r11/bc-r11-portrait-velvet_00001_.png`

```text
Elegant half-body studio portrait, head and shoulders centred in frame.
Photorealistic studio photograph of a handcrafted ball-jointed bone china doll of a princess.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Ball-joint seams at the neck and wrists.
Fine art studio lighting, sharp focus, medium format camera, subtle natural sensor grain,
no digital sharpening She wears a deep royal-blue velvet gown with silver embroidery and a
diamond-set tiara,
pearl drop earrings, a single strand of pearls.
Soft directional key light from the upper left, gentle rim light on the porcelain cheek,
clean dark grey backdrop, tack-sharp focus
```

## R12 · de-CGI round: drop pristine/flawless, describe the physical glaze, one crisp key light; keep the eyes in every crop; simplify the hand to ONE hand

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, nail polish,
coloured fingernails, painted nail art, rainbow iridescence, chromatic aberration,
duplicated fingers, six fingers, fused fingers, extra knuckles, blank eyes, eyeless,
closed eyelids, empty eye sockets, mannequin, wax figure, airbrushed, matte chalky clay
```

### eyes-tiara　seed=1200

产物：`out/r12/bc-r12-eyes-tiara_00001_.png`

```text
Close-up beauty photograph framed from the top of the tiara down to the collarbone,
the face centred, the eyes on the upper third line, open and looking just past the lens.
Photorealistic studio photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real object on a table.
Ivory porcelain covered in a fired glaze that behaves like real glass:
bright crisp specular highlights where the light strikes,
faint undulation in the glaze where it pooled and ran,
microscopic air bubbles and the finest polishing marks caught just under the surface,
warm translucency glowing through the thin porcelain of the ears and the fingertips,
small handmade irregularities, but no cracks and no damage.
Visible ball-joint seams at the neck and the wrists.
Refined adult doll face: oval face, high cheekbones, straight nose bridge,
serene softly closed lips with glaze pooling on the lower lip.
Open glass doll eyes of realistic size, dark brown iris with a ring of fine radial fibres,
clearly defined pupil, one sharp rectangular window catchlight in each eye, sculpted eyelids,
individually painted eyelashes, eyebrows painted hair by hair.
One crisp key light from the upper left so that every highlight is small and sharp,
deep clean falloff, subtle warm bounce on the shadow side, sharp focus, medium format camera,
120mm macro lens, natural sensor grain,
no digital sharpening She wears a silver filigree tiara set with faceted diamond-like stones and
pearl drop earrings;
bare porcelain neck and shoulders.
Dark charcoal backdrop, tack-sharp focus on the eyes, shallow depth of field
```

### hand-single　seed=1210

产物：`out/r12/bc-r12-hand-single_00001_.png`

```text
Extreme macro photograph cropped tight on ONE porcelain hand.
Exactly one hand is in the frame: a left hand resting palm down and relaxed on white lace,
exactly five slender fingers slightly apart,
each finger a single straight segment ending in one clean glossy ivory fingernail,
the ball joint seam clearly visible at the wrist,
a lace cuff with seed pearls at the edge of the frame.
Photorealistic studio photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real object on a table.
Ivory porcelain covered in a fired glaze that behaves like real glass:
bright crisp specular highlights where the light strikes,
faint undulation in the glaze where it pooled and ran,
microscopic air bubbles and the finest polishing marks caught just under the surface,
warm translucency glowing through the thin porcelain of the ears and the fingertips,
small handmade irregularities, but no cracks and no damage.
Visible ball-joint seams at the neck and the wrists.
Refined adult doll face: oval face, high cheekbones, straight nose bridge,
serene softly closed lips with glaze pooling on the lower lip.
Open glass doll eyes of realistic size, dark brown iris with a ring of fine radial fibres,
clearly defined pupil, one sharp rectangular window catchlight in each eye, sculpted eyelids,
individually painted eyelashes, eyebrows painted hair by hair.
One crisp key light from the upper left so that every highlight is small and sharp,
deep clean falloff, subtle warm bounce on the shadow side, sharp focus, medium format camera,
120mm macro lens, natural sensor grain, no digital sharpening.
Razor-sharp focus on the knuckles, shallow depth of field, dark background
```

### portrait-specular　seed=1220

产物：`out/r12/bc-r12-portrait-specular_00001_.png`

```text
Elegant half-body studio portrait, head and shoulders centred in frame,
the doll turned a quarter away from the light so one cheek catches it.
Photorealistic studio photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real object on a table.
Ivory porcelain covered in a fired glaze that behaves like real glass:
bright crisp specular highlights where the light strikes,
faint undulation in the glaze where it pooled and ran,
microscopic air bubbles and the finest polishing marks caught just under the surface,
warm translucency glowing through the thin porcelain of the ears and the fingertips,
small handmade irregularities, but no cracks and no damage.
Visible ball-joint seams at the neck and the wrists.
Refined adult doll face: oval face, high cheekbones, straight nose bridge,
serene softly closed lips with glaze pooling on the lower lip.
Open glass doll eyes of realistic size, dark brown iris with a ring of fine radial fibres,
clearly defined pupil, one sharp rectangular window catchlight in each eye, sculpted eyelids,
individually painted eyelashes, eyebrows painted hair by hair.
One crisp key light from the upper left so that every highlight is small and sharp,
deep clean falloff, subtle warm bounce on the shadow side, sharp focus, medium format camera,
120mm macro lens, natural sensor grain,
no digital sharpening She wears a deep royal-blue velvet gown with silver-thread embroidery and a
diamond-set tiara,
pearl drop earrings, a single strand of pearls.
The crisp key light leaves a small bright highlight on the cheekbone,
the nose tip and the lower lip, and a warm translucent glow along the rim of the ear.
Clean dark grey backdrop, tack-sharp focus on the eyes
```

## R13 · back to the BASE_Q10 baseline; framing-first without deleting material vocabulary; R10 control shot at a new seed + two true macros

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### window-light-control　seed=1300

产物：`out/r13/bc-r13-window-light-control_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality,
three-quarter portrait in soft north window light with a pale rose brocade gown,
gentle shadow gradient across the porcelain cheek, quiet interior backdrop
```

### tiara-macro　seed=1310

产物：`out/r13/bc-r13-tiara-macro_00001_.png`

```text
Close-up photograph cropped tight on the silver filigree tiara and the top of her head:
the jewelled crown fills the frame edge to edge and is cut off just above the eyebrows,
no face and no eyes are visible.
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality Every milled silver edge,
every prong and every facet of the sapphires is razor sharp, the metal shows tiny polishing marks,
the stones show internal refraction.
Dark neutral background, shallow depth of field
```

### hand-macro　seed=1320

产物：`out/r13/bc-r13-hand-macro_00001_.png`

```text
Extreme macro photograph cropped tight on ONE porcelain hand.
Exactly one hand is in the frame: a left hand resting palm down and relaxed on white lace,
exactly five slender fingers slightly apart,
each finger a single straight segment ending in one clean glossy ivory fingernail,
the ball joint seam clearly visible at the wrist,
a lace cuff with seed pearls at the edge of the frame.
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality.
Razor-sharp focus on the knuckles, shallow depth of field, dark background
```

## R14 · resolution ablation at fixed prompt and fixed seed 1400: 1.25x / 1.40x / 1.50x

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### res-125　seed=1400　（本轮覆盖：1600×2144）

产物：`out/r14/bc-r14-res-125_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality,
three-quarter portrait in soft north window light with a pale rose brocade gown,
gentle shadow gradient across the porcelain cheek, quiet interior backdrop
```

### res-140　seed=1400　（本轮覆盖：1792×2400）

产物：`out/r14/bc-r14-res-140_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality,
three-quarter portrait in soft north window light with a pale rose brocade gown,
gentle shadow gradient across the porcelain cheek, quiet interior backdrop
```

### res-150　seed=1400　（本轮覆盖：1920×2560）

产物：`out/r14/bc-r14-res-150_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality,
three-quarter portrait in soft north window light with a pale rose brocade gown,
gentle shadow gradient across the porcelain cheek, quiet interior backdrop
```

## R15 · composition variety via canvas aspect ratio: ultra-tall full figure, square seated, and the first back view of the project

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### full-figure　seed=1500　（本轮覆盖：1024×2048）

产物：`out/r15/bc-r15-full-figure_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality, full-length standing figure:
the entire doll from the top of the tiara down to the hem of the gown and her porcelain slippers is
inside the frame,
standing on a low velvet cushion, the whole gown and its short train clearly visible,
low-key museum lighting with a distant soft spotlight, dark hall backdrop, slight low camera angle
```

### back-view　seed=1510　（本轮覆盖：1280×1712）

产物：`out/r15/bc-r15-back-view_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality,
seen from behind and a little to her left in a three-quarter back view:
the coiled hair and the back of the silver filigree tiara are in sharp focus,
the back of the gown shows the laced bodice, the pearl buttons and the long train,
soft north window light, quiet interior backdrop
```

### seated-square　seed=1520　（本轮覆盖：1600×1600）

产物：`out/r15/bc-r15-seated-square_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality, seated three-quarter view at a small side table,
both porcelain hands resting on her lap with the ball-joint seams at the wrists clearly visible,
a white lace fan lying on the table, soft north window light, pale grey backdrop
```

## R16 · closing round: BASE_Q10 + aspect-driven composition x steps 40; final deliverable set

- 引擎：`qwen`　尺寸：1280×1712　steps：40　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### final-portrait　seed=1600　（本轮覆盖：1280×1712 · steps 40）

产物：`out/r16/bc-r16-final-portrait_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality,
three-quarter portrait in soft north window light with a pale rose brocade gown,
gentle shadow gradient across the porcelain cheek, quiet interior backdrop
```

### final-full-figure　seed=1610　（本轮覆盖：1024×2048 · steps 40）

产物：`out/r16/bc-r16-final-full-figure_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality, full-length standing figure:
the entire doll from the top of the tiara down to the hem of the gown and her porcelain slippers is
inside the frame,
standing on a low velvet cushion, the whole gown and its short train clearly visible,
low-key museum lighting with a distant soft spotlight, dark hall backdrop, slight low camera angle
```

### final-seated　seed=1620　（本轮覆盖：1600×1600 · steps 40）

产物：`out/r16/bc-r16-final-seated_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of a princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair, the faintest soft blush.
A gown of real white lace with individual visible threads, dense hand embroidery,
seed pearls stitched one by one, a pale blue silk sash,
a silver filigree tiara set with sapphires and small diamonds, pearl drop earrings.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant costume craft: ivory silk brocade with raised gold-thread embroidery,
dense lace with individual visible threads, seed pearls stitched one by one,
faceted gemstones set in metal prongs, a pale blue velvet sash,
a heavy ceremonial tiara with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
the matte unglazed foot rim showing a hint of crazing, absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved silver filigree with crisp milled edges,
faceted sapphires and diamonds showing internal refraction and tiny inclusions,
seed pearls with subtle orient and nacre rings, metal prongs and hinges clearly readable.
Fabric realism: silk brocade with raised weft, linen-backed lace, visible individual stitches,
slightly irregular handmade quality, seated three-quarter view at a small side table,
both porcelain hands resting on her lap with the ball-joint seams at the wrists clearly visible,
a white lace fan lying on the table, soft north window light, pale grey backdrop
```

## R17 · phase 3 opens: theme switched to Eastern classical (骨瓷国公主); BASE_Q10 material core kept verbatim, only face/hair/costume/jewellery replaced

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### portrait　seed=1700　（本轮覆盖：1280×1712）

产物：`out/r17/bc-r17-portrait_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners and a subtle crease,
dark brown irises, individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun with a few loose strands at the temples,
held by a gold filigree hairpin set with jade and a dangling pearl ornament.
She wears a classical Eastern gown of ivory silk with a crossed collar,
wide flowing sleeves and a broad sash, woven with gold-thread cloud and peony patterns,
its edges densely embroidered and trimmed with hundreds of tiny seed pearls stitched one by one,
a jade-inlaid gold filigree belt, an embroidered cloud collar over the shoulders,
and carved jade earrings with gold filigree.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant craft: ivory silk brocade with raised gold-thread embroidery,
dense silk embroidery with individual visible threads, seed pearls stitched one by one,
carved jade with a soft waxy lustre and internal veining, gold filigree with milled edges,
a heavy ceremonial headdress with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved gold filigree with crisp milled edges,
carved jade showing internal veining, seed pearls with subtle orient and nacre rings,
metal prongs and hinges clearly readable.
Fabric realism: silk with a visible woven weft, embroidered satin, linen-backed inner layers,
visible individual stitches, slightly irregular handmade quality,
three-quarter portrait in soft north window light,
gentle shadow gradient across the porcelain cheek, quiet neutral interior backdrop
```

### full-figure　seed=1710　（本轮覆盖：1024×2048）

产物：`out/r17/bc-r17-full-figure_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners and a subtle crease,
dark brown irises, individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun with a few loose strands at the temples,
held by a gold filigree hairpin set with jade and a dangling pearl ornament.
She wears a classical Eastern gown of ivory silk with a crossed collar,
wide flowing sleeves and a broad sash, woven with gold-thread cloud and peony patterns,
its edges densely embroidered and trimmed with hundreds of tiny seed pearls stitched one by one,
a jade-inlaid gold filigree belt, an embroidered cloud collar over the shoulders,
and carved jade earrings with gold filigree.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant craft: ivory silk brocade with raised gold-thread embroidery,
dense silk embroidery with individual visible threads, seed pearls stitched one by one,
carved jade with a soft waxy lustre and internal veining, gold filigree with milled edges,
a heavy ceremonial headdress with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved gold filigree with crisp milled edges,
carved jade showing internal veining, seed pearls with subtle orient and nacre rings,
metal prongs and hinges clearly readable.
Fabric realism: silk with a visible woven weft, embroidered satin, linen-backed inner layers,
visible individual stitches, slightly irregular handmade quality, full-length standing figure:
the entire doll from the top of the hair bun down to the hem of the gown and her porcelain slippers
is inside the frame,
standing on a low carved wooden stand, the whole gown and its train clearly visible,
low-key museum lighting with a distant soft spotlight, dark hall backdrop, slight low camera angle
```

### seated　seed=1720　（本轮覆盖：1600×1600）

产物：`out/r17/bc-r17-seated_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners and a subtle crease,
dark brown irises, individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun with a few loose strands at the temples,
held by a gold filigree hairpin set with jade and a dangling pearl ornament.
She wears a classical Eastern gown of ivory silk with a crossed collar,
wide flowing sleeves and a broad sash, woven with gold-thread cloud and peony patterns,
its edges densely embroidered and trimmed with hundreds of tiny seed pearls stitched one by one,
a jade-inlaid gold filigree belt, an embroidered cloud collar over the shoulders,
and carved jade earrings with gold filigree.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant craft: ivory silk brocade with raised gold-thread embroidery,
dense silk embroidery with individual visible threads, seed pearls stitched one by one,
carved jade with a soft waxy lustre and internal veining, gold filigree with milled edges,
a heavy ceremonial headdress with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved gold filigree with crisp milled edges,
carved jade showing internal veining, seed pearls with subtle orient and nacre rings,
metal prongs and hinges clearly readable.
Fabric realism: silk with a visible woven weft, embroidered satin, linen-backed inner layers,
visible individual stitches, slightly irregular handmade quality,
seated three-quarter view at a small rosewood table,
both porcelain hands resting on her lap with the ball-joint seams at the wrists clearly visible,
a round silk fan lying on the table, a carved wooden folding screen softly out of focus behind her,
soft north window light
```

## R18 · fix the full-figure shot by cutting the costume inventory and pushing the canvas taller; add 花钿 forehead ornament and 璎珞 jade-pearl necklace

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### portrait　seed=1800　（本轮覆盖：1280×1712）

产物：`out/r18/bc-r18-portrait_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners and a subtle crease,
dark brown irises, individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun with a few loose strands at the temples,
held by a gold filigree hairpin set with jade and a dangling pearl ornament.
She wears a classical Eastern gown of ivory silk with a crossed collar,
wide flowing sleeves and a broad sash, woven with gold-thread cloud and peony patterns,
its edges densely embroidered and trimmed with hundreds of tiny seed pearls stitched one by one,
a jade-inlaid gold filigree belt, an embroidered cloud collar over the shoulders,
and carved jade earrings with gold filigree.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant craft: ivory silk brocade with raised gold-thread embroidery,
dense silk embroidery with individual visible threads, seed pearls stitched one by one,
carved jade with a soft waxy lustre and internal veining, gold filigree with milled edges,
a heavy ceremonial headdress with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved gold filigree with crisp milled edges,
carved jade showing internal veining, seed pearls with subtle orient and nacre rings,
metal prongs and hinges clearly readable.
Fabric realism: silk with a visible woven weft, embroidered satin, linen-backed inner layers,
visible individual stitches, slightly irregular handmade quality,
a delicate forehead ornament of tiny gold and jade flowers set between the eyebrows,
a beaded necklace of carved jade beads and pearls resting on the collarbone,
the cloud collar worked in ivory silk and gold thread to match the gown,
three-quarter portrait in soft north window light,
gentle shadow gradient across the porcelain cheek, quiet neutral interior backdrop
```

### full-figure　seed=1810　（本轮覆盖：880×2048）

产物：`out/r18/bc-r18-full-figure_00001_.png`

```text
Full-length photograph:
the entire doll from the top of the hair bun down to the hem of the gown and her porcelain slippers
is inside the frame,
standing upright on a low carved wooden stand, the whole robe and its train visible,
low-key museum lighting with a distant soft spotlight, dark hall backdrop, slight low camera angle.
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners, dark brown irises,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun held by a gold filigree hairpin set with
jade and a dangling pearl ornament.
Fine art studio lighting from the upper left, deep but clean shadows, sharp focus,
medium format camera, 120mm macro lens, natural sensor grain, no digital sharpening.
Ivory silk with a visible woven weft, raised gold-thread embroidery,
carved jade with a soft waxy lustre, engraved gold filigree with milled edges, seed pearls,
extremely fine porcelain surface, absolutely no CGI smoothness
```

### seated　seed=1820　（本轮覆盖：1600×1600）

产物：`out/r18/bc-r18-seated_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners and a subtle crease,
dark brown irises, individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun with a few loose strands at the temples,
held by a gold filigree hairpin set with jade and a dangling pearl ornament.
She wears a classical Eastern gown of ivory silk with a crossed collar,
wide flowing sleeves and a broad sash, woven with gold-thread cloud and peony patterns,
its edges densely embroidered and trimmed with hundreds of tiny seed pearls stitched one by one,
a jade-inlaid gold filigree belt, an embroidered cloud collar over the shoulders,
and carved jade earrings with gold filigree.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant craft: ivory silk brocade with raised gold-thread embroidery,
dense silk embroidery with individual visible threads, seed pearls stitched one by one,
carved jade with a soft waxy lustre and internal veining, gold filigree with milled edges,
a heavy ceremonial headdress with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved gold filigree with crisp milled edges,
carved jade showing internal veining, seed pearls with subtle orient and nacre rings,
metal prongs and hinges clearly readable.
Fabric realism: silk with a visible woven weft, embroidered satin, linen-backed inner layers,
visible individual stitches, slightly irregular handmade quality,
a delicate forehead ornament of tiny gold and jade flowers set between the eyebrows,
a beaded necklace of carved jade beads and pearls resting on the collarbone,
the cloud collar worked in ivory silk and gold thread to match the gown,
seated three-quarter view at a small rosewood table,
both porcelain hands resting on her lap with the ball-joint seams at the wrists clearly visible,
a round silk fan lying on the table, a carved wooden folding screen softly out of focus behind her,
soft north window light
```

## R19 · Tang-dynasty variant: high-waisted ruqun + sheer gauze pibo stole + 花钿 forehead ornament; only the garment-shape sentence changes

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### portrait　seed=1900　（本轮覆盖：1280×1712）

产物：`out/r19/bc-r19-portrait_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners and a subtle crease,
dark brown irises, individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun with a few loose strands at the temples,
held by a gold filigree hairpin set with jade and a dangling pearl ornament.
She wears a Tang-dynasty style gown:
a high-waisted ivory silk skirt tied under the arms with a gold-thread sash,
a short crossed-collar silk jacket,
and a long sheer gauze scarf draped over the shoulders and falling in a wide loop;
the silk is woven with gold-thread peony and cloud patterns and its edges are trimmed with hundreds
of tiny seed pearls stitched one by one.
A jade-inlaid gold filigree belt, an embroidered cloud collar,
and carved jade earrings with gold filigree.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant craft: ivory silk brocade with raised gold-thread embroidery,
dense silk embroidery with individual visible threads, seed pearls stitched one by one,
carved jade with a soft waxy lustre and internal veining, gold filigree with milled edges,
a heavy ceremonial headdress with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved gold filigree with crisp milled edges,
carved jade showing internal veining, seed pearls with subtle orient and nacre rings,
metal prongs and hinges clearly readable.
Fabric realism: silk with a visible woven weft, embroidered satin, linen-backed inner layers,
visible individual stitches, slightly irregular handmade quality,
a delicate forehead ornament of tiny gold and jade flowers set between the eyebrows,
a beaded necklace of carved jade beads and pearls resting on the collarbone,
the cloud collar worked in ivory silk and gold thread to match the gown,
a gilded flower ornament painted on the centre of the forehead between the eyebrows,
three-quarter portrait in soft north window light,
gentle shadow gradient across the porcelain cheek, quiet neutral interior backdrop
```

### full-figure　seed=1910　（本轮覆盖：880×2048）

产物：`out/r19/bc-r19-full-figure_00001_.png`

```text
Full-length photograph:
the entire doll from the top of the hair bun down to the hem of the skirt and her porcelain
slippers is inside the frame,
standing upright on a low carved wooden stand, the high-waisted skirt,
the trailing gauze scarf and the hem are all visible,
low-key museum lighting with a distant soft spotlight, dark hall backdrop, slight low camera angle.
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners, dark brown irises,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun held by a gold filigree hairpin set with
jade and a dangling pearl ornament.
Fine art studio lighting from the upper left, deep but clean shadows, sharp focus,
medium format camera, 120mm macro lens, natural sensor grain, no digital sharpening.
Ivory silk with a visible woven weft, sheer gauze with a fine open weave,
raised gold-thread embroidery, carved jade with a soft waxy lustre,
engraved gold filigree with milled edges, seed pearls, extremely fine porcelain surface,
absolutely no CGI smoothness
```

### seated　seed=1920　（本轮覆盖：1600×1600）

产物：`out/r19/bc-r19-seated_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners and a subtle crease,
dark brown irises, individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun with a few loose strands at the temples,
held by a gold filigree hairpin set with jade and a dangling pearl ornament.
She wears a Tang-dynasty style gown:
a high-waisted ivory silk skirt tied under the arms with a gold-thread sash,
a short crossed-collar silk jacket,
and a long sheer gauze scarf draped over the shoulders and falling in a wide loop;
the silk is woven with gold-thread peony and cloud patterns and its edges are trimmed with hundreds
of tiny seed pearls stitched one by one.
A jade-inlaid gold filigree belt, an embroidered cloud collar,
and carved jade earrings with gold filigree.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant craft: ivory silk brocade with raised gold-thread embroidery,
dense silk embroidery with individual visible threads, seed pearls stitched one by one,
carved jade with a soft waxy lustre and internal veining, gold filigree with milled edges,
a heavy ceremonial headdress with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved gold filigree with crisp milled edges,
carved jade showing internal veining, seed pearls with subtle orient and nacre rings,
metal prongs and hinges clearly readable.
Fabric realism: silk with a visible woven weft, embroidered satin, linen-backed inner layers,
visible individual stitches, slightly irregular handmade quality,
a delicate forehead ornament of tiny gold and jade flowers set between the eyebrows,
a beaded necklace of carved jade beads and pearls resting on the collarbone,
the cloud collar worked in ivory silk and gold thread to match the gown,
a gilded flower ornament painted on the centre of the forehead between the eyebrows,
seated three-quarter view at a small rosewood table,
both porcelain hands resting on her lap with the ball-joint seams at the wrists clearly visible,
a round silk fan lying on the table, a carved wooden folding screen softly out of focus behind her,
soft north window light
```

## R20 · high-resolution plates for the Eastern macro set (crop source); no new prompt wording

- 引擎：`qwen`　尺寸：1600×1600　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### plate-portrait　seed=2000　（本轮覆盖：1600×2144）

产物：`out/r20/bc-r20-plate-portrait_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners and a subtle crease,
dark brown irises, individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun with a few loose strands at the temples,
held by a gold filigree hairpin set with jade and a dangling pearl ornament.
She wears a classical Eastern gown of ivory silk with a crossed collar,
wide flowing sleeves and a broad sash, woven with gold-thread cloud and peony patterns,
its edges densely embroidered and trimmed with hundreds of tiny seed pearls stitched one by one,
a jade-inlaid gold filigree belt, an embroidered cloud collar over the shoulders,
and carved jade earrings with gold filigree.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant craft: ivory silk brocade with raised gold-thread embroidery,
dense silk embroidery with individual visible threads, seed pearls stitched one by one,
carved jade with a soft waxy lustre and internal veining, gold filigree with milled edges,
a heavy ceremonial headdress with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved gold filigree with crisp milled edges,
carved jade showing internal veining, seed pearls with subtle orient and nacre rings,
metal prongs and hinges clearly readable.
Fabric realism: silk with a visible woven weft, embroidered satin, linen-backed inner layers,
visible individual stitches, slightly irregular handmade quality,
a delicate forehead ornament of tiny gold and jade flowers set between the eyebrows,
a beaded necklace of carved jade beads and pearls resting on the collarbone,
the cloud collar worked in ivory silk and gold thread to match the gown,
three-quarter portrait in soft north window light,
gentle shadow gradient across the porcelain cheek, quiet neutral interior backdrop
```

### plate-seated　seed=2010　（本轮覆盖：1600×1600）

产物：`out/r20/bc-r20-plate-seated_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners and a subtle crease,
dark brown irises, individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun with a few loose strands at the temples,
held by a gold filigree hairpin set with jade and a dangling pearl ornament.
She wears a classical Eastern gown of ivory silk with a crossed collar,
wide flowing sleeves and a broad sash, woven with gold-thread cloud and peony patterns,
its edges densely embroidered and trimmed with hundreds of tiny seed pearls stitched one by one,
a jade-inlaid gold filigree belt, an embroidered cloud collar over the shoulders,
and carved jade earrings with gold filigree.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant craft: ivory silk brocade with raised gold-thread embroidery,
dense silk embroidery with individual visible threads, seed pearls stitched one by one,
carved jade with a soft waxy lustre and internal veining, gold filigree with milled edges,
a heavy ceremonial headdress with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved gold filigree with crisp milled edges,
carved jade showing internal veining, seed pearls with subtle orient and nacre rings,
metal prongs and hinges clearly readable.
Fabric realism: silk with a visible woven weft, embroidered satin, linen-backed inner layers,
visible individual stitches, slightly irregular handmade quality,
a delicate forehead ornament of tiny gold and jade flowers set between the eyebrows,
a beaded necklace of carved jade beads and pearls resting on the collarbone,
the cloud collar worked in ivory silk and gold thread to match the gown,
seated three-quarter view at a small rosewood table,
both porcelain hands resting on her lap with the ball-joint seams at the wrists clearly visible,
a round silk fan lying on the table, a carved wooden folding screen softly out of focus behind her,
soft north window light
```

### plate-figure　seed=2020　（本轮覆盖：1200×2560）

产物：`out/r20/bc-r20-plate-figure_00001_.png`

```text
Full-length photograph:
the entire doll from the top of the hair bun down to the hem of the skirt and her porcelain
slippers is inside the frame,
standing upright on a low carved wooden stand, the high-waisted skirt,
the trailing gauze scarf and the hem are all visible,
low-key museum lighting with a distant soft spotlight, dark hall backdrop, slight low camera angle.
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners, dark brown irises,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun held by a gold filigree hairpin set with
jade and a dangling pearl ornament.
Fine art studio lighting from the upper left, deep but clean shadows, sharp focus,
medium format camera, 120mm macro lens, natural sensor grain, no digital sharpening.
Ivory silk with a visible woven weft, sheer gauze with a fine open weave,
raised gold-thread embroidery, carved jade with a soft waxy lustre,
engraved gold filigree with milled edges, seed pearls, extremely fine porcelain surface,
absolutely no CGI smoothness
```

## R21 · closing round: medium-density costume base for the wide shot + the two proven compositions; Eastern deliverable set

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background
```

### final-portrait　seed=2100　（本轮覆盖：1280×1712）

产物：`out/r21/bc-r21-final-portrait_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners and a subtle crease,
dark brown irises, individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun with a few loose strands at the temples,
held by a gold filigree hairpin set with jade and a dangling pearl ornament.
She wears a classical Eastern gown of ivory silk with a crossed collar,
wide flowing sleeves and a broad sash, woven with gold-thread cloud and peony patterns,
its edges densely embroidered and trimmed with hundreds of tiny seed pearls stitched one by one,
a jade-inlaid gold filigree belt, an embroidered cloud collar over the shoulders,
and carved jade earrings with gold filigree.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant craft: ivory silk brocade with raised gold-thread embroidery,
dense silk embroidery with individual visible threads, seed pearls stitched one by one,
carved jade with a soft waxy lustre and internal veining, gold filigree with milled edges,
a heavy ceremonial headdress with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved gold filigree with crisp milled edges,
carved jade showing internal veining, seed pearls with subtle orient and nacre rings,
metal prongs and hinges clearly readable.
Fabric realism: silk with a visible woven weft, embroidered satin, linen-backed inner layers,
visible individual stitches, slightly irregular handmade quality,
a delicate forehead ornament of tiny gold and jade flowers set between the eyebrows,
a beaded necklace of carved jade beads and pearls resting on the collarbone,
the cloud collar worked in ivory silk and gold thread to match the gown,
three-quarter portrait in soft north window light,
gentle shadow gradient across the porcelain cheek, quiet neutral interior backdrop
```

### figure-medium　seed=2110　（本轮覆盖：880×2048）

产物：`out/r21/bc-r21-figure-medium_00001_.png`

```text
Full-length photograph:
the entire doll from the top of the hair bun down to the hem of the skirt and her porcelain
slippers is inside the frame,
standing upright on a low carved wooden stand, the high-waisted skirt, the gold chest band,
the trailing gauze scarf and the hem are all visible,
low-key museum lighting with a distant soft spotlight, dark hall backdrop, slight low camera angle.
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners, dark brown irises,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun held by a gold filigree hairpin set with
jade and a dangling pearl ornament.
She wears a high-waisted Tang-style ivory silk gown with a gold-thread sash and a long sheer gauze
scarf,
its chest band woven with gold peony patterns and set with carved jade,
and a jade-inlaid gold filigree belt.
Fine art studio lighting from the upper left, deep but clean shadows, sharp focus,
medium format camera, 120mm macro lens, natural sensor grain, no digital sharpening.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
carved jade with a soft waxy lustre, engraved gold filigree with milled edges,
silk with a visible woven weft, seed pearls, absolutely no CGI smoothness
```

### final-seated　seed=2120　（本轮覆盖：1600×1600）

产物：`out/r21/bc-r21-final-seated_00001_.png`

```text
Museum-quality photograph of a handcrafted ball-jointed bone china doll of an Eastern classical
princess,
photographed like a real physical object under studio light.
Pristine flawless ivory porcelain with a perfectly smooth fired glaze, crisp specular highlights,
delicate warm translucency at the thin porcelain of the ears and fingertips,
microscopic surface texture, completely clean and dust-free.
Visible ball-joint seams at the neck and wrists.
An elegant Eastern classical beauty with refined adult proportions:
a delicate oval face with a softly tapered jaw, fine arched willow-leaf eyebrows,
a slender straight nose bridge, a small rosebud mouth with serene closed lips,
almond eyes of realistic size with gently upswept outer corners and a subtle crease,
dark brown irises, individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush on the cheeks.
Glossy black hair dressed in a classical high coiled bun with a few loose strands at the temples,
held by a gold filigree hairpin set with jade and a dangling pearl ornament.
She wears a classical Eastern gown of ivory silk with a crossed collar,
wide flowing sleeves and a broad sash, woven with gold-thread cloud and peony patterns,
its edges densely embroidered and trimmed with hundreds of tiny seed pearls stitched one by one,
a jade-inlaid gold filigree belt, an embroidered cloud collar over the shoulders,
and carved jade earrings with gold filigree.
Fine art studio lighting from the upper left, gentle rim light, deep but clean shadows,
sharp focus on the face, medium format camera, 120mm macro lens, natural shallow depth of field,
seamless neutral backdrop.
Extravagant craft: ivory silk brocade with raised gold-thread embroidery,
dense silk embroidery with individual visible threads, seed pearls stitched one by one,
carved jade with a soft waxy lustre and internal veining, gold filigree with milled edges,
a heavy ceremonial headdress with enamelled details.
Sculptural chiaroscuro studio lighting with one strong key light and deep natural falloff,
subtle warm bounce on the shadow side, museum-vitrine realism, tack-sharp focus on the face,
extremely fine texture.
Extremely fine porcelain surface: microscopic glaze texture with faint polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle colour variation in the ivory,
absolutely no CGI smoothness.
Photographed with a 100mm macro lens at f/8, focus stacked, ultra high resolution scan quality,
natural sensor grain.
Jewellery realism: engraved gold filigree with crisp milled edges,
carved jade showing internal veining, seed pearls with subtle orient and nacre rings,
metal prongs and hinges clearly readable.
Fabric realism: silk with a visible woven weft, embroidered satin, linen-backed inner layers,
visible individual stitches, slightly irregular handmade quality,
a delicate forehead ornament of tiny gold and jade flowers set between the eyebrows,
a beaded necklace of carved jade beads and pearls resting on the collarbone,
the cloud collar worked in ivory silk and gold thread to match the gown,
seated three-quarter view at a small rosewood table,
both porcelain hands resting on her lap with the ball-joint seams at the wrists clearly visible,
a round silk fan lying on the table, soft north window light, quiet interior backdrop
```

## R22 · phase 4 opens: drop every doll/ball-joint/display-stand word, make her a living princess whose skin is bone-china fine; first Chinese prompt, written in the layered Dream-of-the-Red-Chamber entrance style

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像
```

### portrait　seed=2200　（本轮覆盖：1280×1712）

产物：`out/r22/bc-r22-portrait_00001_.png`

```text
一幅细致入微的东方古典公主写照，写实照片，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支赤金点翠衔珠凤钗，凤口垂下三串米珠，鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。鹅蛋脸儿，
面若中秋之月，色如春晓之花。两弯似蹙非蹙的罥烟眉，眉梢淡淡入鬓。一双似喜非喜的含情目，眸子如秋水，
瞳仁漆黑，虹膜有一圈极细的纹路，睫毛根根分明，眼睑薄得透出一线极淡的血色，瞳子里含着一点窗光。鼻梁秀
挺，
鼻头圆润。樱桃小口，唇色如点朱，唇角含着一点未露的笑意。肌肤莹润如骨瓷：细腻得如同刚出窑的细瓷，
看不见毛孔，却绝不是塑料那样的平滑；面颊覆着一层极薄的釉光，胎薄处——耳缘、鼻翼、
指尖——透着温润的血色与光；颧骨上一抹极淡的绯色，下颌与颈侧有柔和的反射，皮肤上有一层极细的绒毛。项上
一条赤金盘螭璎珞圈，
嵌着羊脂白玉与东珠。身上穿着月白织金团花褙子，领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；
腰间一条秋香色宫绦，垂一块双衡比目玉佩；下着藕荷色绣兰裙。神态端庄沉静，含而不露，
眉心一点若有若无的轻愁。身后一架紫檀绢本屏风，几上博山炉袅袅一缕沉香，窗外疏影横斜。柔和天光自左侧斜
照进来，
面上的明暗过渡自然。真实照片，中画幅相机，120mm 微距镜头，浅景深，自然颗粒，无数字锐化。半身像，
取到腰际，人在内室中，身后屏风与几案柔和虚化
```

### full-figure　seed=2210　（本轮覆盖：880×2048）

产物：`out/r22/bc-r22-full-figure_00001_.png`

```text
一幅细致入微的东方古典公主写照，写实照片，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支赤金点翠衔珠凤钗，凤口垂下三串米珠，鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。鹅蛋脸儿，
面若中秋之月，色如春晓之花。两弯似蹙非蹙的罥烟眉，眉梢淡淡入鬓。一双似喜非喜的含情目，眸子如秋水，
瞳仁漆黑，虹膜有一圈极细的纹路，睫毛根根分明，眼睑薄得透出一线极淡的血色，瞳子里含着一点窗光。鼻梁秀
挺，
鼻头圆润。樱桃小口，唇色如点朱，唇角含着一点未露的笑意。肌肤莹润如骨瓷：细腻得如同刚出窑的细瓷，
看不见毛孔，却绝不是塑料那样的平滑；面颊覆着一层极薄的釉光，胎薄处——耳缘、鼻翼、
指尖——透着温润的血色与光；颧骨上一抹极淡的绯色，下颌与颈侧有柔和的反射，皮肤上有一层极细的绒毛。项上
一条赤金盘螭璎珞圈，
嵌着羊脂白玉与东珠。身上穿着月白织金团花褙子，领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；
腰间一条秋香色宫绦，垂一块双衡比目玉佩；下着藕荷色绣兰裙。神态端庄沉静，含而不露，
眉心一点若有若无的轻愁。身后一架紫檀绢本屏风，几上博山炉袅袅一缕沉香，窗外疏影横斜。柔和天光自左侧斜
照进来，
面上的明暗过渡自然。真实照片，中画幅相机，120mm 微距镜头，浅景深，自然颗粒，无数字锐化。全身像，
自飞仙髻直到裙裾与绣鞋尽入画面，人立于内室地上，裙裾曳地，身姿挺拔，不倚不靠
```

### skin-plate　seed=2220　（本轮覆盖：1600×2144）

产物：`out/r22/bc-r22-skin-plate_00001_.png`

```text
一幅细致入微的东方古典公主写照，写实照片，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支赤金点翠衔珠凤钗，凤口垂下三串米珠，鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。鹅蛋脸儿，
面若中秋之月，色如春晓之花。两弯似蹙非蹙的罥烟眉，眉梢淡淡入鬓。一双似喜非喜的含情目，眸子如秋水，
瞳仁漆黑，虹膜有一圈极细的纹路，睫毛根根分明，眼睑薄得透出一线极淡的血色，瞳子里含着一点窗光。鼻梁秀
挺，
鼻头圆润。樱桃小口，唇色如点朱，唇角含着一点未露的笑意。肌肤莹润如骨瓷：细腻得如同刚出窑的细瓷，
看不见毛孔，却绝不是塑料那样的平滑；面颊覆着一层极薄的釉光，胎薄处——耳缘、鼻翼、
指尖——透着温润的血色与光；颧骨上一抹极淡的绯色，下颌与颈侧有柔和的反射，皮肤上有一层极细的绒毛。项上
一条赤金盘螭璎珞圈，
嵌着羊脂白玉与东珠。身上穿着月白织金团花褙子，领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；
腰间一条秋香色宫绦，垂一块双衡比目玉佩；下着藕荷色绣兰裙。神态端庄沉静，含而不露，
眉心一点若有若无的轻愁。身后一架紫檀绢本屏风，几上博山炉袅袅一缕沉香，窗外疏影横斜。柔和天光自左侧斜
照进来，
面上的明暗过渡自然。真实照片，中画幅相机，120mm 微距镜头，浅景深，自然颗粒，无数字锐化。近景肖像，
面部占据画面大半，肌肤的细腻质感、釉光与眼神里的高光清晰可辨，背景完全虚化
```

## R23 · bilingual base: Chinese for what exists, English for what it is made of -- the subject stays a living princess while her skin is bone china again; makeup pinned to 素面

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容
```

### portrait　seed=2300　（本轮覆盖：1280×1712）

产物：`out/r23/bc-r23-portrait_00001_.png`

```text
一幅细致入微的东方古典公主写照，写实照片，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支金累丝衔珠凤钗，凤口垂下三串米珠，鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。鹅蛋脸儿，
面若中秋之月，色如春晓之花。两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛。一双似喜非喜的含情目，
眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，睫毛根根分明，眼睑薄得透出一线极淡的血色，
瞳子里含着一点窗光。鼻梁秀挺，鼻头圆润。樱桃小口，唇上只点一点浅胭脂，唇角含着一点未露的笑意。妆极淡
，
近乎素面，只在颊上留一抹极淡的绯色。项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。身上穿着月白织金团花
褙子，
领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；腰间一条秋香色宫绦，垂一块双衡比目玉佩；
下着藕荷色绣兰裙。神态端庄沉静，含而不露，眉心一点若有若无的轻愁。身后一架紫檀绢本屏风，
几上博山炉袅袅一缕沉香，窗外疏影横斜。柔和天光自左侧斜照进来，面上的明暗过渡自然。 Her skin is bone
china -- the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
delicate warm translucency glowing through the thin porcelain of the ears,
the wings of the nose and the fingertips,
microscopic glaze texture with the faintest polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle variation in the ivory,
a soft ivory sheen, and absolutely no CGI smoothness and no plastic.
Fine art studio lighting from the upper left, deep but clean shadows, sharp focus on the eyes.
Photographed on a medium format camera with a 120mm macro lens at f/2.8, natural sensor grain,
no digital sharpening。半身像，取到腰际，人在内室中，身后屏风与几案柔和虚化
```

### full-figure　seed=2310　（本轮覆盖：880×2048）

产物：`out/r23/bc-r23-full-figure_00001_.png`

```text
一幅细致入微的东方古典公主写照，写实照片，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支金累丝衔珠凤钗，鬓边一朵白玉兰。鹅蛋脸儿，两弯似蹙非蹙的罥烟眉，一双似喜非喜的含情目，
樱桃小口，妆极淡，近乎素面。身上是月白织金团花褙子，腰间一条秋香色宫绦，垂一块双衡比目玉佩。神态端庄
沉静。身后一架紫檀绢本屏风，
几上一缕沉香，窗外疏影横斜。 Her skin is bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
delicate warm translucency glowing through the thin porcelain of the ears,
the wings of the nose and the fingertips,
microscopic glaze texture with the faintest polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle variation in the ivory,
a soft ivory sheen, and absolutely no CGI smoothness and no plastic.
Fine art studio lighting from the upper left, deep but clean shadows, sharp focus on the eyes.
Photographed on a medium format camera with a 120mm macro lens at f/2.8, natural sensor grain,
no digital sharpening。全身像，自飞仙髻直到裙裾与绣鞋尽入画面，人立于内室地上，裙裾曳地，身姿挺拔，
不倚不靠
```

### skin-plate　seed=2320　（本轮覆盖：1600×2144）

产物：`out/r23/bc-r23-skin-plate_00001_.png`

```text
一幅细致入微的东方古典公主写照，写实照片，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支金累丝衔珠凤钗，凤口垂下三串米珠，鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。鹅蛋脸儿，
面若中秋之月，色如春晓之花。两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛。一双似喜非喜的含情目，
眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，睫毛根根分明，眼睑薄得透出一线极淡的血色，
瞳子里含着一点窗光。鼻梁秀挺，鼻头圆润。樱桃小口，唇上只点一点浅胭脂，唇角含着一点未露的笑意。妆极淡
，
近乎素面，只在颊上留一抹极淡的绯色。项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。身上穿着月白织金团花
褙子，
领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；腰间一条秋香色宫绦，垂一块双衡比目玉佩；
下着藕荷色绣兰裙。神态端庄沉静，含而不露，眉心一点若有若无的轻愁。身后一架紫檀绢本屏风，
几上博山炉袅袅一缕沉香，窗外疏影横斜。柔和天光自左侧斜照进来，面上的明暗过渡自然。 Her skin is bone
china -- the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
delicate warm translucency glowing through the thin porcelain of the ears,
the wings of the nose and the fingertips,
microscopic glaze texture with the faintest polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle variation in the ivory,
a soft ivory sheen, and absolutely no CGI smoothness and no plastic.
Fine art studio lighting from the upper left, deep but clean shadows, sharp focus on the eyes.
Photographed on a medium format camera with a 120mm macro lens at f/2.8, natural sensor grain,
no digital sharpening。近景肖像，面部占据画面大半，肌肤的细腻质感、釉光与眼神里的高光清晰可辨，
背景完全虚化
```

## R24 · material block moved to the FRONT of the prompt (R11/R15 position rule); Chinese passage gains an explicit 瓷胎 layer and drops 写实照片; negative forbids human-skin cues

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容, human skin texture,
realistic skin pores, visible pores, matte skin, ordinary human skin, retouched skin,
airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔
```

### portrait　seed=2400　（本轮覆盖：1280×1712）

产物：`out/r24/bc-r24-portrait_00001_.png`

```text
Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china --
the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
delicate warm translucency glowing through the thin porcelain of the ears,
the wings of the nose and the fingertips,
microscopic glaze texture with the faintest polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle variation in the ivory,
a soft ivory sheen, absolutely no CGI smoothness and no plastic.
Her face is human; her skin is
porcelain. 一幅细致入微的东方古典公主写照，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支金累丝衔珠凤钗，凤口垂下三串米珠，鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。鹅蛋脸儿，
面若中秋之月，色如春晓之花；两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；一双似喜非喜的含情目，
眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，睫毛根根分明，眼睑薄得透出一线极淡的血色，
瞳子里含着一点窗光。鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂。妆极淡，近乎素面。肌肤是骨瓷的
胎质：
莹润而半透，面颊上覆着一层极薄的釉，胎薄处——耳缘、鼻翼、指节——透出温润的血色与光，
釉下可见极细的气泡与磨痕，却不见肉身的毛孔。项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。身上穿着月白
织金团花褙子，
领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；腰间一条秋香色宫绦，垂一块双衡比目玉佩；
下着藕荷色绣兰裙。神态端庄沉静，含而不露，眉心一点若有若无的轻愁。身后一架紫檀绢本屏风，
几上博山炉袅袅一缕沉香，窗外疏影横斜。柔和天光自左侧斜照进来。中画幅相机，120mm 微距镜头，f/2.8，
浅景深，自然颗粒，无数字锐化。半身像，取到腰际，身后屏风与几案柔和虚化
```

### full-figure　seed=2410　（本轮覆盖：880×2048）

产物：`out/r24/bc-r24-full-figure_00001_.png`

```text
Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china --
the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
delicate warm translucency glowing through the thin porcelain of the ears,
the wings of the nose and the fingertips,
microscopic glaze texture with the faintest polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle variation in the ivory,
a soft ivory sheen, absolutely no CGI smoothness and no plastic.
Her face is human; her skin is
porcelain. 一幅细致入微的东方古典公主写照，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支金累丝衔珠凤钗，鬓边一朵白玉兰。鹅蛋脸儿，两弯似蹙非蹙的罥烟眉，一双似喜非喜的含情目，
樱桃小口，妆极淡，近乎素面。肌肤是骨瓷的胎质：莹润而半透，面颊上覆着一层极薄的釉。身上是月白织金团花
褙子，
腰间一条秋香色宫绦，垂一块双衡比目玉佩。神态端庄沉静。身后一架紫檀绢本屏风，几上一缕沉香，
窗外疏影横斜。中画幅相机，120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化。全身像，
自飞仙髻直到裙裾与绣鞋尽入画面，人立于内室地上，裙裾曳地，身姿挺拔，不倚不靠
```

### skin-plate　seed=2420　（本轮覆盖：1600×2144）

产物：`out/r24/bc-r24-skin-plate_00001_.png`

```text
Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china --
the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
delicate warm translucency glowing through the thin porcelain of the ears,
the wings of the nose and the fingertips,
microscopic glaze texture with the faintest polishing marks,
a few microscopic bubbles suspended inside the glaze, gentle variation in the ivory,
a soft ivory sheen, absolutely no CGI smoothness and no plastic.
Her face is human; her skin is
porcelain. 一幅细致入微的东方古典公主写照，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支金累丝衔珠凤钗，凤口垂下三串米珠，鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。鹅蛋脸儿，
面若中秋之月，色如春晓之花；两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；一双似喜非喜的含情目，
眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，睫毛根根分明，眼睑薄得透出一线极淡的血色，
瞳子里含着一点窗光。鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂。妆极淡，近乎素面。肌肤是骨瓷的
胎质：
莹润而半透，面颊上覆着一层极薄的釉，胎薄处——耳缘、鼻翼、指节——透出温润的血色与光，
釉下可见极细的气泡与磨痕，却不见肉身的毛孔。项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。身上穿着月白
织金团花褙子，
领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；腰间一条秋香色宫绦，垂一块双衡比目玉佩；
下着藕荷色绣兰裙。神态端庄沉静，含而不露，眉心一点若有若无的轻愁。身后一架紫檀绢本屏风，
几上博山炉袅袅一缕沉香，窗外疏影横斜。柔和天光自左侧斜照进来。中画幅相机，120mm 微距镜头，f/2.8，
浅景深，自然颗粒，无数字锐化。近景肖像，面部占据画面大半，肌肤的瓷胎质感、
釉光与眼神里的高光清晰可辨，背景完全虚化
```

## R25 · kill the elf-ear artifact, NAME the real defects of a fired glaze (pinholes, bubbles, drag lines, orange peel, uneven glaze) so the surface stops being featureless, and shoot the skin plate on a 2048 square so the face finally occupies enough pixels for a macro

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容, human skin texture,
realistic skin pores, visible pores, matte skin, ordinary human skin, retouched skin,
airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔, pointed ears, elf ears, long pointed ears,
glowing orange ears, animal ears, 尖耳, 精灵耳, smooth featureless skin, uniform flat surface,
completely even skin, waxy flawless surface, 光滑无细节, 死白, 蜡像
```

### portrait　seed=2500　（本轮覆盖：1280×1712）

产物：`out/r25/bc-r25-portrait_00001_.png`

```text
Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china --
the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
warm translucency glowing through the thin porcelain of the fingertips and the temples,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit,
and a soft blush of warm colour across the cheeks -- real variation everywhere,
never a uniform flat surface, absolutely no CGI smoothness and no plastic.
Her face is human; her skin is
porcelain. 一幅细致入微的东方古典公主写照，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支金累丝衔珠凤钗，凤口垂下三串米珠，鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。鹅蛋脸儿，
面若中秋之月，色如春晓之花；两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；一双似喜非喜的含情目，
眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，睫毛根根分明，眼睑薄得透出一线极淡的血色，
瞳子里含着一点窗光。鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂。妆极淡，近乎素面。肌肤是骨瓷的
胎质：
莹润而半透，面颊上覆着一层极薄的釉，颞侧与指节这些胎薄处透出温润的血色与光；釉面并非均匀光滑，
而是有极细的缩釉小点、釉下的小气泡与棕眼、擦拭留下的细磨痕、橘子皮似的细微起伏，釉色深浅也略有不同；
两颊透出温润的血色，却不见肉身的毛孔。项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。身上穿着月白织金团
花褙子，
领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；腰间一条秋香色宫绦，垂一块双衡比目玉佩；
下着藕荷色绣兰裙。神态端庄沉静，含而不露，眉心一点若有若无的轻愁。身后一架紫檀绢本屏风，
几上博山炉袅袅一缕沉香，窗外疏影横斜。柔和天光自左侧斜照进来。中画幅相机，120mm 微距镜头，f/2.8，
浅景深，自然颗粒，无数字锐化。半身像，取到腰际，身后屏风与几案柔和虚化
```

### full-figure　seed=2510　（本轮覆盖：880×2048）

产物：`out/r25/bc-r25-full-figure_00001_.png`

```text
Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china --
the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
warm translucency glowing through the thin porcelain of the fingertips and the temples,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit,
and a soft blush of warm colour across the cheeks -- real variation everywhere,
never a uniform flat surface, absolutely no CGI smoothness and no plastic.
Her face is human; her skin is
porcelain. 一幅细致入微的东方古典公主写照，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支金累丝衔珠凤钗，鬓边一朵白玉兰。鹅蛋脸儿，两弯似蹙非蹙的罥烟眉，一双似喜非喜的含情目，
樱桃小口，妆极淡，近乎素面。肌肤是骨瓷的胎质：莹润而半透，面颊上覆着一层极薄的釉，
釉面有极细的缩釉点与磨痕。身上是月白织金团花褙子，腰间一条秋香色宫绦，垂一块双衡比目玉佩。神态端庄沉
静。身后一架紫檀绢本屏风，
几上一缕沉香，窗外疏影横斜。中画幅相机，120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化。全身像
，
自飞仙髻直到裙裾与绣鞋尽入画面，人立于内室地上，裙裾曳地，身姿挺拔，不倚不靠
```

### skin-square　seed=2520　（本轮覆盖：2048×2048）

产物：`out/r25/bc-r25-skin-square_00001_.png`

```text
Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china --
the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
warm translucency glowing through the thin porcelain of the fingertips and the temples,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit,
and a soft blush of warm colour across the cheeks -- real variation everywhere,
never a uniform flat surface, absolutely no CGI smoothness and no plastic.
Her face is human; her skin is
porcelain. 一幅细致入微的东方古典公主写照，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支金累丝衔珠凤钗，凤口垂下三串米珠，鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。鹅蛋脸儿，
面若中秋之月，色如春晓之花；两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；一双似喜非喜的含情目，
眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，睫毛根根分明，眼睑薄得透出一线极淡的血色，
瞳子里含着一点窗光。鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂。妆极淡，近乎素面。肌肤是骨瓷的
胎质：
莹润而半透，面颊上覆着一层极薄的釉，颞侧与指节这些胎薄处透出温润的血色与光；釉面并非均匀光滑，
而是有极细的缩釉小点、釉下的小气泡与棕眼、擦拭留下的细磨痕、橘子皮似的细微起伏，釉色深浅也略有不同；
两颊透出温润的血色，却不见肉身的毛孔。项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。身上穿着月白织金团
花褙子，
领口袖口滚两道金线绣边，绣的是缠枝莲与折枝海棠；腰间一条秋香色宫绦，垂一块双衡比目玉佩；
下着藕荷色绣兰裙。神态端庄沉静，含而不露，眉心一点若有若无的轻愁。身后一架紫檀绢本屏风，
几上博山炉袅袅一缕沉香，窗外疏影横斜。柔和天光自左侧斜照进来。中画幅相机，120mm 微距镜头，f/2.8，
浅景深，自然颗粒，无数字锐化。近景肖像，面部占据画面大半，肌肤的瓷胎质感、釉面的缩釉点与磨痕、
以及眼神里的高光清晰可辨，背景完全虚化
```

## R26 · clothing-only change: heavy gold brocade -> several layers of cicada-wing gauze over bone-china-white silk, sheer and lifting, with porcelain-crisp weave and edges; the frozen skin block from R25 is reused verbatim

- 引擎：`qwen`　尺寸：1280×1712　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容, human skin texture,
realistic skin pores, visible pores, matte skin, ordinary human skin, retouched skin,
airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔, pointed ears, elf ears, long pointed ears,
glowing orange ears, animal ears, 尖耳, 精灵耳, smooth featureless skin, uniform flat surface,
completely even skin, waxy flawless surface, 光滑无细节, 死白, 蜡像, heavy stiff fabric,
thick brocade, heavy gold embroidery, dense embroidery, bulky robe, cardboard-stiff
cloth, 厚重布料, 硬挺厚缎, 繁密织金, 笨重
```

### portrait　seed=2600　（本轮覆盖：1280×1712）

产物：`out/r26/bc-r26-portrait_00001_.png`

```text
Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china --
the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
warm translucency glowing through the thin porcelain of the fingertips and the temples,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit,
and a soft blush of warm colour across the cheeks -- real variation everywhere,
never a uniform flat surface, absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
Her robes are nearly weightless: several layers of fine translucent gauze as thin as cicada wings,
drifting and floating in the still air,
the outermost layer so sheer that the layers beneath it and the light behind them show through,
the sleeves and hems lifting as if in a breath of air;
the gauze keeps the crisp fine weave and the cleanly cut edge of porcelain rather than the softness
of ordinary cloth,
half gauze and half bone
china。 一幅细致入微的东方古典公主写照，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支金累丝衔珠凤钗，凤口垂下三串米珠，鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。鹅蛋脸儿，
面若中秋之月，色如春晓之花；两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；一双似喜非喜的含情目，
眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，睫毛根根分明，眼睑薄得透出一线极淡的血色，
瞳子里含着一点窗光。鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂。妆极淡，近乎素面。肌肤是骨瓷的
胎质：
莹润而半透，面颊上覆着一层极薄的釉，颞侧与指节这些胎薄处透出温润的血色与光；釉面并非均匀光滑，
而是有极细的缩釉小点、釉下的小气泡与棕眼、擦拭留下的细磨痕、橘子皮似的细微起伏，釉色深浅也略有不同；
两颊透出温润的血色，却不见肉身的毛孔。项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。身上是数层极轻的纱
罗：
外层薄如蝉翼的素纱，内层是骨瓷白的细绢，纱薄得透出里层的光影与轮廓；衣袂与披帛飘飘欲举，
裙裾曳地如烟；纱罗的经纬细密而挺括，边缘清爽利落，有瓷器那样的筋骨，绝不是软塌塌的厚布；
纱上只用极细的银线疏疏绣着几枝兰草，不作繁密织金；腰间一条秋香色宫绦，垂一块双衡比目玉佩。神态端庄沉
静，
含而不露，眉心一点若有若无的轻愁。身后一架紫檀绢本屏风，几上博山炉袅袅一缕沉香，窗外疏影横斜。柔和天
光自左侧斜照进来，
纱罗在光里近乎透亮。中画幅相机，120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化。半身像，
取到腰际，纱罗的层次与透光清晰可见，身后屏风与几案柔和虚化
```

### full-figure　seed=2610　（本轮覆盖：880×2048）

产物：`out/r26/bc-r26-full-figure_00001_.png`

```text
Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china --
the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
warm translucency glowing through the thin porcelain of the fingertips and the temples,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit,
and a soft blush of warm colour across the cheeks -- real variation everywhere,
never a uniform flat surface, absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
Her robes are nearly weightless: several layers of fine translucent gauze as thin as cicada wings,
drifting and floating in the still air,
the outermost layer so sheer that the layers beneath it and the light behind them show through,
the sleeves and hems lifting as if in a breath of air;
the gauze keeps the crisp fine weave and the cleanly cut edge of porcelain rather than the softness
of ordinary cloth,
half gauze and half bone
china。 一幅细致入微的东方古典公主写照，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支金累丝衔珠凤钗，鬓边一朵白玉兰。鹅蛋脸儿，两弯似蹙非蹙的罥烟眉，一双似喜非喜的含情目，
樱桃小口，妆极淡，近乎素面。肌肤是骨瓷的胎质：莹润而半透，面颊上覆着一层极薄的釉，
釉面有极细的缩釉点与磨痕。身上是数层极轻的纱罗，薄如蝉翼，衣袂与裙裾飘飘欲举，纱上疏疏几枝银线兰草。
神态端庄沉静。身后一架紫檀绢本屏风，
几上一缕沉香，窗外疏影横斜。中画幅相机，120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化。全身像
，
自飞仙髻直到裙裾与绣鞋尽入画面，人立于内室地上，裙裾曳地如烟，衣袂飘飘，身姿挺拔，不倚不靠
```

### airy-turn　seed=2620　（本轮覆盖：1600×1600）

产物：`out/r26/bc-r26-airy-turn_00001_.png`

```text
Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china --
the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
warm translucency glowing through the thin porcelain of the fingertips and the temples,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit,
and a soft blush of warm colour across the cheeks -- real variation everywhere,
never a uniform flat surface, absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
Her robes are nearly weightless: several layers of fine translucent gauze as thin as cicada wings,
drifting and floating in the still air,
the outermost layer so sheer that the layers beneath it and the light behind them show through,
the sleeves and hems lifting as if in a breath of air;
the gauze keeps the crisp fine weave and the cleanly cut edge of porcelain rather than the softness
of ordinary cloth,
half gauze and half bone
china。 一幅细致入微的东方古典公主写照，人在内室之中。乌油油的青丝绾成飞仙髻，
正中一支金累丝衔珠凤钗，凤口垂下三串米珠，鬓边斜插一朵白玉兰，耳畔两缕碎发贴颊。鹅蛋脸儿，
面若中秋之月，色如春晓之花；两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；一双似喜非喜的含情目，
眸子如秋水，瞳仁漆黑，虹膜有一圈极细的纹路，睫毛根根分明，眼睑薄得透出一线极淡的血色，
瞳子里含着一点窗光。鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂。妆极淡，近乎素面。肌肤是骨瓷的
胎质：
莹润而半透，面颊上覆着一层极薄的釉，颞侧与指节这些胎薄处透出温润的血色与光；釉面并非均匀光滑，
而是有极细的缩釉小点、釉下的小气泡与棕眼、擦拭留下的细磨痕、橘子皮似的细微起伏，釉色深浅也略有不同；
两颊透出温润的血色，却不见肉身的毛孔。项上一条赤金盘螭璎珞圈，嵌着羊脂白玉与东珠。身上是数层极轻的纱
罗：
外层薄如蝉翼的素纱，内层是骨瓷白的细绢，纱薄得透出里层的光影与轮廓；衣袂与披帛飘飘欲举，
裙裾曳地如烟；纱罗的经纬细密而挺括，边缘清爽利落，有瓷器那样的筋骨，绝不是软塌塌的厚布；
纱上只用极细的银线疏疏绣着几枝兰草，不作繁密织金；腰间一条秋香色宫绦，垂一块双衡比目玉佩。神态端庄沉
静，
含而不露，眉心一点若有若无的轻愁。身后一架紫檀绢本屏风，几上博山炉袅袅一缕沉香，窗外疏影横斜。柔和天
光自左侧斜照进来，
纱罗在光里近乎透亮。中画幅相机，120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化。侧身回眸的瞬间
，
衣袂与披帛随动作扬起，纱罗在光里近乎透亮，能看见里层的轮廓与光影
```

## R27 · natural flush instead of applied blush, languid everyday mood, and three FULL-BODY poses -- seated on a daybed, reclining on one elbow, and lying on the front; the two lying poses use landscape canvases (a new use of the R15 aspect-ratio lever)

- 引擎：`qwen`　尺寸：1200×1600　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容, human skin texture,
realistic skin pores, visible pores, matte skin, ordinary human skin, retouched skin,
airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔, pointed ears, elf ears, long pointed ears,
glowing orange ears, animal ears, 尖耳, 精灵耳, smooth featureless skin, uniform flat surface,
completely even skin, waxy flawless surface, 光滑无细节, 死白, 蜡像, heavy stiff fabric,
thick brocade, heavy gold embroidery, dense embroidery, bulky robe, cardboard-stiff
cloth, 厚重布料, 硬挺厚缎, 繁密织金, 笨重,
blush makeup, rouge, blush patches, circular blush, doll-like blush, heavy blush,
applied cosmetics, stiff formal pose, studio pose, standing to
attention, 腮红, 胭脂印, 高原红, 刻意妆容, 端坐, 摆拍
```

### seated-daybed　seed=2700　（本轮覆盖：1200×1600）

产物：`out/r27/bc-r27-seated-daybed_00001_.png`

```text
Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china --
the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
warm translucency glowing through the thin porcelain of the fingertips and the temples,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit, and only the faint,
uneven flush of real living skin -- colour that wells up from beneath rather than anything applied,
no rouge, no drawn-on blush and no blush patches -- real variation everywhere,
never a uniform flat surface, absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
Her robes are nearly weightless: several layers of fine translucent gauze as thin as cicada wings,
drifting and floating in the still air,
the outermost layer so sheer that the layers beneath it and the light behind them show through,
the sleeves and hems lifting as if in a breath of air;
the gauze keeps the crisp fine weave and the cleanly cut edge of porcelain rather than the softness
of ordinary cloth,
half gauze and half bone china。 一幅细致入微的东方古典公主写照：家常日子里的一个瞬间，
人在内室之中。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，鬓边散下几缕碎发。鹅蛋脸儿，面若中秋之月，
色如春晓之花；两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；一双似喜非喜的含情目，眸子如秋水，
眼神懒懒的，半含睡意；鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂，嘴角松松的，不刻意含笑。妆极
淡，
近乎素面，血色自里透出，深浅不匀，自然得很，绝不是涂上去的胭脂，也不见肉身的毛孔。肌肤是骨瓷的胎质：
莹润而半透，面颊上覆着一层极薄的釉，釉面有极细的缩釉点与磨痕，橘子皮似的细微起伏，
釉色深浅也略有不同。身上是数层极轻的纱罗，薄如蝉翼，衣襟齐整却穿得松泛，袖口松松滑落，宫绦松松系着。
神态慵懒闲适，
不拘礼数，像在自己屋里歇着。内室里一架紫檀绢本屏风，几上一缕沉香，窗外疏影横斜。中画幅相机，
120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化。全身像：她斜坐在一张矮榻上，一条腿屈起，
手肘支在隐囊上，一手托腮，懒懒望向窗外，纱罗的衣袂垂落榻沿，榻边几上一盏半凉的茶，姿态松弛
```

### recline-side　seed=2710　（本轮覆盖：2048×1024）

产物：`out/r27/bc-r27-recline-side_00001_.png`

```text
Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china --
the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
warm translucency glowing through the thin porcelain of the fingertips and the temples,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit, and only the faint,
uneven flush of real living skin -- colour that wells up from beneath rather than anything applied,
no rouge, no drawn-on blush and no blush patches -- real variation everywhere,
never a uniform flat surface, absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
Her robes are nearly weightless: several layers of fine translucent gauze as thin as cicada wings,
drifting and floating in the still air,
the outermost layer so sheer that the layers beneath it and the light behind them show through,
the sleeves and hems lifting as if in a breath of air;
the gauze keeps the crisp fine weave and the cleanly cut edge of porcelain rather than the softness
of ordinary cloth,
half gauze and half bone china。 一幅细致入微的东方古典公主写照：家常日子里的一个瞬间，
人在内室之中。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，鬓边散下几缕碎发。鹅蛋脸儿，面若中秋之月，
色如春晓之花；两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；一双似喜非喜的含情目，眸子如秋水，
眼神懒懒的，半含睡意；鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂，嘴角松松的，不刻意含笑。妆极
淡，
近乎素面，血色自里透出，深浅不匀，自然得很，绝不是涂上去的胭脂，也不见肉身的毛孔。肌肤是骨瓷的胎质：
莹润而半透，面颊上覆着一层极薄的釉，釉面有极细的缩釉点与磨痕，橘子皮似的细微起伏，
釉色深浅也略有不同。身上是数层极轻的纱罗，薄如蝉翼，衣襟齐整却穿得松泛，袖口松松滑落，宫绦松松系着。
神态慵懒闲适，
不拘礼数，像在自己屋里歇着。内室里一架紫檀绢本屏风，几上一缕沉香，窗外疏影横斜。中画幅相机，
120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化。全身横构图：她侧卧在榻上，一手支腮，
另一手随意搭在身侧，数层纱罗铺散在锦垫上，膝上覆着一条薄毯，榻边摊着一卷未读完的书，
午后光斜斜落在榻上
```

### prone　seed=2720　（本轮覆盖：1792×1152）

产物：`out/r27/bc-r27-prone_00001_.png`

```text
Photorealistic portrait of a living Eastern classical princess whose skin is made of bone china --
the material itself,
not a mask: ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes,
warm translucency glowing through the thin porcelain of the fingertips and the temples,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit, and only the faint,
uneven flush of real living skin -- colour that wells up from beneath rather than anything applied,
no rouge, no drawn-on blush and no blush patches -- real variation everywhere,
never a uniform flat surface, absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
Her robes are nearly weightless: several layers of fine translucent gauze as thin as cicada wings,
drifting and floating in the still air,
the outermost layer so sheer that the layers beneath it and the light behind them show through,
the sleeves and hems lifting as if in a breath of air;
the gauze keeps the crisp fine weave and the cleanly cut edge of porcelain rather than the softness
of ordinary cloth,
half gauze and half bone china。 一幅细致入微的东方古典公主写照：家常日子里的一个瞬间，
人在内室之中。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，鬓边散下几缕碎发。鹅蛋脸儿，面若中秋之月，
色如春晓之花；两弯似蹙非蹙的罥烟眉，眉如远山，不施浓黛；一双似喜非喜的含情目，眸子如秋水，
眼神懒懒的，半含睡意；鼻梁秀挺，鼻头圆润；樱桃小口，唇上只点一点浅胭脂，嘴角松松的，不刻意含笑。妆极
淡，
近乎素面，血色自里透出，深浅不匀，自然得很，绝不是涂上去的胭脂，也不见肉身的毛孔。肌肤是骨瓷的胎质：
莹润而半透，面颊上覆着一层极薄的釉，釉面有极细的缩釉点与磨痕，橘子皮似的细微起伏，
釉色深浅也略有不同。身上是数层极轻的纱罗，薄如蝉翼，衣襟齐整却穿得松泛，袖口松松滑落，宫绦松松系着。
神态慵懒闲适，
不拘礼数，像在自己屋里歇着。内室里一架紫檀绢本屏风，几上一缕沉香，窗外疏影横斜。中画幅相机，
120mm 微距镜头，f/2.8，浅景深，自然颗粒，无数字锐化。全身横构图：她伏卧在长榻上，两肘撑着上身，
下巴搁在手背上，小腿在身后轻轻翘起交错，纱罗拖成长长一尾，脚边一只搁倒的团扇，晨光从窗棂斜进来
```

## R28 · lying poses fixed by leading with the pose and cutting the base to essentials, with a 2.67:1 canvas; translucency no longer names a body part (R27 glowed orange hands)

- 引擎：`qwen`　尺寸：2048×768　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容, human skin texture,
realistic skin pores, visible pores, matte skin, ordinary human skin, retouched skin,
airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔, pointed ears, elf ears, long pointed ears,
glowing orange ears, animal ears, 尖耳, 精灵耳, smooth featureless skin, uniform flat surface,
completely even skin, waxy flawless surface, 光滑无细节, 死白, 蜡像, heavy stiff fabric,
thick brocade, heavy gold embroidery, dense embroidery, bulky robe, cardboard-stiff
cloth, 厚重布料, 硬挺厚缎, 繁密织金, 笨重,
blush makeup, rouge, blush patches, circular blush, doll-like blush, heavy blush,
applied cosmetics, stiff formal pose, studio pose, standing to
attention, 腮红, 胭脂印, 高原红, 刻意妆容, 端坐, 摆拍,
glowing hands, orange glowing fingers, luminous hands, glowing skin patches, glowing fingertips,
orange light on the hands, 发光的手, 橙色透光的手, 透光发亮的手指, portrait crop,
head and shoulders crop, close-up crop, bust shot
```

### recline-side　seed=2800　（本轮覆盖：2048×768）

产物：`out/r28/bc-r28-recline-side_00001_.png`

```text
全身横构图，一个人躺满整个画面，从发髻到纱罗裙尾全部在画面里：她侧卧在一张长榻上，一手支腮，
另一手随意搭在身侧，数层纱罗铺散在锦垫上，膝上覆着一条薄毯，榻边摊着一卷未读完的书。
Photorealistic image of a living Eastern classical princess resting in her chamber in the
afternoon.
Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half porcelain,
with the faint uneven flush of living skin and fine micro-texture in the glaze.
She wears several layers of weightless translucent gauze, half gauze and half bone china.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

### prone　seed=2810　（本轮覆盖：2048×768）

产物：`out/r28/bc-r28-prone_00001_.png`

```text
全身横构图，一个人伏卧在整张长榻上，从头到脚全部在画面里：她两肘撑着上身，下巴搁在手背上，
小腿在身后轻轻翘起交错，纱罗拖成长长一尾，脚边一只搁倒的团扇。
Photorealistic image of a living Eastern classical princess resting in her chamber in the
afternoon.
Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half porcelain,
with the faint uneven flush of living skin and fine micro-texture in the glaze.
She wears several layers of weightless translucent gauze, half gauze and half bone china.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

### seated-daybed　seed=2820　（本轮覆盖：1200×1600）

产物：`out/r28/bc-r28-seated-daybed_00001_.png`

```text
全身像，一个人坐在矮榻上，自顶至底全身入画，不裁脚不裁手：她一条腿屈起，手肘支在隐囊上，一手托腮，
懒懒望向窗外，纱罗的衣袂垂落榻沿，榻边几上一盏半凉的茶。
Photorealistic image of a living Eastern classical princess resting in her chamber in the
afternoon.
Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half porcelain,
with the faint uneven flush of living skin and fine micro-texture in the glaze.
She wears several layers of weightless translucent gauze, half gauze and half bone china.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

## R29 · closing round: three more languid daily moments on the R28 formula (pose first, short base, canvas shaped to the pose), with the crossed collar, jade-pearl necklace and jade belt restored

- 引擎：`qwen`　尺寸：2048×768　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容, human skin texture,
realistic skin pores, visible pores, matte skin, ordinary human skin, retouched skin,
airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔, pointed ears, elf ears, long pointed ears,
glowing orange ears, animal ears, 尖耳, 精灵耳, smooth featureless skin, uniform flat surface,
completely even skin, waxy flawless surface, 光滑无细节, 死白, 蜡像, heavy stiff fabric,
thick brocade, heavy gold embroidery, dense embroidery, bulky robe, cardboard-stiff
cloth, 厚重布料, 硬挺厚缎, 繁密织金, 笨重,
blush makeup, rouge, blush patches, circular blush, doll-like blush, heavy blush,
applied cosmetics, stiff formal pose, studio pose, standing to
attention, 腮红, 胭脂印, 高原红, 刻意妆容, 端坐, 摆拍,
glowing hands, orange glowing fingers, luminous hands, glowing skin patches, glowing fingertips,
orange light on the hands, 发光的手, 橙色透光的手, 透光发亮的手指, portrait crop,
head and shoulders crop, close-up crop, bust shot
```

### propped-bolster　seed=2900　（本轮覆盖：2048×768）

产物：`out/r29/bc-r29-propped-bolster_00001_.png`

```text
全身横构图，一个人躺满整个画面，从发髻到脚尖全部在画面里：她半躺在长榻上，背靠着一个大隐囊，
两膝屈起，一手端着茶盏，纱罗从肩头铺散到榻面，裙裾垂落榻沿。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half porcelain,
with the faint uneven flush of living skin and fine micro-texture in the glaze.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

### mat-by-window　seed=2910　（本轮覆盖：1200×1600）

产物：`out/r29/bc-r29-mat-by-window_00001_.png`

```text
全身像，一个人坐在窗边的席垫上，自顶至底全身入画，不裁脚不裁手：她抱着膝坐着，下巴搁在膝上，
懒懒望着窗外，纱罗堆叠在身侧的地上，旁边一只矮几，几上一只香炉。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half porcelain,
with the faint uneven flush of living skin and fine micro-texture in the glaze.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

### doze-on-arms　seed=2920　（本轮覆盖：2048×768）

产物：`out/r29/bc-r29-doze-on-arms_00001_.png`

```text
全身横构图，一个人伏在案上打盹，从头到脚全身在画面里：她坐在案前，上身伏下，头枕在自己的臂弯里，
长发散落案面，数层纱罗从椅背垂下，案上一卷摊开的书与一只茶盏。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half porcelain,
with the faint uneven flush of living skin and fine micro-texture in the glaze.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

## R30 · recover the bone-china skin lost in phase 5: put the phase-4 named glaze-defect inventory back into the pose-first short base, changing nothing else; shots 1-2 reuse R29's pose text verbatim for a direct A/B

- 引擎：`qwen`　尺寸：2048×768　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容, human skin texture,
realistic skin pores, visible pores, matte skin, ordinary human skin, retouched skin,
airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔, pointed ears, elf ears, long pointed ears,
glowing orange ears, animal ears, 尖耳, 精灵耳, smooth featureless skin, uniform flat surface,
completely even skin, waxy flawless surface, 光滑无细节, 死白, 蜡像, heavy stiff fabric,
thick brocade, heavy gold embroidery, dense embroidery, bulky robe, cardboard-stiff
cloth, 厚重布料, 硬挺厚缎, 繁密织金, 笨重,
blush makeup, rouge, blush patches, circular blush, doll-like blush, heavy blush,
applied cosmetics, stiff formal pose, studio pose, standing to
attention, 腮红, 胭脂印, 高原红, 刻意妆容, 端坐, 摆拍,
glowing hands, orange glowing fingers, luminous hands, glowing skin patches, glowing fingertips,
orange light on the hands, 发光的手, 橙色透光的手, 透光发亮的手指, portrait crop,
head and shoulders crop, close-up crop, bust shot
```

### propped-bolster　seed=3000　（本轮覆盖：2048×768）

产物：`out/r30/bc-r30-propped-bolster_00001_.png`

```text
全身横构图，一个人躺满整个画面，从发髻到脚尖全部在画面里：她半躺在长榻上，背靠着一个大隐囊，
两膝屈起，一手端着茶盏，纱罗从肩头铺散到榻面，裙裾垂落榻沿。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half porcelain,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

### mat-by-window　seed=3010　（本轮覆盖：1200×1600）

产物：`out/r30/bc-r30-mat-by-window_00001_.png`

```text
全身像，一个人坐在窗边的席垫上，自顶至底全身入画，不裁脚不裁手：她抱着膝坐着，下巴搁在膝上，
懒懒望着窗外，纱罗堆叠在身侧的地上，旁边一只矮几，几上一只香炉。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half porcelain,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

### square-plate　seed=3020　（本轮覆盖：1600×1600）

产物：`out/r30/bc-r30-square-plate_00001_.png`

```text
全身像，一个人斜坐在矮榻上，自顶至底全身入画，不裁脚不裁手：她一腿屈起，一手托腮，
另一手搁在膝上端着茶盏，纱罗一层层垂落榻沿堆在地上，榻边一只香炉一缕青烟。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
Her skin is bone china -- ivory porcelain under a fired glaze, half real skin and half porcelain,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

## R31 · restore the specular-highlight clause R30 left out, and judge it on a tight portrait plate (R30's square plate was a full body, too few pixels on the face); shot 1 is a same-seed single-variable ablation against R29 mat-by-window

- 引擎：`qwen`　尺寸：2048×768　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容, human skin texture,
realistic skin pores, visible pores, matte skin, ordinary human skin, retouched skin,
airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔, pointed ears, elf ears, long pointed ears,
glowing orange ears, animal ears, 尖耳, 精灵耳, smooth featureless skin, uniform flat surface,
completely even skin, waxy flawless surface, 光滑无细节, 死白, 蜡像, heavy stiff fabric,
thick brocade, heavy gold embroidery, dense embroidery, bulky robe, cardboard-stiff
cloth, 厚重布料, 硬挺厚缎, 繁密织金, 笨重,
blush makeup, rouge, blush patches, circular blush, doll-like blush, heavy blush,
applied cosmetics, stiff formal pose, studio pose, standing to
attention, 腮红, 胭脂印, 高原红, 刻意妆容, 端坐, 摆拍,
glowing hands, orange glowing fingers, luminous hands, glowing skin patches, glowing fingertips,
orange light on the hands, 发光的手, 橙色透光的手, 透光发亮的手指, portrait crop,
head and shoulders crop, close-up crop, bust shot
```

### ablation-window　seed=2910　（本轮覆盖：1200×1600）

产物：`out/r31/bc-r31-ablation-window_00001_.png`

```text
全身像，一个人坐在窗边的席垫上，自顶至底全身入画，不裁脚不裁手：她抱着膝坐着，下巴搁在膝上，
懒懒望着窗外，纱罗堆叠在身侧的地上，旁边一只矮几，几上一只香炉。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
Her skin is bone china -- ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes, half real skin and half porcelain,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

### skin-square　seed=2520　（本轮覆盖：2048×2048）

产物：`out/r31/bc-r31-skin-square_00001_.png`

```text
紧肖像，半身近景，自头顶到胸前入画，脸占画面大部分：她侧过脸来迎着窗光，一只手抬起轻触面颊，
纱罗松松搭在肩上，背景是虚化的窗棂与屏风。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
Her skin is bone china -- ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes, half real skin and half porcelain,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

### portrait　seed=3030　（本轮覆盖：1280×1712）

产物：`out/r31/bc-r31-portrait_00001_.png`

```text
肖像，四分之三身，自头顶到腰际入画：她端坐在矮榻上，一手搁在膝边的茶盏旁，微微侧头望向窗外，
纱罗从肩头垂落。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
Her skin is bone china -- ivory porcelain under a fired glaze,
with crisp specular highlights where the light strikes, half real skin and half porcelain,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

## R32 · swap the material assertion from 'half real skin and half porcelain' to R25's proven 'made of bone china -- the material itself, not a mask' + 'Her face is human; her skin is porcelain.'; every shot mirrors R31's name/seed/size/negative for an exact A/B

- 引擎：`qwen`　尺寸：2048×768　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容, human skin texture,
realistic skin pores, visible pores, matte skin, ordinary human skin, retouched skin,
airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔, pointed ears, elf ears, long pointed ears,
glowing orange ears, animal ears, 尖耳, 精灵耳, smooth featureless skin, uniform flat surface,
completely even skin, waxy flawless surface, 光滑无细节, 死白, 蜡像, heavy stiff fabric,
thick brocade, heavy gold embroidery, dense embroidery, bulky robe, cardboard-stiff
cloth, 厚重布料, 硬挺厚缎, 繁密织金, 笨重,
blush makeup, rouge, blush patches, circular blush, doll-like blush, heavy blush,
applied cosmetics, stiff formal pose, studio pose, standing to
attention, 腮红, 胭脂印, 高原红, 刻意妆容, 端坐, 摆拍,
glowing hands, orange glowing fingers, luminous hands, glowing skin patches, glowing fingertips,
orange light on the hands, 发光的手, 橙色透光的手, 透光发亮的手指, portrait crop,
head and shoulders crop, close-up crop, bust shot
```

### ablation-window　seed=2910　（本轮覆盖：1200×1600）

产物：`out/r32/bc-r32-ablation-window_00001_.png`

```text
全身像，一个人坐在窗边的席垫上，自顶至底全身入画，不裁脚不裁手：她抱着膝坐着，下巴搁在膝上，
懒懒望着窗外，纱罗堆叠在身侧的地上，旁边一只矮几，几上一只香炉。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
Her skin is made of bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

### skin-square　seed=2520　（本轮覆盖：2048×2048）

产物：`out/r32/bc-r32-skin-square_00001_.png`

```text
紧肖像，半身近景，自头顶到胸前入画，脸占画面大部分：她侧过脸来迎着窗光，一只手抬起轻触面颊，
纱罗松松搭在肩上，背景是虚化的窗棂与屏风。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
Her skin is made of bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

### portrait　seed=3030　（本轮覆盖：1280×1712）

产物：`out/r32/bc-r32-portrait_00001_.png`

```text
肖像，四分之三身，自头顶到腰际入画：她端坐在矮榻上，一手搁在膝边的茶盏旁，微微侧头望向窗外，
纱罗从肩头垂落。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
Her skin is made of bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。肌肤半真半骨瓷：
骨瓷的釉面与莹润半透，血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱
罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数。中画幅相机，50mm 镜头，f/2.8，浅景深，
自然颗粒，无数字锐化
```

## R33 · restore the missing face/bearing block (phase-2's proven face clause + an explicit youth band + Chinese bearing lines) and drop the blanket blush bans so the faintest soft blush can render; shots mirror R32's seeds/sizes for a direct A/B

- 引擎：`qwen`　尺寸：2048×768　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容, human skin texture,
realistic skin pores, visible pores, matte skin, ordinary human skin, retouched skin,
airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔, pointed ears, elf ears, long pointed ears,
glowing orange ears, animal ears, 尖耳, 精灵耳, smooth featureless skin, uniform flat surface,
completely even skin, waxy flawless surface, 光滑无细节, 死白, 蜡像, heavy stiff fabric,
thick brocade, heavy gold embroidery, dense embroidery, bulky robe, cardboard-stiff
cloth, 厚重布料, 硬挺厚缎, 繁密织金, 笨重,
blush makeup, rouge, blush patches, circular blush, doll-like blush, heavy blush,
applied cosmetics, stiff formal pose, studio pose, standing to
attention, 腮红, 胭脂印, 高原红, 刻意妆容, 端坐, 摆拍,
glowing hands, orange glowing fingers, luminous hands, glowing skin patches, glowing fingertips,
orange light on the hands, 发光的手, 橙色透光的手, 透光发亮的手指, portrait crop,
head and shoulders crop, close-up crop, bust shot
```

### ablation-window　seed=2910　（本轮覆盖：1200×1600）

产物：`out/r33/bc-r33-ablation-window_00001_.png`

```text
全身像，一个人坐在窗边的席垫上，自顶至底全身入画，不裁脚不裁手：她抱着膝坐着，下巴搁在膝上，
懒懒望着窗外，纱罗堆叠在身侧的地上，旁边一只矮几，几上一只香炉。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush -- a young woman, refined and fresh-faced, never matronly and never severe.
Her skin is made of bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。虽在闲居，
气度仍在：肩背挺秀，下颌微收，目光清亮，一份矜贵自持。肌肤半真半骨瓷：骨瓷的釉面与莹润半透，
血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数，却自带一份矜贵。中画幅相机，50mm 镜头，
f/2.8，浅景深，自然颗粒，无数字锐化
```

### skin-square　seed=2520　（本轮覆盖：2048×2048）

产物：`out/r33/bc-r33-skin-square_00001_.png`

```text
紧肖像，半身近景，自头顶到胸前入画，脸占画面大部分：她侧过脸来迎着窗光，一只手抬起轻触面颊，
纱罗松松搭在肩上，背景是虚化的窗棂与屏风。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush -- a young woman, refined and fresh-faced, never matronly and never severe.
Her skin is made of bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。虽在闲居，
气度仍在：肩背挺秀，下颌微收，目光清亮，一份矜贵自持。肌肤半真半骨瓷：骨瓷的釉面与莹润半透，
血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数，却自带一份矜贵。中画幅相机，50mm 镜头，
f/2.8，浅景深，自然颗粒，无数字锐化
```

### portrait　seed=3030　（本轮覆盖：1280×1712）

产物：`out/r33/bc-r33-portrait_00001_.png`

```text
肖像，四分之三身，自头顶到腰际入画：她端坐在矮榻上，一手搁在膝边的茶盏旁，微微侧头望向窗外，
纱罗从肩头垂落。
Photorealistic image of a living Eastern classical princess at home in her chamber in the
afternoon.
An elegant princess face with refined adult proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush -- a young woman, refined and fresh-faced, never matronly and never severe.
Her skin is made of bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。虽在闲居，
气度仍在：肩背挺秀，下颌微收，目光清亮，一份矜贵自持。肌肤半真半骨瓷：骨瓷的釉面与莹润半透，
血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数，却自带一份矜贵。中画幅相机，50mm 镜头，
f/2.8，浅景深，自然颗粒，无数字锐化
```

## R34 · anchor the age early and hard (young princess / youthful proportions / early twenties / dewy skin) and add anti-ageing terms to the negative; shots mirror R33's seeds/sizes for a direct A/B

- 引擎：`qwen`　尺寸：2048×768　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容, human skin texture,
realistic skin pores, visible pores, matte skin, ordinary human skin, retouched skin,
airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔, pointed ears, elf ears, long pointed ears,
glowing orange ears, animal ears, 尖耳, 精灵耳, smooth featureless skin, uniform flat surface,
completely even skin, waxy flawless surface, 光滑无细节, 死白, 蜡像, heavy stiff fabric,
thick brocade, heavy gold embroidery, dense embroidery, bulky robe, cardboard-stiff
cloth, 厚重布料, 硬挺厚缎, 繁密织金, 笨重,
blush makeup, rouge, blush patches, circular blush, doll-like blush, heavy blush,
applied cosmetics, stiff formal pose, studio pose, standing to
attention, 腮红, 胭脂印, 高原红, 刻意妆容, 端坐, 摆拍,
glowing hands, orange glowing fingers, luminous hands, glowing skin patches, glowing fingertips,
orange light on the hands, 发光的手, 橙色透光的手, 透光发亮的手指, portrait crop,
head and shoulders crop, close-up crop, bust shot
```

### ablation-window　seed=2910　（本轮覆盖：1200×1600）

产物：`out/r34/bc-r34-ablation-window_00001_.png`

```text
全身像，一个人坐在窗边的席垫上，自顶至底全身入画，不裁脚不裁手：她抱着膝坐着，下巴搁在膝上，
懒懒望着窗外，纱罗堆叠在身侧的地上，旁边一只矮几，几上一只香炉。
Photorealistic image of a young living Eastern classical princess at home in her chamber in the
afternoon.
An elegant young princess face with refined youthful proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush -- a young woman in her early twenties, refined and fresh-faced,
with dewy clear skin, never matronly and never severe.
Her skin is made of bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。虽在闲居，
气度仍在：肩背挺秀，下颌微收，目光清亮，一份矜贵自持。肌肤半真半骨瓷：骨瓷的釉面与莹润半透，
血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数，却自带一份矜贵。中画幅相机，50mm 镜头，
f/2.8，浅景深，自然颗粒，无数字锐化
```

### skin-square　seed=2520　（本轮覆盖：2048×2048）

产物：`out/r34/bc-r34-skin-square_00001_.png`

```text
紧肖像，半身近景，自头顶到胸前入画，脸占画面大部分：她侧过脸来迎着窗光，一只手抬起轻触面颊，
纱罗松松搭在肩上，背景是虚化的窗棂与屏风。
Photorealistic image of a young living Eastern classical princess at home in her chamber in the
afternoon.
An elegant young princess face with refined youthful proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush -- a young woman in her early twenties, refined and fresh-faced,
with dewy clear skin, never matronly and never severe.
Her skin is made of bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。虽在闲居，
气度仍在：肩背挺秀，下颌微收，目光清亮，一份矜贵自持。肌肤半真半骨瓷：骨瓷的釉面与莹润半透，
血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数，却自带一份矜贵。中画幅相机，50mm 镜头，
f/2.8，浅景深，自然颗粒，无数字锐化
```

### portrait　seed=3030　（本轮覆盖：1280×1712）

产物：`out/r34/bc-r34-portrait_00001_.png`

```text
肖像，四分之三身，自头顶到腰际入画：她端坐在矮榻上，一手搁在膝边的茶盏旁，微微侧头望向窗外，
纱罗从肩头垂落。
Photorealistic image of a young living Eastern classical princess at home in her chamber in the
afternoon.
An elegant young princess face with refined youthful proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush -- a young woman in her early twenties, refined and fresh-faced,
with dewy clear skin, never matronly and never severe.
Her skin is made of bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。虽在闲居，
气度仍在：肩背挺秀，下颌微收，目光清亮，一份矜贵自持。肌肤半真半骨瓷：骨瓷的釉面与莹润半透，
血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数，却自带一份矜贵。中画幅相机，50mm 镜头，
f/2.8，浅景深，自然颗粒，无数字锐化
```

## R35 · drop the anti-ageing negative words R34 added and change nothing else: test whether they were suppressing the fired-glaze surface (R25 proves the defect inventory is compatible with a young glazed face)

- 引擎：`qwen`　尺寸：2048×768　steps：32　cfg：3.5
- 张数：3（每张独立请求，seed 各自独立）

**负向 prompt（全轮共用）**

```text
cracks, crazing, crackle pattern, broken, damaged, chipped, dirty, dust, stains, plastic, vinyl,
waxy skin, cartoon, anime, chibi, toy-like proportions, oversized eyes, blurry, low detail,
low resolution, oversaturated, harsh flash, cgi, 3d render, extra limbs, extra fingers,
deformed hands, floating objects, text, watermark, signature, logo, busy background, doll,
figurine, ball-jointed doll, ball joint, joint seam, articulated joint, mannequin, display stand,
pedestal, plinth, museum display case, toy, plastic figure,
statue, 人偶, 娃娃, 球形关节, 关节缝, 摆件, 展台, 陈列柜, 底座, 玩具, 雕像,
heavy makeup, bright red lipstick, painted-on eyebrows, modern cosmetics, cosplay,
studio glamour shot, retouched beauty shot, 浓妆, 艳妆, 影楼, 网红妆, 现代妆容, human skin texture,
realistic skin pores, visible pores, matte skin, ordinary human skin, retouched skin,
airbrushed skin, 真人皮肤, 哑光皮肤, 毛孔, pointed ears, elf ears, long pointed ears,
glowing orange ears, animal ears, 尖耳, 精灵耳, smooth featureless skin, uniform flat surface,
completely even skin, waxy flawless surface, 光滑无细节, 死白, 蜡像, heavy stiff fabric,
thick brocade, heavy gold embroidery, dense embroidery, bulky robe, cardboard-stiff
cloth, 厚重布料, 硬挺厚缎, 繁密织金, 笨重,
blush makeup, rouge, blush patches, circular blush, doll-like blush, heavy blush,
applied cosmetics, stiff formal pose, studio pose, standing to
attention, 腮红, 胭脂印, 高原红, 刻意妆容, 端坐, 摆拍,
glowing hands, orange glowing fingers, luminous hands, glowing skin patches, glowing fingertips,
orange light on the hands, 发光的手, 橙色透光的手, 透光发亮的手指, portrait crop,
head and shoulders crop, close-up crop, bust shot
```

### ablation-window　seed=2910　（本轮覆盖：1200×1600）

产物：`out/r35/bc-r35-ablation-window_00001_.png`

```text
全身像，一个人坐在窗边的席垫上，自顶至底全身入画，不裁脚不裁手：她抱着膝坐着，下巴搁在膝上，
懒懒望着窗外，纱罗堆叠在身侧的地上，旁边一只矮几，几上一只香炉。
Photorealistic image of a young living Eastern classical princess at home in her chamber in the
afternoon.
An elegant young princess face with refined youthful proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush -- a young woman in her early twenties, refined and fresh-faced,
with dewy clear skin, never matronly and never severe.
Her skin is made of bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。虽在闲居，
气度仍在：肩背挺秀，下颌微收，目光清亮，一份矜贵自持。肌肤半真半骨瓷：骨瓷的釉面与莹润半透，
血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数，却自带一份矜贵。中画幅相机，50mm 镜头，
f/2.8，浅景深，自然颗粒，无数字锐化
```

### skin-square　seed=2520　（本轮覆盖：2048×2048）

产物：`out/r35/bc-r35-skin-square_00001_.png`

```text
紧肖像，半身近景，自头顶到胸前入画，脸占画面大部分：她侧过脸来迎着窗光，一只手抬起轻触面颊，
纱罗松松搭在肩上，背景是虚化的窗棂与屏风。
Photorealistic image of a young living Eastern classical princess at home in her chamber in the
afternoon.
An elegant young princess face with refined youthful proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush -- a young woman in her early twenties, refined and fresh-faced,
with dewy clear skin, never matronly and never severe.
Her skin is made of bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。虽在闲居，
气度仍在：肩背挺秀，下颌微收，目光清亮，一份矜贵自持。肌肤半真半骨瓷：骨瓷的釉面与莹润半透，
血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数，却自带一份矜贵。中画幅相机，50mm 镜头，
f/2.8，浅景深，自然颗粒，无数字锐化
```

### portrait　seed=3030　（本轮覆盖：1280×1712）

产物：`out/r35/bc-r35-portrait_00001_.png`

```text
肖像，四分之三身，自头顶到腰际入画：她端坐在矮榻上，一手搁在膝边的茶盏旁，微微侧头望向窗外，
纱罗从肩头垂落。
Photorealistic image of a young living Eastern classical princess at home in her chamber in the
afternoon.
An elegant young princess face with refined youthful proportions: oval face, high cheekbones,
straight nose bridge, serene closed lips, almond eyes of realistic size with a subtle crease,
individually painted eyelashes, eyebrows painted hair by hair,
the faintest soft blush -- a young woman in her early twenties, refined and fresh-faced,
with dewy clear skin, never matronly and never severe.
Her skin is made of bone china -- the material itself, not a mask:
ivory porcelain under a fired glaze, with crisp specular highlights where the light strikes,
with the faint uneven flush of living skin,
and above all a REAL fired surface rather than a smooth render:
microscopic pinholes where the glaze pulled back,
tiny trapped bubbles and blisters under the glaze, faint polishing marks and hairline drag lines,
a fine orange-peel ripple, glaze that is very slightly uneven in thickness and in colour,
a few tiny specks of kiln grit -- real variation everywhere, never a uniform flat surface,
absolutely no CGI smoothness and no plastic.
Her face is human; her skin is porcelain.
She wears several layers of weightless translucent gauze over an ivory silk robe with a crossed
collar,
half gauze and half bone china, with a jade-and-pearl necklace and a jade-inlaid belt.
Her hair is loosely pinned with a gold filigree hairpin, makeup barely
there. 东方古典公主在内室里消磨午后时光的写实画面。虽在闲居，
气度仍在：肩背挺秀，下颌微收，目光清亮，一份矜贵自持。肌肤半真半骨瓷：骨瓷的釉面与莹润半透，
血色自里透出、深浅不匀，自然得很，釉面有极细的缩釉点与磨痕。身上是数层极轻的纱罗，
罩在象牙色交领细绢之上，薄如蝉翼，半纱半骨瓷，衣襟齐整却穿得松泛，袖口松松滑落；
颈上一条赤金盘螭璎珞圈，腰间一条金镶玉带。青丝松松绾着，一支金累丝衔珠凤钗斜斜插着，
鬓边散下几缕碎发。妆极淡，近乎素面。神态慵懒闲适，不拘礼数，却自带一份矜贵。中画幅相机，50mm 镜头，
f/2.8，浅景深，自然颗粒，无数字锐化
```

