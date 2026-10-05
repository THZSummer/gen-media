# gen-media · 生成式媒体

> **图片生成**（ComfyUI 本地 + 火山方舟 Seedream 云端）与**视频生成**（Seedance / 本地 fastvideo3）的知识库与作品集。
> 本仓库是工作区 `gits` 中 `Book/image-gen` 与 `Book/video-gen` 两个库的独立归档：以 `git archive` 导出已跟踪文件后重建为**单次初始提交**，因此不保留原仓库的提交历史。

---

## 一、目录

```
gen-media/
├── README.md          ← 你在这里（总入口）
├── image-gen/         图片生成：技能线 + 项目线 + 成品图      （824 文件 / 约 435 MB）
│   ├── README.md          图片库总导航
│   ├── skills/            3 个可执行技能（文生图 / 控制图生图 / 确定性图像工具）
│   └── projects/          bio-splice、bone-china-doll、character-lookbook、_template
└── video-gen/         视频生成：方法 + 技能 + 项目 + 成品视频  （235 文件 / 约 114 MB）
    ├── README.md          视频库总导航
    ├── methods/           10 篇方法手册（文生视频 / 图生视频 / 参考视频 / 音频驱动 / 运镜 …）
    ├── skills/            本地 ComfyUI 可执行技能（fastvideo3 t2va / fl2va）
    └── projects/          giant-kingdom、step-scenery、step-scenery-v2、survival-island、tea-shake-dance
```

合计 **1059 个文件 / 约 550 MB**。

---

## 二、入口

| 我想… | 去哪 |
|------|------|
| 用文字出一张图 | [image-gen/skills/text-to-image-comfyui](image-gen/skills/text-to-image-comfyui/SKILL.md)（本机 ComfyUI：Z-Image-Turbo 快 / Qwen-Image 细） |
| 按控制图改图 / 换背景 | [image-gen/skills/image-edit-comfyui](image-gen/skills/image-edit-comfyui/SKILL.md)（Fun Union ControlNet） |
| 合图 / 比对两张图 / 去元数据 / 缩放裁切 | [image-gen/skills/image-tools](image-gen/skills/image-tools/SKILL.md)（不用 AI，确定性） |
| 看一个完整图片项目的规划与成品 | [image-gen/projects/](image-gen/projects/README.md) |
| 从分镜图生成视频 | [video-gen/skills/image-to-video-fastvideo3](video-gen/skills/image-to-video-fastvideo3/SKILL.md) |
| 纯文字生成带音频的视频 | [video-gen/skills/text-to-video-fastvideo3](video-gen/skills/text-to-video-fastvideo3/SKILL.md) |
| 查视频技术方法与成本 | [video-gen/methods/](video-gen/methods/README.md) |

---

## 三、两个库的分工

| 库 | 回答 | 组织方式 |
|----|------|----------|
| [image-gen](image-gen/README.md) | **生成什么图 / 怎么生成图** | 技能（技术路径）× 项目（具体业务） |
| [video-gen](video-gen/README.md) | **怎么把图变成视频 / 怎么直接生成视频** | 方法手册 × 可执行技能 × 项目 |

图片是视频的前置工序：`image-gen` 出的分镜图 / 首帧，在 `video-gen` 里被 I2V 技能消费。反之，`video-gen` 的 `methods/text-to-image/` 与 `image-gen` 有历史重叠（视频库从图片能力拆出独立成库）。

---

## 四、代表项目：bio-splice（生物拼接）

跨物种、跨界的"部位移植"图像实验系列，是目前规模最大的一个项目：

- **12 个子主题 × 5 期 = 60 期，135 张定稿**（cat-eagle、dragon-nines、turtle-snake、fish-bird、deer-crane、lichen、cordyceps、flytrap-fang、flower-bird、tree-beast、wing-atlas、horn-atlas）
- 引擎 **Z-Image-Turbo**（ComfyUI，1024² / 1280²，12 步，约 25 秒/张）
- 每轮必带同轮**底座对照图**；定稿只收 A–E 五维评分过关的图；累计 **110 条机制结论**（选题 / 写法 / 排布 / 呈现 / 流程）
- 入口：[image-gen/projects/bio-splice/README.md](image-gen/projects/bio-splice/README.md) ｜ 全线总结与 12 张子主题合图：[SUMMARY.md](image-gen/projects/bio-splice/SUMMARY.md)

---

## 五、运行前提

| 依赖 | 用途 |
|------|------|
| ComfyUI HTTP API（`192.168.3.5:18000`，远程 Windows + RTX 4060 Ti 8 GB） | 图片文生图 / 图生图、视频（Z-Image-Turbo、Qwen-Image、Fun Union ControlNet、fastvideo3） |
| `ffmpeg` | 图片编解码、接触印相、合图、去元数据、视频拼接 |
| Python 3 + numpy | 评分、逐像素差分、图集生成（`image-tools` 不需要 Pillow） |
| `arkcli`（火山方舟） | **仅视频库在用**：Seedance 视频、TTS/ASR（图片侧的云端文档技能已于 2026-10-05 移除） |

> 📌 **路径约定**：所有文档里的路径都以仓库根为基准（如 `image-gen/skills/...`、`video-gen/projects/...`）。
> 2026-10-05 已把残留的旧绝对路径（`/home/usb/wks/gits/Book/...`，该布局已废弃）全部改为相对路径，可直接复制执行。

---

## 六、体积与来源

- **来源**：`gits` 仓库（Gitee）提交 `b1e14ad` 的 `Book/image-gen` + `Book/video-gen`。
- **导入方式**：`git archive` 导出已跟踪文件（自动排除被忽略的中间产物）→ 提到仓库根 → 单次初始提交。
- **原仓库已不再包含这部分内容**：`gits` 的索引与历史已用 `filter-branch` 重写摘除这两个目录（1059 个文件 / 168→69 提交），本地工作副本也已删除。**本仓库是这些内容的唯一副本。**
- **不含**：`work/` 等中间产物与半成品轮次 —— 它们是**确定性的**，用固定 seed 可逐像素复现，因此不入库。工作机上的这些中间产物已随目录一并清理：图类可用固定 seed 复现；`video-gen` 的旧版中间视频属已废弃版本（定稿均在本仓库），未另存。
- **体积**：1059 文件 / 约 550 MB，单文件最大约 13 MB（视频成品 `.mp4`），**未使用 Git LFS**（所有文件都远低于 GitHub 的 100 MB 单文件上限）。
- **图片规范**：定稿与对照图用 PNG（无损、去元数据），合并图 / 审计图用 JPEG（控制体积）。

---

## 七、维护与扩展

**本仓库就是内容源头**，不再有上游：新增技能 / 项目直接在 `image-gen/`、`video-gen/` 下建目录，按各自 `README.md` 的规范组织，然后正常 `git commit` + `git push` 即可。

| 想加什么 | 放哪 | 参考规范 |
|----------|------|----------|
| 新图片项目 | `image-gen/projects/<项目名>/` | 复制 `image-gen/projects/_template/`；索引见 `image-gen/projects/README.md` |
| 新图片技能 | `image-gen/skills/<技能名>/SKILL.md` | 技能索引见 `image-gen/skills/README.md` |
| 新视频项目 / 方法 / 技能 | `video-gen/{projects,methods,skills}/` | 见 `video-gen/README.md` |

> 大体积中间产物（`work/`、`out/r*/`、逐镜头 mp4 等）仍按各目录的 `.gitignore` 约定**不入库**；定稿只保留成品与文档，必要时用固定 seed 复现。

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v1.0 | 从 `gits` 拆出 `Book/image-gen` 与 `Book/video-gen`，独立成库 | 小七 |
| 2026-10-05 | v1.1 | 新增 `tools/sync-from-gits.sh` 与「维护」章节 | 小七 |
| 2026-10-05 | v1.2 | 原 `gits` 工作副本与历史均已清理，本仓库成为唯一副本；删除已失效的同步脚本，「维护」章节改写为「维护与扩展」 | 小七 |
