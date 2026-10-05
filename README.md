# gen-media · 生成式媒体

> 🌐 语言：**中文** ｜ [English](README.en.md)

> **图片生成**（本机 ComfyUI：Z-Image-Turbo / Qwen-Image / Fun Union ControlNet）与**视频生成**（本地 FastVideo FastH3；云端 Seedance 走 `arkcli`）的知识库与作品集。
>
> 🗂️ **扁平化结构（2026-10-05）**：不再分 `image-gen/` 与 `video-gen/` 两个库，改为按**内容类型**分三块——`.agents/skills/`（技能）、`projects/`（项目）、`methods/`（视频方法手册）。图片与视频技能现在**同处一个技能库**。

---

## 一、目录

```
gen-media/
├── README.md          ← 你在这里（总入口）
├── .agents/skills/    技能库：dev-guide（开发规范总纲）+ 5 个可执行技能，图片与视频不分家
│   ├── README.md          技能索引（能力地图 + 选路表 + 运行前提与自检）
│   ├── dev-guide/                仓库开发规范总纲：新增/修改任何内容前先加载
│   ├── text-to-image-comfyui/    文生图：Z-Image-Turbo（快）+ Qwen-Image（细）
│   ├── image-edit-comfyui/       控制图生图：Z-Image Fun Union ControlNet
│   ├── image-tools/              确定性图像工具（不用 AI）：速览图/比对/剥元数据/缩放
│   ├── text-to-video-fastvideo3/ 文生视频 + 同步音频（t2va）
│   └── image-to-video-fastvideo3/ 图生视频 + 同步音频（fl2va，首帧/尾帧）
├── projects/          项目库：9 个项目，一项目一目录（图片与视频同处一处）
│   ├── README.md          项目索引 + 建项目规范
│   ├── _template/         项目模板（复制即用，图片/视频共用）
│   ├── bio-splice/ bone-china-doll/ character-lookbook/ shanhai-jing/     （图片）
│   └── giant-kingdom/ step-scenery/ step-scenery-v2/ survival-island/ tea-shake-dance/  （视频）
├── methods/           视频方法手册：10 篇（云端 Ark Seedance 为主）
├── site/              画廊前端（双语）：app.css / app.js / data/*.json
└── tools/             工具链：build_site.py、preview.sh、i18n.py
```

---

## 二、入口

| 我想… | 去哪 |
|------|------|
| **给这个仓库加东西 / 提交前对齐规范** | [`.agents/skills/dev-guide/SKILL.md`](.agents/skills/dev-guide/SKILL.md)（双语、站点、技能、生成、资产、协作六类规范 + 检查脚本） |
| 用文字出一张图 | [.agents/skills/text-to-image-comfyui](.agents/skills/text-to-image-comfyui/SKILL.md)（Z-Image-Turbo 快 / Qwen-Image 细） |
| 按控制图改图 / 换背景 | [.agents/skills/image-edit-comfyui](.agents/skills/image-edit-comfyui/SKILL.md)（Fun Union ControlNet） |
| 合图 / 比对两张图 / 去元数据 / 缩放裁切 | [.agents/skills/image-tools](.agents/skills/image-tools/SKILL.md)（不用 AI，确定性） |
| 纯文字生成带音频的视频 | [.agents/skills/text-to-video-fastvideo3](.agents/skills/text-to-video-fastvideo3/SKILL.md)（本地 FastH3） |
| 从分镜图生成视频 | [.agents/skills/image-to-video-fastvideo3](.agents/skills/image-to-video-fastvideo3/SKILL.md)（本地 FastH3） |
| 查视频技术方法与成本（云端） | [methods/](methods/README.md) |
| 看一个完整项目的规划与成品 | [projects/](projects/README.md) |
| 挑技能 / 确认环境健康 | [.agents/skills/README.md](.agents/skills/README.md)（选路表 + 每个技能一条自检命令） |

---

## 三、三块的分工

| 块 | 回答 | 组织方式 |
|----|------|----------|
| [.agents/skills/](.agents/skills/README.md) | **怎么做**（可执行技术） | 一技能一目录，带 `SKILL.md` + 脚本 + 自检入口；**只收能在真机跑通的** |
| [projects/](projects/README.md) | **做什么**（具体业务） | 一项目一目录，一次性规划，引用 skills / methods |
| [methods/](methods/README.md) | **怎么生成**（视频技术手册，云端为主） | 一方法一目录，可复用 |

一个**项目**按需挑选若干**技能**或**方法**组合完成：例如生物拼接 = 文生图（Z-Image-Turbo 逐轮出图）+ 确定性工具（合图 / 逐像素比对 / 评分佐证）。
图片项目常是视频项目的前置工序：分镜图 / 首帧在 `projects/<图片项目>/out/` 产出，被 `image-to-video-fastvideo3` 消费。

---

## 四、代表项目：bio-splice（生物拼接）

跨物种、跨界的"部位移植"图像实验系列，是目前规模最大的一个项目：

- **12 个子主题 × 5 期 = 60 期，135 张定稿**（cat-eagle、dragon-nines、turtle-snake、fish-bird、deer-crane、lichen、cordyceps、flytrap-fang、flower-bird、tree-beast、wing-atlas、horn-atlas）
- 引擎 **Z-Image-Turbo**（ComfyUI，1024² / 1280²，12 步，约 25 秒/张）
- 每轮必带同轮**底座对照图**；定稿只收 A–E 五维评分过关的图；累计 **110 条机制结论**
- 入口：[projects/bio-splice/README.md](projects/bio-splice/README.md) ｜ 全线总结与 12 张子主题合图：[SUMMARY.md](projects/bio-splice/SUMMARY.md)

另一个值得看的是 [projects/shanhai-jing](projects/shanhai-jing/README.md)：把八轮过程（含三次失败迭代与一次路线推翻）完整留档的项目。

---

## 五、运行前提

| 依赖 | 用途 |
|------|------|
| ComfyUI HTTP API（`192.168.3.5:18000`，远程 Windows + RTX 4060 Ti 8 GB） | 图片文生图 / 图生图、视频（Z-Image-Turbo、Qwen-Image、Fun Union ControlNet、FastH3） |
| `ffmpeg` | 图片编解码、接触印相、合图、去元数据、视频拼接 |
| Python 3 + numpy | 评分、逐像素差分、图集生成（`image-tools` 不需要 Pillow） |
| `arkcli`（火山方舟） | **仅 `methods/` 在用**：Seedance 视频、TTS/ASR |

> 📌 **路径约定**：所有文档里的路径都以仓库根为基准（如 `.agents/skills/...`、`projects/...`），可直接复制执行。
> 改完环境先跑 `.agents/skills/README.md` 里每个技能的自检命令，再谈出图出片。

---

## 六、体积与来源

- **来源**：`gits` 仓库（Gitee）的 `Book/image-gen` + `Book/video-gen`。
- **导入方式**：`git archive` 导出已跟踪文件（自动排除被忽略的中间产物）→ 提到仓库根 → 单次初始提交。
- **`gits` 现在以 submodule 引用本仓库**：`.gitmodules` 里的 `GitHub/gen-media`（branch `main`）——**存的是指针，不是副本**。原目录内容已从 `gits` 的历史中摘除（1059 个文件 / 168→69 提交）。
- **不含**：`work/` 等中间产物与半成品轮次 —— 它们是**确定性的**，用固定 seed 可逐像素复现，因此不入库。
- **体积**：单文件最大约 13 MB（视频成品 `.mp4`），**未使用 Git LFS**。
- **图片规范**：定稿与对照图用 PNG（无损、去元数据），合并图 / 审计图用 JPEG（控制体积）。

---

## 七、维护与扩展

**本仓库就是内容源头**：新增技能 / 项目 / 方法直接在 `.agents/skills/`、`projects/`、`methods/` 下建目录，按各自 `README.md` 的规范组织。

| 想加什么 | 放哪 | 参考规范 |
|----------|------|----------|
| 新技能 | `.agents/skills/<技能名>/SKILL.md` | [.agents/skills/README.md](.agents/skills/README.md)；只收带脚本、有自检入口、真机跑通的 |
| 新项目 | `projects/<项目名>/` | 复制 `projects/_template/`；索引见 [projects/README.md](projects/README.md) |
| 新视频方法 | `methods/<方法名>/` | 见 [methods/README.md](methods/README.md) |

### 提交与协作（含 submodule 指针）

```bash
# 1) 本仓库
git add -A && git commit -m "<做了什么 + 验证证据>" && git push

# 2) 回父仓库 gits 推进 submodule 指针（否则 gits 记的还是旧版本）
cd ../.. && git submodule update --remote GitHub/gen-media \
  && git add GitHub/gen-media \
  && git commit -m "chore(submodule): gen-media → <sha>" && git push
```

> ⚠️ **Gitee 配额**：`gits` 仓库体积已超 Gitee 的 819 MB 阈值（用量 > 80%），继续推大文件可能被硬拦。
> 大体积中间产物（`work/`、`out/r*/`、逐镜头 mp4）仍按各目录的 `.gitignore` 约定**不入库**。

---

## 八、语言版本（i18n）

**中文 `X.md` 是默认版本，英文版是同名 `X.en.md`。** 两份文件顶部各有一行语言切换链接，改文档时请**成对修改**。

| 约定 | 说明 |
|------|------|
| 命名 | `README.md` ↔ `README.en.md`；`projects/<项目>/README.md` ↔ `README.en.md` |
| 排除 | `.agents/skills/**`（含 `.agents/skills/README.md`）与 `.agents/skills/**` 只保留中文（技能文档面向执行，不翻译） |
| 链接 | 英文版内部的相对链接指向 `.en.md`；目标没有英文版时指向中文版（不造死链） |
| 代码 | **逐字保留**：命令、路径、文件名、模型 ID、参数名、seed、prompt 原文、样例字符串 |
| 代码块内的注释 | **要翻译**：目录树的说明文字、bash 示例里的 `#` 注释、ASCII 示意图的标签 |
| 工具 | `python3 tools/i18n.py status / switch / links / check` —— 覆盖报告、写切换行、改链接、体检 |

```bash
python3 tools/i18n.py status          # 还有哪些 md 缺英文版
python3 tools/i18n.py check           # 体检：缺件 / 疑似未翻译 / 英文版断链
python3 tools/i18n.py switch          # 补齐或更新两侧的语言切换行
python3 tools/i18n.py links           # 把英文版的相对链接改指 .en.md
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v1.0 | 从 `gits` 拆出 `Book/image-gen` 与 `Book/video-gen`，独立成库 | 小七 |
| 2026-10-05 | v1.3 | 新增双语规范（中文默认 + `X.en.md`）与 `tools/i18n.py` | 小七 |
| 2026-10-05 | v2.0 | **扁平化重构**：取消 `image-gen/` 与 `video-gen/` 两库划分，改为 `.agents/skills/`（5 个技能合一处）+ `projects/`（9 个项目）+ `methods/`（视频方法）；两个技能索引合并、两个项目索引与模板合并；`tools/{i18n,build_site}.py` 与 dev-guide 同步；**订正"本仓库是唯一副本、不再有上游"的失实表述**——`gits` 以 submodule 引用本仓库 | 小七 |
