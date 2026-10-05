# 第三期 · 皮角俱全

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/tb-r8-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**seed 12101 / 12102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**雨后林 · 硬光 · 横 1280×1024**

雨后硬光把湿树皮与兽皮的反光差拉开；横幅把"树干 + 角 + 树根"完整收进画面。

## 二、本期主题与结果

**底座 ＝ 老树（腾出树皮）**　**移植件 ＝ 兽皮纹 K1 + 兽角 K4**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 兽皮纹 | K1 | 树皮（属性） | ✅ 成立 |
| 兽角 | K4 | 树干（空面） | ✅ 完整成立 |
| 两件同体 | K1+K4 | 材质 + 表面 | ✅ 互不抢占（一个是材质替换、一个是新增结构） |

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-tree-hide-horns.png`](01-tree-hide-horns.png) | **5.00** ✅ 首选 | `8f9cce53` | `b759f03394` |
| 2 | [`02-tree-hide-horns-b.png`](02-tree-hide-horns-b.png) | **5.00** ✅ 首选 | `5c2dcfda` | `3e21a80c7c` |

对照：[`controls/tree.png`](controls/tree.png) —— **同轮**的纯树底座。

## 四、本期验证

1. **"材质替换"与"新增结构"不冲突**：一个改的是表面的材质（属性），
   一个加的是表面之上的结构（空面）——所以两件可以同时成立。
2. 期身份靠光线与画幅（雨后硬光 + 横幅）与前两期区分开。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject tree-beast 8 --dry
python3 run_round.py --subject tree-beast 8
python3 score.py --round work/tree-beast/r8/round.json --scores work/tree-beast/r8/scores.json \
    --control base-tree --region trunk=300,150,680,600 \
    --audit-sheet subjects/tree-beast/rounds/tb-r8-audit.jpg \
    --subject tree-beast -o subjects/tree-beast/rounds/tb-r8-review.md
python3 curate.py --period subjects/tree-beast/period-03 --from work/tree-beast/r8/round.json \
    --pick tree-hide-horns=01-tree-hide-horns --pick tree-hide-horns-b=02-tree-hide-horns-b \
    --control base-tree=controls/tree --note "…" --force
bash make_sheet.sh period subjects/tree-beast/period-03
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第三期【皮角俱全】交付 2 张（全部首选） | 小七 |
