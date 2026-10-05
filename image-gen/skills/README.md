---
name: ark-image-skills-index
description: 火山方舟 Ark Seedream 图片生成技能索引与总览：9 个技能的能力地图、按输入素材的选路表、通用三步法（resources list → models get → +gen）与术语速查。触发词：图片生成怎么开始、seedream 用哪个技能、图片能力地图、文生图/图像编辑/多图参考/多视角怎么选。
whenToUse: 当不确定该用哪个图片生成技能、需要总览能力地图或通用执行流程时使用。确定任务后加载对应的具体技能目录（如 text-to-image/SKILL.md）。
---

# 图片生成技能总览（Skills Index）

> 返回[首页](../README.md) ｜ 项目实践见 [../projects/](../projects/README.md) ｜ 配套视频技能见 [../../video-gen/](../../video-gen/README.md)

> 本目录是**技能库**：每个子目录一个技能，入口为 `SKILL.md`（YAML frontmatter 含 `name` / `description` / `whenToUse`）。
> 技能讲"**怎么做**"，具体项目（"**做什么**"）见 [projects/](../projects/README.md)。

---

## 一、快速选路

**你手里有什么，就加载哪个技能：**

| 你手里有 | 加载技能 |
|----------|----------|
| 只有文字描述（默认走本机 ComfyUI） | [text-to-image-comfyui](text-to-image-comfyui/SKILL.md) |
| 有一张控制图（线稿/照片），要按结构出图 | [image-edit-comfyui](image-edit-comfyui/SKILL.md) |
| 要把多张图合并成速览图 / 比对两张图是否相同 / 去元数据 | [image-tools](image-tools/SKILL.md) |
| 要用方舟 Seedream 云端文生图 | [text-to-image](text-to-image/SKILL.md) |
| 一张图，想改背景/换元素 | [image-editing](image-editing/SKILL.md) |
| 多张图（角色 + 场景），想融合 | [multi-image-reference](multi-image-reference/SKILL.md) |
| 一张图，想补其它视角 | [multi-view-consistency](multi-view-consistency/SKILL.md) |
| 出图不可控 / 要写 prompt | [prompt-engineering](prompt-engineering/SKILL.md) |
| 参数被拒 / 要复现 / 不确定支持啥 | [parameters-and-output](parameters-and-output/SKILL.md) |
| 批量出图 / 控制成本 | [quality-and-cost](quality-and-cost/SKILL.md) |
| 审核被拒 / 题材敏感 | [content-safety](content-safety/SKILL.md) |
| 要落盘归档 / 接视频 | [image-workflow](image-workflow/SKILL.md) |

---

## 二、技能地图

```
skills/
├── README.md                     ← 你在这里（技能索引）
│
├── 🖼️ 出图 / 改图
│   ├── text-to-image-comfyui/    ComfyUI 文生图：远程 Z-Image-Turbo 工作流（HTTP API）
│   ├── image-edit-comfyui/       ComfyUI 图生图：ControlNet（Z-Image Fun Union）控制图驱动
│   ├── text-to-image/            文生图：方舟 Seedream 云端 API（lite / pro）
│   ├── image-editing/            图像编辑：单图换背景/换元素（pro）
│   ├── multi-image-reference/    多图参考：角色×场景融合（pro）
│   └── multi-view-consistency/   多视角一致性：补角度保形象（pro）
│
├── 🎛️ 横切控制
│   ├── prompt-engineering/       提示词：四要素 + 模板
│   ├── parameters-and-output/    参数与输出：尺寸/格式/张数/种子
│   ├── quality-and-cost/         质量与成本：阶段化取舍
│   └── content-safety/           内容安全：过审与合规
│
└── 🔗 工作流
    └── image-workflow/           落盘、追溯、衔接 I2V
```

### 技能表

| 技能 | 一句话 | 输入 → 输出 |
|------|--------|-------------|
| [text-to-image-comfyui](text-to-image-comfyui/SKILL.md) | 远程 ComfyUI 跑 Z-Image-Turbo 工作流 | prompt → 图片文件 |
| [image-edit-comfyui](image-edit-comfyui/SKILL.md) | 远程 ComfyUI 跑 ControlNet 控制图生图 | 控制图 + prompt → 图片文件 |
| [image-tools](image-tools/SKILL.md) | **不用 AI** 的确定性图片处理（ffmpeg + numpy）：拼版速览图、像素比对与 PSNR/SSIM、去元数据、缩放裁切 | 多张图片 → 一张速览图 / 比对报告 |
| [text-to-image](text-to-image/SKILL.md) | 方舟 Seedream 纯 prompt 出图 | prompt → 图片 |
| [image-editing](image-editing/SKILL.md) | 单图 + 编辑指令改图 | 1 图 + 指令 → 图片 |
| [multi-image-reference](multi-image-reference/SKILL.md) | 多图参考融合 | ≥2 图 + prompt → 图片 |
| [multi-view-consistency](multi-view-consistency/SKILL.md) | 参考图生成新视角 | 1 图 + 视角 → 图片 |
| [prompt-engineering](prompt-engineering/SKILL.md) | 结构化写 prompt | 需求 → prompt |
| [parameters-and-output](parameters-and-output/SKILL.md) | 参数与尺寸选型 | 用途 → 参数组合 |
| [quality-and-cost](quality-and-cost/SKILL.md) | 质量成本权衡 | 预算 → 阶段方案 |
| [content-safety](content-safety/SKILL.md) | 过审与合规 | 敏感题材 → 合规 prompt |
| [image-workflow](image-workflow/SKILL.md) | 资产与衔接 | 图片 → 归档/视频 |

### 组合用法

- **角色设定图库**：`text-to-image`（初版正面）→ `multi-view-consistency`（补角度）→ `image-editing`（换装）
- **分镜图先行**：`text-to-image`（每镜关键帧）→ 审核 → `image-workflow`（落盘）→ video-gen I2V
- **海报/封面**：`text-to-image`（主体）→ `image-editing`（改背景/加元素）→ `parameters-and-output`（切竖版尺寸重出）
- **场景化角色**：`multi-image-reference`（角色 + 场景融合）批量产出同角色多场景图

---

## 三、通用执行三步法

> 所有技能都遵循这个流程，区别只在 Step 3 的参数与 `--input` 组合。

```bash
# Step 1：列当前 profile 可用的图片模型
arkcli resources list --modality image

# Step 2：查选定模型 $MODEL 支持的参数
arkcli models get "$MODEL" --transform supported_params

# Step 3：按可用参数生成（图片同步返回，直接拿结果）
arkcli +gen --model "$MODEL" --size "2560x1440" --output-format jpeg "<prompt>" --save-to out/
```

### 同步语义（重点）

```
+gen 提交 ──► 同步返回图片结果（url / b64_json）──► --save-to 落盘
```

- **没有 `task_id`**：图片不像视频那样异步排队，不要去找 `gen get`
- 预签名 `output_url` **24 小时失效**，长期保存依赖 `local_path` 或及时下载

---

## 四、模型与 Profile 路由

| 模型 | 完整 ID | Profile | 能力 |
|------|---------|---------|------|
| Seedream 5.0 Lite | `doubao-seedream-5-0-lite` | agent-plan（**默认**，勿用 Auto） | 仅文生图；⚠️ 像素 ≥3,686,400 |
| Seedream 5.0 Pro | `doubao-seedream-5-0-pro-260628` | ⚠️ `platform_cn-beijing_accountwide` | 文生图 + 编辑 + 多图参考 + 多视角；无像素下限 |

> ⚠️ pro 必须用**完整版本 ID**（`-260628`）；族名在 platform 数据面 NotFound。
> 🔀 lite 走 agent-plan、pro 走 platform 按量，**不可混**：pro 调 agent-plan 报 `does not support the agent plan feature`。

---

## 五、术语速查

| 术语 | 含义 |
|------|------|
| T2I | Text-to-Image，文生图 |
| I2I | Image-to-Image，图生图 / 图像编辑 |
| Seedream | 豆包图片生成模型系列 |
| `--size` | 输出尺寸（像素）；图片比例靠它，不靠 `--ratio` |
| `--input` | 参考图输入；文生图不传 |
| `@图像N` | prompt 中对第 N 张 `--input` 参考图的引用 |
| `--seed` | 固定随机种子，用于复现 |
| `supported_params` | 模型实际支持的参数清单，Step 2 必查 |
| 预签名 URL | 临时下载地址，24h 失效，须及时落盘 |

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-02 | v1.0 | methods/ 改组为技能库 skills/：每个技能以 SKILL.md（frontmatter + 指令体）呈现，索引改技能地图与选路表 | 小七 |
| 2026-10-02 | v1.1 | 新增 text-to-image-comfyui（远程 ComfyUI / Z-Image-Turbo，192.168.3.5:18000），文生图形成 ComfyUI 与 Seedream 两条路径 | 小七 |
| 2026-10-02 | v1.2 | 新增 image-edit-comfyui（Z-Image-Turbo Fun Union ControlNet 控制图生图，全参数 24/24 真机验证）；共享转换器新增 workflow profile、mute/bypass 处理、连线型子图接口回接、SaveImage 过滤与 UI 字段剔除 | 小七 |
| 2026-10-04 | v1.3 | **参数静默失效治理 + 复现判据统一**：转换器与两个引擎新增 unapplied 检测（`UnappliedOverrideError`，默认 strict，`--allow-unapplied` 可放行）；`pngdiff.py` 收进技能（判据统一为解码像素，附 R34/R35 实测：同像素不同 sha）；`verify_params.py` 改为像素判据 + 服务器探活快速失败 + 修好 `--quick` | 小七 |
| 2026-10-04 | v1.4 | **新增 image-tools（不用 AI 的确定性图片处理）**：ffmpeg + numpy 实现拼版速览图（`drawtext` 真字体，支持中文标签）、像素比对与 PSNR/SSIM、PNG 元数据剥离、缩放裁切。`pngdiff.py` 从 text-to-image-comfyui 迁入并补上此前只在文档里被引用、仓库中无实现的 SSIM/PSNR；依赖方向改为「生成技能依赖本技能」 | 小七 |
