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

## R1 · 虫草·第一期候选：蛾幼虫底座 + 菌丝覆体 MY1 / 单根子座 ST1（含同轮底座对照）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：9101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R2 · 虫草·第一期对照【腾出版】：底座不写体表质感 + 菌丝覆体 MY1；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：9101
- 张数：2（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R3 · 期 01 定稿【菌丝覆体】：底座不写体表质感 + MY1（三个 seed）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：9101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R4 · 期 02 定稿【单根子座】：蛾幼虫底座 + 单根 ST1（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1280　steps：12　共用 seed：9101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R5 · 期 03 定稿【多根子座】：蛾幼虫底座 + 多根 ST1x；逆光 · 方（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：9101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R6 · 期 04 定稿【子座与孢子】：蛾幼虫底座 + 单根 ST1 + 孢子 SP1；雪线冷光 · 横；含同轮底座对照

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：9101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R7 · 期 05 收官【冬虫夏草·标本照】：蛾幼虫 + 菌丝覆体 MY1 + 子座 ST1 + 孢子 SP1；中性背景环形光（两个 take）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：9101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

