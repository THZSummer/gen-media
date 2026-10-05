---
name: image-skills-index
description: 本机 ComfyUI 图片生成技能索引：3 个可执行技能（文生图 / 控制图生图 / 确定性图像工具）的能力地图、按输入素材的选路表、运行前提与自检命令。触发词：图片生成怎么开始、用哪个技能、图片能力地图、文生图/图生图/速览图怎么选。
whenToUse: 当不确定该用哪个图片技能、需要总览能力地图、或要确认环境是否健康时使用。确定任务后加载对应技能目录的 SKILL.md（如 text-to-image-comfyui/SKILL.md）。
---

# 图片生成技能总览（Skills Index）

> 返回[首页](../README.md) ｜ 项目实践见 [../projects/](../projects/README.md) ｜ 配套视频技能见 [../../video-gen/](../../video-gen/README.md)

> 本目录是**技能库**：每个子目录一个技能，入口为 `SKILL.md`（YAML frontmatter 含 `name` / `description` / `whenToUse`）。
> 技能讲"**怎么做**"，具体项目（"**做什么**"）见 [projects/](../projects/README.md)。
>
> 📌 **准入标准：只收录带脚本、有自检入口、能在真机跑通的技能。** 纯文档（教你怎么用外部 CLI、但仓库里没有可执行代码）不进这个库 —— 2026-10-05 按此标准移除了 9 个方舟 Seedream 云端文档技能。

---

## 一、快速选路

**你手里有什么，就加载哪个技能：**

| 你手里有 | 加载技能 |
|----------|----------|
| 只有文字描述 | [text-to-image-comfyui](text-to-image-comfyui/SKILL.md) —— 两个引擎：Z-Image-Turbo（快）/ Qwen-Image（细、支持真负向） |
| 有一张控制图（线稿 / 照片 / 姿态图），要按结构出图 | [image-edit-comfyui](image-edit-comfyui/SKILL.md) —— Fun Union ControlNet，控制强度与生效区间可调 |
| 要合并多张图 / 比对两张图 / 去元数据 / 缩放裁切 | [image-tools](image-tools/SKILL.md) —— **不用 AI**，确定性、可复现 |

---

## 二、技能地图

```
skills/
├── README.md                     ← 你在这里（技能索引）
│
├── 🖼️ 生成
│   ├── text-to-image-comfyui/    文生图：Z-Image-Turbo（12 步，~25s/张）+ Qwen-Image（细节、真负向）
│   └── image-edit-comfyui/       控制图生图：Z-Image Fun Union ControlNet（Canny 控制图驱动）
│
└── 🧰 确定性工具（不调模型）
    └── image-tools/              ffmpeg + numpy：拼版速览图、像素比对 + PSNR/SSIM、剥元数据、缩放裁切
```

### 技能表

| 技能 | 一句话 | 输入 → 输出 | 自检 |
|------|--------|-------------|------|
| [text-to-image-comfyui](text-to-image-comfyui/SKILL.md) | 远程 ComfyUI 跑 Z-Image-Turbo / Qwen-Image 文生图 | prompt（+ 负向）→ 图片文件 | `comfyui_gen.py --check` / `comfyui_qwen.py --check` |
| [image-edit-comfyui](image-edit-comfyui/SKILL.md) | 远程 ComfyUI 跑 Fun Union ControlNet 控制图生图 | 控制图 + prompt → 图片文件 | `comfyui_edit.py --check` |
| [image-tools](image-tools/SKILL.md) | **不用 AI** 的确定性图片处理 | 多张图 → 速览图 / 比对报告 / 处理后的图 | `scripts/test_skill.py`（离线） |

### 组合用法

- **从文字到成品**：`text-to-image-comfyui` 逐轮出图 → `image-tools` 拼版速览 + 像素比对（与同轮底座对照）
- **按结构控制构图**：控制图 → `image-edit-comfyui`（调 `--control-strength` / `--canny-low,high`）→ `image-tools` 比对改动是否真的落到区域上
- **交付前规范化**：`image-tools` 的 `ffkit strip`（剥 tEXt 元数据，像素不变）+ `contact_sheet`（合图）+ `resize`（出缩略图）

---

## 三、运行前提与自检（2026-10-05 实测）

```bash
# 服务器：远程 ComfyUI
http://192.168.3.5:18000            # ComfyUI 0.38.0，RTX 4060 Ti 8GB
```

| 技能 | 需要的模型文件（服务器上） | 自检命令 | 上次结果 |
|------|---------------------------|----------|----------|
| text-to-image-comfyui（Z-Image） | `z_image_turbo_bf16` / `qwen_3_4b` / `ae` | `python3 scripts/comfyui_gen.py --check` | ✅ `reachable: true` |
| text-to-image-comfyui（Qwen） | `qwen_image_2512_fp8_e4m3fn` / `qwen_2.5_vl_7b_fp8_scaled` / `qwen_image_vae` | `python3 scripts/comfyui_qwen.py --check` | ✅ `missing: []` |
| image-edit-comfyui | 上面 Z-Image 三件 + `Z-Image-Turbo-Fun-Controlnet-Union.safetensors` | `python3 scripts/comfyui_edit.py --check` | ✅ `missing: []`，且真机参数矩阵 **28/28** 通过 |
| image-tools | `ffmpeg` / `ffprobe`、Python 3 + numpy（**不需要 Pillow**） | `python3 scripts/test_skill.py` | ✅ `RESULT: PASS` |

> 改完环境（换机器 / 换模型 / 升级 ComfyUI）先跑上面这一列，再谈出图。
> `image-edit-comfyui` 另有真机全参数验证脚本 `scripts/verify_params.py`（对每个参数真实出图并用像素差证明改动落地）。

---

## 四、术语速查

| 术语 | 含义 |
|------|------|
| T2I | Text-to-Image，文生图 |
| I2I | Image-to-Image，图生图（本库用控制图驱动） |
| ControlNet / 控制图 | 用一张图约束结构（本库用 `Canny` 预处理 + `ZImageFunControlnet` 应用） |
| 引擎 | 文生图的两条实现：Z-Image-Turbo（快）/ Qwen-Image（细） |
| `--seed` | 固定随机种子，用于复现（同 seed 同参数 → 像素一致） |
| 接触印相 / 速览图 | contact sheet，把一轮多张拼成一张带标签的大图 |
| 像素判据 | 判断"改动是否生效"看**解码后的像素**，不看文件哈希（ComfyUI 会把执行图写进 PNG 的 tEXt，哈希必变） |
| 落点 | 提示词里那个"件"实际应该长在什么位置/结构上 |

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-02 | v1.0 | methods/ 改组为技能库 skills/：每个技能以 SKILL.md（frontmatter + 指令体）呈现，索引改技能地图与选路表 | 小七 |
| 2026-10-02 | v1.1 | 新增 text-to-image-comfyui（远程 ComfyUI / Z-Image-Turbo，192.168.3.5:18000），文生图形成 ComfyUI 与 Seedream 两条路径 | 小七 |
| 2026-10-02 | v1.2 | 新增 image-edit-comfyui（Z-Image-Turbo Fun Union ControlNet 控制图生图，全参数 24/24 真机验证）；共享转换器新增 workflow profile、mute/bypass 处理、连线型子图接口回接、SaveImage 过滤与 UI 字段剔除 | 小七 |
| 2026-10-04 | v1.3 | **参数静默失效治理 + 复现判据统一**：转换器与两个引擎新增 unapplied 检测（`UnappliedOverrideError`，默认 strict，`--allow-unapplied` 可放行）；`pngdiff.py` 收进技能（判据统一为解码像素，附 R34/R35 实测：同像素不同 sha）；`verify_params.py` 改为像素判据 + 服务器探活快速失败 | 小七 |
| 2026-10-04 | v1.4 | **新增 image-tools（不用 AI 的确定性图片处理）**：ffmpeg + numpy 实现拼版速览图、像素比对与 PSNR/SSIM、PNG 元数据剥离、缩放裁切；依赖方向改为「生成技能依赖本技能」 | 小七 |
| 2026-10-05 | **v1.5** | **收敛为只留可执行技能**：移除 9 个无脚本、无自检入口的纯文档技能（方舟 Seedream 云端用法：text-to-image / image-editing / image-workflow / multi-image-reference / multi-view-consistency / prompt-engineering / parameters-and-output / quality-and-cost / content-safety）；索引、选路表、技能地图重写为 3 个本地技能，新增「运行前提与自检」表；6 处旧绝对路径改为仓库相对路径 | 小七 |
