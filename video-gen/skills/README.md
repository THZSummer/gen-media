---
name: ark-video-skills-index
description: 视频生成技能索引与总览：本地 ComfyUI（FastVideo FastH3 / MiniMax-H3）与云端方舟 Seedance 两条出片路径的能力地图与选路表。触发词：视频生成怎么开始、文生视频用哪个技能、图生视频怎么选、ComfyUI 视频、FastH3、Seedance、视频能力地图。
whenToUse: 当不确定该用哪个视频生成技能、需要总览能力地图或选择本地 ComfyUI 与云端 Ark 路径时使用。确定任务后加载具体的技能目录（如 text-to-video-fastvideo3/SKILL.md）或方法手册（../methods/）。
---

# 视频生成技能总览（Skills Index）

> 返回[首页](../README.md) ｜ 技术方法手册见 [../methods/](../methods/README.md) ｜ 项目实践见 [../projects/](../projects/README.md)

> 本目录是**技能库**：每个子目录一个技能，入口为 `SKILL.md`（YAML frontmatter 含 `name` / `description` / `whenToUse`），
> 且都带**可执行脚本 + 工作流资产**，讲"**怎么跑起来**"。
> [../methods/](../methods/README.md) 是**技术方法手册**（云端 Ark / Seedance 路径、镜头运镜、长视频续接等），讲"**怎么生成**"。

---

## 一、快速选路

**你手里有什么、在哪跑，就加载哪个技能：**

| 你手里有 / 条件 | 走哪条路 |
|------------------|----------|
| 只有文字，且要**带同步音频**的短视频，本机 ComfyUI 空闲 | [text-to-video-fastvideo3](text-to-video-fastvideo3/SKILL.md) |
| 有**一张静图**，要它动起来（首帧/可选尾帧），本机 ComfyUI 空闲 | [image-to-video-fastvideo3](image-to-video-fastvideo3/SKILL.md) |
| 只有文字，要云端托管、要 1080p / 长时长 / 快速返回 | [../methods/text-to-video](../methods/text-to-video/README.md)（方舟 Seedance） |
| 有一张图做首帧，要云端出片 | [../methods/image-to-video](../methods/image-to-video/README.md) |
| 有参考视频要模仿运镜/风格 | [../methods/reference-video](../methods/reference-video/README.md) |
| 要口型/配音驱动 | [../methods/audio-driven](../methods/audio-driven/README.md) |
| 要控制镜头运动 | [../methods/cinematography](../methods/cinematography/README.md) |

**两条路的取舍**：

| 维度 | 本地 ComfyUI（本技能库） | 云端 Ark Seedance（methods） |
|------|--------------------------|------------------------------|
| 成本 | 自有显卡电费，可无限重跑 | 按量计费 |
| 速度 | **实测约 3 分钟一条**（576×736 / 56 帧：t2v 165 s、i2v 180 s、i2v+尾帧 195 s）<br>权重 35 GB 压 8 GB 显存会流式换页，但实测换页不是瓶颈 | 快 |
| 音频 | **原生同步生成**（t2va / fl2va，音视频一次出），实测 AAC 32 kHz 双声道 | 需显式开 `generate_audio`，效果有坑 |
| 画幅 | 短边 768、上限 768×1344、32 倍数；**图生视频的画幅跟随输入图** | 480p–1080p、多种比例 |
| 输入条件 | 纯文生（t2va）+ 首帧/尾帧（fl2va，**实测可用**）；多参考（Ref2VA）未蒸馏 | 文生 / 图生 / 参考视频 / 音频驱动 |
| 适合 | 反复试 prompt、要音画同出、不赶时间 | 出成品、要高清、要多种输入路径 |

---

## 二、技能地图

```
skills/
├── README.md                       ← 你在这里（技能索引）
│
└── 🎬 出片（本地 ComfyUI · 同一套 FastH3 权重）
    ├── text-to-video-fastvideo3/     文生视频 + 同步音频（纯文本，t2va）
    │   ├── SKILL.md                  技能入口
    │   ├── assets/                   工作流 JSON + 参数 profile
    │   ├── references/               prompt 写法（分镜 / 音效 / 配乐）
    │   └── scripts/                  命令行引擎 + 离线自检 + 共享引擎定位
    └── image-to-video-fastvideo3/    图生视频 + 同步音频（首帧/尾帧，fl2va）
        ├── SKILL.md                  技能入口
        ├── assets/                   工作流 JSON + 参数 profile
        ├── references/               prompt 写法（<Picture 1> 引用句等）
        └── scripts/                  命令行引擎 + 离线自检 + 共享引擎定位
```

### 技能表

| 技能 | 一句话 | 输入 → 输出 |
|------|--------|-------------|
| [text-to-video-fastvideo3](text-to-video-fastvideo3/SKILL.md) | 远程 ComfyUI 跑 FastH3 文生视频 | 结构化 prompt → mp4（带音频轨） |
| [image-to-video-fastvideo3](image-to-video-fastvideo3/SKILL.md) | 远程 ComfyUI 跑 FastH3 图生视频（首帧/可选尾帧） | 1–2 张图 + prompt → mp4（带音频轨） |

> ⚠️ 两者共用同一套 35 GB 权重，**不能同时跑**。
> 目前技能库只有本地 ComfyUI 这一条可执行路径。云端 Ark / Seedance 的各种生成方式按"方法"组织，
> 一方法一篇，见 [../methods/README.md](../methods/README.md)。
