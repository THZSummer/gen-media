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

## R1 · Tree-beast · Phase 1 candidates [occupied version]: the base writes bark as usual + beast-hide texture K1; includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 12101
- Image count: 2 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with rough fissured bark,
thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide　seed 12101

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide, rough fissured bark,
thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R2 · Tree-beast · Phase 1 control [freed version]: the base does not write bark + beast-hide texture K1; includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 12101
- Image count: 2 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide　seed 12101

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide,
thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R3 · Tree-beast · Phase 2 candidates [the tree whose roots become feet]: old tree + beast feet K2 (two takes); includes a same-round base control

- Engine: `zimage`　Size: 1024×1280　steps: 12　Shared seed: 12101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它长在泥岸边、露出的根系朝向镜头：
an old gnarled tree with rough fissured bark,
thick roots spreading over the ground and a massive trunk.
on a muddy riverbank, the roots exposed above the water line.
low morning light, long shadows across the mud.
a low view looking up the trunk, 35mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-feet　seed 12101

```text
全身像，一个生物体独自占据画面：它长在泥岸边、露出的根系朝向镜头：
an old gnarled tree with heavy clawed mammal feet among the roots, rough fissured bark,
thick roots spreading over the ground and a massive trunk.
on a muddy riverbank, the roots exposed above the water line.
low morning light, long shadows across the mud.
a low view looking up the trunk, 35mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-feet-b　seed 12102

```text
全身像，一个生物体独自占据画面：它长在泥岸边、露出的根系朝向镜头：
an old gnarled tree with heavy clawed mammal feet among the roots, rough fissured bark,
thick roots spreading over the ground and a massive trunk.
on a muddy riverbank, the roots exposed above the water line.
low morning light, long shadows across the mud.
a low view looking up the trunk, 35mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R4 · Tree-beast · Phase 3 candidates [the horned tree]: old tree + beast horns K4 (growing from the trunk, two takes); includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 12101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它立在霜林里、树干侧面朝向镜头：
an old gnarled tree with rough fissured bark,
thick roots spreading over the ground and a massive trunk.
in a frost-covered forest, bare branches around it.
low side-backlight, frost glittering on the bark.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-horns　seed 12101

```text
全身像，一个生物体独自占据画面：它立在霜林里、树干侧面朝向镜头：
an old gnarled tree with a pair of massive curved mammal horns rising from the trunk,
rough fissured bark, thick roots spreading over the ground and a massive trunk.
in a frost-covered forest, bare branches around it.
low side-backlight, frost glittering on the bark.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-horns-b　seed 12102

```text
全身像，一个生物体独自占据画面：它立在霜林里、树干侧面朝向镜头：
an old gnarled tree with a pair of massive curved mammal horns rising from the trunk,
rough fissured bark, thick roots spreading over the ground and a massive trunk.
in a frost-covered forest, bare branches around it.
low side-backlight, frost glittering on the bark.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R5 · Tree-beast · Phase 4 candidates [both hide and feet]: the base does not write bark + beast-hide texture K1 + beast feet K2; includes a same-round base control

- Engine: `zimage`　Size: 1280×1024　steps: 12　Shared seed: 12101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它长在坡地上、树干与根系都朝向镜头：
an old gnarled tree with thick roots spreading over the ground and a massive trunk.
on a forest slope just after rain, wet leaves everywhere.
hard light breaking through after the rain, crisp shadows.
a level view at eye height, 35mm lens at f/11, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide-feet　seed 12101

```text
全身像，一个生物体独自占据画面：它长在坡地上、树干与根系都朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide and heavy clawed mammal feet among
the roots,
thick roots spreading over the ground and a massive trunk.
on a forest slope just after rain, wet leaves everywhere.
hard light breaking through after the rain, crisp shadows.
a level view at eye height, 35mm lens at f/11, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide-feet-b　seed 12102

```text
全身像，一个生物体独自占据画面：它长在坡地上、树干与根系都朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide and heavy clawed mammal feet among
the roots,
thick roots spreading over the ground and a massive trunk.
on a forest slope just after rain, wet leaves everywhere.
hard light breaking through after the rain, crisp shadows.
a level view at eye height, 35mm lens at f/11, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R6 · Tree-beast · Phase 5 finale [tree-beast]: the base does not write bark + beast-hide texture K1 + beast feet K2 + beast horns K4; dusk backlight, wide angle

- Engine: `zimage`　Size: 1280×1024　steps: 12　Shared seed: 12101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它立在暮色林里、整棵树朝向镜头：
an old gnarled tree with thick roots spreading over the ground and a massive trunk.
in a forest at dusk, the far trees lost in haze.
low backlight throwing the whole tree into near-silhouette.
a wide-angle 24mm lens at eye height, f/8, fine surface detail, natural colour, slight film grain,
no digital sharpening, no text, no watermark.
```

### tree-beast　seed 12101

```text
全身像，一个生物体独自占据画面：它立在暮色林里、整棵树朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide and heavy clawed mammal feet among
the roots and a pair of massive curved mammal horns rising from the trunk,
thick roots spreading over the ground and a massive trunk.
in a forest at dusk, the far trees lost in haze.
low backlight throwing the whole tree into near-silhouette.
a wide-angle 24mm lens at eye height, f/8, fine surface detail, natural colour, slight film grain,
no digital sharpening, no text, no watermark.
```

### tree-beast-b　seed 12102

```text
全身像，一个生物体独自占据画面：它立在暮色林里、整棵树朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide and heavy clawed mammal feet among
the roots and a pair of massive curved mammal horns rising from the trunk,
thick roots spreading over the ground and a massive trunk.
in a forest at dusk, the far trees lost in haze.
low backlight throwing the whole tree into near-silhouette.
a wide-angle 24mm lens at eye height, f/8, fine surface detail, natural colour, slight film grain,
no digital sharpening, no text, no watermark.
```

## R7 · Phase 01 final [the tree with a beast hide]: the base does not write bark + beast-hide texture K1 (three seeds); includes a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 12101
- Image count: 4 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide　seed 12101

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide,
thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide-b　seed 12102

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide,
thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide-c　seed 12103

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide,
thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R8 · Phase 03 final [both hide and horns]: the base does not write bark + beast-hide texture K1 + beast horns K4 (two takes); after rain, hard light, landscape

- Engine: `zimage`　Size: 1280×1024　steps: 12　Shared seed: 12101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它长在坡地上、树干与根系都朝向镜头：
an old gnarled tree with thick roots spreading over the ground and a massive trunk.
on a forest slope just after rain, wet leaves everywhere.
hard light breaking through after the rain, crisp shadows.
a level view at eye height, 35mm lens at f/11, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide-horns　seed 12101

```text
全身像，一个生物体独自占据画面：它长在坡地上、树干与根系都朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide and a pair of massive curved mammal
horns rising from the trunk,
thick roots spreading over the ground and a massive trunk.
on a forest slope just after rain, wet leaves everywhere.
hard light breaking through after the rain, crisp shadows.
a level view at eye height, 35mm lens at f/11, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide-horns-b　seed 12102

```text
全身像，一个生物体独自占据画面：它长在坡地上、树干与根系都朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide and a pair of massive curved mammal
horns rising from the trunk,
thick roots spreading over the ground and a massive trunk.
on a forest slope just after rain, wet leaves everywhere.
hard light breaking through after the rain, crisp shadows.
a level view at eye height, 35mm lens at f/11, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R9 · Phase 04 final [the dead wood's hide and horns]: **base swapped (standing dead wood)** + beast-hide texture K1 + beast horns K4 (two takes)

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 12101
- Image count: 3 (each an independent request)

**Constant layer within the round** (shared by every image, ensuring A/B/C differ only in the splice clause)

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它立在霜晨的空地上、树干正面朝向镜头：
a dead standing tree with a splintered bare trunk and exposed roots.
standing dead in a clearing on a frosty morning.
cold flat light, frost on every surface.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### deadwood-hide-horns　seed 12101

```text
全身像，一个生物体独自占据画面：它立在霜晨的空地上、树干正面朝向镜头：
a dead standing tree with a covering of coarse tawny mammal hide and a pair of massive curved
mammal horns rising from the trunk,
a splintered bare trunk and exposed roots.
standing dead in a clearing on a frosty morning.
cold flat light, frost on every surface.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### deadwood-hide-horns-b　seed 12102

```text
全身像，一个生物体独自占据画面：它立在霜晨的空地上、树干正面朝向镜头：
a dead standing tree with a covering of coarse tawny mammal hide and a pair of massive curved
mammal horns rising from the trunk,
a splintered bare trunk and exposed roots.
standing dead in a clearing on a frosty morning.
cold flat light, frost on every surface.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

