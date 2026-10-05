# 第三期 · 多根子座

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/cd-r5-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12　**seed 9101 / 9102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**高山草甸 · 逆光 · 方**

与第二期同一片草甸、同一个部件家族，只把光线换成**强逆光**：
子座半透，顶端发亮，靠"光的形状"把多根子座的层次分开。

## 二、本期主题与结果

**底座 ＝ 蛾幼虫**　**移植件 ＝ 多根子座 ST1x**

| 部位 | 编号 | 结果 |
|------|------|------|
| 多根子座 | ST1x | ✅ **完整成立**：四根子座同时从虫体拔出（另一个 seed 是带伞状顶端的一小丛） |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-larva-stromata.png`](01-larva-stromata.png) | ST1x（**主图**） | **5.00** ✅ 首选 | `46c83411` | `3b5c8aa39d` |
| 2 | [`02-larva-stromata-b.png`](02-larva-stromata-b.png) | ST1x（seed 9102） | **5.00** ✅ 首选 | `e1ac376a` | `80f7140cc9` |

对照：[`controls/larva.png`](controls/larva.png) —— **同轮**的纯幼虫底座。

## 四、本期验证

1. **"多根"同样不成问题**：这类"从体表长出的件"，数量不是一个约束
   （对比动物底座上的"同区域 ≤2"，规律 59 在这里不适用——虫体表面本来就是一个连续的面）。
2. 逆光把子座的半透质感打了出来，是本期与第二期最主要的差别。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject cordyceps 5 --dry
python3 run_round.py --subject cordyceps 5
python3 score.py --round work/cordyceps/r5/round.json --scores work/cordyceps/r5/scores.json \
    --control base-larva --region body=200,250,620,550 \
    --audit-sheet subjects/cordyceps/rounds/cd-r5-audit.jpg \
    --subject cordyceps -o subjects/cordyceps/rounds/cd-r5-review.md
python3 curate.py --period subjects/cordyceps/period-03 --from work/cordyceps/r5/round.json \
    --pick larva-stromata=01-larva-stromata --pick larva-stromata-b=02-larva-stromata-b \
    --control base-larva=controls/larva --note "…" --force
bash make_sheet.sh period subjects/cordyceps/period-03
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第三期【多根子座】交付 2 张（全部首选） | 小七 |
