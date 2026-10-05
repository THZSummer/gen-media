# 项目（Projects）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[首页](../README.md) ｜ 技能见 [../skills/](../skills/README.md) ｜ 视频方法手册见 [../methods/](../methods/README.md)

> 本目录由 `image-gen/projects/` 与 `video-gen/projects/` 合并而来（2026-10-05 扁平化）：
> **不再按图像/视频分库，一律按项目组织**。

---

## 一、本目录是什么

按**具体项目**组织：**一项目一目录**，每个项目目录下一个 `README.md` 作为该项目的生成规划。

| | [skills/](../skills/README.md) | [methods/](../methods/README.md) | projects/（本目录） |
|---|---|---|---|
| 回答 | **怎么做**（可执行技术） | **怎么生成**（方法手册） | **做什么**（具体业务） |
| 组织 | 一技能一目录，带脚本与自检 | 一方法一目录，可复用 | 一项目一目录，一次性规划 |
| 关系 | 被项目引用 | 被项目引用 | 引用 skills / methods |

一个项目按需挑选若干**技能**（出图/出片）或**方法**（云端视频）组合，落地为具体的一批交付物。

---

## 二、建项目规范

### 目录命名

- 小写英文 + 连字符，体现项目特征：`character-lookbook/`、`product-launch-2026q3/`、`brand-intro/`
- 一个项目 = 一个独立交付目标（一批图片/视频 + 一个规划）

### 项目 README 应包含

| 章节 | 内容 |
|------|------|
| 项目背景 | 为什么要做、给谁看、用在哪 / 发布在哪 |
| 交付物清单 | 每件成品的用途、尺寸或时长、比例 |
| 技能 / 方法选型 | 每件成品用哪个技能或方法（链接到 skills/ 或 methods/） |
| 图片清单 / 分镜表 | 图号或镜号 / 主体 / 场景 / 视角 / 风格（图片）；镜号 / 景别 / 运镜 / 内容（视频） |
| Prompt & 参数 | 每件成品的 prompt、模型、关键参数、seed |
| 执行计划 | 定向 / 定型 / 定稿阶段安排 |
| 产出记录 | 模型、seed、prompt_id 或 task_id、local_path、版本 |
| 检查清单 | 交付前核对项 |

### 新建项目

```bash
cd projects
cp -r _template <your-project>
# 编辑 <your-project>/README.md（并补 README.en.md）
```

---

## 三、项目列表

| 项目 | 类型 | 说明 | 状态 |
|------|------|------|------|
| [_template/](_template/README.md) | 模板 | 项目模板（复制即用，勿直接用） | 模板 |
| [bio-splice/](bio-splice/README.md) | 图片 | **生物拼接**：把 A 的**器官**接到 B 的身上，用纪实摄影（或显微/标本）的写实语言拍出来。**不限于动物**——植物、真菌、藻类、地衣都可作底座或供体。结构 = 项目 → 子主题（按**生物组合**分，共 **12 个**）→ **期**（每子主题 5 期，只放成品）。规划见 [PLAN.md](bio-splice/PLAN.md)；**已全部交付：12 个子主题 / 60 期 / 135 成品**（总结见 [SUMMARY.md](bio-splice/SUMMARY.md)），每期与每子主题各有合并图 | 迭代中（规划先行） |
| [bone-china-doll/](bone-china-doll/README.md) | 图片 | **骨瓷国公主**：R1–R29 迭代。一阶段 R1–R6（Z-Image-Turbo）；二阶段 R7–R16（Qwen-Image 2512，质量高地 R8–R10，定稿 R10 `window-light`，R11/R12 为已定位退化轮）；三阶段 R17–R21 **主题变更为东方古典美女**；四阶段 R22–R26 **去摆件化 + 半真半骨瓷**；**五阶段 R27–R29 自然妆容 + 慵懒生活姿态**，当前交付集 `out/final-set-life/` | 迭代中 |
| [character-lookbook/](character-lookbook/README.md) | 图片 | 角色设定图库：一个角色的正面/侧面/背面/多场景/多装扮设定图，供视频与设计复用 | 规划中 |
| [shanhai-jing/](shanhai-jing/README.md) | 图片 | **山海经 · 图赞**：以《山海经》原文为纲的图赞连载，一兽一期，标注**卷次 + 原文 + 郭璞注**。面向小红书竖版（3:4）。规划见 [PLAN.md](shanhai-jing/PLAN.md)；定调期九尾狐已交付（R1–R8 全过程留档） | 定调期完成 |
| [survival-island/](survival-island/README.md) | 视频 | 荒岛求生：6 镜 30s 剧情短片，18 岁东方少女 × 极致反差（荒岛不荒、人更惨） | 规划中 |
| [tea-shake-dance/](tea-shake-dance/README.md) | 视频 | 来杯好茶摇一摇：艺术舞蹈短片，以「摇一摇」为动作母题，茶文化跳成现代舞（6 镜逐镜详解已细化） | 规划中 |
| [step-scenery/](step-scenery/README.md) | 视频 | 移步换景：少女穿越时空，一步一世界（茶室→竹林→沙漠→赛博→星空→雪原→茶室闭环） | 规划中 |
| [step-scenery-v2/](step-scenery-v2/README.md) | 视频 | 移步换景 v2：同故事，seedance-2.0 原生音频版（每镜自带场景音效） | 规划中 |
| [giant-kingdom/](giant-kingdom/README.md) | 视频 | 穿越到巨人女儿国：体型反差视觉奇观（巨手遮天/掌心如地/一肩一世界） | 规划中 |

> 新项目在此追加一行。

---

## 四、图片与视频的衔接

图片项目常作为视频项目的前置工序，两边通过 `out/` 产物对接：

```
projects/<图片项目>/out/storyboard/  ──►  projects/<视频项目>/（I2V 成片）
```

- 同一题材可两边各有一个项目目录（图片规划 + 视频规划），通过 `out/` 对接
- 分镜图 / T2I 首帧在图片项目里完成并审核，视频端只负责「动起来」
- 比例要对齐：图片成品比例需与目标视频一致，否则要重出

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-02 | v1.0 | image-gen 侧：新建项目制与模板，收录 character-lookbook 示例项目 | 小七 |
| 2026-08-01 | v1.4 | video-gen 侧：项目制与模板，累计 5 个视频项目 | 小七 |
| 2026-10-05 | v1.5 | image-gen 侧：新增项目 bone-china-doll；随后新增 shanhai-jing | 小七 |
| **2026-10-05** | **v2.0** | **扁平化合并**：`image-gen/projects/README.md` 与 `video-gen/projects/README.md` 合并为本文件；目录迁至仓库根 `projects/`；模板合并为 `_template/`；项目列表改为图像/视频统一表（9 个项目） | 小七 |
