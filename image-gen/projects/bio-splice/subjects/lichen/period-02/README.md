# 第二期 · 叶状地衣

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/lc-r2-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 8101 / 8102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**树皮 · 湿润 · 微距侧俯 · 方**

叶状地衣是**贴生**的，只有侧俯视角才能同时读出裂片的边缘与贴附方式；
湿润树皮给叶面一点反光。

## 二、本期主题与结果

**底座 ＝ 真菌菌丝体**　**移植件 ＝ 叶状体 FL1 + 藻丝 AL2**

| 部位 | 编号 | 结果 |
|------|------|------|
| 叶状体 | FL1 | ✅ 完整成立：裂片 + 浅色边缘，整体是一枚贴生的叶状地衣 |
| 藻丝 | AL2 | ✅ 成立：绿色细丝穿过叶面之间（比期 01 的藻细胞团细，故 A=4） |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-mycelium-foliose.png`](01-mycelium-foliose.png) | FL1（**主图**） | **5.00** ✅ 首选 | `66db4c27` | `248edfa2d2` |
| 2 | [`02-mycelium-foliose-algae.png`](02-mycelium-foliose-algae.png) | FL1+AL2 | **4.55** ✅ 首选 | `0e70ede1` | `8a9ba9bde6` |

对照：[`controls/mycelium.png`](controls/mycelium.png) —— **同轮**的纯菌丝体底座。

## 四、本期验证

1. 同一个底座上换一种形态（壳状 → 叶状）**同样一次就成**，形态件之间没有互相干扰。
2. **藻件的两种写法在可读性上有差别**：细胞团比细丝醒目（5.00 vs 4.55）——
   以后要展示「共生」优先用细胞团。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject lichen 2 --dry
python3 run_round.py --subject lichen 2
python3 score.py --round work/lichen/r2/round.json --scores work/lichen/r2/scores.json \
    --control base-mycelium --region surface=200,200,620,620 \
    --audit-sheet subjects/lichen/rounds/lc-r2-audit.jpg \
    --subject lichen -o subjects/lichen/rounds/lc-r2-review.md
python3 curate.py --period subjects/lichen/period-02 --from work/lichen/r2/round.json \
    --pick mycelium-foliose=01-mycelium-foliose --pick mycelium-foliose-algae=02-mycelium-foliose-algae \
    --control base-mycelium=controls/mycelium --note "…" --force
bash make_sheet.sh period subjects/lichen/period-02
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第二期【叶状地衣】交付 2 张 | 小七 |
