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

## R1 · 翅图鉴·第一部分【双翼基准】：只有统一底座（三个 take），作为后四部分的参照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：13101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、侧身朝向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a bare branch in a woodland clearing.
soft side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### base-bird-b　seed 13102

```text
全身像，一只动物独自占据画面：它停在枝头、侧身朝向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a bare branch in a woodland clearing.
soft side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### base-bird-c　seed 13103

```text
全身像，一只动物独自占据画面：它停在枝头、侧身朝向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a bare branch in a woodland clearing.
soft side-backlight rimming its outline.
a level view at eye height, 400mm lens at f/4, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R2 · 翅图鉴·第二部分【膜翅】：统一底座 + 昆虫膜翅（背上第二对，两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：13101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-membrane　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a pair of translucent insect membranous wings rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-membrane-b　seed 13102

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a pair of translucent insect membranous wings rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R3 · 翅图鉴·第三部分【皮翼】：统一底座 + 蝙蝠皮翼（背上第二对，两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：13101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它停在岩壁上、侧身朝向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
at the mouth of a dim limestone cave.
hard light from the cave mouth, deep shadows behind.
a level view at eye height, 300mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-bat　seed 13101

```text
全身像，一只动物独自占据画面：它停在岩壁上、侧身朝向镜头：
a medium-sized brown bird with a pair of leathery bat wings rising from its back, a rounded head,
a short dark beak, folded feathered wings and a long tail.
at the mouth of a dim limestone cave.
hard light from the cave mouth, deep shadows behind.
a level view at eye height, 300mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-bat-b　seed 13102

```text
全身像，一只动物独自占据画面：它停在岩壁上、侧身朝向镜头：
a medium-sized brown bird with a pair of leathery bat wings rising from its back, a rounded head,
a short dark beak, folded feathered wings and a long tail.
at the mouth of a dim limestone cave.
hard light from the cave mouth, deep shadows behind.
a level view at eye height, 300mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R4 · 翅图鉴·第四部分【鳍翼】：统一底座 + 鱼胸鳍（背上第二对，两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：13101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它立在水边的石头上、侧身朝向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a wet stone at the edge of a stream.
soft wet light, reflections from the water below.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-fin　seed 13101

```text
全身像，一只动物独自占据画面：它立在水边的石头上、侧身朝向镜头：
a medium-sized brown bird with a pair of stiff fish pectoral fins rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a wet stone at the edge of a stream.
soft wet light, reflections from the water below.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-fin-b　seed 13102

```text
全身像，一只动物独自占据画面：它立在水边的石头上、侧身朝向镜头：
a medium-sized brown bird with a pair of stiff fish pectoral fins rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a wet stone at the edge of a stream.
soft wet light, reflections from the water below.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R5 · 翅图鉴·第五部分【种子翅】：统一底座 + 枫树种子翅（背上第二对，两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：13101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它停在秋枝上、身体侧向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
among turning leaves in an autumn wood.
strong backlight through the leaves.
a wide view at eye height, 135mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-seed　seed 13101

```text
全身像，一只动物独自占据画面：它停在秋枝上、身体侧向镜头：
a medium-sized brown bird with a pair of dry maple seed wings rising from its back, a rounded head,
a short dark beak, folded feathered wings and a long tail.
among turning leaves in an autumn wood.
strong backlight through the leaves.
a wide view at eye height, 135mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-seed-b　seed 13102

```text
全身像，一只动物独自占据画面：它停在秋枝上、身体侧向镜头：
a medium-sized brown bird with a pair of dry maple seed wings rising from its back, a rounded head,
a short dark beak, folded feathered wings and a long tail.
among turning leaves in an autumn wood.
strong backlight through the leaves.
a wide view at eye height, 135mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R6 · 翅图鉴·追问轮：飞鱼鳍翼 / 鹤羽翼 / 纸翅（三种更接近「翅」的供体）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：13101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-flyfish　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a pair of long gliding flying-fish fins rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-crane　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a pair of long white crane wings rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-samara　seed 13101

```text
全身像，一只动物独自占据画面：它停在枝头、身体微微抬起：
a medium-sized brown bird with a pair of broad papery samara wings rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a branch in a sunlit woodland clearing.
flat top light, no shadows.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R7 · 期 04 定稿【飞鱼鳍翼】：统一底座 + 飞鱼的长鳍（背上第二对，两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：13101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它立在水边的石头上、侧身朝向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
on a wet stone at the edge of a stream.
soft wet light, reflections from the water below.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-flyfish　seed 13101

```text
全身像，一只动物独自占据画面：它立在水边的石头上、侧身朝向镜头：
a medium-sized brown bird with a pair of long gliding flying-fish fins rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a wet stone at the edge of a stream.
soft wet light, reflections from the water below.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-flyfish-b　seed 13102

```text
全身像，一只动物独自占据画面：它立在水边的石头上、侧身朝向镜头：
a medium-sized brown bird with a pair of long gliding flying-fish fins rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
on a wet stone at the edge of a stream.
soft wet light, reflections from the water below.
a level view at eye height, 400mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

## R8 · 期 05 收官【鹤羽翼】：统一底座 + 鹤的白翼（背上第二对，两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：13101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一只动物独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, Wildlife photograph, fine surface detail, slight film grain, no digital sharpening,
no text, no watermark.
```

### base-bird　seed 13101

```text
全身像，一只动物独自占据画面：它停在秋枝上、身体侧向镜头：
a medium-sized brown bird with a rounded head, a short dark beak,
folded feathered wings and a long tail.
among turning leaves in an autumn wood.
strong backlight through the leaves.
a wide view at eye height, 135mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-crane　seed 13101

```text
全身像，一只动物独自占据画面：它停在秋枝上、身体侧向镜头：
a medium-sized brown bird with a pair of long white crane wings rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
among turning leaves in an autumn wood.
strong backlight through the leaves.
a wide view at eye height, 135mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

### bird-crane-b　seed 13102

```text
全身像，一只动物独自占据画面：它停在秋枝上、身体侧向镜头：
a medium-sized brown bird with a pair of long white crane wings rising from its back,
a rounded head, a short dark beak, folded feathered wings and a long tail.
among turning leaves in an autumn wood.
strong backlight through the leaves.
a wide view at eye height, 135mm lens at f/5.6, Wildlife photograph, fine surface detail,
slight film grain, no digital sharpening, no text, no watermark.
```

