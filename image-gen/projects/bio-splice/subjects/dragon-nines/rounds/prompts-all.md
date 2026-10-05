# 全部轮次原始 Prompt 存档

> 本文件由 `python3 run_round.py --prompts` 自动生成，内容 = **实际提交给 ComfyUI 的字符串**。
> 为便于查阅与逐轮对照，代码块内已按分句换行；**换行符不属于 prompt，仅排版**。
> 还原规则：行尾是 ASCII 字符时，该换行等于一个空格；否则换行处原本没有字符。
> `run_round.py` 的 `unwrap_prompt()` 就是这条规则，生成时会逐条断言「还原 == 原文」。
> 逐字原文（单行）见 `run_round.py` 的常量（`python3 run_round.py <N> --dry` 可直接打印）
> 与 `work/rN/round.json`；最终依据是服务器 `GET /history/{prompt_id}`。
> 修改 prompt 请改 `subjects/<子主题>/rounds.py`，然后重新生成本文件。
> 返回[子主题首页](../README.md) ｜ [项目首页](../../../README.md)

## 记录在哪（三层）

| 层 | 位置 | 内容 |
|----|------|------|
| 权威源 | `subjects/<子主题>/rounds.py` | 逐字 prompt（真正发出去的，单行） |
| 可读文档 | 本文件 / `docs/rN.md` | 分句换行的 prompt 全文；每轮改动与自检 |
| 机器记录 | `work/rN/round.json` | 文件名 / seed / prompt_id / 引擎 / 参数 / **prompt 原文** |
| 服务器侧 | `GET /history/{prompt_id}` | ComfyUI 实际执行的完整图（最终依据） |

## R1 · 九似·第一期候选：蛇底座 + 鹿角（D1，龙最强的标志）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R2 · 九似·第二期候选：蜥蜴底座（有四肢）+ 鹰爪 D7 / 虎掌 D8；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R3 · 九似·第三期候选：鱼鳞 D6（把底座里鳞的描述删掉腾出占位）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R4 · 九似·第四期候选【合龙】：蜥蜴底座 + 3 处 / 4 处部件叠加；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R5 · 期 02 定稿【卵石河滩·低机位聚焦前足】：蜥蜴底座 + 鹰爪 D7（+虎掌 D8）

- 引擎：`zimage`　尺寸：1024×1280　steps：12　共用 seed：4201
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R6 · 期 03 定稿【林下枯叶·侧俯贴体看鳞】：蛇底座（腾出鳞占位）+ 鱼鳞 D6（+鹿角 D1）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R7 · 期 04 定稿【雨中岩石·黄昏逆光】合龙：蜥蜴底座 + 角/耳/爪/掌

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：4201
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R8 · 期 05 收官【九似小成】：蛇底座（腾出头+眼占位）+ 驼头 D2 / 兔眼 D3（2×2 消融）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R9 · 期 05 候选【龙首特写】：测「底座物种名词=占位」；另出角/耳/鳞的龙首特写

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：5（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R10 · 期 05 定稿【龙首特写】：蛇底座（特写）+ 角 D1 / 耳 D9（+鳞 D6）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：4201
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

