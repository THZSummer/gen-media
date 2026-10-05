# 第五期 · 鹿鹤同春（收官）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/dc-r6-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**seed 7101 起（多 take 见出处表）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**春日梅林 · 柔散光 · 广角 · 横幅 1280×1024**

回到纹样本身：**春日花树下的鹿**是「鹿鹤同春」的经典构图，柔散光与飘落的花瓣给收官期一个「吉祥图案」的气口。

> 呈现层**期内恒定**（该期所有镜头含对照共用一套），**期间各异**（五期各有身份）。

## 二、本期主题与结果

**底座 ＝ 鹿**　**移植件 ＝ 鹤颈 G1 + 鹤腿 G2 + 鹤尾羽 G6（底座不写腿尾）**

| 部位 | 编号 | 结果 |
|------|------|------|
| 长颈 | G1 | ⚠️ 部分 |
| 细腿 | G2 | ⚠️ 部分 |
| 尾羽 | G6 | ✅ 完整（本期两个 seed 都有羽扇） |
| 三件同体 | G1+G2+G6 | ✅ 一只个体，没有第二只 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-deer-crane-3parts.png`](01-deer-crane-3parts.png) | G1+G2+G6（**主图**） | **4.25** ✅ 成品 | `03f3fa4b` | `510077639c` |
| 2 | [`02-deer-crane-3parts-b.png`](02-deer-crane-3parts-b.png) | G1+G2+G6（seed 7102） | **4.25** ✅ 成品 | `1e147177` | `2a0a716d2d` |

对照：[`controls/deer.png`](controls/deer.png) —— **同轮**的纯鹿底座（同 seed、同呈现、句式骨架相同）。

## 四、本期验证

1. **收官期如实标注「同体只算半个」**：三处部件都在，但颈与腿只到部分，整只读起来仍偏「瘦长的鹿」。
2. 这是本项目**唯一一个平均分没到 4.5 的子主题**——原因在供体选择：颈/腿与底座**同形**，改形不改质（规律 91）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject deer-crane 6 --dry
python3 run_round.py --subject deer-crane 6
python3 score.py --round work/deer-crane/r6/round.json --scores work/deer-crane/r6/scores.json \
    --control base-deer --region neck=450,150,380,380 --region legs=420,600,420,380 \
    --audit-sheet subjects/deer-crane/rounds/dc-r6-audit.jpg \
    --subject deer-crane -o subjects/deer-crane/rounds/dc-r6-review.md
python3 curate.py --period subjects/deer-crane/period-05 --from work/deer-crane/r6/round.json \
    --pick deer-crane-3parts=01-deer-crane-3parts --pick deer-crane-3parts-b=02-deer-crane-3parts-b \
    --control base-deer=controls/deer --note "…" --force
bash make_sheet.sh period subjects/deer-crane/period-05
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第五期【鹿鹤同春】交付 2 张（收官，部分成立为主） | 小七 |
