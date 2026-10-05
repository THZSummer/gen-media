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

## R1 · 鹿鹤·第一期候选：鹿底座（腾出颈位）+ 鹤的长颈 G1（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：7101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它站在雾里、正面朝向镜头：a red deer with a slender head, large ears,
a smooth reddish-brown coat, four long legs and a short tail.
in a misty bamboo grove, thin fog drifting between the stems.
soft diffuse morning light.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-craneneck　seed 7101

```text
全身像，一只动物独自占据画面：它站在雾里、正面朝向镜头：
a red deer with a long slender crane's neck with fine grey feathers, a slender head, large ears,
a smooth reddish-brown coat, four long legs and a short tail.
in a misty bamboo grove, thin fog drifting between the stems.
soft diffuse morning light.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-craneneck-b　seed 7102

```text
全身像，一只动物独自占据画面：它站在雾里、正面朝向镜头：
a red deer with a long slender crane's neck with fine grey feathers, a slender head, large ears,
a smooth reddish-brown coat, four long legs and a short tail.
in a misty bamboo grove, thin fog drifting between the stems.
soft diffuse morning light.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R2 · 鹿鹤·第二期候选【腾出版】：鹿底座（不写腿）+ 鹤的细腿 G2；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：7101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它在浅水里走着、侧身朝向镜头：a red deer with a slender head,
large ears, a smooth reddish-brown coat and a short tail.
in shallow marsh water among reeds, ripples around its feet.
low morning sun raking across the water.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranelegs　seed 7101

```text
全身像，一只动物独自占据画面：它在浅水里走着、侧身朝向镜头：
a red deer with a pair of long thin crane's legs, a slender head, large ears,
a smooth reddish-brown coat and a short tail.
in shallow marsh water among reeds, ripples around its feet.
low morning sun raking across the water.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranelegs-b　seed 7102

```text
全身像，一只动物独自占据画面：它在浅水里走着、侧身朝向镜头：
a red deer with a pair of long thin crane's legs, a slender head, large ears,
a smooth reddish-brown coat and a short tail.
in shallow marsh water among reeds, ripples around its feet.
low morning sun raking across the water.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R3 · 鹿鹤·第二期对照【占用版】：鹿底座（照常写 four long legs）+ 鹤的细腿 G2；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：7101
- 张数：2（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它在浅水里走着、侧身朝向镜头：a red deer with a slender head,
large ears, a smooth reddish-brown coat, four long legs and a short tail.
in shallow marsh water among reeds, ripples around its feet.
low morning sun raking across the water.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranelegs　seed 7101

```text
全身像，一只动物独自占据画面：它在浅水里走着、侧身朝向镜头：
a red deer with a pair of long thin crane's legs, a slender head, large ears,
a smooth reddish-brown coat, four long legs and a short tail.
in shallow marsh water among reeds, ripples around its feet.
low morning sun raking across the water.
Photograph, a level camera at eye height, 400mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R4 · 鹿鹤·第三期候选：鹿底座（不写尾）+ 鹤的尾羽 G6（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：7101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：a red deer with a slender head,
large ears, a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranetait　seed 7101

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：
a red deer with a fan of long white crane tail feathers, a slender head, large ears,
a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranetait-b　seed 7102

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：
a red deer with a fan of long white crane tail feathers, a slender head, large ears,
a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R5 · 鹿鹤·第四期候选【颈腿俱全】：鹿底座（不写腿）+ 鹤颈 G1 + 鹤腿 G2；含同轮底座对照

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：7101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它立在结霜的草地上、侧身朝向镜头：a red deer with a slender head,
large ears, a smooth reddish-brown coat and a short tail.
on a frost-covered meadow at first light.
cold low light, frost glittering on the grass.
Photograph, a level camera at eye height, 400mm lens at f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### deer-neck-legs　seed 7101

```text
全身像，一只动物独自占据画面：它立在结霜的草地上、侧身朝向镜头：
a red deer with a long slender crane's neck with fine grey feathers and a pair of long thin crane's
legs,
a slender head, large ears, a smooth reddish-brown coat and a short tail.
on a frost-covered meadow at first light.
cold low light, frost glittering on the grass.
Photograph, a level camera at eye height, 400mm lens at f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### deer-neck-legs-b　seed 7102

```text
全身像，一只动物独自占据画面：它立在结霜的草地上、侧身朝向镜头：
a red deer with a long slender crane's neck with fine grey feathers and a pair of long thin crane's
legs,
a slender head, large ears, a smooth reddish-brown coat and a short tail.
on a frost-covered meadow at first light.
cold low light, frost glittering on the grass.
Photograph, a level camera at eye height, 400mm lens at f/4, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R6 · 鹿鹤·第五期收官【鹿鹤同春】：鹿底座（不写腿尾）+ 鹤颈 G1 + 鹤腿 G2 + 鹤尾羽 G6；含同轮底座对照

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：7101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它站在花树下、身体横向展开：a red deer with a slender head,
large ears and a smooth reddish-brown coat.
under blossoming plum trees in spring, petals drifting down.
soft diffused light through the blossom.
Photograph, a wide-angle 35mm lens at eye height, f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-crane-3parts　seed 7101

```text
全身像，一只动物独自占据画面：它站在花树下、身体横向展开：
a red deer with a long slender crane's neck with fine grey feathers and a pair of long thin crane's
legs and a fan of long white crane tail feathers,
a slender head, large ears and a smooth reddish-brown coat.
under blossoming plum trees in spring, petals drifting down.
soft diffused light through the blossom.
Photograph, a wide-angle 35mm lens at eye height, f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-crane-3parts-b　seed 7102

```text
全身像，一只动物独自占据画面：它站在花树下、身体横向展开：
a red deer with a long slender crane's neck with fine grey feathers and a pair of long thin crane's
legs and a fan of long white crane tail feathers,
a slender head, large ears and a smooth reddish-brown coat.
under blossoming plum trees in spring, petals drifting down.
soft diffused light through the blossom.
Photograph, a wide-angle 35mm lens at eye height, f/4, the whole animal in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

## R7 · 鹿鹤·第三期定稿（补 take）：鹿底座（不写尾）+ 鹤的尾羽 G6（三个 seed）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：7101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
Photograph, <镜头>, fine surface detail, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-deer　seed 7101

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：a red deer with a slender head,
large ears, a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranetait　seed 7101

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：
a red deer with a fan of long white crane tail feathers, a slender head, large ears,
a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranetait-c　seed 7103

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：
a red deer with a fan of long white crane tail feathers, a slender head, large ears,
a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

### deer-cranetait-d　seed 7104

```text
全身像，一只动物独自占据画面：它站在苇丛里、侧身朝向镜头：
a red deer with a fan of long white crane tail feathers, a slender head, large ears,
a smooth reddish-brown coat and four long legs.
among tall reeds at the edge of a marsh.
strong backlight through the reed heads.
Photograph, a level camera at eye height, 600mm lens at f/4, the whole body in frame,
fine surface detail, slight film grain, no digital sharpening, no text, no watermark.
```

