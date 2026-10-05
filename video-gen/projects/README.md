# 项目（Projects）

> 返回[首页](../README.md) ｜ 技术方法见 [../methods/](../methods/README.md)

---

## 一、本目录是什么

按**具体项目**组织：**一项目一目录**，每个项目目录下一个 `README.md` 作为该项目的视频生成规划。

与 [methods/](../methods/README.md) 的区别：

| | methods/ | projects/（本目录） |
|---|----------|---------------------|
| 回答 | **怎么生成**（技术） | **生成什么**（业务） |
| 组织 | 按技术方法分目录，可复用 | 按项目分目录，一次性规划 |
| 关系 | 被项目引用 | 引用 methods |

一个项目按需挑选若干 methods 组合，落地为具体的一批视频交付物。

---

## 二、建项目规范

### 目录命名

- 小写英文 + 连字符，体现项目特征：`product-launch-2026q3/`、`spring-festival-greeting/`、`brand-intro/`
- 一个项目 = 一个独立交付目标（一批视频 + 一个规划）

### 项目 README 应包含

| 章节 | 内容 |
|------|------|
| 项目背景 | 为什么要做、给谁看、发布在哪 |
| 交付物清单 | 每条视频的用途、时长、比例 |
| 方法选型 | 每条视频用哪个方法（链接到 methods/） |
| 分镜表 | 多镜头项目的镜号/景别/运镜/内容 |
| Prompt & 参数 | 每条视频的 prompt、模型、关键参数 |
| 执行计划 | 定向/定型/定稿阶段安排 |
| 产出记录 | task_id、local_path、版本 |
| 检查清单 | 上线前核对项 |

### 新建项目

```bash
cd video-gen/projects
cp -r _template <your-project>
# 编辑 <your-project>/README.md
```

---

## 三、项目列表

| 项目 | 说明 | 状态 |
|------|------|------|
| [_template/](_template/README.md) | 项目模板（复制即用，勿直接用） | 模板 |
| [survival-island/](survival-island/README.md) | 荒岛求生：6 镜 30s 剧情短片，18 岁东方少女 × 极致反差（荒岛不荒、人更惨） | 规划中 |
| [tea-shake-dance/](tea-shake-dance/README.md) | 来杯好茶摇一摇：艺术舞蹈短片，以「摇一摇」为动作母题，茶文化跳成现代舞（6 镜逐镜详解已细化） | 规划中 |
| [step-scenery/](step-scenery/README.md) | 移步换景：少女穿越时空，一步一世界（茶室→竹林→沙漠→赛博→星空→雪原→茶室闭环） | 规划中 |
| [step-scenery-v2/](step-scenery-v2/README.md) | 移步换景 v2：同故事，seedance-2.0 原生音频版（每镜自带场景音效） | 规划中 |
| [giant-kingdom/](giant-kingdom/README.md) | 穿越到巨人女儿国：体型反差视觉奇观（巨手遮天/掌心如地/一肩一世界） | 规划中 |

> 新项目在此追加一行。

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-07-18 | v1.0 | 顶层重构新增 projects/，建立项目制与模板 | 小七 |
| 2026-08-01 | v1.1 | 新增项目 tea-shake-dance（艺术舞蹈短片） | 小七 |
| 2026-08-01 | v1.2 | 新增项目 step-scenery（少女穿越时空·移步换景） | 小七 |
| 2026-08-01 | v1.3 | 新增项目 step-scenery-v2（移步换景 v2，seedance-2.0 原生音频版） | 小七 |
| 2026-08-01 | v1.4 | 新增项目 giant-kingdom（穿越到巨人女儿国，体型反差视觉奇观） | 小七 |
