# 第3期 · 翎绒俱全

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/fb2-r6-review.md)
> 引擎：Z-Image-Turbo　**1024×1024**　steps 12
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**暗背景·硬光·方**

## 二、本期主题与结果

**底座 ＝ 大花**　**移植件 ＝ P6+P5**

见 [parts.md](../parts.md) 的落点分析：P6 落在**花轴**（表面，不需要承载结构），
P5 落在**花心**（腾出花蕊后是半空面）。

## 三、成品

评分 **5.00×2**（全部 ✅ 首选）。详见 [`manifest.json`](manifest.json)：
每张都记录了来源轮次、镜头名、seed、prompt 原文与 sha256。

对照：[`controls/flower.png`](controls/flower.png) —— **同轮**的纯花底座。

## 四、复现

```bash
cd ../../..
python3 run_round.py --subject flower-bird r6 --dry
python3 run_round.py --subject flower-bird r6
python3 score.py --round work/flower-bird/rr6/round.json --scores work/flower-bird/rr6/scores.json \
    --control base-flower --audit-sheet subjects/flower-bird/rounds/fb2-r6-audit.jpg \
    --subject flower-bird -o subjects/flower-bird/rounds/fb2-r6-review.md
bash make_sheet.sh period subjects/flower-bird/period-03
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第3期交付 | 小七 |
