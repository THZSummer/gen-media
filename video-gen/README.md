# 视频生成（Video Generation）- 总导航

> 基于**火山方舟 Ark** 视频生成能力（豆包 Seedance 系列）的视频生成知识库。
> 💰 **Profile 路由**：Seedance 2.0 系列（含 mini）走 platform 按量（`--profile platform_cn-beijing_accountwide`）；其余模型（seedream 图片 / seedance-1.5-pro / TTS / ASR）走 agent-plan。Medium 套餐不含 2.0 系列，1.5-pro 即将下线。
> 工具入口：`arkcli +gen`（三步工作流：① `resources list` 查可用模型 -> ② `models get` 查 supported_params -> ③ `+gen` 生成）。

---

## 一、组织方式

本库按**「方法」+「技能」+「项目」**三条线组织：

```
video-gen/
├── README.md          ← 你在这里（总导航）
├── methods/           技术方法手册：按生成技术路径讲"怎么生成"
│   ├── README.md        方法总览（能力地图 + 三步法 + 8 个方法）
│   ├── text-to-video/   文生视频
│   ├── image-to-video/  图生视频
│   ├── reference-video/ 参考视频
│   ├── audio-driven/    音频驱动
│   ├── cinematography/  镜头运镜
│   ├── quality-and-cost/质量与成本
│   ├── long-video-chain/长视频续接
│   └── content-safety/  内容安全
├── skills/            可执行技能：带脚本与工作流资产，讲"怎么跑起来"（本地 ComfyUI）
│   ├── README.md        技能索引 + 本地/云端选路表
│   ├── text-to-video-fastvideo3/   文生视频 + 同步音频（t2va）
│   └── image-to-video-fastvideo3/  图生视频 + 同步音频（fl2va，首帧/尾帧）
└── projects/          具体项目：一项目一目录，讲"生成什么"
    ├── README.md        项目索引 + 建项目规范
    └── _template/       项目模板（复制即用）
```

### 三条线的关系

| 线 | 回答 | 组织方式 |
|----|------|----------|
| **[methods/](methods/README.md)** | **怎么生成**（技术路径，云端 Ark 为主） | 按技术方法分目录，可复用 |
| **[skills/](skills/README.md)** | **怎么跑起来**（可执行技能，本地 ComfyUI） | 一技能一目录，含 `SKILL.md` + 脚本 + 工作流 |
| **[projects/](projects/README.md)** | **生成什么**（具体业务） | 按项目分目录，引用 methods / skills |

一个**项目**按需挑选若干**方法**或**技能**组合完成：例如"产品广告项目" = 图生视频（首帧）+ 镜头运镜 + 长视频续接。

---

## 二、导航

- 📚 **[methods/](methods/README.md)** — 技术方法手册
  - 文生 / 图生 / 参考视频 / 音频驱动 四条输入路径 + 镜头 / 质量 / 续接 / 安全 四个横切控制
  - 每个方法含：能力映射、prompt 策略、参数选型、命令模板、踩坑点、检查清单
- 🛠️ **[skills/](skills/README.md)** — 可执行技能（本地 ComfyUI）
  - [text-to-video-fastvideo3](skills/text-to-video-fastvideo3/SKILL.md)：FastH3 文生视频 + **同步音频**，8 步出片
  - [image-to-video-fastvideo3](skills/image-to-video-fastvideo3/SKILL.md)：FastH3 图生视频（首帧/可选尾帧）+ 同步音频
  - ⚠️ 成本：35 GB 权重压 8 GB 显存，慢是必然的（技能内有成本章节与应对）；两者共用权重、不能同时跑
- 🗂️ **[projects/](projects/README.md)** — 具体项目
  - 一项目一目录，每个项目 `README.md` 是该项目的视频生成规划
  - 新建项目：复制 [_template/](projects/_template/README.md) 改写

---

## 三、快速上手

### 找方法

进 [methods/README.md](methods/README.md) 看能力地图，按手头素材选路径：

| 你手里有 | 去哪个方法 |
|----------|-----------|
| 只有文字描述 | [text-to-video](methods/text-to-video/README.md) |
| 一张图 | [image-to-video](methods/image-to-video/README.md) |
| 一段参考视频 | [reference-video](methods/reference-video/README.md) |
| 一段音频 | [audio-driven](methods/audio-driven/README.md) |

### 建项目

进 [projects/](projects/README.md)，复制 `_template/` 建项目目录，在项目 README 里规划交付物、分镜、所用方法。

### 通用三步法（所有方法通用）

```bash
arkcli resources list --modality video                   # Step 1 查可用模型
arkcli models get "$MODEL" --transform supported_params  # Step 2 查参数
arkcli +gen --model "$MODEL" "<prompt>" --open           # Step 3 生成（视频异步，返回 task_id）
arkcli gen get <task_id> --open                          # 轮询到 succeeded 自动下载
```

详见 [methods/README.md](methods/README.md)。术语速查亦见该篇。

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-07-18 | v1.0 | 初始规划，建立 8 个主题子目录与总导航 | 小七 |
| 2026-07-18 | v2.0 | 顶层重构为「项目制」：methods/ 汇总技术方法，projects/ 按具体项目组织 | 小七 |
| 2026-07-18 | v2.1 | 标注 agent-plan 不含视频需 platform 按量（仅 mini 可用）；补充 draft/last-frame/save-to 踩坑 | 小七 |
| 2026-07-18 | v2.2 | 修正套餐说明：Medium 含 seedream-5.0-lite/seedance-1.5-pro/TTS/ASR，仅不含 2.0 系列；记录 profile 路由规则 | 小七 |

> 📦 **体积约定（2026-10-05）**：为把仓库体积压回 Gitee 的告警线以下，
> **逐轮中间产物不再入库**（本地文件保留，固定 seed 可复现）：
> - `out/v3-optimized/`、`out/v3-chain-10shots/`、逐镜头 `shot*.mp4`、`test_*.mp4`、`cgt-*.mp4` 等中间件
- 每个项目保留**一个成片**（`*_full.mp4` / `*_narrated.mp4`）与全部文档、分镜图

> 所以本文档里的相关链接指向的是**本地文件**，在远端仓库中不存在。
