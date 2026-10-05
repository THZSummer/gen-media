# 第五期 · 花鸟（收官）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/fb2-r8-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**seed 11101 / 11102**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**满枝 · 逆光 · 广角 45mm · 横幅 1280×1024**

收官不拍一朵，拍**一整枝**：春天的新枝上开着几朵花，
每朵的心里都立着一支羽翎，逆光下羽丝发亮——
这就是「花鸟」这个画科的字面意思。

## 二、本期主题与结果

**底座 ＝ 白兰花枝（玉兰）**　**移植件 ＝ 翎羽 P6 + 绒羽 P5**

| 部位 | 落点 | 结果 |
|------|------|------|
| 翎羽 | 花轴 | ✅ 完整成立（每朵都有） |
| 绒羽 | 花心 | ✅ 成立 |

## 三、成品

| # | 文件 | 评分 | prompt_id | sha256 |
|---|------|------|-----------|--------|
| 1 | [`01-flower-bird.png`](01-flower-bird.png) | **5.00** ✅ 首选 | `13c3bc2c` | `d9b4bd4738` |
| 2 | [`02-flower-bird-b.png`](02-flower-bird-b.png) | **5.00** ✅ 首选 | `319adc0c` | `f76d595e71` |

对照：[`controls/flower.png`](controls/flower.png) —— **同轮**的纯花枝。

## 四、本期验证

1. **满枝多朵同时成立**：同一句话在画面里的每一朵上都生效，没有"只有一朵长出来"的情况。
2. 收官期的意义在于**把这组机制结论收成一个形象**：
   花瓣换不掉（P1 0%）→ 于是让"鸟"从花心里长出来——**限制给出了更好的构图**（规律 104）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject flower-bird 8 --dry
python3 run_round.py --subject flower-bird 8
python3 score.py --round work/flower-bird/r8/round.json --scores work/flower-bird/r8/scores.json \
    --control base-flower --region axis=300,150,680,600 \
    --audit-sheet subjects/flower-bird/rounds/fb2-r8-audit.jpg \
    --subject flower-bird -o subjects/flower-bird/rounds/fb2-r8-review.md
python3 curate.py --period subjects/flower-bird/period-05 --from work/flower-bird/r8/round.json \
    --pick flower-bird=01-flower-bird --pick flower-bird-b=02-flower-bird-b \
    --control base-flower=controls/flower --note "…" --force
bash make_sheet.sh period subjects/flower-bird/period-05
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-05 | v0.1 | 第五期【花鸟】交付 2 张（收官） | 小七 |
