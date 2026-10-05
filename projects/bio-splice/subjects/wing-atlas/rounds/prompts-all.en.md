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

## R1 · Wing Atlas · Part 1 [both-wings baseline]: only the unified base (three takes), as the reference for the following four parts

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 13101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、侧身朝向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a bare branch in a woodland clearing.
soft side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### base-bird-b　seed 13102

```text
全身像，一只动物独自占据画面：它停在枝头、侧身朝向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a bare branch in a woodland clearing.
soft side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### base-bird-c　seed 13103

```text
全身像，一只动物独自占据画面：它停在枝头、侧身朝向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a bare branch in a woodland clearing.
soft side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R2 · Wing Atlas · Part 2 [membranous wings]: unified base + insect membranous wings (a second pair on the back, two takes); includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 13101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-membrane　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a pair of translucent insect membranous wings rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-membrane-b　seed 13102

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a pair of translucent insect membranous wings rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R3 · Wing Atlas · Part 3 [leathery wings]: unified base + bat leathery wings (a second pair on the back, two takes); includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 13101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它停在岩壁上、侧身朝向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
at the mouth of a dim limestone cave.
hard light from the cave mouth, deep shadows behind.
a level view at eye height, 300mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-bat　seed 13101

```text
全身像，一只动物独自占据画面：它停在岩壁上、侧身朝向镜头：
a medium-sized brown bird with a pair of leathery bat wings rising from its back, a rounded head,
a short dark beak, folded feathered wings and a long tail.
at the mouth of a dim limestone cave.
hard light from the cave mouth, deep shadows behind.
a level view at eye height, 300mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-bat-b　seed 13102

```text
全身像，一只动物独自占据画面：它停在岩壁上、侧身朝向镜头：
a medium-sized brown bird with a pair of leathery bat wings rising from its back, a rounded head,
a short dark beak, folded feathered wings and a long tail.
at the mouth of a dim limestone cave.
hard light from the cave mouth, deep shadows behind.
a level view at eye height, 300mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R4 · Wing Atlas · Part 4 [fin wings]: unified base + fish pectoral fins (a second pair on the back, two takes); includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 13101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它立在水边的石头上、侧身朝向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a wet stone at the edge of a stream.
soft wet light, reflections from the water below.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-fin　seed 13101

```text
全身像，一只动物独自占据画面：它立在水边的石头上、侧身朝向镜头：
a medium-sized brown bird with a pair of stiff fish pectoral fins rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a wet stone at the edge of a stream.
soft wet light, reflections from the water below.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-fin-b　seed 13102

```text
全身像，一只动物独自占据画面：它立在水边的石头上、侧身朝向镜头：
a medium-sized brown bird with a pair of stiff fish pectoral fins rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a wet stone at the edge of a stream.
soft wet light, reflections from the water below.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R5 · Wing Atlas · Part 5 [seed wings]: unified base + maple samara wings (a second pair on the back, two takes); includes a same-round base control

- Engine: `zimage`　Size: 1280×1024　steps: 12　Shared seed: 13101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它停在秋枝上、身体侧向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
among turning leaves in an autumn wood.
strong backlight through the leaves.
a wide view at eye height, 135mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-seed　seed 13101

```text
全身像，一只动物独自占据画面：它停在秋枝上、身体侧向镜头：
a medium-sized brown bird with a pair of dry maple seed wings rising from its back, a rounded head,
a short dark beak, folded feathered wings and a long tail.
among turning leaves in an autumn wood.
strong backlight through the leaves.
a wide view at eye height, 135mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-seed-b　seed 13102

```text
全身像，一只动物独自占据画面：它停在秋枝上、身体侧向镜头：
a medium-sized brown bird with a pair of dry maple seed wings rising from its back, a rounded head,
a short dark beak, folded feathered wings and a long tail.
among turning leaves in an autumn wood.
strong backlight through the leaves.
a wide view at eye height, 135mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R6 · Wing Atlas · follow-up round: flying-fish fin wings / crane feather wings / paper wings (three donors closer to a "wing"); includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 13101
- Image count: 4 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-flyfish　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a pair of long gliding flying-fish fins rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-crane　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a pair of long white crane wings rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-samara　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a pair of broad papery samara wings rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R7 · Phase 04 final [flying-fish fin wings]: unified base + the flying fish's long fins (a second pair on the back, two takes); includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 13101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它立在水边的石头上、侧身朝向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a wet stone at the edge of a stream.
soft wet light, reflections from the water below.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-flyfish　seed 13101

```text
全身像，一只动物独自占据画面：它立在水边的石头上、侧身朝向镜头：
a medium-sized brown bird with a pair of long gliding flying-fish fins rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a wet stone at the edge of a stream.
soft wet light, reflections from the water below.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-flyfish-b　seed 13102

```text
全身像，一只动物独自占据画面：它立在水边的石头上、侧身朝向镜头：
a medium-sized brown bird with a pair of long gliding flying-fish fins rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a wet stone at the edge of a stream.
soft wet light, reflections from the water below.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R8 · Phase 05 finale [crane feather wings]: unified base + the crane's white wings (a second pair on the back, two takes); includes a same-round base control

- Engine: `zimage`　Size: 1280×1024　steps: 12　Shared seed: 13101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它停在秋枝上、身体侧向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
among turning leaves in an autumn wood.
strong backlight through the leaves.
a wide view at eye height, 135mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-crane　seed 13101

```text
全身像，一只动物独自占据画面：它停在秋枝上、身体侧向镜头：
a medium-sized brown bird with a pair of long white crane wings rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
among turning leaves in an autumn wood.
strong backlight through the leaves.
a wide view at eye height, 135mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-crane-b　seed 13102

```text
全身像，一只动物独自占据画面：它停在秋枝上、身体侧向镜头：
a medium-sized brown bird with a pair of long white crane wings rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
among turning leaves in an autumn wood.
strong backlight through the leaves.
a wide view at eye height, 135mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

