# All Rounds · Raw Prompt Archive

> 🌐 Language: **English** | [中文](prompts-all.md)

> This file is generated automatically by `python3 run_round.py --prompts`; its content = **the string actually submitted to ComfyUI**.
> For easier reading and round-by-round comparison, the code blocks are broken at sentence boundaries; **the line breaks are not part of the prompt, they are layout only**.
> Unwrapping rule: when the end of a line is an ASCII character, that line break equals one space; otherwise there was no character at the break to begin with.
> `run_round.py`'s `unwrap_prompt()` is exactly this rule, and generation asserts "unwrap == original" for every entry.
> The verbatim original (single line) is in the constants of `run_round.py` (`python3 run_round.py <N> --dry` prints it directly)
> and in `work/rN/round.json`; the final authority is the server's `GET /history/{prompt_id}`.
> To change a prompt, edit `subjects/<子主题>/rounds.py` and then regenerate this file.
> Back to the [sub-theme home page](../README.en.md) ｜ [project home page](../../../README.en.md)

## Where It Is Recorded (three layers)

| Layer | Location | Content |
|----|------|------|
| Authoritative source | `subjects/<子主题>/rounds.py` | the verbatim prompt (what is really sent out, single line) |
| Readable document | this file / `docs/rN.md` | the full prompt with sentence line breaks; each round's changes and self-checks |
| Machine record | `work/rN/round.json` | filename / seed / prompt_id / engine / parameters / **prompt verbatim** |
| Server side | `GET /history/{prompt_id}` | the complete graph ComfyUI actually executed (the final authority) |

## R1 · kun-peng · period 01 candidates: fish base (pectoral-fin slot freed) + three phrasings for bird wings; includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 6101
- Images: 4 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with a long scaled body, a blunt head, small eyes,
a dorsal fin and a broad forked tail.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with broad feathered bird wings on both sides of its body, a long scaled body,
a blunt head, small eyes, a dorsal fin and a broad forked tail.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-flank　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with a pair of broad feathered bird wings along its flanks, a long scaled body,
a blunt head, small eyes, a dorsal fin and a broad forked tail.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-rel　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with broad feathered bird wings in place of its pectoral fins,
a long scaled body, a blunt head, small eyes, a dorsal fin and a broad forked tail.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R2 · kun-peng · period 02 candidates: fish base (tail-fin slot freed) + two phrasings for bird tail feathers; includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 6101
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它悬在水中、身侧朝向镜头：a large wild carp with a long scaled body,
a blunt head, small eyes and four fins.
in dark water a little below the surface.
backlight coming down through the surface.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-tailfeathers　seed 6101

```text
全身像，一只动物独自占据画面：它悬在水中、身侧朝向镜头：
a large wild carp with a fan of long bird tail feathers, a long scaled body, a blunt head,
small eyes and four fins.
in dark water a little below the surface.
backlight coming down through the surface.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-tailfeathers-rel　seed 6101

```text
全身像，一只动物独自占据画面：它悬在水中、身侧朝向镜头：
a large wild carp with long bird tail feathers spreading where the tail fin would be,
a long scaled body, a blunt head, small eyes and four fins.
in dark water a little below the surface.
backlight coming down through the surface.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R3 · kun-peng · empty-slot probe: wings growing from the back / tail feathers spreading above the tail / feathers covering the back (the same base); includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 6101
- Images: 4 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with a long scaled body, a blunt head, small eyes and a dorsal fin.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-back　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with a pair of broad feathered bird wings rising from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-tail-above　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with a fan of long bird tail feathers rising above its tail, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-feathercoat　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with a covering of fine bird feathers over its back, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R4 · kun-peng · out-of-water probe: the same fish base + the same three parts, with only the scene moved above the water; includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 6101
- Images: 4 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：a large wild carp with a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-back　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with a pair of broad feathered bird wings rising from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with broad feathered bird wings on both sides of its body, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-feathercoat　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with a covering of fine bird feathers over its back, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R5 · kun-peng · out-of-water fill-in: tail feathers (at the tail / above the tail) / feathers covering the back / wings + tail feathers stacked; includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 6101
- Images: 5 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：a large wild carp with a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-tail　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with a fan of long bird tail feathers, a long scaled body, a blunt head,
small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-tail-above　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with a fan of long bird tail feathers rising above its tail, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-feathercoat　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with a covering of fine bird feathers over its back, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-tail　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with broad feathered bird wings on both sides of its body and a fan of long bird
tail feathers,
a long scaled body, a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R6 · period 01 final [leaping out of the water · splash not yet fallen]: fish + bird wings (two takes); includes the same-round base control

- Engine: `zimage`　Size: 1280×1024　steps: 12　shared seed: 6101
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它刚从水里跃出、身体还在往上冲：
a large wild carp with a long scaled body, a blunt head, small eyes and a dorsal fin.
in open air just above the surface, spray still falling from its body.
low backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings　seed 6101

```text
全身像，一只动物独自占据画面：它刚从水里跃出、身体还在往上冲：
a large wild carp with broad feathered bird wings on both sides of its body, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air just above the surface, spray still falling from its body.
low backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-spread　seed 6102

```text
全身像，一只动物独自占据画面：它刚从水里跃出、身体还在往上冲：
a large wild carp with a pair of broad feathered bird wings spread wide from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
in open air just above the surface, spray still falling from its body.
low backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R7 · period 02 final [half out of water · waterline crossing the body]: fish + bird wings (two takes); includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 6101
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with a long scaled body, a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings　seed 6101

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with broad feathered bird wings on both sides of its body, a long scaled body,
a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-half　seed 6103

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with a pair of broad feathered bird wings half-opened along its flanks,
a long scaled body, a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R8 · period 03 final [fully clear of the water · both wings spread · high-side view]: fish + bird wings (two takes); includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 6101
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它悬在空中、身体横向展开：a large wild carp with a long scaled body,
a blunt head, small eyes and a dorsal fin.
well above the water, only sky and a distant shoreline behind it.
strong backlight rimming every feather.
Photograph, a view from slightly above and to the side, 85mm lens at f/5.6, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-spread　seed 6101

```text
全身像，一只动物独自占据画面：它悬在空中、身体横向展开：
a large wild carp with a pair of broad feathered bird wings spread wide from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
well above the water, only sky and a distant shoreline behind it.
strong backlight rimming every feather.
Photograph, a view from slightly above and to the side, 85mm lens at f/5.6, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-spread-b　seed 6102

```text
全身像，一只动物独自占据画面：它悬在空中、身体横向展开：
a large wild carp with a pair of broad feathered bird wings spread wide from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
well above the water, only sky and a distant shoreline behind it.
strong backlight rimming every feather.
Photograph, a view from slightly above and to the side, 85mm lens at f/5.6, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R9 · period 04 final [skimming low over the water · long-lens compression]: fish + bird wings (two takes); includes the same-round base control

- Engine: `zimage`　Size: 1280×1024　steps: 12　shared seed: 6101
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它贴着水面低飞、身体近乎水平：
a large wild carp with a long scaled body, a blunt head, small eyes and a dorsal fin.
skimming low over open water, the far shore compressed behind it.
flat overcast light on grey water.
Photograph, a 400mm telephoto compressing the distance, f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings　seed 6101

```text
全身像，一只动物独自占据画面：它贴着水面低飞、身体近乎水平：
a large wild carp with broad feathered bird wings on both sides of its body, a long scaled body,
a blunt head, small eyes and a dorsal fin.
skimming low over open water, the far shore compressed behind it.
flat overcast light on grey water.
Photograph, a 400mm telephoto compressing the distance, f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-spread　seed 6103

```text
全身像，一只动物独自占据画面：它贴着水面低飞、身体近乎水平：
a large wild carp with a pair of broad feathered bird wings spread wide from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
skimming low over open water, the far shore compressed behind it.
flat overcast light on grey water.
Photograph, a 400mm telephoto compressing the distance, f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R10 · period 05 finale [kun-peng]: dusk sea-surface backlit silhouette + fully spread bird wings (two takes); includes the same-round base control

- Engine: `zimage`　Size: 1280×1024　steps: 12　shared seed: 6101
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它在暮色海面上高高跃起、双翼全展：
a large wild carp with a long scaled body, a blunt head, small eyes and a dorsal fin.
above a dark open sea at dusk, the horizon far behind.
low backlight throwing the whole animal into near-silhouette.
Photograph, a wide-angle 35mm lens at eye height, f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-spread　seed 6101

```text
全身像，一只动物独自占据画面：它在暮色海面上高高跃起、双翼全展：
a large wild carp with a pair of broad feathered bird wings spread wide from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
above a dark open sea at dusk, the horizon far behind.
low backlight throwing the whole animal into near-silhouette.
Photograph, a wide-angle 35mm lens at eye height, f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-spread-b　seed 6102

```text
全身像，一只动物独自占据画面：它在暮色海面上高高跃起、双翼全展：
a large wild carp with a pair of broad feathered bird wings spread wide from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
above a dark open sea at dusk, the horizon far behind.
low backlight throwing the whole animal into near-silhouette.
Photograph, a wide-angle 35mm lens at eye height, f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R11 · period 02 final (extra take) [half out of water · waterline crossing the body]: the half-open wing placed high on the flank (three seeds); includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 6101
- Images: 4 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with a long scaled body, a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-half　seed 6101

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with a pair of broad feathered bird wings half-opened along its flanks,
a long scaled body, a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-half-b　seed 6102

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with a pair of broad feathered bird wings half-opened along its flanks,
a long scaled body, a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-half-c　seed 6104

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with a pair of broad feathered bird wings half-opened along its flanks,
a long scaled body, a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

