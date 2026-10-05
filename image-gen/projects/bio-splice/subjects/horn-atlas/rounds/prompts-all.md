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

## R1 · 角图鉴·第一部分【无角基准】：统一底座（三个 take），作为后四部分的参照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：14101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-horse　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
soft diffused light through the mist.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### base-horse-b　seed 14102

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
soft diffused light through the mist.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### base-horse-c　seed 14103

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
soft diffused light through the mist.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R2 · 角图鉴·第二部分【鹿角】：统一底座 + 分叉鹿角（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：14101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-horse　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
low side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-antlers　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：
a bay horse with a pair of branching deer antlers rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
low side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-antlers-b　seed 14102

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：
a bay horse with a pair of branching deer antlers rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
low side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R3 · 角图鉴·第三部分【牛角】：统一底座 + 粗壮牛角（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：14101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-horse　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
flat top light, the coat dull and even.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-oxhorns　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：
a bay horse with a pair of thick curved ox horns rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
flat top light, the coat dull and even.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-oxhorns-b　seed 14102

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：
a bay horse with a pair of thick curved ox horns rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
flat top light, the coat dull and even.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R4 · 角图鉴·第四部分【羊角】：统一底座 + 卷曲羊角（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：14101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-horse　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
low side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-ramhorns　seed 14101

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：
a bay horse with a pair of curled ram horns rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
low side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-ramhorns-b　seed 14102

```text
全身像，一只动物独自占据画面：它立在雾里、侧身朝向镜头：
a bay horse with a pair of curled ram horns rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
in a misty meadow at dawn.
low side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R5 · 角图鉴·第五部分【独角鲸长牙 / 犀角】：统一底座 + 两种单支角（各一张）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1280　steps：12　共用 seed：14101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-horse　seed 14101

```text
头部特写，一只动物独自占据画面：它抬起头、正面朝向镜头：a bay horse with a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
on frost-covered grassland at first light.
low side-backlight, frost glittering.
a tight portrait of the head, 200mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-narwhal　seed 14101

```text
头部特写，一只动物独自占据画面：它抬起头、正面朝向镜头：
a bay horse with a single long spiral narwhal tusk rising from its forehead, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
on frost-covered grassland at first light.
low side-backlight, frost glittering.
a tight portrait of the head, 200mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### horse-rhino　seed 14102

```text
头部特写，一只动物独自占据画面：它抬起头、正面朝向镜头：
a bay horse with a single heavy rhinoceros horn rising from its nose, a long dark mane,
a dark muzzle, four slender legs and a flowing tail.
on frost-covered grassland at first light.
low side-backlight, frost glittering.
a tight portrait of the head, 200mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

