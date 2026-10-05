---
name: comfyui-text-to-video-fastvideo3
description: 通过 HTTP API 调用远程 ComfyUI（默认 http://192.168.3.5:18000）跑 FastVideo FastH3 文生视频（t2va，视频+同步音频）：把 ComfyUI UI 版工作流 JSON（含 definitions.subgraphs 子图）转成 /prompt API 格式，控制 ResolutionSelector 画幅/时长，提交排队、轮询 /history、从 /view 下载 mp4。8 步出片（DMD2 蒸馏）。触发词：ComfyUI 文生视频、FastH3、FastVideo、MiniMax H3、minimax_h3、fasth3、text to video、t2va、18000、192.168.3.5、视频生成、带音频视频。
whenToUse: 当用户要用本机 ComfyUI 跑 MiniMax-H3 / FastVideo FastH3 文生视频（尤其 192.168.3.5:18000），或要脚本化批量出带音频的短视频时使用。云端 Seedance 文生视频走 video-gen 的 methods/text-to-video；纯文生图用 comfyui-text-to-image。
---

# ComfyUI 文生视频（FastVideo FastH3 · MiniMax-H3 8 步蒸馏）

**用途**：给一段**结构化的 prompt**，出一段**带声音的短视频**。全程走 HTTP API，可脚本化、可批量。

- 默认服务器：`http://192.168.3.5:18000`（`--server` 或 `$COMFYUI_SERVER` 覆盖）
- 工作流：`assets/video_fastvideo_fasth3_t2v.json`（ComfyUI 官方模板 "Fast Video FastH3"，v0.33.0 子图格式）
- 权重：FastVideo **FastH3 8-Step V2**（DMD2 蒸馏）+ Qwen3-VL-32B 文本编码器 + 双 VAE（视频/音频）
- 引擎复用 image-gen 的共享转换器，只换工作流与参数 profile

## 前置检查

```bash
cd /home/usb/wks/gits/Book/video-gen/skills/text-to-video-fastvideo3

python3 scripts/comfyui_video.py --check    # 4 个模型文件 + 9 个节点类是否在位
python3 scripts/comfyui_video.py --list     # 工作流接口默认值 + profile 参数 + 默认值
```

`--check` 同时校验**模型**和**节点类**——视频节点比图像节点新，ComfyUI 版本偏旧时是节点缺失而不是模型缺失。

## 执行

```bash
# ① 先出图（免费、不占 GPU）：确认参数真的落到图上
python3 scripts/comfyui_video.py --prompt-file shot.txt --duration 5 --plan

# ② 正式出片
python3 scripts/comfyui_video.py --prompt-file shot.txt --duration 5 \
    --aspect-ratio "16:9 (Widescreen)" --megapixels 0.4 --seed 42 \
    --out-dir out/ --timeout 3600

# 强制精确画布（会切断 ResolutionSelector 的连线）
python3 scripts/comfyui_video.py --prompt-file shot.txt --width 768 --height 1344 --out-dir out/

# 直接给帧数（会切断秒数→帧数的换算）
python3 scripts/comfyui_video.py --prompt-file shot.txt --length 124 --out-dir out/

# 看工作流自带的真实 prompt 样本（3 镜头 + 声音描述，3402 字符）
python3 scripts/comfyui_video.py --show-default-prompt
```

prompt 写法见 **[references/prompt-format.md](references/prompt-format.md)**（三节结构、分镜时间码、音频描述）。
⛔ **没有 `--prompt` 就没有默认值**：工作流自带一段很长的示例 prompt，而一次出片很贵，所以脚本故意不让你"空手跑模板"。

## 参数

| 参数 | 作用 | 默认 |
|------|------|------|
| `--prompt` / `--prompt-file` | 提示词（长文用文件）；**必填** | — |
| `--duration` / `--seconds` | 秒数 → 吸附到 17k+5 帧栅格 | 工作流值 5 |
| `--length` | 直接给帧数（**force**，切断换算） | 跟随 `--duration` |
| `--aspect-ratio` | `1:1 (Square)` / `16:9 (Widescreen)` / `9:16 (Portrait Widescreen)` 等 8 种 | `1:1 (Square)` |
| `--megapixels` | ResolutionSelector 目标像素数 | 0.4 |
| `--multiple` | 画布对齐倍数 | 32 |
| `--width` / `--height` | **强制**画布（**force**，切断 ResolutionSelector 连线） | 由 ResolutionSelector 决定 |
| `--seed` | 随机种子（复现） | 工作流值 |
| `--steps` | 采样步数 | 8（蒸馏权重的训练步数，见下） |
| `--sampler` / `--scheduler` / `--denoise` | 采样器 / 调度器 / 降噪 | `res_multistep` / `simple` / 1.0 |
| `--fps` | 容器帧率 | 24 |
| `--shift-video` / `--shift-audio` | H3 的 sigma shift（视频/音频） | 10 / 3 |
| `--attention` | `comfy kitchen attention` / `pytorch attention` | `comfy kitchen attention` |
| `--sparse-selection` | VSA 稀疏注意力选择：`vsa` / `sla` / `sol-attn` | `vsa` |
| `--sparse-keep-percent` | 保留关键块百分比（vsa/sla 用；FastH3-VSA 训练值 10） | 10 |
| `--sparse-tau` | 仅 `sol-attn` 用的稀疏阈值 | — |
| `--sparse-start` / `--sparse-end` | 稀疏生效区间 | 0.2 / 1.0 |
| `--sparse-min-tokens` / `--sparse-extra-tokens` / `--sparse-dense-blocks` / `--sparse-sink` | 稀疏注意力细项 | 12288 / 256 / `""` / `exact_kv_and_rows` |
| `--video-codec` | CreateVideo 容器编解码：`none` / `auto` / `h264` / `av1` | `none` |
| `--video-format` | SaveVideo 写出的容器：`auto` / `mp4` / `mkv` / `webm` | `auto` |
| `--bit-depth` / `--color-space` | `auto`/8/10 ／ `sRGB`/`HDR`/`HDR PQ` | `auto` / `sRGB` |
| `--filename-prefix` | 输出前缀（含子目录） | `video/MiniMax_H3` |
| `--unet-name` / `--clip-name` / `--vae-name` / `--audio-vae-name` | 覆盖模型文件 | 工作流自带 |
| `--set CLASS.FIELD=VALUE` | 兜底：改任何 profile 未命名的节点字段（可重复） | — |
| `--out-dir` / `--timeout` / `--poll` / `--quiet` / `--no-record` | 输出目录 / 等待秒数 / 轮询间隔 / 静默 / 关闭留档 | `out` / 3600 / 10 / — / 留档开启 |

> ⛔ **无负向提示词**：`MiniMaxH3ImageToVideo` 只有一个 `prompt` 输入，工作流里也没有负向编码节点。
> ⚠️ **`steps` 不要乱调**：FastH3 8-Step 是蒸馏权重，8 步就是它的训练分布；调高只会更慢，不会更细。
> ⚠️ **`--width/--height` 与 `--aspect-ratio/--megapixels` 是两条路**：前者切断连线写死像素，后者让
> ResolutionSelector 算；同时给会被 `--plan` 如实显示（width/height 胜出）。

## ⏱️ 成本：实测约 3 分钟一条

权重构成（决定它**可能**很慢的原因）：

| 项 | 值 |
|----|-----|
| UNET（FastH3 8-Step V2, int8） | **20.61 GB** |
| 文本编码器（Qwen3-VL-32B, nvfp4-awq） | **14.61 GB** |
| 视频 VAE + 音频 VAE | 2.62 GB + 0.58 GB |
| 目标显卡 | RTX 4060 Ti **8 GB** |

**但实测并不慢**（2026-10-03，576×736 / 56 帧 / 8 步）：

| 任务 | 墙钟耗时 |
|------|---------|
| **文生视频（本技能）** | **165.3 s** |
| 图生视频（首帧） | 180.2 s |
| 图生视频（首帧+尾帧） | 195.2 s |

35 GB 权重压 8 GB 显存确实是**流式换页**，但在这台机器上换页不是瓶颈；
"巨慢"的印象更可能来自**当次首批权重从磁盘加载**（35 GB 冷读）与更大的帧数/画布。
估时经验：主要随**帧数 × 画布像素**增长（5 秒 124 帧约 6–7 分钟），同一会话内第二次跑会更快（权重已热）。

因此：

- 先用 `--megapixels 0.4` + `--duration 2`（约 3 分钟）跑通链路，再放大
- 模板给的 H3 原生画布是 **短边 768、上限 768×1344、32 的倍数**；`ResolutionSelector` 是唯一的
  官方画幅入口（默认 1:1 / 0.4MP / 32 → **640×640**）
- 脚本会打印**实际耗时**（`elapsed_s`）并写进 `requests.jsonl`，用它来建立你自己的成本基线
- 所有参数先用 `--plan` 免费验证，别用真机跑参

## 时长与帧栅格（17k+5）

`duration`(秒) 经 `PrimitiveFloat → ComfyMathExpression` 吸附到 **17k+5** 帧栅格，24fps：

```
length = max(5, round(duration*24)) + (5 - (max(5, round(duration*24)) % 17)) % 17
```

| 你要 | 实际帧数 | 实际时长 |
|------|---------|---------|
| 1 s | 39 | 1.625 s |
| 2 s | 56 | 2.333 s |
| 5 s | 124 | **5.167 s** |

（5 秒 → 124 帧这一行是用服务端真实执行过的成品反推验证的：成品 `duration=5.167`。）

## 输出与留档

每次生成在 `--out-dir` 落三样：

| 文件 | 内容 |
|------|------|
| `<服务端生成名>.mp4`（如 `MiniMax_H3_00003_.mp4`） | 成品视频（含音频轨） |
| `<filename-prefix 的基名>.api.json` | **实际提交的完整 API 图**（逐字 prompt、画幅、seed、采样器、全部参数） |
| `requests.jsonl` | 每行一次请求：时间/`prompt_id`/参数/**耗时**/产物路径/ffprobe 摘要 |

> `--filename-prefix` 默认带子目录（`video/MiniMax_H3`），所以成品在服务器的 `output/video/` 下；
> 本地落盘时只取文件名，`/view` 会自动带上 `subfolder=video`。留档名取前缀的**基名**
> （`video/MiniMax_H3` → `MiniMax_H3.api.json`），否则本地会多出一层并不存在的目录。
> 若本机有 `ffprobe`，脚本会顺带报出成品的宽高/帧率/时长；没有就静默跳过。

## 验证

```bash
# 离线自检：57 项断言（参数落图 / force 切断连线 / 帧栅格 / 无悬空连线 +
# 内置 mock ComfyUI 的完整往返，含"临时预览不得被当成品下载"）
python3 scripts/test_skill.py

# 免费核对参数是否真的进了图（不提交、不占 GPU）
python3 scripts/comfyui_video.py --prompt-file shot.txt --duration 5 --plan
```

> 这个技能**没有**真机全参数矩阵：单次出片成本太高（见上），不适合像图像技能那样跑 20+ 次。
> 替代方案是三层验证：`test_skill.py` 覆盖转换与 HTTP 往返，`--plan` 覆盖参数落图，
> 再用**服务端 `/history` 里真实执行过的图**做逐字段比对（20 节点、0 处不一致）。
>
> **真机实测（2026-10-03）**：`--duration 2 --aspect-ratio "3:4 (Portrait Standard)" --megapixels 0.4`
> → `status: success`，576×736 / 56 帧 / 2.333 s / AAC 32 kHz 双声道 / **165.3 s**，
> 画面内容与 prompt 描述逐项吻合（银冠蓝宝石、珍珠项链、蕾丝礼服、瓷玫瑰捧花、纱幕扬起、镜头推近）。

## 检查清单

- [ ] `--check` 通过（4 个模型 + 9 个节点类）
- [ ] prompt 已给（含 `overall_soundscape` / `non_diegetic_music` 两节，否则声音不可控）
- [ ] 已经用 `--plan` 看过参数确实落图
- [ ] 画幅用 `--aspect-ratio` + `--megapixels`；确需精确像素才用 `--width/--height`
- [ ] 首跑用小画幅（`--megapixels 0.4` + `--duration 2`，约 3 分钟）建立时间基线
- [ ] 要复现时固定 `--seed`
- [ ] 产物与 `<prefix>.api.json`、`requests.jsonl` 已落盘

## 已知限制

- **t2va 与 fl2va 都支持**（fl2va 由真机实测确认，见姊妹技能
  [image-to-video-fastvideo3](../image-to-video-fastvideo3/SKILL.md)）；
  **多参考（Ref2VA）未蒸馏**，要它得换基座 MiniMax H3。
  ⚠️ 本模板自带的 MarkdownNote 写的是 "supports t2va only；FL2VA 未蒸馏"——**这句已过时**，
  实测首尾帧可用。
- **无负向提示词**。
- 画幅/时长之外的画质旋钮很少：这套图的自由度主要在 prompt、画幅、steps（固定 8）与稀疏注意力。
