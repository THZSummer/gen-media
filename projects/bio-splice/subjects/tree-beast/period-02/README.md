# 第二期 · 有角的树

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/tb-r4-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 12101 / 12102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**霜林 · 侧逆光 · 方**

侧逆光把霜挂在枝条上、也把角的轮廓勾出来；
本期的主角是**树干上挑着的那对弯角**，所以机位压在树干中段、让角占住画面上方。

## 二、本期主题与结果

**底座 ＝ 老树**　**移植件 ＝ 兽角 K4**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 兽角 | K4 | 树干（**空面**） | ✅ **完整成立**：一对巨大的弯角从树干长出 |

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-tree-horns.png`](01-tree-horns.png) | **5.00** ✅ 首选 | `b331b81c` | `e362d26313` |
| 2 | [`02-tree-horns-b.png`](02-tree-horns-b.png) | **5.00** ✅ 首选 | `643fe056` | `0f4d829360` |

对照：[`controls/tree.png`](controls/tree.png) —— **同轮**的纯树底座（无角）。

## 四、本期验证

1. **空面 + 不同形 + 高辨识度**：树干是空面（规律 97）、角与树形完全不同形（规律 91）——
   三条有利条件齐备，两轮 ×2 take 全成。
2. 与同轮的**兽足（0%）**形成最直接的对照：同一个底座、同一套呈现，**差别只在落点**（规律 105）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject tree-beast 4 --dry
python3 run_round.py --subject tree-beast 4
python3 score.py --round work/tree-beast/r4/round.json --scores work/tree-beast/r4/scores.json \
    --control base-tree --region horn=350,100,400,400 \
    --audit-sheet subjects/tree-beast/rounds/tb-r4-audit.jpg \
    --subject tree-beast -o subjects/tree-beast/rounds/tb-r4-review.md
python3 curate.py --period subjects/tree-beast/period-02 --from work/tree-beast/r4/round.json \
    --pick tree-horns=01-tree-horns --pick tree-horns-b=02-tree-horns-b \
    --control base-tree=controls/tree --note "…" --force
bash make_sheet.sh period subjects/tree-beast/period-02
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第二期【有角的树】交付 2 张（全部首选） | 小七 |
