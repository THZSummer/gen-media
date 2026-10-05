# 第二部分 · 四翼（膜）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/wa-r2-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 13101 / 13102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**枝头 · 顶光 · 方**

图鉴第二页：**背上多出一对昆虫膜翅**。顶光让半透明的膜面透亮、
翅脉在光下成网格——这是"膜翅"与鸟自身羽翼最直观的材质差别。

## 二、本期主题与结果

**底座 ＝ 中型鸟（保留原翼）**　**移植件 ＝ 昆虫膜翅 W2**

| 部位 | 编号 | 落点 | 结果 |
|------|------|------|------|
| 昆虫膜翅 | W2 | 背部（**空面**） | ✅ **完整成立**：一对半透膜翅从背上生出 |

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-bird-membrane.png`](01-bird-membrane.png) | **5.00** ✅ 首选 | `9a71f344` | `f829f76dc8` |
| 2 | [`02-bird-membrane-b.png`](02-bird-membrane-b.png) | **5.00** ✅ 首选 | `7e64c765` | `77266258c2` |

对照：[`controls/bird.png`](controls/bird.png) —— **同轮**的纯鸟（第一部分那只的同一规格版）。

## 四、本期验证

1. **两条门槛都过**（规律 105）：落点是背部空面；供体**本身就是翅**（规律 107）。
2. 膜翅与羽翼**不同形**（规律 91）+ 高辨识度（规律 90）→ 一眼可辨"多了一对"。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject wing-atlas 2 --dry
python3 run_round.py --subject wing-atlas 2
python3 score.py --round work/wing-atlas/r2/round.json --scores work/wing-atlas/r2/scores.json \
    --control base-bird --region back=250,200,550,500 \
    --audit-sheet subjects/wing-atlas/rounds/wa-r2-audit.jpg \
    --subject wing-atlas -o subjects/wing-atlas/rounds/wa-r2-review.md
python3 curate.py --period subjects/wing-atlas/period-02 --from work/wing-atlas/r2/round.json \
    --pick bird-membrane=01-bird-membrane --pick bird-membrane-b=02-bird-membrane-b \
    --control base-bird=controls/bird --note "…" --force
bash make_sheet.sh period subjects/wing-atlas/period-02
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第二部分【四翼（膜）】交付 2 张 | 小七 |
