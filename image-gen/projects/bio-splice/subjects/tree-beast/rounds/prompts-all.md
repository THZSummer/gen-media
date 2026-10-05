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

## R1 · 树兽·第一期候选【占用版】：底座照常写树皮 + 兽皮纹 K1（含同轮底座对照）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：12101
- 张数：2（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with rough fissured bark,
thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide　seed 12101

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide, rough fissured bark,
thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R2 · 树兽·第一期对照【腾出版】：底座不写树皮 + 兽皮纹 K1（含同轮底座对照）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：12101
- 张数：2（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide　seed 12101

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide,
thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R3 · 树兽·第二期候选【根成足的树】：老树 + 兽足 K2（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1280　steps：12　共用 seed：12101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它长在泥岸边、露出的根系朝向镜头：
an old gnarled tree with rough fissured bark,
thick roots spreading over the ground and a massive trunk.
on a muddy riverbank, the roots exposed above the water line.
low morning light, long shadows across the mud.
a low view looking up the trunk, 35mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-feet　seed 12101

```text
全身像，一个生物体独自占据画面：它长在泥岸边、露出的根系朝向镜头：
an old gnarled tree with heavy clawed mammal feet among the roots, rough fissured bark,
thick roots spreading over the ground and a massive trunk.
on a muddy riverbank, the roots exposed above the water line.
low morning light, long shadows across the mud.
a low view looking up the trunk, 35mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-feet-b　seed 12102

```text
全身像，一个生物体独自占据画面：它长在泥岸边、露出的根系朝向镜头：
an old gnarled tree with heavy clawed mammal feet among the roots, rough fissured bark,
thick roots spreading over the ground and a massive trunk.
on a muddy riverbank, the roots exposed above the water line.
low morning light, long shadows across the mud.
a low view looking up the trunk, 35mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R4 · 树兽·第三期候选【有角的树】：老树 + 兽角 K4（从树干生出，两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：12101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它立在霜林里、树干侧面朝向镜头：
an old gnarled tree with rough fissured bark,
thick roots spreading over the ground and a massive trunk.
in a frost-covered forest, bare branches around it.
low side-backlight, frost glittering on the bark.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-horns　seed 12101

```text
全身像，一个生物体独自占据画面：它立在霜林里、树干侧面朝向镜头：
an old gnarled tree with a pair of massive curved mammal horns rising from the trunk,
rough fissured bark, thick roots spreading over the ground and a massive trunk.
in a frost-covered forest, bare branches around it.
low side-backlight, frost glittering on the bark.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-horns-b　seed 12102

```text
全身像，一个生物体独自占据画面：它立在霜林里、树干侧面朝向镜头：
an old gnarled tree with a pair of massive curved mammal horns rising from the trunk,
rough fissured bark, thick roots spreading over the ground and a massive trunk.
in a frost-covered forest, bare branches around it.
low side-backlight, frost glittering on the bark.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R5 · 树兽·第四期候选【皮足俱全】：底座不写树皮 + 兽皮纹 K1 + 兽足 K2；含同轮底座对照

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：12101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它长在坡地上、树干与根系都朝向镜头：
an old gnarled tree with thick roots spreading over the ground and a massive trunk.
on a forest slope just after rain, wet leaves everywhere.
hard light breaking through after the rain, crisp shadows.
a level view at eye height, 35mm lens at f/11, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide-feet　seed 12101

```text
全身像，一个生物体独自占据画面：它长在坡地上、树干与根系都朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide and heavy clawed mammal feet among
the roots,
thick roots spreading over the ground and a massive trunk.
on a forest slope just after rain, wet leaves everywhere.
hard light breaking through after the rain, crisp shadows.
a level view at eye height, 35mm lens at f/11, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide-feet-b　seed 12102

```text
全身像，一个生物体独自占据画面：它长在坡地上、树干与根系都朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide and heavy clawed mammal feet among
the roots,
thick roots spreading over the ground and a massive trunk.
on a forest slope just after rain, wet leaves everywhere.
hard light breaking through after the rain, crisp shadows.
a level view at eye height, 35mm lens at f/11, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R6 · 树兽·第五期收官【树兽】：底座不写树皮 + 兽皮纹 K1 + 兽足 K2 + 兽角 K4；暮色逆光广角

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：12101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它立在暮色林里、整棵树朝向镜头：
an old gnarled tree with thick roots spreading over the ground and a massive trunk.
in a forest at dusk, the far trees lost in haze.
low backlight throwing the whole tree into near-silhouette.
a wide-angle 24mm lens at eye height, f/8, fine surface detail, natural colour, slight film grain,
no digital sharpening, no text, no watermark.
```

### tree-beast　seed 12101

```text
全身像，一个生物体独自占据画面：它立在暮色林里、整棵树朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide and heavy clawed mammal feet among
the roots and a pair of massive curved mammal horns rising from the trunk,
thick roots spreading over the ground and a massive trunk.
in a forest at dusk, the far trees lost in haze.
low backlight throwing the whole tree into near-silhouette.
a wide-angle 24mm lens at eye height, f/8, fine surface detail, natural colour, slight film grain,
no digital sharpening, no text, no watermark.
```

### tree-beast-b　seed 12102

```text
全身像，一个生物体独自占据画面：它立在暮色林里、整棵树朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide and heavy clawed mammal feet among
the roots and a pair of massive curved mammal horns rising from the trunk,
thick roots spreading over the ground and a massive trunk.
in a forest at dusk, the far trees lost in haze.
low backlight throwing the whole tree into near-silhouette.
a wide-angle 24mm lens at eye height, f/8, fine surface detail, natural colour, slight film grain,
no digital sharpening, no text, no watermark.
```

## R7 · 期 01 定稿【兽皮的树】：底座不写树皮 + 兽皮纹 K1（三个 seed）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：12101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide　seed 12101

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide,
thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide-b　seed 12102

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide,
thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide-c　seed 12103

```text
全身像，一个生物体独自占据画面：它立在雾里、树干正面朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide,
thick roots spreading over the ground and a massive trunk.
deep in a misty forest, undergrowth fading into fog.
soft diffused light through the mist.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R8 · 期 03 定稿【皮角俱全】：底座不写树皮 + 兽皮纹 K1 + 兽角 K4（两个 take）；雨后硬光横

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：12101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它长在坡地上、树干与根系都朝向镜头：
an old gnarled tree with thick roots spreading over the ground and a massive trunk.
on a forest slope just after rain, wet leaves everywhere.
hard light breaking through after the rain, crisp shadows.
a level view at eye height, 35mm lens at f/11, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide-horns　seed 12101

```text
全身像，一个生物体独自占据画面：它长在坡地上、树干与根系都朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide and a pair of massive curved mammal
horns rising from the trunk,
thick roots spreading over the ground and a massive trunk.
on a forest slope just after rain, wet leaves everywhere.
hard light breaking through after the rain, crisp shadows.
a level view at eye height, 35mm lens at f/11, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### tree-hide-horns-b　seed 12102

```text
全身像，一个生物体独自占据画面：它长在坡地上、树干与根系都朝向镜头：
an old gnarled tree with a covering of coarse tawny mammal hide and a pair of massive curved mammal
horns rising from the trunk,
thick roots spreading over the ground and a massive trunk.
on a forest slope just after rain, wet leaves everywhere.
hard light breaking through after the rain, crisp shadows.
a level view at eye height, 35mm lens at f/11, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

## R9 · 期 04 定稿【枯木的皮与角】：**换底座（枯立木）** + 兽皮纹 K1 + 兽角 K4（两个 take）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：12101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
全身像，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, fine surface detail, natural colour, slight film grain, no digital sharpening, no text,
no watermark.
```

### base-tree　seed 12101

```text
全身像，一个生物体独自占据画面：它立在霜晨的空地上、树干正面朝向镜头：
a dead standing tree with a splintered bare trunk and exposed roots.
standing dead in a clearing on a frosty morning.
cold flat light, frost on every surface.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### deadwood-hide-horns　seed 12101

```text
全身像，一个生物体独自占据画面：它立在霜晨的空地上、树干正面朝向镜头：
a dead standing tree with a covering of coarse tawny mammal hide and a pair of massive curved
mammal horns rising from the trunk,
a splintered bare trunk and exposed roots.
standing dead in a clearing on a frosty morning.
cold flat light, frost on every surface.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

### deadwood-hide-horns-b　seed 12102

```text
全身像，一个生物体独自占据画面：它立在霜晨的空地上、树干正面朝向镜头：
a dead standing tree with a covering of coarse tawny mammal hide and a pair of massive curved
mammal horns rising from the trunk,
a splintered bare trunk and exposed roots.
standing dead in a clearing on a frosty morning.
cold flat light, frost on every surface.
a level view at eye height, 50mm lens at f/8, fine surface detail, natural colour,
slight film grain, no digital sharpening, no text, no watermark.
```

