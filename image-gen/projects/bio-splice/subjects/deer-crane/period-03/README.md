# 第三期 · 鹤尾的鹿

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/dc-r7-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 7101 起（多 take 见出处表）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**芦苇荡 · 逆光 · 平视 600mm · 方**

逆光把羽毛的半透质感打出来——这一期的主角是**羽毛扇**，只有逆光能一眼读出「这是鸟的羽」而不是鹿的毛。

> 呈现层**期内恒定**（该期所有镜头含对照共用一套），**期间各异**（五期各有身份）。

## 二、本期主题与结果

**底座 ＝ 鹿**　**移植件 ＝ 鹤的尾羽 G6（**真·空位**：鹿尾短到看不见）**

| 部位 | 编号 | 结果 |
|------|------|------|
| 尾羽 | G6 | ✅ **完整成立**：一圈白色羽扇从臀部长出，逆光下半透 |

但**命中率只有 1/4**：四个 seed（7101/7102/7103/7104）里只有 7101 长出了羽扇，其余三个臀部只有鹿自己的白斑。所以本期**只有 1 张成品**——宁可交一张，也不凑数。

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-deer-cranetait.png`](01-deer-cranetait.png) | G6（**主图**） | **5.00** ✅ 首选 | `96e6fe31` | `fc634c0383` |

对照：[`controls/deer.png`](controls/deer.png) —— **同轮**的纯鹿底座（同 seed、同呈现、句式骨架相同）。

## 四、本期验证

1. **空位是必要条件，不是充分条件**（规律 90）：尾位是全局唯一的「真空位」，命中率也只有 1/4。
2. 本件也是本子主题**唯一一眼看得出是移植件**的一件——因为羽扇与鹿身**不同形**（规律 91）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject deer-crane 7 --dry
python3 run_round.py --subject deer-crane 7
python3 score.py --round work/deer-crane/r7/round.json --scores work/deer-crane/r7/scores.json \
    --control base-deer --region tail=520,300,350,350 \
    --audit-sheet subjects/deer-crane/rounds/dc-r7-audit.jpg \
    --subject deer-crane -o subjects/deer-crane/rounds/dc-r7-review.md
python3 curate.py --period subjects/deer-crane/period-03 --from work/deer-crane/r7/round.json \
    --pick deer-cranetait=01-deer-cranetait \
    --control base-deer=controls/deer --note "…" --force
bash make_sheet.sh period subjects/deer-crane/period-03
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第三期【鹤尾的鹿】交付 1 张（完整成立，命中率 1/4） | 小七 |
