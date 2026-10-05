---
name: comfyui-text-to-image
description: 通过 HTTP API 调用远程 ComfyUI（默认 http://192.168.3.5:18000）跑 Z-Image-Turbo 文生图工作流出图：把 ComfyUI UI 版 workflow JSON（含 definitions.subgraphs 子图）转成 /prompt API 格式，提交排队、轮询 /history、从 /view 下载成品到本地。触发词：ComfyUI、comfy、z-image、z-image-turbo、18000、192.168.3.5、工作流生图、跑 workflow、远程出图、text to image comfyui。
whenToUse: 当用户要求用 ComfyUI（尤其 192.168.3.5:18000 的 Z-Image-Turbo 文生图工作流）出图时使用。若要用火山方舟 Seedream 云端 API 出图，改用 ark-image-text-to-image。
---

# ComfyUI 文生图（远程 API · 双引擎）

**用途**：把本技能自带的 ComfyUI 工作流提交到远程 ComfyUI 服务器，拿回图片落盘。全程走 HTTP API，不需要打开 ComfyUI 网页，也不需要在本机装 ComfyUI。

- 默认服务器：`http://192.168.3.5:18000`（可用 `--server` 或环境变量 `COMFYUI_SERVER` 覆盖）
- 工作流：`assets/z-image-turbo-ui.json`（Z-Image-Turbo 文生图，含子图定义）
- 脚本：`scripts/comfyui_convert.py`（UI→API 转换）、`scripts/comfyui_gen.py`（提交+轮询+下载）

## 两个引擎怎么选

| 引擎 | 脚本 | 速度 | 细节/写实 | 负向提示词 | 何时用 |
|------|------|------|-----------|-----------|--------|
| **Z-Image-Turbo** | `comfyui_gen.py` | 快（约 10–60s/张） | 中等，偏风格化 | ❌ 无（`ConditioningZeroOut`） | 快速草稿、构图与机位探索、大批量 |
| **Qwen-Image 2512** | `comfyui_qwen.py` | 慢（约 7–10 min/张，8GB 显存） | **高，接近实物摄影** | ✅ **有真负向** | 成品、需要丰富细节与材质真实感 |

```bash
# Qwen-Image（细节引擎）：先自检模型，再出图
python3 scripts/comfyui_qwen.py --check
python3 scripts/comfyui_qwen.py --prompt "..." --negative "blurry, plastic, cartoon, text" \
  --width 1024 --height 1360 --steps 24 --cfg 3.0 --seed 7 --out-dir out/
```

> 依赖的三个模型文件（服务器上需存在）：`diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors`、`text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors`（CLIP type=`qwen_image`）、`vae/qwen_image_vae.safetensors`。
> 服务器另有 `TextEncodeQwenImage21`（原生 prompt+negative_prompt），本技能走经典 `CLIPTextEncode` 图，已验证可用。

## 何时用

- 用户说"用 ComfyUI 出图 / 跑这个 workflow / z-image-turbo 生图 / 连 192.168.3.5:18000"
- 手里有 ComfyUI 导出的 UI workflow JSON（`nodes` + `definitions.subgraphs` 结构）

## 前置检查（先做，别直接生成）

```bash
cd skills/text-to-image-comfyui

# 1. 服务器是否可达（不可达就别提交，直接报障）
python3 scripts/comfyui_gen.py --server http://192.168.3.5:18000 --check

# 2. 看工作流暴露哪些参数（确认模型文件名与默认值）
python3 scripts/comfyui_convert.py assets/z-image-turbo-ui.json --list

# 3. 确认服务器上确实有工作流要用的三个模型（名字必须完全一致）
python3 scripts/comfyui_gen.py --list-models diffusion_models   # z_image_turbo_bf16.safetensors
python3 scripts/comfyui_gen.py --list-models text_encoders      # qwen_3_4b.safetensors
python3 scripts/comfyui_gen.py --list-models vae                # ae.safetensors
```

## 执行

```bash
# 出图（同步等待并下载，默认 600s 超时）
python3 scripts/comfyui_gen.py \
  --prompt "a red fox in snow, cinematic, shallow depth of field" \
  --width 1024 --height 1024 --steps 8 --seed 42 \
  --out-dir out/

# 快速小图试跑（先定方向再出大图）
python3 scripts/comfyui_gen.py --prompt "..." --width 768 --height 768 --steps 6 --out-dir out/draft/

# 只要 API JSON、不提交（排查参数用）
python3 scripts/comfyui_convert.py assets/z-image-turbo-ui.json \
  --prompt "..." --width 1024 --height 1024 -o /tmp/api.json
```

输出是 JSON，关键字段：`prompt_id`、`images`（服务器侧 filename/subfolder/type）、`local_paths`（本地落盘路径）、`status`。

## Prompt 留档（默认开启）

每次生成都会在 `--out-dir` 里留下可复现凭据，**不需要额外操作**：

| 文件 | 内容 |
|------|------|
| `<filename-prefix>.api.json` | **实际提交给 ComfyUI 的完整 API 图**（逐字 prompt、采样器、模型名、seed…） |
| `requests.jsonl` | 每行一次请求：时间 / 引擎 / prompt_id / 参数 / **prompt 原文** / 产物路径 / **unapplied**（追加写） |

`unapplied` 是本技能的新字段：请求了但**没能落到图上**的参数名。正常情况下它是 `{}`；
非空说明这次实验有一个参数其实没生效——**该轮结论不可信**，必须修掉再跑。

```bash
# 默认就会落盘：
python3 scripts/comfyui_gen.py --prompt "..." --filename-prefix myrun --out-dir out/
# out/myrun.api.json + out/requests.jsonl + 图片

# 不需要留档时显式关闭：
python3 scripts/comfyui_gen.py --prompt "..." --no-record --out-dir /tmp/scratch/
```

> 两个引擎（`comfyui_gen.py` / `comfyui_qwen.py`）行为一致；Qwen 的 `requests.jsonl` 还会记录 `negative`。
> 想核对服务器侧记录：`GET /history/{prompt_id}`（`prompt_id` 在 jsonl 里）。

## 参数必须真的生效（否则报错）

**参数的静默失效是本技能最贵的故障**：任务正常排队、正常出图、留档也照记，
唯一症状是这张图悄悄忽略了你的指令——然后你会去怪提示词。

- `comfyui_gen.py` / `comfyui_convert.py` 默认 **strict**：参数找不到落点就报错退出（exit 2），不留一份假的成功记录
- `comfyui_qwen.py` 也是 strict：未知关键字直接 `ValueError`（它的图是 Python 里拼的，没有"落点"概念）
- 确实要放行（例如故意给一个可能不存在的参数）用 `--allow-unapplied`，此时 `requests.jsonl` 的 `unapplied` 会列出它们

判据是**拿最终要提交的 API 图核对**，不是"写没写过"：一个值可能写进了子图内部、
却被父图连过来的线覆盖（例如顶层 `ResolutionSelector` 驱动子图 `width/height`），
节点也可能被 bypass 掉——**这两种情况都算没落地**。

```bash
# 拿 video 工作流（没有 EmptySD3LatentImage）当反例：--width 落不下去
python3 scripts/comfyui_convert.py ../../../skills/text-to-video-fastvideo3/assets/video_fastvideo_fasth3_t2v.json \
    --prompt "a cat" --width 512 -o /tmp/x.json
# error: 1 requested parameter(s) never reached the graph: width=512 ... [exit 2]

# 同一个图带上它自己的 profile，width 就会落到 MiniMaxH3ToVideo.width → 正常通过
```

> ⚠️ 命令行**拼错参数名**由 `argparse` 拦下（`--widht` → `unrecognized arguments`，同样 exit 2），
> 这里防的是另一类：**参数名合法、但工作流里没有对应输入**（节点改名/被删、profile 漂移、父图连线覆盖）。


## 参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `--server` | ComfyUI 地址 | `http://192.168.3.5:18000` / `$COMFYUI_SERVER` |
| `--workflow` | UI workflow JSON | `assets/z-image-turbo-ui.json` |
| `--prompt` | 正向提示词（必填） | 工作流自带示例 |
| `--width` / `--height` | 出图尺寸（像素，非 `--ratio`） | 1024 / 1024 |
| `--steps` | 采样步数 | 8 |
| `--seed` | 随机种子，固定可复现 | 0（工作流默认 `randomize`） |
| `--unet-name` / `--clip-name` / `--vae-name` | 覆盖模型文件 | 工作流自带三个文件名 |
| `--filename-prefix` | 输出文件名前缀（SaveImage）；同时作为留档文件名 | `z-image-turbo` |
| `--no-record` | 关闭 prompt/图 留档（默认开启） | 关闭留档 |
| `--allow-unapplied` | 参数没有落点时不报错（默认报错退出） | 关闭（即默认 strict） |
| `--out-dir` | 本地保存目录 | `out` |
| `--timeout` | 等待出图秒数 | 600 |
| `--check` / `--list-models FOLDER` | 探测服务器 / 列模型 | - |

> ⚠️ 工作流的 `KSampler` 使用 `control_after_generate=randomize`，所以**不传 `--seed` 时每次结果不同**；要复现就固定 `--seed`。

## 工作流要点（z-image-turbo）

- 子图 `Text to Image (Z-Image-Turbo)` 暴露 8 个输入：`text/width/height/seed/steps/unet_name/clip_name/vae_name`；输出 `IMAGE` 接到顶层 `SaveImage`
- 实际执行的 10 个节点：`CLIPLoader → CLIPTextEncode`（正向）+ `ConditioningZeroOut`（负向置零）、`UNETLoader → ModelSamplingAuraFlow`、`EmptySD3LatentImage`、`KSampler(res_multistep/simple, cfg=1) → VAEDecode → SaveImage`
- `MarkdownNote` 只是说明卡片，转换时会自动剔除（不能进 API prompt）
- 模型文件（ComfyUI 目录）：`diffusion_models/z_image_turbo_bf16.safetensors`、`text_encoders/qwen_3_4b.safetensors`、`vae/ae.safetensors`

## 踩坑点

- ⛔ **UI JSON 不能直接 POST /prompt**：`/prompt` 要的是扁平 `{node_id: {class_type, inputs}}`；本技能的新版工作流把图放在 `definitions.subgraphs` 里，且节点 `type` 是 UUID、`inputs[].link` 为 null（连接信息在 `inputs[].links`），必须经 `comfyui_convert.py` 展开
- ⛔ **ComfyUI 不报"排队中"**：`/history/{prompt_id}` 只在任务结束后才有记录，所以轮询要等到 key 出现，不能拿 200 当完成
- ⛔ **模型名必须完全一致**：`--unet-name` 等写错会在 `/prompt` 返回 `node_errors` 或执行时报模型找不到
- ⛔ **参数没生效时不要以为它生效了**：工作流没有对应输入（拼错名字、或节点被改过）时，参数会被丢掉而**任务照跑**。
  现在这是硬错误（`UnappliedOverrideError`，exit 2），但**从别处拿到一份旧 `requests.jsonl` 时**仍要留意：
  本技能从 2026-10 起才写 `unapplied` 字段，更早的档案里没有这个保证
- ⚠️ **别用文件 sha 判断"是不是同一张图"**：PNG 内嵌执行图，换 `filename_prefix` 就会变 sha 而画面不变。用 [`image-tools`](../image-tools/SKILL.md) 的 `pngdiff.py`
- ⚠️ **首次运行慢**：ComfyUI 首次加载 7.5G 文本编码器 + 11.5G 主模型，等待时间可能远超出图本身；`--timeout` 给足
- ⚠️ **输出文件名带 subfolder**：下载 `/view` 时要带 `subfolder` 与 `type`，否则 404；脚本已处理
- ⚠️ **比例用 `--width/--height`**：ComfyUI 的空 Latent 节点没有 `--ratio` 概念，横竖版靠宽高
- ⚠️ **改参数只改暴露的 8 个**：想改 cfg/sampler/scheduler 要改工作流 JSON 或扩展 `PARAM_SCHEMA`
- ⚠️ **服务器不可达时**：`--check` 给出 `URLError: timed out` = 本机到 192.168.3.5 的 TCP 18000 不通，**不是脚本问题**。注意「Windows 本机浏览器能打开」不能排除此故障——回环访问绕过防火墙。排查步骤见 [`references/server-192.168.3.5.md`](references/server-192.168.3.5.md)

## 验证

```bash
# 离线自检：转换 + 完整 API 往返（内置 mock ComfyUI，不需要真服务器）
python3 scripts/test_skill.py

# 带上真实服务器一起验证
python3 scripts/test_skill.py --server http://192.168.3.5:18000

# 真机参数矩阵：逐个参数出图并比对像素，确认改动真的到达采样器
# （先探活，服务器不可达会立刻退出，不会干等 --timeout）
python3 scripts/verify_params.py --timeout 900
python3 scripts/verify_params.py --quick        # 只跑 4 次出图

# 比两张图到底是不是同一张（判据是像素，不是文件 sha）
# 工具在兄弟技能 image-tools（ffmpeg + numpy），本技能不再自带副本
python3 ../image-tools/scripts/pngdiff.py a.png b.png
python3 ../image-tools/scripts/pngdiff.py a.png b.png --json  # 含 psnr/ssim/chunk/字节

# 一轮多图拼成一张带标签的速览图
python3 ../image-tools/scripts/contact_sheet.py --round out/r1/round.json \
    -o out/r1/sheet.png --cols 3

# 连上服务器后刷新离线节点 schema（可选，提升异形工作流的参数识别）
python3 scripts/dump_node_info.py --server http://192.168.3.5:18000 -o references/node-info.json
```

### 复现性要比像素，不要比文件 sha

ComfyUI 会把**执行过的图**写进 PNG 的 `tEXt` chunk。所以任何改动图的动作——
哪怕只是 `filename_prefix` 换了（每次批量跑都会换）——都会让文件 sha 变化，
而画面**逐像素完全相同**。本项目 R34/R35 的实测：

| 比较对象 | 结果 |
|---|---|
| 文件 sha256 | `1c2aaa2187d2…` vs `5e47b6b227ae…` **不同** |
| 解码像素（1200×1600） | **0 / 1,920,000 不同**，最大通道差 0 |

两者 API 图的唯一差异是 `bc-r34-ablation-window` vs `bc-r35-ablation-window`。
因此：**证明"可复现"用 `pngdiff.pixels_equal`；证明"参数生效了"也用像素差异率**（还可看 `psnr` / `ssim`）
（还能顺带看出影响有多大：`steps 3 vs 6` 差 99.53%、`seed 99 vs 11` 差 99.94%）。


### 已通过的联调记录（2026-10-02）

- 服务器：ComfyUI **0.38.0**，RTX 4060 Ti 8GB，`0.0.0.0:18000`
- 三个模型文件均在位；`RESULT: PASS`（conversion / mock roundtrip / live probe）
- 真实出图：`--prompt "a red fox in fresh snow, ..." --width 1024 --height 1024 --steps 8 --seed 42`
  → `status success`，落盘 `out/z-image-turbo_00016_.png`（1024×1024 PNG，1,149,683 字节）
- **参数矩阵 9/9 通过**（`verify_params.py`）：

  | 检查 | 结果 |
  |------|------|
  | 基线出图 | 768×768，10.1s |
  | `--prompt` | 换词 → 图不同 ✅ |
  | `--width/--height` | 输出实为 (768, 1152) ✅ |
  | `--seed`（换值） | seed 99 ≠ seed 11 ✅ |
  | `--seed`（复现） | 同 seed 两次**解码像素完全相同** ✅（判据是像素：PNG 的 `tEXt` 会让文件 sha 变化，见下文） |
  | `--steps` | steps 3 ≠ steps 6 ✅ |
  | `--filename-prefix` | 落地 `paramcheck_00001_.png` ✅ |
  | `--unet/clip/vae-name` | 三个名字确实进入 API 请求体 ✅ |
  | 非法 `--unet-name` | 服务器 `HTTP 400` 拒绝 → 参数真被校验 ✅ |

- 连不上时的排查过程与防火墙根因见 [`references/server-192.168.3.5.md`](references/server-192.168.3.5.md)

## 检查清单（Qwen 引擎）

- [ ] `comfyui_qwen.py --check` 通过（三个模型文件在位）
- [ ] `--negative` 已填（Qwen 支持真负向，别浪费）
- [ ] 单张耗时按 7–10 分钟预估，`--timeout` ≥1800
- [ ] 不要在主正向里写 `craquelure/cracks` —— Qwen 会放大成满脸裂纹，裂纹应放负向

## 检查清单

- [ ] 已跑 `--check`，服务器可达
- [ ] `--list` 确认参数与默认值，模型文件名与服务器一致（必要时先 `--list-models`）
- [ ] `--prompt` 已给出，尺寸/步数按用途设置
- [ ] 要复现时固定了 `--seed`
- [ ] `--timeout` 足够覆盖首次模型加载
- [ ] 产物已落盘（看 `local_paths`），不是只拿服务器侧文件名
