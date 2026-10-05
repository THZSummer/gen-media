# 第四期 · 颈尾俱全

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/ts-r5-review.md)
> 引擎：Z-Image-Turbo　**1280×1024**　steps 12　**全 3 张共用 seed 5101（另加 5102/5103 的 take）**
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**雨后溪石 · 逆光 · 平视 400mm · 横 1280×1024**

一件一件验完，本期把**颈与尾同时**放上去，并用横幅把首尾两端收进同一画面；逆光把两条蛇形轮廓勾在天光上，正好检验它们**互不干扰**。

> 呈现层**期内恒定**：本轮所有镜头（含底座对照）共用同一生境/光线/机位/画布，
> 所以「移植 vs 底座」的对照干净；**期间各异**，五期各有身份。

## 二、本期主题与结果

**底座 ＝ 龟**　**移植件 ＝ 蛇颈 N1 + 蛇尾 N2**

| 部位 | 编号 | 结果 |
|------|------|------|
| 蛇颈 | N1 | ✅ 完整成立 |
| 蛇尾 | N2 | ✅ 完整成立 |
| 两件同体 | N1+N2 | ✅ **没有互相挤掉**，也没有出现第二个个体 |

颈在头侧、尾在壳后，分属两个区域——这正是规律 59（同区域 ≤2、跨区域可叠加）预期应当成立的情形。

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-turtle-neck-tail.png`](01-turtle-neck-tail.png) | N1+N2（**主图**） | **5.00** ✅ 首选 | `6656eff3` | `adb819cfb0` |
| 2 | [`02-turtle-neck-tail-b.png`](02-turtle-neck-tail-b.png) | N1+N2（seed 5102） | **5.00** ✅ 首选 | `1f3237a5` | `717c3ce298` |

对照：[`controls/turtle.png`](controls/turtle.png) —— **同轮**的纯龟底座（同 seed、同呈现、句式骨架相同），
本轮所有客观指标都是与它比出来的。

## 四、本期验证

1. **跨区域叠加在两个 seed 下都成立**：单件验证过的部件，叠加时只要区域不冲突就稳（规律 69）。
2. 逆光并没有把鳞列吃掉——**实体部件扛得住逆光**（与细线部件不同，见 cat-eagle 的胡须期）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject turtle-snake 5 --dry
python3 run_round.py --subject turtle-snake 5
python3 score.py --round work/turtle-snake/r5/round.json --scores work/turtle-snake/r5/scores.json \
    --control base-turtle --region neck=380,150,340,300 --region tail=620,350,420,300 \
    --audit-sheet subjects/turtle-snake/rounds/ts-r5-audit.jpg \
    --subject turtle-snake -o subjects/turtle-snake/rounds/ts-r5-review.md
python3 curate.py --period subjects/turtle-snake/period-04 --from work/turtle-snake/r5/round.json \
    --pick turtle-neck-tail=01-turtle-neck-tail \
    --pick turtle-neck-tail-b=02-turtle-neck-tail-b \
    --control base-turtle=controls/turtle --note "…" --force
bash make_sheet.sh period subjects/turtle-snake/period-04
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第四期【颈尾俱全】交付 2 张 | 小七 |
