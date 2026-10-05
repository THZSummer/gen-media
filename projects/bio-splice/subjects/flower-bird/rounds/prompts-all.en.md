# Archive of Raw Prompts for All Rounds

> 🌐 Language: **English** | [中文](prompts-all.md)

> This file is generated automatically by `python3 run_round.py --prompts`; its content = **the exact strings actually submitted to ComfyUI**.
> For easy reading and round-by-round comparison, the code blocks are wrapped at clause boundaries; **the newlines are not part of the prompt, they are layout only**.
> Unwrapping rule: when a line ends with an ASCII character, that newline equals one space; otherwise there was no character at the wrap point originally.
> `run_round.py`'s `unwrap_prompt()` implements exactly this rule, and generation asserts item by item that "unwrapped == original".
> The verbatim original (single line) is in the constants of `run_round.py` (`python3 run_round.py <N> --dry` prints it directly)
> and in `work/rN/round.json`; the final authority is the server's `GET /history/{prompt_id}`.
> To change a prompt, edit `subjects/<子主题>/rounds.py`, then regenerate this file.
> Back to [subject home](../README.en.md) ｜ [project home](../../../README.en.md)

## Where it is recorded (three layers)

| Layer | Location | Content |
|----|------|------|
| Authoritative source | `subjects/<子主题>/rounds.py` | the verbatim prompt (what is really sent, single line) |
| Human-readable doc | this file / `docs/rN.md` | the full prompt wrapped at clause boundaries; per-round changes and self-checks |
| Machine record | `work/rN/round.json` | filename / seed / prompt_id / engine / parameters / **the verbatim prompt** |
| Server side | `GET /history/{prompt_id}` | the complete graph ComfyUI actually executed (final authority) |

## R1 · Flower-bird · Phase 1 candidates: the base frees the petal ring + three ways of wording the bird feathers; includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 11101
- Image count: 4 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-feathers-rel　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with broad pale bird feathers in place of the petals,
a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-feathers-ring　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with a ring of broad pale bird feathers, a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-feathers-coat　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with broad pale bird feathers covering the flower,
a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R2 · Flower-bird · Phase 1 control [occupied version]: the base writes the petals as usual + bird feathers; includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 11101
- Image count: 2 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with broad rounded petals and a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-feathers　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with a ring of broad pale bird feathers,
broad rounded petals and a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R3 · Flower-bird · Phase 2 candidates [the flower with a downy centre]: the base frees the flower centre + down feathers P5; includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 11101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with broad rounded petals.
on a spring branch, dew on the petals.
raking side light picking out the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-down　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with a tuft of soft downy bird feathers in the centre of the flower,
broad rounded petals.
on a spring branch, dew on the petals.
raking side light picking out the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-down-b　seed 11102

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with a tuft of soft downy bird feathers in the centre of the flower,
broad rounded petals.
on a spring branch, dew on the petals.
raking side light picking out the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R4 · Flower-bird · Phase 3 candidates [the flower with a plume stalk]: base + plume feathers P6 (growing from the flower stalk); includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 11101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a large white magnolia flower with broad rounded petals and a ring of pale stamens.
on a spring branch among new leaves.
soft light against a dark background.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem,
broad rounded petals and a ring of pale stamens.
on a spring branch among new leaves.
soft light against a dark background.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume-b　seed 11102

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem,
broad rounded petals and a ring of pale stamens.
on a spring branch among new leaves.
soft light against a dark background.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R5 · Phase 01 final [the plumed branch]: magnolia + plume feathers P6 (three seeds); morning-dew soft light, macro; includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 11101
- Image count: 4 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with broad rounded petals and a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem,
broad rounded petals and a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume-b　seed 11102

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem,
broad rounded petals and a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume-c　seed 11103

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem,
broad rounded petals and a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R6 · Phase 03 final [both plumes and down]: magnolia + plume feathers P6 + down feathers P5 (two takes); dark background, hard light

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 11101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with broad rounded petals and a ring of pale stamens.
against a dark blurred background of twigs.
hard light from one side, the background falling to near-black.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume-down　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem and a tuft of
soft downy bird feathers in the centre of the flower,
broad rounded petals and a ring of pale stamens.
against a dark blurred background of twigs.
hard light from one side, the background falling to near-black.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume-down-b　seed 11102

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem and a tuft of
soft downy bird feathers in the centre of the flower,
broad rounded petals and a ring of pale stamens.
against a dark blurred background of twigs.
hard light from one side, the background falling to near-black.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R7 · Phase 04 final [the lily's down and plumes]: lily base + down feathers P5 + plume feathers P6 (two takes); backlight, portrait format

- Engine: `zimage`　Size: 1024×1280　steps: 12　Shared seed: 11101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### lily-down-plume　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with a tuft of soft downy bird feathers in the centre of the flower and long
pale bird plume feathers rising from the stem,
six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### lily-down-plume-b　seed 11102

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with a tuft of soft downy bird feathers in the centre of the flower and long
pale bird plume feathers rising from the stem,
six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R8 · Phase 05 finale [flower-bird]: magnolia + plume feathers P6 + down feathers P5 (two takes); a full branch in backlight, wide angle, landscape

- Engine: `zimage`　Size: 1280×1024　steps: 12　Shared seed: 11101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：一枝上开着好几朵、整体朝向镜头：
a large white magnolia flower with broad rounded petals and a ring of pale stamens.
a whole flowering branch in a spring grove.
warm low backlight, the plumes glowing.
a wide macro view, 45mm lens at f/11, macro photograph, fine surface detail, soft natural colour,
no digital sharpening, no text, no watermark.
```

### flower-bird　seed 11101

```text
微距特写，一个生物体独自占据画面：一枝上开着好几朵、整体朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem and a tuft of
soft downy bird feathers in the centre of the flower,
broad rounded petals and a ring of pale stamens.
a whole flowering branch in a spring grove.
warm low backlight, the plumes glowing.
a wide macro view, 45mm lens at f/11, macro photograph, fine surface detail, soft natural colour,
no digital sharpening, no text, no watermark.
```

### flower-bird-b　seed 11102

```text
微距特写，一个生物体独自占据画面：一枝上开着好几朵、整体朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem and a tuft of
soft downy bird feathers in the centre of the flower,
broad rounded petals and a ring of pale stamens.
a whole flowering branch in a spring grove.
warm low backlight, the plumes glowing.
a wide macro view, 45mm lens at f/11, macro photograph, fine surface detail, soft natural colour,
no digital sharpening, no text, no watermark.
```

## R9 · Phase 04 final (extra take) [the lily's down and plumes]: lily base + down feathers P5 + plume feathers P6 (three seeds); includes a same-round base control

- Engine: `zimage`　Size: 1024×1280　steps: 12　Shared seed: 11101
- Image count: 4 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### lily-down-plume　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with a tuft of soft downy bird feathers in the centre of the flower and long
pale bird plume feathers rising from the stem,
six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### lily-down-plume-c　seed 11103

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with a tuft of soft downy bird feathers in the centre of the flower and long
pale bird plume feathers rising from the stem,
six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### lily-down-plume-d　seed 11104

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with a tuft of soft downy bird feathers in the centre of the flower and long
pale bird plume feathers rising from the stem,
six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

