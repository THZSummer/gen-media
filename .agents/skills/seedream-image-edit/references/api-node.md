# Seedream 图片编辑节点速查（真机事实）

本页只写**实测**出来的东西，每条都注明证据。共用的东西不重复：
凭据通道、`dotted` 输入名的由来、保存格式、schema 对账、缓存语义见姊妹篇
[seedream-text-to-image/references/api-node.md](../../seedream-text-to-image/references/api-node.md)。

先记住三件事，它们各自对应本页一节：

1. 桌面导出的图里带 **前端专有节点**（`MarkdownNote`），不剔掉就 `400 missing_node_type`（§2）；
2. 参考图接 **`model.images.image_N`**（采集式输入），有参考图时 **`thinking` 不能关**（§3）；
3. **`Painter` 是服务器节点**，它把 RGBA 标注层按 alpha 合成到底图上——"标注真的进了图"可以
   用像素证明（§4）。

---

## 1. 这份工作流长什么样

`assets/seedream-5.0-pro-image-edit-ui.json`（用户从桌面版导出的原件，逐字节保存）：

| id | 类 | 角色 |
|----|----|------|
| 3 | `LoadImage` | 底图（服务器 `input/` 目录里的文件名） |
| 7 | `Painter` | 把 RGBA 标注层合成到底图上（可整条不要，见 §4） |
| 5 | `PreviewImage` | 界面预览（无头不需要，默认剔除） |
| 8 | `ByteDanceSeedreamNodeV3` | **付费 partner 节点**：推理在 ByteDance 云端，按张计费 |
| 2 | `SaveImageAdvanced` | 保存成品 |
| 6 / 9 | `MarkdownNote` | 说明文字，**服务器上没有这个类**（§2） |

UI→API 的两条换算规则与文生图完全一致（API 输入名 = `widgets_values_named` 的键、`control_after_generate*`
是前端伪 widget 不进图），见姊妹篇 §1。本页只讲编辑多出来的部分。

链路上的关键一条：

```
LoadImage(3) ─IMAGE─▶ Painter(7) ─IMAGE─▶ Seedream(8).model.images.image_1
                                 └─MASK─▶ (没人用；本工作流只拿 IMAGE)
```

## 2. 前端专有节点：不剔掉就 400

把导出的原图直接转成 API 图提交，服务器原样回绝（**免费**：HTTP 400，还没进执行）：

```json
{"error": {"type": "missing_node_type",
           "message": "Node 'MarkdownNote' not found. The custom node may not be installed.",
           "details": "Node ID '#6'"}}
```

所以引擎先过 `seedream_api.prune_ui_only()`：

- **静态名单**（默认）：`MarkdownNote`、`Note`、`PrimitiveNode`、`Reroute`、`GroupNode`；
- **真机名单**（可选）：把 `/object_info` 的类名集合传进来，凡不在其中的一律删——最稳；
- 删节点会把**指向它的输入**一并清掉（否则留下一张断线的图）；
- 还有一次**级联删除**：删 `Painter` 会带走它的下游 `PreviewImage`。
- `PreviewImage` 是合法服务器节点，但无头没人看，默认也剔（少存一张临时图）；要留着用
  `--keep-preview`。

## 3. 参考图接线（免费探针，三次提交都拿到 HTTP 200）

`model.images` 在 schema 里是 `COMFY_AUTOGROW_V3`（采集式输入，tooltip：*Optional reference
image(s) for image-to-image or multi-reference generation. Up to N images.*）。它在 API 图里的
键名是**按序号带点**的：

```json
"8": {"class_type": "ByteDanceSeedreamNodeV3",
      "inputs": {"model.images.image_1": ["7", 0],
                 "model.images.image_2": ["30", 0], ...}}
```

实测（服务器 0.38.0，用**故意无效**的凭据提交，因此只证形状、不调云端、不花钱）：

| 提交的图 | HTTP | 执行阶段 |
|---|---|---|
| 1 张参考图接 `image_1`（经 Painter） | 200 | `Unauthorized: Please login first to use this node.` |
| 2 张参考图接 `image_1` + `image_2`（不经 Painter） | 200 | 同上 |
| 1 张参考图 + `model.thinking = false` | 200 | `'thinking' can only be disabled for text-to-image; enable it when using reference images.` |

三条结论：

- `image_N` 这个写法服务器认，**多图参考可用**；
- `model.images` 给不给都行（纯文生图不给也能过校验，见姊妹篇）；
- **有参考图时 `thinking` 必须为真**：服务器在**执行阶段**才报，也就是说本地不拦就会白花一次
  排队 + 一次请求。本技能在提交前就拦（`seedream 5.0 flash` 没有 `thinking`，不受影响）。

**张数上限**（按模型，从节点 tooltip 直接读，`--list` / `--check` 会打印）：
pro / flash / 4.5 / 4.0 = **10**，lite = **14**。

## 4. Painter 到底做什么（四次免费实验）

`Painter` 的输入是 `mask`（`widgetType: PAINTER` 的 STRING，值是服务器 `input/` 里的文件名）、
隐藏的 `width` / `height`、`bg_color`，以及可选的 `image`（底图）。输出 `IMAGE` + `MASK`。
"它到底把什么送到下游"曾是个纯猜测问题，于是用**不花钱**的图（`LoadImage → Painter →
SaveImageAdvanced` / `MaskToImage`，不接付费节点）直接测：

| 标注层（上传的 PNG） | Painter 的 `IMAGE` 输出 | Painter 的 `MASK` 输出 |
|---|---|---|
| 透明底 + 不透明红块（ffmpeg `drawbox` 写的，**实测 alpha 全 0**） | 与底图**逐像素相同** | 全黑 |
| 不透明黑底 + 白块（**无 alpha 通道**） | 与标注层相同（底图被整片盖掉） | 全白 |
| 透明底 + 不透明红块（numpy 写的真 alpha：只有框内 255） | 底图 + 红框（差异**恰好**落在框内 66000 px） | 全白 66000 px = 框内 |
| 512×512 的标注层 + 1024×1360 的底图 | 输出 1024×1360，标注层被**拉伸**（比例失真） | — |

结论（写进 SKILL.md 的"踩坑点"）：

1. **只看 alpha**：笔迹必须是不透明像素，底色透明；整块不透明的 PNG 会被读成"全都标了"。
2. `IMAGE` 输出 = **底图与标注层的 alpha 合成**，送进 Seedream 的就是这张 —— 所以
   `--annotate` 的效果可以用像素证明，不依赖模型听不听话。
3. `MASK` 输出 = 标注层的 alpha 通道（本工作流没人用）。
4. 标注层尺寸**不要求**与底图一致，但会被拉到底图尺寸再合成 —— 想精确就按底图尺寸造。
5. 隐藏的 `width` / `height` 不影响输出尺寸（输出跟底图走）；引擎仍会按底图尺寸填，便于复核。
6. 标注层文件名**不需要** `[input]` 后缀（带不带都能跑，上传到 `type=input` 即可）。

## 5. 尺寸：编辑不会跟随底图

`size_preset` 由模型决定，每个模型一套（`--list` 打印原文）。例如 pro 的 1K 档：
`1024x1024 (1:1)` / `864x1152 (3:4)` / `1152x864 (4:3)` / `1312x736 (16:9)` / `736x1312 (9:16)` /
`832x1248 (2:3)` / `1248x832 (3:2)` / `1568x672 (21:9)`；`width` / `height` 只在预设为
`Custom` 时生效。

编辑的常见诉求是"别把比例改掉"，所以本技能默认 `--size auto`：

- 读第 1 张底图的宽高比（PNG 读 IHDR、JPEG 扫 SOF，**不用 Pillow**），
- 在**该模型最小的一档**里挑比例最接近的预设（同比例多档取像素最小的），
- 底图 1024×1360（0.7529）→ `(1K) 864x1152 (3:4)`；要更大写 `--size-tier 2K`。

> 注意 `auto` 只保证**比例**，不保证像素尺寸：1024×1360 的底图会出 864×1152。
> 要等像素级成品就显式给档位或预设原文。

## 6. 验证状态（2026-10-06 真机跑通）

付费矩阵 `verify_edits.py --yes` —— **4 张图、8/8 判据通过**，留档时间戳 20:09:07 → 20:11:58
（含上传与排队约 3 分钟；单张 19 s ~ 115 s，双参考最慢）。全部取 `(1K) 864x1152 (3:4)`
（`--size auto` 从 1024×1360 的底图算出）：

| 步骤 | 提交 | 结果（判据） |
|---|---|---|
| `edit` | 鹿蜀定稿，1 张参考，"把背景改成纯白色" | 尺寸 = 请求的预设；边缘"接近纯白"像素占比 **0.000 → 0.722**（看像素） |
| `annotate` | 同上 + 红框标注层 | Painter 合成图与底图**框内 1.000 不同、框外 0.00000**，尺寸与底图一致 |
| `refs2` | 鹿蜀 + 九尾狐两张参考 | `model.images.image_1` + `image_2` 都接上；出图把两只动物并排画进一张画、各自毛色保留 |
| `flash` | 换 `seedream 5.0 flash` + 参考图 | 照跑，尺寸 = 请求的预设 |

**观察项（不是接线判据，但很重要）**：让模型"把红框标出的整块区域改成纯黑色"时，它**没有**把框内
涂黑（框内平均亮度 202.4 → 147.7），而是**擦掉红框、把黑色画到主体上**（马的胸颈多了一大块黑）。
所以 `--annotate` 是**给模型的提示标记，不是硬遮罩**：要"标哪改哪"得另想办法（先本地遮罩再合成，
或换本机的 inpainting 工作流）。

另外：这 4 张**都没有**出现模型自写的小字/印章，与文生图那轮"6/6 都题款盖印"不同 ——
样本太小，不能当结论，只说明编辑路径下**不必然**发生。定稿前照样要做印面/伪字检查。

仍未验证：lite / 4.5 / 4.0 的编辑（含 `--max-images`）、2K/4K 档、`--watermark`、
`prompt_optimization=fast`，以及"模型遵守标注提示的稳定性"。

## 7. 复现这些探针

```bash
# 免费：把"真机接受的 API 图"重新录一遍（故意用无效凭据：只证形状，不调云端）
python3 scripts/record_fixture.py --ref <底图> [--annotate <标注层>]

# 免费：离线自检（与上面那份基准逐字节比对）
python3 scripts/test_skill.py

# 免费：真机探活 + 节点 + schema 对账 + 凭据
python3 scripts/seedream_edit.py --check

# 付费：四条支路各一张图
python3 scripts/verify_edits.py --api-key-file <key文件> --yes
```
