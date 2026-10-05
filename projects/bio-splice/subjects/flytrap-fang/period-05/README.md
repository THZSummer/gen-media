# 第五期 · 食肉植物（收官）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ff-r7-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**seed 10101 / 10102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**晨雾沼泽 · 逆光 · 广角 45mm · 横幅 1280×1024**

收官不拍单株，拍**一整丛**：晨雾 + 逆光让每一片红色内面都亮起来，
广角横幅把"一片食肉植物"的气势交代出来。

## 二、本期主题与结果

**底座 ＝ 捕蝇草（宽叶面版）**　**移植件 ＝ 兽牙 T1 + 眼 T2 + 舌 T4**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 兽牙 | T1 | 夹子边缘 | ✅ |
| 眼 | T2 | 叶面 | ✅（这一张里较小，不如期 02 醒目） |
| 舌 | T4 | 夹子内腔 | ✅ |
| 三件同体 | 全部 | 三个不同的面 | ✅ 读作一丛**长着眼睛、张着嘴的植物** |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-flytrap-all3.png`](01-flytrap-all3.png) | T1+T2+T4（**主图**） | **5.00** ✅ 首选 | `517319cd` | `d1dbf9cbc7` |
| 2 | [`02-flytrap-all3-b.png`](02-flytrap-all3-b.png) | T1+T2+T4（seed 10101） | **4.55** ✅ 首选 | `e796d791` | `0af2711e81` |

对照：[`controls/flytrap.png`](controls/flytrap.png) —— **同轮**的纯捕蝇草丛。

## 四、本期验证

1. **三件落在三个不同的面上**（边缘 / 叶面 / 内腔），所以叠加没有互相挤掉——
   又一次验证「约束的自变量是区域（面）分布，不是件数」（规律 59/68/99）。
2. 第二张（`-b`）里眼在叶面上偏小、可读性稍弱，如实给 4.55。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject flytrap-fang 7 --dry
python3 run_round.py --subject flytrap-fang 7
python3 score.py --round work/flytrap-fang/r7/round.json --scores work/flytrap-fang/r7/scores.json \
    --control base-flytrap --region lobe=300,150,680,600 \
    --audit-sheet subjects/flytrap-fang/rounds/ff-r7-audit.jpg \
    --subject flytrap-fang -o subjects/flytrap-fang/rounds/ff-r7-review.md
python3 curate.py --period subjects/flytrap-fang/period-05 --from work/flytrap-fang/r7/round.json \
    --pick flytrap-all3-b=01-flytrap-all3 --pick flytrap-all3=02-flytrap-all3-b \
    --control base-flytrap=controls/flytrap --note "…" --force
bash make_sheet.sh period subjects/flytrap-fang/period-05
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第五期【食肉植物】交付 2 张（收官） | 小七 |
