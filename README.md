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
│   ├── skills/            12 个技能，每目录一个 SKILL.md
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
| 用文字出一张图 | [image-gen/skills/text-to-image-comfyui](image-gen/skills/text-to-image-comfyui/SKILL.md)（本机 ComfyUI）或 [text-to-image](image-gen/skills/text-to-image/SKILL.md)（方舟云端） |
| 按控制图改图 / 换背景 | [image-gen/skills/image-edit-comfyui](image-gen/skills/image-edit-comfyui/SKILL.md)、[image-editing](image-gen/skills/image-editing/SKILL.md) |
| 多图参考融合、多视角一致 | [multi-image-reference](image-gen/skills/multi-image-reference/SKILL.md)、[multi-view-consistency](image-gen/skills/multi-view-consistency/SKILL.md) |
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
| ComfyUI HTTP API（`192.168.3.5:18000`，远程 Windows + RTX 4060 Ti 8 GB） | 本地文生图 / 图生图 / 视频（Z-Image-Turbo、fastvideo3） |
| `arkcli`（火山方舟） | 云端 Seedream 图片、Seedance 视频、TTS/ASR |
| `ffmpeg` | 图片编解码、接触印相、合图、视频拼接 |
| Python 3 + Pillow / numpy | 评分、逐像素差分、图集生成 |

> ⚠️ **路径说明**：文档中出现的 `/home/usb/wks/gits/Book/image-gen/...` 之类的绝对路径，是作者工作机的目录布局；在本仓库中对应 `image-gen/...`、`video-gen/...`。各文档之间的相对链接在本仓库内均有效。

---

## 六、体积与来源

- **来源**：`gits` 仓库（Gitee）提交 `b1e14ad` 的 `Book/image-gen` + `Book/video-gen`。
- **导入方式**：`git archive` 导出已跟踪文件（自动排除被忽略的中间产物）→ 提到仓库根 → 单次初始提交。原仓库仍保留同样的内容。
- **不含**：`work/` 等中间产物与半成品轮次 —— 它们是**确定性的**，用固定 seed 可逐像素复现，因此不入库。
- **体积**：1059 文件 / 约 550 MB，单文件最大约 13 MB（视频成品 `.mp4`），**未使用 Git LFS**（所有文件都远低于 GitHub 的 100 MB 单文件上限）。
- **图片规范**：定稿与对照图用 PNG（无损、去元数据），合并图 / 审计图用 JPEG（控制体积）。

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v1.0 | 从 `gits` 拆出 `Book/image-gen` 与 `Book/video-gen`，独立成库 | 小七 |
