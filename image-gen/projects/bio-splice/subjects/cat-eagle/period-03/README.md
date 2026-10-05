# 第三期 · 有翅的猫

> 返回[子主题](../README.md) ｜ [项目首页](../../../README.md) ｜ [部位表](../parts.md) ｜ [复核报告](../rounds/r15-review.md)
> 引擎：Z-Image-Turbo　**1024×1280**　steps 12　**全 4 张共用 seed 4201**（含同轮底座对照）
> 速览图：[`sheet.jpg`](sheet.jpg)　出处：[`manifest.json`](manifest.json)

---

## 一、本期特点（呈现）

**雨后林地 · 逆光 · 广角低机位翼展 · 竖 1024×1280**

本期主角是**翼**，需要一次完整的张翼姿态才看得清结构，所以用**广角低机位**在翼展瞬间拍；雨后林地的逆光把每一根羽枝勾出来——全子主题里最「野生动物纪录片」的一张。

> 呈现层是**期内恒定**的：本轮所有镜头（含底座对照）共用同一生境/光线/机位/画布，
> 所以「移植 vs 底座」的对照仍然干净。**期间各异**——五期各有身份，见
> [子主题首页](../README.md) 的期风格表。

## 二、本期主题与结果

**底座 ＝ 猫**（弱物种）　**移植件 ＝ 鹰的局部件**

| 部位 | 编号 | 结果 |
|------|------|------|
| 鹰翼 | E2 | ✅ 猫展开一对完整的鹰翼 |
| 鹰尾羽 | E5 | ✅ 尾根长出扇形尾羽（略直，可信度稍降） |
| 鹰翼 + 鹰尾羽 | E2+E5 | ✅ 两处同时成立（**主图**） |

## 三、成品

| # | 文件 | 移植部位 | 评分 | prompt_id | sha256 |
|---|------|----------|------|-----------|--------|
| 1 | [`01-cat-eagle-wings.png`](01-cat-eagle-wings.png) | E2 鹰翼（**主图**） | **5.00** ✅ 首选 | `34dd732b` | `6824a52ef7` |
| 2 | [`02-cat-eagle-tail.png`](02-cat-eagle-tail.png) | E5 鹰尾羽 | **4.35** ✅ 成品 | `c5cf8636` | `b0e4ee59ee` |
| 3 | [`03-cat-eagle-wings-tail.png`](03-cat-eagle-wings-tail.png) | E2+E5 | **4.80** ✅ 首选 | `10a04abd` | `eb152c4f9d` |

对照：[`controls/cat.png`](controls/cat.png) —— **同轮**的纯猫底座（同 seed、同呈现、句式骨架相同），
本轮所有客观指标都是与它比出来的。

## 四、本期验证

1. **姿态句必须对目标部位保持沉默**：R11 的姿态写成「它把两翼张开到最大」，结果**连底座对照都长出了鹰翼**——对照被污染，整轮客观指标作废；改成「它正要落定、全身展开」后，对照恢复为无翼的猫（规律 79）。
2. 张翼姿态反而**提高**了翼的可读性：逆光下羽枝根根分明，是「机位冲着主体去」的又一个正例（规律 71）。

## 五、如何复现

```bash
cd ../../..
python3 run_round.py --subject cat-eagle 15 --dry
python3 run_round.py --subject cat-eagle 15
python3 score.py --round work/cat-eagle/r15/round.json --scores work/cat-eagle/r15/scores.json \
    --control base-cat --region wings=140,120,760,480 --region rear=380,600,300,500 \
    --audit-sheet subjects/cat-eagle/rounds/r15-audit.jpg \
    --subject cat-eagle -o subjects/cat-eagle/rounds/r15-review.md
python3 curate.py --period subjects/cat-eagle/period-03 --from work/cat-eagle/r15/round.json \
    --pick c-eagle-wings=01-cat-eagle-wings --pick c-eagle-tail=02-cat-eagle-tail \
    --pick c-eagle-wings-tail=03-cat-eagle-wings-tail \
    --control base-cat=controls/cat.png --note "…" --force
bash make_sheet.sh period subjects/cat-eagle/period-03
```

---

## 文档修订记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2026-10-04 | v0.1 | 第二期交付：猫耳 / 猫尾 / 耳+尾 共 3 张（原呈现＝秋日草甸） | 小七 |
| 2026-10-04 | **v0.2** | **呈现重做**：姿态句去掉「两翼张开」（它污染了底座对照）；改用逆光广角低机位拍翼展瞬间 | 小七 |
