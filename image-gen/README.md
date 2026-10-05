# 图片生成（Image Generation）· 总导航

> 基于**本机 ComfyUI**（远程 GPU 机 `http://192.168.3.5:18000`）的图片生成库：
> 文生图（Z-Image-Turbo / Qwen-Image 两个引擎）、控制图生图（Z-Image Fun Union ControlNet），
> 外加一组**不用 AI** 的确定性图像工具（ffmpeg + numpy：速览图 / 像素比对 / 去元数据 / 缩放裁切）。
> 📌 图片是**同步**返回的：提交即出图，没有 `task_id`、不需要轮询（轮询是视频的异步语义）。

> ⚠️ **2026-10-05 起，本目录只保留带脚本、可在真机跑通的技能。** 原先 9 个只描述方舟 Ark Seedream
> 云端用法、没有脚本也没有自检入口的纯文档技能已移除：`text-to-image`、`image-editing`、
> `multi-image-reference`、`multi-view-consistency`、`prompt-engineering`、`parameters-and-output`、
> `quality-and-cost`、`content-safety`、`image-workflow`。
> 需要时从 git 历史取回：`git log --diff-filter=D --oneline -- image-gen/skills/`。

---

## 一、组织方式

本库按**「技能」+「项目」**两条线组织：

```
image-gen/
├── README.md          ← 你在这里（总导航）
├── skills/           技能库：每个技能一个目录，入口为 SKILL.md，讲"怎么生成"
│   ├── README.md                 技能索引（能力地图 + 选路表 + 运行前提与自检）
│   ├── text-to-image-comfyui/    ComfyUI 文生图：Z-Image-Turbo（快）+ Qwen-Image（细）两个引擎
│   ├── image-edit-comfyui/       ComfyUI 图生图：Fun Union ControlNet 控制图驱动
│   └── image-tools/              确定性图像工具（不用 AI）：速览图 / 像素比对 / 去元数据 / 缩放裁切
└── projects/          具体项目：一项目一目录，讲"生成什么"
    ├── README.md              项目索引 + 建项目规范
    ├── _template/             项目模板（复制即用）
    ├── bio-splice/            生物拼接：12 子主题 × 5 期 / 135 件成品（主力项目）
    ├── bone-china-doll/       骨瓷人偶系列
    └── character-lookbook/    角色多角度设定图库（示例项目）
```

### 两条线的关系

| 线 | 回答 | 组织方式 |
|----|------|----------|
| **[skills/](skills/README.md)** | **怎么生成**（技术路径） | 按技术路径分目录，每目录一个 `SKILL.md`，可复用 |
| **[projects/](projects/README.md)** | **生成什么**（具体业务） | 按项目分目录，引用 skills |

一个**项目**按需挑选若干**技能**组合完成：例如"生物拼接" = 文生图（Z-Image-Turbo 逐轮出图）+ 确定性工具（合图 / 逐像素比对 / 评分佐证）。

---

## 二、导航

- 📚 **[skills/](skills/README.md)** — 技能库（3 个，全部带脚本）
  - 出图（文生图）→ 改图（控制图生图）两条生成路径 + 一个横切的确定性图像工具箱
  - 每个技能含 `SKILL.md`：frontmatter（触发描述）+ 何时用 + 前置检查 + 执行步骤 + 踩坑点 + 检查清单
  - `skills/README.md` 里有**运行前提与自检命令**表：每个技能一条命令，随时可确认环境是否还健康
- 🗂️ **[projects/](projects/README.md)** — 具体项目
  - 一项目一目录，每个项目 `README.md` 是该项目的图片生成规划
  - 新建项目：复制 [_template/](projects/_template/README.md) 改写
- 🎬 **配套视频库**：[../video-gen/](../video-gen/README.md)（图片是视频的前置工序，分镜图 / 首帧在那边被消费）

---

## 三、快速上手

### 找技能

进 [skills/README.md](skills/README.md) 看能力地图，按手头素材选路径：

| 你手里有 | 加载哪个技能 |
|----------|-----------|
| 只有文字描述 | [text-to-image-comfyui](skills/text-to-image-comfyui/SKILL.md)（Z-Image-Turbo 快出 / Qwen-Image 高细节） |
| 有一张控制图（线稿/照片/姿态图），要按结构出图 | [image-edit-comfyui](skills/image-edit-comfyui/SKILL.md) |
| 要把多张图拼成速览图 / 比对两张图是否相同 / 去元数据 / 缩放裁切 | [image-tools](skills/image-tools/SKILL.md) |

### 建项目

进 [projects/](projects/README.md)，复制 `_template/` 建项目目录，在项目 README 里规划交付物、图片清单、所用技能。

### 最常用的命令（都是真机验证过的）

```bash
# 文生图：Z-Image-Turbo（快，约 25 秒/张 @1024²）
cd image-gen/skills/text-to-image-comfyui
python3 scripts/comfyui_gen.py --check                       # 先确认服务器可达
python3 scripts/comfyui_gen.py --prompt "..." --out-dir out/

# 文生图：Qwen-Image（细节引擎，约 7–10 分钟/张，支持真负向）
python3 scripts/comfyui_qwen.py --check                      # 三个模型文件是否在位
python3 scripts/comfyui_qwen.py --prompt "..." --negative "blurry, plastic, cartoon" \
  --width 1024 --height 1360 --steps 24 --cfg 3.0 --seed 7 --out-dir out/

# 控制图生图（输出尺寸默认 = 控制图尺寸）
cd ../image-edit-comfyui
python3 scripts/comfyui_edit.py --check                      # 四个模型文件是否在位
python3 scripts/comfyui_edit.py --image ref.png --prompt "..." --out-dir out/

# 确定性工具：整轮速览图 / 像素比对 / 剥元数据
cd ../image-tools
python3 scripts/contact_sheet.py --round out/r1/round.json -o out/r1/sheet.png --cols 3
python3 scripts/pngdiff.py a.png b.png --json                # 0=同 1=异 2=出错
python3 scripts/ffkit.py strip in.png -o out.png             # 剥 tEXt（像素不变）
```

详见 [skills/README.md](skills/README.md)。

---

## 四、运行前提

| 依赖 | 用途 | 当前状态（2026-10-05 实测） |
|------|------|------------------------------|
| ComfyUI `http://192.168.3.5:18000`（远程 Windows + RTX 4060 Ti 8GB） | 全部出图技能 | ✅ 可达（ComfyUI 0.38.0） |
| 模型 `z_image_turbo_bf16` / `qwen_3_4b` / `ae` | Z-Image 文生图 | ✅ 三件在位 |
| 模型 `qwen_image_2512_fp8_e4m3fn` / `qwen_2.5_vl_7b_fp8_scaled` / `qwen_image_vae` | Qwen-Image 文生图 | ✅ 三件在位 |
| 模型 `Z-Image-Turbo-Fun-Controlnet-Union.safetensors` | 控制图生图 | ✅ 在位（经 `ModelPatchLoader` + `ZImageFunControlnet`） |
| `ffmpeg` / `ffprobe` | 图像编解码、速览图、去元数据 | ✅ ffmpeg 8.0.1 |
| Python 3 + numpy | 像素比对、评分佐证 | ✅ numpy 2.5.0（**不需要 Pillow**） |

每个技能都自带自检入口，改完环境先跑它（详见 [skills/README.md](skills/README.md) 的「运行前提与自检」表）。

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-02 | v1.0 | 初始建立：从 video-gen 拆出图片生成独立成库，建立 9 个技能 + 项目制 + 模板 + 示例项目 | 小七 |
| 2026-10-02 | v2.0 | `methods/` 改组为技能库 `skills/`：每个技能以 `SKILL.md`（YAML frontmatter + 指令体）呈现，导航/术语全面改为"技能" | 小七 |
| 2026-10-02 | v2.1 | 新增 ComfyUI 文生图技能（远程 Z-Image-Turbo 工作流，192.168.3.5:18000）：工作流 JSON→/prompt API 转换 + 提交轮询下载脚本 | 小七 |
| 2026-10-02 | v2.2 | 新增 ComfyUI 图生图技能 image-edit-comfyui（Fun Union Controlnet）：共享转换器支持 workflow profile / mute-bypass / 连线型子图接口 / SaveImage 过滤；24/24 真机参数验证通过 | 小七 |
| 2026-10-05 | **v3.0** | **收敛为"只留可执行技能"**：移除 9 个无脚本、无自检入口的纯文档技能（方舟 Seedream 云端用法），保留 3 个带脚本且真机验证通过的技能；总导航、选路表、模型与前提全部重写为 ComfyUI 本地路径；6 处 `cd /home/usb/wks/gits/Book/...` 旧绝对路径改为仓库相对路径 | 小七 |
