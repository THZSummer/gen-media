# Archive of the Raw Prompts for Every Round

> 🌐 Language: **English** | [中文](prompts-all.md)

> This file is generated automatically by `python3 run_round.py --prompts`; its content = **the exact string actually submitted to ComfyUI**.
> To make it easy to consult and compare round by round, the code blocks are wrapped at clause boundaries; **the line breaks are not part of the prompt, they are layout only**.
> Restoration rule: when the end of a line is an ASCII character, that line break equals one space; otherwise there was no character at the break.
> `unwrap_prompt()` in `run_round.py` is exactly this rule, and generation asserts "restored == original" for every entry.
> The verbatim original (single line) is in the constants of `run_round.py` (`python3 run_round.py <N> --dry` prints it directly)
> and in `work/rN/round.json`; the final authority is the server's `GET /history/{prompt_id}`.
> To change a prompt, edit `subjects/<子主题>/rounds.py` and then regenerate this file.
> Back to [subject home](../README.en.md) ｜ [project home](../../../README.en.md)

## Where this is recorded (three layers)

| Layer | Location | Content |
|----|------|------|
| Authoritative source | `subjects/<子主题>/rounds.py` | The verbatim prompt (what is really sent out, single line) |
| Human-readable doc | this file / `docs/rN.md` | The full prompt wrapped at clause boundaries; per-round changes and self-checks |
| Machine record | `work/rN/round.json` | filename / seed / prompt_id / engine / parameters / **the prompt original** |
| Server side | `GET /history/{prompt_id}` | The complete graph ComfyUI actually executed (final authority) |

## R1 · Horn atlas · part 1 [hornless baseline]: the unified base (three takes), serving as the reference for the following four parts

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 14101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-horse　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
soft diffused light through the mist.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### base-horse-b　seed 14102

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
soft diffused light through the mist.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### base-horse-c　seed 14103

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
soft diffused light through the mist.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R2 · Horn atlas · part 2 [deer antlers]: unified base + branching deer antlers (two takes); with a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 14101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-horse　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
low side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-antlers　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：
a bay horse with a pair of branching deer antlers rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
low side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-antlers-b　seed 14102

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：
a bay horse with a pair of branching deer antlers rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
low side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R3 · Horn atlas · part 3 [ox horns]: unified base + thick ox horns (two takes); with a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 14101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-horse　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
flat top light, the coat dull and even.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-oxhorns　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：
a bay horse with a pair of thick curved ox horns rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
flat top light, the coat dull and even.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-oxhorns-b　seed 14102

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：
a bay horse with a pair of thick curved ox horns rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
flat top light, the coat dull and even.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R4 · Horn atlas · part 4 [ram horns]: unified base + curled ram horns (two takes); with a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 14101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-horse　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
low side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-ramhorns　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：
a bay horse with a pair of curled ram horns rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
low side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-ramhorns-b　seed 14102

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：
a bay horse with a pair of curled ram horns rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
low side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R5 · Horn atlas · part 5 [narwhal tusk / rhino horn]: unified base + two kinds of single horn (one of each); with a same-round base control

- Engine: `zimage`　Size: 1024×1280　steps: 12　Shared seed: 14101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-horse　seed 14101

```text
头部特写，一只动物独自占据画面：它抬起头、正面朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
on frost-covered grassland at first light.
low side-backlight, frost glittering.
a tight portrait of the head, 200mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-narwhal　seed 14101

```text
头部特写，一只动物独自占据画面：它抬起头、正面朝向镜头：
a bay horse with a single long spiral narwhal tusk rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
on frost-covered grassland at first light.
low side-backlight, frost glittering.
a tight portrait of the head, 200mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-rhino　seed 14102

```text
头部特写，一只动物独自占据画面：它抬起头、正面朝向镜头：
a bay horse with a single heavy rhinoceros horn rising from its nose, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
on frost-covered grassland at first light.
low side-backlight, frost glittering.
a tight portrait of the head, 200mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

