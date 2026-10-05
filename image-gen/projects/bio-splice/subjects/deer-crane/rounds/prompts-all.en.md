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

## R1 · Deer-crane · Period 01 candidate: deer base (neck slot vacated) + crane long neck G1 (two takes); includes same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 7101
- Images: 3 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它站在雾里、正面朝向镜头：a red deer with a slender head, large ears,
a smooth reddish-brown coat, four long legs and a short tail.
in a misty bamboo grove, thin fog drifting between the stems.
soft diffuse morning light.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-craneneck　seed 7101

```text
全身像，一只动物独自占据画面：它站在雾里、正面朝向镜头：
a red deer with a long slender crane's neck with fine grey feathers, a slender head, large ears,
a smooth reddish-brown coat, four long legs and a short tail.
in a misty bamboo grove, thin fog drifting between the stems.
soft diffuse morning light.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-craneneck-b　seed 7102

```text
全身像，一只动物独自占据画面：它站在雾里、正面朝向镜头：
a red deer with a long slender crane's neck with fine grey feathers, a slender head, large ears,
a smooth reddish-brown coat, four long legs and a short tail.
in a misty bamboo grove, thin fog drifting between the stems.
soft diffuse morning light.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R2 · Deer-crane · Period 02 candidate [vacated version]: deer base (do not describe the legs) + crane slender legs G2; includes same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 7101
- Images: 3 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它在浅水里走着、侧身朝向镜头：a red deer with a slender head,
large ears, a smooth reddish-brown coat and a short tail.
in shallow marsh water among reeds, ripples around its feet.
low morning sun raking across the water.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranelegs　seed 7101

```text
全身像，一只动物独自占据画面：它在浅水里走着、侧身朝向镜头：
a red deer with a pair of long thin crane's legs, a slender head, large ears,
a smooth reddish-brown coat and a short tail.
in shallow marsh water among reeds, ripples around its feet.
low morning sun raking across the water.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranelegs-b　seed 7102

```text
全身像，一只动物独自占据画面：它在浅水里走着、侧身朝向镜头：
a red deer with a pair of long thin crane's legs, a slender head, large ears,
a smooth reddish-brown coat and a short tail.
in shallow marsh water among reeds, ripples around its feet.
low morning sun raking across the water.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R3 · Deer-crane · Period 02 control [occupied version]: deer base (describe four long legs as usual) + crane slender legs G2; includes same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 7101
- Images: 2 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它在浅水里走着、侧身朝向镜头：a red deer with a slender head,
large ears, a smooth reddish-brown coat, four long legs and a short tail.
in shallow marsh water among reeds, ripples around its feet.
low morning sun raking across the water.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranelegs　seed 7101

```text
全身像，一只动物独自占据画面：它在浅水里走着、侧身朝向镜头：
a red deer with a pair of long thin crane's legs, a slender head, large ears,
a smooth reddish-brown coat, four long legs and a short tail.
in shallow marsh water among reeds, ripples around its feet.
low morning sun raking across the water.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R4 · Deer-crane · Period 03 candidate: deer base (do not describe the tail) + crane tail feathers G6 (two takes); includes same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 7101
- Images: 3 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：a red deer with a slender head,
large ears, a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranetait　seed 7101

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：
a red deer with a fan of long white crane tail feathers, a slender head, large ears,
a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranetait-b　seed 7102

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：
a red deer with a fan of long white crane tail feathers, a slender head, large ears,
a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R5 · Deer-crane · Period 04 candidate [neck and legs complete]: deer base (do not describe the legs) + crane neck G1 + crane legs G2; includes same-round base control

- Engine: `zimage`　Size: 1280×1024　steps: 12　shared seed: 7101
- Images: 3 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它立在结霜的草地上、侧身朝向镜头：a red deer with a slender head,
large ears, a smooth reddish-brown coat and a short tail.
on a frost-covered meadow at first light.
cold low light, frost glittering on the grass.
Photograph, a level camera at eye height, 400mm lens at f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### deer-neck-legs　seed 7101

```text
全身像，一只动物独自占据画面：它立在结霜的草地上、侧身朝向镜头：
a red deer with a long slender crane's neck with fine grey feathers and a pair of long thin crane's
legs,
a slender head, large ears, a smooth reddish-brown coat and a short tail.
on a frost-covered meadow at first light.
cold low light, frost glittering on the grass.
Photograph, a level camera at eye height, 400mm lens at f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### deer-neck-legs-b　seed 7102

```text
全身像，一只动物独自占据画面：它立在结霜的草地上、侧身朝向镜头：
a red deer with a long slender crane's neck with fine grey feathers and a pair of long thin crane's
legs,
a slender head, large ears, a smooth reddish-brown coat and a short tail.
on a frost-covered meadow at first light.
cold low light, frost glittering on the grass.
Photograph, a level camera at eye height, 400mm lens at f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R6 · Deer-crane · Period 05 finale [Deer and Crane Sharing Spring]: deer base (do not describe the legs or tail) + crane neck G1 + crane legs G2 + crane tail feathers G6; includes same-round base control

- Engine: `zimage`　Size: 1280×1024　steps: 12　shared seed: 7101
- Images: 3 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它站在花树下、身体横向展开：a red deer with a slender head,
large ears and a smooth reddish-brown coat.
under blossoming plum trees in spring, petals drifting down.
soft diffused light through the blossom.
Photograph, a wide-angle 35mm lens at eye height, f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-crane-3parts　seed 7101

```text
全身像，一只动物独自占据画面：它站在花树下、身体横向展开：
a red deer with a long slender crane's neck with fine grey feathers and a pair of long thin crane's
legs and a fan of long white crane tail feathers,
a slender head, large ears and a smooth reddish-brown coat.
under blossoming plum trees in spring, petals drifting down.
soft diffused light through the blossom.
Photograph, a wide-angle 35mm lens at eye height, f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-crane-3parts-b　seed 7102

```text
全身像，一只动物独自占据画面：它站在花树下、身体横向展开：
a red deer with a long slender crane's neck with fine grey feathers and a pair of long thin crane's
legs and a fan of long white crane tail feathers,
a slender head, large ears and a smooth reddish-brown coat.
under blossoming plum trees in spring, petals drifting down.
soft diffused light through the blossom.
Photograph, a wide-angle 35mm lens at eye height, f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R7 · Deer-crane · Period 03 final (extra takes): deer base (do not describe the tail) + crane tail feathers G6 (three seeds); includes same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 7101
- Images: 4 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：a red deer with a slender head,
large ears, a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranetait　seed 7101

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：
a red deer with a fan of long white crane tail feathers, a slender head, large ears,
a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranetait-c　seed 7103

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：
a red deer with a fan of long white crane tail feathers, a slender head, large ears,
a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranetait-d　seed 7104

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：
a red deer with a fan of long white crane tail feathers, a slender head, large ears,
a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

