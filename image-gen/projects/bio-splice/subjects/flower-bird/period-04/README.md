# 第四期 · 百合的绒与翎

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/fb2-r9-review.md)
> 引擎：Z-Image-Turbo　**1024×1280**　steps 12　**seed 11101 / 11103 / 11104**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**逆光 · 竖 1024×1280 · 换花种（玉兰 → 百合）**

本期唯一换**花种**的一期：百合的六枚反卷花瓣与玉兰的圆瓣形态完全不同，
逆光下花瓣与羽丝一起半透——**换个底座，同一句话就有了新画面**。

## 二、本期主题与结果

**底座 ＝ 白百合（腾出花蕊）**　**移植件 ＝ 绒羽 P5 + 翎羽 P6**

| 部位 | 落点 | 结果 |
|------|------|------|
| 翎羽 | 花轴 | ✅ 完整成立 |
| 绒羽 | 花心 | ✅ 成立 |

⚠️ **命中率随花种下降**（规律 102）：首轮（R7）两张只成一张，
补三个 seed（R9）才凑齐三张。**同一个写法在玉兰上是 5/5。**

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-lily-down-plume.png`](01-lily-down-plume.png) | **5.00** ✅ 首选 | `c66c6561` | `e83c12ed76` |
| 2 | [`02-lily-down-plume-c.png`](02-lily-down-plume-c.png) | **5.00** ✅ 首选 | `2d72e3bb` | `81ccfe2d64` |
| 3 | [`03-lily-down-plume-d.png`](03-lily-down-plume-d.png) | **5.00** ✅ 首选 | `9800df0a` | `5d171f38ff` |

对照：[`controls/flower.png`](controls/flower.png) —— **同轮**的纯百合底座。

## 四、本期验证

**规律 102：换底座要重新验命中率。** 「写法在 A 上验证过」不等于「在 B 上也稳」——
所以每换一次底座，第一轮都应当当成探针看待（命中后再补 take）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject flower-bird 9 --dry
python3 run_round.py --subject flower-bird 9
python3 score.py --round work/flower-bird/r9/round.json --scores work/flower-bird/r9/scores.json \
    --control base-flower --region axis=300,250,450,700 \
    --audit-sheet subjects/flower-bird/rounds/fb2-r9-audit.jpg \
    --subject flower-bird -o subjects/flower-bird/rounds/fb2-r9-review.md
python3 curate.py --period subjects/flower-bird/period-04 --from work/flower-bird/r9/round.json \
    --pick lily-down-plume=01-lily-down-plume --pick lily-down-plume-c=02-lily-down-plume-c \
    --pick lily-down-plume-d=03-lily-down-plume-d \
    --control base-flower=controls/flower --note "…" --force
bash make_sheet.sh period subjects/flower-bird/period-04
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第四期【百合的绒与翎】交付 3 张（换花种，命中率下降后补 take） | 小七 |
