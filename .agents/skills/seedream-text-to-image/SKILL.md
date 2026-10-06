---
name: seedream-text-to-image
description: 通过本机 ComfyUI（默认 http://192.168.3.5:18000）的 ByteDance Seedream 付费 partner 节点出图：**模型跑在云端**（seedream 5.0 pro / flash / lite、4.5、4.0），本机不需要任何权重；脚本把 UI 工作流转成 /prompt API 图、按节点 schema 校验参数、带上 ComfyUI 账号凭据提交、轮询 /history、下载成品并留档。支持 prompt / 模型 / 尺寸预设与 Custom / seed / thinking / watermark / prompt_optimization / max_images / 保存格式。触发词：Seedream、seedream 5.0、即梦、ByteDance 生图、ComfyUI 云端模型、partner 节点、付费出图、seedream text to image。
whenToUse: 当用户要用 ComfyUI 的 ByteDance Seedream（远端付费模型）出图，或要把桌面端点 Run 跑通的那套 Seedream 工作流脚本化时使用。要跑**本机权重**的文生图改用 comfyui-text-to-image；要直连火山方舟 ARK 按量出 Seedream 图（不经过 ComfyUI）见 methods/text-to-image。
---

# Seedream 文生图（ComfyUI partner 节点 · 远端付费模型）

**用途**：把 `assets/seedream-5.0-pro-t2i-ui.json` 这份工作流提交到 ComfyUI，拿回图片落盘。
工作流里只有一个模型节点 `ByteDanceSeedreamNodeV3` —— 它是 ComfyUI 的 **partner / API 节点**：
本机只做编排，**推理在 ByteDance 云端**，按张计费。

- 默认服务器：`http://192.168.3.5:18000`（`--server` 或 `$COMFYUI_SERVER` 覆盖）
- 工作流：`assets/seedream-5.0-pro-t2i-ui.json`（桌面版导出的原件，逐字节保留）
- 节点事实 / 鉴权 / 踩坑：`references/api-node.md`（**先读这页**）
- schema 快照：`references/node-info.json`（离线对账用）
- 引擎：`scripts/seedream_gen.py`，转换与校验：`scripts/seedream_api.py`

> 📦 **依赖**：本技能自带转换器与 HTTP 客户端，**不依赖** `text-to-image-comfyui` 的脚本
> （那份转换器面向子图工作流，对这份扁平的两节点工作流直接报错）。只依赖 Python 3 标准库；
> `verify_params.py` 的像素判据需要 `ffmpeg`。

## ⛔ 先看这条：付费节点要凭据，桌面端点 Run 能出图不代表脚本能出图

在桌面版界面点 Run 用的是**前端浏览器登录态**，服务端自己**没存**凭据（实测 `comfy.settings.json`
里没有任何 key）。无头请求必须自带凭据，否则执行阶段一定报：

```
Unauthorized: Please login first to use this node.
```

ComfyUI 服务端认两个 `extra_data` 键（源码 `comfy_api_nodes/util/_helpers.py`：前者发
`Authorization: Bearer …`，后者发 `X-API-KEY: …`），本技能两个都能给：

| 通道 | 参数 / 环境变量 | 从哪来 |
|------|----------------|--------|
| **API Key**（推荐） | `--api-key` / `--api-key-file <文件>` / `$COMFYUI_API_KEY`（`$COMFY_API_KEY` 也认） | [platform.comfy.org](https://platform.comfy.org) → API Keys → `+ New`，账号要有 credits |
| Bearer token | `--auth-token` / `$COMFYUI_AUTH_TOKEN` | 桌面端 OAuth 登录态，会过期；只有拿得到时才用 |

命中的顺序是 `--api-key` > `--api-key-file` > 环境变量 > `--auth-token`（前一条命中就不看后面的）。
也可以把同一个 API Key 填进 ComfyUI 的 **Settings → User → 用 API Key 登录**，让服务端替所有无头
请求带上；但**邮箱/浏览器登录不写服务端**，那种"我配置过"对脚本无效——这就是界面能出图、脚本报
`Unauthorized` 的全部原因。**凭据不进留档**：`requests.jsonl` 只记 `credential_channel` / `credential_source`。

## 何时用 / 何时不用

| | 技能 |
|---|---|
| 要 Seedream（云端、按张计费、本机零权重） | **本技能** |
| 要本机权重文生图（Z-Image-Turbo 快 / Qwen-Image 细） | [comfyui-text-to-image](../text-to-image-comfyui/SKILL.md) |
| 有控制图、要 ControlNet 结构约束 | [comfyui-image-edit](../image-edit-comfyui/SKILL.md) |
| 直连火山方舟 ARK 出 Seedream（另一套账，不经过 ComfyUI） | [methods/text-to-image](../../../methods/text-to-image/README.md) |

## 前置检查

```bash
cd .agents/skills/seedream-text-to-image

python3 scripts/seedream_gen.py --check    # 探活 + 节点在不在 + 模型列表 + schema 对账 + 凭据
python3 scripts/seedream_gen.py --list     # 每个模型支持哪些参数、有哪些尺寸预设
```

`--check` 的解读（**它证明不了能出图**）：

| 字段 | 含义 |
|------|------|
| `nodes.ByteDanceSeedreamNodeV3` | 节点类在不在（ComfyUI 太旧、或启动带了 `--disable-partner-nodes`/`--offline` 会不在） |
| `schema_drift` | 真机 `/object_info` 与 `references/node-info.json` 的差异；不是 `none` 就说明服务器换了模型/参数，先更新快照 |
| `model_files_needed` | 恒为空 —— 权重在云端，本机不需要（这不是漏检） |
| `credential.present` | 有没有拿到凭据；`false` 时照 `hint` 补 |
| 退出码 | `0` 正常 ｜ `2` 不可达 ｜ `3` 没有这个节点 |

## 执行

```bash
# 先看逐字 API 图（不花钱）
python3 scripts/seedream_gen.py --prompt "九尾狐 素描 线稿" --dry-run

# 最小出图
python3 scripts/seedream_gen.py --prompt "九尾狐 素描 线稿" --size 1024x1024 --out-dir out/

# 长提示词走文件；固定 seed 便于复跑
python3 scripts/seedream_gen.py --prompt-file p.txt --seed 1766827367 --out-dir out/

# 竖幅 + 关 thinking（pro 的 thinking 会明显加时间）
python3 scripts/seedream_gen.py --prompt-file p.txt --size 1440x2560 --no-thinking --out-dir out/

# 换更便宜的档 / 换模型（注意不同模型的参数面不同）
python3 scripts/seedream_gen.py --prompt "..." --model "seedream 5.0 lite" --size "2048x2048" --out-dir out/

# 派生多张关联图（仅 lite / 4.5 / 4.0）
python3 scripts/seedream_gen.py --prompt "..." --model "seedream 5.0 lite" --max-images 3 --out-dir out/

# 凭据
python3 scripts/seedream_gen.py --prompt "..." --api-key-file ../../../work/comfy_api_key --out-dir out/
```

## 参数

| 参数 | 作用 | 默认 |
|------|------|------|
| `--prompt` / `--prompt-file` | 提示词（二选一，必给一个） | 工作流自带 |
| `--model` | 模型键（5 个可选，见 `--list`） | `seedream 5.0 pro`（工作流值） |
| `--size` | 尺寸：预设原文 / `1024x1024` / `1:1` | `(1K) 1024x1024 (1:1)` |
| `--width` / `--height` | 只在 `--size Custom`（或只给宽高、成对）时有意义 | 2048 / 2048 |
| `--seed` | 随机种子 | 工作流值 |
| `--thinking` / `--no-thinking` | 提示词遵循度推理（pro/lite/4.5/4.0 支持，更慢） | 工作流值（true） |
| `--prompt-optimization {standard,fast}` | 仅 `seedream 5.0 pro` | 工作流值（standard） |
| `--watermark` / `--no-watermark` | 加/不加 "AI generated" 水印 | 工作流值（false） |
| `--max-images` | 一次要几张关联图（仅 lite/4.5/4.0） | 工作流值 |
| `--fail-on-partial` / `--no-fail-on-partial` | 缺图即失败（仅 lite/4.5/4.0） | 工作流值 |
| `--format` / `--bit-depth` | 保存格式（png/exr/avif）与位深 | 工作流值（png / 8-bit） |
| `--filename-prefix` | 输出前缀（同时是留档名） | 工作流值 `Seedream5.0_Pro_T2I` |
| `--api-key` / `--api-key-file` | ComfyUI 账号凭据（见上） | `$COMFYUI_API_KEY` |
| `--dry-run` | 只打印 API 图，不提交 | 关闭 |
| `--out-dir` / `--timeout` / `--poll` / `--quiet` / `--no-record` | 输出目录 / 等待秒数 / 轮询间隔 / 静默 / 关留档 | `out` / 900 / 3 / — / 留档开启 |
| `--allow-unapplied` | 参数对所选模型不存在时不报错（默认报错退出 8） | 关闭 |

**退出码**：`0` 成功 ｜ `1` 没下到图 ｜ `2` 服务器不可达 ｜ `3` 没有该节点 ｜
`4` 鉴权被拒 ｜ `5` 服务器拒了这张图（HTTP 400） ｜ `6` 节点执行报错 ｜
`7` 超时 ｜ `8` 参数不成立（未知模型 / 该模型不支持该参数 / 尺寸非法）。

> ⛔ **参数不静默丢弃**：请求了所选模型没有的输入（例如给 flash 传 thinking、给 pro 传 max-images），
> 默认直接报错退出，而不是跑到云端出一张"参数其实没生效"的图。确需放行加 `--allow-unapplied`，
> 此时 `requests.jsonl` 的 `unapplied` 会列出被丢掉的参数——**看到非空就当这轮没跑**。

## 留档（默认开启）

| 文件 | 内容 |
|------|------|
| `<filename-prefix>.api.json` | 实际提交的整张 API 图（逐字 prompt、模型、尺寸预设、seed、保存格式） |
| `requests.jsonl` | 每行一次请求：时间 / 引擎 / `prompt_id` / 参数 / 产物路径 / `api_key_used` / `api_key_source` |

## 踩坑点

- **输入名带点**：API 格式用 `model.size_preset`、`model.thinking`、`format.bit_depth` 这种名字；
  写成 `height` 会被服务器判 `Required input is missing`（`references/api-node.md` §3 有 400 原文）。
- **每个模型支持的东西不一样**：flash 连 `thinking` 都没有，pro 没有 `max_images`；
  `--list` 是唯一可信来源，schema 快照更新前别照抄别人的命令。
- **`size_preset` 与 `width/height` 的关系**：宽高只在预设为 `Custom` 时生效；
  工作流里写着 2048×2048 但预设是 1K，出图就是 1024×1024。
- **`model.images` 不是必填**：schema 把它列在 `required` 下，但纯文生图不给也能过校验（实测 200）。
  本技能只做文生图，不接参考图；要多图参考请用 pro 的编辑能力（见 methods 文档）或另建技能。
- **别拿 `show_signin_button` 判断登录**：那是 Desktop 注入的启动 feature flag，与登录态无关。
- **付费即计费**：每次重试都是真花钱；先 `--dry-run`，再固定 `--seed` 复跑。
- **`--timeout` 默认 900s 是留余量的**：实测 pro 1K + thinking 端到端约 **63 秒**
  （2K/4K 或排队时会明显更久）；超时后任务可能仍在云端跑，去 ComfyUI 队列里看，别急着重复提交。
- **同 seed 重跑"像素一致"可能只是 ComfyUI 缓存**：缓存按节点输入命中，输入没变就不会再调云端。
  引擎会把这次执行里被缓存的节点放在 `cached_nodes` 里；要真测远端模型复现性，得让服务器带
  `--cache-none` 重启。

## 验证

```bash
# 离线自检：转换（与真机实测被接受的那张图逐字节比对）+ 参数面 + mock 往返 + 错误分类
python3 scripts/test_skill.py

# 真机探活与 schema 对账（不花钱）
python3 scripts/seedream_gen.py --check

# 真机参数矩阵（**付费**：默认 6 张图，需要凭据；没有凭据会 SKIPPED 退出）
python3 scripts/verify_params.py --api-key-file <key文件> --yes
```

判据：尺寸看 **PNG 头解出来的真实宽高**；"参数是否生效"看**解码后的像素**（`ffmpeg` 解成 raw RGB24
再哈希），不看文件哈希（PNG 里嵌了执行图，换个前缀哈希就变）。同 seed 重跑是否逐像素一致
**只记录不判定**——远端模型的复现性不能假设。更细的差异比较可用
[image-tools](../image-tools/scripts/pngdiff.py) 的 PSNR/SSIM。

> **验证状态**（详见 `references/api-node.md` §5）：**已真机跑通**。首次出图
> （pro 1K + thinking）端到端 63 秒、1024×1024 PNG；参数矩阵 6/6 通过（换 seed 像素会变、
> `--size 1440x2560` 落成 1440×2560、`--no-thinking` 与换 flash 模型都能出图），合计 3 分 41 秒。
> 仍未验证：水印、`fast` 提示词优化、lite/4.5/4.0 的 `--max-images`、2K/4K 档，
> 以及"远端模型本身是否可复现"（缓存会挡住这件事，要 `--cache-none` 才测得准）。

## 检查清单

- [ ] `--check` 通过（节点在位、`schema_drift: none`）
- [ ] 凭据已给（`--api-key-file` / `$COMFYUI_API_KEY`），否则预期 exit 4
- [ ] `--prompt` / `--prompt-file` 已给；长提示词走文件
- [ ] 参数对所选模型成立（先 `--list` 确认，别跨模型抄）
- [ ] 尺寸用 `--size` 写（预设或 `WxH`），不是"横图硬裁"
- [ ] 要复现就固定 `--seed`（并接受"同 seed 未必同像素"）
- [ ] `--dry-run` 看过逐字 API 图再真出（每次都是计费的）
- [ ] 产物与 `<prefix>.api.json`、`requests.jsonl` 已落盘
