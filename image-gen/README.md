# 图片生成（Image Generation）- 总导航

> 基于**火山方舟 Ark** 图片生成能力（豆包 Seedream 系列）的图片生成知识库。
> 💰 **Profile 路由**：`doubao-seedream-5-0-lite` 走 agent-plan（默认 profile，Medium 套餐含）；`doubao-seedream-5-0-pro-260628` 走 platform 按量（`--profile platform_cn-beijing_accountwide`）。两者不可混。
> 工具入口：`arkcli +gen`（三步工作流：① `resources list` 查可用模型 -> ② `models get` 查 supported_params -> ③ `+gen` 生成）。
> 📌 **图片是同步返回的**：提交即出图，没有 `task_id`、不需要 `gen get` 轮询（轮询是视频的异步语义）。

---

## 一、组织方式

本库按**「技能」+「项目」**两条线组织：

```
image-gen/
├── README.md          ← 你在这里（总导航）
├── skills/           技能库：每个技能一个目录，入口为 SKILL.md，讲"怎么生成"
│   ├── README.md          技能索引（能力地图 + 选路表 + 三步法）
│   ├── text-to-image-comfyui/  ComfyUI 文生图：远程 Z-Image-Turbo 工作流（HTTP API）
│   ├── image-edit-comfyui/     ComfyUI 图生图：ControlNet 控制图驱动（Z-Image Fun Union）
│   ├── text-to-image/     文生图：方舟 Seedream 云端 API（纯 prompt 出图）
│   ├── image-editing/     图像编辑（单图改背景/换元素）
│   ├── multi-image-reference/  多图参考（角色 × 场景融合）
│   ├── multi-view-consistency/ 多视角一致性（正面图→背面/侧面）
│   ├── prompt-engineering/     提示词工程（结构化 prompt 写法）
│   ├── parameters-and-output/  参数与输出（--size / --n / --seed …）
│   ├── quality-and-cost/       质量与成本（尺寸/张数/模型权衡）
│   ├── content-safety/         内容安全（审核拦截与合规）
│   └── image-workflow/         图片工作流（T2I → I2V 衔接、落盘、资产库）
└── projects/          具体项目：一项目一目录，讲"生成什么"
    ├── README.md         项目索引 + 建项目规范
    ├── _template/        项目模板（复制即用）
    └── character-lookbook/  示例项目：角色多角度设定图库
```

### 两条线的关系

| 线 | 回答 | 组织方式 |
|----|------|----------|
| **[skills/](skills/README.md)** | **怎么生成**（技术路径） | 按技术路径分目录，每目录一个 `SKILL.md`，可复用 |
| **[projects/](projects/README.md)** | **生成什么**（具体业务） | 按项目分目录，引用 skills |

一个**项目**按需挑选若干**技能**组合完成：例如"角色设定图库" = 文生图（初版）+ 多视角一致性（补角度）+ 图像编辑（换装）+ 多图参考（场景融合）。

---

## 二、导航

- 📚 **[skills/](skills/README.md)** — 技能库
  - 出图（文生图）→ 改图（图像编辑）→ 融合（多图参考）→ 一致性（多视角）四条生成路径 + 提示词 / 参数 / 质量成本 / 安全 / 工作流五个横切技能
  - 每个技能含 `SKILL.md`：frontmatter（触发描述）+ 何时用 + 前置检查 + 执行步骤 + 踩坑点 + 检查清单
- 🗂️ **[projects/](projects/README.md)** — 具体项目
  - 一项目一目录，每个项目 `README.md` 是该项目的图片生成规划
  - 新建项目：复制 [_template/](projects/_template/README.md) 改写
- 🎬 **配套视频库**：[../video-gen/](../video-gen/README.md)（图片是视频的前置工序，分镜图/T2I 首帧在那边被消费）

---

## 三、快速上手

### 找技能

进 [skills/README.md](skills/README.md) 看能力地图，按手头素材选路径：

| 你手里有 | 加载哪个技能 |
|----------|-----------|
| 只有文字描述（默认走本机 ComfyUI） | [text-to-image-comfyui](skills/text-to-image-comfyui/SKILL.md) |
| 有一张控制图要按结构出图 | [image-edit-comfyui](skills/image-edit-comfyui/SKILL.md) |
| 要用方舟 Seedream 云端文生图 | [text-to-image](skills/text-to-image/SKILL.md) |
| 一张图，想改背景/换元素 | [image-editing](skills/image-editing/SKILL.md) |
| 多张图（角色 + 场景），想融合 | [multi-image-reference](skills/multi-image-reference/SKILL.md) |
| 一张图，想补其它视角 | [multi-view-consistency](skills/multi-view-consistency/SKILL.md) |
| 已有图，想接入视频 | [image-workflow](skills/image-workflow/SKILL.md) → video-gen I2V |

### 建项目

进 [projects/](projects/README.md)，复制 `_template/` 建项目目录，在项目 README 里规划交付物、图片清单、所用技能。

### 通用三步法（所有技能通用）

```bash
# Step 1：列当前 profile 可用的图片模型
arkcli resources list --modality image

# Step 2：查选定模型 $MODEL 支持的参数（sp 空则用 modality 兜底默认）
arkcli models get "$MODEL" --transform supported_params

# Step 3：按可用参数生成（图片同步返回，无需轮询）
arkcli +gen --model "$MODEL" --size "2560x1440" --output-format jpeg \
  "<prompt>" --save-to out/
```

### 最常用的两条命令

```bash
# 文生图：lite（agent-plan 默认 profile）
MODEL="doubao-seedream-5-0-lite"
arkcli +gen --model "$MODEL" --size "2560x1440" --output-format jpeg \
  "<prompt>" --save-to out/

# 图像编辑：pro（platform 按量，完整版本 ID，无像素下限）
MODEL="doubao-seedream-5-0-pro-260628"
arkcli +gen --model "$MODEL" --profile platform_cn-beijing_accountwide \
  --input @base.jpg --size "2560x1440" --output-format jpeg \
  "把背景改成赛博都市夜景，霓虹灯箱与车流光轨，人物保持完全不变" --save-to out/
```

详见 [skills/README.md](skills/README.md)。术语速查亦见该篇。

---

## 四、当前模型速查（2026-08 实测，以 `resources list` 为准）

| 模型 | 完整 ID | Profile | 核心能力 | 像素下限 |
|------|---------|---------|----------|----------|
| Seedream 5.0 Lite | `doubao-seedream-5-0-lite` | agent-plan（默认） | 文生图 | ⚠️ ≥3,686,400 |
| Seedream 5.0 Pro | `doubao-seedream-5-0-pro-260628` | platform 按量 | 文生图 + **图像编辑/多图参考** | ✅ 无下限 |

> ⚠️ 图片比例用 `--size`（像素）指定，**不是 `--ratio`**（`--ratio` 只对视频任务生效，图片任务传了会被忽略，落到默认 2048×2048 正方形）。

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-02 | v1.0 | 初始建立：从 video-gen 拆出图片生成独立成库，建立 9 个技能 + 项目制 + 模板 + 示例项目 | 小七 |
| 2026-10-02 | v2.0 | `methods/` 改组为技能库 `skills/`：每个技能以 `SKILL.md`（YAML frontmatter + 指令体）呈现，导航/术语全面改为"技能" | 小七 |
| 2026-10-02 | v2.1 | 新增 ComfyUI 文生图技能（远程 Z-Image-Turbo 工作流，192.168.3.5:18000）：工作流 JSON→/prompt API 转换 + 提交轮询下载脚本 | 小七 |
| 2026-10-02 | v2.2 | 新增 ComfyUI 图生图技能 image-edit-comfyui（Fun Union ControlNet）：共享转换器支持 workflow profile / mute-bypass / 连线型子图接口 / SaveImage 过滤；24/24 真机参数验证通过 | 小七 |
