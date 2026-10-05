# 玄武部位表（龟 + 蛇）

> 🌐 语言：**中文** ｜ [English](parts.en.md)

> 返回[子主题首页](README.md) ｜ [项目首页](../../README.md)

**设计源**：玄武是四象里唯一的**合体**形象——龟与蛇同体。
所以这个子主题不是我们发明拼接，而是**复刻一个已经存在的合体**。

**底座 ＝ 龟**（背甲 / 腹甲 / 短足）。
底座描述里**刻意不写颈的长短、不写尾**——把这两处腾出来（规律 66）。

---

## 一、部位表与实测

| 编号 | 部位 | 供体 | prompt 锚点（只出部位） | 龟底座上有无占位 | 实测结果 |
|------|------|------|--------------------------|------------------|----------|
| N1 | 蛇颈 | 蛇 | `a long sinuous snake's neck with fine keeled scales` | **占位可腾出**（龟有短颈） | ✅ **完整成立**（三个 seed 全成，5.00） |
| N2 | 蛇尾 | 蛇 | `a long tapering snake's tail with keeled scales` | **占位可腾出**（龟有小尾） | ✅ **完整成立**（5.00 / 4.85 / 4.55） |
| N3 | 缠体 | 蛇 | `thick snake coils around its shell` | 空位（壳上没有东西） | ✅ 成立（4.70），**但写法敏感**，见下 |
| N4 | ~~蛇头~~ | 蛇 | — | — | ⛔ **不做**：头部件不可移植（规律 73） |
| N5 | 蛇鳞 | 蛇 | `large overlapping snake scales` | 占位（壳上有盾片） | 未测（本期不需要，留作备用） |

## 二、N3 缠体：写法比占位更重要（规律 81）

N3 是"空位新增"，按规律 67 本该是最容易成的一件，**但第一轮 0% 落地**。
同一轮换三种写法，**三种全部落地**：

| 写法 | 结果 |
|------|------|
| ❌ `the thick coiled body of a large snake wrapped around its shell` | **空操作** |
| ✅ `a thick snake's body coiled on the stones beneath it, its coils visible on both sides` | ✅ |
| ✅ `thick snake coils around its shell` | ✅（最短最稳） |
| ✅ `thick snake coils around the rim of its shell` | ✅ |

> **规律 81：空间关系从句失效，改名词短语。**
> `X wrapped around Y`（关系从句 + 长定语）不会被执行；
> `X coils around Y`（名词短语 + 动词）才落地。
> 这是规律 69（复合部件要拆开写）的延伸：**部件与底座之间的空间关系也要写直白**。

## 三、底座选择与腾出占位

| 做法 | 说明 |
|------|------|
| 底座写什么 | 壳（`a dark domed shell`）+ 头（`a small wrinkled head`）+ 四肢（`four short webbed legs`） |
| 底座**不写**什么 | 颈的长短、尾——这两处要留给 N1 / N2 |
| 为什么 | 规律 56/66：底座描述里占住的部位，移植件会被覆盖；没占住的才腾得出来 |

## 四、移植件写法纪律

```
✅ a long sinuous snake's neck with fine keeled scales    ← 部位短语，安全
✅ thick snake coils around its shell                    ← 名词短语 + 动词，安全
❌ the thick coiled body of a large snake wrapped around its shell   ← 关系从句，空操作
❌ a snake's body                                          ← 整体名词，会拖出整只蛇
```

且**不给蛇头**（规律 73：头部件是双向死局）——
玄武的蛇从颈开始、到尾结束，颈与尾之间由缠体连接，**唯独没有头**。

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 玄武部位表 N1–N5 + 五期实测结果 + 规律 81（空间关系写法） | 小七 |
