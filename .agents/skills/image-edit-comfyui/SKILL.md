---
name: comfyui-image-edit
description: 通过 HTTP API 调用远程 ComfyUI（默认 http://192.168.3.5:18000）跑 Z-Image-Turbo Fun Union ControlNet 图生图/编辑工作流：上传控制图 → Canny（可关）→ ControlNet patch → 采样 → 下载；支持 prompt/seed/steps/cfg/sampler/scheduler/denoise/shift/control 强度与区间/Canny 阈值/强制尺寸/batch/文件名前缀/各模型覆盖/大图预缩放/关闭预处理器等全部参数。触发词：ComfyUI 图生图、ControlNet、controlnet union、z-image fun、Canny 生图、参考图生成、control to image、192.168.3.5、image edit。
whenToUse: 当需要用一张控制图（线稿/照片/Canny 边缘图）驱动出图，或要跑 ComfyUI 的 Z-Image-Turbo Fun Union ControlNet 工作流时使用。纯文生图用 ark-image-text-to-image 或 comfyui-text-to-image；Qwen-Image 引擎（真负向、更写实）见 comfyui-text-to-image 的 comfyui_qwen.py。
---

# ComfyUI 图生图 / ControlNet 编辑（Z-Image-Turbo Fun Union）

**用途**：给一张**控制图**，用 ControlNet 结构约束生成新图。全程走 HTTP API，可脚本化、可批量。

- 默认服务器：`http://192.168.3.5:18000`（`--server` 或 `$COMFYUI_SERVER` 覆盖）
- 工作流：`assets/z-image-turbo-fun-union-controlnet.json`（附件原样保存，v0.4 子图格式）
- 参数表：`assets/z-image-turbo-fun-union-controlnet.profile.json`（每个参数映射到接口/节点字段）
- 引擎：`scripts/comfyui_edit.py`

> 📦 **依赖**：本技能复用 `../text-to-image-comfyui/scripts/` 的转换器与 HTTP 客户端（`comfyui_convert.py` / `comfyui_gen.py`）。两个技能必须同处一个 `.agents/skills/` 目录，否则 `scripts/_shared.py` 会明确报错。

## 何时用

- 有参考图/线稿，要**按结构**生成新图（换材质、换风格、换主体，保留构图）
- 需要 ControlNet 强度/生效区间、Canny 阈值这类结构控制
- 要批量跑一批控制图

## 前置检查

```bash
cd .agents/skills/image-edit-comfyui

python3 scripts/comfyui_edit.py --check     # 四个模型文件是否在位
python3 scripts/comfyui_edit.py --list      # 工作流可用参数 + profile 参数 + 默认值
python3 scripts/comfyui_edit.py --image ref.png --prompt "..." --out-dir out/
```

`--check` 校验：`diffusion_models/z_image_turbo_bf16.safetensors`、`text_encoders/qwen_3_4b.safetensors`、`vae/ae.safetensors`、`model_patches/Z-Image-Turbo-Fun-Controlnet-Union.safetensors`。

## 执行

```bash
# 基础：上传控制图 + 提示词（输出尺寸默认 = 控制图尺寸）
python3 scripts/comfyui_edit.py --image ref.png --prompt "realistic photo, soft studio light" --out-dir out/

# 控制强度与生效区间（越小越自由；区间控制在哪几步施加控制）
python3 scripts/comfyui_edit.py --image ref.png --prompt "..." \
  --control-strength 0.6 --control-start 0.0 --control-end 0.8 --out-dir out/

# Canny 阈值（低阈值保留更多细节）
python3 scripts/comfyui_edit.py --image ref.png --prompt "..." --canny-low 0.05 --canny-high 0.25 --out-dir out/

# 采样与调度：步数/cfg/采样器/调度器/降噪/流模型 shift
python3 scripts/comfyui_edit.py --image ref.png --prompt "..." \
  --steps 12 --cfg 1.5 --sampler euler --scheduler karras --denoise 0.9 --shift 2.5 --out-dir out/

# 强制输出尺寸（会切断“跟随控制图尺寸”的连线）
python3 scripts/comfyui_edit.py --image ref.png --prompt "..." --width 768 --height 1024 --out-dir out/

# 批量 / 命名
python3 scripts/comfyui_edit.py --image ref.png --prompt "..." --batch 3 --filename-prefix myrun --out-dir out/

# 大图预缩放（默认该节点被 bypass；传参会自动启用）
python3 scripts/comfyui_edit.py --image huge.png --prompt "..." --max-dimension 1024 --scale-method lanczos --out-dir out/

# 关闭 Canny 预处理：把原图直接喂给 ControlNet（union patch 也接受原图）
python3 scripts/comfyui_edit.py --image ref.png --prompt "..." --no-preprocessor --out-dir out/

# 任意节点 bypass（重复使用）
python3 scripts/comfyui_edit.py --image ref.png --prompt "..." --disable-node PreviewImage --out-dir out/

# 复用服务器上已存在的输入图（免上传）
python3 scripts/comfyui_edit.py --image-name uploaded-ref.png --prompt "..." --out-dir out/
```

## 参数

| 参数 | 作用 | 默认 |
|------|------|------|
| `--image` / `--image-name` | 本地控制图（自动上传）/ 服务器 input 目录已有文件 | 必填其一 |
| `--prompt` | 正向提示词 | 工作流自带示例 |
| `--seed` | 随机种子（复现） | 工作流值 |
| `--steps` / `--cfg` | 采样步数 / 提示词遵循度 | 8 / 1.0 |
| `--sampler` / `--scheduler` | 采样器 / 调度器 | `res_multistep` / `simple` |
| `--denoise` | 降噪强度 | 1.0 |
| `--shift` / `--sampling` | AuraFlow shift / 采样模式 | 3.0 / `flow` |
| `--control-strength` | ControlNet 强度 | 1.0 |
| `--control-start` / `--control-end` | 控制生效区间 | 0.0 / 1.0 |
| `--canny-low` / `--canny-high` | Canny 双阈值 | 0.1 / 0.32 |
| `--width` / `--height` | **强制**输出尺寸（切断 GetImageSize 连线） | 跟随控制图 |
| `--batch` | 每次出图张数 | 1 |
| `--filename-prefix` | 输出名前缀（同时作为留档名） | `z-image-turbo-fun` |
| `--max-dimension` / `--scale-method` | 启用大图预缩放（bypass 节点）与重采样滤镜 | 关闭 / `lanczos` |
| `--no-preprocessor` | bypass Canny，原图直连 ControlNet | 关闭 |
| `--disable-node CLASS` | bypass 任意节点类（可重复） | — |
| `--unet-name` / `--clip-name` / `--vae-name` / `--controlnet-name` | 覆盖模型文件 | 工作流自带 |
| `--allow-unapplied` | 参数没有落点时不报错（默认报错退出） | 关闭（即默认 strict） |
| `--out-dir` / `--timeout` / `--quiet` / `--no-record` | 输出目录 / 等待秒数 / 静默 / 关闭留档 | `out` / 600 / — / 留档开启 |

> ⛔ **参数必须真的落到图上**：请求了但工作流里没有对应输入时，默认**直接报错退出（exit 2）**，
> 而不是跑完一张、把该参数悄悄忽略掉的图。确需放行加 `--allow-unapplied`，此时 `requests.jsonl`
> 的 `unapplied` 字段会列出被丢掉的参数——**看到非空就当这轮没跑**。

> ⛔ **无负向提示词**：工作流用 `ConditioningZeroOut` 把负向置零，`--negative` 不支持（引擎不接收该参数）。
> ⚠️ **输出尺寸默认跟随控制图**（子图内 `GetImageSize → EmptySD3LatentImage`）；要固定尺寸必须显式 `--width/--height`（引擎会切断该连线）。
> ⚠️ 工作流用 **Canny** 作控制预处理；union patch 还支持 HED/Depth/Pose/MLSD，换预处理节点即可（或用 `--no-preprocessor` 试原图直连）。

## Prompt 留档（默认开启）

每次生成在 `--out-dir` 留两份可复现凭据：

| 文件 | 内容 |
|------|------|
| `<filename-prefix>.api.json` | 实际提交的完整 API 图（含逐字 prompt、控制图名、采样器、模型、seed） |
| `requests.jsonl` | 每行一次请求：时间/引擎/`prompt_id`/参数/`control_image`/产物路径 |

与 `text-to-image-comfyui` 共用同一套留档实现。

## 示例

结构保留的画风迁移：骨瓷公主定稿（R11 肖像）→ 厚涂油画，姿势/构图/冠冕/珍珠项链全保留，只换材质与画风。
输入控制图、完整命令与保留/改变清单见 [examples/README.md](examples/README.md)，产物 `examples/example-oil-painting.png`。

## 验证

```bash
# 离线自检：转换（含 bypass/接口回接/全参数/unapplied）+ 内置 mock ComfyUI 的完整往返（含 /upload/image）
python3 scripts/test_skill.py

# 真机全参数矩阵：为每个可选参数实跑一次并比对像素
python3 scripts/verify_params.py

# 比两张图是不是同一张（判据是像素，不是文件 sha —— PNG 内嵌执行图，换前缀就会变 sha）
python3 ../image-tools/scripts/pngdiff.py a.png b.png
```

真机矩阵覆盖：基线尺寸跟随、prompt、seed（变化+复现）、steps、cfg、sampler、scheduler、denoise、shift、control 强度、control 区间、Canny 双阈值、强制尺寸、batch、文件名前缀、预缩放启用、关闭预处理器、服务器图复用、第二张控制图、**unapplied 参数报错 / 节点漂移报错 / 全 profile 参数零静默丢弃**、全参数 payload 断言、非法 patch 模型被服务器拒绝。

> 像素比对工具与判据由兄弟技能 [`image-tools`](../image-tools/SKILL.md) 提供
> （`../image-tools/scripts/pngdiff.py`，ffmpeg + numpy），所有技能的"可复现"定义因此不会漂移。

## 检查清单

- [ ] `--check` 通过（四个模型在位）
- [ ] 控制图已提供（`--image` 或 `--image-name`）
- [ ] `--prompt` 已给出；不需要负向（该工作流不支持）
- [ ] 需要固定尺寸时显式 `--width/--height`
- [ ] 大图先 `--max-dimension`（否则按原尺寸出图，显存/时间会飙升）
- [ ] 要复现时固定 `--seed`
- [ ] 产物与 `<prefix>.api.json`、`requests.jsonl` 已落盘
