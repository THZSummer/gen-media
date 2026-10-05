# Raw Prompt Archive for All Rounds

> 🌐 Language: **English** | [中文](prompts-all.md)

> This file is generated automatically by `python3 run_round.py --prompts`; its content = **the exact string actually submitted to ComfyUI**.
> For ease of reference and round-by-round comparison, the code blocks are wrapped at clause boundaries; **the line breaks are not part of the prompt, they are layout only**.
> Unwrapping rule: when the end of a line is an ASCII character, that line break equals one space; otherwise there was originally no character at the line break.
> `unwrap_prompt()` in `run_round.py` is exactly this rule; at generation time it asserts "unwrapped == original" entry by entry.
> The verbatim original (single line) is in the constants of `run_round.py` (`python3 run_round.py <N> --dry` prints it directly)
> and in `work/rN/round.json`; the final authority is the server's `GET /history/{prompt_id}`.
> To change a prompt, edit `subjects/<子主题>/rounds.py`, then regenerate this file.
> Back to the [sub-theme home](../README.en.md) ｜ [project home](../../../README.en.md)

## Where things are recorded (three layers)

| Layer | Location | Content |
|----|------|------|
| Authoritative source | `subjects/<子主题>/rounds.py` | verbatim prompt (the one actually sent, single line) |
| Readable document | this file / `docs/rN.md` | the full prompt wrapped at clause boundaries; per-round changes and self-checks |
| Machine record | `work/rN/round.json` | filename / seed / prompt_id / engine / parameters / **prompt original** |
| Server side | `GET /history/{prompt_id}` | the full graph ComfyUI actually executed (final authority) |

## R1 · Xuanwu · Period 01 candidate: turtle base + snake neck N1 / snake tail N2 / coiled body N3 (includes same-round base control)

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 5101
- Images: 5 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Wildlife photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-turtle　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-snakeneck　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-snaketail　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a long tapering snake's tail with keeled scales, a dark domed shell,
a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-coil　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with the thick coiled body of a large snake wrapped around its shell,
a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-neck-tail　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales and a long
tapering snake's tail with keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R2 · Xuanwu · Period 03 candidate: three wordings for the coiled body N3 (wrapped around the shell rim / coiled on the stone beneath the body / shortest form); includes same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 5101
- Images: 4 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Wildlife photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-turtle　seed 5101

```text
全身像，一只动物独自占据画面：它伏在井边的石台上、龟壳朝向镜头：
a large wild river turtle with a dark domed shell, a small wrinkled head, four short webbed legs.
on a mossy stone ledge beside an old stone well.
hard side light raking across the shell.
Wildlife photograph, a view from slightly above, 100mm lens at f/5.6, the whole shell in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### coil-rim　seed 5101

```text
全身像，一只动物独自占据画面：它伏在井边的石台上、龟壳朝向镜头：
a large wild river turtle with thick snake coils around the rim of its shell, a dark domed shell,
a small wrinkled head, four short webbed legs.
on a mossy stone ledge beside an old stone well.
hard side light raking across the shell.
Wildlife photograph, a view from slightly above, 100mm lens at f/5.6, the whole shell in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### coil-ground　seed 5101

```text
全身像，一只动物独自占据画面：它伏在井边的石台上、龟壳朝向镜头：
a large wild river turtle with a thick snake's body coiled on the stones beneath it,
its coils visible on both sides, a dark domed shell, a small wrinkled head, four short webbed legs.
on a mossy stone ledge beside an old stone well.
hard side light raking across the shell.
Wildlife photograph, a view from slightly above, 100mm lens at f/5.6, the whole shell in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### coil-min　seed 5101

```text
全身像，一只动物独自占据画面：它伏在井边的石台上、龟壳朝向镜头：
a large wild river turtle with thick snake coils around its shell, a dark domed shell,
a small wrinkled head, four short webbed legs.
on a mossy stone ledge beside an old stone well.
hard side light raking across the shell.
Wildlife photograph, a view from slightly above, 100mm lens at f/5.6, the whole shell in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R3 · Period 01 final [shallow stream stones · morning light · eye level 600mm]: turtle base + snake neck N1 (two takes); includes same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 5101
- Images: 4 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Wildlife photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-turtle　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-snakeneck　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-snakeneck-b　seed 5102

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-snakeneck-c　seed 5103

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R4 · Period 02 final [wetland mud bank · overcast · eye level full body 400mm]: turtle base + snake tail N2 (two takes); includes same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 5101
- Images: 4 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Wildlife photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-turtle　seed 5101

```text
全身像，一只动物独自占据画面：它正在泥岸上爬行、侧身朝向镜头：
a large wild river turtle with a dark domed shell, a small wrinkled head, four short webbed legs.
on the muddy bank of a marsh pool, wet silt and trampled reeds.
flat overcast light.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### turtle-snaketail　seed 5101

```text
全身像，一只动物独自占据画面：它正在泥岸上爬行、侧身朝向镜头：
a large wild river turtle with a long tapering snake's tail with keeled scales, a dark domed shell,
a small wrinkled head, four short webbed legs.
on the muddy bank of a marsh pool, wet silt and trampled reeds.
flat overcast light.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### turtle-snaketail-b　seed 5102

```text
全身像，一只动物独自占据画面：它正在泥岸上爬行、侧身朝向镜头：
a large wild river turtle with a long tapering snake's tail with keeled scales, a dark domed shell,
a small wrinkled head, four short webbed legs.
on the muddy bank of a marsh pool, wet silt and trampled reeds.
flat overcast light.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### turtle-snaketail-c　seed 5103

```text
全身像，一只动物独自占据画面：它正在泥岸上爬行、侧身朝向镜头：
a large wild river turtle with a long tapering snake's tail with keeled scales, a dark domed shell,
a small wrinkled head, four short webbed legs.
on the muddy bank of a marsh pool, wet silt and trampled reeds.
flat overcast light.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R5 · Period 04 final [stones after rain · backlight · eye level 400mm · landscape]: turtle base + snake neck N1 + snake tail N2; includes same-round base control

- Engine: `zimage`　Size: 1280×1024　steps: 12　shared seed: 5101
- Images: 3 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Wildlife photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-turtle　seed 5101

```text
全身像，一只动物独自占据画面：它伏在湿石上、侧身朝向镜头：
a large wild river turtle with a dark domed shell, a small wrinkled head, four short webbed legs.
on rain-soaked stones in a mountain stream.
backlight through the spray, rimming its outline.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### turtle-neck-tail　seed 5101

```text
全身像，一只动物独自占据画面：它伏在湿石上、侧身朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales and a long
tapering snake's tail with keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on rain-soaked stones in a mountain stream.
backlight through the spray, rimming its outline.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### turtle-neck-tail-b　seed 5102

```text
全身像，一只动物独自占据画面：它伏在湿石上、侧身朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales and a long
tapering snake's tail with keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on rain-soaked stones in a mountain stream.
backlight through the spray, rimming its outline.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R6 · Period 05 finale [Xuanwu]: turtle base + snake neck N1 + snake tail N2 + coiled body N3; dusk water surface · eye level wide-angle · landscape

- Engine: `zimage`　Size: 1280×1024　steps: 12　shared seed: 5101
- Images: 3 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Wildlife photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-turtle　seed 5101

```text
全身像，一只动物独自占据画面：它伏在水边的石台上、身体横向展开：
a large wild river turtle with a dark domed shell, a small wrinkled head, four short webbed legs.
on a flat stone at the edge of dark water at dusk.
low backlight from across the water, throwing the animal into near-silhouette.
Wildlife photograph, a wide-angle 35mm lens at eye height, f/4,
the whole animal and its reflection in frame, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### turtle-all3　seed 5101

```text
全身像，一只动物独自占据画面：它伏在水边的石台上、身体横向展开：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales and a long
tapering snake's tail with keeled scales and thick snake coils around its shell,
a dark domed shell, a small wrinkled head, four short webbed legs.
on a flat stone at the edge of dark water at dusk.
low backlight from across the water, throwing the animal into near-silhouette.
Wildlife photograph, a wide-angle 35mm lens at eye height, f/4,
the whole animal and its reflection in frame, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### turtle-all3-b　seed 5102

```text
全身像，一只动物独自占据画面：它伏在水边的石台上、身体横向展开：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales and a long
tapering snake's tail with keeled scales and thick snake coils around its shell,
a dark domed shell, a small wrinkled head, four short webbed legs.
on a flat stone at the edge of dark water at dusk.
low backlight from across the water, throwing the animal into near-silhouette.
Wildlife photograph, a wide-angle 35mm lens at eye height, f/4,
the whole animal and its reflection in frame, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

