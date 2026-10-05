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

## R1 · 鲲鹏·第一期候选：鱼底座（腾出胸鳍位）+ 鸟翼的三种写法；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：6101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with a long scaled body, a blunt head, small eyes,
a dorsal fin and a broad forked tail.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with broad feathered bird wings on both sides of its body, a long scaled body,
a blunt head, small eyes, a dorsal fin and a broad forked tail.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-flank　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with a pair of broad feathered bird wings along its flanks, a long scaled body,
a blunt head, small eyes, a dorsal fin and a broad forked tail.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-rel　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with broad feathered bird wings in place of its pectoral fins,
a long scaled body, a blunt head, small eyes, a dorsal fin and a broad forked tail.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R2 · 鲲鹏·第二期候选：鱼底座（腾出尾鳍位）+ 鸟尾羽的两种写法；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：6101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它悬在水中、身侧朝向镜头：a large wild carp with a long scaled body,
a blunt head, small eyes and four fins.
in dark water a little below the surface.
backlight coming down through the surface.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-tailfeathers　seed 6101

```text
全身像，一只动物独自占据画面：它悬在水中、身侧朝向镜头：
a large wild carp with a fan of long bird tail feathers, a long scaled body, a blunt head,
small eyes and four fins.
in dark water a little below the surface.
backlight coming down through the surface.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-tailfeathers-rel　seed 6101

```text
全身像，一只动物独自占据画面：它悬在水中、身侧朝向镜头：
a large wild carp with long bird tail feathers spreading where the tail fin would be,
a long scaled body, a blunt head, small eyes and four fins.
in dark water a little below the surface.
backlight coming down through the surface.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R3 · 鲲鹏·空位探针：翼从背上生出 / 尾羽在尾之上张开 / 羽覆背（同一底座）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：6101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with a long scaled body, a blunt head, small eyes and a dorsal fin.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-back　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with a pair of broad feathered bird wings rising from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-tail-above　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with a fan of long bird tail feathers rising above its tail, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-feathercoat　seed 6101

```text
全身像，一只动物独自占据画面：它悬停在水中、侧身朝向镜头：
a large wild carp with a covering of fine bird feathers over its back, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in shallow clear water over pale gravel.
soft side light through the water.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R4 · 鲲鹏·离水探针：同样的鱼底座 + 同样的三个部件，只把场景换到水面之上；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：6101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：a large wild carp with a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-back　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with a pair of broad feathered bird wings rising from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with broad feathered bird wings on both sides of its body, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-feathercoat　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with a covering of fine bird feathers over its back, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R5 · 鲲鹏·离水补齐：尾羽（尾位 / 尾上方）/ 羽覆背 / 翼+尾羽叠加；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：6101
- 张数：5（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：a large wild carp with a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-tail　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with a fan of long bird tail feathers, a long scaled body, a blunt head,
small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-tail-above　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with a fan of long bird tail feathers rising above its tail, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-feathercoat　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with a covering of fine bird feathers over its back, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-tail　seed 6101

```text
全身像，一只动物独自占据画面：它跃出水面、身体完全离水：
a large wild carp with broad feathered bird wings on both sides of its body and a fan of long bird
tail feathers,
a long scaled body, a blunt head, small eyes and a dorsal fin.
in open air above the water surface, spray falling away below it.
backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/5.6, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R6 · 期 01 定稿【跃出水面·水花未落】：鱼 + 鸟翼（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：6101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它刚从水里跃出、身体还在往上冲：
a large wild carp with a long scaled body, a blunt head, small eyes and a dorsal fin.
in open air just above the surface, spray still falling from its body.
low backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings　seed 6101

```text
全身像，一只动物独自占据画面：它刚从水里跃出、身体还在往上冲：
a large wild carp with broad feathered bird wings on both sides of its body, a long scaled body,
a blunt head, small eyes and a dorsal fin.
in open air just above the surface, spray still falling from its body.
low backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-spread　seed 6102

```text
全身像，一只动物独自占据画面：它刚从水里跃出、身体还在往上冲：
a large wild carp with a pair of broad feathered bird wings spread wide from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
in open air just above the surface, spray still falling from its body.
low backlight through the flying spray.
Photograph, a level view from the side, 100mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R7 · 期 02 定稿【半出水·水线穿过身体】：鱼 + 鸟翼（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：6101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with a long scaled body, a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings　seed 6101

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with broad feathered bird wings on both sides of its body, a long scaled body,
a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-half　seed 6103

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with a pair of broad feathered bird wings half-opened along its flanks,
a long scaled body, a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R8 · 期 03 定稿【完全离水·双翼全展·侧上方】：鱼 + 鸟翼（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：6101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它悬在空中、身体横向展开：a large wild carp with a long scaled body,
a blunt head, small eyes and a dorsal fin.
well above the water, only sky and a distant shoreline behind it.
strong backlight rimming every feather.
Photograph, a view from slightly above and to the side, 85mm lens at f/5.6, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-spread　seed 6101

```text
全身像，一只动物独自占据画面：它悬在空中、身体横向展开：
a large wild carp with a pair of broad feathered bird wings spread wide from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
well above the water, only sky and a distant shoreline behind it.
strong backlight rimming every feather.
Photograph, a view from slightly above and to the side, 85mm lens at f/5.6, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-spread-b　seed 6102

```text
全身像，一只动物独自占据画面：它悬在空中、身体横向展开：
a large wild carp with a pair of broad feathered bird wings spread wide from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
well above the water, only sky and a distant shoreline behind it.
strong backlight rimming every feather.
Photograph, a view from slightly above and to the side, 85mm lens at f/5.6, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R9 · 期 04 定稿【低空掠水·长焦压缩】：鱼 + 鸟翼（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：6101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它贴着水面低飞、身体近乎水平：
a large wild carp with a long scaled body, a blunt head, small eyes and a dorsal fin.
skimming low over open water, the far shore compressed behind it.
flat overcast light on grey water.
Photograph, a 400mm telephoto compressing the distance, f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings　seed 6101

```text
全身像，一只动物独自占据画面：它贴着水面低飞、身体近乎水平：
a large wild carp with broad feathered bird wings on both sides of its body, a long scaled body,
a blunt head, small eyes and a dorsal fin.
skimming low over open water, the far shore compressed behind it.
flat overcast light on grey water.
Photograph, a 400mm telephoto compressing the distance, f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-spread　seed 6103

```text
全身像，一只动物独自占据画面：它贴着水面低飞、身体近乎水平：
a large wild carp with a pair of broad feathered bird wings spread wide from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
skimming low over open water, the far shore compressed behind it.
flat overcast light on grey water.
Photograph, a 400mm telephoto compressing the distance, f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R10 · 期 05 收官【鲲鹏】：暮色海面逆光剪影 + 全展鸟翼（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：6101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它在暮色海面上高高跃起、双翼全展：
a large wild carp with a long scaled body, a blunt head, small eyes and a dorsal fin.
above a dark open sea at dusk, the horizon far behind.
low backlight throwing the whole animal into near-silhouette.
Photograph, a wide-angle 35mm lens at eye height, f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-spread　seed 6101

```text
全身像，一只动物独自占据画面：它在暮色海面上高高跃起、双翼全展：
a large wild carp with a pair of broad feathered bird wings spread wide from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
above a dark open sea at dusk, the horizon far behind.
low backlight throwing the whole animal into near-silhouette.
Photograph, a wide-angle 35mm lens at eye height, f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-spread-b　seed 6102

```text
全身像，一只动物独自占据画面：它在暮色海面上高高跃起、双翼全展：
a large wild carp with a pair of broad feathered bird wings spread wide from its back,
a long scaled body, a blunt head, small eyes and a dorsal fin.
above a dark open sea at dusk, the horizon far behind.
low backlight throwing the whole animal into near-silhouette.
Photograph, a wide-angle 35mm lens at eye height, f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R11 · 期 02 定稿（补 take）【半出水·水线穿过身体】：半张的翼在体侧偏上（三个 seed）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：6101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-fish　seed 6101

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with a long scaled body, a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-half　seed 6101

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with a pair of broad feathered bird wings half-opened along its flanks,
a long scaled body, a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-half-b　seed 6102

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with a pair of broad feathered bird wings half-opened along its flanks,
a long scaled body, a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### fish-wings-half-c　seed 6104

```text
全身像，一只动物独自占据画面：它半个身体还在水里、前半身已经抬起：
a large wild carp with a pair of broad feathered bird wings half-opened along its flanks,
a long scaled body, a blunt head, small eyes and a dorsal fin.
at the water surface, the waterline cutting across its body.
soft side light with the surface breaking into highlights.
Photograph, a level view from the side, 135mm lens at f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

