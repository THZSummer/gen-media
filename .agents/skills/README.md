# gen-media 技能库总览（Skills Index）

> 返回[首页](../../README.md) ｜ 项目实践见 [../projects/](../../projects/README.md) ｜ 视频方法手册见 [../methods/](../../methods/README.md)

> ⚠️ **本文件是索引，不是技能。** `.agents/skills/` 是技能根，**任何带 frontmatter 的 md 都会被当作技能加载**，
> 所以本 README **刻意不写 frontmatter**，按普通文档写。真正的技能是各子目录里的 `SKILL.md`。

> 本目录是**技能库**：每个子目录一个技能，入口为 `SKILL.md`（YAML frontmatter 含 `name` / `description` / `whenToUse`）。
> 技能讲「**怎么做**」，具体项目（「**做什么**」）见 [projects/](../../projects/README.md)。
>
> 📌 **准入标准：只收录带脚本、有自检入口、能在真机跑通的技能。** 纯文档（教你怎么用外部 CLI、但仓库里没有可执行代码）不进这个库。
> 2026-10-05 按此标准移除了 9 个无脚本的方舟 Seedream 云端文档技能。
> 2026-10-06 **按同一标准重新收录** Seedream 云端出图：`seedream-text-to-image`——
> 这次带脚本（转换 / 提交 / 轮询 / 下载 / 留档）、带自检（离线 `test_skill.py` + 真机 `--check` + 付费矩阵 `verify_params.py`）。
>
> ⚠️ **2026-10-11 的例外（已知并留在明面上）**：`seedance-reference-to-video` 按用户明确要求
> **"只建不验"** 交付 —— 有脚本、有 `--check/--list/--plan` 入口，但**没跑过任何验证**，
> 因此**尚未满足准入标准**，也**没有进 `check.sh`**。它自己的 SKILL.md 顶部写明了
> "首次真机使用前必做的 5 步"与待补的验证记录。
>
> 🗂️ **本目录由 image-gen/skills 与 video-gen/skills 合并而来**（2026-10-05 扁平化）：图像与视频技能不再分库，按能力放在一起。

---

## 一、快速选路

**按你手里的素材与跑在哪，直接选：**

| 你手里有 / 条件 | 加载技能 |
|------------------|----------|
| 只有文字描述，要**出图** | [text-to-image-comfyui](text-to-image-comfyui/SKILL.md) —— 两个引擎：Z-Image-Turbo（快）/ Qwen-Image（细、支持真负向） |
| 只有文字，要**云端付费模型**出图（本机零权重） | [seedream-text-to-image](seedream-text-to-image/SKILL.md) —— 本机 ComfyUI 编排 + ByteDance Seedream 5.0 云端推理（pro / flash / lite / 4.5 / 4.0），按张计费、要 ComfyUI 账号 API Key |
| **已有图片**要按提示词改（换背景 / 换主体 / 局部标注 / 多图参考） | [seedream-image-edit](seedream-image-edit/SKILL.md) —— 同一个 Seedream 付费节点，参考图接 `model.images.image_N`；也可用本机 ControlNet 那条路 |
| 有**参考图**，要**云端**出片（1080p / 长时长 / 主体一致性，按次计费） | [seedance-reference-to-video](seedance-reference-to-video/SKILL.md) —— Seedance 2.5 付费 partner 节点做 r2v；⚠️ **只建未验**（见该技能顶部声明） |
| 有一张控制图（线稿 / 照片 / 姿态图），要按结构出图 | [image-edit-comfyui](image-edit-comfyui/SKILL.md) —— Fun Union ControlNet，控制强度与生效区间可调 |
| 有**一张图**，要同一主体的**多个机位/角度**（本机免费、可重复跑） | [comfyui-multi-angle](comfyui-multi-angle/SKILL.md) —— Qwen-Image-Edit 2511 + Multiple-Angles LoRA，**一次 8 个角度，实测 8 张约 4 分 46 秒**；可 `--only` 只出几个 |
| 要合并多张图 / 比对两张图 / 去元数据 / 缩放裁切 | [image-tools](image-tools/SKILL.md) —— **不用 AI**，确定性、可复现 |
| 只有文字，要**带同步音频**的短视频 | [text-to-video-fastvideo3](text-to-video-fastvideo3/SKILL.md) —— FastH3 t2va（本地 ComfyUI） |
| 有一张静图，要它动起来（首帧/可选尾帧） | [image-to-video-fastvideo3](image-to-video-fastvideo3/SKILL.md) —— FastH3 fl2va（本地 ComfyUI） |
| 要一段**音乐 / BGM**（纯音乐、可脚本化、无 API 计费） | [comfyui-music-minimax3](comfyui-music-minimax3/SKILL.md) —— MiniMax Music 3（开放权重），caption + lyrics → mp3；**很慢：≈16.7 s 墙钟 / 1 s 音频** |
| 要**先看清楚服务器有什么**（权重 / 节点 / 模板 / 历史 / 队列），或某个工作流**在本机能不能跑** | [comfyui-server](comfyui-server/SKILL.md) —— 一步生成都不做：只读探查 + `audit` 缺件点名 + 队列/显存运维（写操作要 `--yes`） |
| 要云端托管、1080p / 长时长 / 多种输入 | [../methods/](../../methods/README.md)（方舟 Seedance，**不作为技能收录**，只有方法手册） |

**本地 ComfyUI 与云端 Ark 的取舍**：

| 维度 | 本地 ComfyUI（本技能库） | 云端 Ark Seedance（[methods/](../../methods/README.md)） |
|------|--------------------------|------------------------------------------------------|
| 成本 | 自有显卡电费，可无限重跑 | 按量计费 |
| 速度 | 视频实测约 3 分钟一条（576×736 / 56 帧） | 快 |
| 音频 | **原生同步生成**（t2va / fl2va，音视频一次出） | 需显式开 `generate_audio`，效果有坑 |
| 适合 | 反复试 prompt、要音画同出、不赶时间 | 出成品、要高清、要多种输入路径 |

> 🔀 **还有第三条路：模型在云端、编排在本机 ComfyUI**。`seedream-text-to-image` 用 ComfyUI 的
> **partner（付费）节点**调 ByteDance Seedream：本机不装权重、不占显存，但**按张计费**，
> 且无头调用必须带 ComfyUI 账号 API Key（桌面端界面点 Run 的登录态不够用）。
> 三条路的取舍：本机权重（免费、可无限重跑、吃显存）／ComfyUI 付费节点（按张计费、省显存）／
> 方舟 ARK 直连（按量计费、不经过 ComfyUI）。

---

## 二、技能地图

```
.agents/skills/
├── README.md                            ← 你在这里（技能索引）
│
├── 🖼️ 出图
│   ├── text-to-image-comfyui/           文生图：Z-Image-Turbo（12 步，~25s/张）+ Qwen-Image（细节、真负向）
│   ├── seedream-text-to-image/        文生图：ByteDance Seedream 5.0 —— **模型在云端**，ComfyUI 付费节点，按张计费
│   ├── seedream-image-edit/             图片编辑：同一个 Seedream 云端节点，底图（+ 标注）接 model.images.image_N
│   ├── image-edit-comfyui/              控制图生图：Z-Image Fun Union ControlNet（Canny 驱动）
│   └── comfyui-multi-angle/             一张图 → 8 个角度（Qwen-Image-Edit 2511 + Multiple-Angles LoRA；实测 8 张 ≈ 4 分 46 秒）
│
├── 🎬 出片
│   ├── text-to-video-fastvideo3/        文生视频 + 同步音频（t2va）· **本地** ComfyUI
│   ├── image-to-video-fastvideo3/       图生视频 + 同步音频（fl2va，首帧/可选尾帧）· **本地** ComfyUI
│   └── seedance-reference-to-video/     参考生视频：Seedance 2.5 **云端付费** partner 节点（r2v，最多 30 张参考图）⚠️ **未验证**
│
│   > 前两个共用同一套 FastH3 权重，**不能同时跑**；第三个本机零权重、按次计费。
│
├── 🎵 出音频（本地 ComfyUI · 与上面两套不共用权重）
│   └── comfyui-music-minimax3/        文生音乐：MiniMax Music 3（caption + lyrics → mp3；≈16.7 s 墙钟/音频秒）
│
├── 🔎 服务器探查与运维（不做生成 —— 只回答"现在有什么、能不能跑、谁在占"）
│   └── comfyui-server/                 权重/节点/模板目录、audit 缺件点名、历史产物、队列与显存（写操作要 --yes）
│
└── 🧰 确定性工具（不调模型）
    └── image-tools/                     ffmpeg + numpy：拼版速览图、像素比对 + PSNR/SSIM、剥元数据、缩放裁切
```

### 技能表

| 技能 | 一句话 | 输入 → 输出 | 自检 |
|------|--------|-------------|------|
| [text-to-image-comfyui](text-to-image-comfyui/SKILL.md) | 远程 ComfyUI 跑 Z-Image-Turbo / Qwen-Image 文生图 | prompt（+ 负向）→ 图片文件 | `comfyui_gen.py --check` / `comfyui_qwen.py --check` |
| [seedream-text-to-image](seedream-text-to-image/SKILL.md) | ComfyUI 付费节点跑 **ByteDance Seedream 5.0**（云端模型） | prompt → 图片文件 | `seedream_gen.py --check` / `test_skill.py` |
| [seedream-image-edit](seedream-image-edit/SKILL.md) | 同一个 Seedream 云端节点做**图片编辑** | 底图（+ 标注层，可多张参考图）+ 指令 → 图片文件 | `seedream_edit.py --check` / `test_skill.py`（复用它那一份引擎） |
| [seedance-reference-to-video](seedance-reference-to-video/SKILL.md) ⚠️ | ComfyUI 付费节点跑 **Seedance 2.5** 参考生视频（r2v） | 参考图（1–30 张）+ 提示词 → mp4（带同步音频） | `seedance_r2v.py --list`（离线）/ `--check`（真机）—— ⚠️ **均未跑过** |
| [image-edit-comfyui](image-edit-comfyui/SKILL.md) | 远程 ComfyUI 跑 Fun Union ControlNet 控制图生图 | 控制图 + prompt → 图片文件 | `comfyui_edit.py --check` |
| [comfyui-multi-angle](comfyui-multi-angle/SKILL.md) | 远程 ComfyUI 跑 **Qwen-Image-Edit 2511 + Multiple-Angles LoRA**：一张图出多机位 | 1 张参考图 → 8 张不同角度（可 `--only` 子集） | `test_skill.py`（离线 65 项）/ `comfyui_angles.py --check` |
| [text-to-video-fastvideo3](text-to-video-fastvideo3/SKILL.md) | 远程 ComfyUI 跑 FastH3 文生视频 | 结构化 prompt → mp4（带音频轨） | `comfyui_video.py --check` |
| [image-to-video-fastvideo3](image-to-video-fastvideo3/SKILL.md) | 远程 ComfyUI 跑 FastH3 图生视频（首帧/可选尾帧） | 1–2 张图 + prompt → mp4（带音频轨） | `comfyui_i2v.py --check` |
| [comfyui-music-minimax3](comfyui-music-minimax3/SKILL.md) | 远程 ComfyUI 跑 **MiniMax Music 3** 文生音乐 | caption（+ lyrics）→ mp3（纯音乐/BGM 或整首歌） | `test_skill.py`（离线 43 项）/ `comfyui_music.py --check` |
| [comfyui-server](comfyui-server/SKILL.md) | 查**服务器本身**：权重 / 节点 / 模板 / 历史 / 队列 + `audit` 判能不能跑 | 动词（status / models / nodes / templates / audit / history / queue …）→ JSON | `test_skill.py`（离线 64 项）/ `comfyui_server.py --check` |
| [image-tools](image-tools/SKILL.md) | **不用 AI** 的确定性图片处理 | 多张图 → 速览图 / 比对报告 / 处理后的图 | `scripts/test_skill.py`（离线） |

> ⚠️ 两个视频技能**共用同一套 35 GB 权重，不能同时跑**；权重压 8 GB 显存会流式换页，慢是必然的。

### 组合用法

- **动手前的第一步**：`comfyui-server status` 看版本/显存、`queue` 看谁在跑、`models --search X` 确认权重在位；想拿官方模板当起点就 `templates --pull <name> --audit`，再交给对应生成技能
- **一张图要多个机位**：`comfyui-multi-angle`（本机免费，8 个角度 ≈ 5 分钟）→ 用 `image-tools` 拼版对照；同一主体的多机位也是图生视频/i2v 的好素材
- **从文字到成品**：`text-to-image-comfyui` 逐轮出图 → `image-tools` 拼版速览 + 像素比对（与同轮底座对照）
- **要云端模型的画质/中文理解、又不想装权重**：`seedream-text-to-image`（本机 ComfyUI 编排，推理在 ByteDance 云端；按张计费，先 `--dry-run`）
- **改已有的图**：`seedream-image-edit`（底图 + 指令；要局部就在标注层上画一笔，Painter 会按 alpha 合成进去）→ 交付前用 `image-tools` 比对改动是否真的落在目标区域
- **按结构控制构图**：控制图 → `image-edit-comfyui`（调 `--control-strength` / `--canny-low,high`）→ `image-tools` 比对改动是否真的落到区域上
- **图 → 视频**：`text-to-image-comfyui` 出首帧 → `image-to-video-fastvideo3` 让它动起来
- **给图文/短视频配乐**：`comfyui-music-minimax3` 出纯音乐（先 `--plan` 免费验证参数，再按"最短够用"要时长）→ 用 `image-tools` 的 `ffprobe` 核对时长与码率 → 剪辑时 loop 到片长
- **交付前规范化**：`image-tools` 的 `ffkit strip`（剥 tEXt 元数据，像素不变）+ `contact_sheet`（合图）+ `resize`（出缩略图）

---

## 三、运行前提与自检

```bash
# 服务器：远程 ComfyUI
http://192.168.3.5:18000            # ComfyUI 0.39.0，RTX 4060 Ti 8GB
```

| 技能 | 需要的模型 / 节点（服务器上） | 自检命令 | 上次结果 |
|------|------------------------------|----------|----------|
| text-to-image-comfyui（Z-Image） | `z_image_turbo_bf16` / `qwen_3_4b` / `ae` | `python3 scripts/comfyui_gen.py --check` | ✅ `reachable: true` |
| text-to-image-comfyui（Qwen） | `qwen_image_2512_fp8_e4m3fn` / `qwen_2.5_vl_7b_fp8_scaled` / `qwen_image_vae` | `python3 scripts/comfyui_qwen.py --check` | ✅ `missing: []` |
| seedream-text-to-image | **本机不需要权重**；要节点 `ByteDanceSeedreamNodeV3` + ComfyUI 账号 API Key + credits | `python3 scripts/seedream_gen.py --check` | ✅ 节点在位、`schema_drift: none`；真机出图 pro 1K+thinking **63 秒**，参数矩阵 **6/6**（`verify_params.py --yes`，3 分 41 秒） |
| seedream-image-edit | 同上 + `LoadImage` / `Painter`（`Painter` 只在 `--annotate` 时需要） | `python3 scripts/seedream_edit.py --check` | ✅ 四类节点在位、`schema_drift: none`；真机编辑矩阵 **8/8**（`verify_edits.py --yes`，4 张图约 3 分钟）：背景改纯白落到像素上（边缘白占比 0.000→0.722）、标注合成图框内 1.000 不同/框外 0.00000、双参考 `image_1`+`image_2` 可用、flash + 参考图照跑 |
| image-edit-comfyui | 上面 Z-Image 三件 + `Z-Image-Turbo-Fun-Controlnet-Union.safetensors` | `python3 scripts/comfyui_edit.py --check` | ✅ `missing: []`，真机参数矩阵 **28/28** 通过 |
| comfyui-multi-angle | `qwen_image_edit_2511_bf16` / `qwen_2.5_vl_7b_fp8_scaled` / `qwen_image_vae` / `Qwen-Image-Edit-2511-Lightning-4steps` / `qwen-image-edit-2511-multiple-angles-lora` + **13 个节点类** | `python3 scripts/test_skill.py`（离线）+ `python3 scripts/comfyui_angles.py --check` | ✅ 离线 **65/65**；真机 `ok: true`；**真机 8 角度出片 285.8 s**（1024×1024 ×8，单张 35.7 s），人眼+数值双核对 |
| seedance-reference-to-video ⚠️ | **本机不需要权重**；要节点 `ByteDance2ReferenceNodeV2` + `SaveVideo` + `LoadImage` + ComfyUI 账号 API Key + credits | `python3 scripts/seedance_r2v.py --list`（离线）/ `--check`（真机） | ⚠️ **未验证**：语法编译通过而已；`--check` / `--plan` / 真机出片**都没跑过**（按要求"只建不验"） |
| text-to-video-fastvideo3 | 4 个模型文件 + **9 个节点类** | `python3 scripts/comfyui_video.py --check` | ✅ |
| image-to-video-fastvideo3 | 同上（共用权重） | `python3 scripts/comfyui_i2v.py --check` | ✅ |
| comfyui-music-minimax3 | `minimax_music3_dit_fp16` / `minimax_music3_text_encoder_pruned_int8_convrot` / `minimax_music3_dav` + **7 个节点类** | `python3 scripts/test_skill.py`（离线）+ `python3 scripts/comfyui_music.py --check` | ✅ 离线 **43/43**；`--check` `ok: true` |
| comfyui-server | **不需要任何权重**（只查不跑）；读的是 `/system_stats`、`/api/models`、`/api/object_info`、`/templates/index.json`、`/queue` | `python3 scripts/test_skill.py`（离线）+ `python3 scripts/comfyui_server.py --check` | ✅ 离线 **64/64**；真机 `ok: true`（0.39.0 / 114 个权重文件 / 980 个节点类 / 598 个模板）；`audit` 对 6 个在用模板判 `ok: true`、对 3 个缺权重模板准确点名 |
| image-tools | `ffmpeg` / `ffprobe`、Python 3 + numpy（**不需要 Pillow**） | `python3 scripts/test_skill.py` | ✅ `RESULT: PASS` |

> 改完环境（换机器 / 换模型 / 升级 ComfyUI）先跑上面这一列，再谈出图出片。
> 视频节点的**节点类**比图像节点新：ComfyUI 版本偏旧时是节点缺失而不是模型缺失。
> `image-edit-comfyui` 另有真机全参数验证脚本 `scripts/verify_params.py`（对每个参数真实出图并用像素差证明改动落地）。
> `seedream-text-to-image` 同样有 `scripts/verify_params.py`，但它是**付费**的（每步一张图），
> 且必须先有 ComfyUI 账号 API Key；没有凭据会以 `SKIPPED_NO_CREDENTIAL` 退出而不是假装通过。

---

## 四、术语速查

| 术语 | 含义 |
|------|------|
| T2I | Text-to-Image，文生图 |
| I2I | Image-to-Image，图生图（本库用控制图驱动） |
| ControlNet / 控制图 | 用一张图约束结构（本库用 `Canny` 预处理 + `ZImageFunControlnet` 应用） |
| 引擎 | 文生图的两条实现：Z-Image-Turbo（快）/ Qwen-Image（细） |
| partner 节点 / API 节点 | ComfyUI 里**推理不在本机**的节点（`ByteDanceSeedreamNodeV3` 等）：本机不装权重，按张计费 |
| 采集式输入 / `COMFY_AUTOGROW_V3` | 可增删序号的输入，API 名形如 `model.images.image_1`、`image_2` …；Seedream 的参考图就走它 |
| Painter | 服务器端节点：把 RGBA 标注层按 **alpha** 合成到底图上（`IMAGE` 出合成图、`MASK` 出笔迹），桌面端"在图上画一笔再改"就是它 |
| 前端专有节点 | 只存在于界面画布、服务器上没有实现的类（`MarkdownNote` 等）；原样提交会被判 `missing_node_type`，转换后要剔掉 |
| ComfyUI 账号 API Key | platform.comfy.org 发的凭据；无头调用付费节点必须放进 `extra_data.api_key_comfy_org`，否则报 `Unauthorized` |
| T2V / I2V | Text-to-Video / Image-to-Video |
| T2M | Text-to-Music，文生音乐（`comfyui-music-minimax3`） |
| caption / lyrics | MiniMax Music 3 的两个输入：**caption** 是结构化音乐描述（Global Metadata → Vocal Details → Arrangement）；**lyrics** 里只有 `[intro]`/`[verse]`/`[chorus]` 等**段落标签是可执行指令**，歌词文本只传递情绪 |
| tiled decode | 音频 VAE 分块解码：大幅降显存、略慢、接缝有极小风险；本模板默认开着（`ComfyUI` 里那个 `tiled_decode` 开关） |
| ETA（本技能） | 提交前打印的墙钟估算＝`音频秒数 × 16.7`；**这个倍率是真机实测值**，换机器/换精度会变 |
| t2va / fl2va | FastH3 的两个工作流：文生视频+音频 / 首尾帧+音频 |
| `--seed` | 固定随机种子，用于复现（同 seed 同参数 → 像素一致） |
| 接触印相 / 速览图 | contact sheet，把一轮多张拼成一张带标签的大图 |
| 像素判据 | 判断「改动是否生效」看**解码后的像素**，不看文件哈希（ComfyUI 会把执行图写进 PNG 的 tEXt，哈希必变） |
| 落点 | 提示词里那个「件」实际应该长在什么位置/结构上 |
| 探活 | 干活之前的第一个请求（本库统一用 `/system_stats`）：不可达立刻报错退出，不提交任务后长等 |
| 多角度（multi-angle） | 同一主体换机位出图：`comfyui-multi-angle` 一次 8 个（特写/45°右/俯拍/广角/90°右/低机位/90°左/45°左），靠 Multiple-Angles LoRA + 角度提示词 |
| 子图摊平（flatten） | 把"父图套子图"的两级嵌套改成一级再转换——共享转换器只可靠处理一级，否则参考图会丢、输出连线会悬空（实测坑） |
| 可达性剪枝 | 从输出节点出发删掉没人依赖的节点；`--only` 靠它把 193 节点降到 49、KSampler 8→2，真省时间 |
| `audit` / 可跑性审计 | 把工作流引用的权重与节点类和服务器实际清单对账（`comfyui-server`）：先按 `node.mode` 分 active/bypass，再看 `/api/models/<folder>` 与 `/api/object_info` |
| active / bypass 分支 | 工作流里 `mode` 为 0 的节点会执行，`2`（mute）/`4`（bypass）不执行但仍在图里；官方模板常备着"另一条分支"的权重，审计区分错就会误判 |
| `model_patches` | 模型补丁目录：Z-Image Fun Union ControlNet 的权重在这里，**不在 `controlnet`**；`/api/object_info` 不枚举它，得查 `/api/models` |
| userdata | ComfyUI 的 `/api/userdata`（桌面端"我保存的工作流"）；`/templates/index.json` 才是官方模板目录（本机 598 条），`/api/workflow_templates` 在 0.39.0 上是空的 |
| 写操作护栏 / `--yes` | 会打断别人或改服务器状态的动词（`interrupt` / `free` / `clear-queue`）必须显式 `--yes`，否则退出码 3 且一个请求都不发 |

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-02 | v1.0 | image-gen 侧：`methods/` 改组为技能库 .agents/skills/，索引改技能地图与选路表 | 小七 |
| 2026-10-04 | v1.4 | image-gen 侧：参数静默失效治理 + 复现判据统一；新增 image-tools | 小七 |
| 2026-10-05 | v1.5 | image-gen 侧：收敛为只留可执行技能（移除 9 个纯文档技能） | 小七 |
| **2026-10-05** | **v2.0** | **扁平化合并**：`image-gen/.agents/skills/README.md` 与 `video-gen/.agents/skills/README.md` 合并为本文件；目录从 `image-gen/skills`、`video-gen/skills` 迁至仓库根 `.agents/skills/`；技能地图与选路表改为图像/视频统一索引（5 个技能） | 小七 |
| 2026-10-06 | v2.1 | **重新收录 Seedream 云端出图**：新增 [`seedream-text-to-image`](seedream-text-to-image/SKILL.md)（ComfyUI partner 节点跑 ByteDance Seedream 5.0，本机零权重、按张计费、无头要 API Key）；选路表/技能地图/技能表/自检表各加一行，补"第三条路"（模型在云端、编排在本机）的取舍说明与两条术语 | 小七 |
| 2026-10-06 | v2.2 | **新增 [`seedream-image-edit`](seedream-image-edit/SKILL.md)**：同一个 Seedream 付费节点做**图片编辑**——上传底图（+ 可选 RGBA 标注层，Painter 按 alpha 合成）接进 `model.images.image_N`，支持多图参考、`--size auto`（按底图比例挑预设）；用 `_shared.py` 复用姊妹技能的引擎，不复制凭据/schema 代码。同时给 `seedream_api.py` 补 `prune_ui_only()`（桌面导出图里的 `MarkdownNote` 会让 /prompt 判 `missing_node_type`）。选路表/技能地图/技能表/自检表/组合用法各加一行，补两条术语 | 小七 |
| 2026-10-11 | v2.3 | **新增 [`comfyui-server`](comfyui-server/SKILL.md)**（技能库第 9 个）：把"**服务器本身**"当对象来查——状态/显存/队列、`/api/models` 权重目录、`/api/object_info` 节点 schema、`/templates/index.json` 官方模板（本机 598 个，可搜可拉）、`audit` 判某模板/工作流**在本机缺什么**、历史记录与任意产物下载、userdata 工作流；写操作 `interrupt`/`free`/`clear-queue`/`upload` 一律要 `--yes`（护栏缺失时退出码 3）。**边界判据**："这个功能在完全没有 prompt 的情况下还有意义吗？"有 → 归它；没有 → 归生成技能，因此它**一步生成都不做**（UI→API 转换仍在 `text-to-image-comfyui`）。选路表/技能地图/技能表/自检表/组合用法各加一行，新增 6 条术语；同时订正服务器版本 `0.38.0` → **`0.39.0`**（实测） | 小七 |
| 2026-10-11 | v2.4 | **新增 [`seedance-reference-to-video`](seedance-reference-to-video/SKILL.md)**（技能库第 10 个）**⚠️ 按用户要求"只建不验"**：以一份导出的 UI 工作流（`ByteDance2ReferenceNodeV2`，`LoadImage → Seedance 2.5 → SaveVideo`）为资产 + 一份**本地缓存的** schema 快照（5 个模型键、动态下拉框子输入、autogrow 参考上限 30/9）静态构造；脚本 `seedance_r2v.py` 提供 `--list / --check / --show-default-prompt / --plan / 生成`，复用兄弟技能的凭据通道与 UI→API 转换器。**没跑过 `--check`/`--plan`/真机出片，没有 `test_skill.py`，未进 `check.sh`** —— 例外与"首次真机前必做的 5 步"写在文件头与该技能 SKILL.md 顶部。技能地图的"出片"组改为本地/云端混排并注明权重约束 | 小七 |
| 2026-10-12 | v2.5 | **新增 [`comfyui-multi-angle`](comfyui-multi-angle/SKILL.md)**（技能库第 11 个）：一张图一次出 **8 个不同角度**（Qwen-Image-Edit 2511 + Multiple-Angles LoRA，本机免费可重复跑）。以官方模板 "1 Click Multiple Character Angles" 的导出图为资产（498 KB / 三级图层 / 展开 193 节点），脚本提供 `--list / --check / --plan / 生成` + `--only`（按节点 id 旁路 + 可达性剪枝）/ `--angle` / 前后缀 / `--output-prefix` / `--fast, --no-fast` / `--seed`。**两个实测坑都修在技能里**：① 两级嵌套共享转换器处理不了（参考图会丢 + 8 条输出连线悬空）→ 新增 `flatten_parent()` 摊平父图，并把"指向图外节点的连线"升级成硬校验；② 官方模板两处输出前缀写错/重名（45°右→wide_shot、90°右→aerial_view）→ 资产已修正。真机：`--check` ok、`--plan` 0 悬空、**8 角度出片 285.8 s**（1024×1024×8，单张 35.7 s），人眼与数值双核对；离线自检 **65/65**。选路表/技能地图/技能表/自检表/组合用法各加一条，新增 3 条术语 | 小七 |
