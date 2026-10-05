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

## R1 · 花鸟·第一期候选：底座腾出花瓣环 + 鸟羽的三种写法（含同轮底座对照）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：11101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-feathers-rel　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with broad pale bird feathers in place of the petals,
a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-feathers-ring　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with a ring of broad pale bird feathers, a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-feathers-coat　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with broad pale bird feathers covering the flower,
a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R2 · 花鸟·第一期对照【占用版】：底座照常写花瓣 + 鸟羽（含同轮底座对照）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：11101
- 张数：2（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with broad rounded petals and a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-feathers　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with a ring of broad pale bird feathers,
broad rounded petals and a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R3 · 花鸟·第二期候选【绒心的花】：底座腾出花心 + 绒羽 P5；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：11101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with broad rounded petals.
on a spring branch, dew on the petals.
raking side light picking out the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-down　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with a tuft of soft downy bird feathers in the centre of the flower,
broad rounded petals.
on a spring branch, dew on the petals.
raking side light picking out the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-down-b　seed 11102

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with a tuft of soft downy bird feathers in the centre of the flower,
broad rounded petals.
on a spring branch, dew on the petals.
raking side light picking out the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R4 · 花鸟·第三期候选【翎梗的花】：底座 + 翎羽 P6（从花梗生出）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：11101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a large white magnolia flower with broad rounded petals and a ring of pale stamens.
on a spring branch among new leaves.
soft light against a dark background.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem,
broad rounded petals and a ring of pale stamens.
on a spring branch among new leaves.
soft light against a dark background.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume-b　seed 11102

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem,
broad rounded petals and a ring of pale stamens.
on a spring branch among new leaves.
soft light against a dark background.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R5 · 期 01 定稿【翎枝的花】：玉兰 + 翎羽 P6（三个 seed）；晨露柔光微距；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：11101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with broad rounded petals and a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem,
broad rounded petals and a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume-b　seed 11102

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem,
broad rounded petals and a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume-c　seed 11103

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem,
broad rounded petals and a ring of pale stamens.
on a spring branch, dew on the petals.
soft diffused morning light.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R6 · 期 03 定稿【翎绒俱全】：玉兰 + 翎羽 P6 + 绒羽 P5（两个 take）；暗背景硬光

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：11101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with broad rounded petals and a ring of pale stamens.
against a dark blurred background of twigs.
hard light from one side, the background falling to near-black.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume-down　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem and a tuft of
soft downy bird feathers in the centre of the flower,
broad rounded petals and a ring of pale stamens.
against a dark blurred background of twigs.
hard light from one side, the background falling to near-black.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### flower-plume-down-b　seed 11102

```text
微距特写，一个生物体独自占据画面：它开在枝头、正面朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem and a tuft of
soft downy bird feathers in the centre of the flower,
broad rounded petals and a ring of pale stamens.
against a dark blurred background of twigs.
hard light from one side, the background falling to near-black.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R7 · 期 04 定稿【百合的绒与翎】：百合底座 + 绒羽 P5 + 翎羽 P6（两个 take）；逆光竖幅

- 引擎：`zimage`　尺寸：1024×1280　steps：12　共用 seed：11101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### lily-down-plume　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with a tuft of soft downy bird feathers in the centre of the flower and long
pale bird plume feathers rising from the stem,
six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### lily-down-plume-b　seed 11102

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with a tuft of soft downy bird feathers in the centre of the flower and long
pale bird plume feathers rising from the stem,
six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

## R8 · 期 05 收官【花鸟】：玉兰 + 翎羽 P6 + 绒羽 P5（两个 take）；满枝逆光广角横幅

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：11101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：一枝上开着好几朵、整体朝向镜头：
a large white magnolia flower with broad rounded petals and a ring of pale stamens.
a whole flowering branch in a spring grove.
warm low backlight, the plumes glowing.
a wide macro view, 45mm lens at f/11, macro photograph, fine surface detail, soft natural colour,
no digital sharpening, no text, no watermark.
```

### flower-bird　seed 11101

```text
微距特写，一个生物体独自占据画面：一枝上开着好几朵、整体朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem and a tuft of
soft downy bird feathers in the centre of the flower,
broad rounded petals and a ring of pale stamens.
a whole flowering branch in a spring grove.
warm low backlight, the plumes glowing.
a wide macro view, 45mm lens at f/11, macro photograph, fine surface detail, soft natural colour,
no digital sharpening, no text, no watermark.
```

### flower-bird-b　seed 11102

```text
微距特写，一个生物体独自占据画面：一枝上开着好几朵、整体朝向镜头：
a large white magnolia flower with long pale bird plume feathers rising from the stem and a tuft of
soft downy bird feathers in the centre of the flower,
broad rounded petals and a ring of pale stamens.
a whole flowering branch in a spring grove.
warm low backlight, the plumes glowing.
a wide macro view, 45mm lens at f/11, macro photograph, fine surface detail, soft natural colour,
no digital sharpening, no text, no watermark.
```

## R9 · 期 04 定稿（补 take）【百合的绒与翎】：百合底座 + 绒羽 P5 + 翎羽 P6（三个 seed）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1280　steps：12　共用 seed：11101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, fine surface detail, soft natural colour, no digital sharpening, no text,
no watermark.
```

### base-flower　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### lily-down-plume　seed 11101

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with a tuft of soft downy bird feathers in the centre of the flower and long
pale bird plume feathers rising from the stem,
six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### lily-down-plume-c　seed 11103

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with a tuft of soft downy bird feathers in the centre of the flower and long
pale bird plume feathers rising from the stem,
six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

### lily-down-plume-d　seed 11104

```text
微距特写，一个生物体独自占据画面：它开在枝头、侧面朝向镜头：
a white lily flower with a tuft of soft downy bird feathers in the centre of the flower and long
pale bird plume feathers rising from the stem,
six long recurved petals.
on a leafy stem in a spring garden.
strong backlight through the petals.
a level macro view, 100mm macro lens at f/8, macro photograph, fine surface detail,
soft natural colour, no digital sharpening, no text, no watermark.
```

