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

## R1 · Cordyceps · Period 01 candidate: moth larva base + mycelium coating MY1 / single stroma ST1 (includes same-round base control)

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 9101
- Images: 4 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-larva　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在土面上、身体侧向镜头：
a large moth larva with a segmented pale body, a dark head capsule and short stubby legs.
on damp dark soil among dead leaves.
soft diffused light under a forest canopy.
a low macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### larva-mycelium　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在土面上、身体侧向镜头：
a large moth larva with a dense coating of pale fungal mycelium across the whole body,
a segmented pale body, a dark head capsule and short stubby legs.
on damp dark soil among dead leaves.
soft diffused light under a forest canopy.
a low macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### larva-stroma　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在土面上、身体侧向镜头：
a large moth larva with a single tall club-shaped fungal stroma rising from its body,
a segmented pale body, a dark head capsule and short stubby legs.
on damp dark soil among dead leaves.
soft diffused light under a forest canopy.
a low macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### larva-mycelium-stroma　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在土面上、身体侧向镜头：
a large moth larva with a dense coating of pale fungal mycelium across the whole body and a single
tall club-shaped fungal stroma rising from its body,
a segmented pale body, a dark head capsule and short stubby legs.
on damp dark soil among dead leaves.
soft diffused light under a forest canopy.
a low macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

## R2 · Cordyceps · Period 01 control [vacated version]: base does not describe the surface texture + mycelium coating MY1; includes same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 9101
- Images: 2 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-larva　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在土面上、身体侧向镜头：
a large moth larva with a dark head capsule and short stubby legs.
on damp dark soil among dead leaves.
soft diffused light under a forest canopy.
a low macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### larva-mycelium　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在土面上、身体侧向镜头：
a large moth larva with a dense coating of pale fungal mycelium across the whole body,
a dark head capsule and short stubby legs.
on damp dark soil among dead leaves.
soft diffused light under a forest canopy.
a low macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

## R3 · Period 01 final [mycelium coating]: base does not describe the surface texture + MY1 (three seeds); includes same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 9101
- Images: 4 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-larva　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在土面上、身体侧向镜头：
a large moth larva with a dark head capsule and short stubby legs.
on damp dark soil among dead leaves.
soft diffused light under a forest canopy.
a low macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### larva-mycelium　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在土面上、身体侧向镜头：
a large moth larva with a dense coating of pale fungal mycelium across the whole body,
a dark head capsule and short stubby legs.
on damp dark soil among dead leaves.
soft diffused light under a forest canopy.
a low macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### larva-mycelium-b　seed 9102

```text
微距特写，一个生物体独自占据画面：它伏在土面上、身体侧向镜头：
a large moth larva with a dense coating of pale fungal mycelium across the whole body,
a dark head capsule and short stubby legs.
on damp dark soil among dead leaves.
soft diffused light under a forest canopy.
a low macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### larva-mycelium-c　seed 9103

```text
微距特写，一个生物体独自占据画面：它伏在土面上、身体侧向镜头：
a large moth larva with a dense coating of pale fungal mycelium across the whole body,
a dark head capsule and short stubby legs.
on damp dark soil among dead leaves.
soft diffused light under a forest canopy.
a low macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

## R4 · Period 02 final [single stroma]: moth larva base + single ST1 (two takes); includes same-round base control

- Engine: `zimage`　Size: 1024×1280　steps: 12　shared seed: 9101
- Images: 3 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-larva　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在草甸的土面上、身体侧向镜头：
a large moth larva with a segmented pale body, a dark head capsule and short stubby legs.
on alpine meadow soil among short grasses.
low morning sun, dew on the ground.
a low macro view from just above the ground, 100mm macro lens at f/8, macro photograph,
focus-stacked, fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### larva-stroma　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在草甸的土面上、身体侧向镜头：
a large moth larva with a single tall club-shaped fungal stroma rising from its body,
a segmented pale body, a dark head capsule and short stubby legs.
on alpine meadow soil among short grasses.
low morning sun, dew on the ground.
a low macro view from just above the ground, 100mm macro lens at f/8, macro photograph,
focus-stacked, fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### larva-stroma-b　seed 9102

```text
微距特写，一个生物体独自占据画面：它伏在草甸的土面上、身体侧向镜头：
a large moth larva with a single tall club-shaped fungal stroma rising from its body,
a segmented pale body, a dark head capsule and short stubby legs.
on alpine meadow soil among short grasses.
low morning sun, dew on the ground.
a low macro view from just above the ground, 100mm macro lens at f/8, macro photograph,
focus-stacked, fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

## R5 · Period 03 final [multiple stromata]: moth larva base + multiple ST1x; backlight · square (two takes); includes same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 9101
- Images: 3 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-larva　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在草甸的土面上、身体侧向镜头：
a large moth larva with a segmented pale body, a dark head capsule and short stubby legs.
on alpine meadow soil among short grasses.
strong backlight through the grass, rimming the stromata.
a low macro view from just above the ground, 100mm macro lens at f/8, macro photograph,
focus-stacked, fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### larva-stromata　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在草甸的土面上、身体侧向镜头：
a large moth larva with several tall club-shaped fungal stromata rising from its body,
a segmented pale body, a dark head capsule and short stubby legs.
on alpine meadow soil among short grasses.
strong backlight through the grass, rimming the stromata.
a low macro view from just above the ground, 100mm macro lens at f/8, macro photograph,
focus-stacked, fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### larva-stromata-b　seed 9102

```text
微距特写，一个生物体独自占据画面：它伏在草甸的土面上、身体侧向镜头：
a large moth larva with several tall club-shaped fungal stromata rising from its body,
a segmented pale body, a dark head capsule and short stubby legs.
on alpine meadow soil among short grasses.
strong backlight through the grass, rimming the stromata.
a low macro view from just above the ground, 100mm macro lens at f/8, macro photograph,
focus-stacked, fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

## R6 · Period 04 final [stroma and spores]: moth larva base + single ST1 + spores SP1; snowline cold light · landscape; includes same-round base control

- Engine: `zimage`　Size: 1280×1024　steps: 12　shared seed: 9101
- Images: 3 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-larva　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在砾石土面上、身体侧向镜头：
a large moth larva with a segmented pale body, a dark head capsule and short stubby legs.
on gravelly soil at the snow line, patches of old snow behind.
cold flat light, no shadows.
a low macro view, 100mm macro lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### larva-stroma-spores　seed 9101

```text
微距特写，一个生物体独自占据画面：它伏在砾石土面上、身体侧向镜头：
a large moth larva with a single tall club-shaped fungal stroma rising from its body and clusters
of fine pale spores dusting the surface,
a segmented pale body, a dark head capsule and short stubby legs.
on gravelly soil at the snow line, patches of old snow behind.
cold flat light, no shadows.
a low macro view, 100mm macro lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### larva-stroma-spores-b　seed 9102

```text
微距特写，一个生物体独自占据画面：它伏在砾石土面上、身体侧向镜头：
a large moth larva with a single tall club-shaped fungal stroma rising from its body and clusters
of fine pale spores dusting the surface,
a segmented pale body, a dark head capsule and short stubby legs.
on gravelly soil at the snow line, patches of old snow behind.
cold flat light, no shadows.
a low macro view, 100mm macro lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

## R7 · Period 05 finale [caterpillar fungus · specimen photo]: moth larva + mycelium coating MY1 + stroma ST1 + spores SP1; neutral background ring light (two takes)

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 9101
- Images: 3 (each an independent request)

**Round-constant layer** (shared by all images, so that A/B/C differ only in the splice clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-larva　seed 9101

```text
标本照，一个标本独自占据画面：它被放在灰色台面上、身体侧向镜头：
a large moth larva with a segmented pale body, a dark head capsule and short stubby legs.
on a plain neutral grey background, nothing else in frame.
ring light, deep even illumination, everything in focus.
a flat-on macro view, 100mm macro lens at f/16, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### cordyceps-specimen　seed 9101

```text
标本照，一个标本独自占据画面：它被放在灰色台面上、身体侧向镜头：
a large moth larva with a dense coating of pale fungal mycelium across the whole body and a single
tall club-shaped fungal stroma rising from its body and clusters of fine pale spores dusting the
surface,
a segmented pale body, a dark head capsule and short stubby legs.
on a plain neutral grey background, nothing else in frame.
ring light, deep even illumination, everything in focus.
a flat-on macro view, 100mm macro lens at f/16, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### cordyceps-specimen-b　seed 9102

```text
标本照，一个标本独自占据画面：它被放在灰色台面上、身体侧向镜头：
a large moth larva with a dense coating of pale fungal mycelium across the whole body and a single
tall club-shaped fungal stroma rising from its body and clusters of fine pale spores dusting the
surface,
a segmented pale body, a dark head capsule and short stubby legs.
on a plain neutral grey background, nothing else in frame.
ring light, deep even illumination, everything in focus.
a flat-on macro view, 100mm macro lens at f/16, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

