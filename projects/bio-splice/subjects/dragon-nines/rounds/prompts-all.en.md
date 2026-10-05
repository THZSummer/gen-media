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

## R1 · nine resemblances · period 01 candidates: snake base + deer antlers (D1, the dragon's strongest marker); includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 4 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<底座 with 部位>.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-snake　seed 4201

```text
全身像，一只动物独自占据画面：a large wild snake with its head raised, a blunt scaled head,
dark lidless eyes, a flickering forked tongue, keeled scales along a long muscular body.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### snake-antler　seed 4201

```text
全身像，一只动物独自占据画面：a large wild snake with a pair of branching deer antlers,
its head raised, a blunt scaled head, dark lidless eyes, a flickering forked tongue,
keeled scales along a long muscular body.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### snake-antler-oxear　seed 4201

```text
全身像，一只动物独自占据画面：
a large wild snake with a pair of branching deer antlers and a small pointed ox's ear,
its head raised, a blunt scaled head, dark lidless eyes, a flickering forked tongue,
keeled scales along a long muscular body.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### snake-antler-claw　seed 4201

```text
全身像，一只动物独自占据画面：
a large wild snake with a pair of branching deer antlers and sharp curved eagle talons on the front
limbs,
its head raised, a blunt scaled head, dark lidless eyes, a flickering forked tongue,
keeled scales along a long muscular body.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R2 · nine resemblances · period 02 candidates: lizard base (with limbs) + eagle talons D7 / tiger paws D8; includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<底座 with 部位>.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-lizard　seed 4201

```text
全身像，一只动物独自占据画面：a large monitor lizard with its head raised, a blunt scaled snout,
dark lidless eyes, a flickering forked tongue, four stout legs and a long tapering tail.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### lizard-talons　seed 4201

```text
全身像，一只动物独自占据画面：
a large monitor lizard with sharp curved eagle talons on its front feet, its head raised,
a blunt scaled snout, dark lidless eyes, a flickering forked tongue,
four stout legs and a long tapering tail.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### lizard-talons-paws　seed 4201

```text
全身像，一只动物独自占据画面：
a large monitor lizard with sharp curved eagle talons on its front feet and broad tiger paws with
heavy pads on its hind feet,
its head raised, a blunt scaled snout, dark lidless eyes, a flickering forked tongue,
four stout legs and a long tapering tail.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R3 · nine resemblances · period 03 candidates: fish scales D6 (delete the scale description from the base to free the placeholder); includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<底座 with 部位>.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-snake-clean　seed 4201

```text
全身像，一只动物独自占据画面：a large wild snake with its head raised, a blunt head,
dark lidless eyes, a flickering forked tongue, and a long smooth muscular body.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### snake-fishscale　seed 4201

```text
全身像，一只动物独自占据画面：a large wild snake with large overlapping fish scales,
its head raised, a blunt head, dark lidless eyes, a flickering forked tongue,
and a long smooth muscular body.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### snake-fishscale-antler　seed 4201

```text
全身像，一只动物独自占据画面：
a large wild snake with a pair of branching deer antlers and large overlapping fish scales,
its head raised, a blunt head, dark lidless eyes, a flickering forked tongue,
and a long smooth muscular body.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R4 · nine resemblances · period 04 candidates [composite dragon]: lizard base + 3 / 4 stacked parts; includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<底座 with 部位>.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-lizard　seed 4201

```text
全身像，一只动物独自占据画面：a large monitor lizard with its head raised, a blunt scaled snout,
dark lidless eyes, a flickering forked tongue, four stout legs and a long tapering tail.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### dragon-3parts　seed 4201

```text
全身像，一只动物独自占据画面：
a large monitor lizard with a pair of branching deer antlers and sharp curved eagle talons on its
front feet and broad tiger paws with heavy pads on its hind feet,
its head raised, a blunt scaled snout, dark lidless eyes, a flickering forked tongue,
four stout legs and a long tapering tail.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### dragon-4parts　seed 4201

```text
全身像，一只动物独自占据画面：
a large monitor lizard with a pair of branching deer antlers and a small pointed ox's ear and sharp
curved eagle talons on its front feet and broad tiger paws with heavy pads on its hind feet,
its head raised, a blunt scaled snout, dark lidless eyes, a flickering forked tongue,
four stout legs and a long tapering tail.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R5 · period 02 final [pebble riverbank · low camera focused on the front feet]: lizard base + eagle talons D7 (+ tiger paws D8)

- Engine: `zimage`　Size: 1024×1280　steps: 12　shared seed: 4201
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<底座 with 部位>.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-lizard　seed 4201

```text
全身像，一只动物独自占据画面：它以后肢撑起上身、两前足抬起张开：
a large monitor lizard with its head raised, a blunt scaled snout, dark lidless eyes,
a flickering forked tongue, four stout legs and a long tapering tail.
on a wet pebble riverbank just after rain, water still sheeting over the stones.
wet overcast light with a soft backlight rimming its body.
Wildlife photograph, a low ground-level camera angle, 85mm lens at f/3.2,
very shallow depth of field, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### lizard-talons　seed 4201

```text
全身像，一只动物独自占据画面：它以后肢撑起上身、两前足抬起张开：
a large monitor lizard with sharp curved eagle talons on its front feet, its head raised,
a blunt scaled snout, dark lidless eyes, a flickering forked tongue,
four stout legs and a long tapering tail.
on a wet pebble riverbank just after rain, water still sheeting over the stones.
wet overcast light with a soft backlight rimming its body.
Wildlife photograph, a low ground-level camera angle, 85mm lens at f/3.2,
very shallow depth of field, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### lizard-talons-paws　seed 4201

```text
全身像，一只动物独自占据画面：它以后肢撑起上身、两前足抬起张开：
a large monitor lizard with sharp curved eagle talons on its front feet and broad tiger paws with
heavy pads on its hind feet,
its head raised, a blunt scaled snout, dark lidless eyes, a flickering forked tongue,
four stout legs and a long tapering tail.
on a wet pebble riverbank just after rain, water still sheeting over the stones.
wet overcast light with a soft backlight rimming its body.
Wildlife photograph, a low ground-level camera angle, 85mm lens at f/3.2,
very shallow depth of field, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

## R6 · period 03 final [forest floor leaf litter · side-high body-hugging view of the scales]: snake base (scale placeholder freed) + fish scales D6 (+ deer antlers D1)

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<底座 with 部位>.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-snake　seed 4201

```text
全身像，一只动物独自占据画面：它把身体平铺在地、整个背脊朝向镜头：
a large wild snake with its head raised, a blunt head, dark lidless eyes,
a flickering forked tongue, and a long smooth muscular body.
on damp leaf litter deep on a forest floor.
dappled light falling through the canopy.
Wildlife photograph, 100mm macro lens, side view from slightly above, f/5.6,
the whole length of the body in focus, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### snake-fishscale　seed 4201

```text
全身像，一只动物独自占据画面：它把身体平铺在地、整个背脊朝向镜头：
a large wild snake with large overlapping fish scales, its head raised, a blunt head,
dark lidless eyes, a flickering forked tongue, and a long smooth muscular body.
on damp leaf litter deep on a forest floor.
dappled light falling through the canopy.
Wildlife photograph, 100mm macro lens, side view from slightly above, f/5.6,
the whole length of the body in focus, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### snake-fishscale-antler　seed 4201

```text
全身像，一只动物独自占据画面：它把身体平铺在地、整个背脊朝向镜头：
a large wild snake with a pair of branching deer antlers and large overlapping fish scales,
its head raised, a blunt head, dark lidless eyes, a flickering forked tongue,
and a long smooth muscular body.
on damp leaf litter deep on a forest floor.
dappled light falling through the canopy.
Wildlife photograph, 100mm macro lens, side view from slightly above, f/5.6,
the whole length of the body in focus, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

## R7 · period 04 final [rain-soaked rock · dusk backlight] composite dragon: lizard base + antlers/ears/talons/paws

- Engine: `zimage`　Size: 1280×1024　steps: 12　shared seed: 4201
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<底座 with 部位>.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-lizard　seed 4201

```text
全身像，一只动物独自占据画面：它昂首挺立、四肢张开、全身展开：
a large monitor lizard with its head raised, a blunt scaled snout, dark lidless eyes,
a flickering forked tongue, four stout legs and a long tapering tail.
on a rain-slicked rock outcrop.
dusk backlight through falling rain, water beading along its back.
Wildlife photograph, a wide-angle 35mm lens at a low angle, f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### dragon-3parts　seed 4201

```text
全身像，一只动物独自占据画面：它昂首挺立、四肢张开、全身展开：
a large monitor lizard with a pair of branching deer antlers and sharp curved eagle talons on its
front feet and broad tiger paws with heavy pads on its hind feet,
its head raised, a blunt scaled snout, dark lidless eyes, a flickering forked tongue,
four stout legs and a long tapering tail.
on a rain-slicked rock outcrop.
dusk backlight through falling rain, water beading along its back.
Wildlife photograph, a wide-angle 35mm lens at a low angle, f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### dragon-4parts　seed 4201

```text
全身像，一只动物独自占据画面：它昂首挺立、四肢张开、全身展开：
a large monitor lizard with a pair of branching deer antlers and a small pointed ox's ear and sharp
curved eagle talons on its front feet and broad tiger paws with heavy pads on its hind feet,
its head raised, a blunt scaled snout, dark lidless eyes, a flickering forked tongue,
four stout legs and a long tapering tail.
on a rain-slicked rock outcrop.
dusk backlight through falling rain, water beading along its back.
Wildlife photograph, a wide-angle 35mm lens at a low angle, f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R8 · period 05 finale [nine resemblances partially achieved]: snake base (head + eye placeholders freed) + camel head D2 / rabbit eyes D3 (2×2 ablation)

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 4 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<底座 with 部位>.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-snake-open　seed 4201

```text
头部特写，一只动物独自占据画面：它昂起头颈、正面朝向镜头：a large wild snake with its neck lifted,
a flickering forked tongue, keeled scales along a long muscular body.
at the edge of a misty marsh before sunrise, the far bank lost in grey.
low side-backlight from the first light, rimming the outline of the head.
Wildlife photograph, a tight close-up portrait of the head and neck, 200mm lens at f/4,
the background dissolved into soft grey, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### snake-camelhead　seed 4201

```text
头部特写，一只动物独自占据画面：它昂起头颈、正面朝向镜头：
a large wild snake with an elongated camel's head with a blunt muzzle, its neck lifted,
a flickering forked tongue, keeled scales along a long muscular body.
at the edge of a misty marsh before sunrise, the far bank lost in grey.
low side-backlight from the first light, rimming the outline of the head.
Wildlife photograph, a tight close-up portrait of the head and neck, 200mm lens at f/4,
the background dissolved into soft grey, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### snake-rabbiteyes　seed 4201

```text
头部特写，一只动物独自占据画面：它昂起头颈、正面朝向镜头：
a large wild snake with a pair of round dark rabbit's eyes, its neck lifted,
a flickering forked tongue, keeled scales along a long muscular body.
at the edge of a misty marsh before sunrise, the far bank lost in grey.
low side-backlight from the first light, rimming the outline of the head.
Wildlife photograph, a tight close-up portrait of the head and neck, 200mm lens at f/4,
the background dissolved into soft grey, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### dragon-head-eyes　seed 4201

```text
头部特写，一只动物独自占据画面：它昂起头颈、正面朝向镜头：
a large wild snake with an elongated camel's head with a blunt muzzle and a pair of round dark
rabbit's eyes,
its neck lifted, a flickering forked tongue, keeled scales along a long muscular body.
at the edge of a misty marsh before sunrise, the far bank lost in grey.
low side-backlight from the first light, rimming the outline of the head.
Wildlife photograph, a tight close-up portrait of the head and neck, 200mm lens at f/4,
the background dissolved into soft grey, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

## R9 · period 05 candidates [dragon-head close-up]: testing "the base's species noun = a placeholder"; plus dragon-head close-ups with antlers/ears/scales

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 5 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<底座 with 部位>.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-nospecies　seed 4201

```text
头部特写，一只动物独自占据画面：它昂起头颈、正面朝向镜头：
a long muscular low body with keeled scales and a flickering forked tongue.
at the edge of a misty marsh before sunrise, the far bank lost in grey.
low side-backlight from the first light, rimming the outline of the head.
Wildlife photograph, a tight close-up portrait of the head and neck, 200mm lens at f/4,
the background dissolved into soft grey, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### nospecies-camelhead　seed 4201

```text
头部特写，一只动物独自占据画面：它昂起头颈、正面朝向镜头：
a long muscular low body with an elongated camel's head with a blunt muzzle,
keeled scales and a flickering forked tongue.
at the edge of a misty marsh before sunrise, the far bank lost in grey.
low side-backlight from the first light, rimming the outline of the head.
Wildlife photograph, a tight close-up portrait of the head and neck, 200mm lens at f/4,
the background dissolved into soft grey, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### nospecies-camelhead-eye　seed 4201

```text
头部特写，一只动物独自占据画面：它昂起头颈、正面朝向镜头：
a long muscular low body with an elongated camel's head with a blunt muzzle and a pair of round
dark rabbit's eyes,
keeled scales and a flickering forked tongue.
at the edge of a misty marsh before sunrise, the far bank lost in grey.
low side-backlight from the first light, rimming the outline of the head.
Wildlife photograph, a tight close-up portrait of the head and neck, 200mm lens at f/4,
the background dissolved into soft grey, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### snake-antler-oxear　seed 4201

```text
头部特写，一只动物独自占据画面：它昂起头颈、正面朝向镜头：
a large wild snake with a pair of branching deer antlers and a small pointed ox's ear,
its head raised, a blunt scaled head, dark lidless eyes, a flickering forked tongue,
keeled scales along a long muscular body.
at the edge of a misty marsh before sunrise, the far bank lost in grey.
low side-backlight from the first light, rimming the outline of the head.
Wildlife photograph, a tight close-up portrait of the head and neck, 200mm lens at f/4,
the background dissolved into soft grey, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### snake-antler-oxear-scale　seed 4201

```text
头部特写，一只动物独自占据画面：它昂起头颈、正面朝向镜头：
a large wild snake with a pair of branching deer antlers and a small pointed ox's ear and large
overlapping fish scales,
its head raised, a blunt head, dark lidless eyes, a flickering forked tongue,
and a long smooth muscular body.
at the edge of a misty marsh before sunrise, the far bank lost in grey.
low side-backlight from the first light, rimming the outline of the head.
Wildlife photograph, a tight close-up portrait of the head and neck, 200mm lens at f/4,
the background dissolved into soft grey, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

## R10 · period 05 final [dragon-head close-up]: snake base (close-up) + antlers D1 / ears D9 (+ scales D6); includes the same-round base control

- Engine: `zimage`　Size: 1024×1024　steps: 12　shared seed: 4201
- Images: 3 (each an independent request)

**In-round constant layer** (shared by all images, ensuring that A/B/C differ only in the splice sentence)

```text
全身像，一只动物独自占据画面：<底座 with 部位>.
among wet reeds at the edge of a misty marsh,
the background falling away into soft grey-green bokeh.
Wildlife photograph, 600mm telephoto lens, f/4, shallow depth of field, soft overcast daylight,
muted natural colour, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-snake　seed 4201

```text
头部特写，一只动物独自占据画面：它昂起头颈、正面朝向镜头：a large wild snake with its head raised,
a blunt scaled head, dark lidless eyes, a flickering forked tongue,
keeled scales along a long muscular body.
at the edge of a misty marsh before sunrise, the far bank lost in grey.
low side-backlight from the first light, rimming the outline of the head.
Wildlife photograph, a tight close-up portrait of the head and neck, 200mm lens at f/4,
the background dissolved into soft grey, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### dragon-head　seed 4201

```text
头部特写，一只动物独自占据画面：它昂起头颈、正面朝向镜头：
a large wild snake with a pair of branching deer antlers and a small pointed ox's ear,
its head raised, a blunt scaled head, dark lidless eyes, a flickering forked tongue,
keeled scales along a long muscular body.
at the edge of a misty marsh before sunrise, the far bank lost in grey.
low side-backlight from the first light, rimming the outline of the head.
Wildlife photograph, a tight close-up portrait of the head and neck, 200mm lens at f/4,
the background dissolved into soft grey, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### dragon-head-scale　seed 4201

```text
头部特写，一只动物独自占据画面：它昂起头颈、正面朝向镜头：
a large wild snake with a pair of branching deer antlers and a small pointed ox's ear and large
overlapping fish scales,
its head raised, a blunt head, dark lidless eyes, a flickering forked tongue,
and a long smooth muscular body.
at the edge of a misty marsh before sunrise, the far bank lost in grey.
low side-backlight from the first light, rimming the outline of the head.
Wildlife photograph, a tight close-up portrait of the head and neck, 200mm lens at f/4,
the background dissolved into soft grey, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

