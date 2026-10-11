---
name: seedance-reference-to-video
description: 通过本机 ComfyUI（默认 192.168.3.5:18000）的 ByteDance Seedance 2.5 **付费 partner 节点**做**参考生视频（r2v）**：上传参考图 → 接进 ByteDance2ReferenceNodeV2 的 model.reference_images.image_N → 校验 resolution/ratio/duration/task_type → 带 ComfyUI 账号凭据提交 → 轮询 /history → 拉回 mp4 并留档；5 个云端模型（2.5/2.5 Draft/2.0/2.0 Fast/2.0 Mini）、最多 30 张参考图、4–30 s、7 种画幅。**云端按次计费、本机零权重**。⚠️ 本技能**只建未验**（无离线自检、未真机出片）。触发词：Seedance、Seedance 2.5、seedance2.5、参考生视频、r2v、reference to video、ByteDance2ReferenceNodeV2、ComfyUI 付费节点、partner 节点、18000、192.168.3.5。
whenToUse: 当要用**一张或多张参考图 + 提示词**生成带同步音频的云端正片（1080p、可到 30 s、要真实人物/商品一致性）时使用。要"本机免费、可无限重跑"的图生视频用 image-to-video-fastvideo3（FastH3 fl2va）；要纯文生视频用 text-to-video-fastvideo3；要图片编辑用 seedream-image-edit；要先看清服务器有什么、某工作流缺不缺东西，用 comfyui-server。
---

# ComfyUI 参考生视频（Seedance 2.5 · 云端付费 partner 节点）

> ## ⚠️ 未验证声明（重要）
>
> 本技能按"**只建不验**"交付：**没有离线自检、没有真机出片记录、没有跑过 `--check`**。
> 它由一份导出的 UI 工作流 + 一份**本地缓存的**节点 schema 快照静态构造而成，
> 参数名与枚举值都来自那份快照（来源与抓取时间见 [references/node-info.json](references/node-info.json) 的 `_source`）。
>
> **已知漂移风险**：快照里是 **970** 个节点类；同一台服务器在 2026-10-11 实测报 **980** 个。
> 也就是说这份快照**可能已经过时**。
>
> **首次真机使用前，请按这个顺序做**（每一步都不该跳）：
> 1. `python3 scripts/seedance_r2v.py --check` → 看 `schema_drift` 是不是 `none`、`nodes` 全在不在、有没有凭据；
> 2. `--list` 对一眼枚举值（`resolution` / `ratio` / `duration` 上下限）；
> 3. `--plan` 确认参数真的落图、参考图接线对不对（**不花钱**）；
> 4. 用**最短时长**（`--duration 4`）真跑一条，确认能出片、能下载、留档正常；
> 5. 把上面四步的结果补进本文件的"验证记录"，再把这个技能的 `test_skill.py` 与 `check.sh` 两项补上
>    —— 在那之前它**不算**符合技能库准入标准（见 [../dev-guide/references/skills.md](../dev-guide/references/skills.md)）。

**用途**：给**一张或多张参考图** + 一段提示词，出**带同步音频的云端视频**。全程 HTTP API，
可脚本化、可留档；模型跑在字节云端，**本机不需要任何权重**，代价是**按次计费**。

- 默认服务器：`http://192.168.3.5:18000`（`--server` 或 `$COMFYUI_SERVER` 覆盖）
- 工作流：`assets/seedance-2.5-reference-r2v-ui.json`（节点 `ByteDance2ReferenceNodeV2`）
- schema 快照：`references/node-info.json`（3 个类：`ByteDance2ReferenceNodeV2` / `SaveVideo` / `LoadImage`）
- 共享引擎：复用兄弟技能 [seedream-text-to-image](../seedream-text-to-image/SKILL.md) 的
  `seedream_api.py`（UI→API 转换 / schema / 参数落图）与 `seedream_gen.py`（**凭据通道** / 排队 / 轮询 / 下载 / 留档）

## 与其它技能的边界

| 想要什么 | 用哪个 |
|---|---|
| **云端**出片、要 1080p / 长时长 / 真实主体一致性，愿意按次付费 | **本技能** |
| 本机免费出片、可无限重跑、音视频同出 | [image-to-video-fastvideo3](../image-to-video-fastvideo3/SKILL.md) / [text-to-video-fastvideo3](../text-to-video-fastvideo3/SKILL.md) |
| 只要图片（出图 / 改图） | [text-to-image-comfyui](../text-to-image-comfyui/SKILL.md) / [seedream-image-edit](../seedream-image-edit/SKILL.md) |
| 先看服务器有什么、某工作流缺什么 | [comfyui-server](../comfyui-server/SKILL.md) |

## 前置检查

```sh
cd .agents/skills/seedance-reference-to-video

# ① 离线：看模型、每个模型的参数与枚举、参考图上限、schema 快照的来源
python3 scripts/seedance_r2v.py --list

# ② 工作流自带的那条 r2v 提示词样本（只当格式参考，不会当默认值用）
python3 scripts/seedance_r2v.py --show-default-prompt

# ③ 真机：节点在不在 + schema 对账 + 凭据通道（不提交任务、不花钱）
python3 scripts/seedance_r2v.py --check
```

## 成本：**按次计费**，先 `--plan` 再真跑

- 这是 `partner/video/ByteDance` 付费节点：**模型在云端、按次计费、本机零权重**。
- ⚠️ **本技能不含价格表**：单价以 ComfyUI 账号（platform.comfy.org）的 credits 口径为准，
  我**没有核实过**。别照抄任何数字。
- 建议：`--plan`（免费）→ `--duration 4`（该模型下限）跑一条 → 确认链路与画质后再上长时长/高分辨率。
- 分辨率与时长都直接影响成本与等待：`480p` 最省，`1080p` 最贵；`duration` 越大越贵。

## 参数

| 参数 | 落点 | 工作流默认 | 说明 |
|------|------|-----------|------|
| `--prompt` / `--prompt-file` | `model.prompt` | （样本，不用） | **必填**，一次出片很贵，刻意不给默认 |
| `--model` | `model` | `Seedance 2.5` | 5 个键见 `--list` |
| `--resolution` | `model.resolution` | `480p` | `480p` / `720p` / `1080p`（Seedance 2.0 另有 `4k`） |
| `--ratio` | `model.ratio` | `9:16` | `16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `21:9` / `adaptive` |
| `--duration` | `model.duration` | `5` | 整数秒；Seedance 2.5：**4–30**，2.0：4–15 |
| `--audio` / `--no-audio` | `model.generate_audio` | `true` | 是否生成同步音频 |
| `--task-type` | `model.task_type` | `reference` | `auto` / `reference` / `edit` / `extend`（**仅 Seedance 2.5 有**） |
| `--output-format` | `model.output_format` | `mp4` | 模板只列了 mp4 |
| `--auto-downscale` / `--no-auto-downscale` | `model.auto_downscale` | `true` | 云端自动降采样 |
| `--auto-upscale` / `--no-auto-upscale` | `model.auto_upscale` | `false` | 云端自动放大 |
| `--seed` | `seed` | `0` | 云端结果本身**非确定性**（schema 里写明），seed 只控制节点要不要重跑 |
| `--watermark` / `--no-watermark` | `watermark` | `false` | 是否加水印 |
| `--reference`（可重复） | 上传后接 `model.reference_images.image_N` | — | 本地图路径，脚本负责上传 |
| `--reference-name`（可重复） | 同上 | — | 服务器 `input/` 里已有的图，免上传 |
| `--filename-prefix` | `SaveVideo.filename_prefix` | `video/Seedance2.5_r2v` | 成品落在服务器 `output/video/` |
| `--video-format` | `SaveVideo.format` | `auto` | `auto` / `mp4` / `mkv` / `webm` |
| `--set CLASS.FIELD=VALUE` | 任意节点字段 | — | 兜底逃生口（可重复） |
| `--plan` | — | — | **不提交、不上传、不花钱**，只验证参数落图与参考图接线 |
| `--out-dir` / `--timeout` / `--poll` / `--quiet` / `--no-record` | — | `out` / 3600 / 5 / — / 留档开 | 产物与留档 |

> **参考图上限**（schema 快照）：Seedance 2.5 / 2.5 Draft = **30 张图 / 10 视频 / 10 音频 / 30 素材**；
> Seedance 2.0 系列 = **9 / 3 / 3 / 9**。⚠️ **本技能 v1 只支持参考图**（工作流里只有 `LoadImage` 一个源节点），
> 传 `--task-type edit`/`extend` 会给一条 warning —— 那两档通常要参考视频。

## 执行

```sh
# ① 先免费验证：参数真的落图、参考图接到 image_1、节点连线完整
python3 scripts/seedance_r2v.py \
    --reference ref.png --prompt-file prompt.txt \
    --resolution 1080p --ratio 9:16 --duration 5 --plan

# ② 真出片（**按次计费**；首次建议 --duration 4 最短档）
python3 scripts/seedance_r2v.py \
    --reference ref.png --prompt-file prompt.txt \
    --resolution 1080p --ratio 9:16 --duration 5 \
    --out-dir out/ --timeout 3600

# ③ 多张参考图（顺序就是 image_1 / image_2 …，在 prompt 里用 <Picture 1> 指代）
python3 scripts/seedance_r2v.py \
    --reference front.png --reference side.png --prompt-file prompt.txt --plan

# ④ 服务器 input 里已有的图，免上传
python3 scripts/seedance_r2v.py --reference-name uploaded.png --prompt-file prompt.txt --plan

# ⑤ 换模型 / 换档
python3 scripts/seedance_r2v.py --reference ref.png --prompt-file prompt.txt \
    --model "Seedance 2.5 Draft" --resolution 480p --duration 4 --plan
```

## prompt 写法（r2v）

参考生视频的提示词与图生视频**同一个三节结构**，开头多一句把输入图引进来：

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
integrated_multimodal_description: [Shot 1] ... [Shot 2] At 01.900, ... [Shot 3] At 03.900, ...
overall_soundscape: ...
non_diegetic_music: ...
```

- `<Picture 1>` / `<Picture 2>` 按 `--reference` 的**顺序**对应 `image_1` / `image_2`。
- 三节的职责、逐镜头写法、切点惯例见
  [image-to-video-fastvideo3/references/prompt-format.md](../image-to-video-fastvideo3/references/prompt-format.md)（同一套 H3 系写法）。
- 本技能的工作流里**自带一条 13929 字符的样本提示词**（雨林花神的芭蕾，7 镜 15 s），
  用 `--show-default-prompt` 看 —— 它是格式样本，不是默认值。

## 输出与留档

| 文件 | 内容 |
|------|------|
| `<服务端生成名>.mp4` | 成品视频（含音频轨，`--audio` 开着时） |
| `<prefix 基名>.api.json` | 实际提交的完整 API 图（含参考图名、全部参数、提示词全文） |
| `requests.jsonl` | 每行一次请求：时间 / `prompt_id` / 参数 / `elapsed_s` / 产物路径 / 凭据通道 / **提示词 sha256 + 字符数**（全文在 `.api.json` 里，免得长文撑爆 jsonl） |

**退出码**（沿用兄弟技能）：`0` 正常 / `1` 没有产物 / `2` 服务器不可达 / `3` 缺节点 /
`4` 凭据被拒 / `5` 被 `/prompt` 拒绝 / `6` 节点执行失败 / `7` 超时 / `8` 参数问题。

## 踩坑点

1. **凭据不是"登录了就行"**：无头调用付费节点要在 `/prompt` 的 `extra_data.api_key_comfy_org`
   里带 ComfyUI 账号 API Key（`--api-key` / `--api-key-file` / `$COMFYUI_API_KEY`）。
   在桌面端用邮箱/浏览器登录**不足以**让无头请求通过（实测报 `Unauthorized`）。
2. **`model` 是动态下拉框（`COMFY_DYNAMICCOMBO_V3`）**：`prompt` / `resolution` / `ratio` / …
   都是**挂在模型下面的子输入**，API 图里的名字带点（`model.resolution`）。
   文档上"节点只有一个 model 输入"是真的，但参数一个都不能少。
3. **参考图是采集式输入（`COMFY_AUTOGROW_V3`）**：API 名是 `model.reference_images.image_1`…`image_30`。
   脚本会复用工作流里那个 `LoadImage` 改写它、不够就补节点、多余就删掉
   （删很重要：留着没接线的 `LoadImage` 会让服务器去加载一个不存在的图片名）。
4. **`seed` 不保证复现**：schema 的 tooltip 写明"results are non-deterministic regardless of seed"。
   要复现只能固定**其它**参数并接受±。
5. **`task_type` 四档只有 2.5 有**：`reference`（参考生视频，本技能默认）、`edit`（视频编辑）、
   `extend`（视频延长）、`auto`（让云端判断）。后两档通常要**参考视频**，本工作流没接。
6. **画幅参数与输入图无关**：与本地 i2v 不同，这里是**显式 `--ratio`**；
   但 `adaptive` 会跟随参考图比例（官方模板的默认就是 `adaptive`）。
7. **schema 快照会漂移**：`--check` 的 `schema_drift` 就是干这个的。它是**本地快照 vs 真机**逐项对账；
   报出漂移不代表坏了，代表"参数名/枚举可能变了，先看差异再跑"。

## 验证记录（**待补**）

| 项 | 状态 |
|----|------|
| 语法编译（`py_compile`） | ✅ 通过（仅语法，不代表行为正确） |
| 离线自检 `scripts/test_skill.py` | ❌ **没写**（按要求"只建不验"） |
| 真机 `--check` | ❌ 未跑 |
| 真机 `--plan` | ❌ 未跑 |
| 真机出片 | ❌ 未跑 |
| 进入 `check.sh` | ❌ 未纳入（未验证的技能不该进交付门） |

## 检查清单

- [ ] `--check` 报了 `schema_drift: none`、`nodes` 全在、`credential.present: true`
- [ ] `--list` 里的 `resolution` / `ratio` / `duration` 范围与你要用的一致
- [ ] `--plan` 通过：参考图真的接到 `model.reference_images.image_N`、参数在 `applied` 里
- [ ] prompt 三节齐全，`<Picture N>` 与 `--reference` 顺序对得上
- [ ] 首次真跑用最短时长；确认能下载、`requests.jsonl` 留档正常
- [ ] 产物与 `.api.json` 已落盘；大体积中间产物（`work/`、`out/`）未入库
- [ ] 真机验证后回来更新上面的"验证记录"，并补 `test_skill.py` 与 `check.sh` 两项

## 修订记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-10-11 | v0.1 | **建立（只建不验）**：以一份导出的 UI 工作流（`ByteDance2ReferenceNodeV2`，3 节点：`LoadImage` → Seedance → `SaveVideo`）为资产，配一份**本地缓存的** schema 快照（含 5 个模型键、动态下拉框子输入、autogrow 参考上限），脚本 `seedance_r2v.py` 提供 `--list / --check / --show-default-prompt / --plan / 生成`；复用兄弟技能的凭据通道与 UI→API 转换器，不复制引擎。未写离线自检、未跑真机、未进 `check.sh` —— 理由与"首次真机前必做的 5 步"写在顶部声明里 |
