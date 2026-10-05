# gen-media 技能库总览（Skills Index）

> 返回[首页](../../README.md) ｜ 项目实践见 [../projects/](../../projects/README.md) ｜ 视频方法手册见 [../methods/](../../methods/README.md)

> ⚠️ **本文件是索引，不是技能。** `.agents/skills/` 是技能根，**任何带 frontmatter 的 md 都会被当作技能加载**，
> 所以本 README **刻意不写 frontmatter**，按普通文档写。真正的技能是各子目录里的 `SKILL.md`。

> 本目录是**技能库**：每个子目录一个技能，入口为 `SKILL.md`（YAML frontmatter 含 `name` / `description` / `whenToUse`）。
> 技能讲「**怎么做**」，具体项目（「**做什么**」）见 [projects/](../../projects/README.md)。
>
> 📌 **准入标准：只收录带脚本、有自检入口、能在真机跑通的技能。** 纯文档（教你怎么用外部 CLI、但仓库里没有可执行代码）不进这个库。
> 2026-10-05 按此标准移除了 9 个无脚本的方舟 Seedream 云端文档技能。
>
> 🗂️ **本目录由 image-gen/skills 与 video-gen/skills 合并而来**（2026-10-05 扁平化）：图像与视频技能不再分库，按能力放在一起。

---

## 一、快速选路

**按你手里的素材与跑在哪，直接选：**

| 你手里有 / 条件 | 加载技能 |
|------------------|----------|
| 只有文字描述，要**出图** | [text-to-image-comfyui](text-to-image-comfyui/SKILL.md) —— 两个引擎：Z-Image-Turbo（快）/ Qwen-Image（细、支持真负向） |
| 有一张控制图（线稿 / 照片 / 姿态图），要按结构出图 | [image-edit-comfyui](image-edit-comfyui/SKILL.md) —— Fun Union ControlNet，控制强度与生效区间可调 |
| 要合并多张图 / 比对两张图 / 去元数据 / 缩放裁切 | [image-tools](image-tools/SKILL.md) —— **不用 AI**，确定性、可复现 |
| 只有文字，要**带同步音频**的短视频 | [text-to-video-fastvideo3](text-to-video-fastvideo3/SKILL.md) —— FastH3 t2va（本地 ComfyUI） |
| 有一张静图，要它动起来（首帧/可选尾帧） | [image-to-video-fastvideo3](image-to-video-fastvideo3/SKILL.md) —— FastH3 fl2va（本地 ComfyUI） |
| 要云端托管、1080p / 长时长 / 多种输入 | [../methods/](../../methods/README.md)（方舟 Seedance，**不作为技能收录**，只有方法手册） |

**本地 ComfyUI 与云端 Ark 的取舍**：

| 维度 | 本地 ComfyUI（本技能库） | 云端 Ark Seedance（[methods/](../../methods/README.md)） |
|------|--------------------------|------------------------------------------------------|
| 成本 | 自有显卡电费，可无限重跑 | 按量计费 |
| 速度 | 视频实测约 3 分钟一条（576×736 / 56 帧） | 快 |
| 音频 | **原生同步生成**（t2va / fl2va，音视频一次出） | 需显式开 `generate_audio`，效果有坑 |
| 适合 | 反复试 prompt、要音画同出、不赶时间 | 出成品、要高清、要多种输入路径 |

---

## 二、技能地图

```
.agents/skills/
├── README.md                            ← 你在这里（技能索引）
│
├── 🖼️ 出图
│   ├── text-to-image-comfyui/           文生图：Z-Image-Turbo（12 步，~25s/张）+ Qwen-Image（细节、真负向）
│   └── image-edit-comfyui/              控制图生图：Z-Image Fun Union ControlNet（Canny 驱动）
│
├── 🎬 出片（本地 ComfyUI · 同一套 FastH3 权重，不能同时跑）
│   ├── text-to-video-fastvideo3/        文生视频 + 同步音频（t2va）
│   └── image-to-video-fastvideo3/       图生视频 + 同步音频（fl2va，首帧/可选尾帧）
│
└── 🧰 确定性工具（不调模型）
    └── image-tools/                     ffmpeg + numpy：拼版速览图、像素比对 + PSNR/SSIM、剥元数据、缩放裁切
```

### 技能表

| 技能 | 一句话 | 输入 → 输出 | 自检 |
|------|--------|-------------|------|
| [text-to-image-comfyui](text-to-image-comfyui/SKILL.md) | 远程 ComfyUI 跑 Z-Image-Turbo / Qwen-Image 文生图 | prompt（+ 负向）→ 图片文件 | `comfyui_gen.py --check` / `comfyui_qwen.py --check` |
| [image-edit-comfyui](image-edit-comfyui/SKILL.md) | 远程 ComfyUI 跑 Fun Union ControlNet 控制图生图 | 控制图 + prompt → 图片文件 | `comfyui_edit.py --check` |
| [text-to-video-fastvideo3](text-to-video-fastvideo3/SKILL.md) | 远程 ComfyUI 跑 FastH3 文生视频 | 结构化 prompt → mp4（带音频轨） | `comfyui_video.py --check` |
| [image-to-video-fastvideo3](image-to-video-fastvideo3/SKILL.md) | 远程 ComfyUI 跑 FastH3 图生视频（首帧/可选尾帧） | 1–2 张图 + prompt → mp4（带音频轨） | `comfyui_i2v.py --check` |
| [image-tools](image-tools/SKILL.md) | **不用 AI** 的确定性图片处理 | 多张图 → 速览图 / 比对报告 / 处理后的图 | `scripts/test_skill.py`（离线） |

> ⚠️ 两个视频技能**共用同一套 35 GB 权重，不能同时跑**；权重压 8 GB 显存会流式换页，慢是必然的。

### 组合用法

- **从文字到成品**：`text-to-image-comfyui` 逐轮出图 → `image-tools` 拼版速览 + 像素比对（与同轮底座对照）
- **按结构控制构图**：控制图 → `image-edit-comfyui`（调 `--control-strength` / `--canny-low,high`）→ `image-tools` 比对改动是否真的落到区域上
- **图 → 视频**：`text-to-image-comfyui` 出首帧 → `image-to-video-fastvideo3` 让它动起来
- **交付前规范化**：`image-tools` 的 `ffkit strip`（剥 tEXt 元数据，像素不变）+ `contact_sheet`（合图）+ `resize`（出缩略图）

---

## 三、运行前提与自检

```bash
# 服务器：远程 ComfyUI
http://192.168.3.5:18000            # ComfyUI 0.38.0，RTX 4060 Ti 8GB
```

| 技能 | 需要的模型 / 节点（服务器上） | 自检命令 | 上次结果 |
|------|------------------------------|----------|----------|
| text-to-image-comfyui（Z-Image） | `z_image_turbo_bf16` / `qwen_3_4b` / `ae` | `python3 scripts/comfyui_gen.py --check` | ✅ `reachable: true` |
| text-to-image-comfyui（Qwen） | `qwen_image_2512_fp8_e4m3fn` / `qwen_2.5_vl_7b_fp8_scaled` / `qwen_image_vae` | `python3 scripts/comfyui_qwen.py --check` | ✅ `missing: []` |
| image-edit-comfyui | 上面 Z-Image 三件 + `Z-Image-Turbo-Fun-Controlnet-Union.safetensors` | `python3 scripts/comfyui_edit.py --check` | ✅ `missing: []`，真机参数矩阵 **28/28** 通过 |
| text-to-video-fastvideo3 | 4 个模型文件 + **9 个节点类** | `python3 scripts/comfyui_video.py --check` | ✅ |
| image-to-video-fastvideo3 | 同上（共用权重） | `python3 scripts/comfyui_i2v.py --check` | ✅ |
| image-tools | `ffmpeg` / `ffprobe`、Python 3 + numpy（**不需要 Pillow**） | `python3 scripts/test_skill.py` | ✅ `RESULT: PASS` |

> 改完环境（换机器 / 换模型 / 升级 ComfyUI）先跑上面这一列，再谈出图出片。
> 视频节点的**节点类**比图像节点新：ComfyUI 版本偏旧时是节点缺失而不是模型缺失。
> `image-edit-comfyui` 另有真机全参数验证脚本 `scripts/verify_params.py`（对每个参数真实出图并用像素差证明改动落地）。

---

## 四、术语速查

| 术语 | 含义 |
|------|------|
| T2I | Text-to-Image，文生图 |
| I2I | Image-to-Image，图生图（本库用控制图驱动） |
| ControlNet / 控制图 | 用一张图约束结构（本库用 `Canny` 预处理 + `ZImageFunControlnet` 应用） |
| 引擎 | 文生图的两条实现：Z-Image-Turbo（快）/ Qwen-Image（细） |
| T2V / I2V | Text-to-Video / Image-to-Video |
| t2va / fl2va | FastH3 的两个工作流：文生视频+音频 / 首尾帧+音频 |
| `--seed` | 固定随机种子，用于复现（同 seed 同参数 → 像素一致） |
| 接触印相 / 速览图 | contact sheet，把一轮多张拼成一张带标签的大图 |
| 像素判据 | 判断「改动是否生效」看**解码后的像素**，不看文件哈希（ComfyUI 会把执行图写进 PNG 的 tEXt，哈希必变） |
| 落点 | 提示词里那个「件」实际应该长在什么位置/结构上 |

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-02 | v1.0 | image-gen 侧：`methods/` 改组为技能库 .agents/skills/，索引改技能地图与选路表 | 小七 |
| 2026-10-04 | v1.4 | image-gen 侧：参数静默失效治理 + 复现判据统一；新增 image-tools | 小七 |
| 2026-10-05 | v1.5 | image-gen 侧：收敛为只留可执行技能（移除 9 个纯文档技能） | 小七 |
| **2026-10-05** | **v2.0** | **扁平化合并**：`image-gen/.agents/skills/README.md` 与 `video-gen/.agents/skills/README.md` 合并为本文件；目录从 `image-gen/skills`、`video-gen/skills` 迁至仓库根 `.agents/skills/`；技能地图与选路表改为图像/视频统一索引（5 个技能） | 小七 |
