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

## R1 · Venus flytrap · period 1 candidate [occupied]: the base writes the hard teeth as usual + mammal fangs T1 (with a same-round base control)

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 10101
- Images: 2 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-flytrap　seed 10101

```text
微距特写，一个生物体独自占据画面：它张着夹子、内面朝向镜头：
a Venus flytrap with two wide-open trap lobes,
a red inner surface and a fringe of stiff marginal teeth.
in a sphagnum bog among wet moss.
raking side-backlight, the red inner surface glowing.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-fangs　seed 10101

```text
微距特写，一个生物体独自占据画面：它张着夹子、内面朝向镜头：
a Venus flytrap with a row of sharp white mammal fangs along the trap edges,
two wide-open trap lobes, a red inner surface and a fringe of stiff marginal teeth.
in a sphagnum bog among wet moss.
raking side-backlight, the red inner surface glowing.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

## R2 · Venus flytrap · period 1 control [freed up]: the base does not write the hard teeth + mammal fangs T1 (with a same-round base control)

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 10101
- Images: 2 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-flytrap　seed 10101

```text
微距特写，一个生物体独自占据画面：它张着夹子、内面朝向镜头：
a Venus flytrap with two wide-open trap lobes and a red inner surface.
in a sphagnum bog among wet moss.
raking side-backlight, the red inner surface glowing.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-fangs　seed 10101

```text
微距特写，一个生物体独自占据画面：它张着夹子、内面朝向镜头：
a Venus flytrap with a row of sharp white mammal fangs along the trap edges,
two wide-open trap lobes and a red inner surface.
in a sphagnum bog among wet moss.
raking side-backlight, the red inner surface glowing.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

## R3 · Period 01 final [the flytrap with fangs]: the base does not write the marginal teeth + mammal fangs T1 (three seeds); with a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 10101
- Images: 4 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-flytrap　seed 10101

```text
微距特写，一个生物体独自占据画面：它张着夹子、内面朝向镜头：
a Venus flytrap with two wide-open trap lobes and a red inner surface.
in a sphagnum bog among wet moss.
raking side-backlight, the red inner surface glowing.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-fangs　seed 10101

```text
微距特写，一个生物体独自占据画面：它张着夹子、内面朝向镜头：
a Venus flytrap with a row of sharp white mammal fangs along the trap edges,
two wide-open trap lobes and a red inner surface.
in a sphagnum bog among wet moss.
raking side-backlight, the red inner surface glowing.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-fangs-b　seed 10102

```text
微距特写，一个生物体独自占据画面：它张着夹子、内面朝向镜头：
a Venus flytrap with a row of sharp white mammal fangs along the trap edges,
two wide-open trap lobes and a red inner surface.
in a sphagnum bog among wet moss.
raking side-backlight, the red inner surface glowing.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-fangs-c　seed 10103

```text
微距特写，一个生物体独自占据画面：它张着夹子、内面朝向镜头：
a Venus flytrap with a row of sharp white mammal fangs along the trap edges,
two wide-open trap lobes and a red inner surface.
in a sphagnum bog among wet moss.
raking side-backlight, the red inner surface glowing.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

## R4 · Period 02 final [the flytrap with eyes]: broad-leaf-blade base + eye T2 (two takes); with a same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 10101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-flytrap　seed 10101

```text
微距特写，一个生物体独自占据画面：它把宽叶面朝向镜头、夹子在后：
a Venus flytrap with broad flat leaf blades and two wide-open trap lobes with a red inner surface.
in a sphagnum bog among wet moss.
flat overcast light, no glare on the leaf.
a flat-on macro view of the leaf blade, 100mm macro lens at f/11, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-eye　seed 10101

```text
微距特写，一个生物体独自占据画面：它把宽叶面朝向镜头、夹子在后：
a Venus flytrap with a glossy dark animal eye on the leaf blade,
broad flat leaf blades and two wide-open trap lobes with a red inner surface.
in a sphagnum bog among wet moss.
flat overcast light, no glare on the leaf.
a flat-on macro view of the leaf blade, 100mm macro lens at f/11, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-eye-b　seed 10102

```text
微距特写，一个生物体独自占据画面：它把宽叶面朝向镜头、夹子在后：
a Venus flytrap with a glossy dark animal eye on the leaf blade,
broad flat leaf blades and two wide-open trap lobes with a red inner surface.
in a sphagnum bog among wet moss.
flat overcast light, no glare on the leaf.
a flat-on macro view of the leaf blade, 100mm macro lens at f/11, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

## R5 · Period 03 final [the tongue-flicking flytrap]: broad-leaf-blade base + tongue T4 (two takes); low mossy camera, portrait format

- Engine: `zimage`　Size: 1024×1280　steps: 12　Shared seed: 10101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-flytrap　seed 10101

```text
微距特写，一个生物体独自占据画面：它张着夹子、内腔朝向镜头：
a Venus flytrap with broad flat leaf blades and two wide-open trap lobes with a red inner surface.
low among wet moss, the trap opening facing the camera.
soft light falling into the open trap.
a low macro view looking into the trap, 100mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-tongue　seed 10101

```text
微距特写，一个生物体独自占据画面：它张着夹子、内腔朝向镜头：
a Venus flytrap with a long pink mammal tongue curling out of the trap,
broad flat leaf blades and two wide-open trap lobes with a red inner surface.
low among wet moss, the trap opening facing the camera.
soft light falling into the open trap.
a low macro view looking into the trap, 100mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-tongue-b　seed 10102

```text
微距特写，一个生物体独自占据画面：它张着夹子、内腔朝向镜头：
a Venus flytrap with a long pink mammal tongue curling out of the trap,
broad flat leaf blades and two wide-open trap lobes with a red inner surface.
low among wet moss, the trap opening facing the camera.
soft light falling into the open trap.
a low macro view looking into the trap, 100mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

## R6 · Period 04 final [fangs and tongue together]: the base does not write the marginal teeth + mammal fangs T1 + tongue T4 (two takes); hard side light after rain

- Engine: `zimage`　Size: 1024×1024　steps: 12　Shared seed: 10101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-flytrap　seed 10101

```text
微距特写，一个生物体独自占据画面：它张着夹子、内面朝向镜头：
a Venus flytrap with two wide-open trap lobes and a red inner surface.
in a bog just after rain, water beading on the lobes.
hard side light after the rain, crisp shadows.
a level macro view, 100mm macro lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-fangs-tongue　seed 10101

```text
微距特写，一个生物体独自占据画面：它张着夹子、内面朝向镜头：
a Venus flytrap with a row of sharp white mammal fangs along the trap edges and a long pink mammal
tongue curling out of the trap,
two wide-open trap lobes and a red inner surface.
in a bog just after rain, water beading on the lobes.
hard side light after the rain, crisp shadows.
a level macro view, 100mm macro lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-fangs-tongue-b　seed 10102

```text
微距特写，一个生物体独自占据画面：它张着夹子、内面朝向镜头：
a Venus flytrap with a row of sharp white mammal fangs along the trap edges and a long pink mammal
tongue curling out of the trap,
two wide-open trap lobes and a red inner surface.
in a bog just after rain, water beading on the lobes.
hard side light after the rain, crisp shadows.
a level macro view, 100mm macro lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

## R7 · Period 05 finale [carnivorous plant]: broad-leaf-blade base + mammal fangs T1 + eye T2 + tongue T4; dawn mist over the bog, backlit wide landscape

- Engine: `zimage`　Size: 1280×1024　steps: 12　Shared seed: 10101
- Images: 3 (one independent request each)

**Constant layer within the round** (shared by all images, so that A/B/C differ only in the spliced clause)

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-flytrap　seed 10101

```text
微距特写，一个生物体独自占据画面：一整丛捕蝇草张着夹子、朝向镜头：
a Venus flytrap with broad flat leaf blades and two wide-open trap lobes with a red inner surface.
in a misty bog at dawn, several traps in the frame.
low backlight through the mist, the red inner surfaces glowing.
a wide macro view, 45mm lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-all3　seed 10101

```text
微距特写，一个生物体独自占据画面：一整丛捕蝇草张着夹子、朝向镜头：
a Venus flytrap with a row of sharp white mammal fangs along the trap edges and a glossy dark
animal eye on the leaf blade and a long pink mammal tongue curling out of the trap,
broad flat leaf blades and two wide-open trap lobes with a red inner surface.
in a misty bog at dawn, several traps in the frame.
low backlight through the mist, the red inner surfaces glowing.
a wide macro view, 45mm lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### flytrap-all3-b　seed 10102

```text
微距特写，一个生物体独自占据画面：一整丛捕蝇草张着夹子、朝向镜头：
a Venus flytrap with a row of sharp white mammal fangs along the trap edges and a glossy dark
animal eye on the leaf blade and a long pink mammal tongue curling out of the trap,
broad flat leaf blades and two wide-open trap lobes with a red inner surface.
in a misty bog at dawn, several traps in the frame.
low backlight through the mist, the red inner surfaces glowing.
a wide macro view, 45mm lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

