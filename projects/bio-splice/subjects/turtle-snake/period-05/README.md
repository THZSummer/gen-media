# 第五期 · 玄武（收官）

> 🌐 语言：**中文** ｜ [English](README.en.md)

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ts-r6-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**全 3 张共用 seed 5101（另加 5102/5103 的 take）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**暮色水面 · 逆光剪影 · 平视广角 35mm · 横幅 1280×1024**

收官期直接把**颈 + 尾 + 缠体三件**放到同一只龟上，并给玄武一个它该有的场景：暮色水面、逆光、宽阔的横幅，水里的倒影与主体的剪影合成一个完整的四象形象。

> 呈现层**期内恒定**：本轮所有镜头（含底座对照）共用同一生境/光线/机位/画布，
> 所以「移植 vs 底座」的对照干净；**期间各异**，五期各有身份。

## 二、本期主题与结果

**底座 ＝ 龟**　**移植件 ＝ 蛇颈 N1 + 蛇尾 N2 + 缠体 N3**

| 部位 | 编号 | 结果 |
|------|------|------|
| 蛇颈 | N1 | ✅ |
| 蛇尾 | N2 | ✅ |
| 缠体 | N3 | ✅ 盘在壳前/壳侧 |
| 三件同体 | N1+N2+N3 | ✅ **一只个体，没有第二只** |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-turtle-xuanwu.png`](01-turtle-xuanwu.png) | N1+N2+N3（**主图**） | **5.00** ✅ 首选 | `707c87f7` | `78ef41eb7c` |
| 2 | [`02-turtle-xuanwu-coiled.png`](02-turtle-xuanwu-coiled.png) | N1+N2+N3（seed 5102） | **5.00** ✅ 首选 | `d267d6c0` | `c76b0f0f04` |

对照：[`controls/turtle.png`](controls/turtle.png) —— **同轮**的纯龟底座（同 seed、同呈现、句式骨架相同），
本轮所有客观指标都是与它比出来的。

## 四、本期验证

1. **「玄武」成立**：蛇颈抬起、长尾拖出、蛇身盘在壳上，读作一个合体形象而不是「龟身上贴了三条蛇」。
2. 三处分属头颈 / 壳 / 尾三个区域——再一次验证**约束的自变量是区域分布，不是件数**（规律 68）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject turtle-snake 6 --dry
python3 run_round.py --subject turtle-snake 6
python3 score.py --round work/turtle-snake/r6/round.json --scores work/turtle-snake/r6/scores.json \
    --control base-turtle --region neck=400,150,300,300 --region coil=520,300,420,300 \
    --audit-sheet subjects/turtle-snake/rounds/ts-r6-audit.jpg \
    --subject turtle-snake -o subjects/turtle-snake/rounds/ts-r6-review.md
python3 curate.py --period subjects/turtle-snake/period-05 --from work/turtle-snake/r6/round.json \
    --pick turtle-all3=01-turtle-xuanwu \
    --pick turtle-all3-b=02-turtle-xuanwu-coiled \
    --control base-turtle=controls/turtle --note "…" --force
bash make_sheet.sh period subjects/turtle-snake/period-05
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第五期【玄武】交付 2 张：颈+尾+缠体三件同体 | 小七 |
