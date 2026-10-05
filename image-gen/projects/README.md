# 项目（Projects）

> 返回[首页](../README.md) ｜ 技术技能见 [../skills/](../skills/README.md)

---

## 一、本目录是什么

按**具体项目**组织：**一项目一目录**，每个项目目录下一个 `README.md` 作为该项目的图片生成规划。

与 [skills/](../skills/README.md) 的区别：

| | skills/ | projects/（本目录） |
|---|----------|---------------------|
| 回答 | **怎么生成**（技术） | **生成什么**（业务） |
| 组织 | 按技术路径分目录，每目录一个 `SKILL.md`，可复用 | 按项目分目录，一次性规划 |
| 关系 | 被项目引用 | 引用 skills |

一个项目按需挑选若干**技能**组合，落地为具体的一批图片交付物。

---

## 二、建项目规范

### 目录命名

- 小写英文 + 连字符，体现项目特征：`character-lookbook/`、`poster-2026q4/`、`brand-assets/`
- 一个项目 = 一个独立交付目标（一批图片 + 一个规划）

### 项目 README 应包含

| 章节 | 内容 |
|------|------|
| 项目背景 | 为什么要做、给谁看、用在哪 |
| 交付物清单 | 每张图的用途、尺寸、比例 |
| 技能选型 | 每张图用哪个技能（链接到 skills/） |
| 图片清单 | 图号/主体/场景/视角/风格 |
| Prompt & 参数 | 每张图的 prompt、模型、关键参数、seed |
| 执行计划 | 定向/定型/定稿阶段安排 |
| 产出记录 | 模型、seed、local_path、版本 |
| 检查清单 | 交付前核对项 |

### 新建项目

```bash
cd /home/usb/wks/gits/Book/image-gen/projects
cp -r _template <your-project>
# 编辑 <your-project>/README.md
```

---

## 三、项目列表

| 项目 | 说明 | 状态 |
|------|------|------|
| [_template/](_template/README.md) | 项目模板（复制即用，勿直接用） | 模板 |
| [character-lookbook/](character-lookbook/README.md) | 角色设定图库：一个角色的正面/侧面/背面/多场景/多装扮设定图，供视频与设计复用 | 规划中 |
| [bone-china-doll/](bone-china-doll/README.md) | **骨瓷国公主**：R1–R29 迭代。一阶段 R1–R6（Z-Image-Turbo）；二阶段 R7–R16（Qwen-Image 2512，质量高地 R8–R10，定稿 R10 `window-light`，R11/R12 为已定位退化轮）；三阶段 R17–R21 **主题变更为东方古典美女**；四阶段 R22–R26 **去摆件化 + 半真半骨瓷**（活人公主、釉光+真人血色、具名釉面缺陷、半纱半骨瓷轻纱）；**五阶段 R27–R29 自然妆容 + 慵懒生活姿态**（全身的坐/卧/半躺日常瞬间），当前交付集 `out/final-set-life/` | 迭代中 |
| [bio-splice/](bio-splice/README.md) | **生物拼接**：把 A 的**器官**接到 B 的身上，用纪实摄影（或显微/标本）的写实语言拍出来。**不限于动物**——植物、真菌、藻类、地衣都可作底座或供体。结构 = 项目 → 子主题（按**生物组合**分，共 **12 个**）→ **期**（每子主题 5 期，只放成品）。规划见 [PLAN.md](bio-splice/PLAN.md)；**已全部交付：12 个子主题 / 60 期 / 135 成品**（总结见 [SUMMARY.md](bio-splice/SUMMARY.md)），每期与每子主题各有合并图 | 迭代中（规划先行） |

> 新项目在此追加一行。

---

## 四、与 video-gen 的关系

图片项目常作为 [video-gen](../../video-gen/projects/README.md) 项目的前置工序：

```
image-gen/projects/<project>/out/storyboard/  ──►  video-gen/projects/<project>/（I2V 成片）
```

- 同一题材可两边各有一个项目目录（图片规划 + 视频规划），通过 `out/` 产物对接
- 分镜图/T2I 首帧在 image-gen 完成并审核，视频端只负责"动起来"

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-02 | v1.0 | 新建项目制与模板，收录 character-lookbook 示例项目 | 小七 |
| 2026-10-02 | v1.1 | 随 `methods/`→`skills/` 改组：术语改为"技能"，链接指向 skills/ | 小七 |
| 2026-10-02 | v1.2 | 新增项目 bone-china-doll（骨瓷娃娃，6 轮迭代已完成） | 小七 |
