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

## R1 · 玄武·第一期候选：龟底座 + 蛇颈 N1 / 蛇尾 N2 / 缠体 N3（含同轮底座对照）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：5101
- 张数：5（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Wildlife photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-turtle　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-snakeneck　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-snaketail　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a long tapering snake's tail with keeled scales, a dark domed shell,
a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-coil　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with the thick coiled body of a large snake wrapped around its shell,
a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-neck-tail　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales and a long
tapering snake's tail with keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R2 · 玄武·第三期候选：缠体 N3 的三种写法（环绕壳沿 / 盘在身下石面 / 最短式）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：5101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Wildlife photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-turtle　seed 5101

```text
全身像，一只动物独自占据画面：它伏在井边的石台上、龟壳朝向镜头：
a large wild river turtle with a dark domed shell, a small wrinkled head, four short webbed legs.
on a mossy stone ledge beside an old stone well.
hard side light raking across the shell.
Wildlife photograph, a view from slightly above, 100mm lens at f/5.6, the whole shell in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### coil-rim　seed 5101

```text
全身像，一只动物独自占据画面：它伏在井边的石台上、龟壳朝向镜头：
a large wild river turtle with thick snake coils around the rim of its shell, a dark domed shell,
a small wrinkled head, four short webbed legs.
on a mossy stone ledge beside an old stone well.
hard side light raking across the shell.
Wildlife photograph, a view from slightly above, 100mm lens at f/5.6, the whole shell in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### coil-ground　seed 5101

```text
全身像，一只动物独自占据画面：它伏在井边的石台上、龟壳朝向镜头：
a large wild river turtle with a thick snake's body coiled on the stones beneath it,
its coils visible on both sides, a dark domed shell, a small wrinkled head, four short webbed legs.
on a mossy stone ledge beside an old stone well.
hard side light raking across the shell.
Wildlife photograph, a view from slightly above, 100mm lens at f/5.6, the whole shell in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### coil-min　seed 5101

```text
全身像，一只动物独自占据画面：它伏在井边的石台上、龟壳朝向镜头：
a large wild river turtle with thick snake coils around its shell, a dark domed shell,
a small wrinkled head, four short webbed legs.
on a mossy stone ledge beside an old stone well.
hard side light raking across the shell.
Wildlife photograph, a view from slightly above, 100mm lens at f/5.6, the whole shell in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R3 · 期 01 定稿【溪石浅滩·晨光·平视 600mm】：龟底座 + 蛇颈 N1（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：5101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Wildlife photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-turtle　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-snakeneck　seed 5101

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-snakeneck-b　seed 5102

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### turtle-snakeneck-c　seed 5103

```text
全身像，一只动物独自占据画面：它从水里爬上溪石、正面朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on wet river stones at the edge of a shallow stream in early morning.
soft low morning light.
Wildlife photograph, a level camera at eye height, 600mm telephoto lens at f/4,
the whole body in frame, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

## R4 · 期 02 定稿【湿地泥岸·阴天·平视全身 400mm】：龟底座 + 蛇尾 N2（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：5101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Wildlife photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-turtle　seed 5101

```text
全身像，一只动物独自占据画面：它正在泥岸上爬行、侧身朝向镜头：
a large wild river turtle with a dark domed shell, a small wrinkled head, four short webbed legs.
on the muddy bank of a marsh pool, wet silt and trampled reeds.
flat overcast light.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### turtle-snaketail　seed 5101

```text
全身像，一只动物独自占据画面：它正在泥岸上爬行、侧身朝向镜头：
a large wild river turtle with a long tapering snake's tail with keeled scales, a dark domed shell,
a small wrinkled head, four short webbed legs.
on the muddy bank of a marsh pool, wet silt and trampled reeds.
flat overcast light.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### turtle-snaketail-b　seed 5102

```text
全身像，一只动物独自占据画面：它正在泥岸上爬行、侧身朝向镜头：
a large wild river turtle with a long tapering snake's tail with keeled scales, a dark domed shell,
a small wrinkled head, four short webbed legs.
on the muddy bank of a marsh pool, wet silt and trampled reeds.
flat overcast light.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### turtle-snaketail-c　seed 5103

```text
全身像，一只动物独自占据画面：它正在泥岸上爬行、侧身朝向镜头：
a large wild river turtle with a long tapering snake's tail with keeled scales, a dark domed shell,
a small wrinkled head, four short webbed legs.
on the muddy bank of a marsh pool, wet silt and trampled reeds.
flat overcast light.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R5 · 期 04 定稿【雨后溪石·逆光·平视 400mm·横】：龟底座 + 蛇颈 N1 + 蛇尾 N2；含同轮底座对照

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：5101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Wildlife photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-turtle　seed 5101

```text
全身像，一只动物独自占据画面：它伏在湿石上、侧身朝向镜头：
a large wild river turtle with a dark domed shell, a small wrinkled head, four short webbed legs.
on rain-soaked stones in a mountain stream.
backlight through the spray, rimming its outline.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### turtle-neck-tail　seed 5101

```text
全身像，一只动物独自占据画面：它伏在湿石上、侧身朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales and a long
tapering snake's tail with keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on rain-soaked stones in a mountain stream.
backlight through the spray, rimming its outline.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### turtle-neck-tail-b　seed 5102

```text
全身像，一只动物独自占据画面：它伏在湿石上、侧身朝向镜头：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales and a long
tapering snake's tail with keeled scales,
a dark domed shell, a small wrinkled head, four short webbed legs.
on rain-soaked stones in a mountain stream.
backlight through the spray, rimming its outline.
Wildlife photograph, a level camera at eye height, 400mm lens at f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R6 · 期 05 收官【玄武】：龟底座 + 蛇颈 N1 + 蛇尾 N2 + 缠体 N3；暮色水面·平视广角·横幅

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：5101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Wildlife photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-turtle　seed 5101

```text
全身像，一只动物独自占据画面：它伏在水边的石台上、身体横向展开：
a large wild river turtle with a dark domed shell, a small wrinkled head, four short webbed legs.
on a flat stone at the edge of dark water at dusk.
low backlight from across the water, throwing the animal into near-silhouette.
Wildlife photograph, a wide-angle 35mm lens at eye height, f/4,
the whole animal and its reflection in frame, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### turtle-all3　seed 5101

```text
全身像，一只动物独自占据画面：它伏在水边的石台上、身体横向展开：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales and a long
tapering snake's tail with keeled scales and thick snake coils around its shell,
a dark domed shell, a small wrinkled head, four short webbed legs.
on a flat stone at the edge of dark water at dusk.
low backlight from across the water, throwing the animal into near-silhouette.
Wildlife photograph, a wide-angle 35mm lens at eye height, f/4,
the whole animal and its reflection in frame, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

### turtle-all3-b　seed 5102

```text
全身像，一只动物独自占据画面：它伏在水边的石台上、身体横向展开：
a large wild river turtle with a long sinuous snake's neck with fine keeled scales and a long
tapering snake's tail with keeled scales and thick snake coils around its shell,
a dark domed shell, a small wrinkled head, four short webbed legs.
on a flat stone at the edge of dark water at dusk.
low backlight from across the water, throwing the animal into near-silhouette.
Wildlife photograph, a wide-angle 35mm lens at eye height, f/4,
the whole animal and its reflection in frame, fine surface detail, slight film grain,
no digital sharpening, no text, no watermark.
```

