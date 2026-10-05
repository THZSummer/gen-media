# 第四期 · 子座与孢子

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/cd-r6-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**seed 9101 / 9102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**雪线砾石 · 冷光 · 横 1280×1024**

往上走到雪线：砾石土面 + 残雪把画面压成冷调，
**冷光不抢质感**，正好让子座表面的粉状孢子读得出来。

## 二、本期主题与结果

**底座 ＝ 蛾幼虫**　**移植件 ＝ 单根子座 ST1 + 孢子 SP1**

| 部位 | 编号 | 结果 |
|------|------|------|
| 单根子座 | ST1 | ✅ 完整成立 |
| 孢子 | SP1 | ✅ 完整成立：子座表面覆着一层粉状孢子 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-larva-stroma-spores.png`](01-larva-stroma-spores.png) | ST1+SP1（**主图**） | **5.00** ✅ 首选 | `5c8af570` | `f44e867a64` |
| 2 | [`02-larva-stroma-spores-b.png`](02-larva-stroma-spores-b.png) | ST1+SP1（seed 9102） | **5.00** ✅ 首选 | `defa9e60` | `b2e4aa7d65` |

对照：[`controls/larva.png`](controls/larva.png) —— **同轮**的纯幼虫底座。

## 四、本期验证

1. 两件同体（子座 + 孢子）互不干扰：孢子只是**子座表面的属性**，
   不占额外位置——这与动物底座上"两件部件抢同一区域"完全不同。
2. 冷光 + 残雪把产地（雪线）交代清楚，是本期与期 02/03 的身份差别。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject cordyceps 6 --dry
python3 run_round.py --subject cordyceps 6
python3 score.py --round work/cordyceps/r6/round.json --scores work/cordyceps/r6/scores.json \
    --control base-larva --region body=300,250,680,500 \
    --audit-sheet subjects/cordyceps/rounds/cd-r6-audit.jpg \
    --subject cordyceps -o subjects/cordyceps/rounds/cd-r6-review.md
python3 curate.py --period subjects/cordyceps/period-04 --from work/cordyceps/r6/round.json \
    --pick larva-stroma-spores=01-larva-stroma-spores \
    --pick larva-stroma-spores-b=02-larva-stroma-spores-b \
    --control base-larva=controls/larva --note "…" --force
bash make_sheet.sh period subjects/cordyceps/period-04
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第四期【子座与孢子】交付 2 张（全部首选） | 小七 |
