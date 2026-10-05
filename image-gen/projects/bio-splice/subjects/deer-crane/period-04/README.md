# 第四期 · 颈腿俱全

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/dc-r5-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**seed 7101 起（多 take 见出处表）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**霜晨草地 · 冷光 · 平视 · 横 1280×1024**

霜把草地压成一片冷白，鹿与它的部件成为画面里唯一的暖色；横幅把「修长的颈 + 细长的腿」这条竖向变化放进横向构图里。

> 呈现层**期内恒定**（该期所有镜头含对照共用一套），**期间各异**（五期各有身份）。

## 二、本期主题与结果

**底座 ＝ 鹿**　**移植件 ＝ 鹤颈 G1 + 鹤腿 G2（底座不写腿）**

| 部位 | 编号 | 结果 |
|------|------|------|
| 长颈 | G1 | ⚠️ 部分成立 |
| 细腿 | G2 | ⚠️ 部分成立 |
| 两件同体 | G1+G2 | ✅ 没有互相挤掉，也没有出现第二个个体 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-deer-neck-legs.png`](01-deer-neck-legs.png) | G1+G2（**主图**） | **4.25** ✅ 成品 | `39c69736` | `8eea44bee6` |
| 2 | [`02-deer-neck-legs-b.png`](02-deer-neck-legs-b.png) | G1+G2（seed 7102） | **4.25** ✅ 成品 | `8798278f` | `5756c5a9bc` |

对照：[`controls/deer.png`](controls/deer.png) —— **同轮**的纯鹿底座（同 seed、同呈现、句式骨架相同）。

## 四、本期验证

1. 跨区域叠加（颈在头侧、腿在下半身）成立，两件互不干扰（规律 59）。
2. 但两件各自都只到部分，所以合起来仍是「一只瘦长的鹿」——**叠加不能把部分变成完整**。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject deer-crane 5 --dry
python3 run_round.py --subject deer-crane 5
python3 score.py --round work/deer-crane/r5/round.json --scores work/deer-crane/r5/scores.json \
    --control base-deer --region neck=450,150,380,380 --region legs=420,600,420,380 \
    --audit-sheet subjects/deer-crane/rounds/dc-r5-audit.jpg \
    --subject deer-crane -o subjects/deer-crane/rounds/dc-r5-review.md
python3 curate.py --period subjects/deer-crane/period-04 --from work/deer-crane/r5/round.json \
    --pick deer-neck-legs=01-deer-neck-legs --pick deer-neck-legs-b=02-deer-neck-legs-b \
    --control base-deer=controls/deer --note "…" --force
bash make_sheet.sh period subjects/deer-crane/period-04
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第四期【颈腿俱全】交付 2 张（部分成立） | 小七 |
