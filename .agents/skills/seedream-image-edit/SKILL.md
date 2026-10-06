---
name: seedream-image-edit
description: 通过本机 ComfyUI（默认 http://192.168.3.5:18000）的 ByteDance Seedream 付费 partner 节点做**图片编辑**：底图（可再叠一层 RGBA 标注）上传后接进 model.images.image_N，按提示词改图；**模型在云端**，本机零权重、按张计费。脚本负责上传参考图、把 UI 工作流改造成 /prompt API 图（剔除前端专有节点）、按底图比例挑尺寸预设、带 ComfyUI 账号凭据提交、轮询 /history、下载成品与标注合成图并留档。触发词：Seedream 编辑、图片编辑、改图、图生图、参考图编辑、换背景、局部重绘、多图参考、seedream image edit。
whenToUse: 当要用 Seedream（远端付费模型）**基于已有图片**改图——换背景/换主体/局部重画/风格迁移/多张参考图合成——时使用。纯文生图用姊妹技能 seedream-text-to-image；要**本机权重**的控制图生图（ControlNet）用 comfyui-image-edit；要直连火山方舟 ARK 出图见 methods/text-to-image。
---

# Seedream 图片编辑（ComfyUI partner 节点 · 远端付费模型）

**用途**：把 `assets/seedream-5.0-pro-image-edit-ui.json` 这份工作流（桌面版导出原件）提交到
ComfyUI，拿回改好的图片落盘。工作流里最关键的仍是 `ByteDanceSeedreamNodeV3` ——
ComfyUI 的 **partner / API 节点**：本机只做编排，**推理在 ByteDance 云端**，按张计费。

和姊妹技能 [seedream-text-to-image](../seedream-text-to-image/SKILL.md) 的关系：**同一个节点、
同一套凭据、同一套 schema**；差别只在"**给不给参考图**"。所以本技能不复制那份引擎，而是用
`scripts/_shared.py` 把它的 `seedream_api.py` / `seedream_gen.py` 挂上 `sys.path` 复用——
凭据通道、dotted 输入名、schema 快照这些事实只维护一份。

- 默认服务器：`http://192.168.3.5:18000`（`--server` 或 `$COMFYUI_SERVER` 覆盖）
- 工作流：`assets/seedream-5.0-pro-image-edit-ui.json`（`LoadImage → Painter → Seedream → 保存`）
- 参考图 / 标注 / 鉴权 / 踩坑：`references/api-node.md`（**先读这页**）
- 真机接受的 API 图基准：`references/accepted-api-graph.json`（离线自检逐字节比对用）
- 引擎：`scripts/seedream_edit.py`，建图与尺寸：`scripts/seedream_edit_graph.py`

> 📦 **依赖**：复用姊妹技能的引擎（`../../seedream-text-to-image/scripts`，可用
> `$SEEDREAM_SHARED_SCRIPTS` 覆盖），只依赖 Python 3 标准库。
> `verify_edits.py` 的像素判据需要 `ffmpeg` + `numpy`。

## ⛔ 凭据：和文生图一模一样的那一关

编辑走的是**同一个付费节点**，所以"桌面端点 Run 能出图、脚本报 Unauthorized"这件事照样成立。
凭据三条通道（`--api-key` / `--api-key-file` / `$COMFYUI_API_KEY`，另有一条会过期的
Bearer token 通道）与排错顺序见
[seedream-text-to-image/SKILL.md §凭据](../seedream-text-to-image/SKILL.md)；
**凭据不进留档**（`requests.jsonl` 只记 `credential_channel` / `credential_source`）。

## 何时用 / 何时不用

| 你手里的东西 | 技能 |
|---|---|
| **已有图片**，要按提示词改（换背景 / 换主体 / 局部重画 / 多图参考） | **本技能** |
| 只有文字，要出图 | [seedream-text-to-image](../seedream-text-to-image/SKILL.md)（Seedream 云端）/ [comfyui-text-to-image](../text-to-image-comfyui/SKILL.md)（本机权重） |
| 有控制图（线稿 / 姿态 / Canny），要**本机** ControlNet 约束结构 | [comfyui-image-edit](../image-edit-comfyui/SKILL.md) |
| 只想确定性处理图片（拼版 / 比对 / 裁切 / 缩图） | [image-tools](../image-tools/SKILL.md)（不调模型） |
| 直连火山方舟 ARK 出 Seedream（另一套账，不经过 ComfyUI） | [methods/text-to-image](../../../methods/text-to-image/README.md) |

## 前置检查

```bash
cd .agents/skills/seedream-image-edit

python3 scripts/seedream_edit.py --check    # 探活 + 节点 + schema 对账 + 凭据 + 工作流可跑性
python3 scripts/seedream_edit.py --list     # 模型 / 参数 / 尺寸预设 / 每个模型能收几张参考图
```

`--check` 的解读（**它证明不了能出图**）：

| 字段 | 含义 |
|------|------|
| `nodes` | 四个类都在不在：`ByteDanceSeedreamNodeV3` / `SaveImageAdvanced` / `LoadImage` / `Painter`（`Painter` 只在 `--annotate` 时需要） |
| `max_refs` | 每个模型能收几张参考图（从节点 tooltip 里读：pro/flash 10、lite 14） |
| `schema_drift` | 真机 `/object_info` 与姊妹技能那份快照的差异；不是 `none` 先更新快照 |
| `workflow_classes` | 这份工作流提交前实际会用到的类 |
| `headless_dropped` | `--check` 顺手报的"会被剔除的节点"：`MarkdownNote`（服务器上没有）+ `PreviewImage`（无头不需要） |
| `credential.present` | 有没有拿到凭据；`false` 时照 `hint` 补 |
| 退出码 | `0` 正常 ｜ `2` 不可达 ｜ `3` 缺节点 |

## 执行

```bash
# 先看逐字 API 图（不花钱，也不上传）
python3 scripts/seedream_edit.py --image base.png --prompt "女主换成男主" --dry-run

# 最小编辑：底图 + 指令（尺寸默认 auto：按底图比例挑同档最小的预设）
python3 scripts/seedream_edit.py --image base.png --prompt "把背景改成纯白色" --out-dir out/

# 带标注：marks.png 是 RGBA 图（alpha 就是笔迹），Painter 会把它合成到底图上再送去编辑
python3 scripts/seedream_edit.py --image base.png --annotate marks.png \
    --prompt "把红框标出的区域改成纯黑色" --out-dir out/

# 多图参考（第 1 张是底图，其余进 image_2 / image_3 …）
python3 scripts/seedream_edit.py --image a.png --image b.png \
    --prompt "把两张图里的动物并排画在同一张画里" --out-dir out/

# 要更大的成品：显式给档位或预设（编辑不会自动跟随底图像素尺寸）
python3 scripts/seedream_edit.py --image base.png --prompt "..." --size-tier 2K --out-dir out/

# 凭据 + 固定 seed
python3 scripts/seedream_edit.py --image base.png --prompt "..." --seed 7 \
    --api-key-file ../../../work/comfy_api_key --out-dir out/
```

## 参数

| 参数 | 作用 | 默认 |
|------|------|------|
| `--image` | 参考图（**可重复，至少一张**；第 1 张是底图） | 必给 |
| `--annotate` | RGBA 标注层（alpha = 笔迹）：先经 Painter 合成到底图上 | 无（不要标注） |
| `--prompt` / `--prompt-file` | 编辑指令（二选一，必给一个） | 工作流自带的值 |
| `--size` | `auto` / 预设原文 / `1024x1024` / `1:1` / `Custom`+宽高 | `auto` |
| `--size-tier` | `auto` 用哪一档（`1K` / `1.5K` / `2K` / `3K` / `4K`） | 该模型最小档 |
| `--model` | 模型键（5 个可选，见 `--list`） | `seedream 5.0 pro`（工作流值） |
| `--seed` | 随机种子 | 工作流值 |
| `--thinking` / `--no-thinking` | 有参考图时**必须开**；给 `--no-thinking` 会被本地拦下（服务器也会拒） | 开 |
| `--prompt-optimization {standard,fast}` | 仅 `seedream 5.0 pro`，给参考图时才有意义 | 工作流值（standard） |
| `--watermark` / `--no-watermark` | 加/不加 "AI generated" 水印 | 工作流值（false） |
| `--max-images` / `--fail-on-partial` | 一次要几张关联图 / 缺图即失败（仅 lite/4.5/4.0） | 工作流值 |
| `--format` | 保存格式（本机 `SaveImageAdvanced` 只接受 **png / exr / avif**） | 工作流值（png） |
| `--filename-prefix` | 输出前缀（同时是留档名） | `seedream-edit` |
| `--api-key` / `--api-key-file` / `--auth-token` | 凭据（见上） | `$COMFYUI_API_KEY` |
| `--dry-run` | 只打印 API 图：**不上传、不提交** | 关闭 |
| `--keep-preview` | 保留工作流里的 `PreviewImage`（默认剔除） | 关闭 |
| `--out-dir` / `--timeout` / `--poll` / `--quiet` / `--no-record` | 输出目录 / 等待秒数 / 轮询间隔 / 静默 / 关留档 | `out` / 900 / 3 / — / 留档开启 |
| `--allow-unapplied` | 参数对所选模型不存在时不报错（默认报错退出 8） | 关闭 |

**退出码**：`0` 成功 ｜ `1` 没下到图 ｜ `2` 服务器不可达 ｜ `3` 没有该节点 ｜
`4` 鉴权被拒 ｜ `5` 服务器拒了这张图（HTTP 400） ｜ `6` 节点执行报错 ｜
`7` 超时 ｜ `8` 参数不成立（无参考图 / 未知模型 / 参考图超上限 / 有参考图还关 thinking / 尺寸非法）。

## 参考图是怎么接进去的（四个真机事实）

1. **接线**：第 N 张参考图接 `model.images.image_N`（`COMFY_AUTOGROW_V3` 采集式输入，API 名带点）。
   `image_2` 真的被服务器接受（免费探针：HTTP 200 → 执行阶段才因无效凭据止步）。
2. **前端专有节点必须先剔**：桌面导出的图里有 `MarkdownNote`，服务器上没有这个类，
   原样提交直接 `400 missing_node_type`。引擎提交前会剔掉（见 `references/api-node.md` §2）。
3. **Painter 是服务器节点**（不是界面把戏）：它把标注层按 **alpha 合成**到底图上，
   `IMAGE` 输出 = 合成图（送进 Seedream 的就是这张），`MASK` 输出 = 标注层 alpha。
   所以"标注真的进去了"这件事可以用像素证明，不靠模型听话。
4. **`thinking` 有参考图时不能关**：服务器原话
   `'thinking' can only be disabled for text-to-image; enable it when using reference images.`
   本地先拦，省一次付费请求。

> ⚠️ **尺寸不跟随底图**：Seedream 出图尺寸只由 `size_preset` 决定，编辑也不会自动保持底图
> 像素尺寸。`--size auto`（默认）取"与底图同比例的最小预设"；要更大写 `--size-tier 2K` 或直接给预设。

## 留档（默认开启）

| 文件 | 内容 |
|------|------|
| `<filename-prefix>.api.json` | 实际提交的整张 API 图（含 `model.images.image_N` 接线、标注层文件名） |
| `requests.jsonl` | 每行一次请求：时间 / `prompt_id` / 参数 / `ref_keys` / `server_refs` / 产物路径 / 凭据通道（**不含凭据本身**） |
| `<prefix>-composite-*.png` | `--annotate` 时的 Painter 合成图（"标注真的进了图"的证据） |

## 踩坑点

- **`--size auto` 只会挑同比例的最小档**：1024×1360 的底图会落到 `(1K) 864x1152 (3:4)`——
  比底图略小。要原尺寸级成品就写 `--size-tier 2K`（1728×2304）。
- **标注层会被拉伸到底图尺寸**：Painter 把标注层按底图宽高比缩放（实测 512×512 的标注层
  被拉到 1024×1360，比例失真）。自己造标注层就按底图尺寸造。
- **标注层只认 alpha**：整块不透明黑底的 PNG 会被当成"全都标了"（MASK 全白）；要局部标注就用
  透明底 + 不透明笔迹。
- **`--annotate` 是提示、不是遮罩**：实测让模型"把红框标出的区域改成纯黑"，它把红框**擦掉**、
  把黑画到了**主体**上（框内亮度只从 202 降到 148）。要"标哪改哪"得另想办法（先本地遮罩合成，
  或换本机的 inpainting 工作流）。标注层能保证的只是"这张合成图确实进了模型"（像素可证）。
- **参考图上限按模型算**（pro/flash 10、lite 14）：超了本地就报错，不会白花钱。
- **付费即计费**：每次重试都是真花钱；先 `--dry-run`，再固定 `--seed` 复跑。
- **注意模型会在画面里题款盖印**：实测 Seedream 编辑/文生图都爱在空白处写小字、盖印章，
  而本仓库的交付纪律是"字不由模型写"。编辑完要做**印面/伪字检查**再定稿
  （见 `projects/shanhai-jing/scripts/seal_check.py` 与 `patch_region.py`）。
- **超时后任务可能仍在云端跑**：`--timeout` 默认 900s（有参考图时 thinking 强制开，pro 会慢）；
  超时先去 ComfyUI 队列看，别急着重复提交。

## 验证

```bash
# 离线自检：建图（与真机接受的图逐字节比对）+ 四条接线 + 参数面 + mock 往返；不花钱不联网
python3 scripts/test_skill.py

# 真机探活与 schema 对账（不花钱）
python3 scripts/seedream_edit.py --check

# 重建"真机接受的 API 图"基准（不花钱：故意用无效凭据，只证形状不调模型）
python3 scripts/record_fixture.py --ref <底图> [--annotate <标注层>]

# 真机付费矩阵（**付费**：默认 4 张图；没有凭据会 SKIPPED 退出）
python3 scripts/verify_edits.py --api-key-file <key文件> --yes
```

判据纪律：尺寸看 **PNG 头解出来的真实宽高**；"改动是否落地"看**解码后的像素**，不看文件哈希。
`verify_edits.py` 把"接线判据"（合成图只在标注框内不同、`image_2` 真的接上、尺寸等于请求的预设）
与"模型听不听话"（标注区有没有真的变黑）分开记录，后者是观察项。

> **验证状态**：见 `references/api-node.md` §5（真机跑通的证据、耗时与仍未验证的部分）。

## 检查清单

- [ ] `--check` 通过（四个节点在位、`schema_drift: none`）
- [ ] 凭据已给（`--api-key-file` / `$COMFYUI_API_KEY`），否则预期 exit 4
- [ ] `--image` 至少一张；第 1 张是**底图**，顺序别搞错（第 N 张 → `image_N`）
- [ ] 参考图张数没超该模型上限（先 `--list`）
- [ ] 尺寸想清楚：`auto` 只保证比例，不保证像素尺寸
- [ ] `--annotate` 用透明底 RGBA 图，尺寸与底图一致
- [ ] `--dry-run` 看过逐字 API 图与接线再真出（每次都是计费的）
- [ ] 产物 + `<prefix>.api.json` + `requests.jsonl` 已落盘；带标注时确认合成图也下来了
- [ ] 成品做过印面/伪字检查（模型爱题款盖印）
