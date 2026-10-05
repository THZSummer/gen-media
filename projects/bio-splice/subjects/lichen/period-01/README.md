# 第一期 · 壳状地衣

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/lc-r1-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**全 4 张同 seed 8101**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**岩面 · 侧光 · 微距平视 100mm · 方**

立题期：把「真菌 + 藻」这两半分别拍清楚，再拍它们合起来的样子。
岩面 + 掠射侧光把壳状面的每一条裂纹都挑出来。

> 本子主题的恒定层与动物子主题不同：**微距取景句 + `macro photograph, focus-stacked`**
> ——**尺度也是呈现层的一部分**（规律 93）。

## 二、本期主题与结果

**底座 ＝ 真菌菌丝体**　**移植件 ＝ 壳状形态 CR1 + 绿色藻细胞 AL1**

| 部位 | 编号 | 结果 |
|------|------|------|
| 壳状形态 | CR1 | ✅ 完整成立：龟裂的壳状壳，边缘放射 |
| 绿色藻细胞 | AL1 | ✅ **完整成立**：一簇簇鲜绿藻细胞嵌在菌丝之间 |
| 两件同体 | CR1+AL1 | ✅ 读作一枚完整的地衣，而不是拼贴 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-mycelium-crust.png`](01-mycelium-crust.png) | CR1（**主图**） | **5.00** ✅ 首选 | `3b2a1c5c` | `db31e693c6` |
| 2 | [`02-mycelium-algae.png`](02-mycelium-algae.png) | AL1 | **5.00** ✅ 首选 | `55365538` | `9d63662222` |
| 3 | [`03-mycelium-crust-algae.png`](03-mycelium-crust-algae.png) | CR1+AL1 | **5.00** ✅ 首选 | `488dbcbb` | `9c5d1ac97c` |

对照：[`controls/mycelium.png`](controls/mycelium.png) —— **同轮**的纯菌丝体底座（同 seed、同呈现、句式骨架相同）。

## 四、本期验证

1. **跨域供体第一次 100% 落地**：绿色藻细胞是跨界的件（藻 vs 真菌），本项目此前从没有跨域件完整成立过。
2. 原因在底座：**菌丝体是一团没有固定形状的东西**（规律 92）——模型没有「它应该长成什么」的先验来抵抗移植件。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject lichen 1 --dry
python3 run_round.py --subject lichen 1
python3 score.py --round work/lichen/r1/round.json --scores work/lichen/r1/scores.json \
    --control base-mycelium --region surface=200,200,620,620 \
    --audit-sheet subjects/lichen/rounds/lc-r1-audit.jpg \
    --subject lichen -o subjects/lichen/rounds/lc-r1-review.md
python3 curate.py --period subjects/lichen/period-01 --from work/lichen/r1/round.json \
    --pick mycelium-crust=01-mycelium-crust --pick mycelium-algae=02-mycelium-algae \
    --pick mycelium-crust-algae=03-mycelium-crust-algae \
    --control base-mycelium=controls/mycelium --note "…" --force
bash make_sheet.sh period subjects/lichen/period-01
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第一期【壳状地衣】交付 3 张（全部首选） | 小七 |
