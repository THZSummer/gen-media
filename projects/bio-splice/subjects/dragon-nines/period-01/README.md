# 第一期 · 有角的蛇

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/dn-r1-review.md)
> 引擎：Z-Image-Turbo　1024×1024　steps 12　**全 3 张共用 seed 4201**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期主题

九似里的第一项、也是龙**最强的标志**：**角似鹿（D1）**。

底座 = **蛇**（「项似蛇」即身体主轴）

| 部位 | 编号 | 结果 |
|------|------|------|
| 鹿角 | D1 | ✅ 分叉鹿角从颅骨自然长出，**一眼读作龙** |
| 鹿角 + 牛耳 | D1+D9 | ✅ 两者同时在位（**同区域两处**，规律 59 的上限内） |

## 二、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-snake-antler.png`](01-snake-antler.png) | D1 鹿角（**主图**） | **5.00** ✅ 首选 | `156422e9` | `dc000f115c` |
| 2 | [`02-snake-antler-ox-ear.png`](02-snake-antler-ox-ear.png) | D1+D9 | **4.65** ✅ 首选 | `30dc0dfd` | `1a7924340d` |

对照：[`controls/snake.png`](controls/snake.png) —— 未移植的纯蛇底座（同轮同 seed）。

## 三、本期排除的一张

`snake-antler-claw`（D1 鹿角 + D7 鹰爪）**未纳入**：鹿角成立，但**鹰爪完全没出现**。

原因不是被底座描述覆盖，而是蛇**没有四肢**——爪**无处可长**。
这条发现直接改变了后续期规划（见[子主题 README](../README.md) §三），
第二期因此换成蜥蜴底座。

## 四、如何复现

```bash
cd ../../..
python3 run_round.py --subject dragon-nines 1 --dry
python3 run_round.py --subject dragon-nines 1
python3 score.py --round work/dragon-nines/r1/round.json --scores work/dragon-nines/r1/scores.json --control base-snake \
    --region head=430,120,380,260 --region body=380,560,520,420 \
    --audit-sheet subjects/dragon-nines/rounds/dn-r1-audit.jpg \
    -o subjects/dragon-nines/rounds/dn-r1-review.md
python3 curate.py --period subjects/dragon-nines/period-01 --from work/dragon-nines/r1/round.json \
    --pick snake-antler=01-snake-antler \
    --pick snake-antler-oxear=02-snake-antler-ox-ear \
    --control base-snake=controls/snake --note "…" --force
bash make_sheet.sh period subjects/dragon-nines/period-01
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第一期交付：鹿角 / 鹿角+牛耳 共 2 张 | 小七 |
