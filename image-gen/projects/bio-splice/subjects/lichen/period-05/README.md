# 第五期 · 共生体（收官）

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/lc-r5-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**seed 8101 / 8102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**雾林 · 散射光 · 广角 · 横幅 1280×1024**

收官回到本源：**一株地衣本来就可以同时有叶状与枝状结构**。
雾林散射光没有硬阴影，把这枚「复合体」的层次一次交代清楚。

## 二、本期主题与结果

**底座 ＝ 真菌菌丝体**　**移植件 ＝ 三种形态（壳／叶／枝）± 绿色藻细胞**

| 部位 | 编号 | 结果 |
|------|------|------|
| 三种形态 | CR1+FL1+FR1 | ✅ 叶状裂片 + 枝状分叉长在同一个体上 |
| 形态 + 藻 | FL1+FR1+AL1 | ✅ 复合形态之外，绿色藻细胞嵌在缝隙里 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-mycelium-3forms.png`](01-mycelium-3forms.png) | 三种形态（**主图**） | **5.00** ✅ 首选 | `125acdd7` | `694e593ffe` |
| 2 | [`02-mycelium-forms-algae.png`](02-mycelium-forms-algae.png) | 形态 + 藻 | **4.55** ✅ 首选 | `65a78031` | `d036280d0b` |

对照：[`controls/mycelium.png`](controls/mycelium.png) —— **同轮**的纯菌丝体底座。

## 四、本期验证

1. **三种形态叠加在一个个体上没有互相挤掉**——对这类「没有固定形状」的底座，
   规律 59（同区域 ≤2）也不适用：它本来就没有「区域」可分。
2. 收官图给人的感觉是「一枚真实的复合地衣」，而不是「三种地衣拼在一起」。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject lichen 5 --dry
python3 run_round.py --subject lichen 5
python3 score.py --round work/lichen/r5/round.json --scores work/lichen/r5/scores.json \
    --control base-mycelium --region surface=300,150,680,700 \
    --audit-sheet subjects/lichen/rounds/lc-r5-audit.jpg \
    --subject lichen -o subjects/lichen/rounds/lc-r5-review.md
python3 curate.py --period subjects/lichen/period-05 --from work/lichen/r5/round.json \
    --pick mycelium-3forms=01-mycelium-3forms --pick mycelium-forms-algae=02-mycelium-forms-algae \
    --control base-mycelium=controls/mycelium --note "…" --force
bash make_sheet.sh period subjects/lichen/period-05
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第五期【共生体】交付 2 张（收官） | 小七 |
