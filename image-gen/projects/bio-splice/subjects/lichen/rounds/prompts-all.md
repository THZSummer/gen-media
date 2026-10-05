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

## R1 · 地衣·第一期候选：菌丝体底座 + 壳状形态 CR1 / 绿色藻细胞 AL1（含同轮底座对照）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：8101
- 张数：4（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-mycelium　seed 8101

```text
微距特写，一个生物体独自占据画面：它铺在岩面上、表面朝向镜头：
a dense mat of pale fungal mycelium with fine branching threads and a soft dusty surface.
on a bare granite rock face.
raking side light that picks out every crack in the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-crust　seed 8101

```text
微距特写，一个生物体独自占据画面：它铺在岩面上、表面朝向镜头：
a dense mat of pale fungal mycelium with a hard crustose lichen crust with a cracked areolate
surface,
fine branching threads and a soft dusty surface.
on a bare granite rock face.
raking side light that picks out every crack in the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-algae　seed 8101

```text
微距特写，一个生物体独自占据画面：它铺在岩面上、表面朝向镜头：
a dense mat of pale fungal mycelium with clusters of bright green algal cells,
fine branching threads and a soft dusty surface.
on a bare granite rock face.
raking side light that picks out every crack in the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-crust-algae　seed 8101

```text
微距特写，一个生物体独自占据画面：它铺在岩面上、表面朝向镜头：
a dense mat of pale fungal mycelium with a hard crustose lichen crust with a cracked areolate
surface and clusters of bright green algal cells,
fine branching threads and a soft dusty surface.
on a bare granite rock face.
raking side light that picks out every crack in the surface.
a level macro view, 100mm macro lens at f/8, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

## R2 · 地衣·第二期候选：菌丝体底座 + 叶状体 FL1 / 藻丝 AL2（含同轮底座对照）

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：8101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-mycelium　seed 8101

```text
微距特写，一个生物体独自占据画面：它贴在树皮上、表面斜向镜头：
a dense mat of pale fungal mycelium with fine branching threads and a soft dusty surface.
on the wet bark of an old tree trunk.
soft wet light with a faint sheen on the surface.
a macro view from slightly above, 100mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-foliose　seed 8101

```text
微距特写，一个生物体独自占据画面：它贴在树皮上、表面斜向镜头：
a dense mat of pale fungal mycelium with leafy foliose lichen lobes with pale rims,
fine branching threads and a soft dusty surface.
on the wet bark of an old tree trunk.
soft wet light with a faint sheen on the surface.
a macro view from slightly above, 100mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-foliose-algae　seed 8102

```text
微距特写，一个生物体独自占据画面：它贴在树皮上、表面斜向镜头：
a dense mat of pale fungal mycelium with leafy foliose lichen lobes with pale rims and fine bright
green algal filaments woven through the surface,
fine branching threads and a soft dusty surface.
on the wet bark of an old tree trunk.
soft wet light with a faint sheen on the surface.
a macro view from slightly above, 100mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

## R3 · 地衣·第三期候选：菌丝体底座 + 枝状体 FR1（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1280　steps：12　共用 seed：8101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-mycelium　seed 8101

```text
微距特写，一个生物体独自占据画面：它立在冻原的石面上、整体朝向镜头：
a dense mat of pale fungal mycelium with fine branching threads and a soft dusty surface.
on a frost-covered stone in open tundra.
low backlight through ice fog, rimming every tip.
a low three-quarter macro view, 90mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-fruticose　seed 8101

```text
微距特写，一个生物体独自占据画面：它立在冻原的石面上、整体朝向镜头：
a dense mat of pale fungal mycelium with branching fruticose lichen tufts standing up like tiny
shrubs,
fine branching threads and a soft dusty surface.
on a frost-covered stone in open tundra.
low backlight through ice fog, rimming every tip.
a low three-quarter macro view, 90mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-fruticose-b　seed 8103

```text
微距特写，一个生物体独自占据画面：它立在冻原的石面上、整体朝向镜头：
a dense mat of pale fungal mycelium with branching fruticose lichen tufts standing up like tiny
shrubs,
fine branching threads and a soft dusty surface.
on a frost-covered stone in open tundra.
low backlight through ice fog, rimming every tip.
a low three-quarter macro view, 90mm macro lens at f/8, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

## R4 · 地衣·第四期候选【藻层可见】：菌丝体底座 + 绿色细胞 AL1 + 藻丝 AL2（拟剖面）；含同轮底座对照

- 引擎：`zimage`　尺寸：1024×1024　steps：12　共用 seed：8101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-mycelium　seed 8101

```text
微距特写，一个生物体独自占据画面：它的表层被掀开、露出内部结构：
a dense mat of pale fungal mycelium with fine branching threads and a soft dusty surface.
as if in cross-section, the upper cortex lifted away.
ring light, deep even depth of field, everything in focus.
a flat-on macro view, 100mm macro lens at f/16, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-algal-layer　seed 8101

```text
微距特写，一个生物体独自占据画面：它的表层被掀开、露出内部结构：
a dense mat of pale fungal mycelium with clusters of bright green algal cells and fine bright green
algal filaments woven through the surface,
fine branching threads and a soft dusty surface.
as if in cross-section, the upper cortex lifted away.
ring light, deep even depth of field, everything in focus.
a flat-on macro view, 100mm macro lens at f/16, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-algal-layer-b　seed 8102

```text
微距特写，一个生物体独自占据画面：它的表层被掀开、露出内部结构：
a dense mat of pale fungal mycelium with clusters of bright green algal cells and fine bright green
algal filaments woven through the surface,
fine branching threads and a soft dusty surface.
as if in cross-section, the upper cortex lifted away.
ring light, deep even depth of field, everything in focus.
a flat-on macro view, 100mm macro lens at f/16, macro photograph, focus-stacked,
fine surface detail, natural colour, no digital sharpening, no text, no watermark.
```

## R5 · 地衣·第五期收官【共生体】：菌丝体底座 + 三种形态 / 两种形态+藻（两个 take）；含同轮底座对照

- 引擎：`zimage`　尺寸：1280×1024　steps：12　共用 seed：8101
- 张数：3（每张独立请求）

**轮内恒定层**（所有张共用，保证 A/B/C 只差拼接句）

```text
微距特写，一个生物体独自占据画面：<姿态><底座 with 部位>.
<生境>.
<光线>.
<镜头>, macro photograph, focus-stacked, fine surface detail, natural colour,
no digital sharpening, no text, no watermark.
```

### base-mycelium　seed 8101

```text
微距特写，一个生物体独自占据画面：它铺在林地上的石面上、整体展开：
a dense mat of pale fungal mycelium with fine branching threads and a soft dusty surface.
on a mossy boulder in a misty forest, the background dissolving into fog.
soft scattered light, no hard shadows.
a wide macro view, 45mm lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-3forms　seed 8101

```text
微距特写，一个生物体独自占据画面：它铺在林地上的石面上、整体展开：
a dense mat of pale fungal mycelium with a hard crustose lichen crust with a cracked areolate
surface and leafy foliose lichen lobes with pale rims and branching fruticose lichen tufts standing
up like tiny shrubs,
fine branching threads and a soft dusty surface.
on a mossy boulder in a misty forest, the background dissolving into fog.
soft scattered light, no hard shadows.
a wide macro view, 45mm lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

### mycelium-forms-algae　seed 8102

```text
微距特写，一个生物体独自占据画面：它铺在林地上的石面上、整体展开：
a dense mat of pale fungal mycelium with leafy foliose lichen lobes with pale rims and branching
fruticose lichen tufts standing up like tiny shrubs and clusters of bright green algal cells,
fine branching threads and a soft dusty surface.
on a mossy boulder in a misty forest, the background dissolving into fog.
soft scattered light, no hard shadows.
a wide macro view, 45mm lens at f/11, macro photograph, focus-stacked, fine surface detail,
natural colour, no digital sharpening, no text, no watermark.
```

