# 第四期 · 藻层可见

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/lc-r4-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 8101 / 8102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**拟剖面 · 环形光 · 深景深 · 方**

藻层本来藏在地衣内部，是**最难看**的一期。于是干脆把呈现写成
「表层被掀开、露出内部结构」——剖面一旦成立，绿球与藻丝就**成了画面主角**。

## 二、本期主题与结果

**底座 ＝ 真菌菌丝体**　**移植件 ＝ 绿色藻细胞 AL1 + 藻丝 AL2（拟剖面）**

| 部位 | 编号 | 结果 |
|------|------|------|
| 绿色藻细胞 | AL1 | ✅ 完整成立：杯状剖面里铺满绿球 |
| 藻丝 | AL2 | ✅ 完整成立：细丝在绿球之间穿引 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-mycelium-algal-layer.png`](01-mycelium-algal-layer.png) | AL1+AL2（**主图**） | **5.00** ✅ 首选 | `dc6d41cb` | `cb9d81c1eb` |
| 2 | [`02-mycelium-algal-layer-b.png`](02-mycelium-algal-layer-b.png) | AL1+AL2（seed 8102） | **5.00** ✅ 首选 | `b5af9b8f` | `2af32f0c81` |

对照：[`controls/mycelium.png`](controls/mycelium.png) —— **同轮**的纯菌丝体底座。

## 四、本期验证

1. **呈现可以救弱期**（规律 94）：这一期在机制上属「内部结构／同材质」档，本该最难；
   换成拟剖面后两张都是 5.00。
2. 这说明**「看不见」常常是呈现问题，不是移植问题**——先改呈现，再考虑换部件。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject lichen 4 --dry
python3 run_round.py --subject lichen 4
python3 score.py --round work/lichen/r4/round.json --scores work/lichen/r4/scores.json \
    --control base-mycelium --region surface=200,200,620,620 \
    --audit-sheet subjects/lichen/rounds/lc-r4-audit.jpg \
    --subject lichen -o subjects/lichen/rounds/lc-r4-review.md
python3 curate.py --period subjects/lichen/period-04 --from work/lichen/r4/round.json \
    --pick mycelium-algal-layer=01-mycelium-algal-layer \
    --pick mycelium-algal-layer-b=02-mycelium-algal-layer-b \
    --control base-mycelium=controls/mycelium --note "…" --force
bash make_sheet.sh period subjects/lichen/period-04
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第四期【藻层可见】交付 2 张（拟剖面救弱期） | 小七 |
