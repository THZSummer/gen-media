# 第二期 · 单根子座

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/cd-r4-review.md)
> 引擎：Z-Image-Turbo　**1024×1280**　steps 12　**seed 9101 / 9102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**高山草甸 · 晨光 · 低机位微距 · 竖 1024×1280**

子座是**竖起来**的结构，所以用竖幅 + 贴地低机位看它的高度；
晨光与草叶给画面一个真实的产地感。

## 二、本期主题与结果

**底座 ＝ 蛾幼虫**　**移植件 ＝ 单根子座 ST1**

| 部位 | 编号 | 结果 |
|------|------|------|
| 单根子座 | ST1 | ✅ **完整成立**：一根棒状子座从虫体上拔起，冬虫夏草最标志性的那根「草」 |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-larva-stroma.png`](01-larva-stroma.png) | ST1（**主图**） | **5.00** ✅ 首选 | `378a77d6` | `aa2f01482e` |
| 2 | [`02-larva-stroma-b.png`](02-larva-stroma-b.png) | ST1（seed 9102） | **5.00** ✅ 首选 | `446977d1` | `7820e78aa3` |

对照：[`controls/larva.png`](controls/larva.png) —— **同轮**的纯幼虫底座。

## 四、本期验证

1. **子座一次就成**：空位新增（67）+ 不同形（91）+ 高辨识度（90）三条同时满足。
2. **它不需要承载结构**（规律 97）：从体表直接长出，只要有「体表」这个面就有落点——
   对比 dragon-nines 的鹰爪必须"先有四肢"。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject cordyceps 4 --dry
python3 run_round.py --subject cordyceps 4
python3 score.py --round work/cordyceps/r4/round.json --scores work/cordyceps/r4/scores.json \
    --control base-larva --region body=250,300,520,700 \
    --audit-sheet subjects/cordyceps/rounds/cd-r4-audit.jpg \
    --subject cordyceps -o subjects/cordyceps/rounds/cd-r4-review.md
python3 curate.py --period subjects/cordyceps/period-02 --from work/cordyceps/r4/round.json \
    --pick larva-stroma=01-larva-stroma --pick larva-stroma-b=02-larva-stroma-b \
    --control base-larva=controls/larva --note "…" --force
bash make_sheet.sh period subjects/cordyceps/period-02
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第二期【单根子座】交付 2 张（全部首选） | 小七 |
