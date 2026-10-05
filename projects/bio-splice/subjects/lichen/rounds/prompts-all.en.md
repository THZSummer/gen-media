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

## R1 · Lichen · period 1 candidate: mycelium base + crustose form CR1 / green algal cells AL1 (with a same-round base control)

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 8101
- Images: 4 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-mycelium　seed 8101

```text
微距特写，一个生物体独自占据画面：它铺在岩面上、表面朝向镜头：
a dense mat of pale fungal mycelium with fine branching threads and a soft dusty surface.
on a bare granite rock face.
raking side light that picks out every crack in the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-crust　seed 8101

```text
微距特写，一个生物体独自占据画面：它铺在岩面上、表面朝向镜头：
a dense mat of pale fungal mycelium with a hard crustose lichen crust with a cracked areolate
surface,
fine branching threads and a soft dusty surface.
on a bare granite rock face.
raking side light that picks out every crack in the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-algae　seed 8101

```text
微距特写，一个生物体独自占据画面：它铺在岩面上、表面朝向镜头：
a dense mat of pale fungal mycelium with clusters of bright green algal cells,
fine branching threads and a soft dusty surface.
on a bare granite rock face.
raking side light that picks out every crack in the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-crust-algae　seed 8101

```text
微距特写，一个生物体独自占据画面：它铺在岩面上、表面朝向镜头：
a dense mat of pale fungal mycelium with a hard crustose lichen crust with a cracked areolate
surface and clusters of bright green algal cells,
fine branching threads and a soft dusty surface.
on a bare granite rock face.
raking side light that picks out every crack in the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

## R2 · Lichen · period 2 candidate: mycelium base + foliose lobes FL1 / algal filaments AL2 (with a same-round base control)

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 8101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-mycelium　seed 8101

```text
微距特写，一个生物体独自占据画面：它贴在树皮上、表面斜向镜头：
a dense mat of pale fungal mycelium with fine branching threads and a soft dusty surface.
on the wet bark of an old tree trunk.
soft wet light with a faint sheen on the surface.
a macro view from slightly above, 100mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-foliose　seed 8101

```text
微距特写，一个生物体独自占据画面：它贴在树皮上、表面斜向镜头：
a dense mat of pale fungal mycelium with leafy foliose lichen lobes with pale rims,
fine branching threads and a soft dusty surface.
on the wet bark of an old tree trunk.
soft wet light with a faint sheen on the surface.
a macro view from slightly above, 100mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-foliose-algae　seed 8102

```text
微距特写，一个生物体独自占据画面：它贴在树皮上、表面斜向镜头：
a dense mat of pale fungal mycelium with leafy foliose lichen lobes with pale rims and fine bright
green algal filaments woven through the surface,
fine branching threads and a soft dusty surface.
on the wet bark of an old tree trunk.
soft wet light with a faint sheen on the surface.
a macro view from slightly above, 100mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

## R3 · Lichen · period 3 candidate: mycelium base + fruticose tufts FR1 (two takes); with a same-round base control

- Engine: `zimage`　Size: 1024×1280　steps: 12　Shared seed: 8101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-mycelium　seed 8101

```text
微距特写，一个生物体独自占据画面：它立在冻原的石面上、整体朝向镜头：
a dense mat of pale fungal mycelium with fine branching threads and a soft dusty surface.
on a frost-covered stone in open tundra.
low backlight through ice fog, rimming every tip.
a low three-quarter macro view, 90mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-fruticose　seed 8101

```text
微距特写，一个生物体独自占据画面：它立在冻原的石面上、整体朝向镜头：
a dense mat of pale fungal mycelium with branching fruticose lichen tufts standing up like tiny
shrubs,
fine branching threads and a soft dusty surface.
on a frost-covered stone in open tundra.
low backlight through ice fog, rimming every tip.
a low three-quarter macro view, 90mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-fruticose-b　seed 8103

```text
微距特写，一个生物体独自占据画面：它立在冻原的石面上、整体朝向镜头：
a dense mat of pale fungal mycelium with branching fruticose lichen tufts standing up like tiny
shrubs,
fine branching threads and a soft dusty surface.
on a frost-covered stone in open tundra.
low backlight through ice fog, rimming every tip.
a low three-quarter macro view, 90mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

## R4 · Lichen · period 4 candidate [algal layer visible]: mycelium base + green cells AL1 + algal filaments AL2 (pseudo cross-section); with a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 8101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-mycelium　seed 8101

```text
微距特写，一个生物体独自占据画面：它的表层被掀开、露出内部结构：
a dense mat of pale fungal mycelium with fine branching threads and a soft dusty surface.
as if in cross-section, the upper cortex lifted away.
ring light, deep even depth of field, everything in focus.
a flat-on macro view, 100mm macro lens at f/16, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-algal-layer　seed 8101

```text
微距特写，一个生物体独自占据画面：它的表层被掀开、露出内部结构：
a dense mat of pale fungal mycelium with clusters of bright green algal cells and fine bright green
algal filaments woven through the surface,
fine branching threads and a soft dusty surface.
as if in cross-section, the upper cortex lifted away.
ring light, deep even depth of field, everything in focus.
a flat-on macro view, 100mm macro lens at f/16, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-algal-layer-b　seed 8102

```text
微距特写，一个生物体独自占据画面：它的表层被掀开、露出内部结构：
a dense mat of pale fungal mycelium with clusters of bright green algal cells and fine bright green
algal filaments woven through the surface,
fine branching threads and a soft dusty surface.
as if in cross-section, the upper cortex lifted away.
ring light, deep even depth of field, everything in focus.
a flat-on macro view, 100mm macro lens at f/16, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

## R5 · Lichen · period 5 finale [the symbiont]: mycelium base + all three forms / two forms + algae (two takes); with a same-round base control

- Engine: `zimage`　Size: 1280×1024　steps: 12　Shared seed: 8101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-mycelium　seed 8101

```text
微距特写，一个生物体独自占据画面：它铺在林地上的石面上、整体展开：
a dense mat of pale fungal mycelium with fine branching threads and a soft dusty surface.
on a mossy boulder in a misty forest, the background dissolving into fog.
soft scattered light, no hard shadows.
a wide macro view, 45mm lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-3forms　seed 8101

```text
微距特写，一个生物体独自占据画面：它铺在林地上的石面上、整体展开：
a dense mat of pale fungal mycelium with a hard crustose lichen crust with a cracked areolate
surface and leafy foliose lichen lobes with pale rims and branching fruticose lichen tufts standing
up like tiny shrubs,
fine branching threads and a soft dusty surface.
on a mossy boulder in a misty forest, the background dissolving into fog.
soft scattered light, no hard shadows.
a wide macro view, 45mm lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-forms-algae　seed 8102

```text
微距特写，一个生物体独自占据画面：它铺在林地上的石面上、整体展开：
a dense mat of pale fungal mycelium with leafy foliose lichen lobes with pale rims and branching
fruticose lichen tufts standing up like tiny shrubs and clusters of bright green algal cells,
fine branching threads and a soft dusty surface.
on a mossy boulder in a misty forest, the background dissolving into fog.
soft scattered light, no hard shadows.
a wide macro view, 45mm lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

