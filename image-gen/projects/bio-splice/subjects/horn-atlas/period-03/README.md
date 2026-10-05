# 第三部分 · 牛角

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ha-r3-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 14101 / 14102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**晨雾草场 · 顶光 · 平视 · 方**

本页改用**平顶光**：牛角是"粗壮、光滑、有角质环"的实心结构，
顶光把它的体积与基部环纹交代清楚，与鹿角（靠轮廓识别）正好互补。

## 二、本期主题与结果

**底座 ＝ 一匹无角的马**　**移植件 ＝ 粗壮牛角 H2**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 牛角 | H2 | 额顶（**空面**） | ✅ **完整成立** |

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-horse-oxhorns.png`](01-horse-oxhorns.png) | **5.00** ✅ 首选 | `b6b9275d` | `399a5c969a` |
| 2 | [`02-horse-oxhorns-b.png`](02-horse-oxhorns-b.png) | **5.00** ✅ 首选 | `2c6bbd3c` | `5583ca598f` |

对照：[`controls/horse.png`](controls/horse.png) —— **同轮**的纯马。

## 四、本期验证

**同一底座、同一片草场，只换角**——图鉴的"期内恒定、期间各异"在这里体现得最清楚：
底座与机位不动，**只让角与光线变化**，读起来就是同一册的相邻两页。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject horn-atlas 3 --dry
python3 run_round.py --subject horn-atlas 3
python3 score.py --round work/horn-atlas/r3/round.json --scores work/horn-atlas/r3/scores.json \
    --control base-horse --region head=350,80,400,400 \
    --audit-sheet subjects/horn-atlas/rounds/ha-r3-audit.jpg \
    --subject horn-atlas -o subjects/horn-atlas/rounds/ha-r3-review.md
python3 curate.py --period subjects/horn-atlas/period-03 --from work/horn-atlas/r3/round.json \
    --pick horse-oxhorns=01-horse-oxhorns --pick horse-oxhorns-b=02-horse-oxhorns-b \
    --control base-horse=controls/horse --note "…" --force
bash make_sheet.sh period subjects/horn-atlas/period-03
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第三部分【牛角】交付 2 张 | 小七 |
