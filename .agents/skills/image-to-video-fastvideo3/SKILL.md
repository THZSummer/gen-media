---
name: comfyui-image-to-video-fastvideo3
description: 通过 HTTP API 调用远程 ComfyUI（默认 http://192.168.3.5:18000）跑 FastVideo FastH3 图生视频（fl2va，首帧/可选尾帧 → 视频 + 同步音频）：上传控制图 → ImageScaleToTotalPixels 定画布 → GetImageSize → MiniMaxH3ImageToVideo，转换 UI 工作流为 /prompt API 格式，排队轮询 /history 并下载 mp4。8 步出片（DMD2 蒸馏）。触发词：ComfyUI 图生视频、i2v、fl2va、FastH3 图生视频、FastVideo、MiniMax H3、minimax_h3、首帧生视频、first frame、18000、192.168.3.5。
whenToUse: 当用户要用本机 ComfyUI 把一张静图变成带声音的短视频（尤其 192.168.3.5:18000 的 FastH3 fl2va），或要脚本化批量做首帧/尾帧驱动出片时使用。纯文生视频用 text-to-video-fastvideo3；图像编辑（ControlNet）用 comfyui-image-edit；云端图生视频走 video-gen 的 methods/image-to-video。
---

# ComfyUI 图生视频（FastVideo FastH3 fl2va · MiniMax-H3 8 步蒸馏）

**用途**：给**一张静图**（可选再给尾帧），出**带声音**的短视频。画幅**从输入图读**，不来自参数。

- 默认服务器：`http://192.168.3.5:18000`（`--server` 或 `$COMFYUI_SERVER` 覆盖）
- 工作流：`assets/video_fastvideo_fasth3_i2v.json`（ComfyUI 官方模板 "Fast Video FastH3" 的 Image-to-Video 变体）
- 权重：与文生视频技能**同一套**（FastH3 8-Step V2 + Qwen3-VL-32B + 双 VAE）
- 引擎与转换器复用 image-gen 的共享实现；与 [text-to-video-fastvideo3](../text-to-video-fastvideo3/SKILL.md) 是姊妹技能

> ✅ **技能本身已离线验证（62/62）**，且**已真机跑通**（2026-10-03，三次运行全部 success）。
> 首跑实测还裁定了一件官方文档互相矛盾的事：**蒸馏权重确实支持 fl2va**。详见下方"验证"一节。

## 前置检查

```bash
cd .agents/skills/image-to-video-fastvideo3

python3 scripts/comfyui_i2v.py --check    # 4 个模型文件 + 11 个节点类是否在位
python3 scripts/comfyui_i2v.py --list     # 工作流接口默认值 + profile 参数 + 默认值
```

## 执行

```bash
# ① 先出图（免费、不占 GPU、不上传）：确认参数真的落到图上
python3 scripts/comfyui_i2v.py --image ref.png --prompt-file shot.txt --duration 5 --plan

# ② 正式出片（首帧驱动）
python3 scripts/comfyui_i2v.py --image ref.png --prompt-file shot.txt --duration 5 \
    --megapixels 0.4 --seed 42 --out-dir out/ --timeout 3600

# ③ 首帧 + 尾帧（脚本注入一个 LoadImage 接到 last_frame）
python3 scripts/comfyui_i2v.py --image first.png --last-frame last.png \
    --prompt-file shot.txt --duration 5 --out-dir out/

# ④ 服务器上已有的图，免上传
python3 scripts/comfyui_i2v.py --image-name uploaded.png --prompt-file shot.txt --out-dir out/

# 看工作流自带的真实 prompt 样本（4 镜头 + 声音描述 + <Picture 1> 引用，6285 字符）
python3 scripts/comfyui_i2v.py --show-default-prompt
```

prompt 写法见 **[references/prompt-format.md](references/prompt-format.md)**（输入图引用句、分镜时间码、音效/配乐）。
⛔ **没有 `--prompt` 就没有默认值**：一次出片很贵，脚本不让你空手跑模板。

## 画幅：从输入图读，不是从参数读

这是与文生视频技能最大的结构差异：

```
LoadImage ──┬─→ first_frame（**原图**直接进模型）
            └─→ ImageScaleToTotalPixels(megapixels, resolution_steps)
                    └─→ GetImageSize ──→ MiniMaxH3ImageToVideo.width/height
```

- **要改比例，就改输入图**（裁剪/扩画布）。没有 `aspect_ratio` 参数。
- `--megapixels` 决定**目标画布总像素**（默认 0.4 ≈ 640×640），比例跟随输入图。
- `--resolution-steps` 是画布对齐步长（工作流默认 **32**）。
- ⚠️ 因为 `first_frame` 接的是**原图**，输入图别给太大——建议先压到与目标画布同量级（≤1MP）。

## 参数

| 参数 | 作用 | 默认 |
|------|------|------|
| `--image` / `--image-name` | 首帧：本地文件（自动上传）／服务器 input 目录已有文件 | 必填其一 |
| `--last-frame` / `--last-frame-name` | 可选尾帧（脚本注入 LoadImage 接到 `last_frame`） | 不接 |
| `--prompt` / `--prompt-file` | 提示词（长文用文件）；**必填** | — |
| `--megapixels` | 输入图缩放到多少 MP 来决定画布 | 0.4 |
| `--resolution-steps` | 画布对齐步长 | 32 |
| `--scale-method` | 定尺寸时的重采样滤镜 | `nearest-exact` |
| `--duration` / `--seconds` | 秒数 → 吸附到 17k+5 帧栅格 | 工作流值 5 |
| `--length` | 直接给帧数（**force**，切断换算） | 跟随 `--duration` |
| `--width` / `--height` | **强制**画布（**force**，切断 GetImageSize 连线） | 由输入图决定 |
| `--seed` | 随机种子（复现） | 工作流值 |
| `--steps` | 采样步数 | 8（蒸馏权重的训练步数） |
| `--sampler` / `--scheduler` / `--denoise` | 采样器 / 调度器 / 降噪 | `res_multistep` / `simple` / 1.0 |
| `--fps` | 容器帧率 | 24 |
| `--shift-video` / `--shift-audio` | H3 的 sigma shift | 10 / 3 |
| `--attention` | `comfy kitchen attention` / `pytorch attention` | `comfy kitchen attention` |
| `--sparse-selection` / `--sparse-keep-percent` / `--sparse-tau` | VSA 稀疏注意力（`vsa`/`sla`/`sol-attn`） | `vsa` / 10 / — |
| `--sparse-start` / `--sparse-end` / `--sparse-min-tokens` / `--sparse-extra-tokens` / `--sparse-dense-blocks` / `--sparse-sink` | 稀疏注意力细项 | 0.2 / 1.0 / 12288 / 256 / `""` / `exact_kv_and_rows` |
| `--video-codec` / `--video-format` / `--bit-depth` / `--color-space` | 编码与容器 | `none` / `auto` / `auto` / `sRGB` |
| `--filename-prefix` | 输出前缀（含子目录） | `video/MiniMax_H3` |
| `--unet-name` / `--clip-name` / `--vae-name` / `--audio-vae-name` | 覆盖模型文件 | 工作流自带 |
| `--set CLASS.FIELD=VALUE` | 兜底：改任何 profile 未命名的节点字段（可重复） | — |
| `--out-dir` / `--timeout` / `--poll` / `--quiet` / `--no-record` | 输出目录 / 等待秒数 / 轮询间隔 / 静默 / 关闭留档 | `out` / 3600 / 10 / — / 留档开启 |

> ⛔ **无负向提示词**：`MiniMaxH3ImageToVideo` 只有一个 `prompt` 输入。
> ⚠️ **`steps` 不要乱调**：FastH3 8-Step 是蒸馏权重，8 步即训练分布。
> ⚠️ **`--width/--height` 与 `--megapixels` 是两条路**：前者切断连线写死像素，后者让输入图定尺寸。

## ⏱️ 成本：实测比预期快得多

**实测（2026-10-03，服务器 192.168.3.5，RTX 4060 Ti 8GB，576×736 / 56 帧 / 8 步）**：

| 任务 | 墙钟耗时 | 产物 |
|------|---------|------|
| 文生视频（t2v） | **165.3 s** | 646 KB mp4 |
| 图生视频（首帧，i2v） | **180.2 s** | 761 KB mp4 |
| 图生视频（首帧+尾帧，fl2va） | **195.2 s** | 806 KB mp4 |

**约 3 分钟一条**，不是几十分钟。权重确实超出显存（UNET 20.61 GB + 文本编码器 14.61 GB +
双 VAE ≈ 35 GB 压 8 GB → 必然流式换页），但在这台机器上换页**不是瓶颈**；
早期"巨慢"的印象更可能来自**当次首批权重从磁盘加载**（35 GB 冷读）和更大的帧数/画布。

缩放规律（经验，供估时）：

- 主要随**帧数 × 画布像素**增长：56 帧 @0.42MP ≈ 3 min；5 秒 124 帧 @0.4MP 约 6–7 min
- 图生视频比文生视频多 **~15 s**（多一次图像编码），加尾帧再多 ~15 s
- **同一会话内第二次跑会快一些**（权重已热）

因此：

- 首跑用 `--duration 2 --megapixels 0.4`（约 3 分钟）验证链路，再放大
- **输入图先压到目标量级**（≤1MP）：因为 `first_frame` 接的是原图，大图会额外抬高压力
- 脚本打印并记录**实际耗时**（`elapsed_s`），用它建立自己的成本基线
- 所有参数先用 `--plan` 免费验证

## 时长与帧栅格（17k+5）

与文生视频技能一致，24fps：

| 你要 | 实际帧数 | 实际时长 |
|------|---------|---------|
| 1 s | 39 | 1.625 s |
| 2 s | 56 | 2.333 s |
| 5 s | 124 | 5.167 s |

## 输出与留档

| 文件 | 内容 |
|------|------|
| `<服务端生成名>.mp4` | 成品视频（含音频轨） |
| `<filename-prefix 的基名>.api.json` | 实际提交的完整 API 图（含输入图名、尾帧注入节点、全部参数） |
| `requests.jsonl` | 每行一次请求：时间/`prompt_id`/参数/**耗时**/`input_image`/`last_frame_image`/产物路径 |

> `--filename-prefix` 默认带子目录（`video/MiniMax_H3`），成品落在服务器 `output/video/`；
> 本地落盘只取文件名，`/view` 自动带 `subfolder=video`。留档名取前缀基名。
> 本机有 `ffprobe` 时会顺带报成品宽高/帧率/时长；没有则静默跳过。

## 验证

```bash
# 离线自检：62 项断言（首帧接线 / 画布链路 / 尾帧注入为真连线 / force 切断 /
# 参数落图 / 帧栅格 / 无悬空连线 + mock ComfyUI 全往返，含 /upload/image 与防误下载）
python3 scripts/test_skill.py

# 免费核对参数是否真的进了图（不提交、不上传、不占 GPU）
python3 scripts/comfyui_i2v.py --image ref.png --prompt-file shot.txt --duration 5 --plan
```

**已验证**：

| 项 | 结果 |
|----|------|
| 离线自检 | **62/62 通过** |
| 对服务器实况 | `--check` 通过：4 个模型 + 11 个节点类全部在位 |
| **真机首跑（2026-10-03）** | **`status: success`**，576×736 / 56 帧 / 2.333 s / AAC 32 kHz 双声道 / **180.2 s** |
| **首帧条件确实生效** | 输出首帧就是输入的那尊骨瓷公主（同款冠、项链、捧花）；与输入图 SSIM **0.929** / PSNR **30.3 dB** |
| **fl2va 真的支持** | 传首帧+尾帧跑通（195.2 s）：**帧 0 = 图 A，帧 55 = 图 B**，视频在两张图之间插值 |
| 画布链路 | `LoadImage → ImageScaleToTotalPixels → GetImageSize → width/height` 连线正确；0.4MP + 32 对齐 → 实测 576×736 |
| 时长栅格 | 实测 56 帧 / 2.333 s，与 `--plan` 预测完全一致 |
| 音频 | 三次运行（t2v / i2v / i2v+尾帧）**全部带 AAC 双声道音轨** |
| 尾帧注入 | 生成独立 LoadImage 节点并接成 `[node, slot]` 真连线，服务端接受并生效 |
| **金标准比对** | 提交图 vs 服务器执行图：**22 节点、0 处差异**（与文生视频技能同级） |
| 上传通道 | `/upload/image` 往返正常，图出现在服务端 input 列表 |
| 共享转换器回归 | 图像技能与文生视频技能的转换输出**逐字段不变** |

**仍未验证 / 已知偏差**：

- ⚠️ **首帧不是输入图的像素级复制**：SSIM 0.929 说明结构高度一致，但模型是**重绘**——
  实测有轻微重新构图与调色（首跑里镜头比原图略紧）。要"完全照搬"，请在 `[Shot 1]` 里
  把主体外观逐项写清。
- ⚠️ **多参考（Ref2VA）未验证**：本模板也只声明支持 t2va + fl2va。
- ⚠️ 只跑过 2 秒 / 0.4MP 这一档；更长的帧数与更大的画布按上文经验公式估时。
- ⚠️ **两个官方模板关于 fl2va 的说法矛盾，本次实测裁定**：真实支持 fl2va，
  故 T2V 模板那句 "supports t2va only / FL2VA 未蒸馏" 是过时的。

> 与文生视频技能一样，**不做**真机全参数矩阵（参数已在 `--plan` 层逐项断言）；
> 真机只跑"能否出片 + 条件是否生效"这一层。

## 检查清单

- [ ] `--check` 通过（4 个模型 + 11 个节点类）
- [ ] 输入图已备好，且尺寸不过大（≤1MP 量级）
- [ ] prompt 已给（含 `<Picture 1>` 引用句与声音两节）
- [ ] 已经用 `--plan` 看过参数确实落图、且**没有上传**
- [ ] 要改画幅就先改输入图；确需精确像素才用 `--width/--height`
- [ ] 首跑小画幅建立时间基线，`--timeout` 给足
- [ ] 要复现时固定 `--seed`
- [ ] 产物与 `<prefix>.api.json`、`requests.jsonl` 已落盘

## 已知限制

- **只支持 fl2va（首帧/尾帧）**：蒸馏权重未蒸馏多参考（Ref2VA），后者要换基座 MiniMax H3。
- **无负向提示词**。
- **画幅不可参数化**：想换比例只能换输入图。
- 与文生视频技能共用同一套 35 GB 权重，所以两者**不能同时跑**（显存/内存会互相挤爆）。
