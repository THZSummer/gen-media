# 全部轮次原始 Prompt 存档

> 🌐 语言：**中文** ｜ [English](prompts-all.en.md)

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

## R1 · 捕蝇草·第一期候选【占用版】：底座照常写硬齿 + 兽牙 T1（含同轮底座对照）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：10101
- 张数：2（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R2 · 捕蝇草·第一期对照【腾出版】：底座不写硬齿 + 兽牙 T1（含同轮底座对照）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：10101
- 张数：2（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R3 · 期 01 定稿【有牙的捕蝇草】：底座不写缘齿 + 兽牙 T1（三个 seed）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：10101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R4 · 期 02 定稿【有眼的捕蝇草】：宽叶面底座 + 眼 T2（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：10101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R5 · 期 03 定稿【吐信的捕蝇草】：宽叶面底座 + 舌 T4（两个 take）；苔藓低机位竖幅

- 引擎：`zimage`　尺寸：1024×1280　steps：12　共用 seed：10101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R6 · 期 04 定稿【牙舌俱全】：底座不写缘齿 + 兽牙 T1 + 舌 T4（两个 take）；雨后硬侧光

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：10101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

## R7 · 期 05 收官【食肉植物】：宽叶面底座 + 兽牙 T1 + 眼 T2 + 舌 T4；晨雾沼泽逆光广角横幅

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：10101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

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

